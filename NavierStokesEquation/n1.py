from manim import *
import numpy as np

class Scene1_Hook_Trimmed(Scene):
    def construct(self):
        self.camera.background_color = "#050810"

        t_offset = ValueTracker(0)

        # --- Layered wave curves ---
        num_layers = 18
        waves = VGroup()

        for i in range(num_layers):
            layer_index = i

            def make_wave_func(idx):
                phase     = idx * 0.38
                amplitude = 0.18 + 0.07 * np.sin(idx * 1.1)
                y_base    = -3.2 + idx * 0.38
                freq      = 0.55 + 0.06 * idx
                speed     = 0.9 + 0.15 * (idx % 4)

                def wave(t_val):
                    return lambda x: np.array([
                        x,
                        y_base
                        + amplitude * np.sin(freq * x + phase + speed * t_val)
                        + 0.09 * np.sin(1.8 * freq * x - phase * 1.3 + 0.7 * speed * t_val),
                        0,
                    ])
                return wave

            wave_func_factory = make_wave_func(layer_index)

            blue_t = layer_index / (num_layers - 1)
            r = int(interpolate(5,   30,  blue_t))
            g = int(interpolate(20,  160, blue_t))
            b = int(interpolate(80,  255, blue_t))
            color = rgb_to_color([r / 255, g / 255, b / 255])
            opacity = 0.25 + 0.45 * blue_t

            curve = always_redraw(
                lambda wf=wave_func_factory, c=color, o=opacity: ParametricFunction(
                    wf(t_offset.get_value()),
                    t_range=[-7.2, 7.2, 0.08],
                    color=c,
                    stroke_width=1.4 + 1.6 * (o - 0.25),
                    stroke_opacity=o,
                )
            )
            waves.add(curve)

        self.add(waves)

        # --- Subtle glow lines ---
        glow_lines = VGroup()
        for i in range(5):
            idx = i * 3 + 2

            def make_glow(idx2=idx):
                phase     = idx2 * 0.38
                amplitude = 0.22 + 0.05 * np.sin(idx2 * 1.1)
                y_base    = -3.2 + idx2 * 0.38
                freq      = 0.55 + 0.06 * idx2
                speed     = 0.9 + 0.15 * (idx2 % 4)

                def gf(t_val):
                    return lambda x: np.array([
                        x,
                        y_base
                        + amplitude * np.sin(freq * x + phase + speed * t_val)
                        + 0.09 * np.sin(1.8 * freq * x - phase * 1.3 + 0.7 * speed * t_val),
                        0,
                    ])
                return gf

            gf = make_glow()
            glow = always_redraw(
                lambda gff=gf, ii=i: ParametricFunction(
                    gff(t_offset.get_value()),
                    t_range=[-7.2, 7.2, 0.12],
                    color=TEAL_A,
                    stroke_width=9,
                    stroke_opacity=0.06 + 0.04 * ii,
                )
            )
            glow_lines.add(glow)

        self.add(glow_lines)

        # --- Floating particles ---
        num_particles = 55
        particles = VGroup()
        p_data = []

        rng = np.random.default_rng(42)
        for _ in range(num_particles):
            px    = rng.uniform(-7.0,  7.0)
            py    = rng.uniform(-3.2,  3.2)
            spd   = rng.uniform( 0.4,  1.1)
            amp   = rng.uniform( 0.12, 0.35)
            freq  = rng.uniform( 0.4,  0.8)
            phase = rng.uniform(0, TAU)
            size  = rng.uniform(0.025, 0.065)
            bright = rng.uniform(0.5, 1.0)
            p_data.append((px, py, spd, amp, freq, phase, size, bright))

            dot = Dot(point=[px, py, 0], radius=size,
                      color=interpolate_color(BLUE_B, WHITE, bright),
                      fill_opacity=0.55)
            particles.add(dot)

        self.add(particles)

        def update_particles(group, dt):
            for dot, (px, py, spd, amp, freq, phase, size, bright) in zip(group, p_data):
                t = t_offset.get_value()
                new_x = dot.get_center()[0] + spd * dt
                if new_x > 7.3:
                    new_x = -7.3
                new_y = py + amp * np.sin(freq * new_x + phase + t)
                dot.move_to([new_x, new_y, 0])

        particles.add_updater(update_particles)

        # --- Faint grid (already visible from start) ---
        grid = VGroup()
        for x in np.arange(-7, 7.5, 1.4):
            line = Line([x, -4, 0], [x, 4, 0],
                        stroke_color=GREY, stroke_width=0.4, stroke_opacity=0.18)
            grid.add(line)
        for y in np.arange(-3.5, 4, 1.0):
            line = Line([-7.5, y, 0], [7.5, y, 0],
                        stroke_color=GREY, stroke_width=0.4, stroke_opacity=0.18)
            grid.add(line)

        self.add(grid)

        # --- Velocity arrows (already visible from start) ---
        arrow_positions = [
            (-5.0, -1.2), (-3.0,  0.5), (-1.0, -0.8),
            ( 1.0,  1.1), ( 3.0,  0.0), ( 5.0, -1.0),
        ]
        arrows = VGroup()
        for (ax, ay) in arrow_positions:
            def make_arrow_updater(base_x, base_y):
                def updater(arr):
                    t = t_offset.get_value()
                    dy = 0.22 * np.cos(0.6 * base_x + t * 0.9) * 0.6
                    direction = np.array([1.0, dy, 0])
                    direction /= np.linalg.norm(direction)
                    start = np.array([base_x, base_y + 0.18 * np.sin(0.5 * base_x + t), 0])
                    end   = start + direction * 0.55
                    arr.become(
                        Arrow(start, end, buff=0, max_tip_length_to_length_ratio=0.35,
                              stroke_width=1.8, color=TEAL_A, fill_opacity=0.7)
                    )
                return updater

            arrow = Arrow(
                [ax, ay, 0], [ax + 0.5, ay, 0],
                buff=0, max_tip_length_to_length_ratio=0.35,
                stroke_width=1.8, color=TEAL_A, fill_opacity=0.7,
            )
            arrow.add_updater(make_arrow_updater(ax, ay))
            arrows.add(arrow)

        self.add(arrows)

        # ─────────────────────────────────────────────
        # PRE-PART 1: Visuals only (5 sec extra)
        # ─────────────────────────────────────────────

        self.play(
            t_offset.animate.set_value(2.5),
            run_time=5,
            rate_func=linear,
        )

        # ─────────────────────────────────────────────
        # PART 1: Question Appears (0–5 sec)
        # ─────────────────────────────────────────────

        question = Text(
            "What is a fluid?",
            font="Georgia",
            font_size=52,
            color=WHITE,
            weight=NORMAL,
        ).move_to(ORIGIN + UP * 0.3)

        question.set_opacity(0)
        self.add(question)

        self.play(
            question.animate.set_opacity(1).scale(1.06),
            t_offset.animate.set_value(5.5),
            run_time=5,
            rate_func=smooth,
        )

        # ─────────────────────────────────────────────
        # PART 2: Answer + Flow Intensifies (5–15 sec)
        # ─────────────────────────────────────────────

        answer = Text(
            "A fluid continuously deforms (flows)\nwhen a force is applied.",
            font="Georgia",
            font_size=28,
            color=WHITE,
            line_spacing=1.5,
            weight=NORMAL,
        ).next_to(question, DOWN, buff=0.55)
        answer.set_opacity(0)
        self.add(answer)

        self.play(
            question.animate.shift(UP * 0.15),
            answer.animate.set_opacity(0.92).shift(UP * 0.12),
            t_offset.animate.set_value(12.5),
            run_time=7,
            rate_func=smooth,
        )

        # Hold final frame with everything alive
        self.play(
            t_offset.animate.set_value(15.5),
            run_time=3,
            rate_func=linear,
        )