class Ball:
    def __init__(self, x, y, radius, speed, width, height):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.width = width
        self.height = height

    def move_up(self):
        if self.y - self.speed - self.radius >= 0:
            self.y -= self.speed

    def move_down(self):
        if self.y + self.speed + self.radius <= self.height:
            self.y += self.speed

    def move_left(self):
        if self.x - self.speed - self.radius >= 0:
            self.x -= self.speed

    def move_right(self):
        if self.x + self.speed + self.radius <= self.width:
            self.x += self.speed