import pyxel


SCREEN_SIZE = 160, 120
MID = SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2


def center_rect(rect, pos):
    return pos[0] - rect[0] / 2, pos[1] - rect[1] / 2


class App:
    def __init__(self) -> None:
        pyxel.init(*SCREEN_SIZE)
        self.x = 0
        pyxel.run(self.update, self.draw)


    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()


    def draw(self):
        pyxel.cls(0)
        rect_size = 20, 20
        rect_pos = center_rect(rect_size, MID)
        pyxel.rect(*rect_pos, *rect_size, 11)
        pyxel.circb(*MID, 50, 7)


App()
