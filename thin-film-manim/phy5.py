from manim import *
import numpy as np


class NewtonsRingsComplete(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#020617"

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 1: AIM AND APPARATUS
        # ══════════════════════════════════════════════════════════════════════

        title_aim = Text("AIM", font_size=42, color="#fde68a", weight=BOLD)
        title_aim.to_edge(UP, buff=0.5)
        underline = Line(
            title_aim.get_left(), title_aim.get_right(),
            color="#fbbf24", stroke_width=2
        ).next_to(title_aim, DOWN, buff=0.08)

        aim_text = Text(
            "To determine the wavelength of sodium light\nusing Newton's Rings experiment",
            font_size=26, color="#e2e8f0", line_spacing=1.4
        )
        aim_text.next_to(underline, DOWN, buff=0.45)

        self.play(FadeIn(title_aim, shift=DOWN * 0.3), run_time=1.2)
        self.play(Create(underline), run_time=0.6)
        self.play(Write(aim_text), run_time=2.0)
        self.wait(1.5)

        sep = DashedLine(
            [-6.5, 0, 0], [6.5, 0, 0],
            color="#1e3a5f", stroke_width=1.5, dash_length=0.2
        )
        sep.next_to(aim_text, DOWN, buff=0.45)
        self.play(Create(sep), run_time=0.8)

        title_app = Text("APPARATUS REQUIRED", font_size=34,
                         color="#7dd3fc", weight=BOLD)
        title_app.next_to(sep, DOWN, buff=0.35)
        underline2 = Line(
            title_app.get_left(), title_app.get_right(),
            color="#38bdf8", stroke_width=2
        ).next_to(title_app, DOWN, buff=0.08)

        self.play(FadeIn(title_app, shift=DOWN * 0.2), run_time=1.0)
        self.play(Create(underline2), run_time=0.5)

        apparatus = [
            ("1.", "Plano-convex lens"),
            ("2.", "Optically plane glass plate"),
            ("3.", "Sodium vapour lamp"),
            ("4.", "Travelling microscope"),
            ("5.", "Magnifying glass"),
        ]

        items_group = VGroup()
        for num, item in apparatus:
            num_txt = Text(num, font_size=22, color="#94a3b8")
            item_txt = Text(item, font_size=22, color="#fde68a")
            row = VGroup(num_txt, item_txt).arrange(RIGHT, buff=0.3)
            items_group.add(row)

        items_group.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        items_group.next_to(underline2, DOWN, buff=0.4)
        items_group.shift(RIGHT * 0.5)

        for item in items_group:
            self.play(FadeIn(item, shift=RIGHT * 0.3), run_time=0.6)

        self.wait(2.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)
        self.wait(0.3)

        # ══════════════════════════════════════════════════════════════════════
        # SCENE 2: NEWTON'S RINGS MASTER
        # ══════════════════════════════════════════════════════════════════════

        grid = NumberPlane(
            x_range=[-8, 8, 1], y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": "#0f172a",
                "stroke_width": 1,
                "stroke_opacity": 0.5
            },
            axis_config={"stroke_opacity": 0},
        )
        self.play(FadeIn(grid, run_time=2.5))

        title = Text("Newton's Rings Experiment", font_size=36, color=WHITE)
        title.set_opacity(0.92)
        title.to_edge(UP, buff=0.3)
        self.play(FadeIn(title, run_time=2.5))
        self.wait(2.5)

        glass_plate = Rectangle(
            width=5.0, height=0.22,
            fill_color="#1e3a5f", fill_opacity=0.85,
            stroke_color="#94a3b8", stroke_width=2
        )
        glass_plate.move_to([0, -2.8, 0])

        plate_group = VGroup(glass_plate)
        self.play(FadeIn(plate_group, run_time=2.0))
        self.wait(0.5)

        glass_lbl = Text("Plane Glass Plate", font_size=16, color="#94a3b8")
        glass_lbl.next_to(glass_plate, LEFT, buff=0.25)
        self.play(FadeIn(glass_lbl, run_time=1.5))
        self.wait(1.5)

        lens_cx = 0.0
        lens_cy = -2.8 + 0.11

        def lens_bottom_y(x, R=3.2):
            return lens_cy + (x ** 2) / (2 * R)

        lens_hw = 2.0
        lens_curve = ParametricFunction(
            lambda x: np.array([lens_cx + x, lens_bottom_y(x), 0]),
            t_range=[-lens_hw, lens_hw, 0.04],
            color="#7dd3fc", stroke_width=2.5
        )
        lens_top_y = lens_bottom_y(lens_hw) + 0.45
        lens_top_line = Line(
            [lens_cx - lens_hw, lens_top_y, 0],
            [lens_cx + lens_hw, lens_top_y, 0],
            color="#7dd3fc", stroke_width=2.5
        )
        lens_left_edge = Line(
            [lens_cx - lens_hw, lens_bottom_y(-lens_hw), 0],
            [lens_cx - lens_hw, lens_top_y, 0],
            color="#7dd3fc", stroke_width=2.5
        )
        lens_right_edge = Line(
            [lens_cx + lens_hw, lens_bottom_y(lens_hw), 0],
            [lens_cx + lens_hw, lens_top_y, 0],
            color="#7dd3fc", stroke_width=2.5
        )
        lens_fill_pts = [
            np.array([lens_cx + x, lens_bottom_y(x), 0])
            for x in np.linspace(-lens_hw, lens_hw, 50)
        ]
        lens_fill_pts += [
            np.array([lens_cx + lens_hw, lens_top_y, 0]),
            np.array([lens_cx - lens_hw, lens_top_y, 0]),
        ]
        lens_fill = Polygon(*lens_fill_pts,
                            fill_color="#0ea5e9", fill_opacity=0.18,
                            stroke_width=0)

        lens_group = VGroup(lens_fill, lens_curve, lens_top_line,
                            lens_left_edge, lens_right_edge)
        lens_group.shift(UP * 4)

        self.play(lens_group.animate(run_time=3.0, rate_func=smooth).shift(DOWN * 4))

        contact_glow = Dot([lens_cx, lens_cy, 0], radius=0.08,
                           color="#fbbf24", fill_opacity=0.75)
        self.play(FadeIn(contact_glow, run_time=0.8))
        self.wait(0.5)

        lens_lbl = Text("Plano-Convex Lens", font_size=16, color="#7dd3fc")
        lens_lbl.next_to(lens_right_edge, RIGHT, buff=0.25)
        self.play(FadeIn(lens_lbl, run_time=1.5))
        self.wait(2.0)

        self.play(
            self.camera.frame.animate(
                run_time=2.5, rate_func=smooth
            ).scale(0.45).move_to([lens_cx, lens_cy - 0.1, 0])
        )
        self.wait(0.8)

        air_film_glow = ParametricFunction(
            lambda x: np.array([lens_cx + x, lens_bottom_y(x) - 0.012, 0]),
            t_range=[-lens_hw, lens_hw, 0.04],
            color="#fde68a", stroke_width=10, stroke_opacity=0.18
        )
        air_film_line = ParametricFunction(
            lambda x: np.array([lens_cx + x, lens_bottom_y(x) - 0.012, 0]),
            t_range=[-lens_hw, lens_hw, 0.04],
            color="#fde68a", stroke_width=2.2, stroke_opacity=0.85
        )
        self.play(Create(air_film_glow, run_time=2.0),
                  Create(air_film_line, run_time=2.0))
        self.wait(0.5)

        air_film_lbl = Text("Thin Air Film", font_size=8, color="#fde68a")
        air_film_lbl.move_to([lens_cx - 0.9, lens_cy - 0.38, 0])
        thickness_note = Text("t increases away from centre", font_size=7,
                              color="#fbbf24")
        thickness_note.next_to(air_film_lbl, DOWN, buff=0.04)
        self.play(FadeIn(air_film_lbl, run_time=1.2),
                  FadeIn(thickness_note, run_time=1.2))
        self.wait(2.0)

        self.play(
            self.camera.frame.animate(
                run_time=2.5, rate_func=smooth
            ).scale(1 / 0.45).move_to(ORIGIN)
        )
        self.wait(0.8)

        splitter_cx = 0.0
        splitter_cy = -0.3

        splitter = Rectangle(
            width=1.5, height=0.12,
            fill_color="#bae6fd", fill_opacity=0.35,
            stroke_color="#7dd3fc", stroke_width=2.5
        )
        splitter.move_to([splitter_cx, splitter_cy, 0])
        splitter.rotate(PI / 4)

        splitter_lbl = Text("Glass Plate (45°)", font_size=14, color="#7dd3fc")
        splitter_lbl.move_to([-2.8, splitter_cy + 0.5, 0])

        self.play(FadeIn(splitter, run_time=1.5))
        self.play(FadeIn(splitter_lbl, run_time=1.2))
        self.wait(1.5)

        lamp_cx = 5.5
        lamp_cy = splitter_cy

        lamp_body = RoundedRectangle(
            width=0.75, height=1.0, corner_radius=0.15,
            fill_color="#78350f", fill_opacity=0.92,
            stroke_color="#fbbf24", stroke_width=2
        )
        lamp_bulb = Ellipse(
            width=0.6, height=0.28,
            fill_color="#fef08a", fill_opacity=0.88,
            stroke_color="#fbbf24", stroke_width=1.5
        )
        lamp_stand = Line([0, 0, 0], [0, -1.0, 0], color="#92400e", stroke_width=4)
        lamp_base = Rectangle(
            width=1.1, height=0.18,
            fill_color="#92400e", fill_opacity=0.95,
            stroke_color="#fbbf24", stroke_width=1
        )

        lamp_group = VGroup(lamp_body, lamp_bulb, lamp_stand, lamp_base)
        lamp_group.move_to([lamp_cx, lamp_cy, 0])

        self.play(FadeIn(lamp_group, run_time=2.0))
        self.wait(0.5)

        rays = VGroup()
        for dy in [-0.15, 0, 0.15]:
            ray = Line(
                [lamp_cx - 0.4, lamp_cy + dy, 0],
                [splitter_cx + 0.1, lamp_cy + dy, 0],
                stroke_color="#fef08a", stroke_width=1.8, stroke_opacity=0.55
            )
            rays.add(ray)
        ray_down = Line(
            [splitter_cx, splitter_cy - 0.05, 0],
            [splitter_cx, lens_top_y + 0.05, 0],
            stroke_color="#fef08a", stroke_width=1.8, stroke_opacity=0.55
        )
        ray_up = Line(
            [splitter_cx, lens_top_y + 0.05, 0],
            [splitter_cx, splitter_cy + 0.8, 0],
            stroke_color="#fbbf24", stroke_width=1.8, stroke_opacity=0.45,
        )

        self.play(LaggedStart(*[Create(r, run_time=1.2) for r in rays], lag_ratio=0.15))
        self.play(Create(ray_down, run_time=1.2))
        self.play(Create(ray_up, run_time=1.0))
        self.wait(0.5)

        lamp_lbl = Text("Sodium Lamp", font_size=15, color="#fde68a")
        lamp_lbl.next_to(lamp_group, DOWN, buff=0.25)
        self.play(FadeIn(lamp_lbl, run_time=1.5))
        self.wait(2.0)

        scope_cx = 0.0
        scope_top_y = 3.8

        scope_barrel = Rectangle(
            width=0.5, height=1.6,
            fill_color="#334155", fill_opacity=0.95,
            stroke_color="#64748b", stroke_width=2
        )
        scope_objective = Ellipse(
            width=0.6, height=0.22,
            fill_color="#1e3a5f", fill_opacity=0.9,
            stroke_color="#38bdf8", stroke_width=1.8
        )
        scope_eyepiece = Ellipse(
            width=0.42, height=0.18,
            fill_color="#1e3a5f", fill_opacity=0.9,
            stroke_color="#64748b", stroke_width=1.5
        )
        scope_arm = Rectangle(
            width=2.0, height=0.22,
            fill_color="#334155", fill_opacity=0.95,
            stroke_color="#64748b", stroke_width=1.8
        )
        scope_stand = Rectangle(
            width=0.22, height=3.2,
            fill_color="#475569", fill_opacity=0.95,
            stroke_color="#64748b", stroke_width=1.5
        )
        scope_base = Rectangle(
            width=1.5, height=0.18,
            fill_color="#334155", fill_opacity=0.95,
            stroke_color="#64748b", stroke_width=1.5
        )

        scope_barrel.move_to([scope_cx, scope_top_y - 0.8, 0])
        scope_objective.move_to([scope_cx, scope_top_y - 1.7, 0])
        scope_eyepiece.move_to([scope_cx, scope_top_y, 0])
        scope_arm.move_to([scope_cx - 1.0, scope_top_y - 0.8, 0])
        scope_stand.move_to([scope_cx - 2.0, scope_top_y - 0.8 - 1.6 + 0.1, 0])
        scope_base.move_to([scope_cx - 2.0, scope_top_y - 0.8 - 3.2 + 0.09, 0])

        scope_group = VGroup(scope_base, scope_stand, scope_arm,
                             scope_barrel, scope_objective, scope_eyepiece)
        scope_group.shift(UP * 6)

        self.play(scope_group.animate(run_time=3.0, rate_func=smooth).shift(DOWN * 6))
        self.wait(0.8)

        scope_lbl = Text("Travelling Microscope", font_size=16, color="#64748b")
        scope_lbl.move_to([scope_cx + 2.5, scope_top_y, 0])
        self.play(FadeIn(scope_lbl, run_time=1.5))
        self.wait(2.5)

        self.play(
            self.camera.frame.animate(
                run_time=3.0, rate_func=smooth
            ).scale(0.40).move_to([lens_cx, lens_cy, 0])
        )
        self.wait(1.0)

        obs_rings = VGroup()
        center_dark_obs = Dot([lens_cx, lens_cy, 0], radius=0.04,
                              color="#020617", fill_opacity=0)
        obs_rings.add(center_dark_obs)

        lam_R_obs = 0.58
        R_obs = 1.5
        for n in range(1, 10):
            r_n = np.sqrt(n * lam_R_obs * R_obs) * 0.18
            bright = (n % 2 == 1)
            inner = max(0.01, r_n - 0.020)
            outer = r_n + 0.020
            col = "#fde68a" if bright else "#020617"
            ann = Annulus(inner_radius=inner, outer_radius=outer,
                          fill_color=col, fill_opacity=0, stroke_width=0)
            ann.move_to([lens_cx, lens_cy, 0])
            obs_rings.add(ann)

        self.play(center_dark_obs.animate(run_time=0.8).set_fill(opacity=1.0))
        self.play(
            LaggedStart(
                *[r.animate(run_time=0.7).set_fill(
                    opacity=0.88 if i % 2 == 0 else 0.96
                ) for i, r in enumerate(obs_rings[1:])],
                lag_ratio=0.22
            )
        )
        self.wait(0.8)

        obs_text = Text("Interference Pattern Appears", font_size=8, color=WHITE)
        obs_text.move_to([lens_cx, lens_cy + 0.55, 0])
        self.play(FadeIn(obs_text, run_time=1.2))
        self.wait(2.5)

        self.play(
            self.camera.frame.animate(
                run_time=2.5, rate_func=smooth
            ).scale(1 / 0.40).move_to(ORIGIN)
        )
        self.wait(0.8)

        lab_group = VGroup(
            grid, title, plate_group, glass_lbl,
            lens_group, lens_lbl, contact_glow,
            air_film_glow, air_film_line, air_film_lbl, thickness_note,
            splitter, splitter_lbl,
            lamp_group, rays, ray_down, ray_up, lamp_lbl,
            scope_group, scope_lbl,
            obs_rings, obs_text
        )
        self.play(FadeOut(lab_group, run_time=2.5))
        self.wait(1.0)

        # ══════════════════════════════════════════════════════════════════════
        # PHYSICS SECTION
        # ══════════════════════════════════════════════════════════════════════

        xsec_title = Text("Cross-Section View", font_size=24, color="#94a3b8")
        xsec_title.to_edge(UP, buff=0.45)
        self.play(Write(xsec_title, run_time=1.5))
        self.wait(0.5)

        plate2 = Rectangle(
            width=9.0, height=0.4,
            fill_color="#1e3a5f", fill_opacity=0.88,
            stroke_color="#94a3b8", stroke_width=2
        )
        plate2.move_to([0, -2.0, 0])

        def lens_y(x, R=3.8):
            return -2.0 + (x ** 2) / (2 * R)

        lens_curve2 = ParametricFunction(
            lambda x: np.array([x, lens_y(x), 0]),
            t_range=[-3.5, 3.5, 0.05],
            color="#7dd3fc", stroke_width=3
        )
        lens_top2 = Line(
            [-3.5, lens_y(3.5) + 0.6, 0],
            [3.5, lens_y(3.5) + 0.6, 0],
            color="#7dd3fc", stroke_width=2.5
        )
        lens_l2 = Line([-3.5, lens_y(3.5), 0],
                       [-3.5, lens_y(3.5) + 0.6, 0],
                       color="#7dd3fc", stroke_width=2.5)
        lens_r2 = Line([3.5, lens_y(3.5), 0],
                       [3.5, lens_y(3.5) + 0.6, 0],
                       color="#7dd3fc", stroke_width=2.5)

        air_glow2 = ParametricFunction(
            lambda x: np.array([x, lens_y(x) - 0.02, 0]),
            t_range=[-3.5, 3.5, 0.05],
            color="#fde68a", stroke_width=9, stroke_opacity=0.22
        )
        air_line2 = ParametricFunction(
            lambda x: np.array([x, lens_y(x) - 0.02, 0]),
            t_range=[-3.5, 3.5, 0.05],
            color="#fde68a", stroke_width=2.2, stroke_opacity=0.85
        )

        film_lbl2 = Text("Thin Air Film (variable thickness)", font_size=15,
                         color="#fde68a")
        film_lbl2.move_to([0, 2.5, 0])
        thickness_eq = MathTex(r"t = \frac{r^2}{2R}", font_size=30,
                               color="#fbbf24")
        thickness_eq.move_to([-3.5, 1.2, 0])

        self.play(FadeIn(plate2, run_time=1.5))
        self.wait(0.3)
        self.play(Create(lens_curve2, run_time=2.0),
                  Create(lens_top2, run_time=1.5),
                  Create(lens_l2, run_time=1.5),
                  Create(lens_r2, run_time=1.5))
        self.wait(0.5)
        self.play(Create(air_glow2, run_time=1.8),
                  Create(air_line2, run_time=1.8))
        self.wait(0.5)
        self.play(Write(film_lbl2, run_time=1.5),
                  Write(thickness_eq, run_time=1.8))

        center_dot = Dot([0, -2.0, 0], color="#fde68a", radius=0.1)
        center_lbl = Text("t = 0 at center", font_size=15, color="#fde68a")
        center_lbl.next_to(center_dot, DOWN, buff=0.18)
        self.play(FadeIn(center_dot, run_time=1.2),
                  Write(center_lbl, run_time=1.2))
        self.wait(2.0)
        self.play(FadeOut(center_lbl, run_time=1.0),
                  FadeOut(film_lbl2, run_time=1.0),
                  FadeOut(thickness_eq, run_time=1.0))
        self.wait(0.5)

        rx = 1.6
        ry_top = lens_y(rx) + 0.02
        inc_start = [rx, 1.8, 0]
        hit_lens = [rx, ry_top, 0]
        hit_plate = [rx, -2.0, 0]

        inc_glow = Arrow(inc_start, hit_lens, color="#fde68a", stroke_width=14,
                         buff=0, max_tip_length_to_length_ratio=0.07,
                         tip_length=0.2, stroke_opacity=0.2)
        inc_ray = Arrow(inc_start, hit_lens, color="#fef3c7", stroke_width=3,
                        buff=0, max_tip_length_to_length_ratio=0.07, tip_length=0.2)
        inc_lbl = Text("Incident Ray", font_size=15, color="#fef3c7")
        inc_lbl.next_to(inc_ray, RIGHT, buff=0.15)

        ray1_end = [rx - 0.4, 1.8, 0]
        r1_glow = Arrow(hit_lens, ray1_end, color="#38bdf8", stroke_width=12,
                        buff=0, max_tip_length_to_length_ratio=0.08,
                        tip_length=0.18, stroke_opacity=0.2)
        r1_ray = Arrow(hit_lens, ray1_end, color="#7dd3fc", stroke_width=2.8,
                       buff=0, max_tip_length_to_length_ratio=0.08, tip_length=0.18)
        r1_lbl = Text("Ray 1 (lens→air)", font_size=14, color="#7dd3fc")
        r1_lbl.move_to([rx - 1.8, 2.3, 0])

        r2_down = Arrow(hit_lens, hit_plate, color="#fb923c", stroke_width=10,
                        buff=0, max_tip_length_to_length_ratio=0.08,
                        tip_length=0.18, stroke_opacity=0.2)
        r2_down2 = Arrow(hit_lens, hit_plate, color="#fdba74", stroke_width=2.5,
                         buff=0, max_tip_length_to_length_ratio=0.08, tip_length=0.18)

        ray2_up_end = [rx + 0.4, 1.8, 0]
        r2_up = Arrow(hit_plate, ray2_up_end, color="#fb923c", stroke_width=10,
                      buff=0, max_tip_length_to_length_ratio=0.08,
                      tip_length=0.18, stroke_opacity=0.2)
        r2_up2 = Arrow(hit_plate, ray2_up_end, color="#fdba74", stroke_width=2.5,
                       buff=0, max_tip_length_to_length_ratio=0.08, tip_length=0.18)
        r2_lbl = Text("Ray 2 (air→glass)", font_size=14, color="#fdba74")
        r2_lbl.next_to(r2_up2, RIGHT, buff=0.1)

        self.play(Create(inc_glow, run_time=1.5),
                  Create(inc_ray, run_time=1.5),
                  Write(inc_lbl, run_time=1.2))
        self.wait(0.8)
        self.play(Create(r1_glow, run_time=1.5),
                  Create(r1_ray, run_time=1.5),
                  Write(r1_lbl, run_time=1.2))
        self.wait(0.8)
        self.play(Create(r2_down, run_time=1.2),
                  Create(r2_down2, run_time=1.2))
        self.wait(0.5)
        self.play(Create(r2_up, run_time=1.5),
                  Create(r2_up2, run_time=1.5),
                  Write(r2_lbl, run_time=1.2))
        self.wait(2.0)

        self.play(FadeOut(inc_lbl, run_time=0.8),
                  FadeOut(r1_lbl, run_time=0.8),
                  FadeOut(r2_lbl, run_time=0.8))

        phase_title = Text("Phase Change on Reflection", font_size=22,
                           color=WHITE, weight=BOLD)
        phase_title.set_color_by_gradient("#38bdf8", "#fbbf24")
        phase_title.to_edge(UP, buff=0.45)
        self.play(ReplacementTransform(xsec_title, phase_title, run_time=1.2))
        self.wait(0.5)

        dot_lens = Dot(hit_lens, color="#fbbf24", radius=0.11)
        circ_lens = Circle(radius=0.26, color="#fbbf24", stroke_width=2)
        circ_lens.move_to(hit_lens)
        lbl_phase1 = Text("Air→Glass: Phase shift = λ/2", font_size=15,
                          color="#f87171", weight=BOLD)
        lbl_phase1.move_to([-2.5, ry_top + 0.4, 0])

        dot_plate = Dot(hit_plate, color="#4ade80", radius=0.11)
        circ_plate = Circle(radius=0.26, color="#4ade80", stroke_width=2)
        circ_plate.move_to(hit_plate)
        lbl_phase2 = Text("Glass→Air: No phase shift", font_size=15,
                          color="#4ade80", weight=BOLD)
        lbl_phase2.move_to([2.8, -2.45, 0])

        eff_pd = MathTex(r"\text{Eff. Path Diff.} = 2t + \frac{\lambda}{2}",
                         font_size=26, color="#e2e8f0")
        eff_pd_box = SurroundingRectangle(eff_pd, color="#1e3a5f",
                                          fill_color="#0f172a", fill_opacity=0.9,
                                          buff=0.2, corner_radius=0.14)
        eff_pd.move_to([-3.5, -0.5, 0])
        eff_pd_box.move_to([-3.5, -0.5, 0])

        self.play(FadeIn(dot_lens, run_time=1.0),
                  Create(circ_lens, run_time=1.2),
                  Write(lbl_phase1, run_time=1.5))
        self.wait(1.5)
        self.play(FadeIn(dot_plate, run_time=1.0),
                  Create(circ_plate, run_time=1.2),
                  Write(lbl_phase2, run_time=1.5))
        self.wait(1.5)
        self.play(FadeIn(eff_pd_box, run_time=1.2),
                  Write(eff_pd, run_time=2.0))
        self.wait(2.5)

        self.play(
            FadeOut(lbl_phase1), FadeOut(lbl_phase2),
            FadeOut(eff_pd_box), FadeOut(eff_pd),
            FadeOut(dot_lens), FadeOut(circ_lens),
            FadeOut(dot_plate), FadeOut(circ_plate),
            FadeOut(inc_glow), FadeOut(inc_ray),
            FadeOut(r1_glow), FadeOut(r1_ray),
            FadeOut(r2_down), FadeOut(r2_down2),
            FadeOut(r2_up), FadeOut(r2_up2),
            FadeOut(phase_title),
            run_time=1.2
        )
        self.wait(0.5)

        zoom_circle = Circle(radius=0.55, color="#fbbf24",
                             stroke_width=2, stroke_opacity=0.7)
        zoom_circle.move_to([0, -2.0, 0])
        self.play(Create(zoom_circle, run_time=1.5))
        self.wait(0.5)

        center_dark = Dot([0, -2.0, 0], color="#020617",
                          radius=0.22, fill_opacity=1.0)
        center_dark_ring = Circle(radius=0.22, color="#333333", stroke_width=2)
        center_dark_ring.move_to([0, -2.0, 0])

        dark_title = Text("Central Dark Spot", font_size=24,
                          color="#f87171", weight=BOLD)
        dark_title.to_edge(UP, buff=0.45)
        dark_reason = Text("t = 0  but  Phase shift = λ/2  →  Destructive",
                           font_size=18, color="#fca5a5")
        dark_reason.next_to(dark_title, DOWN, buff=0.2)

        self.play(FadeIn(center_dark, run_time=1.5),
                  Create(center_dark_ring, run_time=1.5),
                  Write(dark_title, run_time=1.5))
        self.wait(0.5)
        self.play(Write(dark_reason, run_time=2.0))
        self.wait(2.5)

        self.play(
            FadeOut(center_dark), FadeOut(center_dark_ring),
            FadeOut(zoom_circle), FadeOut(dark_title), FadeOut(dark_reason),
            FadeOut(lens_curve2), FadeOut(lens_top2),
            FadeOut(lens_l2), FadeOut(lens_r2),
            FadeOut(air_glow2), FadeOut(air_line2),
            FadeOut(plate2), FadeOut(center_dot),
            run_time=1.5
        )
        self.wait(0.5)

        ring_title = Text("Newton's Rings (Top View)", font_size=26,
                          color=WHITE, weight=BOLD)
        ring_title.set_color_by_gradient("#fde68a", "#fbbf24")
        ring_title.to_edge(UP, buff=0.45)
        self.play(Write(ring_title, run_time=1.5))
        self.wait(0.5)

        rings_center = [0, -0.3, 0]
        rings_group = VGroup()

        center_spot = Dot(rings_center, color="#111827",
                          radius=0.18, fill_opacity=1.0)
        rings_group.add(center_spot)

        ring_labels = VGroup()
        lam_R = 0.58
        R_val = 1.5
        ring_radii = []

        for n in range(1, 9):
            r_n = np.sqrt(n * lam_R * R_val) * 0.72
            ring_radii.append(r_n)
            bright = (n % 2 == 1)
            if bright:
                thickness = 0.16
                col = "#fde68a"
                op = 0.88
            else:
                thickness = 0.18
                col = "#111827"
                op = 0.95

            inner_r = max(0.01, r_n - thickness / 2)
            outer_r = r_n + thickness / 2
            ann = Annulus(inner_radius=inner_r, outer_radius=outer_r,
                          fill_color=col, fill_opacity=op, stroke_width=0)
            ann.move_to(rings_center)
            rings_group.add(ann)

            if n <= 5:
                lbl_n = Text(f"n={n}", font_size=12, color="#94a3b8")
                lbl_n.move_to([rings_center[0] + r_n + 0.22,
                               rings_center[1], 0])
                ring_labels.add(lbl_n)

        glow_outer = Circle(radius=ring_radii[-1] + 0.3,
                            color="#fbbf24", stroke_width=20, stroke_opacity=0.06)
        glow_outer.move_to(rings_center)
        rings_group.add(glow_outer)

        self.play(
            LaggedStart(*[FadeIn(r, run_time=0.9) for r in rings_group],
                        lag_ratio=0.10),
            run_time=3.5
        )
        self.wait(0.5)
        self.play(
            LaggedStart(*[Write(l, run_time=0.8) for l in ring_labels],
                        lag_ratio=0.15),
            run_time=2.0
        )
        self.wait(2.5)

        self.play(FadeOut(ring_title, run_time=0.8))
        math_title = Text("Mathematical Relations", font_size=24,
                          color=WHITE, weight=BOLD)
        math_title.set_color_by_gradient("#38bdf8", "#4ade80")
        math_title.to_edge(UP, buff=0.45)
        self.play(Write(math_title, run_time=1.5))
        self.wait(0.5)

        eq1 = MathTex(r"t = \frac{r^2}{2R}", font_size=30, color="#fbbf24")
        eq2 = MathTex(r"r_n^2 = n\lambda R", font_size=30, color="#4ade80")
        eq3 = MathTex(r"D_n^2 = 4n\lambda R", font_size=30, color="#7dd3fc")
        eq_group = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.35)
        eq_group.move_to([-4.0, 0.0, 0])

        eq_boxes = VGroup(*[
            SurroundingRectangle(e, color="#1e3a5f", fill_color="#0f172a",
                                 fill_opacity=0.85, buff=0.18, corner_radius=0.12)
            for e in eq_group
        ])

        self.play(FadeIn(eq_boxes[0], run_time=1.0), Write(eq1, run_time=2.0))
        self.wait(1.5)
        self.play(FadeIn(eq_boxes[1], run_time=1.0), Write(eq2, run_time=2.0))
        self.wait(1.5)
        self.play(FadeIn(eq_boxes[2], run_time=1.0), Write(eq3, run_time=2.0))
        self.wait(2.5)

        self.play(
            FadeOut(math_title), FadeOut(eq_group), FadeOut(eq_boxes),
            FadeOut(ring_labels), FadeOut(rings_group),
            run_time=1.2
        )
        self.wait(0.5)

        # ══════════════════════════════════════════════════════════════════════
        # MEASUREMENT WITH TRAVELLING MICROSCOPE
        # ══════════════════════════════════════════════════════════════════════

        meas_title = Text("Measurement with Travelling Microscope", font_size=22,
                          color=WHITE, weight=BOLD)
        meas_title.set_color_by_gradient("#fde68a", "#94a3b8")
        meas_title.to_edge(UP, buff=0.45)
        self.play(Write(meas_title, run_time=1.5))
        self.wait(0.5)

        rings_group2 = VGroup()
        c2 = [-3.2, -0.3, 0]
        spot2 = Dot(c2, color="#111827", radius=0.15, fill_opacity=1.0)
        rings_group2.add(spot2)
        for n in range(1, 8):
            r_n = np.sqrt(n * lam_R * R_val) * 0.60
            bright = (n % 2 == 1)
            col = "#fde68a" if bright else "#111827"
            op = 0.85 if bright else 0.95
            inner_r = max(0.01, r_n - 0.08)
            outer_r = r_n + 0.08
            ann = Annulus(inner_radius=inner_r, outer_radius=outer_r,
                          fill_color=col, fill_opacity=op, stroke_width=0)
            ann.move_to(c2)
            rings_group2.add(ann)

        self.play(FadeIn(rings_group2, run_time=1.5))
        self.wait(0.5)

        cv = Line([c2[0], c2[1] + 2.2, 0], [c2[0], c2[1] - 2.2, 0],
                  color="#4ade80", stroke_width=1.5, stroke_opacity=0.8)
        ch = Line([c2[0] - 2.5, c2[1], 0], [c2[0] + 2.5, c2[1], 0],
                  color="#4ade80", stroke_width=1.5, stroke_opacity=0.8)
        crosshair = VGroup(cv, ch)
        self.play(FadeIn(crosshair), run_time=0.8)

        # FIX: RoundedRectangle instead of Rectangle with corner_radius
        panel_bg = RoundedRectangle(
            width=5.6, height=6.5,
            corner_radius=0.15,
            fill_color="#0f172a", fill_opacity=0.92,
            stroke_color="#1e3a5f", stroke_width=1.8
        )
        panel_bg.move_to([3.6, -0.3, 0])
        self.play(FadeIn(panel_bg), run_time=0.6)

        panel_title = Text("Live Readings", font_size=18, color="#7dd3fc", weight=BOLD)
        panel_title.move_to([3.6, 2.85, 0])
        self.play(Write(panel_title), run_time=0.5)

        col_x_panel = [1.55, 2.85, 4.25, 5.6]
        headers = ["Ring (n)", "TL (mm)", "TR (mm)"]
        col_colors_panel = ["#fde68a", "#f87171", "#38bdf8"]
        for cx, hdr, col in zip(col_x_panel[:3], headers, col_colors_panel):
            h = Text(hdr, font_size=13, color=col, weight=BOLD)
            h.move_to([cx, 2.45, 0])
            self.add(h)

        hdr_line = Line([1.22, 2.25, 0], [5.95, 2.25, 0],
                        color="#334155", stroke_width=1.5)
        self.add(hdr_line)

        measure_rings = [1, 3, 5]
        scale_mm = 7.2
        center_mm = 13.850

        collected_data = []
        row_y_start = 1.92
        row_spacing = 0.72

        for idx, n in enumerate(measure_rings):
            r_n_vis = np.sqrt(n * lam_R * R_val) * 0.60
            r_mm = r_n_vis * scale_mm

            tl_mm = center_mm - r_mm
            tr_mm = center_mm + r_mm
            D_mm = tr_mm - tl_mm
            D2_mm2 = D_mm ** 2
            collected_data.append((n, tl_mm, tr_mm, D_mm, D2_mm2))

            left_x = c2[0] - r_n_vis
            right_x = c2[0] + r_n_vis
            row_y = row_y_start - idx * row_spacing

            ring_flash = Text(f"Measuring Ring n = {n}", font_size=14,
                              color="#fbbf24")
            ring_flash.move_to([c2[0], c2[1] + 2.5, 0])
            self.play(Write(ring_flash), run_time=0.5)

            self.play(
                crosshair.animate.move_to([left_x, c2[1], 0]),
                run_time=1.2, rate_func=smooth
            )
            left_dot = Dot([left_x, c2[1], 0], color="#f87171", radius=0.10)
            self.play(FadeIn(left_dot), run_time=0.3)
            self.wait(0.2)

            self.play(
                crosshair.animate.move_to([right_x, c2[1], 0]),
                run_time=1.4, rate_func=smooth
            )
            right_dot = Dot([right_x, c2[1], 0], color="#38bdf8", radius=0.10)
            self.play(FadeIn(right_dot), run_time=0.3)
            self.wait(0.2)

            diam_dash = DashedLine(
                [left_x, c2[1], 0], [right_x, c2[1], 0],
                color="#fbbf24", stroke_width=1.8, dash_length=0.1
            )
            self.play(Create(diam_dash), run_time=0.5)

            self.play(
                crosshair.animate.move_to(c2),
                run_time=0.6, rate_func=smooth
            )

            n_txt = Text(str(n), font_size=14, color="#fde68a")
            n_txt.move_to([col_x_panel[0], row_y, 0])
            tl_txt = Text(f"{tl_mm:.3f}", font_size=14, color="#f87171")
            tl_txt.move_to([col_x_panel[1], row_y, 0])
            tr_txt = Text(f"{tr_mm:.3f}", font_size=14, color="#38bdf8")
            tr_txt.move_to([col_x_panel[2], row_y, 0])

            row_grp = VGroup(n_txt, tl_txt, tr_txt)

            if idx < len(measure_rings) - 1:
                row_sep = Line(
                    [1.22, row_y - row_spacing / 2, 0],
                    [5.95, row_y - row_spacing / 2, 0],
                    color="#1e3a5f", stroke_width=0.8, stroke_opacity=0.7
                )
                self.add(row_sep)

            self.play(
                FadeIn(row_grp, shift=RIGHT * 0.2),
                FadeOut(ring_flash),
                run_time=0.6
            )
            self.wait(0.4)

            self.play(
                FadeOut(left_dot), FadeOut(right_dot), FadeOut(diam_dash),
                run_time=0.4
            )

        self.wait(1.5)

        self.play(
            FadeOut(crosshair), FadeOut(rings_group2),
            FadeOut(meas_title), FadeOut(panel_bg), FadeOut(panel_title),
            run_time=1.2
        )
        self.wait(0.5)

        # ══════════════════════════════════════════════════════════════════════
        # OBSERVATION TABLE
        # ══════════════════════════════════════════════════════════════════════

        obs_table_title = Text("Observation Table", font_size=30,
                               color=WHITE, weight=BOLD)
        obs_table_title.set_color_by_gradient("#fde68a", "#7dd3fc")
        obs_table_title.to_edge(UP, buff=0.35)
        obs_underline = Line(
            obs_table_title.get_left(), obs_table_title.get_right(),
            color="#fbbf24", stroke_width=2
        ).next_to(obs_table_title, DOWN, buff=0.1)

        self.play(FadeIn(obs_table_title, shift=DOWN * 0.2), run_time=1.0)
        self.play(Create(obs_underline), run_time=0.5)

        lambda_note = Text("λ (Sodium) = 589.3 nm  |  R (Lens) = calculated below",
                           font_size=14, color="#94a3b8")
        lambda_note.next_to(obs_underline, DOWN, buff=0.15)
        self.play(FadeIn(lambda_note), run_time=0.6)

        col_w = [1.1, 2.1, 2.1, 2.0, 2.1]
        col_hdrs = ["Ring\n(n)", "TL\n(mm)", "TR\n(mm)", "D = TR−TL\n(mm)", "D²\n(mm²)"]
        col_clrs = ["#fde68a", "#f87171", "#38bdf8", "#4ade80", "#c4b5fd"]
        total_w = sum(col_w)
        table_left = -total_w / 2
        header_y = 1.8
        row_h = 0.60
        num_rows = len(collected_data)
        table_h = row_h * (num_rows + 1)

        # FIX: RoundedRectangle instead of Rectangle with corner_radius
        outer_rect = RoundedRectangle(
            width=total_w + 0.1, height=table_h + 0.05,
            corner_radius=0.1,
            fill_color="#0a0f1e", fill_opacity=0.88,
            stroke_color="#1e3a5f", stroke_width=2
        )
        outer_rect.move_to([0, header_y - table_h / 2 + row_h / 2, 0])
        self.play(FadeIn(outer_rect), run_time=0.6)

        header_bg = Rectangle(
            width=total_w + 0.1, height=row_h,
            fill_color="#1e3a5f", fill_opacity=0.95,
            stroke_width=0
        )
        header_bg.move_to([0, header_y - row_h / 2, 0])
        self.play(FadeIn(header_bg), run_time=0.4)

        col_centers = []
        x_cur = table_left
        for cw in col_w:
            col_centers.append(x_cur + cw / 2)
            x_cur += cw

        x_cur = table_left
        for cw in col_w[:-1]:
            x_cur += cw
            vl = Line([x_cur, header_y, 0],
                      [x_cur, header_y - table_h, 0],
                      color="#1e3a5f", stroke_width=1.0, stroke_opacity=0.7)
            self.add(vl)

        hdr_grp = VGroup()
        for cx, hdr, col in zip(col_centers, col_hdrs, col_clrs):
            h = Text(hdr, font_size=12, color=col, weight=BOLD, line_spacing=0.85)
            h.move_to([cx, header_y - row_h / 2, 0])
            hdr_grp.add(h)
        self.play(LaggedStart(*[Write(h) for h in hdr_grp], lag_ratio=0.1), run_time=1.0)

        hl = Line([table_left, header_y - row_h, 0],
                  [table_left + total_w, header_y - row_h, 0],
                  color="#334155", stroke_width=1.5)
        self.play(Create(hl), run_time=0.4)

        for row_idx, (n, tl, tr, D, D2) in enumerate(collected_data):
            row_y = header_y - row_h * (row_idx + 1) - row_h / 2

            if row_idx % 2 == 0:
                row_bg = Rectangle(
                    width=total_w + 0.1, height=row_h,
                    fill_color="#0f172a", fill_opacity=0.6,
                    stroke_width=0
                )
                row_bg.move_to([0, row_y, 0])
                self.add(row_bg)

            values = [str(n), f"{tl:.3f}", f"{tr:.3f}", f"{D:.3f}", f"{D2:.4f}"]
            row_group = VGroup()
            for cx, val, col in zip(col_centers, values, col_clrs):
                cell = Text(val, font_size=13, color=col)
                cell.move_to([cx, row_y, 0])
                row_group.add(cell)

            if row_idx < num_rows - 1:
                sep = Line(
                    [table_left, header_y - row_h * (row_idx + 2), 0],
                    [table_left + total_w, header_y - row_h * (row_idx + 2), 0],
                    color="#1e3a5f", stroke_width=0.8, stroke_opacity=0.6
                )
                self.add(sep)

            self.play(FadeIn(row_group, shift=RIGHT * 0.2), run_time=0.65)

        self.wait(1.2)

        calc_y = header_y - row_h * (num_rows + 1) - 0.42
        n1_data = collected_data[0]
        n3_data = collected_data[-1]

        calc_title = Text(
            f"Calculation  (using rings n={n1_data[0]} and n={n3_data[0]}):",
            font_size=15, color="#94a3b8"
        )
        calc_title.move_to([0, calc_y, 0])
        self.play(Write(calc_title), run_time=0.8)

        formula = MathTex(
            r"R = \frac{D_{n_2}^2 - D_{n_1}^2}{4(n_2 - n_1)\,\lambda}",
            font_size=26, color="#e2e8f0"
        )
        formula.move_to([-2.2, calc_y - 0.62, 0])

        dn1 = n1_data[3]
        dn3 = n3_data[3]
        n1v = n1_data[0]
        n3v = n3_data[0]
        lam_nm = 589.3e-6

        R_result = (dn3 ** 2 - dn1 ** 2) / (4 * (n3v - n1v) * lam_nm)

        result_txt = MathTex(
            rf"R = \frac{{{dn3**2:.4f} - {dn1**2:.4f}}}{{4 \times {n3v - n1v} \times 589.3 \times 10^{{-6}}}}",
            font_size=18, color="#fbbf24"
        )
        result_txt.move_to([2.5, calc_y - 0.55, 0])

        # FIX: SurroundingRectangle corner_radius is fine (it's its own class)
        result_box = SurroundingRectangle(
            result_txt, color="#1e3a5f", fill_color="#0f172a",
            fill_opacity=0.88, buff=0.14, corner_radius=0.1
        )

        r_final = Text(f"R  ≈  {R_result:.2f}  mm", font_size=20,
                       color="#4ade80", weight=BOLD)
        r_final.move_to([2.5, calc_y - 1.18, 0])
        r_final_box = SurroundingRectangle(
            r_final, color="#14532d", fill_color="#052e16",
            fill_opacity=0.88, buff=0.16, corner_radius=0.1
        )

        self.play(Write(formula), run_time=1.2)
        self.play(FadeIn(result_box), Write(result_txt), run_time=1.2)
        self.play(FadeIn(r_final_box), Write(r_final), run_time=1.0)
        self.wait(2.5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=2.0)
        self.wait(0.5)

        # ══════════════════════════════════════════════════════════════════════
        # D² vs n GRAPH
        # ══════════════════════════════════════════════════════════════════════

        graph_title = Text("D² vs n Graph", font_size=24, color=WHITE, weight=BOLD)
        graph_title.set_color_by_gradient("#4ade80", "#38bdf8")
        graph_title.to_edge(UP, buff=0.45)
        self.play(Write(graph_title, run_time=1.5))
        self.wait(0.5)

        axes = Axes(
            x_range=[0, 7, 1], y_range=[0, 7, 1],
            x_length=6.5, y_length=4.5,
            axis_config={"color": "#475569", "stroke_width": 2},
            tips=False
        )
        axes.move_to([0.3, -0.5, 0])
        x_lbl = Text("Ring number (n)", font_size=16, color="#94a3b8")
        x_lbl.next_to(axes, DOWN, buff=0.3)
        y_lbl = Text("D² (mm²)", font_size=16, color="#94a3b8")
        y_lbl.next_to(axes, LEFT, buff=0.3).rotate(PI / 2)

        self.play(Create(axes, run_time=2.0),
                  Write(x_lbl, run_time=1.2),
                  Write(y_lbl, run_time=1.2))
        self.wait(0.8)

        plot_dots = VGroup()
        for n in range(1, 7):
            r_n = np.sqrt(n * lam_R * R_val) * 0.72
            D_n = 2 * r_n
            D2 = D_n ** 2
            dot = Dot(axes.c2p(n, D2 * 1.05), color="#fde68a", radius=0.1)
            plot_dots.add(dot)

        slope_line = axes.plot(lambda x: x * 1.02, x_range=[0, 6.5],
                               color="#4ade80", stroke_width=3)
        slope_lbl = Text("Slope = 4λR", font_size=16, color="#4ade80")
        slope_lbl.move_to(axes.c2p(5.5, 5.5) + [-0.3, 0.3, 0])

        self.play(
            LaggedStart(*[FadeIn(d, run_time=0.8) for d in plot_dots], lag_ratio=0.18),
            run_time=2.5
        )
        self.wait(0.8)
        self.play(Create(slope_line, run_time=2.0), Write(slope_lbl, run_time=1.5))
        self.wait(2.5)

        self.play(
            FadeOut(axes), FadeOut(plot_dots), FadeOut(slope_line),
            FadeOut(slope_lbl), FadeOut(x_lbl), FadeOut(y_lbl),
            FadeOut(graph_title),
            run_time=1.2
        )
        self.wait(0.5)

        # ══════════════════════════════════════════════════════════════════════
        # FINAL FORMULA
        # ══════════════════════════════════════════════════════════════════════

        formula_title = Text("Radius of Curvature", font_size=28,
                             color=WHITE, weight=BOLD)
        formula_title.set_color_by_gradient("#fde68a", "#4ade80")
        formula_title.to_edge(UP, buff=0.45)
        self.play(Write(formula_title, run_time=1.5))
        self.wait(0.5)

        final_eq = MathTex(
            r"R = \frac{D_m^2 - D_n^2}{4(m - n)\lambda}",
            font_size=52, color="#e2e8f0"
        )
        final_box = SurroundingRectangle(final_eq, color="#1e3a5f",
                                          fill_color="#0f172a", fill_opacity=0.92,
                                          buff=0.35, corner_radius=0.2)
        final_eq.move_to([0, -0.2, 0])
        final_box.move_to([0, -0.2, 0])

        r_note = Text("R = Radius of Curvature of the lens",
                      font_size=18, color="#94a3b8")
        r_note.move_to([0, -2.0, 0])

        self.play(FadeIn(final_box, run_time=1.5), Write(final_eq, run_time=3.0))
        self.wait(1.0)
        self.play(Write(r_note, run_time=1.5))
        self.wait(3.0)

        self.play(FadeOut(final_box), FadeOut(final_eq), FadeOut(r_note),
                  FadeOut(formula_title), run_time=1.2)
        self.wait(0.5)

        # ══════════════════════════════════════════════════════════════════════
        # MONO vs WHITE LIGHT
        # ══════════════════════════════════════════════════════════════════════

        comp_title = Text("Monochromatic vs White Light", font_size=24,
                          color=WHITE, weight=BOLD)
        comp_title.set_color_by_gradient("#fde68a", "#f87171")
        comp_title.to_edge(UP, buff=0.45)
        self.play(Write(comp_title, run_time=1.5))
        self.wait(0.5)

        divider = Line([0, 3.2, 0], [0, -3.2, 0],
                       color="#334155", stroke_width=1.2, stroke_opacity=0.6)
        self.play(Create(divider, run_time=1.0))

        mono_lbl = Text("Monochromatic (Sodium)", font_size=17,
                        color="#fde68a", weight=BOLD)
        mono_lbl.move_to([-3.5, 2.2, 0])
        white_lbl = Text("White Light", font_size=17, color=WHITE, weight=BOLD)
        white_lbl.move_to([3.5, 2.2, 0])

        mono_rings = VGroup()
        mc = [-3.5, -0.2, 0]
        for n in range(1, 7):
            r_n = np.sqrt(n * lam_R * R_val) * 0.52
            bright = (n % 2 == 1)
            col = "#fde68a" if bright else "#0a0f1e"
            ann = Annulus(inner_radius=max(0.01, r_n - 0.07),
                          outer_radius=r_n + 0.07,
                          fill_color=col, fill_opacity=0.9, stroke_width=0)
            ann.move_to(mc)
            mono_rings.add(ann)

        mono_note = Text("Sharp, clear rings", font_size=15, color="#fbbf24")
        mono_note.move_to([-3.5, -2.1, 0])

        white_rings = VGroup()
        wc = [3.5, -0.2, 0]
        wcols = ["#f87171", "#fb923c", "#fde68a", "#4ade80", "#38bdf8", "#818cf8"]
        for n in range(1, 7):
            r_n = np.sqrt(n * lam_R * R_val) * 0.52
            col = wcols[(n - 1) % len(wcols)]
            ann = Annulus(inner_radius=max(0.01, r_n - 0.13),
                          outer_radius=r_n + 0.13,
                          fill_color=col, fill_opacity=0.65, stroke_width=0)
            ann.move_to(wc)
            white_rings.add(ann)

        white_note = Text("Colored, overlapping rings", font_size=15,
                          color="#94a3b8")
        white_note.move_to([3.5, -2.1, 0])

        self.play(Write(mono_lbl, run_time=1.2), Write(white_lbl, run_time=1.2))
        self.wait(0.5)
        self.play(
            LaggedStart(*[FadeIn(r, run_time=0.8) for r in mono_rings], lag_ratio=0.10),
            LaggedStart(*[FadeIn(r, run_time=0.8) for r in white_rings], lag_ratio=0.10),
            run_time=2.5
        )
        self.wait(0.5)
        self.play(Write(mono_note, run_time=1.2), Write(white_note, run_time=1.2))
        self.wait(2.5)

        self.play(
            FadeOut(comp_title), FadeOut(divider),
            FadeOut(mono_lbl), FadeOut(white_lbl),
            FadeOut(mono_rings), FadeOut(white_rings),
            FadeOut(mono_note), FadeOut(white_note),
            run_time=1.2
        )
        self.wait(0.5)

        # ══════════════════════════════════════════════════════════════════════
        # SUMMARY PIPELINE
        # ══════════════════════════════════════════════════════════════════════

        steps = [
            ("Air Film", "#fde68a"),
            ("Path Diff", "#fb923c"),
            ("Phase Shift", "#f87171"),
            ("Interference", "#4ade80"),
            ("Rings", "#7dd3fc"),
            ("Measurement", "#818cf8"),
        ]
        sum_title = Text("Newton's Rings: Summary", font_size=26,
                         color=WHITE, weight=BOLD)
        sum_title.set_color_by_gradient("#fde68a", "#818cf8")
        sum_title.to_edge(UP, buff=0.45)
        self.play(Write(sum_title, run_time=1.5))
        self.wait(0.5)

        pipeline = VGroup()
        arrows_pl = VGroup()
        total_w2 = 12.0
        step_w = total_w2 / len(steps)
        start_x = -total_w2 / 2 + step_w / 2

        for i, (name, col) in enumerate(steps):
            xpos = start_x + i * step_w
            box = RoundedRectangle(width=step_w * 0.80, height=0.72,
                                   corner_radius=0.16, fill_color=col,
                                   fill_opacity=0.18, stroke_color=col,
                                   stroke_width=1.8)
            box.move_to([xpos, -0.2, 0])
            lbl = Text(name, font_size=16, color=col, weight=BOLD)
            lbl.move_to([xpos, -0.2, 0])
            pipeline.add(box, lbl)
            if i < len(steps) - 1:
                arr = Arrow(
                    [xpos + step_w * 0.42, -0.2, 0],
                    [xpos + step_w * 0.58, -0.2, 0],
                    color="#475569", buff=0, stroke_width=1.8,
                    max_tip_length_to_length_ratio=0.5, tip_length=0.16
                )
                arrows_pl.add(arr)

        self.play(
            LaggedStart(*[FadeIn(p, run_time=0.9) for p in pipeline], lag_ratio=0.12),
            run_time=2.5
        )
        self.wait(0.5)
        self.play(
            LaggedStart(*[Create(a, run_time=0.8) for a in arrows_pl], lag_ratio=0.15),
            run_time=2.0
        )
        self.wait(2.5)

        all_final = VGroup(pipeline, arrows_pl, sum_title)
        self.play(all_final.animate(run_time=1.5, rate_func=smooth).scale(1.08))
        self.wait(0.5)
        self.play(FadeOut(all_final, run_time=2.5))
        self.wait(0.5)