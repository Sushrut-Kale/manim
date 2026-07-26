from manim import *
import numpy as np


class ThinFilmOverview(Scene):
    def construct(self):
        self.camera.background_color = "#020617"

        # ── PART 1: TRANSITION FROM THIN FILM (0–4s) ─────────────────────────
        film_top_y = 0.5
        film_bot_y = -0.5
        top_surf = Line([-5.5, film_top_y, 0], [5.5, film_top_y, 0],
                        color="#e2e8f0", stroke_width=2.5)
        bot_surf = Line([-5.5, film_bot_y, 0], [5.5, film_bot_y, 0],
                        color="#94a3b8", stroke_width=2.5)
        film_fill = Polygon(
            [-5.5, film_top_y, 0], [5.5, film_top_y, 0],
            [5.5, film_bot_y, 0], [-5.5, film_bot_y, 0],
            fill_color="#0ea5e9", fill_opacity=0.18, stroke_width=0
        )

        inc_ray = Arrow([-4.0, film_top_y + 1.8, 0], [-1.0, film_top_y, 0],
                        color="#fef3c7", stroke_width=3.5, buff=0,
                        max_tip_length_to_length_ratio=0.07, tip_length=0.22)
        ref_ray = Arrow([-1.0, film_top_y, 0], [1.8, film_top_y + 1.8, 0],
                        color="#7dd3fc", stroke_width=3.5, buff=0,
                        max_tip_length_to_length_ratio=0.07, tip_length=0.22)

        film_group = VGroup(film_fill, top_surf, bot_surf, inc_ray, ref_ray)

        self.play(FadeIn(film_group), run_time=0.8)

        principle_text = Text("This same principle appears in many forms",
                              font_size=28, color=WHITE)
        principle_text.set_color_by_gradient("#38bdf8", "#818cf8")
        principle_text.to_edge(UP, buff=0.5)
        self.play(Write(principle_text), run_time=1.2)
        self.wait(0.5)

        glow_layer = Rectangle(width=11.0, height=1.2,
                               fill_color="#0ea5e9", fill_opacity=0.22,
                               stroke_color="#38bdf8", stroke_width=1.5,
                               stroke_opacity=0.5)
        glow_layer.move_to([0, 0, 0])

        self.play(
            ReplacementTransform(film_group, glow_layer),
            run_time=1.2
        )
        self.play(FadeOut(principle_text), FadeOut(glow_layer), run_time=0.8)

        # ── PART 2: SPLIT INTO THREE PANELS (4–8s) ────────────────────────────
        panel_w = 4.1
        panel_h = 5.2
        panel_y = -0.3
        gap = 0.18

        left_box = RoundedRectangle(width=panel_w, height=panel_h,
                             fill_color="#0f172a", fill_opacity=0.92,
                             stroke_color="#1e3a5f", stroke_width=1.8,
                             corner_radius=0.22)
        left_box.move_to([-4.3, panel_y, 0])

        center_box = RoundedRectangle(width=panel_w, height=panel_h,
                               fill_color="#0f172a", fill_opacity=0.92,
                               stroke_color="#1e3a5f", stroke_width=1.8,
                               corner_radius=0.22)
        center_box.move_to([0, panel_y, 0])

        right_box = RoundedRectangle(width=panel_w, height=panel_h,
                              fill_color="#0f172a", fill_opacity=0.92,
                              stroke_color="#1e3a5f", stroke_width=1.8,
                              corner_radius=0.22)
        right_box.move_to([4.3, panel_y, 0])

        left_title = Text("Air Film", font_size=20, color="#fde68a", weight=BOLD)
        left_sub_title = Text("(Newton's Rings)", font_size=15, color="#fbbf24")
        left_header = VGroup(left_title, left_sub_title).arrange(DOWN, buff=0.1)
        left_header.move_to([-4.3, panel_y + panel_h / 2 - 0.42, 0])

        center_title = Text("Lens Coating", font_size=20, color="#7dd3fc", weight=BOLD)
        center_sub_title = Text("(Anti-Reflection)", font_size=15, color="#38bdf8")
        center_header = VGroup(center_title, center_sub_title).arrange(DOWN, buff=0.1)
        center_header.move_to([0, panel_y + panel_h / 2 - 0.42, 0])

        right_title = Text("Oil Film", font_size=20, color="#c4b5fd", weight=BOLD)
        right_sub_title = Text("(Iridescence)", font_size=15, color="#a78bfa")
        right_header = VGroup(right_title, right_sub_title).arrange(DOWN, buff=0.1)
        right_header.move_to([4.3, panel_y + panel_h / 2 - 0.42, 0])

        self.play(
            FadeIn(left_box), FadeIn(center_box), FadeIn(right_box),
            run_time=0.9
        )
        self.play(
            Write(left_header), Write(center_header), Write(right_header),
            run_time=1.0
        )
        self.wait(0.5)

        # ── PART 3: NEWTON'S RINGS (8–14s) ────────────────────────────────────
        rings_center = [-4.3, panel_y - 0.25, 0]
        rings_group = VGroup()

        ring_colors = []
        for i in range(9):
            bright = (i % 2 == 0)
            col = "#fde68a" if bright else "#020617"
            opacity = 0.85 if bright else 0.95
            r_outer = 0.22 + i * 0.2
            r_inner = max(0.0, r_outer - 0.18)
            if i == 0:
                dot = Dot(rings_center, radius=0.12,
                          color="#fde68a", fill_opacity=0.9)
                rings_group.add(dot)
            else:
                ann = Annulus(inner_radius=r_inner, outer_radius=r_outer,
                              fill_color=col, fill_opacity=opacity,
                              stroke_width=0)
                ann.move_to(rings_center)
                rings_group.add(ann)

        glow_rings = Circle(radius=1.98, color="#fbbf24",
                            stroke_width=18, stroke_opacity=0.08)
        glow_rings.move_to(rings_center)
        rings_group.add(glow_rings)

        rings_subtitle = Text("Interference in a thin air layer",
                              font_size=13, color="#fbbf24")
        rings_subtitle.move_to([-4.3, panel_y - panel_h / 2 + 0.42, 0])

        self.play(LaggedStart(*[FadeIn(r) for r in rings_group],
                              lag_ratio=0.08), run_time=1.5)
        self.play(Write(rings_subtitle), run_time=0.7)
        self.play(rings_group.animate.scale(1.08).move_to(rings_center),
                  run_time=1.0, rate_func=smooth)
        self.play(rings_group.animate.scale(1 / 1.08).move_to(rings_center),
                  run_time=0.8, rate_func=smooth)
        self.wait(0.5)

        # ── PART 4: LENS COATING (14–20s) ─────────────────────────────────────
        lens_cx, lens_cy = 0, panel_y - 0.1

        # Lens arc
        lens_arc = Arc(radius=1.8, start_angle=PI * 0.68, angle=PI * 0.64,
                       color="#94a3b8", stroke_width=3)
        lens_arc.move_to([lens_cx, lens_cy, 0])

        lens_fill = ArcPolygon(
            *[lens_arc.point_from_proportion(t) for t in np.linspace(0, 1, 30)],
            color="#1e3a5f", fill_opacity=0.45, stroke_width=0
        )

        # Before: strong reflection lines
        refl_before = VGroup()
        for i in range(5):
            xi = lens_cx - 0.8 + i * 0.4
            yi_start = lens_cy + 0.9
            line_b = Line([xi - 0.15, yi_start + 0.5, 0],
                          [xi + 0.15, yi_start + 0.9, 0],
                          color=WHITE, stroke_width=2.5, stroke_opacity=0.9)
            refl_before.add(line_b)

        coating_layer = Arc(radius=1.82, start_angle=PI * 0.68, angle=PI * 0.64,
                            color="#818cf8", stroke_width=6, stroke_opacity=0.55)
        coating_layer.move_to([lens_cx, lens_cy, 0])

        rainbow_arcs = VGroup()
        rainbow_colors = ["#f87171", "#fb923c", "#fde68a",
                          "#4ade80", "#38bdf8", "#818cf8"]
        for idx, rc in enumerate(rainbow_colors):
            rl = Arc(radius=1.79 + idx * 0.008,
                     start_angle=PI * 0.70, angle=PI * 0.60,
                     color=rc, stroke_width=1.8, stroke_opacity=0.55)
            rl.move_to([lens_cx, lens_cy, 0])
            rainbow_arcs.add(rl)

        # After: reduced reflections
        refl_after = VGroup()
        for i in range(5):
            xi = lens_cx - 0.8 + i * 0.4
            yi_start = lens_cy + 0.9
            line_a = Line([xi - 0.08, yi_start + 0.5, 0],
                          [xi + 0.08, yi_start + 0.75, 0],
                          color=WHITE, stroke_width=1.0, stroke_opacity=0.28)
            refl_after.add(line_a)

        lens_subtitle = Text("Destructive interference reduces reflection",
                             font_size=12, color="#7dd3fc")
        lens_subtitle.move_to([0, panel_y - panel_h / 2 + 0.42, 0])

        self.play(Create(lens_arc), FadeIn(lens_fill), run_time=0.8)
        self.play(FadeIn(refl_before), run_time=0.6)
        self.wait(0.35)
        self.play(
            FadeIn(coating_layer), FadeIn(rainbow_arcs),
            ReplacementTransform(refl_before, refl_after),
            run_time=1.2
        )
        self.play(Write(lens_subtitle), run_time=0.7)
        self.wait(0.5)

        # ── PART 5: OIL FILM (20–26s) ─────────────────────────────────────────
        oil_cx, oil_cy = 4.3, panel_y - 0.25
        oil_w, oil_h = 3.5, 3.2
        oil_time = ValueTracker(0)

        # Layered gradient rectangles for oil
        oil_base = Rectangle(width=oil_w, height=oil_h,
                             fill_color="#0c1220", fill_opacity=0.95,
                             stroke_width=0)
        oil_base.move_to([oil_cx, oil_cy, 0])

        oil_colors = [
            "#f87171", "#fb923c", "#fde68a",
            "#4ade80", "#38bdf8", "#818cf8", "#c4b5fd"
        ]

        oil_strips = VGroup()
        strip_h = oil_h / len(oil_colors)
        for idx, oc in enumerate(oil_colors):
            strip = Rectangle(width=oil_w, height=strip_h,
                              fill_color=oc, fill_opacity=0.38, stroke_width=0)
            yp = oil_cy + oil_h / 2 - strip_h * (idx + 0.5)
            strip.move_to([oil_cx, yp, 0])
            oil_strips.add(strip)

        # Wavy shimmer lines
        oil_shimmer = VGroup()
        for row in range(8):
            y_row = oil_cy + oil_h / 2 - 0.2 - row * (oil_h / 8)
            col_idx = row % len(oil_colors)
            wave_line = always_redraw(
                lambda y0=y_row, ci=col_idx: ParametricFunction(
                    lambda x: np.array([
                        x,
                        y0 + 0.055 * np.sin(3.5 * (x - oil_cx) + oil_time.get_value() + ci),
                        0
                    ]),
                    t_range=[oil_cx - oil_w / 2 + 0.1, oil_cx + oil_w / 2 - 0.1, 0.05],
                    color=oil_colors[ci], stroke_width=2.8, stroke_opacity=0.65
                )
            )
            oil_shimmer.add(wave_line)

        oil_clip = Rectangle(width=oil_w, height=oil_h, stroke_width=0,
                             fill_opacity=0).move_to([oil_cx, oil_cy, 0])

        oil_subtitle = Text("Thickness variations create colors",
                            font_size=13, color="#c4b5fd")
        oil_subtitle.move_to([4.3, panel_y - panel_h / 2 + 0.42, 0])

        self.play(FadeIn(oil_base), FadeIn(oil_strips), run_time=0.8)
        self.play(FadeIn(oil_shimmer), Write(oil_subtitle), run_time=0.8)
        self.play(oil_time.animate.set_value(6.0), run_time=3.5, rate_func=linear)
        self.wait(0.3)

        # ── PART 6: CONNECT THEM (26–32s) ─────────────────────────────────────
        self.play(
            left_box.animate.set_stroke(color="#fde68a", width=2.5),
            center_box.animate.set_stroke(color="#7dd3fc", width=2.5),
            right_box.animate.set_stroke(color="#c4b5fd", width=2.5),
            run_time=0.8
        )

        same_physics = Text("Same Physics", font_size=32, color=WHITE,
                            weight=BOLD)
        same_physics.set_color_by_gradient("#fde68a", "#7dd3fc", "#c4b5fd")
        different_patterns = Text("Different Patterns", font_size=24,
                                  color="#94a3b8")
        connect_group = VGroup(same_physics, different_patterns).arrange(DOWN, buff=0.22)
        connect_group.to_edge(UP, buff=0.38)

        bg_ray = Line([-6.5, 0.2, 0], [6.5, 0.2, 0],
                      color="#fde68a", stroke_width=18, stroke_opacity=0.07)
        bg_ray2 = Line([-6.5, -0.4, 0], [6.5, -0.4, 0],
                       color="#7dd3fc", stroke_width=12, stroke_opacity=0.05)

        self.play(FadeIn(bg_ray), FadeIn(bg_ray2), run_time=0.6)
        self.play(Write(same_physics), run_time=0.8)
        self.play(Write(different_patterns), run_time=0.7)
        self.wait(1.5)

        self.play(
            FadeOut(same_physics), FadeOut(different_patterns),
            FadeOut(bg_ray), FadeOut(bg_ray2),
            run_time=0.6
        )

        # ── PART 7: TRANSITION TO NEXT SCENE (32–36s) ─────────────────────────
        next_text = Text("Let's start with air film interference",
                         font_size=26, color="#fde68a")
        next_text.set_color_by_gradient("#fde68a", "#fbbf24")
        next_text.to_edge(UP, buff=0.45)
        self.play(Write(next_text), run_time=0.8)

        # Fade center and right panels
        center_content = VGroup(lens_arc, lens_fill, coating_layer,
                                rainbow_arcs, refl_after,
                                center_header, center_box, lens_subtitle)
        right_content = VGroup(oil_base, oil_strips, oil_shimmer,
                               right_header, right_box, oil_subtitle)

        self.play(
            FadeOut(center_content),
            FadeOut(right_content),
            run_time=1.0
        )

        left_content = VGroup(rings_group, left_header, left_box, rings_subtitle)
        self.play(
            left_content.animate.scale(1.25).move_to([0, -0.1, 0]),
            run_time=1.5, rate_func=smooth
        )
        self.wait(0.5)

        all_remaining = VGroup(left_content, next_text)
        self.play(FadeOut(all_remaining), run_time=1.8)
        self.wait(0.3)