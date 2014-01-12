
import pygame, json, math

class Animation:
    """
* Convert image so that the base is the start
* Rotate image around start point
* Detect collisions on line from start to end point
* Execute animation sequences
"""
    def __init__(self, imgName, aniName):
        self.name = imgName
        self.ani = json.load(open(aniName))

        img = pygame.image.load(imgName).convert_alpha()

        iw = img.get_width()
        ih = img.get_height()

        sx = self.ani['base']['x']
        sy = self.ani['base']['y']
        ex = self.ani['tip']['x']
        ey = self.ani['tip']['y']

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

        brmx = brw / 2
        brmy = brh / 2

    def get(self):
        return self.br

    # Returns rotated image with "base" at the center
    def rotate(self, r):
        return pygame.transform.rotate(self.br, r)

    # Offset from "base" to "tip"
    def tip(self, r=0):
        rad = math.radians(-r)
        x = self.dx * math.cos(rad) - self.dy * math.sin(rad)
        y = self.dx * math.sin(rad) + self.dy * math.cos(rad)
        return (int(x), int(y))

