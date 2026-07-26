from manim import *
import numpy as np


class InterferenceIntro(Scene):
    def construct(self):
        self.camera.background_color = "#020617"

        A = 0.7
        k = 2 * PI / 2.5
        omega = 1.8
        x_min, x_max = -7, 7

        time_tracker = ValueTracker(0)
        phase_tracker = ValueTracker(0)

        # ── PART 1: CINEMATIC OPEN ────────────────────────────────────────────
        grid_lines = VGroup()
        for i in np.arange(-6, 7, 1.5):
            grid_lines.add(
                Line([i, -4, 0], [i, 4, 0],
                     stroke_color="#0f1f3d", stroke_width=1, stroke_opacity=0.4)
            )
        for j in np.arange(-3.5, 4, 1.2):
            grid_lines.add(
                Line([-7, j, 0], [7, j, 0],
                     stroke_color="#0f1f3d", stroke_width=1, stroke_opacity=0.4)
            )

        self.play(FadeIn(grid_lines), run_time=1.5)

        title = Text("INTERFERENCE OF LIGHT", font_size=52,
                     color=WHITE, weight=BOLD)
        title.set_color_by_gradient("#38bdf8", "#818cf8")
        subtitle = Text("When waves meet, they interfere", font_size=26,
                        color="#94a3b8")
        subtitle.next_to(title, DOWN, buff=0.35)

        self.play(FadeIn(title, scale=0.85), run_time=1.2)
        self.play(FadeIn(subtitle), run_time=0.8)
        self.wait(1.5)

        self.play(
            title.animate.set_opacity(0.18).shift(UP * 0.6),
            subtitle.animate.set_opacity(0),
            run_time=1.0
        )

        # ── PART 2: SINGLE WAVE INTRO ─────────────────────────────────────────
        def make_wave_glow(color_main, color_glow, phase_fn, amp=A,
                           opacity_glow=0.15, width_glow=18, width_main=3.5):
            bg = always_redraw(lambda: ParametricFunction(
                lambda x: np.array([x, amp * np.sin(k * x - omega * time_tracker.get_value() + phase_fn()), 0]),
                t_range=[x_min, x_max, 0.04],
                color=color_glow, stroke_width=width_glow, stroke_opacity=opacity_glow
            ))
            fg = always_redraw(lambda: ParametricFunction(
                lambda x: np.array([x, amp * np.sin(k * x - omega * time_tracker.get_value() + phase_fn()), 0]),
                t_range=[x_min, x_max, 0.04],
                color=color_main, stroke_width=width_main
            ))
            return bg, fg

        w1_bg, w1 = make_wave_glow("#38bdf8", "#7dd3fc",
                                   lambda: 0, opacity_glow=0.2, width_glow=20)

        label_wave = Text("Light behaves like a wave", font_size=26,
                          color="#94a3b8")
        label_wave.to_corner(UL, buff=0.5)

        self.play(FadeIn(w1_bg), FadeIn(w1), FadeIn(label_wave), run_time=1.0)
        self.play(time_tracker.animate.set_value(3.5), run_time=3.5,
                  rate_func=linear)

        # ── PART 3: SECOND WAVE ENTRY ─────────────────────────────────────────
        w2_bg, w2 = make_wave_glow("#a78bfa", "#c4b5fd",
                                   lambda: phase_tracker.get_value(),
                                   opacity_glow=0.18, width_glow=18)

        self.play(FadeIn(w2_bg), FadeIn(w2), run_time=0.8)
        self.play(time_tracker.animate.set_value(7.0), run_time=3.5,
                  rate_func=linear)

        # ── PART 4: CONSTRUCTIVE INTERFERENCE ────────────────────────────────
        self.play(FadeOut(label_wave), run_time=0.4)

        result_bg = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([
                x,
                A * np.sin(k * x - omega * time_tracker.get_value()) +
                A * np.sin(k * x - omega * time_tracker.get_value() + phase_tracker.get_value()),
                0
            ]),
            t_range=[x_min, x_max, 0.04],
            color="#4ade80", stroke_width=22, stroke_opacity=0.15
        ))
        result_fg = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([
                x,
                A * np.sin(k * x - omega * time_tracker.get_value()) +
                A * np.sin(k * x - omega * time_tracker.get_value() + phase_tracker.get_value()),
                0
            ]),
            t_range=[x_min, x_max, 0.04],
            color="#86efac", stroke_width=4.5
        ))

        self.play(FadeIn(result_bg), FadeIn(result_fg), run_time=0.7)

        lbl_c = Text("Constructive Interference", font_size=32,
                     color="#4ade80", weight=BOLD)
        lbl_c.to_edge(UP, buff=0.45)
        sub_c = Text("Waves in phase  →  amplitudes add", font_size=22,
                     color="#86efac")
        sub_c.next_to(lbl_c, DOWN, buff=0.18)

        self.play(Write(lbl_c), FadeIn(sub_c), run_time=1.0)
        self.play(time_tracker.animate.set_value(10.5), run_time=3.5,
                  rate_func=linear)
        self.wait(0.3)

        # ── PART 5: PHASE SHIFT TRANSITION ───────────────────────────────────
        self.play(FadeOut(lbl_c), FadeOut(sub_c), run_time=0.5)

        shift_note = Text("Shifting phase by π…", font_size=24,
                          color="#94a3b8")
        shift_note.to_edge(UP, buff=0.5)
        self.play(FadeIn(shift_note), run_time=0.5)

        self.play(
            phase_tracker.animate.set_value(PI),
            time_tracker.animate.set_value(12.5),
            run_time=3.0, rate_func=smooth
        )
        self.play(FadeOut(shift_note), run_time=0.4)

        # ── PART 6: DESTRUCTIVE INTERFERENCE ─────────────────────────────────
        lbl_d = Text("Destructive Interference", font_size=32,
                     color="#f87171", weight=BOLD)
        lbl_d.to_edge(UP, buff=0.45)
        sub_d = Text("Waves out of phase  →  cancel", font_size=22,
                     color="#fca5a5")
        sub_d.next_to(lbl_d, DOWN, buff=0.18)

        self.play(Write(lbl_d), FadeIn(sub_d), run_time=1.0)
        self.play(time_tracker.animate.set_value(16.0), run_time=3.5,
                  rate_func=linear)
        self.wait(0.3)

        # ── PART 7: INTENSITY VISUALIZATION ──────────────────────────────────
        self.play(
            FadeOut(lbl_d), FadeOut(sub_d),
            FadeOut(w1_bg), FadeOut(w1),
            FadeOut(w2_bg), FadeOut(w2),
            FadeOut(result_bg), FadeOut(result_fg),
            FadeOut(grid_lines),
            run_time=0.8
        )

        bar_bright = Rectangle(width=4.5, height=0.55,
                               fill_color="#fde68a", fill_opacity=0.92,
                               stroke_width=0)
        bar_bright.move_to([-3.0, -2.8, 0])
        glow_bright = Rectangle(width=4.7, height=0.75,
                                fill_color="#fde68a", fill_opacity=0.15,
                                stroke_width=0)
        glow_bright.move_to([-3.0, -2.8, 0])

        bar_dark = Rectangle(width=4.5, height=0.55,
                             fill_color="#1e293b", fill_opacity=0.95,
                             stroke_color="#334155", stroke_width=1)
        bar_dark.move_to([3.0, -2.8, 0])

        hi_txt = Text("High Intensity", font_size=22, color="#fde68a")
        hi_txt.next_to(bar_bright, DOWN, buff=0.18)
        lo_txt = Text("Low Intensity", font_size=22, color="#475569")
        lo_txt.next_to(bar_dark, DOWN, buff=0.18)

        # Static constructive wave (left)
        w_c_bg = ParametricFunction(
            lambda x: np.array([x, 1.4 * A * np.sin(k * x), 0]),
            t_range=[-6.8, -0.3, 0.04],
            color="#38bdf8", stroke_width=16, stroke_opacity=0.14
        )
        w_c = ParametricFunction(
            lambda x: np.array([x, 1.4 * A * np.sin(k * x), 0]),
            t_range=[-6.8, -0.3, 0.04],
            color="#7dd3fc", stroke_width=3.5
        )
        w_c_r = ParametricFunction(
            lambda x: np.array([x, 1.4 * A * np.sin(k * x), 0]),
            t_range=[-6.8, -0.3, 0.04],
            color="#4ade80", stroke_width=5, stroke_opacity=0.85
        )

        # Static destructive wave (right, near zero)
        w_d_bg = ParametricFunction(
            lambda x: np.array([x, 0.04 * np.sin(k * x), 0]),
            t_range=[0.3, 6.8, 0.04],
            color="#a78bfa", stroke_width=14, stroke_opacity=0.10
        )
        w_d = ParametricFunction(
            lambda x: np.array([x, 0.04 * np.sin(k * x), 0]),
            t_range=[0.3, 6.8, 0.04],
            color="#7c3aed", stroke_width=3.5
        )
        w_d_r = ParametricFunction(
            lambda x: np.array([x, 0.04 * np.sin(k * x), 0]),
            t_range=[0.3, 6.8, 0.04],
            color="#f87171", stroke_width=4.5, stroke_opacity=0.8
        )

        divider = Line([0, 3.5, 0], [0, -3.5, 0],
                       stroke_color="#1e3a5f", stroke_width=1.5,
                       stroke_opacity=0.6)

        self.play(
            FadeIn(divider),
            FadeIn(w_c_bg), FadeIn(w_c), FadeIn(w_c_r),
            FadeIn(w_d_bg), FadeIn(w_d), FadeIn(w_d_r),
            FadeIn(glow_bright), FadeIn(bar_bright), FadeIn(hi_txt),
            FadeIn(bar_dark), FadeIn(lo_txt),
            run_time=1.2
        )
        self.wait(1.5)

        # ── PART 8: FINAL COMPOSITION ─────────────────────────────────────────
        bright_lbl = Text("Bright", font_size=36, color="#fde68a",
                          weight=BOLD)
        bright_lbl.move_to([-3.3, 2.9, 0])
        dark_lbl = Text("Dark", font_size=36, color="#475569",
                        weight=BOLD)
        dark_lbl.move_to([3.3, 2.9, 0])

        self.play(Write(bright_lbl), Write(dark_lbl), run_time=0.9)

        all_objs = VGroup(
            w_c_bg, w_c, w_c_r,
            w_d_bg, w_d, w_d_r,
            glow_bright, bar_bright, hi_txt,
            bar_dark, lo_txt,
            divider, bright_lbl, dark_lbl, title
        )
        self.play(all_objs.animate.scale(1.06).shift(UP * 0.1),
                  run_time=1.8, rate_func=smooth)
        self.wait(0.5)
        self.play(FadeOut(all_objs), run_time=2.0)
        self.wait(0.3)