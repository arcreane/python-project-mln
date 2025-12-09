from PySide6.QtWidgets import (QMainWindow, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QStatusBar,
                               QLineEdit, QApplication, QMessageBox, QFrame, QGridLayout, QFormLayout)
from PySide6.QtCore import Qt, QTimer
from core.aircraft import Aircraft
from core.aircraft_manager import AircraftManager
from gui.radar_view import RadarScene, RadarView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Contrôle Aérien")
        self.setGeometry(100, 100, 1400, 800)

        self.manager = AircraftManager()
        self.current_aircraft_symbol = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        self.radar_scene = RadarScene()
        self.radar_view = RadarView(self.radar_scene)
        main_layout.addWidget(self.radar_view)

        control_panel = self.build_right_panel()
        main_layout.addWidget(control_panel)

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.radar_scene.selectionChanged.connect(self, on_aircraft_selected)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(100)

    def build_right_panel(self):
        panel = QFrame()
        panel.setFixedWidht(260)
        layout = QVBoxLayout(panel)

        self.info_label = QLabel()
        self.info_label.setStyleSheet("font-weight; bold; font-size: 14px;")
        layout.addWidget(self.info_label)

        self.info_label = QLabel("Sélectionnez un avion.")
        self.info_label.setAlignment(Qt.AlignTop)
        self.info_label.setMinimumHeight(200)
        layout.addWidget(self.info_label)

        form_group = QFrame()
        form_group.setStyleSheet("border: 1px solid grey; padding: 5px; border-radius: 5px;")
        form_layout = QGridLayout(form_group)

        form_layout.addWidget(QLabel("Alt. (ft):"), 0, 0)
        self.input_alt = QLineEdit()
        form_layout.addWidget(self.input_alt, 0, 1)

        form_layout.addWidget(QLabel("Vitesse (kts):"), 1, 0)
        self.input_vites = QLineEdit()
        form_layout.addWidget(self.input_vites, 1, 1)


        form_layout.addWidget(QLabel("Cap (deg):"), 2, 0)
        self.input_cap = QLineEdit()
        form_layout.addWidget(self.input_cap, 2, 1)

        self.btn_apply = QPushButton("Envoyer Instructions")
        self.btn_apply.clicked.connect(self.send_instruction)
        self.btn_apply.setEnable(False)
        form_layout.addWidget(self.btn_apply, 3, 0, 1, 2)

        layout.addWidget(form_group)
        layout.addStretch()

        return panel


    def on_aircraft_selected(self):
        items = self.radar_scene.selectedItems()
        self.current_aircraft_symbol = None

        if not items :
            self.btn_apply.setEnabled(False)
            self.input_alt.clear()
            self.input_speed.clear()
            self.input_heading.clear()
            return

        symbol = items[0]

        if hasattr(symbol, "aircraft"):
            self.current_aircraft_symbol = symbol
            data = symbol.aircraft.get_data()

            self.input_alt.setText(str(data['Target Alt (ft)']))
            self.input_speed.setText(str(data['Target Speed (kts)']))
            self.input_heading.setText(str(data['Target Cap (deg)']))

            self.btn_apply.setEnabled(True)
            self.update_info_display()

    def update_info_display(self):
        if not self.current_aircraft_symbol:
            return
        data = ("red" if data["Collision"] else ("blue" if data["Status"] == "Atteri" else "green"))
        text = (
            f"Avion : {data['ID']}\n"
            f"Statut : {status}\n"
            f"Altitude : {data['Altitude (ft)']} → {data['Target Alt (ft)']}\n"
            f"Vitesse : {data['Vitesse (kts)']} → {data['Target Speed (kts)']}\n"
            f"Cap : {data['Cap (deg)']}° → {data['Target Cap (deg)']}°\n"
            f"Carburant : {data['Carburant (min)']:.1f} min"
        )
        self.info_label.setText(text)

    def send_instruction(self):
        if not self.current_aircraft_symbol:
            return








