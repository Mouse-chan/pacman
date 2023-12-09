import pyray
import raylib
from raylib import colors

from objects.text import Text
from scenes.base import BaseScene
from settings import Settings

from game_objects.pacman import PacmanLogic
from game_objects.pole import LogicPole
from game_objects.cell import Cell
from game_objects.field import FieldDrawer
from game_objects.pacman import Pacman
from game_objects.seeds import *

from objects.button_menu import ButtonMenu
from objects.button_pause import ButtonPause

from objects.figure import *

from objects.counter import Counter


class GameScene(BaseScene):  # Сцена 2
    def __init__(self):
        # self.hello_text = Text(Settings.WIDTH // 2, Settings.HEIGHT // 2, "Game", 32, colors.GREEN)
        self.pole = LogicPole()
        self.pac = self.pole.pacman.image_pacman
        self.button_menu = ButtonMenu()
        self.button_pause = ButtonPause()

        self.rec = Rect((Settings.WIDTH - 17 * 30) // 2, (Settings.HEIGHT - 21 * 30) // 2,
                        Settings.WIDTH - (Settings.WIDTH - 17 * 30), Settings.HEIGHT - (Settings.HEIGHT - 21 * 30),
                        colors.BLUE, True)

        self.field_drawer = FieldDrawer(self.pole.data)
        self.seeds = SeedsLogic()

        self.gameover_text = Text(Settings.WIDTH // 2 - 270, Settings.HEIGHT // 2 - 50, "GAME OVER", 100,
                               colors.RED)
        self.rec_gameover = Rect((Settings.WIDTH - 17 * 30) // 2, (Settings.HEIGHT - 21 * 30) // 2,
                        Settings.WIDTH - (Settings.WIDTH - 17 * 30), Settings.HEIGHT - (Settings.HEIGHT - 21 * 30),
                        (0, 0, 0, 160), False)

        self.counter = Counter(300, 30)

        super().__init__()

    def set_up_objects(self):
        self.objects.append(self.pole)
        self.objects.append(self.button_menu)
        self.objects.append(self.button_pause)
        # self.objects.append(self.rec)
        self.objects.append(self.field_drawer)
        self.objects.append(self.pac)
        self.objects.append(self.seeds)
        """self.objects.append(self.cell0)
        self.objects.append(self.cell1)
        self.objects.append(self.cell2)"""
        #self.objects.append(self.rec_gameover)
        #self.objects.append(self.gameover_text)
        self.objects.append(self.counter)

    def additional_process_event(self):
        if pyray.is_key_pressed(pyray.KeyboardKey.KEY_ZERO):
            Settings.set_scene(0)
        if pyray.is_key_pressed(pyray.KeyboardKey.KEY_ONE):
            Settings.set_scene(1)
        if pyray.is_key_pressed(pyray.KeyboardKey.KEY_THREE):
            Settings.set_scene(3)

        for i in range(len(self.seeds.seeds)):
            c1 = self.seeds.seeds[i].get_center()
            c2 = self.pac.get_center()
            r1 = self.seeds.seeds[i].get_radius()
            r2 = self.pac.get_radius()

            # print(c1, r1, c2, r2)
            if pyray.check_collision_circles(c1, r1, c2, r2):
                # TODO: seed eaten
                self.seeds.seeds[i].eaten(self.counter)
                self.seeds.seeds.remove(self.seeds.seeds[i])
                break
        # TODO: Если зёрен не осталось, победа
        if len(self.seeds.seeds) <= 0:
            self.objects.append(self.rec_gameover)
            self.objects.append(self.gameover_text)
            Settings.is_gameover = True

