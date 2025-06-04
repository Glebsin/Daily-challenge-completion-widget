from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

def handle_key_press(self, event):
    if event.key() == Qt.Key_F4 and event.modifiers() == Qt.AltModifier:
        self.closeApp()
        return
    if event.key() == Qt.Key_A and event.modifiers() == Qt.ControlModifier:
        event.ignore()
        return
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