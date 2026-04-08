# SceneManager.py - With Mode Selector

import GameGreenLight
import GameCookieCutter
import Menu
from time import sleep


def OpenScene(sceneName):
    """Scene management system"""


    if sceneName == 'Menu':
        Menu.Menu()

    # elif sceneName == "GameGreenLight":
    #     GameGreenLight.Game()

    elif sceneName == "GameGreenLightSingle":
        from GameGreenLight import GameGreenLightSingleplayer
        GameGreenLightSingleplayer()

    elif sceneName == "GameGreenLightMulti":
        from GameGreenLight import GameGreenLightMultiplayer
        GameGreenLightMultiplayer()

    elif sceneName == "GameGreenLightMode":
        # Mode selector screen
        from GameModeSelector import GameModeSelector
        GameModeSelector()

    elif sceneName == "GameCookieCutter":
        GameCookieCutter.Game()


if __name__ == "__main__":
    OpenScene("Menu")