import math
import random

class Aircraft:
    def __init__(self, identifier, route, route_manager):
        self.identifier = identifier
        self.route = route
        self.route_manager = route_manager

        self.current_waypoint_index = 0

        #position initial
        first_wp = route.waypoints[0]
        self.x = first_wp.x
        self.y = first_wp.y
        self.altitude = first_wp.altitude if first_wp.altitude else 300000

        #cap vers le prochain waypoint
        if len(route.waypoints) > 1:
            next_wp = route.waypoints[1]
            dx = next_wp.x - self.x
            dy = next_wp.y - self.y
            self.heading = math.degrees(math.atan2(dx, -dy)) % 360
        else:
            self.heading = 0

        self.speed = random.randint(350, 500)
        self.fuel = random.randint(30, 60) # minutes
        self.status = "Cruise" if route.route_type == "cruise" esle "Approach"

        self.target_altitude = self.altitude
        self.target_speed = self.speed
        self.target_heading = self.heading


        #Etat
        slef.in_collision = False
        self.in_warning = False
        self.has_emergency = False
        self.holding_center = None
        self.holding_radius = 5000
        self.manual_control = False
        self.has_lended = False
        self.is_destroyed = False

    def set_holding_pattern(self, enable = True):
        self.is_holding = enable
        if enable and not self.holding_center:
            self.holding_center = (self.x, self.y)

    def change_approach(self, approach_name):
        new_route = self.route_manager.get_route(approach_name)
        if new_route and new_route.route_type == "approach":
            self.route = new_route
            self.current_waypoint_index = 0
            self.manual_control = False
            self.is_holding = False
            slef.status = "Changed Approach"
            return True
        return False

    def trigger_emergency(self):
        if not self.has_emergency:
            self.has_emergency = True
            self.emergency_type = random.choice(["engine", "fuel"])
            if self.emergency_type == "engine":
                self.status = "URGENCE MOTEUR"
                self.fuel = max(5, self.fuel - 20)
            else:
                self.status = "URGENCE CARBURANT"
                self.fuel = random.randint(2, 8)

    def simulate_movement(self, dt = 1):
        if self.has_lended:
            return

        #taux de changement
        RATE_ALT = 800 * dt
        RATE_SPEED = 8 * dt
        RATE_HEADING = 3 * dt

        if not self.manual_control and not self.is_holding:
            self.auto_navigate()

        if self.is_holding and self.holding_center:
            self.holding_pattern()

        if abs(self.altitude - self.target_altitude) > RATE_ALT:
            if self.altitude < self.target_altitude:
                self.altitude = min(self.altitude + RATE_ALT, self.target_altitude)
            else:
                self.altitude = max(self.altitude - RATE_ALT, self.target_altitude)
        else:
            self.altitude = self.target_altitude


        if abs(self.speed - self.target_speed) > RATE_SPEED:
            if self.speed < self.target_speed:
                self.speed = min(self.speed + RATE_SPEED, self.target_speed)
            else:
                self.speed = max(self.speed - RATE_SPEED, self.target_speed)
        else:
            self.speed = self.target_speed


        diff = self.target_heading - self.heading
        if diff > 180:
            diff -= 360
        elif diff < -180:
            diff += 360
            if abs(diff) > RATE_HEADING:
                self.heading += RATE_HEADING if diff > 0 else -RATE_HEADING
            else:
                self.heading = self.target_heading
            self.heading %= 360



        rad = math.radians(self.heading)
        scale = 2.0
        dx = self.speed * scale * dt * math.sin(rad)
        dy = self.speed * scale * dt * math.cos(rad)
        self.x += dx
        self.y += dy

        fuel.rate = 0.02 if not self.manual_emergency else 0.04
        self.fuel -= fuel_rate * dt
        if self.fuel < 0:
            self.fuel = 0

        if self.altitude < 100 and math.sqrt(self.x ** 2 + self.y ** 2) < 2000:
            self.has_landed = True
            self.status = "Landed"
            self.speed = 0

    def _auto_navigate(self):
        if self.current_waypoint_index >= len(self.route.waypoints):
            return

        target_wp = self.route.waypoints[self.current_waypoint_index]
        dx = target_wp.x - self.x
        dy = target_wp.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < 5000:
            next_wp, next_idx = self.route.get_next_waypoint(self.current_waypoint_index)
            if next_wp:
                self.current_waypoint_index = next_idx
                target_wp = next_wp
                dx = target_wp.x - self.x
                dy = target_wp.y - self.y

        self.target_heading = math.degrees(math.atan2(dx, -dy)) % 360

        if target_wp.altitude is not None:
            self.target_altitude = target_wp.altitude

        if self.route_type == "approach":
            if self.altitude > 20000:
                self.target_speed = 380  # Haute altitude : vitesse normale
            elif self.altitude > 15000:
                self.target_speed = 320  # Descente initiale
            elif self.altitude > 10000:
                self.target_speed = 280  # Approche intermédiaire
            elif self.altitude > 5000:
                self.target_speed = 220  # Approche finale
            elif self.altitude > 2000:
                self.target_speed = 180  # Finale courte
            else:
                self.target_speed = 150

    def _holding_pattern(self):
        if not self.holding_center:
            return
        cx, cy = self.holding_center
        dx = self.x - cx
        dy = self.y - cy

        angle_to_center = math.atan2(dx, dy)
        tangent_angle = angle_to_center + math.pi / 2
        self.target_heading = math.degrees(-tangent_angle + math.pi / 2) % 360

        self.target_altitude = max(5000, self.altitude)

    def get_data(self):
        return {
            "ID": self.identifier,
            "X": round(self.x, 1),
            "Y": round(self.y, 1),
            "Altitude (ft)": round(self.altitude),
            "Vitesse (kts)": round(self.speed),
            "Cap (°)": round(self.heading, 1),
            "Carburant (min)": round(self.fuel, 1),
            "Statut": self.status,
            "Route": self.route.name,
            "Emergency": self.emergency_type if self.has_emergency else "None",
            "Holding": self.is_holding,
            "Collision": self.in_collision,
            "Landed": self.has_landed
        }


