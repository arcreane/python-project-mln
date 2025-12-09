import random
from core.aircraft import Aircraft

class AircraftManager:

    COLLISION_HORITZ_DIST = 4000
    COLLISION_VERT_DIST = 1000
    SPAWN_PROBABILITY = 0.010

    def __init__(self):
        self.aircraft_list = []

    def add_aircraft(self, aircraft: Aircraft):
        self.aircraft_list.append(aircraft)

    def remove_aircraft(self, aircraft: Aircraft):
        if aircraft in self.aircraft_list:
            self.aircraft_list.remove(aircraft)

    def generate_random_aircraft(self):
        airlines = ["AF", "BA", "LH", "DL", "UA", "RYR", "EZY"]
        code = random.choice(airlines) + str(random.randint(100, 999))
        new_ac = Aircraft(code)
        self.aircraft_list.append(new_ac)
        return new_ac


    def detect_collision(self):
        for ac in self.aircraft_list:
            ac.in_collision = False
        n = len(self.aircraft_list)
        horiz_sq = self.COLLISION_HORITZ_DIST ** 2

        for i in range(n):
            a1 = self.aircraft_list[i]
            if a1.status == "Atterri":
                continue

            for j in range(i+1, n):
                a2 = self.aircraft_list[j]
                if a2.status == "Atterri":
                    continue

                dx = a1.x - a2.x
                dy = a1.y - a2.y
                dist_sq = dx * dx + dy * dy

                d_alt = abs(a1.altitude - a2.altitude)

                if dist_sq < horiz_sq and d_alt < self.COLLISION_VERT_DIST:
                    a1.in_collision = True
                    a2.in_collision = True

    def update_movement(self, dt: float):
        for ac in self.aircraft_list:
            ac.mouvements(dt)

    def update(self, dt = 0.1):
        self.detect_collision()
        self.update_movement(dt)

        if random.random() < self.SPAWN_PROBABILITY:
            return self.generate_random_aircraft()

        return None
    def get_all_aircrafts(self):
        return self.aircraft_list

