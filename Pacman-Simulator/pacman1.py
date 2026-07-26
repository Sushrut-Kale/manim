from manim import *
import numpy as np
import random

PAC_YELLOW = "#FFFF00"
BLINKY_RED = "#FF0000"
PINKY_PINK = "#FFB8FF"
INKY_CYAN = "#00FFFF"
CLYDE_ORANGE = "#FFB852"
MAZE_BLUE = "#2121DE"
PELLET_COLOR = "#FFB8AE"
ARCADE_FONT = "Courier New" 

class PacMan(VGroup):
    def __init__(self, color=PAC_YELLOW, **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.upper = Sector(radius=0.5, start_angle=0, angle=PI, color=self.color)
        self.lower = Sector(radius=0.5, start_angle=PI, angle=PI, color=self.color)
        self.add(self.upper, self.lower)
        self.time = 0
        self.chomping = True
        self.base_angle = 0
        self.current_opening = 0
        self.add_updater(self.update_mouth)
    def update_mouth(self, m, dt):
        if not self.chomping:
            return
        self.time += dt * 15 
        target_opening = (np.sin(self.time) + 1) / 2 * 0.7
        diff = target_opening - self.current_opening
        center = m.get_center()
        m.upper.rotate(diff, about_point=center)
        m.lower.rotate(-diff, about_point=center)
        self.current_opening = target_opening
    def set_direction(self, vector):
        target_angle = np.arctan2(vector[1], vector[0])
        angle_diff = target_angle - self.base_angle
        self.rotate(angle_diff, about_point=self.get_center())
        self.base_angle = target_angle
        return self
class Ghost(VGroup):
    def __init__(self, color=BLINKY_RED, **kwargs):
        super().__init__(**kwargs)
        head = Sector(radius=0.4, start_angle=0, angle=PI, color=color).shift(UP*0.1)
        body = Rectangle(width=0.8, height=0.4, color=color, fill_opacity=1, stroke_width=0)
        body.next_to(head, DOWN, buff=0) 
        skirt = VGroup(
            Circle(radius=0.133, color=color, fill_opacity=1, stroke_width=0),
            Circle(radius=0.133, color=color, fill_opacity=1, stroke_width=0),
            Circle(radius=0.133, color=color, fill_opacity=1, stroke_width=0)
        ).arrange(RIGHT, buff=0).next_to(body, DOWN, buff=0)
        eye_l = Circle(radius=0.12, color=WHITE, fill_opacity=1, stroke_width=0).move_to(head.get_center() + LEFT*0.15 + DOWN*0.1)
        eye_r = Circle(radius=0.12, color=WHITE, fill_opacity=1, stroke_width=0).move_to(head.get_center() + RIGHT*0.15 + DOWN*0.1)
        pupil_l = Circle(radius=0.06, color=MAZE_BLUE, fill_opacity=1, stroke_width=0).move_to(eye_l.get_center() + RIGHT*0.04)
        pupil_r = Circle(radius=0.06, color=MAZE_BLUE, fill_opacity=1, stroke_width=0).move_to(eye_r.get_center() + RIGHT*0.04)
        self.add(head, body, skirt, eye_l, eye_r, pupil_l, pupil_r)
class PacManSimulator(Scene):
    def construct(self):
        self.matrix_binary_intro()
        self.intro_scene()
        self.loading_scene()
        self.character_intro()
        self.chase_scene_1()
        self.score_system()
        self.chase_scene_2()
        self.maze_gameplay()
    def transition_clean(self):
        self.play(FadeOut(Group(*self.mobjects)))
        self.clear()
    def matrix_binary_intro(self):
        self.camera.background_color = "#000500"
        COLORS = ["#FFFFFF", "#99FF99", "#00FF41", "#008F11", "#003B00"]
        FONT_SIZE = 22
        COLS = 40  
        SPACING_X = 0.35
        COLUMN_SPEEDS = [random.uniform(1.5, 4.0) for _ in range(COLS)]
        all_columns = VGroup()
        for c in range(COLS):
            column = VGroup()
            trail_length = random.randint(15, 25)
            for r in range(trail_length):
                char = random.choice(["0", "1"])
                color_index = min(r, len(COLORS) - 1)
                digit = Text(char, font="Monospace", font_size=FONT_SIZE, color=COLORS[color_index])
                digit.move_to([c * SPACING_X - (COLS * SPACING_X / 2), r * 0.4, 0])
                column.add(digit)
            column.shift(UP * random.uniform(0, 10))
            column.speed = COLUMN_SPEEDS[c]
            all_columns.add(column)
        self.add(all_columns)
        def update_rain(mobs, dt):
            for col in mobs:
                col.shift(DOWN * col.speed * dt)
                if col.get_top()[1] < -5:
                    col.set_y(random.uniform(6, 10))
                    for digit in col:
                        if random.random() > 0.8:
                            new_char = random.choice(["0", "1"])
                            digit.become(Text(new_char, font="Monospace", font_size=FONT_SIZE, color=digit.color).move_to(digit.get_center()))
        all_columns.add_updater(update_rain)
        self.wait(5)
        all_columns.remove_updater(update_rain)
        self.play(FadeOut(all_columns, run_time=2))
    def intro_scene(self):
        try:
            pacman_logo = ImageMobject("PacManBF-title.png") #
        except Exception:
            pacman_logo = Text("IMAGE NOT FOUND", color=RED)  
        pacman_logo.scale(3.5)
        pacman_logo.center()
        self.play(FadeIn(pacman_logo, run_time=1.5))
        self.wait(2)
        self.play(FadeOut(pacman_logo, run_time=1.5))
        self.wait(0.5)
    def loading_scene(self):
        loading_text = Text("LOADING...", font=ARCADE_FONT, color=WHITE).scale(1.2).shift(UP*1)
        bar_outline = Rectangle(width=6, height=0.5, color=WHITE)
        bar_fill = Rectangle(width=6, height=0.5, color=PAC_YELLOW, fill_opacity=1).align_to(bar_outline, LEFT)
        mask = Rectangle(width=6.1, height=0.6, color=BLACK, fill_opacity=1).move_to(bar_outline)
        pm = PacMan().scale(0.5).next_to(bar_outline, LEFT, buff=0)
        self.add(loading_text, bar_fill, mask, bar_outline, pm)
        self.play(mask.animate.shift(RIGHT*6), pm.animate.shift(RIGHT*6.5), run_time=2, rate_func=linear)
        self.transition_clean()
    def character_intro(self):
        header = Text("CHARACTER / NICKNAME", font=ARCADE_FONT, color=WHITE).scale(0.6).to_edge(UP, buff=1)
        self.add(header)
        ghost_data = [
            (BLINKY_RED, "SHADOW", "BLINKY"),
            (PINKY_PINK, "SPEEDY", "PINKY"),
            (INKY_CYAN, "BASHFUL", "INKY"),
            (CLYDE_ORANGE, "POKEY", "CLYDE")
        ]
        text_rows = VGroup()
        for i, (color, char, nick) in enumerate(ghost_data):
            g_list = Ghost(color).scale(0.4)
            g_list.add_updater(lambda m, dt, i=i: m.shift(UP * 0.05 * np.sin(self.time * 3 + i)))
            def update_list_eyes(m, dt):
                offset = 0.04 if int(self.time) % 2 == 0 else -0.04
                m[5].set_x(m[3].get_x() + offset) 
                m[6].set_x(m[4].get_x() + offset)
            g_list.add_updater(update_list_eyes)
            row = VGroup(
                g_list,
                Text(f"- {char}", font=ARCADE_FONT, color=color).scale(0.5),
                Text(f'"{nick}"', font=ARCADE_FONT, color=color).scale(0.5)
            ).arrange(RIGHT, buff=0.6)
            text_rows.add(row)        
        text_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5).center().shift(UP*0.2)
        self.play(
            LaggedStart(*[FadeIn(row, shift=UP*0.3) for row in text_rows], lag_ratio=0.2)
        )
        self.wait(4)       
        for m in self.mobjects: m.clear_updaters()
        self.transition_clean()
    def chase_scene_1(self):
        self._run_chase(speed_multiplier=1.0)
        self.transition_clean()
    def score_system(self):
        small_p = Circle(radius=0.1, color=PELLET_COLOR, fill_opacity=1)
        big_p = Circle(radius=0.25, color=PELLET_COLOR, fill_opacity=1)
        ghost_p = Ghost(INKY_CYAN).scale(0.6)
        items = VGroup(small_p, big_p, ghost_p).arrange(DOWN, buff=1.5).shift(RIGHT*2)
        pm = PacMan().scale(0.6)
        self.add(items, pm)
        score_descriptions = ["Small Pellet = +10 Points", "Power Pellet = +50 Points", "Ghost Hit = -100 Points"]
        for i, (item, score, color) in enumerate(zip(items, ["+10", "+50", "-100"], [WHITE, WHITE, BLINKY_RED])):
            pm.move_to(item.get_center() + LEFT*4)
            pm.set_direction([1, 0, 0])
            desc = Text(score_descriptions[i], font=ARCADE_FONT, color=WHITE).scale(0.5).to_edge(DOWN, buff=1)
            self.play(FadeIn(desc))
            self.play(pm.animate.move_to(item.get_center()), run_time=0.8)
            t = Text(score, font=ARCADE_FONT, color=color).scale(0.6).move_to(item)
            self.play(FadeOut(item), FadeIn(t, shift=UP*0.5), run_time=0.3)
            self.wait(0.5)
            self.play(FadeOut(desc))
        self.transition_clean()
    def chase_scene_2(self):
        self._run_chase(speed_multiplier=1.6)
        self.transition_clean()
    def _run_chase(self, speed_multiplier):
        pm = PacMan().scale(0.8)
        pm.set_direction([-1, 0, 0])
        ghosts = VGroup(*[Ghost(c).scale(0.8) for c in [BLINKY_RED, PINKY_PINK, INKY_CYAN, CLYDE_ORANGE]])
        ghosts.arrange(RIGHT, buff=0.5)
        group = VGroup(pm, ghosts).arrange(RIGHT, buff=2.0)
        group.move_to(RIGHT * 12)
        self.add(group)
        self.play(group.animate.move_to(LEFT * 12), run_time=4 / speed_multiplier, rate_func=linear)
    def maze_gameplay(self):
        ready_text = Text("READY!", font=ARCADE_FONT, color=PAC_YELLOW).scale(1.5)
        self.play(Write(ready_text))
        self.play(ready_text.animate.scale(0.1).set_opacity(0), run_time=0.5)
        self.wait(1)
