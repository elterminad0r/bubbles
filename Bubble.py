STANDARD_RAD = 30
MAX_RAD_FACTOR = 0.5
SHRINK_FACTOR = 0.999
BUBBLE_SPEED = 0.5
LERP_FACTOR = 0.95
DIST_FACTOR = 0.2
EATING_FACTOR = 0.1

def apply_to(l):
    def to_all(func):
        def f(*args, **kwargs):
            for i in list(l):
                func(i, *args, **kwargs)
        return f
    return to_all    

def touches(x1, y1, x2, y2, r1, r2):
    return dist(x1, y1, x2, y2) < (r1 + r2)

def avg(l):
    return float(sum(l)) / float(len(l))

def avg_coord(coords):
    xs, ys = zip(*coords)
    return avg(xs), avg(ys)

def coord_lerp(x1, y1, x2, y2, l):
    return lerp(x1, x2, l), lerp(y1, y2, l)

class Bubble(object):
    inst = set()
    
    rainbow = False
    srainbow = False
    do_stroke = True
    
    def __init__(self):
        self.R = STANDARD_RAD
        self.pos = PVector(random(self.R, width - self.R),
                           random(self.R, height - self.R))
        self.vel = PVector.random2D().mult(BUBBLE_SPEED)
        self.group = set()
        self.inst.add(self)
        self.c = random(255)
        self.sc = random(255)
    
    @staticmethod
    @apply_to(inst)
    def update(self):
        self.pos += self.vel
        if self.R > STANDARD_RAD:
            self.R *= SHRINK_FACTOR
        if self.R > width * MAX_RAD_FACTOR:
            self.inst.remove(self)
        if self.pos.x - self.R < 0:
            self.vel.x *= -1
            self.pos.x = self.R
        if self.pos.x + self.R > width:
            self.vel.x *= -1
            self.pos.x = width - self.R
        if self.pos.y - self.R < 0:
            self.vel.y *= -1
            self.pos.y = self.R
        if self.pos.y + self.R > height:
            self.vel.y *= -1
            self.pos.y = height - self.R
        
        for b in self.inst:
            if b != self and self.R <= b.R and touches(self.pos.x, self.pos.y, b.pos.x, b.pos.y, self.R, b.R):
                self.inst.remove(self)
                b.group.add(self)
                b.R += self.R * EATING_FACTOR
                b.c = map(self.R, 0, b.R, self.c, b.c)
                b.sc = map(self.R, 0, b.R, self.sc, b.sc)
                Bubble()
                break

        if self.group:
            for b in list(self.group):
                b.pos.x, b.pos.y = coord_lerp(self.pos.x, self.pos.y, b.pos.x, b.pos.y, LERP_FACTOR)
                if dist(b.pos.x, b.pos.y, self.pos.x, self.pos.y) < float(self.R) * DIST_FACTOR:
                    self.group.remove(b)

    @staticmethod
    @apply_to(inst)
    def mousePressed(self, x, y):
        if dist(x, y, self.pos.x, self.pos.y) < self.R:
            self.inst.remove(self)

    @staticmethod
    @apply_to(inst)
    def _draw(self, fill_=False, stroke_=False):
        if fill_:
            if self.rainbow:
                fill(self.c, 255, 255)
            else:
                fill(0)
        else:
            noFill()
        
        if stroke_:
            if self.srainbow:
                stroke(self.sc, 255, 255)
            else:
                stroke(255)
        else:
            noStroke()

        ellipse(self.pos.x, self.pos.y, self.R * 2, self.R * 2)
        for b in self.group:
            ellipse(b.pos.x, b.pos.y, b.R * 2, b.R * 2)
        
    @classmethod
    def draw(cls):
        colorMode(HSB, 255, 255, 255)
        strokeWeight(3)
        if cls.do_stroke:
            cls._draw(stroke_=True)
        cls._draw(fill_=True)
