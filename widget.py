import sys
import json
import os
from datetime import datetime, timezone, timedelta
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMenu, QAction, QWidgetAction, QWidget, QVBoxLayout, QLabel, QLineEdit
)
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QRect, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineProfile
from PyQt5.QtGui import QCursor
from widget_templates import DEFAULT_TEMPLATE, ALTERNATIVE_TEMPLATE
from ossapi import Ossapi
from autostart_utils import add_to_startup_registry, remove_from_startup_registry, is_in_startup_registry

class NoSelectWebEngineView(QWebEngineView):
    def keyPressEvent(self, event):
        # Prevent Ctrl+A selection
        if event.key() == Qt.Key_A and event.modifiers() == Qt.ControlModifier:
            event.ignore()
            return
        super().keyPressEvent(event)

class NonClosingMenu(QMenu):
    def mouseReleaseEvent(self, e):
        action = self.activeAction()
        if action and isinstance(action, QWidgetAction):
            e.ignore()
        elif action and action.isEnabled():
            action.trigger()
        else:
            e.ignore()
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter:
            e.ignore()
        else:
            super().keyPressEvent(e)

class TransparentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.debug_border = False
        self.enable_logging = False if getattr(sys, 'frozen', False) else False

        if getattr(sys, 'frozen', False):
            self.settings_file = os.path.join(os.path.dirname(sys.executable), "widget_settings.json")
        else:
            self.settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "widget_settings.json")

        self.settings = self.load_settings()
        self.scale = self.settings.get('scale', 100)
        self.base_width = 150
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
        self.use_alternative_template = self.settings.get('use_alternative_template', False)
        self.always_on_top = self.settings.get('always_on_top', True)
        self.enable_logging = False if getattr(sys, 'frozen', False) else self.settings.get('enable_logging', False)

        if getattr(sys, 'frozen', False) and self.settings.get('autostart', True):
            add_to_startup_registry()

        self.animation = None
        self.snap_distance = 10
        self.arrow_step = 2

        self.last_update_time = None  # Track last osu!api update time

        self.initUI()
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_streak)
        self.update_timer.start(300000)

    def calculate_days_since_start(self):
        start_date = datetime(2024, 7, 24, 0, 0, 0, tzinfo=timezone.utc)
        current_date = datetime.now(timezone.utc)
        days = (current_date - start_date).days
        if self.enable_logging:
            print(f"[Widget] Days since start (2024-07-24): {days}")
        return days

    def get_daily_streak(self):
        try:
            if not self.osu_client_id or not self.osu_client_secret or not self.osu_username:
                if self.enable_logging:
                    print("[osu!api] Skipping API request - missing credentials")
                self.use_alternative_template = False
                return '0d'
            if self.enable_logging:
                print(f"[osu!api] All credentials present, sending request for user {self.osu_username}")
            try:
                api = Ossapi(self.osu_client_id, self.osu_client_secret)
                user = api.user(self.osu_username)
                streak_value = user.daily_challenge_user_stats.daily_streak_current
                if self.enable_logging:
                    print(f"[osu!api] Received streak value: {streak_value}")
                days_since_start = self.calculate_days_since_start()
                streak_difference = days_since_start - streak_value
                if self.enable_logging:
                    print(f"[Widget] Streak difference: {streak_difference}")
                if streak_difference == 0:
                    if self.enable_logging:
                        print("[Widget] Setting ALTERNATIVE_TEMPLATE (streak is current)")
                    self.use_alternative_template = True
                else:
                    if self.enable_logging:
                        print("[Widget] Setting DEFAULT_TEMPLATE (streak is behind)")
                    self.use_alternative_template = False
                self.last_update_time = datetime.now(timezone.utc)
                return f"{streak_value}d"
            except Exception as api_error:
                if self.enable_logging:
                    print(f"[osu!api] API request error: {api_error}")
                self.use_alternative_template = False
                return '0d'
        except Exception as e:
            if self.enable_logging:
                print(f"[osu!api] Error getting daily streak: {e}")
            self.use_alternative_template = False
            return '0d'

    def update_streak(self):
        if self.enable_logging:
            print("[Widget] Updating streak value...")
        streak_value = self.get_daily_streak()
        current_template = ALTERNATIVE_TEMPLATE if self.use_alternative_template else DEFAULT_TEMPLATE
        html_content = current_template.format(
            current_time=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
            current_user=self.osu_username if self.osu_username else "rvany345",
            daily_streak=streak_value
        )
        if hasattr(self, 'webView'):
            self.webView.setHtml(html_content)
            if self.enable_logging:
                print(f"[Widget] Streak value updated: {streak_value}")
                print(f"[Widget] Using {'ALTERNATIVE' if self.use_alternative_template else 'DEFAULT'} template")

    def load_settings(self):
        try:
            if self.enable_logging:
                print(f"[Settings] Attempting to load settings from: {self.settings_file}")
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    if 'position' in loaded_settings:
                        pos = loaded_settings['position']
                        if not isinstance(pos, dict) or 'x' not in pos or 'y' not in pos:
                            if self.enable_logging:
                                print("[Settings] Invalid position format in settings")
                            loaded_settings.pop('position')
                        else:
                            loaded_settings['position'] = {
                                'x': int(pos['x']),
                                'y': int(pos['y'])
                            }
                    if 'scale' in loaded_settings:
                        try:
                            scale = int(loaded_settings['scale'])
                            if scale < 100 or scale > 500:
                                if self.enable_logging:
                                    print("[Settings] Invalid scale value, resetting to 100")
                                loaded_settings['scale'] = 100
                            else:
                                loaded_settings['scale'] = scale
                        except (ValueError, TypeError):
                            if self.enable_logging:
                                print("[Settings] Invalid scale format, resetting to 100")
                            loaded_settings['scale'] = 100
                    if self.enable_logging:
                        print(f"[Settings] Successfully loaded settings: {loaded_settings}")
                    return loaded_settings
            else:
                if self.enable_logging:
                    print("[Settings] Settings file not found")
        except Exception as e:
            if self.enable_logging:
                print(f"[Settings] Error loading settings: {e}")
        return {}

    def save_settings(self):
        try:
            settings_dir = os.path.dirname(self.settings_file)
            if not os.path.exists(settings_dir):
                os.makedirs(settings_dir)
            current_pos = {
                'x': int(self.geometry().x()),
                'y': int(self.geometry().y())
            }
            if self.enable_logging:
                print(f"[Settings] Saving window position: {current_pos}")
                print(f"[Settings] Saving to file: {self.settings_file}")
            settings = {
                'position': current_pos,
                'scale': self.scale,
                'use_alternative_template': self.use_alternative_template,
                'always_on_top': self.always_on_top,
                'enable_logging': self.enable_logging if not getattr(sys, 'frozen', False) else False,
                'osu_client_id': self.osu_client_id,
                'osu_client_secret': self.osu_client_secret,
                'osu_username': self.osu_username,
                'autostart': is_in_startup_registry() if getattr(sys, 'frozen', False) else False
            }
            temp_file = self.settings_file + '.tmp'
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            if sys.platform == 'win32':
                if os.path.exists(self.settings_file):
                    os.replace(temp_file, self.settings_file)
                else:
                    os.rename(temp_file, self.settings_file)
            else:
                os.rename(temp_file, self.settings_file)
            if self.enable_logging:
                print("[Settings] Settings saved successfully")
        except Exception as e:
            if self.enable_logging:
                print(f"[Settings] Error saving settings: {e}")
            try:
                with open(self.settings_file, 'w', encoding='utf-8') as f:
                    json.dump(settings, f)
            except Exception as e:
                if self.enable_logging:
                    print(f"[Settings] Fatal error saving settings: {e}")

    def update_osu_settings(self, client_id=None, client_secret=None, username=None):
        settings_changed = False
        if client_id is not None:
            if not self.osu_client_secret or not self.osu_username:
                if self.enable_logging:
                    print("[osu!api] Missing client secret or username, skipping API request")
                self.osu_client_id = client_id
                settings_changed = True
            else:
                self.osu_client_id = client_id
                settings_changed = True
                if self.enable_logging:
                    print("[osu!api] Client ID updated, all fields present")
                self.update_streak()
        if client_secret is not None:
            if not self.osu_client_id or not self.osu_username:
                if self.enable_logging:
                    print("[osu!api] Missing client ID or username, skipping API request")
                self.osu_client_secret = client_secret
                settings_changed = True
            else:
                self.osu_client_secret = client_secret
                settings_changed = True
                if self.enable_logging:
                    print("[osu!api] Client Secret updated, all fields present")
                self.update_streak()
        if username is not None:
            if not self.osu_client_id or not self.osu_client_secret:
                if self.enable_logging:
                    print("[osu!api] Missing client ID or client secret, skipping API request")
                self.osu_username = username
                settings_changed = True
            else:
                self.osu_username = username
                settings_changed = True
                if self.enable_logging:
                    print("[osu!api] Username updated, all fields present")
                self.update_streak()
        if settings_changed:
            self.save_settings()

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
        additional_style = """
            * {
                -webkit-user-select: none !important;
                -moz-user-select: none !important;
                -ms-user-select: none !important;
                user-select: none !important;
            }
            ::selection {
                background: transparent !important;
            }
        """
        current_template = ALTERNATIVE_TEMPLATE if self.use_alternative_template else DEFAULT_TEMPLATE
        html_content = current_template.format(
            current_time=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
            current_user=self.osu_username if self.osu_username else "rvany345",
            daily_streak="0d"
        ).replace('</style>', additional_style + '</style>')
        self.webView.page().setBackgroundColor(Qt.transparent)
        self.webView.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.webView.setHtml(html_content)
        if self.scale != 100:
            self.webView.setZoomFactor(self.scale / 100)
        self.webView.show()
        self.show()
        QTimer.singleShot(100, self.update_streak)

    def updateWindowStyle(self):
        self.setAttribute(Qt.WA_TranslucentBackground, not self.debug_border)
        if self.debug_border:
            self.setStyleSheet("""
                QMainWindow {
                    border: 2px solid red;
                    background-color: rgba(0, 0, 0, 10);
                }
            """)
        else:
            self.setStyleSheet("")

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
        self.updateWindowStyle()

    def toggle_template(self):
        current_pos = self.pos()
        current_scale = self.scale
        self.use_alternative_template = not self.use_alternative_template
        if hasattr(self, 'webView'):
            self.webView.setHtml("")
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
        current_width = int(self.base_width * (self.scale / 100))
        current_height = int(self.base_height * (self.scale / 100))
        self.webView.setFixedSize(current_width, current_height)
        self.webView.setGeometry(0, 0, current_width, current_height)
        additional_style = """
            * {
                -webkit-user-select: none !important;
                -moz-user-select: none !important;
                -ms-user-select: none !important;
                user-select: none !important;
            }
            ::selection {
                background: transparent !important;
            }
        """
        current_template = ALTERNATIVE_TEMPLATE if self.use_alternative_template else DEFAULT_TEMPLATE
        streak_value = self.get_daily_streak()
        html_content = current_template.format(
            current_time=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
            current_user=self.osu_username if self.osu_username else "rvany345",
            daily_streak=streak_value
        ).replace('</style>', additional_style + '</style>')
        self.webView.page().setBackgroundColor(Qt.transparent)
        self.webView.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.webView.setHtml(html_content)
        if current_scale != 100:
            self.webView.setZoomFactor(current_scale / 100)
        self.webView.show()
        self.move(current_pos)
        self.save_settings()

    def createContextMenu(self):
        menu = NonClosingMenu(self)
        scaleWidget = QWidget()
        scaleLayout = QVBoxLayout(scaleWidget)
        scaleLabel = QLabel('Scale, % (100-500)')
        scaleLabel.setStyleSheet("color: white; padding: 2px 0;")
        scaleInput = QLineEdit()
        scaleInput.setText(str(self.scale))
        scaleInput.setFixedWidth(100)
        scaleInput.setStyleSheet("""
            QLineEdit {
                background-color: #3D3D3D;
                color: white;
                border: 1px solid #4D4D4D;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        def updateScale():
            try:
                value = int(scaleInput.text())
                value = min(500, max(100, value))
                scaleInput.setText(str(value))
                self.setScale(value)
            except ValueError:
                scaleInput.setText(str(self.scale))
            finally:
                scaleInput.setFocus()
                scaleInput.selectAll()
        scaleInput.returnPressed.connect(updateScale)
        scaleLayout.addWidget(scaleLabel)
        scaleLayout.addWidget(scaleInput)
        scaleAction = QWidgetAction(menu)
        scaleAction.setDefaultWidget(scaleWidget)
        menu.addAction(scaleAction)
        menu.addSeparator()
        osuWidget = QWidget()
        osuLayout = QVBoxLayout(osuWidget)
        clientIdLabel = QLabel('osu!api Client ID')
        clientIdLabel.setStyleSheet("color: white; padding: 2px 0;")
        clientIdInput = QLineEdit()
        clientIdInput.setText(self.osu_client_id)
        clientIdInput.setPlaceholderText("Enter client ID")
        clientIdInput.setFixedWidth(200)
        clientIdInput.setStyleSheet("""
            QLineEdit {
                background-color: #3D3D3D;
                color: white;
                border: 1px solid #4D4D4D;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        clientSecretLabel = QLabel('osu!api Client Secret')
        clientSecretLabel.setStyleSheet("color: white; padding: 2px 0;")
        clientSecretInput = QLineEdit()
        clientSecretInput.setText(self.osu_client_secret)
        clientSecretInput.setPlaceholderText("Enter client secret")
        clientSecretInput.setFixedWidth(200)
        clientSecretInput.setStyleSheet("""
            QLineEdit {
                background-color: #3D3D3D;
                color: white;
                border: 1px solid #4D4D4D;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        usernameLabel = QLabel('osu! Username')
        usernameLabel.setStyleSheet("color: white; padding: 2px 0;")
        usernameInput = QLineEdit()
        usernameInput.setText(self.osu_username)
        usernameInput.setPlaceholderText("Enter username")
        usernameInput.setFixedWidth(200)
        usernameInput.setStyleSheet("""
            QLineEdit {
                background-color: #3D3D3D;
                color: white;
                border: 1px solid #4D4D4D;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        def updateOsuSettings():
            self.update_osu_settings(
                clientIdInput.text(),
                clientSecretInput.text(),
                usernameInput.text()
            )
        for input_field in [clientIdInput, clientSecretInput, usernameInput]:
            input_field.returnPressed.connect(updateOsuSettings)
        osuLayout.addWidget(clientIdLabel)
        osuLayout.addWidget(clientIdInput)
        osuLayout.addWidget(clientSecretLabel)
        osuLayout.addWidget(clientSecretInput)
        osuLayout.addWidget(usernameLabel)
        osuLayout.addWidget(usernameInput)
        osuWidget.setLayout(osuLayout)
        osuAction = QWidgetAction(menu)
        osuAction.setDefaultWidget(osuWidget)
        menu.addAction(osuAction)
        menu.addSeparator()
        # Manual update button
        manualUpdateAction = QAction('Manual Update', self)
        manualUpdateAction.setToolTip("Click to manually refresh the widget (same as F5)")
        manualUpdateAction.triggered.connect(self.update_streak)
        menu.addAction(manualUpdateAction)
        menu.addSeparator()
        alwaysOnTopAction = QAction('Always on Top', self)
        alwaysOnTopAction.setCheckable(True)
        alwaysOnTopAction.setChecked(self.always_on_top)
        alwaysOnTopAction.triggered.connect(self.toggle_always_on_top)
        menu.addAction(alwaysOnTopAction)
        if getattr(sys, 'frozen', False):
            autostartAction = QAction('Run at Startup', self)
            autostartAction.setCheckable(True)
            autostartAction.setChecked(is_in_startup_registry())
            autostartAction.triggered.connect(self.toggle_autostart)
            menu.addAction(autostartAction)
        if not getattr(sys, 'frozen', False):
            loggingAction = QAction('Enable API Logging', self)
            loggingAction.setCheckable(True)
            loggingAction.setChecked(self.enable_logging)
            loggingAction.triggered.connect(self.toggle_logging)
            menu.addAction(loggingAction)
        menu.addSeparator()
        update_str = self.last_update_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_update_time else "-"
        timeAction = QAction(f'Updated: {update_str}', self)
        timeAction.setEnabled(False)
        menu.addAction(timeAction)
        menu.addSeparator()
        exitAction = menu.addAction('Exit')
        exitAction.triggered.connect(self.closeApp)
        menu.setStyleSheet("""
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
        pos = QCursor.pos()
        screen = QApplication.primaryScreen().geometry()
        menu_size = menu.sizeHint()
        if pos.x() + menu_size.width() > screen.right():
            pos.setX(pos.x() - menu_size.width())
        menu.exec_(pos)
        scaleInput.setFocus()
        scaleInput.selectAll()

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
            self.webView.page().profile().clearAllVisitedLinks()
            self.webView.close()
            self.webView.deleteLater()
        raise SystemExit('Exit button pressed')

    def closeEvent(self, event):
        try:
            self.closeApp()
        except SystemExit:
            QApplication.instance().quit()
        event.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F4 and event.modifiers() == Qt.AltModifier:
            self.closeApp()
            return
        if event.key() == Qt.Key_A and event.modifiers() == Qt.ControlModifier:
            event.ignore()
            return
        # Manual update on F5
        if event.key() == Qt.Key_F5:
            self.update_streak()
            return
        self.key_sequence.append(event.key())
        if len(self.key_sequence) > 3:
            self.key_sequence = self.key_sequence[-3:]
        if len(self.key_sequence) == 3:
            if self.key_sequence == [Qt.Key_7, Qt.Key_2, Qt.Key_7]:
                self.toggleDebugBorder()
                print(f"Debug border {'enabled' if self.debug_border else 'disabled'}")
            self.key_sequence = []
        moved = False
        if event.key() == Qt.Key_Left:
            self.move(self.x() - self.arrow_step, self.y())
            moved = True
        elif event.key() == Qt.Key_Right:
            self.move(self.x() + self.arrow_step, self.y())
            moved = True
        elif event.key() == Qt.Key_Up:
            self.move(self.x(), self.y() - self.arrow_step)
            moved = True
        elif event.key() == Qt.Key_Down:
            self.move(self.x(), self.y() + self.arrow_step)
            moved = True
        if moved:
            QApplication.processEvents()
            self.settings['position'] = {
                'x': int(self.geometry().x()),
                'y': int(self.geometry().y())
            }
            self.save_settings()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.createContextMenu()
        else:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        new_pos = QPoint(self.x() + delta.x(), self.y() + delta.y())
        screens = QApplication.screens()
        current_screen = None
        for screen in screens:
            if screen.geometry().contains(event.globalPos()):
                current_screen = screen
                break
        if not current_screen:
            current_screen = QApplication.primaryScreen()
        if abs(delta.x()) < 5 and abs(delta.y()) < 5:
            screen_geo = current_screen.geometry()
            if abs(new_pos.x() - screen_geo.x()) < self.snap_distance:
                new_pos.setX(screen_geo.x())
            elif abs((screen_geo.x() + screen_geo.width()) - (new_pos.x() + self.width())) < self.snap_distance:
                new_pos.setX(screen_geo.x() + screen_geo.width() - self.width())
            if abs(new_pos.y() - screen_geo.y()) < self.snap_distance:
                new_pos.setY(screen_geo.y())
            elif abs((screen_geo.y() + screen_geo.height()) - (new_pos.y() + self.height())) < self.snap_distance:
                new_pos.setY(screen_geo.y() + screen_geo.height() - self.height())
        self.move(new_pos)
        self.oldPos = event.globalPos()
        if abs(delta.x()) < 5 and abs(delta.y()) < 5:
            self.settings['position'] = {
                'x': int(self.geometry().x()),
                'y': int(self.geometry().y())
            }
            self.save_settings()

if __name__ == '__main__':
    os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--disable-logging --disable-gpu --disable-software-rasterizer --disable-dev-shm-usage'
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    ex = TransparentWindow()
    sys.exit(app.exec_())