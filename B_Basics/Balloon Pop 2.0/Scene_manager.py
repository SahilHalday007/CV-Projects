import Menu, Game

def open_scene(scene_name):
    if scene_name == "Menu":
        Menu.Menu()
    elif scene_name == "Game":
        Game.Game()