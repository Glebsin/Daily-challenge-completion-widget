import sys
import os
from datetime import datetime, timezone
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QAction, QDesktopWidget
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QTimer, QPoint
from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEngineProfile, QWebEngineView
from autostart_utils import add_to_startup_registry, remove_from_startup_registry, is_in_startup_registry
from context_menu_processing import NoSelectWebEngineView, MouseMoveMixin
from streak_utils import UPDATE_INTERVALS, update_streak, update_osu_settings
from context_menu import createContextMenu, mousePressEvent
from widget_keyevents import handle_key_press
from saveload_settings_utils import load_settings, save_settings as utils_save_settings
from popup_template import HTML_POPUP_TEMPLATE

class Widget(QMainWindow, MouseMoveMixin):
    def __init__(self):
        super().__init__()
        self.debug_border = False
        self.enable_logging = False if getattr(sys, 'frozen', False) else False

        if getattr(sys, 'frozen', False):
            self.settings_file = os.path.join(os.path.dirname(sys.executable), "widget_settings.json")
        else:
            self.settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "widget_settings.json")

        self.settings = load_settings(self.settings_file, self.enable_logging)
        self.scale = self.settings.get('scale', 100)
        self.base_width = 160
        self.base_height = 57
        current_width = int(self.base_width * (self.scale / 100))
        current_height = int(self.base_height * (self.scale / 100))

        flags = Qt.FramelessWindowHint | Qt.Tool
        if self.settings.get('always_on_top', True):
            flags |= Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.setFixedSize(current_width, current_height)

        pos = self.settings.get('position', {'x': 100, 'y': 100})
        screens = QApplication.screens()
        valid_position = False
        for screen in screens:
            screen_geo = screen.geometry()
            x, y = pos.get('x', 0), pos.get('y', 0)
            if (x >= screen_geo.x() and
                x + current_width <= screen_geo.x() + screen_geo.width() and
                y >= screen_geo.y() and
                y + current_height <= screen_geo.y() + screen_geo.height()):
                valid_position = True
                break
        if valid_position:
            self.move(pos['x'], pos['y'])
        else:
            center = QApplication.primaryScreen().geometry().center()
            self.move(center.x() - current_width // 2, center.y() - current_height // 2)
        self.oldPos = self.pos()

        self.osu_client_id = self.settings.get('osu_client_id', '')
        self.osu_client_secret = self.settings.get('osu_client_secret', '')
        self.osu_username = self.settings.get('osu_username', '')

        self.key_sequence = []
        self.always_on_top = self.settings.get('always_on_top', True)
        self.enable_logging = False if getattr(sys, 'frozen', False) else self.settings.get('enable_logging', False)

        self.open_context_menu = None
        self.menu_time_action = None
        self.menu_time_timer = QTimer(self)
        self.menu_time_timer.setInterval(1000)
        self.menu_time_timer.timeout.connect(self.update_menu_time_action)

        self.tray_time_action = None
        self.tray_time_timer = QTimer(self)
        self.tray_time_timer.setInterval(1000)
        self.tray_time_timer.timeout.connect(self.update_tray_time_action)

        if getattr(sys, 'frozen', False) and self.settings.get('autostart', True):
            add_to_startup_registry()

        self.animation = None
        self.snap_distance = 10
        self.arrow_step = 2
        self.last_update_time = None
        self.update_interval = self.settings.get('update_interval', UPDATE_INTERVALS[0][0])

        self.tray_icon = None
        self.tray_menu = None
        self.init_tray_icon()

        self.popup = None

        self.initUI()
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.on_update_timer)
        self.restart_update_timer()

        self.cursor_check_timer = QTimer(self)
        self.cursor_check_timer.setInterval(100)
        self.cursor_check_timer.timeout.connect(self.check_cursor_over_widget)
        self.cursor_check_timer.start()
        self._popup_visible = False

    def check_cursor_over_widget(self):
        global_mouse_pos = QCursor.pos()
        widget_rect = QRect(self.mapToGlobal(QPoint(0, 0)), self.size())
        if widget_rect.contains(global_mouse_pos):
            if not self._popup_visible:
                self.show_popup()
                self._popup_visible = True
        else:
            if self._popup_visible:
                self.hide_popup()
                self._popup_visible = False

    def init_tray_icon(self):
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DCCW.ico')
        icon = QIcon(icon_path)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(icon)
        self.tray_icon.setToolTip("DCCW")
        self.update_tray_menu()
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()

    def update_tray_menu(self):
        tray_menu = QMenu()
        tray_menu.setStyleSheet("""
            QMenu {
                background-color: #2D2D2D;
                color: white;
                border: 1px solid #3D3D3D;
                padding: 5px;
            }
            QMenu::item {
                background-color: transparent;
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: #3D3D3D;
            }
            QMenu::item:disabled {
                color: #808080;
            }
            QMenu::item:disabled:selected {
                background-color: transparent;
            }
            QMenu::indicator {
                width: 15px;
                height: 15px;
            }
            QMenu::indicator:checked {
                background: #4CAF50;
            }
            QLabel {
                color: white;
                padding: 2px 0;
            }
            QWidget {
                background-color: #2D2D2D;
            }
        """)

        if not self.always_on_top:
            show_action = QAction("Show", self)
            show_action.triggered.connect(self.show_from_tray)
            tray_menu.addAction(show_action)

        if self.last_update_time:
            local_update_time = self.last_update_time.astimezone()
            update_str = local_update_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            update_str = "-"
        tray_time_action = QAction(f'Updated: {update_str}', self)
        tray_time_action.setEnabled(False)
        tray_menu.addAction(tray_time_action)
        self.tray_time_action = tray_time_action
        self.tray_time_timer.start()

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_menu = tray_menu

    def update_tray_time_action(self):
        if self.tray_time_action:
            if self.last_update_time:
                local_update_time = self.last_update_time.astimezone()
                update_str = local_update_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                update_str = "-"
            self.tray_time_action.setText(f'Updated: {update_str}')

    def show_from_tray(self):
        if not self.always_on_top:
            self.showNormal()
            self.activateWindow()
            self.raise_()

    def toggle_always_on_top(self):
        self.always_on_top = not self.always_on_top
        flags = Qt.FramelessWindowHint | Qt.Tool
        if self.always_on_top:
            flags |= Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        current_pos = self.pos()
        self.show()
        self.move(current_pos)
        self.save_settings()
        self.update_tray_menu()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            if self.isVisible():
                self.hide()
            else:
                if not self.always_on_top:
                    self.show_from_tray()

    def update_menu_time_action(self):
        if self.open_context_menu and self.menu_time_action:
            if self.last_update_time:
                local_update_time = self.last_update_time.astimezone()
                update_str = local_update_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                update_str = "-"
            self.menu_time_action.setText(f'Updated: {update_str}')

    def save_settings(self):
        current_pos = {
            'x': int(self.geometry().x()),
            'y': int(self.geometry().y())
        }
        settings = {
            'position': current_pos,
            'scale': self.scale,
            'always_on_top': self.always_on_top,
            'enable_logging': self.enable_logging if not getattr(sys, 'frozen', False) else False,
            'osu_client_id': self.osu_client_id,
            'osu_client_secret': self.osu_client_secret,
            'osu_username': self.osu_username,
            'autostart': is_in_startup_registry() if getattr(sys, 'frozen', False) else False,
            'update_interval': self.update_interval,
        }
        utils_save_settings(self.settings_file, settings, self.enable_logging)

    def set_update_interval(self, interval_ms):
        self.update_interval = interval_ms
        self.settings['update_interval'] = interval_ms
        self.save_settings()

        now = datetime.now(timezone.utc)
        if self.last_update_time is None:
            self.last_update_time = now
        elapsed = (now - self.last_update_time).total_seconds() * 1000
        time_to_next = max(0, self.update_interval - elapsed)

        self.update_timer.stop()
        self.restart_update_timer(int(time_to_next))
        def restart_timer():
            self.restart_update_timer()
            self.update_timer.timeout.disconnect(restart_timer)
            self.update_timer.timeout.connect(restart_timer)

    def restart_update_timer(self, interval=None):
        self.update_timer.stop()
        self.update_timer.start(interval if interval is not None else self.update_interval)

    def initUI(self):
        self.updateWindowStyle()
        current_width = int(self.base_width * (self.scale / 100))
        current_height = int(self.base_height * (self.scale / 100))
        if hasattr(self, 'webView'):
            self.webView.deleteLater()
        self.webView = NoSelectWebEngineView(self)
        settings = self.webView.settings()
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, False)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, False)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, False)
        settings.setAttribute(QWebEngineSettings.AutoLoadIconsForPage, False)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.ErrorPageEnabled, False)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, False)
        profile = QWebEngineProfile.defaultProfile()
        profile.clearHttpCache()
        profile.setCachePath("")
        profile.setPersistentStoragePath("")
        profile.setHttpCacheType(QWebEngineProfile.NoCache)
        profile.setHttpCacheMaximumSize(0)
        self.webView.setFixedSize(current_width, current_height)
        self.webView.setGeometry(0, 0, current_width, current_height)
        self.webView.page().setBackgroundColor(Qt.transparent)
        self.webView.setAttribute(Qt.WA_TransparentForMouseEvents)
        if self.scale != 100:
            self.webView.setZoomFactor(self.scale / 100)
        self.webView.show()
        self.show()
        QTimer.singleShot(100, self.update_streak)

    def updateWindowStyle(self):
        self.setAttribute(Qt.WA_TranslucentBackground, not self.debug_border)
        self.setStyleSheet("""
            QMainWindow {
                border: 2px solid black;
                background-color: rgba(0, 0, 0, 10);
            }
        """ if self.debug_border else "")
        self.repaint()
        self.update()
        QApplication.processEvents()

    def toggle_autostart(self):
        if is_in_startup_registry():
            success = remove_from_startup_registry()
            if success:
                self.settings['autostart'] = False
                self.save_settings()
        else:
            success = add_to_startup_registry()
            if success:
                self.settings['autostart'] = True
                self.save_settings()

    def toggle_logging(self):
        if not getattr(sys, 'frozen', False):
            self.enable_logging = not self.enable_logging
            if self.enable_logging:
                print("[Widget] Logging enabled")
            else:
                print("[Widget] Logging disabled")
            self.settings['enable_logging'] = self.enable_logging
            self.save_settings()

    def updateSize(self):
        if hasattr(self, 'animation') and self.animation and self.animation.state() == QPropertyAnimation.Running:
            self.animation.stop()
        current_pos = self.geometry().topLeft()
        new_width = int(self.base_width * (self.scale / 100))
        new_height = int(self.base_height * (self.scale / 100))
        new_geometry = QRect(current_pos.x(), current_pos.y(), new_width, new_height)
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(100)
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(new_geometry)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.webView.setFixedSize(new_width, new_height)
        self.webView.setZoomFactor(self.scale / 100)
        def onAnimationFinished():
            self.setFixedSize(new_width, new_height)
            if hasattr(self, 'animation'):
                self.animation.finished.disconnect()
                self.animation = None
            QApplication.processEvents()
            self.settings['position'] = {
                'x': int(self.geometry().x()),
                'y': int(self.geometry().y())
            }
            self.save_settings()
        self.animation.finished.connect(onAnimationFinished)
        self.animation.start()

    def setScale(self, scale):
        old_pos = self.geometry().topLeft()
        self.scale = scale
        self.settings['scale'] = scale
        self.save_settings()
        self.updateSize()
        self.move(old_pos)

    def toggleDebugBorder(self):
        self.debug_border = not self.debug_border
        if self.enable_logging:
            print(f"[Widget] Debug border {'enabled' if self.debug_border else 'disabled'}")
        self.updateWindowStyle()

    def closeApp(self):
        current_pos = {
            'x': int(self.geometry().x()),
            'y': int(self.geometry().y())
        }
        self.settings['position'] = current_pos
        self.save_settings()
        QApplication.processEvents()
        if hasattr(self, 'webView'):
            self.webView.setHtml("")
            self.webView.close()
            self.webView.deleteLater()
        if self.popup:
            self.popup.close()
            self.popup.deleteLater()
            self.popup = None
        self.tray_time_timer.stop()
        QApplication.instance().quit()

    def closeEvent(self, event):
        try:
            self.closeApp()
        except SystemExit:
            QApplication.instance().quit()
        event.accept()

    def createContextMenu(self):
        createContextMenu(self)

    def mousePressEvent(self, event):
        mousePressEvent(self, event)

    def keyPressEvent(self, event):
        handle_key_press(self, event)

    def update_streak(self):
        update_streak(self)

    def on_update_timer(self):
        self.update_streak()
        self.restart_update_timer()

    def update_osu_settings(self, client_id=None, client_secret=None, username=None):
        update_osu_settings(self, client_id, client_secret, username)

    def enterEvent(self, event):
        pass

    def leaveEvent(self, event):
        pass

    def show_popup(self):
        popup_width = 420
        popup_height = 210
        global_widget_pos = self.mapToGlobal(QPoint(0, 0))
        widget_rect = QRect(global_widget_pos, self.size())

        matching_screen = None
        for screen in QApplication.screens():
            geo = screen.geometry()
            if geo.contains(widget_rect.center()):
                matching_screen = geo
                break
        if matching_screen is None:
            matching_screen = QApplication.primaryScreen().availableGeometry()
        desktop = matching_screen

        right_space = desktop.right() - widget_rect.right()
        left_space = widget_rect.left() - desktop.left()
        below_space = desktop.bottom() - widget_rect.bottom()
        above_space = widget_rect.top() - desktop.top()

        if below_space < popup_height and above_space >= popup_height:
            x = widget_rect.left() + (widget_rect.width() - popup_width) // 2
            x = max(desktop.left(), min(x, desktop.right() - popup_width))
            y = widget_rect.top() - popup_height
        elif right_space >= popup_width:
            x = widget_rect.right()
            y = widget_rect.top() + (widget_rect.height() - popup_height) // 2
            y = max(desktop.top(), min(y, desktop.bottom() - popup_height))
        elif left_space >= popup_width:
            x = widget_rect.left() - popup_width
            y = widget_rect.top() + (widget_rect.height() - popup_height) // 2
            y = max(desktop.top(), min(y, desktop.bottom() - popup_height))
        elif below_space >= popup_height:
            x = widget_rect.left() + (widget_rect.width() - popup_width) // 2
            x = max(desktop.left(), min(x, desktop.right() - popup_width))
            y = widget_rect.bottom()
        elif above_space >= popup_height:
            x = widget_rect.left() + (widget_rect.width() - popup_width) // 2
            x = max(desktop.left(), min(x, desktop.right() - popup_width))
            y = widget_rect.top() - popup_height
        else:
            x = widget_rect.left() + (widget_rect.width() - popup_width) // 2
            y = widget_rect.top() + (widget_rect.height() - popup_height) // 2

        if x < desktop.left():
            x = desktop.left()
        if x + popup_width > desktop.right():
            x = desktop.right() - popup_width
        if y < desktop.top():
            y = desktop.top()
        if y + popup_height > desktop.bottom():
            y = desktop.bottom() - popup_height

        popup_pos = QPoint(x, y)
        if self.popup is None:
            self.popup = QWebEngineView()
            self.popup.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.Tool)
            self.popup.setAttribute(Qt.WA_TranslucentBackground, True)
            self.popup.setAttribute(Qt.WA_ShowWithoutActivating)
            self.popup.setStyleSheet("background: transparent; border: none;")
            self.popup.setFixedSize(popup_width, popup_height)
            self.popup.page().setBackgroundColor(Qt.transparent)
            self.popup.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        else:
            if self.popup.isVisible():
                return
            self.popup.setFixedSize(popup_width, popup_height)
        self.popup.setHtml(HTML_POPUP_TEMPLATE)
        self.popup.move(popup_pos)
        self.popup.show()
        self.popup.raise_()

    def hide_popup(self):
        if self.popup is not None:
            self.popup.hide()

if __name__ == '__main__':
    os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--disable-logging --disable-gpu --disable-software-rasterizer --disable-dev-shm-usage'
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    ex = Widget()
    sys.exit(app.exec_())