from manim import *
import numpy as np
import random

class Pong(Scene):
    def construct(self):
        self.add_sound("game_start.mpeg")
        txt = Text("PONG", color="GOLD")
        self.play(Write(txt), run_time=2)
        self.play(FadeOut(txt))
        self.wait(0.5)
        rect1 = Rectangle(height=2, width=0.2, color=PURPLE).move_to(LEFT * 7)
        rect2 = Rectangle(height=2, width=0.2, color=PURPLE).move_to(RIGHT * 7)
        rect1.set_fill(BLACK, opacity=1)
        rect2.set_fill(BLACK, opacity=1)
        rect1.blink_time = 0
        rect2.blink_time = 0
        self.add(rect1, rect2)
        t = 0
        def leftupdate(mob, dt):
            nonlocal t
            t += dt
            mob.set_y(np.sin(t * 2) * 2.2)
        def rightupdate(mob, dt):
            mob.set_y(np.sin(t * 2 + PI) * 2.2)
        rect1.add_updater(leftupdate)
        rect2.add_updater(rightupdate)
        def blink_updater(mob, dt):
            if mob.blink_time > 0:
                mob.blink_time -= dt
                mob.set_fill(ORANGE, opacity=1)
            else:
                mob.set_fill(BLACK, opacity=1)
        rect1.add_updater(blink_updater)
        rect2.add_updater(blink_updater)
        ball = Circle(radius=0.5, color=WHITE).move_to(ORIGIN)
        ball.set_fill(GREEN_A, opacity=0.5)
        self.add(ball)
        velocity = np.array([3, 2, 0])
        reset_cooldown = 0
        game_over_timer = 0  
        colors = [RED, GREEN_A, BLUE, YELLOW, ORANGE, PURPLE, PINK]
        game_text = Text("GAME OVER", font_size=72, color=YELLOW)
        game_text.set_opacity(0)
        self.add(game_text)
        def reset_ball():
            self.add_sound("game_end.mpeg")
            nonlocal velocity, reset_cooldown
            ball.move_to(ORIGIN)
            ball.set_fill(random.choice(colors), opacity=0.7)
            angle = random.uniform(-PI/3, PI/3)
            direction = random.choice([-1, 1])
            speed = 3.7
            velocity = np.array([
                direction * np.cos(angle) * speed,
                np.sin(angle) * speed,
                0
            ])
            reset_cooldown = 0.5
        def ballupdate(mob, dt):
            nonlocal velocity, reset_cooldown, game_over_timer
            if reset_cooldown > 0:
                reset_cooldown -= dt
                return
            mob.shift(velocity * dt)
            if mob.get_top()[1] >= 3.5:
                velocity[1] *= -1
                self.add_sound("bounce.mpeg")
                mob.set_y(3.5 - mob.radius)
                mob.scale(0.8)
            if mob.get_bottom()[1] <= -3.5:
                velocity[1] *= -1
                self.add_sound("bounce.mpeg")
                mob.set_y(-3.5 + mob.radius)
                mob.scale(0.8)
            if (
                mob.get_right()[0] >= rect2.get_left()[0]
                and rect2.get_bottom()[1] <= mob.get_y() <= rect2.get_top()[1]
            ):
                velocity[0] *= -1
                self.add_sound("bounce.mpeg")
                rect2.blink_time = 0.12
                mob.set_x(rect2.get_left()[0] - mob.radius)
                mob.scale(1.2)
            if (
                mob.get_left()[0] <= rect1.get_right()[0]
                and rect1.get_bottom()[1] <= mob.get_y() <= rect1.get_top()[1]
            ):
                velocity[0] *= -1
                self.add_sound("bounce.mpeg")
                rect1.blink_time = 0.12
                mob.set_x(rect1.get_right()[0] + mob.radius)
                mob.scale(1.2)
            if mob.get_left()[0] > rect2.get_right()[0]:
                game_text.set_opacity(1)
                game_over_timer = 0.2
                reset_ball()
            if mob.get_right()[0] < rect1.get_left()[0]:
                game_text.set_opacity(1)
                game_over_timer = 0.2
                reset_ball()
            if game_over_timer > 0:
                game_over_timer -= dt
                if game_over_timer <= 0:
                    game_text.set_opacity(0)
        ball.add_updater(ballupdate)
        self.wait(25)
