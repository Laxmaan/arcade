"""
Starting Template Simple

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template_simple
"""
import arcade

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
SCREEN_TITLE = "GUI Example"

import logging

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.WHITE)

        logging.basicConfig(level=logging.DEBUG)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        ui_element = arcade.experimental.gui.flat_button.FlatButton(center_x=50, center_y=50, width=90, height=50)
        self.ui_manager.append(ui_element)
        ui_element = arcade.experimental.gui.flat_button.FlatButton(center_x=50, center_y=150, width=90, height=50)
        self.ui_manager.append(ui_element)
        ui_element = arcade.experimental.gui.flat_button.FlatButton(center_x=50, center_y=250, width=90, height=50)
        self.ui_manager.append(ui_element)

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()

        self.ui_manager.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """
        print("Click Window")


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()