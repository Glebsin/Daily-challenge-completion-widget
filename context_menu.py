from PyQt5.QtWidgets import (
    QAction, QWidgetAction, QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QApplication
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QCursor
from context_menu_processing import SaveOnFocusOutLineEdit, NonClosingMenu
from streak_utils import UPDATE_INTERVALS

def createContextMenu(self):
    menu = NonClosingMenu(self)
    scaleWidget = QWidget()
    scaleLayout = QVBoxLayout(scaleWidget)
    scaleLabel = QLabel('Scale, % (100-500)')
    scaleLabel.setStyleSheet("color: white; padding: 2px 0;")
    def updateScale():
        try:
            value = int(scaleInput.text())
            value = min(500, max(100, value))
            scaleInput.setText(str(value))
            self.setScale(value)
        except ValueError:
            scaleInput.setText(str(self.scale))
    scaleInput = SaveOnFocusOutLineEdit(updateScale)
    scaleInput.setText(str(self.scale))
    scaleInput.setFixedWidth(230)
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
    clientSecretLabel = QLabel('osu!api Client Secret')
    clientSecretLabel.setStyleSheet("color: white; padding: 2px 0;")
    usernameLabel = QLabel('osu! Username')
    usernameLabel.setStyleSheet("color: white; padding: 2px 0;")
    def updateOsuFields():
        self.update_osu_settings(
            clientIdInput.text(),
            clientSecretInput.text(),
            usernameInput.text()
        )
    clientIdInput = SaveOnFocusOutLineEdit(updateOsuFields)
    clientIdInput.setText(self.osu_client_id)
    clientIdInput.setPlaceholderText("Enter client ID")
    clientIdInput.setFixedWidth(230)
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
    clientIdInput.returnPressed.connect(updateOsuFields)
    clientSecretInput = SaveOnFocusOutLineEdit(updateOsuFields)
    clientSecretInput.setText(self.osu_client_secret)
    clientSecretInput.setPlaceholderText("Enter client secret")
    clientSecretInput.setFixedWidth(230)
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
    clientSecretInput.returnPressed.connect(updateOsuFields)
    usernameInput = SaveOnFocusOutLineEdit(updateOsuFields)
    usernameInput.setText(self.osu_username)
    usernameInput.setPlaceholderText("Enter username")
    usernameInput.setFixedWidth(230)
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
    usernameInput.returnPressed.connect(updateOsuFields)
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
    import sys
    from autostart_utils import is_in_startup_registry
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
    intervalWidget = QWidget()
    intervalLayout = QHBoxLayout(intervalWidget)
    intervalLabel = QLabel('Update interval')
    intervalLabel.setStyleSheet("color: white; padding: 2px 0;")
    intervalCombo = QComboBox()
    desired_height = 28
    intervalCombo.setStyleSheet(f"""
QComboBox {{
    background-color: #222;
    color: white;
    border: 1px solid #4D4D4D;
    padding: 0 10px 0 3px;
    min-width: 100px;
    height: {desired_height}px;
    font-size: 14px;
}}
QComboBox QAbstractItemView {{
    background-color: #222;
    color: white;
    border: 1px solid #4D4D4D;
    selection-background-color: #333;
    selection-color: white;
    outline: none;
}}
QComboBox QAbstractItemView::item {{
    height: {desired_height}px;
    min-height: {desired_height}px;
    max-height: {desired_height}px;
    font-size: 14px;
    padding: 0 10px;
}}
""")
    intervalCombo.setFixedHeight(desired_height)
    intervalCombo.view().setStyleSheet(f"QListView::item{{height: {desired_height}px;}}")
    for idx, (interval, label) in enumerate(UPDATE_INTERVALS):
        intervalCombo.addItem(label, interval)
        if interval == self.update_interval:
            intervalCombo.setCurrentIndex(idx)
    def onIntervalChanged(idx):
        value = intervalCombo.itemData(idx)
        self.set_update_interval(value)
    intervalCombo.currentIndexChanged.connect(onIntervalChanged)
    intervalLayout.addWidget(intervalLabel)
    intervalLayout.addWidget(intervalCombo)
    intervalWidget.setLayout(intervalLayout)
    intervalAction = QWidgetAction(menu)
    intervalAction.setDefaultWidget(intervalWidget)
    menu.addAction(intervalAction)
    menu.addSeparator()
    if self.last_update_time:
        local_update_time = self.last_update_time.astimezone()
        update_str = local_update_time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        update_str = "-"
    timeAction = QAction(f'Updated: {update_str}', self)
    timeAction.setEnabled(False)
    menu.addAction(timeAction)
    self.open_context_menu = menu
    self.menu_time_action = timeAction
    if not hasattr(self, 'menu_time_timer'):
        self.menu_time_timer = QTimer(self)
        self.menu_time_timer.setInterval(1000)
        self.menu_time_timer.timeout.connect(self._update_menu_time_action)
    self.menu_time_timer.start()
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
    self.open_context_menu = None
    self.menu_time_action = None
    self.menu_time_timer.stop()

def mousePressEvent(self, event):
    if event.button() == Qt.RightButton:
        self.createContextMenu()
    else:
        self.oldPos = event.globalPos()