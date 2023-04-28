import pyxel

SCREEN_SIZE = 360, 240
MID = SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2

# sprites
#   image, u, v, w, h, colkey
FISH1 = 0, 0, 32, 24, 16, 0
FISH2 = 0, 0, 48, 24, 16, 0


def rndxy():
    return pyxel.rndi(0, SCREEN_SIZE[0]), pyxel.rndi(0, SCREEN_SIZE[1])


class App:
    def __init__(self) -> None:
        pyxel.init(*SCREEN_SIZE)
        pyxel.load("assets/fishing2.pyxres")
        pyxel.playm(0, loop=True)
        self.bfish = 0, MID[1]
        self.bfish2 = 0, MID[1] + 10
        self.fishs = [(*rndxy(), FISH1) for _ in range(10)]
        self.bg = [rndxy() for _ in range(15)]
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        line_start = MID[0], 0
        line_end = MID

        # image, u, v, w, h, colkey
        hook = (0, 0, 8, 8, 8, 0)
        fish = (0, 0, 32, 24, 16, 0)

        self.draw_bg()
        self.fishes()

        pyxel.line(*line_start, *line_end, 9)
        pyxel.blt(MID[0] - 7, MID[1], *hook)
    

    def fishes(self):
        for i, (x, y, sprite) in enumerate(self.fishs):
            pyxel.blt(x, y, *sprite)

            if x - 24 > SCREEN_SIZE[0]:
                self.fishs[i] = 0 - 24, pyxel.rndi(0, SCREEN_SIZE[1]), sprite
                # pyxel.play(0, 0)
            else:
                self.fishs[i] = x + 1, y, sprite

    def draw_bg(self):
        pyxel.cls(1)
        sprite_change_frame = 16
        offset = pyxel.frame_count % sprite_change_frame
        halfframe = sprite_change_frame / 2

        new_bg = self.bg.copy()
        for i, fish_pos in enumerate(self.bg):
            spr = fish_pos[0] % 4 * 8
            fish2 = (0, spr, 0, 8, 8, 0)
            pyxel.blt(*fish_pos, *fish2)
            if offset == halfframe:
                new_fish = fish_pos[0] + 1, fish_pos[1]
                if new_fish[0] > SCREEN_SIZE[0] + 8: 
                    new_fish = 0, new_fish[1]
                new_bg[i] = new_fish

        self.bg = new_bg


App()
