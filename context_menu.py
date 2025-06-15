from PyQt5.QtWidgets import (
    QAction, QWidgetAction, QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QApplication, QToolTip, QSlider, QStyleOptionSlider
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QCursor
from context_menu_processing import SaveOnFocusOutLineEdit, NonClosingMenu
from streak_utils import UPDATE_INTERVALS

APP_VERSION = "2025.616.0"

class MyMenu(NonClosingMenu):
    def event(self, e):
        if e.type() == 110: 
            action = self.actionAt(e.pos())
            if action and getattr(action, "_is_version_action", False):
                QToolTip.showText(e.globalPos(), "Click to copy version")
                return True
        return super().event(e)

def createContextMenu(self):
    menu = MyMenu(self)
    scaleWidget = QWidget()
    scaleLayout = QVBoxLayout(scaleWidget)
    scaleLayout.setContentsMargins(5, 5, 5, 5)
    scaleLayout.setSpacing(2)

    default_font = QApplication.font("QMenu")

    scaleTitle = QLabel('Scale (100-500, %)')
    scaleTitle.setStyleSheet("color: white; font-weight: normal; padding-bottom: 2px;")
    scaleTitle.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    scaleTitle.setFont(default_font)
    scaleLayout.addWidget(scaleTitle)

    sliderRow = QWidget()
    sliderRowLayout = QHBoxLayout(sliderRow)
    sliderRowLayout.setContentsMargins(0, 0, 0, 0)
    sliderRowLayout.setSpacing(0)
    min_scale = 100
    max_scale = 500
    step = 10
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(min_scale)
    slider.setMaximum(max_scale)
    slider.setSingleStep(step)
    slider.setTickInterval(step)
    slider.setTickPosition(QSlider.TicksBelow)
    slider.setValue(self.scale)
    slider.setFixedWidth(180)
    slider.setFont(default_font)
    slider.setStyleSheet("""
        QSlider::groove:horizontal {
            border: none;
            height: 4px;
            background: #555;
            margin: 0; /* убрали отступы, чтобы ручка доходила до края */
            border-radius: 2px;
        }
        QSlider::handle:horizontal {
            background: #4CAF50;
            border: 2px solid #388E3C;
            width: 10px;
            height: 24px;
            margin: -10px 0; /* убрали левый margin */
            border-radius: 2px;
        }
        QSlider::handle:horizontal:pressed {
            background: #81C784;
            border: 2px solid #388E3C;
        }
        QSlider::sub-page:horizontal {
            background: #888;
            border-radius: 2px;
        }
        QSlider::add-page:horizontal {
            background: #555;
            border-radius: 2px;
        }
        QSlider::tick-mark {
            background: #888;
        }
    """)
    minLabel = QLabel(str(min_scale))
    minLabel.setStyleSheet("color: white; font-weight: normal;")
    minLabel.setFixedWidth(24)
    minLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    minLabel.setFont(default_font)
    maxLabel = QLabel(str(max_scale))
    maxLabel.setStyleSheet("color: white; font-weight: normal;")
    maxLabel.setFixedWidth(28)
    maxLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    maxLabel.setFont(default_font)
    valueLabel = QLabel(str(self.scale))
    valueLabel.setStyleSheet("color: white; font-weight: normal;")
    valueLabel.setFixedWidth(40)
    valueLabel.setAlignment(Qt.AlignCenter)
    valueLabel.setFont(default_font)
    sliderRowLayout.addWidget(minLabel)
    sliderRowLayout.addWidget(slider)
    sliderRowLayout.addWidget(maxLabel)
    sliderRow.setLayout(sliderRowLayout)
    scaleLayout.addWidget(sliderRow)
    valueRow = QWidget()
    valueRowLayout = QHBoxLayout(valueRow)
    valueRowLayout.setContentsMargins(0, 0, 0, 0)
    valueRowLayout.setSpacing(0)
    valueRowLayout.addStretch()
    valueRowLayout.addWidget(valueLabel)
    valueRowLayout.addStretch()
    valueRow.setLayout(valueRowLayout)
    scaleLayout.addWidget(valueRow)
    scaleWidget.setLayout(scaleLayout)
    scaleAction = QWidgetAction(menu)
    scaleAction.setDefaultWidget(scaleWidget)
    menu.addAction(scaleAction)

    def applySliderScale():
        value = slider.value()
        snapped = round((value - min_scale) / step) * step + min_scale
        slider.setValue(snapped)
        valueLabel.setText(str(snapped))
        self.setScale(snapped)
    slider.sliderReleased.connect(applySliderScale)
    slider.valueChanged.connect(lambda value: valueLabel.setText(str(round((value - min_scale) / step) * step + min_scale)))
    original_mousePressEvent = slider.mousePressEvent
    def sliderMousePressEvent(event):
        if event.button() == Qt.LeftButton and slider.rect().contains(event.pos()):
            handle_w = slider.style().pixelMetric(slider.style().PM_SliderLength)
            opt = QStyleOptionSlider()
            slider.initStyleOption(opt)
            handle_rect = slider.style().subControlRect(
                slider.style().CC_Slider,
                opt,
                slider.style().SC_SliderHandle,
                slider
            )
            if not handle_rect.contains(event.pos()):
                slider_w = slider.width() - handle_w
                x = event.pos().x() - handle_w // 2
                x = max(0, min(slider_w, x))
                value = min_scale + round((x / slider_w) * (max_scale - min_scale) / step) * step
                slider.setValue(value)
                valueLabel.setText(str(value))
                self.setScale(value)
                slider.setSliderDown(False)
            else:
                original_mousePressEvent(event)
        else:
            original_mousePressEvent(event)
    slider.mousePressEvent = sliderMousePressEvent

    menu.addSeparator()
    osuWidget = QWidget()
    osuLayout = QVBoxLayout(osuWidget)
    clientIdLabel = QLabel('osu!api Client ID')
    clientIdLabel.setStyleSheet("color: white; padding: 2px 0;")
    clientIdLabel.setFont(default_font)
    clientSecretLabel = QLabel('osu!api Client Secret')
    clientSecretLabel.setStyleSheet("color: white; padding: 2px 0;")
    clientSecretLabel.setFont(default_font)
    usernameLabel = QLabel('osu! Username')
    usernameLabel.setStyleSheet("color: white; padding: 2px 0;")
    usernameLabel.setFont(default_font)
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
    clientIdInput.setFont(default_font)
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
    clientSecretInput.setFont(default_font)
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
    usernameInput.setFont(default_font)
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
    intervalLabel.setFont(default_font)
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
    intervalCombo.setFont(default_font)
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
    versionAction = QAction(f'Version: {APP_VERSION}', self)
    versionAction.setEnabled(True)
    versionAction._is_version_action = True
    def copy_version_to_clipboard():
        QApplication.clipboard().setText(APP_VERSION)
    versionAction.triggered.connect(copy_version_to_clipboard)
    menu.addAction(versionAction)
    menu.addSeparator()
    exitAction = menu.addAction('Quit')
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
    pos = QCursor.pos()
    screen = QApplication.primaryScreen().geometry()
    menu_size = menu.sizeHint()
    if pos.x() + menu_size.width() > screen.right():
        pos.setX(pos.x() - menu_size.width())
    menu.exec_(pos)
    self.open_context_menu = None
    self.menu_time_action = None
    self.menu_time_timer.stop()

def mousePressEvent(self, event):
    if event.button() == Qt.RightButton:
        self.createContextMenu()
    else:
        self.oldPos = event.globalPos()