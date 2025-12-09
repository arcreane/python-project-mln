import random as r
import math as m



class Aircraft:
    def __init__(self, aircraft_id):
        self.aircraft_id = aircraft_id
        Map_size = 15000
        center = Map_size/2

        side = r.randint(0, 3)

        if side == 0:
            self.x = r.randint(0, Map_size)
            self.y = 0
        elif side == 1:
            self.x = r.randint(0, Map_size)
            self.y = Map_size
        elif side == 2:
            self.x = 0
            self.y = r.randint(0, Map_size)
        elif side == 3:
            self.x = Map_size
            self.y = r.randint(0, Map_size)

        angle_rad = m.atan2(center-self.y, center-self.x)
        angle_deg = m.degrees(angle_rad)
        self.heading = (angle_deg + 90) % 360

        self.altitude = r.randint(15000, 35000)
        self.speed = r.randint(350, 500)
        self.fuel = r.randint(200, 400)
        self.status = 'en approche'

        self.target_altitude = self.altitude
        self.target_speed = self.speed
        self.target_heading = self.heading

        self.in_collision = False

    def get_data(self):
        return {
            'id': self.aircraft_id,
            'x': self.x,
            'y': self.y,
            'Cap (deg)': self.heading,
            'Altitude (ft)': self.altitude,
            'Vitesse (kts)': self.speed,
            'Carburant (min)' : self.fuel,
            'Status': self.status,
            'Target altitude (ft)': self.target_altitude,
            'Target speed (kts)': self.target_speed,
            'Target heading (deg)': self.target_heading,
            }

    def set_instructions(self, alt=None, speed=None, heading=None):
        if alt is not None:
            self.target_altitude = max(0, int(alt))
        if speed is not None:
            self.target_speed = max(0, int(speed))
        if heading is not None:
            self.target_heading = heading % 360

    def mouvements(self, dt=1):
        Rate_altitude = 500*dt
        Rate_speed = 5*dt
        Rate_heading = 5*dt

        if self.altitude < self.target_altitude:
            self.altitude = min(self.altitude + Rate_altitude, self.target_altitude)
        elif self.altitude > self.target_altitude:
            self.altitude = max(self.altitude - Rate_altitude, self.target_altitude)

        if self.speed < self.target_speed:
            self.speed = min(self.speed + Rate_speed, self.target_speed)
        elif self.speed > self.target_speed:
            self.speed = max(self.speed - Rate_speed, self.target_speed)

        diff = self.target_heading - self.heading
        if diff > 180:
            diff -= 360
        elif diff < -180:
            diff += 360
        if abs(diff) > Rate_heading:
            if diff > 0:
                self.heading = Rate_heading
            else:
                self.heading = -Rate_heading
        else:
            self.heading = self.target_heading

        heading_rad = self.heading*m.pi/180
        scale_factor = 10.0
        dx = self.speed * scale_factor * dt * m.sin(heading_rad)
        dy = self.speed * scale_factor * dt * -m.cos(heading_rad)
        self.x += dx
        self.y += dy

        self.fuel -= dt/60.0
        if self.fuel < 0 :
            self.fuel = 0

    def is_in_collision(self):
        return self.in_collision