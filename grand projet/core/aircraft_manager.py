import random
import math
from core.aircraft import Aircraft
from core.routes import RouteManager


class AircraftManager:
    def __init__(self):
        self.aircraft_list = []
        self.route_manager = RouteManager()
        self.spawn_counter = 0
        self.collision_detected = False
        self.collision_pairs = []
        self.warning_pairs = []

        self.total_spawned = 0
        self.total_landed = 0
        self.collision_history = set()
        self.total_collisions = 0

    def get_all_aircrafts(self):
        return [ac for ac in self.aircraft_list
                if not ac.has_landed and not getattr(ac, 'is_destroyed', False)]

    def _spawn_initial_aircraft(self):
        num_initial = random.randint(5, 8)
        for _ in range(num_initial):
            self.spawn_aircraft()

    def spawn_aircraft(self):
        """Génère un nouvel avion"""
        self.spawn_counter += 1
        self.total_spawned += 1

        if random.random() < 0.7:
            route = self.route_manager.get_random_cruise_route()
            prefix = "CRZ"
        else:
            route = self.route_manager.get_random_approach_route()
            prefix = "APP"

        identifier = f"{prefix}{random.randint(100, 999)}"
        aircraft = Aircraft(identifier, route, self.route_manager)
        self.aircraft_list.append(aircraft)

        return aircraft

    def update(self, dt):
        """Mise à jour de tous les avions"""
        for ac in self.aircraft_list:
            if not getattr(ac, 'is_destroyed', False):
                ac.simulate_movement(dt)
            ac.in_collision = False
            ac.in_warning = False


        self.collision_detected = False
        self.collision_pairs = []
        self.warning_pairs = []

        DIST_COLLISION = 4000
        DIST_WARNING = 8000
        ALT_COLLISION = 1000
        ALT_WARNING = 2000

        active_aircraft = self.get_all_aircrafts()
        n = len(active_aircraft)

        for i in range(n):
            ac1 = active_aircraft[i]
            for j in range(i + 1, n):
                ac2 = active_aircraft[j]
                dx = ac1.x - ac2.x
                dy = ac1.y - ac2.y
                d_alt = abs(ac1.altitude - ac2.altitude)
                dist = math.sqrt(dx ** 2 + dy ** 2)

                if dist < DIST_COLLISION and d_alt < ALT_COLLISION:
                    ac1.in_collision = True
                    ac2.in_collision = True
                    self.collision_detected = True

                    if not hasattr(ac1, 'collision_timer'):
                        ac1.collision_timer = 0
                        ac2.collision_timer = 0

                    ac1.collision_timer += dt
                    ac2.collision_timer += dt

                    if ac1.collision_timer > 2.0:
                        ac1.is_destroyed = True
                        ac1.status = "💥 DÉTRUIT"
                    if ac2.collision_timer > 2.0:
                        ac2.is_destroyed = True
                        ac2.status = "💥 DÉTRUIT"

                    pair_key = tuple(sorted([ac1.identifier, ac2.identifier]))
                    self.collision_pairs.append((ac1.identifier, ac2.identifier))

                    if pair_key not in self.collision_history:
                        self.collision_history.add(pair_key)
                        self.total_collisions += 1

                elif dist < DIST_WARNING and d_alt < ALT_WARNING:
                    ac1.in_warning = True
                    ac2.in_warning = True
                    self.warning_pairs.append((ac1.identifier, ac2.identifier,
                                               round(dist / 1000, 1), round(d_alt)))

        for ac in active_aircraft:
            if not ac.has_emergency and random.random() < 0.0001:
                ac.trigger_emergency()

        new_aircraft = None
        if random.random() < 0.005:
            new_aircraft = self.spawn_aircraft()

        for ac in self.aircraft_list:
            if ac.has_landed and ac.status == "Atterri":
                self.total_landed += 1
                ac.status = "Landed (counted)"

        return new_aircraft

    def force_landing(self, aircraft_id):
        aircraft = self.get_aircraft_by_id(aircraft_id)
        if aircraft:
            approaches = [r for r in self.route_manager.routes.values()
                          if r.route_type == "approach"]

            min_dist = float('inf')
            best_approach = None

            for approach in approaches:
                first_wp = approach.waypoints[0]
                dist = math.sqrt((aircraft.x - first_wp.x) ** 2 +
                                 (aircraft.y - first_wp.y) ** 2)
                if dist < min_dist:
                    min_dist = dist
                    best_approach = approach

            if best_approach:
                aircraft.route = best_approach
                aircraft.current_waypoint_index = 0
                aircraft.manual_control = False
                aircraft.is_holding = False
                aircraft.status = "Atterrissage forcé"
                return True
        return False

    def get_aircraft_by_id(self, aircraft_id):
        for ac in self.aircraft_list:
            if ac.identifier == aircraft_id:
                return ac
        return None

    def get_statistics(self):
        return {
            "total_spawned": self.total_spawned,
            "active": len(self.get_all_aircrafts()),
            "landed": self.total_landed,
            "collisions": self.total_collisions
        }