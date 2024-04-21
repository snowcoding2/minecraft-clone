import ursina.prefabs.first_person_controller
from perlin_noise import PerlinNoise
from ursina import *
import Game
import threading

if __name__ == "__main__":
    app = Ursina()

    seed = 420
    noises = [PerlinNoise(12, seed), PerlinNoise(6, seed), PerlinNoise(24, seed), PerlinNoise(3, seed)]

    game = Game.Game(ursina.prefabs.first_person_controller.FirstPersonController(gravity=0), noises)
    game.start()

    t1 = threading.Thread(target=game.render())
    t2 = threading.Thread(target=app.run())

    # ursina functions can't make oop
    def update():
        game.update()


    def input(key):
        if key == 'left mouse down':
            game.break_block()
        elif key == 'right mouse down':
            game.place_block()


    app.run()
