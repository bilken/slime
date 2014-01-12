
import pygame, json, math

class Animation:
    """
* Rotate image around start point
* Detect collisions on line from start to end point
* Execute animation sequences
"""
    def __init__(self, imgName, aniName):
        self.ani = json.load(open(aniName))

        img = pygame.image.load(imgName).convert_alpha()

        iw = img.get_width()
        ih = img.get_height()

        sx = self.ani['base']['x']
        sy = self.ani['base']['y']
        #ex = self.ani['tip']['x']
        #ey = self.ani['tip']['y']

        brw = 2 * sx
        brx = 0
        if brw < iw:
            brw = 2 * ((iw / 2) - sx)
            brx = brw / 2 + sx
        brh = 2 * sy
        bry = 0
        if brh < ih:
            brh = 2 * ((ih / 2) - sy)
            bry = brh / 2 + sy

        self.br = pygame.Surface((brw, brh)).convert_alpha()
        self.br.fill((0,0,0,0))
        self.br.blit(img, (brx, bry))

        brmx = brw / 2
        brmy = brh / 2

    def rotate(self, r):
        return pygame.transform.rotate(self.br, r)

