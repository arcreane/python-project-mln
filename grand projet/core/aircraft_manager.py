import random
from core.aircraft import Aircraft

class AircraftManager:
    def __init__(self):
        self.aircraft_list = []

    def get_all_aircrafts(self):
        return self.aircraft_list

    def update(self, dt):
        for ac in self.aircraft_list:
            ac.simulate_movement(dt)
            ac.in_collision = False

    DIST_LIMIT = 3500
    ALT_LIMIT = 1000
    n = len(self.aircraft_list)
    for i in range(n):
        ac1 = self.aircraft_list[i]
        for j in range(i+1, n):
            ac2 = self.aircraft_list[j]
            dx = ac1.x - ac2.x
            dy = ac1.y - ac2.y
            d_alt = abs(ac1.altitude - ac2.altitude)
            if dx**2 + dy**2 < DIST_LIMIT**2 and d_alt < ALT_LIMIT:
                ac1.in_collision = True
                ac2.in_collision = True

    if random.randint(0, 100) < 10:
        airlines = ["AF", "AA", "AC", "AO", "BA", "CA", "EG", "LH", "LX", "QR", "JU"]
        IATA = random.choice(airlines)
        new_ac = Aircraft(f"{IATA}{random.randint(100, 999)}")
        self.aircraft_list.append(new_ac)
        return new_ac
    return None

