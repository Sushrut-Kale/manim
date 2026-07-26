from manim import *
import numpy as np

_VIOLET   = ManimColor("#9B59FF")
_BLUE_B   = ManimColor("#58C4DD")
_BLUE_C   = ManimColor("#29ABCA")
_GREEN_B  = ManimColor("#83C167")
_GREEN_C  = ManimColor("#5FAD41")
_GREEN_A  = ManimColor("#C9E88C")
_TEAL_A   = ManimColor("#ACEAD7")
_TEAL_B   = ManimColor("#5CD0B3")
_YELLOW_A = ManimColor("#FFFF8D")
_YELLOW_B = ManimColor("#F4D345")
_RED_A    = ManimColor("#F7A1A3")
_RED_B    = ManimColor("#E8534A")
_GRAY     = ManimColor("#888888")
_CYAN     = ManimColor("#00FFFF")
_BLUE     = ManimColor("#0000FF")


class StokesLawScene(Scene):
    def construct(self):
        self.camera.background_color = "#020617"

        def make_wave(x, phase=0, amp=0.5, freq=1.2):
            return amp * np.sin(2 * PI * freq * x + phase)

        def make_flipped_wave(x, phase=0, amp=0.5, freq=1.2):
            return -amp * np.sin(2 * PI * freq * x + phase)

        # ─── PART 1: INTRO QUESTION ───────────────────────────────────────────
        t = ValueTracker(0)
        incident_wave = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, make_wave(x, phase=-t.get_value() * 2, amp=0.45, freq=1.0), 0]),
            t_range=[-5, 5, 0.02], color=_BLUE_B, stroke_width=3,
        ))
        reflected_flipped = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, make_flipped_wave(x, phase=-t.get_value() * 2, amp=0.45, freq=1.0), 0]),
            t_range=[-5, 5, 0.02], color=_VIOLET, stroke_width=3,
        ))
        self.play(Create(incident_wave), run_time=1.0)
        self.play(Create(reflected_flipped), run_time=1.0)
        self.play(t.animate.set_value(3), run_time=2.0, rate_func=linear)
        question = Text(
            "Why does a reflected light wave sometimes flip?",
            font="Georgia", font_size=30, color=WHITE,
        ).to_edge(UP, buff=0.4)
        self.play(FadeIn(question, shift=UP * 0.3), run_time=1.2)
        self.wait(0.8)
        self.play(FadeOut(incident_wave), FadeOut(reflected_flipped), FadeOut(question), run_time=1.0)

        # ─── PART 2: TWO MEDIA SETUP ──────────────────────────────────────────
        boundary = Line(LEFT * 6.5, RIGHT * 6.5, color=WHITE, stroke_width=1.5).set_opacity(0.6)
        air_rect   = Rectangle(width=14, height=3.5, fill_color="#0a1628",
                                fill_opacity=0.55, stroke_width=0).move_to(UP * 1.75)
        glass_rect = Rectangle(width=14, height=3.5, fill_color="#0d1f12",
                                fill_opacity=0.55, stroke_width=0).move_to(DOWN * 1.75)
        air_label   = Text("Rarer Medium  (Air)",    font="Georgia", font_size=26, color=_BLUE_B).move_to(UP * 2.8)
        glass_label = Text("Denser Medium  (Glass)", font="Georgia", font_size=26, color=_GREEN_B).move_to(DOWN * 2.8)

        self.play(FadeIn(air_rect), FadeIn(glass_rect), run_time=1.0)
        self.play(Create(boundary), run_time=0.8)
        self.play(Write(air_label), Write(glass_label), run_time=1.2)
        self.wait(0.5)

        # ─── PART 3: RAY FALLING RARER->DENSER ───────────────────────────────
        hit_point = np.array([0.0, 0.0, 0])
        inc_ray   = Arrow(start=np.array([-3.0, 3.0, 0]), end=hit_point, color=_BLUE_B, buff=0, stroke_width=3)
        refl_ray  = Arrow(start=hit_point, end=np.array([3.0, 3.0, 0]),  color=_VIOLET, buff=0, stroke_width=3)
        trans_ray = Arrow(start=hit_point, end=np.array([2.0, -2.8, 0]), color=_GREEN_B, buff=0, stroke_width=2.5)

        inc_ray_lbl   = Text("Incident Ray",              font="Georgia", font_size=20, color=_BLUE_B).move_to(np.array([-4.2, 2.3, 0]))
        refl_ray_lbl  = Text("Reflected Ray\n(flipped pi)", font="Georgia", font_size=18, color=_VIOLET).move_to(np.array([4.6, 2.3, 0]))
        trans_ray_lbl = Text("Transmitted\n(Refracted)",  font="Georgia", font_size=18, color=_GREEN_B).move_to(np.array([4.2, -1.8, 0]))

        self.play(GrowArrow(inc_ray), Write(inc_ray_lbl), run_time=1.2)
        self.play(Flash(hit_point, color=YELLOW, flash_radius=0.5, line_length=0.3), run_time=0.5)
        self.play(GrowArrow(refl_ray), GrowArrow(trans_ray), run_time=1.0)
        self.play(Write(refl_ray_lbl), Write(trans_ray_lbl), run_time=0.9)
        self.wait(1.0)
        self.play(FadeOut(inc_ray), FadeOut(refl_ray), FadeOut(trans_ray),
                  FadeOut(inc_ray_lbl), FadeOut(refl_ray_lbl), FadeOut(trans_ray_lbl), run_time=0.7)

        # ─── PART 4: RARER->DENSER WAVES ─────────────────────────────────────
        # Waves occupy x in [-3.5, 3.5] to leave room on sides for arrows/labels
        t2 = ValueTracker(0)
        inc_wave_rd = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, make_wave(x, phase=-t2.get_value() * 2.5, amp=0.38, freq=1.1) + 1.45, 0]),
            t_range=[-3.2, 3.2, 0.02], color=_BLUE_B, stroke_width=3,
        ))
        # Direction arrow far left, label above it — no wave overlap
        dir_arrow_inc = Arrow(start=UP * 2.9 + LEFT * 6.0, end=UP * 0.25 + LEFT * 6.0,
                              color=_BLUE_B, stroke_width=2.5, buff=0)
        dir_lbl_inc   = Text("Incident\n(down)", font="Georgia", font_size=15,
                              color=_BLUE_B).move_to(LEFT * 5.0 + UP * 3.2)
        inc_label_rd  = Text("Incident Wave (Air)", font="Georgia", font_size=19,
                              color=_BLUE_B).move_to(RIGHT * 5.2 + UP * 2.3)

        self.play(Create(inc_wave_rd), FadeIn(inc_label_rd),
                  GrowArrow(dir_arrow_inc), Write(dir_lbl_inc), run_time=1.0)
        self.play(t2.animate.set_value(2.0), run_time=2.0, rate_func=linear)

        t3 = ValueTracker(0)
        refl_wave_rd = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, make_flipped_wave(x, phase=t3.get_value() * 2.5, amp=0.38, freq=1.1) + 1.45, 0]),
            t_range=[-3.2, 3.2, 0.02], color=_VIOLET, stroke_width=3,
        ))
        # Reflected arrow same left column, label clearly above
        dir_arrow_refl = Arrow(start=UP * 0.25 + LEFT * 5.2, end=UP * 2.9 + LEFT * 5.2,
                               color=_VIOLET, stroke_width=2.5, buff=0)
        dir_lbl_refl   = Text("Reflected\n(up, flipped)", font="Georgia", font_size=14,
                               color=_VIOLET).move_to(LEFT * 4.1 + UP * 3.25)
        refl_label_rd  = Text("Reflected (flipped)", font="Georgia", font_size=19,
                               color=_VIOLET).move_to(RIGHT * 5.2 + UP * 0.65)

        t2b = ValueTracker(0)
        trans_wave_rd = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, make_wave(x, phase=-t2b.get_value() * 2.0, amp=0.30, freq=1.4) - 1.5, 0]),
            t_range=[-3.2, 3.2, 0.02], color=_GREEN_B, stroke_width=2.5,
        ))
        # Transmitted arrow on right side
        dir_arrow_trans = Arrow(start=DOWN * 0.25 + RIGHT * 5.8, end=DOWN * 2.9 + RIGHT * 5.8,
                                color=_GREEN_B, stroke_width=2.5, buff=0)
        dir_lbl_trans   = Text("Transmitted\n(down)", font="Georgia", font_size=15,
                                color=_GREEN_B).move_to(RIGHT * 4.8 + DOWN * 3.25)
        trans_label_rd  = Text("Transmitted (Glass)", font="Georgia", font_size=19,
                                color=_GREEN_B).move_to(RIGHT * 5.1 + DOWN * 2.1)

        self.play(Flash(boundary.get_center(), color=YELLOW, flash_radius=0.5, line_length=0.3), run_time=0.5)
        self.play(Create(refl_wave_rd), FadeIn(refl_label_rd),
                  GrowArrow(dir_arrow_refl), Write(dir_lbl_refl),
                  Create(trans_wave_rd), FadeIn(trans_label_rd),
                  GrowArrow(dir_arrow_trans), Write(dir_lbl_trans), run_time=1.0)
        self.play(t2.animate.set_value(4.5), t3.animate.set_value(2.5),
                  t2b.animate.set_value(2.5), run_time=2.5, rate_func=linear)

        # Physics text in center of glass region, away from labels
        rd_text1 = MathTex(r"\text{Rarer} \rightarrow \text{Denser reflection}",
                           font_size=26, color=_YELLOW_A).move_to(DOWN * 1.0 + LEFT * 1.8)
        rd_text2 = MathTex(r"\Delta\phi = \pi \;\Rightarrow\; \tfrac{\lambda}{2}\text{ phase shift}",
                           font_size=26, color=_YELLOW_B).move_to(DOWN * 1.65 + LEFT * 1.8)

        self.play(Write(rd_text1), run_time=1.0)
        self.play(Write(rd_text2), run_time=1.2)
        self.wait(1.2)
        self.play(
            FadeOut(inc_wave_rd), FadeOut(refl_wave_rd), FadeOut(trans_wave_rd),
            FadeOut(inc_label_rd), FadeOut(refl_label_rd), FadeOut(trans_label_rd),
            FadeOut(dir_arrow_inc), FadeOut(dir_lbl_inc),
            FadeOut(dir_arrow_refl), FadeOut(dir_lbl_refl),
            FadeOut(dir_arrow_trans), FadeOut(dir_lbl_trans),
            FadeOut(rd_text1), FadeOut(rd_text2), run_time=0.8)

        # ─── PART 5: VISUALIZE THE FLIP ───────────────────────────────────────
        orig_wave_static = ParametricFunction(
            lambda x: np.array([x, make_wave(x, phase=0, amp=0.5, freq=1.0) + 1.5, 0]),
            t_range=[-4, 4, 0.02], color=_BLUE_B, stroke_width=3.5,
        )
        flip_wave_static = ParametricFunction(
            lambda x: np.array([x, make_flipped_wave(x, phase=0, amp=0.5, freq=1.0) + 1.5, 0]),
            t_range=[-4, 4, 0.02], color=_VIOLET, stroke_width=3.5,
        )
        crest_dot    = Dot(np.array([0, 2.0, 0]), color=YELLOW, radius=0.12)
        trough_dot   = Dot(np.array([0, 1.0, 0]), color=RED, radius=0.12)
        crest_arrow  = Arrow(start=np.array([0.7, 2.35, 0]), end=np.array([0.0, 2.05, 0]),
                             color=YELLOW, buff=0.05, stroke_width=2.5)
        trough_arrow = Arrow(start=np.array([0.7, 0.65, 0]), end=np.array([0.0, 0.95, 0]),
                             color=RED, buff=0.05, stroke_width=2.5)
        crest_lbl = MathTex(r"\text{Crest} \rightarrow \text{Trough}",
                            font_size=24, color=YELLOW).move_to(RIGHT * 2.8 + UP * 2.35)
        flip_lbl  = Text("Wave Inversion", font="Georgia", font_size=26, color=WHITE).move_to(DOWN * 1.1)

        self.play(Create(orig_wave_static), run_time=0.8)
        self.wait(0.3)
        self.play(Transform(orig_wave_static, flip_wave_static), run_time=1.5)
        self.play(FadeIn(crest_dot), FadeIn(trough_dot),
                  GrowArrow(crest_arrow), GrowArrow(trough_arrow), Write(crest_lbl), run_time=1.2)
        self.play(Write(flip_lbl), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(orig_wave_static), FadeOut(crest_dot), FadeOut(trough_dot),
                  FadeOut(crest_arrow), FadeOut(trough_arrow), FadeOut(crest_lbl), FadeOut(flip_lbl), run_time=0.8)

        # ─── PART 6: RAY DENSER->RARER ────────────────────────────────────────
        hit2 = np.array([0.0, 0.0, 0])
        inc_ray2   = Arrow(start=np.array([-2.5, -3.0, 0]), end=hit2, color=_GREEN_B, buff=0, stroke_width=3)
        refl_ray2  = Arrow(start=hit2, end=np.array([2.5, -3.0, 0]),  color=_TEAL_B,  buff=0, stroke_width=3)
        trans_ray2 = Arrow(start=hit2, end=np.array([2.5,  3.0, 0]),  color=_BLUE_B,  buff=0, stroke_width=2.5)

        inc_lbl2   = Text("Incident Ray\n(from glass)", font="Georgia", font_size=19, color=_GREEN_B).move_to(np.array([-4.5, -2.2, 0]))
        refl_lbl2  = Text("Reflected Ray\n(No flip)",   font="Georgia", font_size=19, color=_TEAL_B).move_to(np.array([4.5, -2.2, 0]))
        trans_lbl2 = Text("Transmitted Ray",            font="Georgia", font_size=19, color=_BLUE_B).move_to(np.array([4.5,  2.2, 0]))

        self.play(GrowArrow(inc_ray2), Write(inc_lbl2), run_time=1.2)
        self.play(Flash(hit2, color=GREEN, flash_radius=0.5, line_length=0.3), run_time=0.5)
        self.play(GrowArrow(refl_ray2), GrowArrow(trans_ray2), run_time=1.0)
        self.play(Write(refl_lbl2), Write(trans_lbl2), run_time=0.9)
        self.wait(1.0)
        self.play(FadeOut(inc_ray2), FadeOut(refl_ray2), FadeOut(trans_ray2),
                  FadeOut(inc_lbl2), FadeOut(refl_lbl2), FadeOut(trans_lbl2), run_time=0.7)

        # ─── PART 7: DENSER->RARER WAVES ─────────────────────────────────────
        t4 = ValueTracker(0)
        inc_wave_dr = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, make_wave(x, phase=-t4.get_value() * 2.5, amp=0.38, freq=1.1) - 1.45, 0]),
            t_range=[-3.2, 3.2, 0.02], color=_GREEN_B, stroke_width=3,
        ))
        dir_arrow_inc2 = Arrow(start=DOWN * 2.9 + LEFT * 6.0, end=DOWN * 0.25 + LEFT * 6.0,
                               color=_GREEN_B, stroke_width=2.5, buff=0)
        dir_lbl_inc2   = Text("Incident\n(up)", font="Georgia", font_size=15,
                               color=_GREEN_B).move_to(LEFT * 5.0 + DOWN * 3.25)
        inc_lbl_dr     = Text("Incident Wave (Glass)", font="Georgia", font_size=19,
                               color=_GREEN_B).move_to(RIGHT * 5.1 + DOWN * 2.1)

        self.play(Create(inc_wave_dr), FadeIn(inc_lbl_dr),
                  GrowArrow(dir_arrow_inc2), Write(dir_lbl_inc2), run_time=1.0)
        self.play(t4.animate.set_value(2.0), run_time=2.0, rate_func=linear)

        t5 = ValueTracker(0)
        refl_wave_dr = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, make_wave(x, phase=t5.get_value() * 2.5, amp=0.38, freq=1.1) - 1.45, 0]),
            t_range=[-3.2, 3.2, 0.02], color=_TEAL_B, stroke_width=3,
        ))
        dir_arrow_refl2 = Arrow(start=DOWN * 0.25 + LEFT * 5.2, end=DOWN * 2.9 + LEFT * 5.2,
                                color=_TEAL_B, stroke_width=2.5, buff=0)
        dir_lbl_refl2   = Text("Reflected\n(down, no flip)", font="Georgia", font_size=14,
                                color=_TEAL_B).move_to(LEFT * 4.0 + DOWN * 3.3)
        refl_lbl_dr     = Text("Reflected (NOT flipped)", font="Georgia", font_size=19,
                                color=_TEAL_B).move_to(RIGHT * 5.0 + DOWN * 0.55)

        t4b = ValueTracker(0)
        trans_wave_dr = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, make_wave(x, phase=-t4b.get_value() * 2.5, amp=0.38, freq=0.9) + 1.45, 0]),
            t_range=[-3.2, 3.2, 0.02], color=_BLUE_B, stroke_width=2.5,
        ))
        dir_arrow_trans2 = Arrow(start=UP * 0.25 + RIGHT * 5.8, end=UP * 2.9 + RIGHT * 5.8,
                                 color=_BLUE_B, stroke_width=2.5, buff=0)
        dir_lbl_trans2   = Text("Transmitted\n(up)", font="Georgia", font_size=15,
                                 color=_BLUE_B).move_to(RIGHT * 4.8 + UP * 3.25)
        trans_lbl_dr     = Text("Transmitted (Air)", font="Georgia", font_size=19,
                                 color=_BLUE_B).move_to(RIGHT * 5.1 + UP * 2.1)

        self.play(Flash(boundary.get_center(), color=GREEN, flash_radius=0.5, line_length=0.3), run_time=0.5)
        self.play(Create(refl_wave_dr), FadeIn(refl_lbl_dr),
                  GrowArrow(dir_arrow_refl2), Write(dir_lbl_refl2),
                  Create(trans_wave_dr), FadeIn(trans_lbl_dr),
                  GrowArrow(dir_arrow_trans2), Write(dir_lbl_trans2), run_time=1.0)
        self.play(t4.animate.set_value(4.5), t5.animate.set_value(2.5),
                  t4b.animate.set_value(2.5), run_time=2.5, rate_func=linear)

        # Physics text in TOP-CENTER of air region — well above wave
        dr_text1 = MathTex(r"\text{Denser} \rightarrow \text{Rarer reflection}",
                           font_size=26, color=_TEAL_A).move_to(UP * 2.75 + LEFT * 1.0)
        dr_text2 = Text("No phase change", font="Georgia", font_size=22,
                        color=_GREEN_A).move_to(UP * 2.2 + LEFT * 1.0)

        self.play(Write(dr_text1), run_time=1.0)
        self.play(Write(dr_text2), run_time=0.9)
        self.wait(1.2)
        self.play(
            FadeOut(inc_wave_dr), FadeOut(refl_wave_dr), FadeOut(trans_wave_dr),
            FadeOut(inc_lbl_dr), FadeOut(refl_lbl_dr), FadeOut(trans_lbl_dr),
            FadeOut(dir_arrow_inc2), FadeOut(dir_lbl_inc2),
            FadeOut(dir_arrow_refl2), FadeOut(dir_lbl_refl2),
            FadeOut(dir_arrow_trans2), FadeOut(dir_lbl_trans2),
            FadeOut(dr_text1), FadeOut(dr_text2), run_time=0.8)

        # ─── PART 8: SIDE-BY-SIDE ─────────────────────────────────────────────
        self.play(FadeOut(air_rect), FadeOut(glass_rect),
                  FadeOut(boundary), FadeOut(air_label), FadeOut(glass_label), run_time=0.7)

        divider = DashedLine(UP * 3.5, DOWN * 3.5, color=_GRAY, stroke_width=1.5).set_x(0)
        left_bnd  = Line(LEFT * 6 + UP * 0, LEFT * 0.3 + UP * 0, color=WHITE, stroke_width=1.2, stroke_opacity=0.5)
        left_inc  = ParametricFunction(
            lambda x: np.array([x - 3.5, make_wave(x, amp=0.42, freq=1.0) + 1.2, 0]),
            t_range=[0, 4.5, 0.02], color=_BLUE_B, stroke_width=2.8)
        left_refl = ParametricFunction(
            lambda x: np.array([x - 3.5, make_flipped_wave(x, amp=0.42, freq=1.0) + 1.2, 0]),
            t_range=[0, 4.5, 0.02], color=_VIOLET, stroke_width=2.8)
        left_title = MathTex(r"\text{Rarer} \rightarrow \text{Denser}",
                             font_size=28, color=_BLUE_B).move_to(LEFT * 3.5 + UP * 2.7)
        left_tag   = Text("Phase Reversal", font="Georgia", font_size=20,
                          color=YELLOW).move_to(LEFT * 3.5 + DOWN * 1.5)
        left_pi    = MathTex(r"\Delta\phi = \pi", font_size=28,
                             color=_YELLOW_B).move_to(LEFT * 3.5 + DOWN * 2.2)

        right_bnd  = Line(RIGHT * 0.3 + UP * 0, RIGHT * 6 + UP * 0, color=WHITE, stroke_width=1.2, stroke_opacity=0.5)
        right_inc  = ParametricFunction(
            lambda x: np.array([x + 0.3, make_wave(x, amp=0.42, freq=1.0) + 1.2, 0]),
            t_range=[0, 4.5, 0.02], color=_GREEN_B, stroke_width=2.8)
        right_refl = ParametricFunction(
            lambda x: np.array([x + 0.3, make_wave(x, amp=0.42, freq=1.0) + 1.2, 0]),
            t_range=[0, 4.5, 0.02], color=_TEAL_B, stroke_width=2.8)
        right_title = MathTex(r"\text{Denser} \rightarrow \text{Rarer}",
                              font_size=28, color=_GREEN_B).move_to(RIGHT * 3.0 + UP * 2.7)
        right_tag   = Text("No Phase Reversal", font="Georgia", font_size=20,
                           color=_TEAL_A).move_to(RIGHT * 3.0 + DOWN * 1.5)
        right_zero  = MathTex(r"\Delta\phi = 0", font_size=28,
                              color=_TEAL_B).move_to(RIGHT * 3.0 + DOWN * 2.2)

        self.play(Create(divider), Create(left_bnd), Create(right_bnd), run_time=0.8)
        self.play(Create(left_inc), Create(left_refl), Create(right_inc), Create(right_refl), run_time=1.2)
        self.play(Write(left_title), Write(right_title), run_time=0.9)
        self.play(Write(left_tag), Write(right_tag), Write(left_pi), Write(right_zero), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(divider), FadeOut(left_bnd), FadeOut(right_bnd),
                  FadeOut(left_inc), FadeOut(left_refl), FadeOut(right_inc), FadeOut(right_refl),
                  FadeOut(left_title), FadeOut(right_title), FadeOut(left_tag), FadeOut(right_tag),
                  FadeOut(left_pi), FadeOut(right_zero), run_time=1.0)

        # ─── PART 9: THIN FILM ────────────────────────────────────────────────
        film_top  = Line(LEFT * 5, RIGHT * 5, color=_BLUE_C, stroke_width=2).move_to(UP * 1.2)
        film_bot  = Line(LEFT * 5, RIGHT * 5, color=_BLUE_C, stroke_width=2).move_to(DOWN * 1.2)
        film_rect = Rectangle(width=10, height=2.4, fill_color="#0a1a3a",
                              fill_opacity=0.5, stroke_width=0).move_to(ORIGIN)
        film_lbl   = Text("Thin Film", font="Georgia", font_size=22, color=_BLUE_C).move_to(RIGHT * 4.2)
        air_lbl2   = Text("Air",       font="Georgia", font_size=20, color=WHITE).move_to(LEFT * 5.5 + UP * 2.2)
        glass_lbl2 = Text("Glass",     font="Georgia", font_size=20, color=_GREEN_B).move_to(LEFT * 5.5 + DOWN * 2.2)

        ray1_inc  = Arrow(start=LEFT * 3 + UP * 3,    end=LEFT * 3 + UP * 1.2,   color=_BLUE_B, stroke_width=2.5, buff=0)
        ray1_refl = Arrow(start=LEFT * 3 + UP * 1.2,  end=LEFT * 2 + UP * 3,     color=_VIOLET, stroke_width=2.5, buff=0)
        ray1_lbl  = Text("Phase flip (pi)", font="Georgia", font_size=18, color=_VIOLET).move_to(LEFT * 0.8 + UP * 2.6)

        ray2_inc  = Arrow(start=RIGHT * 1 + UP * 3,    end=RIGHT * 1 + DOWN * 1.2, color=_BLUE_B, stroke_width=2.5, buff=0)
        ray2_refl = Arrow(start=RIGHT * 1 + DOWN * 1.2, end=RIGHT * 2 + UP * 3,    color=_TEAL_B, stroke_width=2.5, buff=0)
        ray2_lbl  = Text("No phase flip", font="Georgia", font_size=18, color=_TEAL_B).move_to(RIGHT * 3.8 + UP * 2.6)

        path_diff = MathTex(r"\text{Path Diff} = 2\mu t + \tfrac{\lambda}{2}",
                            font_size=30, color=_YELLOW_A).move_to(DOWN * 2.6)

        self.play(FadeIn(film_rect), Create(film_top), Create(film_bot), run_time=0.8)
        self.play(Write(film_lbl), Write(air_lbl2), Write(glass_lbl2), run_time=0.8)
        self.play(GrowArrow(ray1_inc), GrowArrow(ray2_inc), run_time=1.0)
        self.play(GrowArrow(ray1_refl), GrowArrow(ray2_refl), run_time=1.0)
        self.play(Write(ray1_lbl), Write(ray2_lbl), run_time=0.9)
        self.play(Write(path_diff), run_time=1.2)
        self.wait(1.5)
        self.play(FadeOut(film_rect), FadeOut(film_top), FadeOut(film_bot),
                  FadeOut(film_lbl), FadeOut(air_lbl2), FadeOut(glass_lbl2),
                  FadeOut(ray1_inc), FadeOut(ray1_refl), FadeOut(ray2_inc), FadeOut(ray2_refl),
                  FadeOut(ray1_lbl), FadeOut(ray2_lbl), FadeOut(path_diff), run_time=1.0)

        # ─── PART 10: NEWTON'S RINGS ──────────────────────────────────────────
        nr_title = Text("Newton's Rings  -  Central Spot", font="Georgia",
                        font_size=28, color=WHITE).to_edge(UP, buff=0.4)
        self.play(Write(nr_title), run_time=0.9)
        rings = VGroup()
        for r in [0.3, 0.65, 1.0, 1.38, 1.75, 2.12, 2.5]:
            ring = Circle(radius=r, color=interpolate_color(_BLUE, _CYAN, r / 2.5),
                          stroke_width=1.5, stroke_opacity=0.7)
            rings.add(ring)
        rings.move_to(DOWN * 0.4 + LEFT * 1.5)
        self.play(Create(rings), run_time=1.5)
        center_dot  = Dot(rings.get_center(), color=BLACK, radius=0.18).set_fill(BLACK, opacity=1)
        center_ring = Circle(radius=0.18, color=WHITE, stroke_width=1.5).move_to(rings.get_center())
        self.play(FadeIn(center_dot), Create(center_ring), run_time=0.7)
        t_zero     = MathTex(r"t = 0", font_size=30, color=YELLOW).move_to(RIGHT * 3.5 + UP * 0.8)
        phase_note = MathTex(r"\text{Path diff} = \tfrac{\lambda}{2} \Rightarrow \text{Destructive}",
                             font_size=26, color=_RED_B).move_to(RIGHT * 3.5 + DOWN * 0.2)
        dark_lbl   = Text("Central Dark Spot", font="Georgia", font_size=24,
                          color=_RED_A).move_to(RIGHT * 3.5 + DOWN * 1.2)
        self.play(Write(t_zero), run_time=0.7)
        self.play(Write(phase_note), run_time=1.0)
        self.play(Write(dark_lbl), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(nr_title), FadeOut(rings), FadeOut(center_dot), FadeOut(center_ring),
                  FadeOut(t_zero), FadeOut(phase_note), FadeOut(dark_lbl), run_time=1.0)

        # ─── PART 11: STOKES' LAW SUMMARY ────────────────────────────────────
        summary_title = Text("Stokes' Law", font="Georgia", font_size=38,
                             color=_YELLOW_A, weight=BOLD).to_edge(UP, buff=0.5)
        line1  = MathTex(r"\text{Reflection: rarer} \rightarrow \text{denser medium}",
                         font_size=30, color=_BLUE_C).move_to(UP * 0.9)
        line1b = MathTex(r"\Rightarrow \text{ Phase shift of } \pi",
                         font_size=28, color=_VIOLET).next_to(line1, DOWN, buff=0.25)
        sep    = Line(LEFT * 4, RIGHT * 4, color=_GRAY, stroke_width=0.8).move_to(DOWN * 0.22)
        line2  = MathTex(r"\text{Reflection: denser} \rightarrow \text{rarer medium}",
                         font_size=30, color=_GREEN_C).move_to(DOWN * 0.9)
        line2b = MathTex(r"\Rightarrow \text{ No phase shift}",
                         font_size=28, color=_TEAL_B).next_to(line2, DOWN, buff=0.25)

        self.play(Write(summary_title), run_time=1.0)
        self.play(Write(line1),  run_time=1.0)
        self.play(Write(line1b), run_time=0.8)
        self.play(Create(sep),   run_time=0.5)
        self.play(Write(line2),  run_time=1.0)
        self.play(Write(line2b), run_time=0.8)
        self.wait(2.5)
        self.play(FadeOut(summary_title), FadeOut(line1), FadeOut(line1b),
                  FadeOut(sep), FadeOut(line2), FadeOut(line2b), run_time=1.0)

        # ─── PART 12: CINEMATIC END ───────────────────────────────────────────
        t_end = ValueTracker(0)
        end_wave1 = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, make_wave(x, phase=-t_end.get_value() * 1.5, amp=0.55, freq=0.9) + 0.6, 0]),
            t_range=[-6, 6, 0.02], color=_BLUE_B, stroke_width=2.5, stroke_opacity=0.7,
        ))
        end_wave2 = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, make_wave(x, phase=-t_end.get_value() * 1.5 + PI, amp=0.55, freq=0.9) - 0.6, 0]),
            t_range=[-6, 6, 0.02], color=_VIOLET, stroke_width=2.5, stroke_opacity=0.7,
        ))
        final_text = Text("Stokes' Law explains phase reversal",
                          font="Georgia", font_size=34, color=WHITE).move_to(ORIGIN)
        self.play(Create(end_wave1), Create(end_wave2), run_time=0.8)
        self.play(t_end.animate.set_value(4), run_time=2.5, rate_func=linear)
        self.play(Write(final_text), t_end.animate.set_value(6), run_time=2.5, rate_func=linear)
        self.wait(0.5)
        self.play(FadeOut(end_wave1, run_time=2.0), FadeOut(end_wave2, run_time=2.0),
                  FadeOut(final_text, run_time=2.0))
        self.wait(0.5)
