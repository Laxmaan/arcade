import arcade
import pymunk
import random
import timeit
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800


class CircleSprite(arcade.Sprite):
    def __init__(self, filename, pymunk_shape):
        super().__init__(filename, center_x=pymunk_shape.body.position.x, center_y=pymunk_shape.body.position.y)
        self.width = pymunk_shape.radius * 2
        self.height = pymunk_shape.radius * 2
        self.pymunk_shape = pymunk_shape

class MyApplication(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height)
        self.sprite_list = arcade.SpriteList()
        self.ball_list = arcade.SpriteList()
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        # -- Pymunk
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -900.0)

        ## Balls
        # self.balls = []
        self.static_lines = []

        self.ticks_to_next_ball = 10

        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, [0, 10], [SCREEN_WIDTH, 10], 0.0)
        shape.friction = 10
        self.space.add(shape)
        self.static_lines.append(shape)

        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, [SCREEN_WIDTH - 50, 10], [SCREEN_WIDTH, 30], 0.0)
        shape.friction = 10
        self.space.add(shape)
        self.static_lines.append(shape)

        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, [50, 10], [0, 30], 0.0)
        shape.friction = 10
        self.space.add(shape)
        self.static_lines.append(shape)

        radius = 20
        separation = 150
        for row in range(6):
            for column in range(6):
                x = column * separation + (separation // 2 * (row % 2))
                y = row * separation + separation // 2
                body = pymunk.Body(body_type=pymunk.Body.STATIC)
                body.position = x, y
                shape = pymunk.Circle(body, radius, pymunk.Vec2d(0, 0))
                shape.friction = 0.3
                self.space.add(body, shape)

                sprite = CircleSprite("images/bumper.png", shape)
                self.sprite_list.append(sprite)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        draw_start_time = timeit.default_timer()
        self.sprite_list.draw()

        for line in self.static_lines:
            body = line.body

            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            arcade.draw_line(pv1.x, pv1.y, pv2.x, pv2.y, arcade.color.WHITE, 2)

        draw_time = timeit.default_timer() - draw_start_time
        arcade.draw_text("Processing time: {:.3f}".format(self.time), 20, SCREEN_HEIGHT - 20, arcade.color.BLACK, 12)
        arcade.draw_text("Drawing time: {:.3f}".format(draw_time), 20, SCREEN_HEIGHT - 40, arcade.color.BLACK, 12)

    def animate(self, delta_time):
        start_time = timeit.default_timer()

        self.ticks_to_next_ball -= 1
        if self.ticks_to_next_ball <= 0:
            self.ticks_to_next_ball = 20
            mass = 0.5
            radius = 15
            inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
            body = pymunk.Body(mass, inertia)
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT
            body.position = x, y
            shape = pymunk.Circle(body, radius, pymunk.Vec2d(0, 0))
            shape.friction=0.3
            self.space.add(body, shape)

            sprite = CircleSprite("images/coin_01.png", shape)
            self.sprite_list.append(sprite)
            self.ball_list.append(sprite)

        # Check for balls that fall off the screen
        for ball in self.ball_list:
            if ball.pymunk_shape.body.position.y < 0:
                # Remove balls from physics space
                self.space.remove(ball.pymunk_shape, ball.pymunk_shape.body)
                # Remove balls from physics list
                ball.kill()

        # Update physics
        self.space.step(1 / 80.0)

        # Move sprites to where physics objects are
        for ball in self.ball_list:
            ball.center_x = ball.pymunk_shape.body.position.x
            ball.center_y = ball.pymunk_shape.body.position.y
            ball.angle = math.degrees(ball.pymunk_shape.body.angle)

        self.time = timeit.default_timer() - start_time

window = MyApplication(SCREEN_WIDTH, SCREEN_HEIGHT)

arcade.run()