from manim import *
import numpy as np


class StickFigure(VGroup):
    """A stick figure built from Manim primitives."""

    def __init__(self, color=WHITE, scale_factor=1.0, **kwargs):
        super().__init__(**kwargs)
        self.fig_color = color
        self.sf = scale_factor

        # Head
        self.head = Circle(radius=0.18 * self.sf, color=color, stroke_width=2.5)
        self.head.set_fill(BLACK, opacity=0)

        # Body
        self.body = Line(
            self.head.get_bottom(),
            self.head.get_bottom() + DOWN * 0.55 * self.sf,
            color=color, stroke_width=2.5
        )

        body_bottom = self.body.get_end()

        # Left arm
        self.left_arm = Line(
            self.body.get_start() + DOWN * 0.12 * self.sf,
            self.body.get_start() + DOWN * 0.12 * self.sf + LEFT * 0.28 * self.sf + DOWN * 0.18 * self.sf,
            color=color, stroke_width=2.2
        )

        # Right arm
        self.right_arm = Line(
            self.body.get_start() + DOWN * 0.12 * self.sf,
            self.body.get_start() + DOWN * 0.12 * self.sf + RIGHT * 0.28 * self.sf + DOWN * 0.18 * self.sf,
            color=color, stroke_width=2.2
        )

        # Left leg
        self.left_leg = Line(
            body_bottom,
            body_bottom + LEFT * 0.22 * self.sf + DOWN * 0.40 * self.sf,
            color=color, stroke_width=2.2
        )

        # Right leg
        self.right_leg = Line(
            body_bottom,
            body_bottom + RIGHT * 0.22 * self.sf + DOWN * 0.40 * self.sf,
            color=color, stroke_width=2.2
        )

        self.add(self.head, self.body, self.left_arm, self.right_arm,
                 self.left_leg, self.right_leg)

    def get_feet_center(self):
        left_foot = self.left_leg.get_end()
        right_foot = self.right_leg.get_end()
        return (left_foot + right_foot) / 2


