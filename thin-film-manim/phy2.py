from manim import *
import numpy as np


class PhaseUnderstanding(Scene):
    def construct(self):
        self.camera.background_color = "#020617"

        A = 0.7
        k = 2 * PI / 2.5
        omega = 1.5
        x_min, x_max = -7, 7

        time_tracker = ValueTracker(0)
        phase_tracker = ValueTracker(0)

        # ── PART 1: CONTINUATION TRANSITION (0–3s) ───────────────────────────
        single_wave_bg = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, A * np.sin(k * x - omega * time_tracker.get_value()), 0]),
            t_range=[x_min, x_max, 0.04],
            color="#38bdf8", stroke_width=18, stroke_opacity=0.12
        ))
        single_wave = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, A * np.sin(k * x - omega * time_tracker.get_value()), 0]),
            t_range=[x_min, x_max, 0.04],
            color="#7dd3fc", stroke_width=3.5
        ))

        why_text = Text("But why does interference happen?", font_size=34,
                        color=WHITE)
        why_text.set_color_by_gradient("#38bdf8", "#818cf8")
        why_text.to_edge(UP, buff=0.6)

        self.play(FadeIn(single_wave_bg), FadeIn(single_wave), run_time=0.8)
        self.play(Write(why_text), run_time=1.2)
        self.play(time_tracker.animate.set_value(2.0), run_time=2.0,
                  rate_func=linear)
        self.wait(0.3)

        # ── PART 2: PHASE EXPLANATION (3–8s) ──────────────────────────────────
        self.play(FadeOut(why_text), run_time=0.5)

        wave2_bg = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, A * np.sin(k * x - omega * time_tracker.get_value() + phase_tracker.get_value()), 0]),
            t_range=[x_min, x_max, 0.04],
            color="#a78bfa", stroke_width=18, stroke_opacity=0.12
        ))
        wave2 = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, A * np.sin(k * x - omega * time_tracker.get_value() + phase_tracker.get_value()), 0]),
            t_range=[x_min, x_max, 0.04],
            color="#c4b5fd", stroke_width=3.5
        ))

        in_phase_label = Text("In Phase", font_size=32, color="#4ade80",
                              weight=BOLD)
        in_phase_label.to_edge(UP, buff=0.5)

        self.play(FadeIn(wave2_bg), FadeIn(wave2), Write(in_phase_label),
                  run_time=1.0)

        # Crest markers
        crest_arrows = VGroup()
        t_val = time_tracker.get_value()
        for x_crest in [-5.0, -2.5, 0.0, 2.5, 5.0]:
            y_crest = A * np.sin(k * x_crest - omega * t_val)
            if abs(y_crest - A) < 0.15:
                arr = Arrow(
                    start=[x_crest, A + 0.5, 0],
                    end=[x_crest, A + 0.1, 0],
                    color="#fbbf24", buff=0, stroke_width=2,
                    max_tip_length_to_length_ratio=0.3,
                    tip_length=0.15
                )
                lbl = Text("↑ crest", font_size=14, color="#fbbf24")
                lbl.next_to(arr, UP, buff=0.05)
                crest_arrows.add(arr, lbl)

        if len(crest_arrows) == 0:
            for x_crest in [-3.75, -1.25, 1.25, 3.75]:
                arr = Arrow(
                    start=[x_crest, A + 0.5, 0],
                    end=[x_crest, A + 0.1, 0],
                    color="#fbbf24", buff=0, stroke_width=2,
                    max_tip_length_to_length_ratio=0.3,
                    tip_length=0.15
                )
                crest_arrows.add(arr)

        self.play(FadeIn(crest_arrows), run_time=0.8)
        self.play(time_tracker.animate.set_value(5.0), run_time=3.0,
                  rate_func=linear)
        self.play(FadeOut(crest_arrows), FadeOut(in_phase_label), run_time=0.5)

        # ── PART 3: PHASE SHIFT VISUALIZATION (8–14s) ─────────────────────────
        phase_label = always_redraw(lambda: Text(
            f"Phase Difference = {phase_tracker.get_value():.2f} rad",
            font_size=28, color="#e2e8f0"
        ).to_edge(UP, buff=0.5))

        self.play(FadeIn(phase_label), run_time=0.5)

        self.play(
            phase_tracker.animate.set_value(PI),
            time_tracker.animate.set_value(9.5),
            run_time=5.5,
            rate_func=linear
        )
        self.wait(0.3)

        # ── PART 4: OUT OF PHASE (14–18s) ─────────────────────────────────────
        self.play(FadeOut(phase_label), run_time=0.4)

        out_phase_label = Text("Out of Phase", font_size=32, color="#f87171",
                               weight=BOLD)
        out_phase_label.to_edge(UP, buff=0.5)
        cancel_sub = Text("Waves cancel → Flat line", font_size=22,
                          color="#fca5a5")
        cancel_sub.next_to(out_phase_label, DOWN, buff=0.2)

        result_flat_bg = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([
                x,
                A * np.sin(k * x - omega * time_tracker.get_value()) +
                A * np.sin(k * x - omega * time_tracker.get_value() + phase_tracker.get_value()),
                0
            ]),
            t_range=[x_min, x_max, 0.04],
            color="#4ade80", stroke_width=20, stroke_opacity=0.12
        ))
        result_flat = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([
                x,
                A * np.sin(k * x - omega * time_tracker.get_value()) +
                A * np.sin(k * x - omega * time_tracker.get_value() + phase_tracker.get_value()),
                0
            ]),
            t_range=[x_min, x_max, 0.04],
            color="#86efac", stroke_width=4.5
        ))

        self.play(
            Write(out_phase_label), FadeIn(cancel_sub),
            FadeIn(result_flat_bg), FadeIn(result_flat),
            run_time=1.0
        )
        self.play(time_tracker.animate.set_value(12.0), run_time=3.0,
                  rate_func=linear)
        self.wait(0.4)

        # ── PART 5: CONNECT PHASE TO PATH (18–24s) ────────────────────────────
        self.play(
            FadeOut(out_phase_label), FadeOut(cancel_sub),
            FadeOut(single_wave_bg), FadeOut(single_wave),
            FadeOut(wave2_bg), FadeOut(wave2),
            FadeOut(result_flat_bg), FadeOut(result_flat),
            run_time=0.8
        )

        # Ray diagram
        ray_y_top = 1.2
        ray_y_bot = -1.0
        ray_color1 = "#38bdf8"
        ray_color2 = "#a78bfa"

        ray1 = Arrow(
            start=[-6, ray_y_top, 0], end=[5, ray_y_top, 0],
            color=ray_color1, buff=0, stroke_width=3,
            max_tip_length_to_length_ratio=0.06, tip_length=0.25
        )
        ray2_straight = Arrow(
            start=[-6, ray_y_bot, 0], end=[5, ray_y_bot, 0],
            color=ray_color2, buff=0, stroke_width=3,
            max_tip_length_to_length_ratio=0.06, tip_length=0.25
        )

        # Extra path dashed
        extra_path = DashedLine(
            start=[5, ray_y_bot, 0], end=[6.5, ray_y_bot, 0],
            color="#fbbf24", stroke_width=3, dash_length=0.15
        )
        delta_x_brace = BraceBetweenPoints(
            [5, ray_y_bot - 0.15, 0], [6.5, ray_y_bot - 0.15, 0],
            direction=DOWN, color="#fbbf24"
        )
        delta_x_label = Text("Δx  (Path Difference)", font_size=22,
                             color="#fbbf24")
        delta_x_label.next_to(delta_x_brace, DOWN, buff=0.18)

        ray_title = Text("Path Difference → Phase Difference",
                         font_size=28, color=WHITE)
        ray_title.set_color_by_gradient("#38bdf8", "#fbbf24")
        ray_title.to_edge(UP, buff=0.5)

        self.play(Write(ray_title), run_time=0.8)
        self.play(Create(ray1), Create(ray2_straight), run_time=1.2)
        self.play(
            Create(extra_path), Create(delta_x_brace),
            Write(delta_x_label), run_time=1.2
        )

        # Equation
        equation = MathTex(
            r"\Delta\phi = \frac{2\pi}{\lambda} \times \Delta x",
            font_size=38, color="#e2e8f0"
        )
        equation.move_to([0, 0.1, 0])
        eq_box = SurroundingRectangle(equation, color="#1e3a5f",
                                      fill_color="#0f172a", fill_opacity=0.8,
                                      buff=0.25, corner_radius=0.15)

        self.play(FadeIn(eq_box), Write(equation), run_time=1.5)

        longer_path_note = Text("Longer path  →  more phase shift",
                                font_size=22, color="#94a3b8")
        longer_path_note.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(longer_path_note), run_time=0.8)
        self.wait(1.5)

        # ── PART 6: KEY CONDITIONS (24–30s) ───────────────────────────────────
        self.play(
            FadeOut(ray_title), FadeOut(ray1), FadeOut(ray2_straight),
            FadeOut(extra_path), FadeOut(delta_x_brace), FadeOut(delta_x_label),
            FadeOut(equation), FadeOut(eq_box), FadeOut(longer_path_note),
            run_time=0.8
        )

        divider = Line([0, 3.5, 0], [0, -3.5, 0],
                       stroke_color="#1e3a5f", stroke_width=1.5,
                       stroke_opacity=0.6)

        # Case 1: constructive (left)
        case1_wave_bg = ParametricFunction(
            lambda x: np.array([x, 1.4 * A * np.sin(k * x), 0]),
            t_range=[-6.8, -0.3, 0.04],
            color="#38bdf8", stroke_width=16, stroke_opacity=0.14
        )
        case1_wave = ParametricFunction(
            lambda x: np.array([x, 1.4 * A * np.sin(k * x), 0]),
            t_range=[-6.8, -0.3, 0.04],
            color="#4ade80", stroke_width=4.5
        )
        case1_title = Text("Δx = nλ", font_size=28, color="#4ade80",
                           weight=BOLD)
        case1_title.move_to([-3.5, 2.8, 0])
        case1_sub = Text("Constructive  →  Bright", font_size=20,
                         color="#86efac")
        case1_sub.move_to([-3.5, 2.2, 0])

        bright_bar = Rectangle(width=3.8, height=0.45,
                               fill_color="#fde68a", fill_opacity=0.88,
                               stroke_width=0)
        bright_bar.move_to([-3.5, -2.6, 0])
        bright_bar_glow = Rectangle(width=4.0, height=0.65,
                                    fill_color="#fde68a", fill_opacity=0.12,
                                    stroke_width=0)
        bright_bar_glow.move_to([-3.5, -2.6, 0])

        # Case 2: destructive (right)
        case2_wave_bg = ParametricFunction(
            lambda x: np.array([x, 0.04 * np.sin(k * x), 0]),
            t_range=[0.3, 6.8, 0.04],
            color="#a78bfa", stroke_width=14, stroke_opacity=0.10
        )
        case2_wave = ParametricFunction(
            lambda x: np.array([x, 0.04 * np.sin(k * x), 0]),
            t_range=[0.3, 6.8, 0.04],
            color="#f87171", stroke_width=4.5
        )
        case2_title = MathTex(
            r"\Delta x = \left(n+\tfrac{1}{2}\right)\lambda",
            font_size=28, color="#f87171"
        )
        case2_title.move_to([3.5, 2.8, 0])
        case2_sub = Text("Destructive  →  Dark", font_size=20,
                         color="#fca5a5")
        case2_sub.move_to([3.5, 2.2, 0])

        dark_bar = Rectangle(width=3.8, height=0.45,
                             fill_color="#0f172a", fill_opacity=0.95,
                             stroke_color="#334155", stroke_width=1.5)
        dark_bar.move_to([3.5, -2.6, 0])

        self.play(FadeIn(divider), run_time=0.5)
        self.play(
            FadeIn(case1_wave_bg), FadeIn(case1_wave),
            Write(case1_title), FadeIn(case1_sub),
            FadeIn(case2_wave_bg), FadeIn(case2_wave),
            Write(case2_title), FadeIn(case2_sub),
            run_time=1.2
        )
        self.play(
            FadeIn(bright_bar_glow), FadeIn(bright_bar),
            FadeIn(dark_bar),
            run_time=0.8
        )
        self.wait(2.0)

        # ── PART 7: FINAL INTUITION (30–35s) ─────────────────────────────────
        self.play(
            FadeOut(case1_wave_bg), FadeOut(case1_wave),
            FadeOut(case2_wave_bg), FadeOut(case2_wave),
            FadeOut(case1_title), FadeOut(case1_sub),
            FadeOut(case2_title), FadeOut(case2_sub),
            FadeOut(bright_bar_glow), FadeOut(bright_bar),
            FadeOut(dark_bar), FadeOut(divider),
            run_time=0.8
        )

        phase_tracker.set_value(0)
        time_tracker.set_value(0)

        final_w1_bg = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, A * np.sin(k * x - omega * time_tracker.get_value()), 0]),
            t_range=[x_min, x_max, 0.04],
            color="#38bdf8", stroke_width=18, stroke_opacity=0.13
        ))
        final_w1 = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, A * np.sin(k * x - omega * time_tracker.get_value()), 0]),
            t_range=[x_min, x_max, 0.04],
            color="#7dd3fc", stroke_width=3.5
        ))
        final_w2_bg = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, A * np.sin(k * x - omega * time_tracker.get_value() + phase_tracker.get_value()), 0]),
            t_range=[x_min, x_max, 0.04],
            color="#a78bfa", stroke_width=18, stroke_opacity=0.13
        ))
        final_w2 = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, A * np.sin(k * x - omega * time_tracker.get_value() + phase_tracker.get_value()), 0]),
            t_range=[x_min, x_max, 0.04],
            color="#c4b5fd", stroke_width=3.5
        ))

        self.play(
            FadeIn(final_w1_bg), FadeIn(final_w1),
            FadeIn(final_w2_bg), FadeIn(final_w2),
            run_time=0.8
        )

        final_text1 = Text("Path difference controls phase",
                           font_size=30, color="#e2e8f0")
        final_text1.set_color_by_gradient("#38bdf8", "#a78bfa")
        final_text1.to_edge(UP, buff=0.55)

        final_text2 = Text("Phase controls interference",
                           font_size=30, color="#e2e8f0")
        final_text2.set_color_by_gradient("#a78bfa", "#4ade80")
        final_text2.next_to(final_text1, DOWN, buff=0.3)

        self.play(Write(final_text1), run_time=1.0)
        self.play(Write(final_text2), run_time=1.0)
        self.play(time_tracker.animate.set_value(4.5), run_time=2.5,
                  rate_func=linear)
        self.wait(0.5)

        all_final = VGroup(
            final_w1_bg, final_w1, final_w2_bg, final_w2,
            final_text1, final_text2
        )
        self.play(FadeOut(all_final), run_time=2.0)
        self.wait(0.3)