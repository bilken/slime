
import pygame, json, math

class Animations:
    def __init__(self, aniName):
        f = open(aniName)
        ani = json.load(f)
        f.close()

        self.items = dict()
        for k in ani['items']:
            self.items[k] = Animation(ani['items'][k])

        self.sequences = dict()
        for k in ani['sequences']:
            self.sequences[k] = ani['sequences'][k]

    def begin(self, item, sequence):
        if sequence not in self.sequences:
            return
        self.items[item].begin(self.sequences[sequence])

    def done(self, item):
        return self.items[item].done()

    def get(self, item, angleOffset):
        return self.items[item].get(angleOffset)

    def tip(self, item, angleOffset):
        return self.items[item].tip(angleOffset)

    def angle(self, item):
        return self.items[item].angle

class Animation:
    """
* Convert image so that the base is the start
* Rotate image around start point
* Detect collisions on line from start to end point
* Execute animation sequences
"""
    def __init__(self, ani):
        self.ani = ani

        self.sequence = None
        self.name = self.ani['file']
        self.variety = self.ani['variety']
        img = pygame.image.load(self.name).convert_alpha()

        iw = img.get_width()
        ih = img.get_height()

        sx = self.ani['base']['x']
        sy = self.ani['base']['y']
        ex = self.ani['tip']['x']
        ey = self.ani['tip']['y']

        self.orgAngle = self.ani['angle']
        self.angle = self.orgAngle

        self.dx = ex - sx
        self.dy = ey - sy

        brw = 2 * sx
        brx = 0
        if brw < iw:
            brw = 2 * (iw - sx)
            brx = brw / 2
        brh = 2 * sy
        bry = 0
        if brh < ih:
            brh = 2 * (ih - sy)
            bry = brh / 2

        self.br = pygame.Surface((brw, brh)).convert_alpha()
        self.br.fill((0,0,0,0))
        self.br.blit(img, (brx, bry))

        print '%s size (%d, %d), bound (%d, %d), at (%d, %d)' % (self.name, iw, ih, brw, brh, brx, bry)

    def begin(self, sequences):
        self.angle = self.orgAngle
        if self.variety not in sequences:
            self.sequence = None
            return
        self.sequence = sequences[self.variety]
        print self.sequence
        self.index = 0

    def done(self):
        return (self.sequence == None)

    # Returns image with "base" at the center
    def get(self, angleOffset):
        if self.sequence:
            self.angle += self.sequence[self.index]
            self.index += 1
            if self.index >= len(self.sequence):
                self.sequence = None
                self.index = 0
        return pygame.transform.rotate(self.br, self.angle + angleOffset)

    # Offset from "base" to "tip"
    def tip(self, angleOffset):
        rad = math.radians(-(self.angle+angleOffset))
        x = self.dx * math.cos(rad) - self.dy * math.sin(rad)
        y = self.dx * math.sin(rad) + self.dy * math.cos(rad)
        return (int(x), int(y))

    def angleOffset(self):
        return self.angle - self.orgAngle

