
import pygame, json, math
import demjson

class Animations:
    def __init__(self, aniName):
        f = open(aniName)
        try:
            ani = json.load(f)
        except:
            demjson.decode(f.read())
        f.close()

        self.items = dict()
        for k in ani['items']:
            self.items[k] = Animation(ani['items'][k])

        self.sequences = dict()
        for k in ani['sequences']:
            self.sequences[k] = ani['sequences'][k]

        self.forms = ani['forms']
        self.sets = ani['sets']

    def begin(self, item, variety, sequence):
        if sequence not in self.sequences:
            return
        self.items[item].begin(self.sequences[sequence], variety)

    def done(self, item):
        return self.items[item].done()

    def get(self, item, angleOffset):
        return self.items[item].get(angleOffset)

    def tip(self, item, endpoint, angleOffset):
        return self.items[item].tip(endpoint, angleOffset)

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
        img = pygame.image.load(self.name).convert_alpha()

        iw = img.get_width()
        ih = img.get_height()

        sx = self.ani['base']['x']
        sy = self.ani['base']['y']

        self.orgAngle = self.ani['angle']
        self.angle = self.orgAngle


        brw = 2 * sx
        brx = 0
        if brw < iw:
            brw = 2 * (iw - sx)
            brx = brw / 2 - sx
        brh = 2 * sy
        bry = 0
        if brh < ih:
            brh = 2 * (ih - sy)
            bry = brh / 2 - sy

        self.br = pygame.Surface((brw, brh)).convert_alpha()
        self.br.fill((0,0,0,0))
        self.br.blit(img, (brx, bry))

        print '%s size (%d, %d), start (%d, %d), bound (%d, %d), at (%d, %d)' % (self.name, iw, ih, sx, sy, brw, brh, brx, bry)

    def begin(self, sequences, variety):
        self.angle = self.orgAngle
        if variety not in sequences:
            self.sequence = None
            return
        self.sequence = sequences[variety]
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

    # Offset from "base" to endpoint, "tip" if not found/specified
    def tip(self, endpoint, angleOffset):
        sx = self.ani['base']['x']
        sy = self.ani['base']['y']
        if endpoint not in self.ani:
            #print self.name, endpoint, self.ani
            endpoint = 'tip'
        ex = self.ani[endpoint]['x']
        ey = self.ani[endpoint]['y']
        dx = ex - sx
        dy = ey - sy
        #print self.name, endpoint, sx, sy, ex, ey

        rad = math.radians(-(self.angle+angleOffset))
        x = dx * math.cos(rad) - dy * math.sin(rad)
        y = dx * math.sin(rad) + dy * math.cos(rad)
        return (int(x), int(y))

    def angleOffset(self):
        return self.angle - self.orgAngle

