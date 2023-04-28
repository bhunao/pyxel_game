import pyxel

SCREEN_SIZE = 160, 120
MID = SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2


def rndxy():
    return pyxel.rndi(0, SCREEN_SIZE[0]), pyxel.rndi(0, SCREEN_SIZE[1])


class App:
    def __init__(self) -> None:
        pyxel.init(*SCREEN_SIZE)
        pyxel.load("assets/fishing.pyxres")
        # pyxel.playm(0, loop=False)
        self.bg_pos = 100, 0
        self.bg = [rndxy() for _ in range(15)]
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        line_start = MID[0], 0
        line_end = MID

        hook = (0, 0, 0, 8, 8, 0)

        self.draw_bg()

        pyxel.line(*line_start, *line_end, 9)
        pyxel.blt(MID[0] - 7, MID[1], *hook)

    def draw_bg(self):
        pyxel.cls(1)
        sprite_change_frame = 18
        offset = pyxel.frame_count % sprite_change_frame
        halfframe = sprite_change_frame / 2

        new_bg = self.bg.copy()
        for i, fish_pos in enumerate(self.bg):
            spr = fish_pos[0] % 3 * 8
            fish2 = (0, 24, spr, 8, 8, 0)
            pyxel.blt(*fish_pos, *fish2)
            if offset == halfframe:
                new_fish = fish_pos[0] - 1, fish_pos[1]

                if new_fish[0] < -8:
                    new_fish = SCREEN_SIZE[0], new_fish[1]

                new_bg[i] = new_fish

        self.bg = new_bg


App()
