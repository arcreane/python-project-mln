class Waypoint:

    def __init__(self, x, y, altitude=None):
        self.x = x
        self.y = y
        self.altitude = altitude


class Route:

    def __init__(self, name, waypoints, route_type="cruise"):
        self.name = name
        self.waypoints = waypoints
        self.route_type = route_type

    def get_next_waypoint(self, current_index):
        if current_index < len(self.waypoints) - 1:
            return self.waypoints[current_index + 1], current_index + 1
        return None, current_index


class RouteManager:

    def __init__(self):
        self.routes = {}
        self._create_routes()

    def _create_routes(self):
        """Crée les routes cruise et approches - CORRIGÉ : routes beaucoup plus longues"""

        # Route Cruise 1 : Nord -> Sud (étendue à 100km)
        self.routes["CRUISE_N_S"] = Route("CRUISE_N_S", [
            Waypoint(0, -100000, 30000),
            Waypoint(0, -60000, 30000),
            Waypoint(0, -20000, 30000),
            Waypoint(0, 20000, 30000),
            Waypoint(0, 60000, 30000),
            Waypoint(0, 100000, 30000)
        ], "cruise")

        # Route Cruise 2 : Est -> Ouest (étendue à 100km)
        self.routes["CRUISE_E_W"] = Route("CRUISE_E_W", [
            Waypoint(100000, 0, 32000),
            Waypoint(60000, 0, 32000),
            Waypoint(20000, 0, 32000),
            Waypoint(-20000, 0, 32000),
            Waypoint(-60000, 0, 32000),
            Waypoint(-100000, 0, 32000)
        ], "cruise")

        # Route Cruise 3 : Nord-Est -> Sud-Ouest (étendue)
        self.routes["CRUISE_NE_SW"] = Route("CRUISE_NE_SW", [
            Waypoint(70000, -70000, 28000),
            Waypoint(40000, -40000, 28000),
            Waypoint(15000, -15000, 28000),
            Waypoint(-15000, 15000, 28000),
            Waypoint(-40000, 40000, 28000),
            Waypoint(-70000, 70000, 28000)
        ], "cruise")

        # Route Cruise 4 : Sud-Est -> Nord-Ouest (étendue)
        self.routes["CRUISE_SE_NW"] = Route("CRUISE_SE_NW", [
            Waypoint(70000, 70000, 34000),
            Waypoint(40000, 40000, 34000),
            Waypoint(15000, 15000, 34000),
            Waypoint(-15000, -15000, 34000),
            Waypoint(-40000, -40000, 34000),
            Waypoint(-70000, -70000, 34000)
        ], "cruise")

        # Approche 1 : Standard ILS (depuis le Nord - commence à 80km)
        self.routes["APPROACH_1"] = Route("APPROACH_1", [
            Waypoint(0, -80000, 28000),
            Waypoint(0, -50000, 20000),
            Waypoint(0, -25000, 12000),
            Waypoint(0, -15000, 8000),
            Waypoint(0, -8000, 4000),
            Waypoint(0, -4000, 2000),
            Waypoint(0, 0, 0)  # Piste
        ], "approach")

        # Approche 2 : Depuis l'Est (commence à 80km)
        self.routes["APPROACH_2"] = Route("APPROACH_2", [
            Waypoint(80000, 0, 28000),
            Waypoint(50000, 0, 20000),
            Waypoint(25000, 0, 12000),
            Waypoint(15000, 0, 8000),
            Waypoint(8000, 0, 4000),
            Waypoint(4000, 0, 2000),
            Waypoint(0, 0, 0)
        ], "approach")

        # Approche 3 : Depuis le Sud (circuit plus long)
        self.routes["APPROACH_3"] = Route("APPROACH_3", [
            Waypoint(0, 80000, 28000),
            Waypoint(10000, 50000, 20000),
            Waypoint(20000, 30000, 15000),
            Waypoint(15000, 15000, 10000),
            Waypoint(10000, 5000, 5000),
            Waypoint(5000, 0, 2000),
            Waypoint(0, 0, 0)
        ], "approach")

        # Approche 4 : Depuis l'Ouest
        self.routes["APPROACH_4"] = Route("APPROACH_4", [
            Waypoint(-80000, 0, 28000),
            Waypoint(-50000, -5000, 20000),
            Waypoint(-25000, -5000, 12000),
            Waypoint(-15000, -3000, 8000),
            Waypoint(-8000, -2000, 4000),
            Waypoint(-4000, 0, 2000),
            Waypoint(0, 0, 0)
        ], "approach")

    def get_route(self, route_name):
        return self.routes.get(route_name)

    def get_random_cruise_route(self):
        import random
        cruise_routes = [r for r in self.routes.values() if r.route_type == "cruise"]
        return random.choice(cruise_routes)

    def get_random_approach_route(self):
        import random
        approach_routes = [r for r in self.routes.values() if r.route_type == "approach"]
        return random.choice(approach_routes)

    def get_all_approach_names(self):
        return [name for name, route in self.routes.items() if route.route_type == "approach"]