class SushrutScene(MovingCameraScene):
    def construct(self):
        # ── Camera / background ──────────────────────────────────────────────
        self.camera.background_color = "#0d0d0d"
        self.camera.frame.save_state()

        # Ground line
        ground = Line(LEFT * 8, RIGHT * 8, color=GREY, stroke_width=1.5, stroke_opacity=0.4)
        ground.move_to(DOWN * 1.5)
        self.add(ground)

        # ── Build stick figure ───────────────────────────────────────────────
        figure = StickFigure(color=WHITE, scale_factor=1.0)
        figure.move_to(LEFT * 6 + UP * 0.08)

        self.play(Create(figure), run_time=0.6)

        # ── Walking from LEFT → CENTER ────────────────────────────────────────
        walk_tracker = ValueTracker(0)
        start_x = -6.0
        end_x = 0.0
        walk_duration = 3.5

        def walking_updater(mob):
            t = walk_tracker.get_value()
            # Horizontal position
            x = start_x + (end_x - start_x) * t

            # Oscillation phase (cycle every ~0.6 units)
            phase = t * walk_duration * TAU * 2.0

            # Leg swing
            leg_swing = 0.18 * np.sin(phase)
            arm_swing = 0.12 * np.sin(phase + PI)

            body_bottom = figure.body.get_end()

            figure.left_leg.put_start_and_end_on(
                body_bottom,
                body_bottom + np.array([-0.22 + leg_swing, -0.40, 0])
            )
            figure.right_leg.put_start_and_end_on(
                body_bottom,
                body_bottom + np.array([0.22 - leg_swing, -0.40, 0])
            )

            arm_base = figure.body.get_start() + DOWN * 0.12
            figure.left_arm.put_start_and_end_on(
                arm_base,
                arm_base + np.array([-0.28 + arm_swing, -0.18, 0])
            )
            figure.right_arm.put_start_and_end_on(
                arm_base,
                arm_base + np.array([0.28 - arm_swing, -0.18, 0])
            )

            mob.move_to(np.array([x, 0.08, 0]))

        figure.add_updater(walking_updater)
        self.play(walk_tracker.animate.set_value(1), run_time=walk_duration,
                  rate_func=linear)
        figure.remove_updater(walking_updater)

        # Re-settle legs/arms to neutral
        body_bottom = figure.body.get_end()
        arm_base = figure.body.get_start() + DOWN * 0.12
        figure.left_leg.put_start_and_end_on(body_bottom, body_bottom + np.array([-0.22, -0.40, 0]))
        figure.right_leg.put_start_and_end_on(body_bottom, body_bottom + np.array([0.22, -0.40, 0]))
        figure.left_arm.put_start_and_end_on(arm_base, arm_base + np.array([-0.28, -0.18, 0]))
        figure.right_arm.put_start_and_end_on(arm_base, arm_base + np.array([0.28, -0.18, 0]))
        figure.move_to(ORIGIN + UP * 0.08)

        # ── "Hello, I am Sushrut" text ────────────────────────────────────────
        greeting = Text("Hello, I am Sushrut", font_size=30, color=YELLOW_B)
        greeting.next_to(figure, UP, buff=0.45)

        self.play(Write(greeting), run_time=1.2)
        self.wait(1.2)

        # ── Camera zoom-out to reveal full stage ─────────────────────────────
        self.play(
            self.camera.frame.animate.set_width(18),
            run_time=0.8, rate_func=smooth
        )

        # ── Fade out greeting ────────────────────────────────────────────────
        self.play(FadeOut(greeting), run_time=0.5)

        # ── Water waves spawning from LEFT ────────────────────────────────────
        wave_colors = [BLUE_E, BLUE_D, BLUE_C, TEAL_E, BLUE_B]
        num_waves = 5
        wave_width = 16
        wave_amplitude = [0.18, 0.22, 0.15, 0.25, 0.12]
        wave_freq = [1.8, 2.2, 1.5, 2.6, 1.2]
        wave_y_offsets = [-1.3, -1.55, -1.1, -1.7, -0.95]

        water_tracker = ValueTracker(-9.0)   # x-offset of wave front

        def make_wave_updater(amp, freq, y_off, color, lag):
            def updater(mob):
                x0 = water_tracker.get_value() - lag
                pts = []
                for i in range(120):
                    xi = x0 + i * (wave_width / 119)
                    yi = y_off + amp * np.sin(freq * xi + water_tracker.get_value() * 3)
                    pts.append([xi, yi, 0])
                mob.set_points_as_corners(pts)
                mob.set_stroke(color=color, width=2.5, opacity=0.85)
            return updater

        waves = []
        for i in range(num_waves):
            wave = VMobject()
            wave.set_points_as_corners([[0, 0, 0], [0.01, 0, 0]])
            wave.set_stroke(color=wave_colors[i], width=2.5)
            self.add(wave)
            updater_fn = make_wave_updater(
                wave_amplitude[i], wave_freq[i],
                wave_y_offsets[i], wave_colors[i],
                lag=i * 0.3
            )
            wave.add_updater(updater_fn)
            waves.append(wave)

        # Water surface (filled polygon for volume feel)
        water_fill = VMobject()
        water_fill.set_points_as_corners([[0, 0, 0], [0.01, 0, 0]])

        def water_fill_updater(mob):
            x0 = water_tracker.get_value()
            top_pts = []
            for i in range(80):
                xi = x0 + i * (wave_width / 79)
                yi = -1.2 + 0.20 * np.sin(1.8 * xi + water_tracker.get_value() * 3)
                top_pts.append([xi, yi, 0])
            bottom_pts = [[top_pts[-1][0], -2.5, 0], [top_pts[0][0], -2.5, 0]]
            all_pts = top_pts + bottom_pts
            mob.set_points_as_corners(all_pts)
            mob.set_fill(BLUE_E, opacity=0.25)
            mob.set_stroke(width=0)

        water_fill.add_updater(water_fill_updater)
        self.add(water_fill)

        # Animate water rushing in — figure notices and starts running
        run_tracker = ValueTracker(0)
        run_start_x = 0.0
        run_end_x = 10.0

        def running_updater(mob):
            t = run_tracker.get_value()
            x = run_start_x + (run_end_x - run_start_x) * t

            # Fast leg/arm oscillation
            phase = t * 14 * TAU

            leg_swing = 0.28 * np.sin(phase)
            arm_swing = 0.20 * np.sin(phase + PI)
            leg_lift = abs(0.12 * np.sin(phase))

            body_bottom = figure.body.get_end()
            arm_base_pt = figure.body.get_start() + DOWN * 0.12

            figure.left_leg.put_start_and_end_on(
                body_bottom,
                body_bottom + np.array([-0.22 + leg_swing, -0.40 + leg_lift, 0])
            )
            figure.right_leg.put_start_and_end_on(
                body_bottom,
                body_bottom + np.array([0.22 - leg_swing, -0.40 + leg_lift * 0.5, 0])
            )
            figure.left_arm.put_start_and_end_on(
                arm_base_pt,
                arm_base_pt + np.array([-0.32 + arm_swing, -0.15, 0])
            )
            figure.right_arm.put_start_and_end_on(
                arm_base_pt,
                arm_base_pt + np.array([0.32 - arm_swing, -0.15, 0])
            )

            # Slight forward lean
            mob.move_to(np.array([x, 0.08, 0]))

        figure.add_updater(running_updater)

        # Panic text briefly
        panic = Text("!", font_size=50, color=RED_B, weight=BOLD)
        panic.next_to(figure, UP, buff=0.3)
        self.play(FadeIn(panic, scale=1.5), run_time=0.3)
        self.play(FadeOut(panic), run_time=0.3)

        # Run + water chase simultaneously
        self.play(
            water_tracker.animate.set_value(5),
            run_tracker.animate.set_value(1),
            run_time=4.5,
            rate_func=linear
        )

        figure.remove_updater(running_updater)

        # Continue water after figure exits
        self.play(
            water_tracker.animate.set_value(12),
            run_time=2.0,
            rate_func=linear
        )

        # ── Fade everything out ───────────────────────────────────────────────
        self.play(
            *[FadeOut(w) for w in waves],
            FadeOut(water_fill),
            FadeOut(figure),
            FadeOut(ground),
            run_time=1.2
        )

        self.wait(0.5)