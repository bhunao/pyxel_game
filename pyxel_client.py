from dataclasses import dataclass
import json
from typing import Sequence, Tuple
from uuid import uuid1
from client import Client

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
    name: str = "Player"


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
            print(render, "sprite")
            pyxel.blt(render.x, render.y, *sprite)


class ConnectionSystem(esper.Processor):
    def __init__(self) -> None:
        pass

    def process(self):
        for ent, (client, player) in self.world.get_components(Client, PlayerComponent):
            if pyxel.frame_count % 2 == 0:
                connection_result = client.connection()
                if connection_result:
                    username, message = connection_result
                    print(type(message))
                    message = message.replace("'", '"')
                    message = message.replace("(", "[")
                    message = message.replace(")", "]")
                    print("qwerty:", message)
                    message_dict = json.loads(message)
                    self.world.create_entity(
                        PlayerComponent(username),
                        AnimatedSpriteComponent(
                            message_dict[0], message_dict[1],
                            message_dict[2]
                        )
                    )


class KeyboardInputProcessor(esper.Processor):
    def __init__(self) -> None:
        super().__init__()

    def send_player_pos(self, client, render):
        values = render.__dict__
        values = [values["x"], values["y"], list(*values["images"])]
        client.send(str(values))

    def process(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        for ent, (render, client, player) in self.world.get_components(AnimatedSpriteComponent, Client, PlayerComponent):
            if pyxel.btn(pyxel.KEY_LEFT):
                self.send_player_pos(client, render)
                render.x -= 1
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.send_player_pos(client, render)
                render.x += 1
            if pyxel.btn(pyxel.KEY_UP):
                self.send_player_pos(client, render)
                render.y -= 1
            if pyxel.btn(pyxel.KEY_DOWN):
                self.send_player_pos(client, render)
                render.y += 1
            if pyxel.btn(pyxel.KEY_SPACE):
                self.send_player_pos(client, render)


class App:
    def __init__(self) -> None:
        pyxel.init(*SCREEN_SIZE)
        pyxel.load("assets/fishing2.pyxres")
        # pyxel.playm(0, loop=True)

        self.world = esper.World()
        self.world.add_processor(AnimatedSpriteSystem())
        self.world.add_processor(MovementSystem())
        self.world.add_processor(ConnectionSystem())
        self.world.add_processor(KeyboardInputProcessor())

        connection = Client(str(uuid1()))
        self.world.create_entity(
            connection,
            AnimatedSpriteComponent(
                0, 0,
                [FISH2]
            ),
            PlayerComponent()
        )

        pyxel.run(self.update, self.draw)

    def update(self):
        return

    def draw(self):
        pyxel.cls(1)

        line_start = MID[0], 0
        pyxel.line(*line_start, *MID, 9)
        pyxel.blt(MID[0] - 7, MID[1], *HOOK)
        self.world.process()


App()
