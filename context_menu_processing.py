from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QLineEdit, QMenu, QWidgetAction, QApplication
from PyQt5.QtCore import Qt, QPoint

class NoSelectWebEngineView(QWebEngineView):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A and event.modifiers() == Qt.ControlModifier:
            event.ignore()
            return
        super().keyPressEvent(event)

class SaveOnFocusOutLineEdit(QLineEdit):
    def __init__(self, save_callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save_callback = save_callback

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.save_callback()

class NonClosingMenu(QMenu):
    def __init__(self, parent_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent_window = parent_window

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
        elif e.key() == Qt.Key_F5:
            if self.parent_window:
                self.parent_window.update_streak()
        else:
            super().keyPressEvent(e)

class MouseMoveMixin:
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