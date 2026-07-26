from manim import *
import numpy as np


class ThinFilmMasterScene(Scene):
    def construct(self):
        self.camera.background_color = "#020617"

        # ── PART 1: TRANSITION FROM WAVE TO RAY (0–4s) ───────────────────────
        time_t = ValueTracker(0)
        A, k, omega = 0.5, 2 * PI / 2.5, 1.5

        wave_bg = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, A * np.sin(k * x - omega * time_t.get_value()), 0]),
            t_range=[-6, 6, 0.04],
            color="#38bdf8", stroke_width=16, stroke_opacity=0.13
        ))
        wave_fg = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, A * np.sin(k * x - omega * time_t.get_value()), 0]),
            t_range=[-6, 6, 0.04],
            color="#7dd3fc", stroke_width=3.5
        ))

        self.play(FadeIn(wave_bg), FadeIn(wave_fg), run_time=0.6)
        self.play(time_t.animate.set_value(1.5), run_time=1.2, rate_func=linear)

        transition_text = Text("Now let's see how this happens in real materials",
                               font_size=26, color=WHITE)
        transition_text.set_color_by_gradient("#38bdf8", "#818cf8")
        transition_text.to_edge(UP, buff=0.5)
        self.play(Write(transition_text), run_time=1.0)
        self.play(time_t.animate.set_value(3.0), run_time=1.0, rate_func=linear)

        straight_glow = Line([-6, 0, 0], [6, 0, 0], color="#fde68a",
                             stroke_width=18, stroke_opacity=0.22)
        straight_ray = Line([-6, 0, 0], [6, 0, 0], color="#fef3c7", stroke_width=4)

        self.play(
            ReplacementTransform(wave_fg, straight_ray),
            ReplacementTransform(wave_bg, straight_glow),
            run_time=1.2
        )
        self.play(FadeOut(transition_text), FadeOut(straight_ray),
                  FadeOut(straight_glow), run_time=0.6)

        # ── PART 2: CREATE THIN FILM (4–9s) ───────────────────────────────────
        film_top_y = 0.8
        film_bot_y = -0.7
        film_left_x = -6.0
        film_right_x = 6.0

        top_surface = Line([film_left_x, film_top_y, 0], [film_right_x, film_top_y, 0],
                           color="#e2e8f0", stroke_width=2.5)
        bot_surface = Line([film_left_x, film_bot_y, 0], [film_right_x, film_bot_y, 0],
                           color="#94a3b8", stroke_width=2.5)

        film_poly = Polygon(
            [film_left_x, film_top_y, 0], [film_right_x, film_top_y, 0],
            [film_right_x, film_bot_y, 0], [film_left_x, film_bot_y, 0],
            fill_color="#0ea5e9", fill_opacity=0.13, stroke_width=0
        )
        film_poly2 = Polygon(
            [film_left_x, film_top_y, 0], [film_right_x, film_top_y, 0],
            [film_right_x, film_bot_y, 0], [film_left_x, film_bot_y, 0],
            fill_color="#818cf8", fill_opacity=0.07, stroke_width=0
        )

        air_lbl = Text("Air  (n=1)", font_size=17, color="#64748b")
        air_lbl.move_to([-4.8, film_top_y + 0.5, 0])
        film_lbl = Text("Thin Film  (thickness t, refractive index μ)", font_size=18, color="#7dd3fc")
        film_lbl.move_to([0, (film_top_y + film_bot_y) / 2, 0])
        sub_lbl = Text("Substrate  (Glass)", font_size=17, color="#64748b")
        sub_lbl.move_to([-4.5, film_bot_y - 0.45, 0])

        normal_line = DashedLine([-1.2, film_top_y + 1.4, 0], [-1.2, film_bot_y - 0.6, 0],
                                 color="#334155", stroke_width=1.5, dash_length=0.14)
        normal_lbl = Text("Normal", font_size=15, color="#475569")
        normal_lbl.next_to(normal_line, RIGHT, buff=0.08).shift(UP * 0.6)

        self.play(Create(top_surface), Create(bot_surface), run_time=0.8)
        self.play(FadeIn(film_poly), FadeIn(film_poly2), run_time=0.6)
        self.play(Write(air_lbl), Write(film_lbl), Write(sub_lbl), run_time=0.8)
        self.play(Create(normal_line), Write(normal_lbl), run_time=0.6)
        self.wait(0.8)

        # ── PART 3: INCIDENT LIGHT (9–13s) ────────────────────────────────────
        inc_start = [-4.8, film_top_y + 2.0, 0]
        hit_top = [-1.2, film_top_y, 0]

        inc_glow = Arrow(inc_start, hit_top, color="#fde68a", stroke_width=16,
                         buff=0, max_tip_length_to_length_ratio=0.07,
                         tip_length=0.22, stroke_opacity=0.22)
        inc_ray = Arrow(inc_start, hit_top, color="#fef3c7", stroke_width=3.5,
                        buff=0, max_tip_length_to_length_ratio=0.07, tip_length=0.22)
        inc_lbl = Text("Incident Light", font_size=19, color="#fef3c7")
        inc_lbl.move_to([-4.0, film_top_y + 1.5, 0])

        angle_arc = Arc(radius=0.5, start_angle=-PI / 2, angle=PI / 4,
                        color="#fbbf24", stroke_width=1.8)
        angle_arc.move_to([-1.2, film_top_y, 0])
        angle_lbl = Text("θ", font_size=16, color="#fbbf24")
        angle_lbl.next_to(angle_arc, UP + RIGHT, buff=0.05)

        self.play(Create(inc_glow), Create(inc_ray), run_time=0.9)
        self.play(Write(inc_lbl), Create(angle_arc), Write(angle_lbl), run_time=0.7)
        self.wait(0.8)
        self.play(FadeOut(inc_lbl), run_time=0.3)

        # ── PART 4: RAY SPLITTING (13–20s) ────────────────────────────────────
        # Ray 1: reflects up from top
        ref1_end = [2.4, film_top_y + 2.0, 0]
        r1_glow = Arrow(hit_top, ref1_end, color="#38bdf8", stroke_width=14,
                        buff=0, max_tip_length_to_length_ratio=0.07,
                        tip_length=0.22, stroke_opacity=0.22)
        r1_ray = Arrow(hit_top, ref1_end, color="#7dd3fc", stroke_width=3.5,
                       buff=0, max_tip_length_to_length_ratio=0.07, tip_length=0.22)
        r1_lbl = Text("Ray 1 (Top Reflection)", font_size=17, color="#7dd3fc")
        r1_lbl.move_to([3.5, film_top_y + 1.6, 0])

        # Ray 2: into film, reflect bottom, exit
        hit_bot = [0.4, film_bot_y, 0]
        exit_top = [2.0, film_top_y, 0]
        ref2_end = [4.8, film_top_y + 2.0, 0]

        r2_down_glow = Arrow(hit_top, hit_bot, color="#fb923c", stroke_width=14,
                             buff=0, max_tip_length_to_length_ratio=0.07,
                             tip_length=0.22, stroke_opacity=0.22)
        r2_down = Arrow(hit_top, hit_bot, color="#fdba74", stroke_width=3.5,
                        buff=0, max_tip_length_to_length_ratio=0.07, tip_length=0.22)
        r2_up_glow = Arrow(hit_bot, exit_top, color="#fb923c", stroke_width=14,
                           buff=0, max_tip_length_to_length_ratio=0.07,
                           tip_length=0.22, stroke_opacity=0.22)
        r2_up = Arrow(hit_bot, exit_top, color="#fdba74", stroke_width=3.5,
                      buff=0, max_tip_length_to_length_ratio=0.07, tip_length=0.22)
        r2_exit_glow = Arrow(exit_top, ref2_end, color="#fb923c", stroke_width=14,
                             buff=0, max_tip_length_to_length_ratio=0.07,
                             tip_length=0.22, stroke_opacity=0.22)
        r2_exit = Arrow(exit_top, ref2_end, color="#fdba74", stroke_width=3.5,
                        buff=0, max_tip_length_to_length_ratio=0.07, tip_length=0.22)
        r2_lbl = Text("Ray 2 (Bottom Reflection)", font_size=17, color="#fdba74")
        r2_lbl.move_to([5.2, film_top_y + 1.3, 0])

        self.play(Create(r1_glow), Create(r1_ray), run_time=0.7)
        self.play(Write(r1_lbl), run_time=0.5)
        self.play(Create(r2_down_glow), Create(r2_down), run_time=0.6)
        self.play(Create(r2_up_glow), Create(r2_up), run_time=0.6)
        self.play(Create(r2_exit_glow), Create(r2_exit), Write(r2_lbl), run_time=0.7)
        self.wait(1.0)

        # ── PART 5: OPTICAL PATH DIFFERENCE (20–28s) ──────────────────────────
        self.play(FadeOut(r1_lbl), FadeOut(r2_lbl), run_time=0.4)

        dash_down = DashedLine(hit_top, hit_bot, color="#fbbf24",
                               stroke_width=2.5, dash_length=0.12)
        dash_up = DashedLine(hit_bot, exit_top, color="#fbbf24",
                             stroke_width=2.5, dash_length=0.12)

        geom_lbl = Text("Geometric path  =  2t", font_size=19, color="#fbbf24")
        geom_lbl.move_to([-3.2, (film_top_y + film_bot_y) / 2 + 0.2, 0])
        opt_lbl = Text("Optical path  =  2μt", font_size=19, color="#fde68a")
        opt_lbl.next_to(geom_lbl, DOWN, buff=0.22)
        mu_note = Text("(μ = refractive index)", font_size=15, color="#94a3b8")
        mu_note.next_to(opt_lbl, DOWN, buff=0.15)

        pd_eq = MathTex(r"\text{Path Difference} = 2\mu t",
                        font_size=32, color="#e2e8f0")
        pd_box = SurroundingRectangle(pd_eq, color="#1e3a5f", fill_color="#0f172a",
                                      fill_opacity=0.88, buff=0.22, corner_radius=0.14)
        pd_eq.move_to([0, -1.9, 0])
        pd_box.move_to([0, -1.9, 0])

        self.play(Create(dash_down), Create(dash_up), run_time=0.8)
        self.play(Write(geom_lbl), run_time=0.7)
        self.play(Write(opt_lbl), Write(mu_note), run_time=0.7)
        self.play(FadeIn(pd_box), Write(pd_eq), run_time=0.9)
        self.wait(1.2)

        self.play(FadeOut(geom_lbl), FadeOut(opt_lbl), FadeOut(mu_note),
                  FadeOut(pd_box), FadeOut(pd_eq),
                  FadeOut(dash_down), FadeOut(dash_up), run_time=0.6)

        # ── PART 6: PHASE CHANGE ON REFLECTION (28–36s) ───────────────────────
        phase_title = Text("Phase Change on Reflection", font_size=26,
                           color=WHITE, weight=BOLD)
        phase_title.set_color_by_gradient("#38bdf8", "#818cf8")
        phase_title.to_edge(UP, buff=0.45)
        self.play(Write(phase_title), run_time=0.8)

        # Highlight top surface reflection point
        dot_top = Dot(hit_top, color="#fbbf24", radius=0.12)
        circle_top = Circle(radius=0.28, color="#fbbf24", stroke_width=2)
        circle_top.move_to(hit_top)

        phase_top_lbl = Text("Air → Film  (denser medium)", font_size=17,
                             color="#fbbf24")
        phase_top_lbl.move_to([-3.5, film_top_y + 0.55, 0])
        phase_shift_lbl = Text("Phase shift = π  (λ/2 shift)", font_size=17,
                               color="#f87171", weight=BOLD)
        phase_shift_lbl.next_to(phase_top_lbl, DOWN, buff=0.18)

        self.play(FadeIn(dot_top), Create(circle_top), run_time=0.6)
        self.play(Write(phase_top_lbl), Write(phase_shift_lbl), run_time=0.8)
        self.wait(0.7)

        # Bottom surface
        dot_bot = Dot(hit_bot, color="#4ade80", radius=0.12)
        circle_bot = Circle(radius=0.28, color="#4ade80", stroke_width=2)
        circle_bot.move_to(hit_bot)

        phase_bot_lbl = Text("Film → Air  (less dense medium)", font_size=17,
                             color="#4ade80")
        phase_bot_lbl.move_to([2.5, film_bot_y - 0.42, 0])
        no_shift_lbl = Text("No phase shift", font_size=17, color="#86efac",
                            weight=BOLD)
        no_shift_lbl.next_to(phase_bot_lbl, DOWN, buff=0.18)

        self.play(FadeIn(dot_bot), Create(circle_bot), run_time=0.6)
        self.play(Write(phase_bot_lbl), Write(no_shift_lbl), run_time=0.8)
        self.wait(0.6)

        eff_eq = MathTex(
            r"\text{Effective Path Difference} = 2\mu t + \frac{\lambda}{2}",
            font_size=28, color="#e2e8f0"
        )
        eff_box = SurroundingRectangle(eff_eq, color="#1e3a5f", fill_color="#0f172a",
                                       fill_opacity=0.90, buff=0.22, corner_radius=0.14)
        eff_eq.move_to([0, -2.1, 0])
        eff_box.move_to([0, -2.1, 0])
        self.play(FadeIn(eff_box), Write(eff_eq), run_time=1.0)
        self.wait(1.2)

        self.play(
            FadeOut(phase_title), FadeOut(dot_top), FadeOut(circle_top),
            FadeOut(phase_top_lbl), FadeOut(phase_shift_lbl),
            FadeOut(dot_bot), FadeOut(circle_bot),
            FadeOut(phase_bot_lbl), FadeOut(no_shift_lbl),
            FadeOut(eff_box), FadeOut(eff_eq), run_time=0.7
        )

        # ── PART 7: INTERFERENCE FORMATION (36–44s) ───────────────────────────
        self.play(
            FadeOut(inc_glow), FadeOut(inc_ray),
            FadeOut(angle_arc), FadeOut(angle_lbl),
            FadeOut(r1_glow), FadeOut(r1_ray),
            FadeOut(r2_down_glow), FadeOut(r2_down),
            FadeOut(r2_up_glow), FadeOut(r2_up),
            FadeOut(r2_exit_glow), FadeOut(r2_exit),
            FadeOut(normal_line), FadeOut(normal_lbl),
            run_time=0.6
        )

        interf_title = Text("Interference of Reflected Rays", font_size=26,
                            color=WHITE, weight=BOLD)
        interf_title.set_color_by_gradient("#4ade80", "#f87171")
        interf_title.to_edge(UP, buff=0.45)
        self.play(Write(interf_title), run_time=0.7)

        tw = ValueTracker(0)
        A2, k2, om2 = 0.42, 2 * PI / 1.6, 2.2

        # Constructive: left half
        cw1 = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, A2 * np.sin(k2 * x - om2 * tw.get_value()) + film_top_y + 1.3, 0]),
            t_range=[-6.5, -0.3, 0.04],
            color="#7dd3fc", stroke_width=3
        ))
        cw2 = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, A2 * np.sin(k2 * x - om2 * tw.get_value()) + film_top_y + 1.3, 0]),
            t_range=[-6.5, -0.3, 0.04],
            color="#fdba74", stroke_width=3
        ))
        c_result = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, 2 * A2 * np.sin(k2 * x - om2 * tw.get_value()) + film_top_y + 1.3, 0]),
            t_range=[-6.5, -0.3, 0.04],
            color="#4ade80", stroke_width=5
        ))
        c_lbl = Text("Constructive → Bright", font_size=18, color="#4ade80", weight=BOLD)
        c_lbl.move_to([-3.5, film_top_y + 0.2, 0])

        # Destructive: right half
        dw1 = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, A2 * np.sin(k2 * x - om2 * tw.get_value()) + film_top_y + 1.3, 0]),
            t_range=[0.3, 6.5, 0.04],
            color="#7dd3fc", stroke_width=3
        ))
        dw2 = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, A2 * np.sin(k2 * x - om2 * tw.get_value() + PI) + film_top_y + 1.3, 0]),
            t_range=[0.3, 6.5, 0.04],
            color="#fdba74", stroke_width=3
        ))
        d_result = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, 0.03 * np.sin(k2 * x) + film_top_y + 1.3, 0]),
            t_range=[0.3, 6.5, 0.04],
            color="#f87171", stroke_width=5
        ))
        d_lbl = Text("Destructive → Dark", font_size=18, color="#f87171", weight=BOLD)
        d_lbl.move_to([3.5, film_top_y + 0.2, 0])

        sep = Line([0, film_top_y + 2.4, 0], [0, film_top_y - 0.1, 0],
                   color="#334155", stroke_width=1.2, stroke_opacity=0.6)

        self.play(FadeIn(sep), run_time=0.4)
        self.play(
            FadeIn(cw1), FadeIn(cw2), FadeIn(c_result),
            FadeIn(dw1), FadeIn(dw2), FadeIn(d_result),
            Write(c_lbl), Write(d_lbl), run_time=1.0
        )
        self.play(tw.animate.set_value(4.0), run_time=3.5, rate_func=linear)
        self.wait(0.4)

        self.play(
            FadeOut(cw1), FadeOut(cw2), FadeOut(c_result),
            FadeOut(dw1), FadeOut(dw2), FadeOut(d_result),
            FadeOut(c_lbl), FadeOut(d_lbl), FadeOut(sep),
            FadeOut(interf_title), run_time=0.7
        )

        # ── PART 8: CONDITIONS FOR INTERFERENCE (44–52s) ──────────────────────
        cond_title = Text("Interference Conditions", font_size=30,
                          color=WHITE, weight=BOLD)
        cond_title.set_color_by_gradient("#38bdf8", "#4ade80")
        cond_title.to_edge(UP, buff=0.45)
        self.play(Write(cond_title), run_time=0.7)

        destr_eq = MathTex(r"2\mu t = n\lambda", font_size=38, color="#f87171")
        destr_note = Text("(Destructive — Dark)", font_size=20, color="#fca5a5")
        destr_group = VGroup(destr_eq, destr_note).arrange(DOWN, buff=0.18)
        destr_box = SurroundingRectangle(destr_group, color="#7f1d1d",
                                          fill_color="#1c0a0a", fill_opacity=0.85,
                                          buff=0.28, corner_radius=0.16)
        destr_group.move_to([-3.0, 0.1, 0])
        destr_box.move_to([-3.0, 0.1, 0])

        constr_eq = MathTex(r"2\mu t = \left(n + \frac{1}{2}\right)\lambda",
                             font_size=38, color="#4ade80")
        constr_note = Text("(Constructive — Bright)", font_size=20, color="#86efac")
        constr_group = VGroup(constr_eq, constr_note).arrange(DOWN, buff=0.18)
        constr_box = SurroundingRectangle(constr_group, color="#14532d",
                                           fill_color="#052e16", fill_opacity=0.85,
                                           buff=0.28, corner_radius=0.16)
        constr_group.move_to([3.0, 0.1, 0])
        constr_box.move_to([3.0, 0.1, 0])

        phase_note = Text("(includes λ/2 phase change at top surface)", font_size=16,
                          color="#64748b")
        phase_note.move_to([0, -1.8, 0])

        self.play(FadeIn(destr_box), Write(destr_eq), Write(destr_note), run_time=1.0)
        self.play(FadeIn(constr_box), Write(constr_eq), Write(constr_note), run_time=1.0)
        self.play(Write(phase_note), run_time=0.7)

        # Animate flicker bright/dark
        for _ in range(2):
            self.play(destr_box.animate.set_fill(color="#3b0000", opacity=0.95), run_time=0.4)
            self.play(constr_box.animate.set_fill(color="#052e16", opacity=0.95), run_time=0.4)
            self.play(destr_box.animate.set_fill(color="#1c0a0a", opacity=0.85), run_time=0.4)
        self.wait(0.5)

        self.play(
            FadeOut(cond_title), FadeOut(destr_box), FadeOut(destr_group),
            FadeOut(constr_box), FadeOut(constr_group), FadeOut(phase_note),
            run_time=0.7
        )

        # ── PART 9: THICKNESS VARIATION (52–60s) ──────────────────────────────
        thick_tracker = ValueTracker(0.15)

        thick_title = Text("Thickness Controls Brightness", font_size=26,
                           color=WHITE, weight=BOLD)
        thick_title.set_color_by_gradient("#fbbf24", "#4ade80")
        thick_title.to_edge(UP, buff=0.45)
        self.play(Write(thick_title), run_time=0.7)

        # Wedge-shaped film
        wedge = always_redraw(lambda: Polygon(
            [-5.5, film_top_y, 0], [5.5, film_top_y, 0],
            [5.5, film_top_y - thick_tracker.get_value() * 5, 0],
            [-5.5, film_top_y - 0.05, 0],
            fill_color="#0ea5e9", fill_opacity=0.25 + thick_tracker.get_value() * 0.3,
            stroke_width=0
        ))

        thick_lbl = always_redraw(lambda: Text(
            f"Thickness t = {thick_tracker.get_value():.2f} (normalized)",
            font_size=20, color="#7dd3fc"
        ).move_to([0, -2.3, 0]))

        bright_indicator = always_redraw(lambda: Rectangle(
            width=11.0,
            height=0.4,
            fill_color="#fde68a",
            fill_opacity=abs(np.sin(PI * thick_tracker.get_value() * 4)) * 0.85,
            stroke_width=0
        ).move_to([0, film_top_y + 0.55, 0]))

        self.play(FadeIn(wedge), FadeIn(thick_lbl), FadeIn(bright_indicator), run_time=0.8)
        self.play(thick_tracker.animate.set_value(1.0), run_time=4.5, rate_func=linear)
        self.wait(0.4)

        self.play(
            FadeOut(thick_title), FadeOut(wedge),
            FadeOut(thick_lbl), FadeOut(bright_indicator),
            run_time=0.6
        )

        # ── PART 10: COLOR FORMATION (60–70s) ─────────────────────────────────
        color_title = Text("Thickness Selects Wavelength → Color!", font_size=26,
                           color=WHITE, weight=BOLD)
        color_title.set_color_by_gradient("#f87171", "#4ade80", "#818cf8")
        color_title.to_edge(UP, buff=0.45)
        self.play(Write(color_title), run_time=0.8)

        tw2 = ValueTracker(0)
        wavelengths = [
            (1.4, "#f87171", "Red  λ_R"),
            (1.0, "#4ade80", "Green  λ_G"),
            (0.7, "#818cf8", "Blue  λ_B"),
        ]

        wave_objs = []
        wave_lbls = []
        y_positions = [1.8, 0.5, -0.8]

        for i, (wl, col, name) in enumerate(wavelengths):
            ki = 2 * PI / wl
            y0 = y_positions[i]
            wbg = always_redraw(lambda ki=ki, col=col, y0=y0: ParametricFunction(
                lambda x: np.array([x, 0.32 * np.sin(ki * x - 2.0 * tw2.get_value()) + y0, 0]),
                t_range=[-6.5, 6.5, 0.04],
                color=col, stroke_width=14, stroke_opacity=0.12
            ))
            wfg = always_redraw(lambda ki=ki, col=col, y0=y0: ParametricFunction(
                lambda x: np.array([x, 0.32 * np.sin(ki * x - 2.0 * tw2.get_value()) + y0, 0]),
                t_range=[-6.5, 6.5, 0.04],
                color=col, stroke_width=3
            ))
            lbl = Text(name, font_size=16, color=col)
            lbl.move_to([-5.5, y0 + 0.45, 0])
            wave_objs.extend([wbg, wfg])
            wave_lbls.append(lbl)

        self.play(*[FadeIn(w) for w in wave_objs],
                  *[Write(l) for l in wave_lbls], run_time=1.0)
        self.play(tw2.animate.set_value(5.0), run_time=4.5, rate_func=linear)

        select_txt = Text("Thickness selects which wavelength reflects strongly",
                          font_size=22, color="#fde68a")
        select_txt.move_to([0, -2.1, 0])
        self.play(Write(select_txt), run_time=0.9)
        self.wait(1.0)

        self.play(
            *[FadeOut(w) for w in wave_objs],
            *[FadeOut(l) for l in wave_lbls],
            FadeOut(color_title), FadeOut(select_txt),
            run_time=0.7
        )

        # ── PART 11: FINAL SUMMARY VISUAL (70–75s) ────────────────────────────
        self.play(
            FadeOut(top_surface), FadeOut(bot_surface),
            FadeOut(film_poly), FadeOut(film_poly2),
            FadeOut(air_lbl), FadeOut(film_lbl), FadeOut(sub_lbl),
            run_time=0.7
        )

        steps = [
            ("Light", "#fef3c7"),
            ("Split", "#fbbf24"),
            ("Path Diff", "#fdba74"),
            ("Phase Δ", "#f87171"),
            ("Interference", "#4ade80"),
        ]
        arrows_pipeline = VGroup()
        boxes_pipeline = VGroup()
        labels_pipeline = VGroup()

        total_w = 12.0
        step_w = total_w / len(steps)
        start_x = -total_w / 2 + step_w / 2

        for i, (name, col) in enumerate(steps):
            xpos = start_x + i * step_w
            box = RoundedRectangle(width=step_w * 0.82, height=0.75,
                                   corner_radius=0.18, fill_color=col,
                                   fill_opacity=0.18, stroke_color=col,
                                   stroke_width=2)
            box.move_to([xpos, 0, 0])
            lbl = Text(name, font_size=19, color=col, weight=BOLD)
            lbl.move_to([xpos, 0, 0])
            boxes_pipeline.add(box)
            labels_pipeline.add(lbl)
            if i < len(steps) - 1:
                arr = Arrow(
                    [xpos + step_w * 0.42, 0, 0],
                    [xpos + step_w * 0.58, 0, 0],
                    color="#475569", buff=0, stroke_width=2,
                    max_tip_length_to_length_ratio=0.4, tip_length=0.18
                )
                arrows_pipeline.add(arr)

        pipeline_title = Text("The Complete Picture", font_size=28,
                              color=WHITE, weight=BOLD)
        pipeline_title.set_color_by_gradient("#38bdf8", "#4ade80")
        pipeline_title.to_edge(UP, buff=0.5)

        self.play(Write(pipeline_title), run_time=0.7)
        self.play(
            LaggedStart(*[FadeIn(b) for b in boxes_pipeline], lag_ratio=0.15),
            LaggedStart(*[Write(l) for l in labels_pipeline], lag_ratio=0.15),
            run_time=1.5
        )
        self.play(
            LaggedStart(*[Create(a) for a in arrows_pipeline], lag_ratio=0.2),
            run_time=1.0
        )
        self.wait(1.5)

        all_objs = VGroup(boxes_pipeline, labels_pipeline, arrows_pipeline, pipeline_title)
        self.play(all_objs.animate.scale(1.1).shift(UP * 0.1), run_time=1.5, rate_func=smooth)
        self.wait(0.5)
        self.play(FadeOut(all_objs), run_time=2.0)
        self.wait(0.3)