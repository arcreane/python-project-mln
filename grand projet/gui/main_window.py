from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
                               QLabel, QListWidget, QLineEdit, QGroupBox, QComboBox,
                               QTextEdit)
from PySide6.QtCore import QTimer, Qt
from gui.radar_scene import RadarScene
from gui.radar_view import RadarView


class MainWindow(QWidget):
    def __init__(self, aircraft_manager):
        super().__init__()
        self.aircraft_manager = aircraft_manager
        self.selected_aircraft = None

        self.setWindowTitle("ATC Simulator - Tour de Contrôle")
        self.resize(1600, 900)

        # Style sombre
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                color: #00ff00;
                font-family: 'Courier New', monospace;
            }
            QGroupBox {
                border: 2px solid #00ff00;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                color: #00ff00;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #2a2a2a;
                border: 2px solid #00ff00;
                border-radius: 5px;
                padding: 8px;
                color: #00ff00;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00ff00;
                color: #000000;
            }
            QPushButton:pressed {
                background-color: #00cc00;
            }
            QLineEdit, QComboBox {
                background-color: #2a2a2a;
                border: 2px solid #00ff00;
                border-radius: 3px;
                padding: 5px;
                color: #00ff00;
            }
            QListWidget {
                background-color: #0a0a0a;
                border: 2px solid #00ff00;
                border-radius: 3px;
                color: #00ff00;
            }
            QTextEdit {
                background-color: #0a0a0a;
                border: 2px solid #00ff00;
                border-radius: 3px;
                color: #00ff00;
            }
        """)

        # Radar
        self.scene = RadarScene(radar_radius=500)
        self.view = RadarView(self.scene)

        # Dessiner les routes
        self.scene.draw_routes(self.aircraft_manager.route_manager)

        self._build_ui()

        # Connexions
        self.scene.aircraft_selected.connect(self.on_aircraft_selected)
        self.list_widget.itemSelectionChanged.connect(self.on_list_selected)

        # Timer simulation
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(50)  # 50ms = 20 FPS

    def _build_ui(self):
        """Construction de l'interface"""
        layout = QHBoxLayout(self)

        # Panneau gauche - Statistiques et liste
        left_panel = QVBoxLayout()

        # Statistiques
        stats_group = QGroupBox("STATISTIQUES")
        stats_layout = QVBoxLayout()
        self.stats_label = QLabel("Initialisation...")
        self.stats_label.setStyleSheet("font-size: 12px;")
        stats_layout.addWidget(self.stats_label)
        stats_group.setLayout(stats_layout)
        left_panel.addWidget(stats_group)

        # Alertes collision
        alert_group = QGroupBox("⚠️ ALERTES")
        alert_layout = QVBoxLayout()
        self.alert_text = QTextEdit()
        self.alert_text.setReadOnly(True)
        self.alert_text.setMaximumHeight(100)
        self.alert_text.setStyleSheet("color: #ff0000; font-weight: bold;")
        alert_layout.addWidget(self.alert_text)
        alert_group.setLayout(alert_layout)
        left_panel.addWidget(alert_group)

        # Liste avions
        list_group = QGroupBox("AVIONS ACTIFS")
        list_layout = QVBoxLayout()
        self.list_widget = QListWidget()
        list_layout.addWidget(self.list_widget)
        list_group.setLayout(list_layout)
        left_panel.addWidget(list_group)

        # Panneau central - Radar
        center_layout = QVBoxLayout()
        radar_label = QLabel("RADAR ATC")
        radar_label.setAlignment(Qt.AlignCenter)
        radar_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        center_layout.addWidget(radar_label)
        center_layout.addWidget(self.view)

        # Panneau droit - Contrôles
        right_panel = QVBoxLayout()

        # Info avion sélectionné
        info_group = QGroupBox("AVION SÉLECTIONNÉ")
        info_layout = QVBoxLayout()
        self.info_label = QTextEdit()
        self.info_label.setReadOnly(True)
        self.info_label.setMaximumHeight(200)
        info_layout.addWidget(self.info_label)
        info_group.setLayout(info_layout)
        right_panel.addWidget(info_group)

        # Instructions manuelles
        manual_group = QGroupBox("CONTRÔLE MANUEL")
        manual_layout = QVBoxLayout()

        # Instructions claires
        help_label = QLabel("Entrez les nouvelles valeurs souhaitées\n(laissez vide pour ne pas modifier)")
        help_label.setStyleSheet("color: #888888; font-size: 10px; font-style: italic;")
        manual_layout.addWidget(help_label)

        manual_layout.addWidget(QLabel("Altitude (ft):"))
        self.alt_input = QLineEdit()
        self.alt_input.setReadOnly(False)
        self.alt_input.setPlaceholderText("Ex: 25000")
        manual_layout.addWidget(self.alt_input)

        manual_layout.addWidget(QLabel("Vitesse (kts):"))
        self.speed_input = QLineEdit()
        self.speed_input.setReadOnly(False)
        self.speed_input.setPlaceholderText("Ex: 350")
        manual_layout.addWidget(self.speed_input)

        manual_layout.addWidget(QLabel("Cap (°):"))
        self.heading_input = QLineEdit()
        self.heading_input.setReadOnly(False)
        self.heading_input.setPlaceholderText("Ex: 180")
        manual_layout.addWidget(self.heading_input)

        self.btn_apply = QPushButton("📡 APPLIQUER")
        self.btn_apply.clicked.connect(self.apply_instructions)
        manual_layout.addWidget(self.btn_apply)

        manual_group.setLayout(manual_layout)
        right_panel.addWidget(manual_group)

        # Commandes spéciales
        commands_group = QGroupBox("COMMANDES")
        commands_layout = QVBoxLayout()

        # Attente
        self.btn_holding = QPushButton("⏸️ METTRE EN ATTENTE")
        self.btn_holding.clicked.connect(self.toggle_holding)
        commands_layout.addWidget(self.btn_holding)

        # Changer approche
        commands_layout.addWidget(QLabel("Changer approche:"))
        self.approach_combo = QComboBox()
        approach_names = self.aircraft_manager.route_manager.get_all_approach_names()
        self.approach_combo.addItems(approach_names)
        commands_layout.addWidget(self.approach_combo)

        self.btn_change_approach = QPushButton("✈️ CHANGER APPROCHE")
        self.btn_change_approach.clicked.connect(self.change_approach)
        commands_layout.addWidget(self.btn_change_approach)

        # Atterrissage forcé
        self.btn_force_land = QPushButton("🚨 ATTERRISSAGE FORCÉ")
        self.btn_force_land.clicked.connect(self.force_landing)
        self.btn_force_land.setStyleSheet("""
            QPushButton {
                background-color: #cc0000;
                border: 2px solid #ff0000;
            }
            QPushButton:hover {
                background-color: #ff0000;
            }
        """)
        commands_layout.addWidget(self.btn_force_land)

        commands_group.setLayout(commands_layout)
        right_panel.addWidget(commands_group)

        right_panel.addStretch()

        # Assembly
        layout.addLayout(left_panel, 1)
        layout.addLayout(center_layout, 3)
        layout.addLayout(right_panel, 1)

    def on_aircraft_selected(self, symbol):
        """Quand un avion est sélectionné sur le radar"""
        # Si on change d'avion, vider les champs de contrôle
        if self.selected_aircraft != symbol.aircraft:
            self.alt_input.clear()
            self.speed_input.clear()
            self.heading_input.clear()

        self.selected_aircraft = symbol.aircraft
        self.update_info_panel()
        self.select_in_list(symbol.aircraft.identifier)

    def on_list_selected(self):
        """Quand un avion est sélectionné dans la liste"""
        items = self.list_widget.selectedItems()
        if not items:
            return

        ac_id = items[0].text().split(" - ")[0]
        symbol = self.scene.aircraft_symbols.get(ac_id)

        if symbol:
            # Si on change d'avion, vider les champs de contrôle
            if self.selected_aircraft != symbol.aircraft:
                self.alt_input.clear()
                self.speed_input.clear()
                self.heading_input.clear()

            self.selected_aircraft = symbol.aircraft
            symbol.setSelected(True)
            self.update_info_panel()

    def update_info_panel(self):
        """Met à jour le panneau d'information"""
        if not self.selected_aircraft:
            self.info_label.setText("Aucun avion sélectionné")
            return

        ac = self.selected_aircraft
        data = ac.get_data()

        # Afficher UNIQUEMENT les infos (lecture seule)
        info_text = f"""ID: {data['ID']}
Route: {data['Route']}
Statut: {data['Statut']}

POSITION ACTUELLE:
  X: {data['X']} m
  Y: {data['Y']} m
  Altitude: {data['Altitude (ft)']} ft
  Vitesse: {data['Vitesse (kts)']} kts
  Cap: {data['Cap (°)']}°

CARBURANT: {data['Carburant (min)']} min

CIBLES ACTUELLES:
  Altitude cible: {int(ac.target_altitude)} ft
  Vitesse cible: {int(ac.target_speed)} kts
  Cap cible: {round(ac.target_heading, 1)}°

ALERTES:
  Urgence: {data['Emergency']}
  En attente: {'OUI' if data['Holding'] else 'NON'}
  Collision: {'⚠️ OUI' if data['Collision'] else 'NON'}
        """

        self.info_label.setText(info_text)
        # Ne PLUS remplir automatiquement les champs de contrôle

    def select_in_list(self, ac_id):
        """Sélectionne un avion dans la liste"""
        for i in range(self.list_widget.count()):
            if self.list_widget.item(i).text().startswith(ac_id):
                self.list_widget.setCurrentRow(i)
                return

    def apply_instructions(self):
        """Applique les instructions manuelles"""
        if not self.selected_aircraft:
            return

        try:
            # Lire les valeurs saisies
            alt_text = self.alt_input.text().strip()
            speed_text = self.speed_input.text().strip()
            heading_text = self.heading_input.text().strip()

            # Appliquer seulement les valeurs non-vides
            if alt_text:
                alt = int(alt_text)
                self.selected_aircraft.set_instruction(alt=alt)

            if speed_text:
                speed = int(speed_text)
                self.selected_aircraft.set_instruction(speed=speed)

            if heading_text:
                heading = float(heading_text)
                self.selected_aircraft.set_instruction(heading=heading)

            # Vider les champs après application
            self.alt_input.clear()
            self.speed_input.clear()
            self.heading_input.clear()

            # Feedback visuel temporaire
            self.btn_apply.setText("✓ APPLIQUÉ")
            QTimer.singleShot(1000, lambda: self.btn_apply.setText("📡 APPLIQUER"))

        except ValueError:
            # Feedback d'erreur
            self.btn_apply.setText("❌ ERREUR")
            QTimer.singleShot(1000, lambda: self.btn_apply.setText("📡 APPLIQUER"))

    def toggle_holding(self):
        """Bascule le mode attente"""
        if not self.selected_aircraft:
            return

        self.selected_aircraft.set_holding_pattern(not self.selected_aircraft.is_holding)
        self.update_info_panel()

    def change_approach(self):
        """Change l'approche de l'avion"""
        if not self.selected_aircraft:
            return

        approach_name = self.approach_combo.currentText()
        success = self.selected_aircraft.change_approach(approach_name)
        if success:
            self.update_info_panel()

    def force_landing(self):
        """Force l'atterrissage"""
        if not self.selected_aircraft:
            return

        self.aircraft_manager.force_landing(self.selected_aircraft.identifier)
        self.update_info_panel()

    def update_simulation(self):
        """Mise à jour de la simulation"""
        # Update des avions
        new_ac = self.aircraft_manager.update(0.1)

        if new_ac:
            self.scene.add_aircraft_to_scene(new_ac)

        # Mise à jour positions
        self.scene.update_positions()

        # Mise à jour liste
        self.list_widget.clear()
        for ac in self.aircraft_manager.get_all_aircrafts():
            status = ""
            if ac.has_emergency:
                status = "🚨"
            elif ac.in_collision:
                status = "⚠️"
            elif ac.is_holding:
                status = "⏸️"

            self.list_widget.addItem(f"{ac.identifier} - {status} {ac.status}")

        # Mise à jour statistiques
        stats = self.aircraft_manager.get_statistics()
        stats_text = f"""
Total générés: {stats['total_spawned']}
Actifs: {stats['active']}
Atterris: {stats['landed']}
Collisions: {stats['collisions']}
        """
        self.stats_label.setText(stats_text)

        # Alertes collision ET avertissements préventifs
        alert_msg = ""

        # Collisions imminentes (ROUGE)
        if self.aircraft_manager.collision_detected:
            alert_msg += "🚨 COLLISION IMMINENTE! 🚨\n"
            alert_msg += "=" * 30 + "\n"
            for pair in self.aircraft_manager.collision_pairs:
                alert_msg += f"💥 {pair[0]} ↔ {pair[1]}\n"
            alert_msg += "\n"

        # Avertissements (ORANGE)
        if self.aircraft_manager.warning_pairs:
            alert_msg += "⚠️ ATTENTION - Collision possible\n"
            alert_msg += "=" * 30 + "\n"
            for warning in self.aircraft_manager.warning_pairs:
                ac1, ac2, dist, alt_diff = warning
                alert_msg += f"⚡ {ac1} ↔ {ac2}\n"
                alert_msg += f"   Distance: {dist} km\n"
                alert_msg += f"   Séparation alt: {alt_diff} ft\n\n"

        # Si tout va bien
        if not alert_msg:
            alert_msg = "✓ Aucune alerte\n✓ Séparation sécurisée"

        self.alert_text.setText(alert_msg)

        # Mise à jour info si avion sélectionné
        if self.selected_aircraft:
            is_destroyed = getattr(self.selected_aircraft, 'is_destroyed', False)
            if self.selected_aircraft.has_landed or is_destroyed:
                # L'avion sélectionné a atterri ou est détruit, le désélectionner
                self.selected_aircraft = None
                self.info_label.setText("Avion atterri ou détruit")
                self.alt_input.clear()
                self.speed_input.clear()
                self.heading_input.clear()
            else:
                self.update_info_panel()