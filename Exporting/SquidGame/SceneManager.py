import GameGreenLight,GameCookieCutter, Menu
from time import sleep


def OpenScene(sceneName):
    sleep(0.25)
    if sceneName == 'Menu':
        Menu.Menu()
    elif sceneName == "GameGreenLight":
        GameGreenLight.Game()
    elif sceneName == "GameCookieCutter":
        GameCookieCutter.Game()
