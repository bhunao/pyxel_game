from dataclasses import dataclass
from typing import Sequence, Tuple

import esper
import pyxel

SCREEN_SIZE = 360, 240
MID = SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2

# sprites
#   image, u, v, w, h, colkey
FISH1 = 0, 0, 32, 24, 16, 0
FISH2 = 0, 0, 48, 24, 16, 0
HOOK = (0, 0, 8, 8, 8, 0)

#   image, u, v, w, h, colkey
IMAGE = Tuple[int, int, int, int, int, int]


def rndxy():
    return pyxel.rndi(0, SCREEN_SIZE[0]), pyxel.rndi(0, SCREEN_SIZE[1])


@dataclass
class AnimatedSpriteComponent:
    x: int
    y: int
    images: Sequence[IMAGE]


@dataclass
class VelocityComponent:
    x: int = 1
    y: int = 0

@dataclass
class PlayerComponent:
    pass


class MovementSystem(esper.Processor):
    def __init__(self) -> None:
        super().__init__()

    def process(self):
        for ent, (render, velocity) in self.world.get_components(AnimatedSpriteComponent, VelocityComponent):
            render = render
            render.x += velocity.x
            render.y += velocity.y

            sprite = render.images[pyxel.frame_count % len(render.images)]
            if render.x - sprite[3] > SCREEN_SIZE[0]:
                render.x = 0 - sprite[3]
                render.y = pyxel.rndi(0, SCREEN_SIZE[1])
                velocity.x = pyxel.rndi(1, 3)


class AnimatedSpriteSystem(esper.Processor):
    def __init__(self) -> None:
        super().__init__()

    def process(self):
        for ent, (render) in self.world.get_components(AnimatedSpriteComponent):
            render = render[0]

            sprite = render.images[pyxel.frame_count % len(render.images)]
            pyxel.blt(render.x, render.y, *sprite)

class KeyboardInputProcessor(esper.Processor):
    def __init__(self) -> None:
        super().__init__()
    
    def send_player_pos(self, client, render):
        client.send(str(render.__dict__))


    def process(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        for ent, (render, player) in self.world.get_components(AnimatedSpriteComponent, PlayerComponent):
            if pyxel.btn(pyxel.KEY_LEFT):
                render.x -= 1
            if pyxel.btn(pyxel.KEY_RIGHT):
                render.x += 1
            if pyxel.btn(pyxel.KEY_UP):
                render.y -= 1
            if pyxel.btn(pyxel.KEY_DOWN):
                render.y += 1
            if pyxel.btn(pyxel.KEY_SPACE):
                pass

class App:
    def __init__(self) -> None:
        pyxel.init(*SCREEN_SIZE)
        pyxel.load("assets/fishing2.pyxres")
        pyxel.playm(0, loop=True)

        self.world = esper.World()
        self.world.add_processor(AnimatedSpriteSystem())
        self.world.add_processor(MovementSystem())
        self.world.add_processor(KeyboardInputProcessor())
        self.spawn_entities()

        self.world.create_entity(
            AnimatedSpriteComponent(
                0, 0,
                [FISH1]
            ),
            PlayerComponent()
        )

        

        pyxel.run(self.update, self.draw)
    
    def spawn_entities(self):
        for _ in range(20):
            self.world.create_entity(
                AnimatedSpriteComponent(
                    *rndxy(),
                    [(0, i * 8, 0, 8, 8, 0) for i in range(4)]
                ),
                VelocityComponent(x=pyxel.rndi(1, 3))
            )

        for _ in range(10):
            self.world.create_entity(
                AnimatedSpriteComponent(
                    *rndxy(),
                    [FISH1]
                ),
                VelocityComponent(x=pyxel.rndi(1, 4))
            )


    def update(self):
        return
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(1)

        line_start = MID[0], 0
        pyxel.line(*line_start, *MID, 9)
        pyxel.blt(MID[0] - 7, MID[1], *HOOK)
        self.world.process()


App()
