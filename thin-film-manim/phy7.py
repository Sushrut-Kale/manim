from manim import *
import numpy as np


def interference_color(thickness, wavelengths=None, mu=1.45):
    if wavelengths is None:
        wavelengths = [
            (380, [0.18, 0.00, 0.40]),
            (420, [0.40, 0.00, 0.80]),
            (450, [0.10, 0.20, 1.00]),
            (490, [0.00, 0.70, 1.00]),
            (530, [0.00, 1.00, 0.30]),
            (570, [0.80, 1.00, 0.00]),
            (600, [1.00, 0.60, 0.00]),
            (640, [1.00, 0.10, 0.00]),
            (700, [0.60, 0.00, 0.00]),
        ]
    r_sum, g_sum, b_sum, w_sum = 0.0, 0.0, 0.0, 0.0
    for wl_nm, (wr, wg, wb) in wavelengths:
        lam = wl_nm * 1e-9
        phase = 2.0 * mu * thickness / lam
        intensity = np.cos(np.pi * phase) ** 2
        r_sum += intensity * wr
        g_sum += intensity * wg
        b_sum += intensity * wb
        w_sum += intensity
    if w_sum < 1e-9:
        return ManimColor([0.0, 0.0, 0.0])
    scale = max(r_sum, g_sum, b_sum, w_sum * 0.1)
    if scale < 1e-9:
        return ManimColor([0.0, 0.0, 0.0])
    r = min(r_sum / scale, 1.0)
    g = min(g_sum / scale, 1.0)
    b = min(b_sum / scale, 1.0)
    return ManimColor([r, g, b])


def thickness_at(x, y, t_offset=0.0, base=120e-9, scale=300e-9):
    r = np.sqrt(x**2 + y**2)
    ripple = (
        0.5 * np.sin(r * 2.2 - t_offset * 0.8)
        + 0.3 * np.cos(x * 1.5 + t_offset * 0.5)
        + 0.2 * np.sin(y * 1.8 - t_offset * 0.6)
    )
    norm = (ripple + 1.0) / 2.0
    return base + norm * scale


class OilFilmScene(Scene):
    def construct(self):
        self.camera.background_color = "#020617"
        self.part0_title()
        self.part1_intro()
        self.part2_thickness_map()
        self.part3_light_interaction()
        self.part4_wavelength_separation()
        self.part5_color_formation()
        self.part6_dynamic_motion()
        self.part7_closeup()
        self.part8_physics()
        self.part9_cinematic()
        self.part10_transition()

    # ─────────────────────────────────────────────
    def part0_title(self):
        """Title screen shown before part1."""

        bg = Rectangle(width=16, height=9,
                       color=ManimColor([0.01, 0.03, 0.10]),
                       fill_opacity=1.0, stroke_width=0)
        self.add(bg)

        # Decorative rainbow shimmer bar
        n_segs = 90
        bar_w = 9.0
        seg_w = bar_w / n_segs
        shimmer = VGroup()
        for i in range(n_segs):
            frac = i / (n_segs - 1)
            t = 120e-9 + frac * 380e-9
            col = interference_color(t)
            seg = Rectangle(width=seg_w * 1.02, height=0.18,
                            fill_color=col, fill_opacity=0.85, stroke_width=0)
            seg.move_to([-bar_w / 2 + i * seg_w + seg_w / 2, -0.62, 0])
            shimmer.add(seg)

        shimmer2 = shimmer.copy().move_to([0, 0.62, 0])

        main_title = Text(
            "Oil Film Interference",
            font="Liberation Sans", font_size=68,
            color=ManimColor([1.0, 0.92, 0.45]),
            weight=BOLD,
        )
        main_title.move_to([0, 1.55, 0])

        subtitle = Text(
            "The Physics of Thin-Film Colors",
            font="Liberation Sans", font_size=28,
            color=ManimColor([0.72, 0.85, 1.0]),
            slant=ITALIC,
        )
        subtitle.move_to([0, 0.72, 0])

        byline = Text(
            "Constructive & Destructive Interference",
            font="Liberation Sans", font_size=19,
            color=ManimColor([0.50, 0.65, 0.85]),
        )
        byline.move_to([0, -1.10, 0])

        # Animate title in
        self.play(FadeIn(main_title, shift=DOWN * 0.2), run_time=1.0)
        self.play(FadeIn(subtitle, shift=UP * 0.12), run_time=0.7)
        self.play(
            LaggedStart(
                FadeIn(shimmer,  lag_ratio=0.02),
                FadeIn(shimmer2, lag_ratio=0.02),
                lag_ratio=0.3,
            ),
            run_time=1.2,
        )
        self.play(FadeIn(byline, shift=UP * 0.08), run_time=0.6)
        self.wait(2.5)
        self.play(
            FadeOut(VGroup(bg, main_title, subtitle, shimmer, shimmer2, byline)),
            run_time=1.0,
        )

    # ─────────────────────────────────────────────
    def _make_text(self, txt, size=20, color="#CCDDFF", italic=False):
        slant = ITALIC if italic else NORMAL
        return Text(txt, font="Liberation Sans", font_size=size,
                    color=color, slant=slant)

    def _make_caption(self, txt, size=21, text_color="#FFFFFF",
                      bg_color="#020617", border_color="#4488CC",
                      padding_w=0.55, padding_h=0.28, border_width=2.0,
                      italic=False):
        slant = ITALIC if italic else NORMAL
        label = Text(txt, font="Liberation Sans", font_size=size,
                     color=text_color, slant=slant, weight=BOLD)
        bg = RoundedRectangle(
            width=label.width + padding_w * 2,
            height=label.height + padding_h * 2,
            corner_radius=0.18,
            fill_color=bg_color,
            fill_opacity=0.92,
            stroke_color=border_color,
            stroke_width=border_width,
        )
        bg.move_to(label.get_center())
        return VGroup(bg, label)

    # ─────────────────────────────────────────────
    def part1_intro(self):
        """0–6s  calm water, oil drop falls, spreads."""

        water_lines = VGroup()
        for i in range(14):
            y = -3.2 + i * 0.5
            amp = 0.05 + 0.03 * np.sin(i * 1.1)
            pts = [[x, y + amp * np.sin(x * 3.0 + i * 0.7), 0]
                   for x in np.linspace(-7.5, 7.5, 120)]
            line = VMobject(color=ManimColor([0.15, 0.35, 0.55]),
                            stroke_width=1.2, stroke_opacity=0.55)
            line.set_points_smoothly(pts)
            water_lines.add(line)

        water_bg = Rectangle(width=16, height=9,
                             color=ManimColor([0.01, 0.07, 0.18]),
                             fill_opacity=0.6, stroke_width=0)
        self.add(water_bg)
        self.play(FadeIn(water_lines, lag_ratio=0.06), run_time=1.5)

        drop = Ellipse(width=0.18, height=0.26,
                       color=ManimColor([0.85, 0.78, 0.30]),
                       fill_opacity=0.85, stroke_width=1.5,
                       stroke_color=ManimColor([1.0, 0.95, 0.5]))
        drop.move_to([0, 3.2, 0])
        self.play(FadeIn(drop), run_time=0.3)
        self.play(drop.animate.move_to([0, -0.15, 0]),
                  rate_func=rate_functions.ease_in_cubic, run_time=1.1)

        ripples = VGroup()
        for r_scale in [0.5, 1.0, 1.7, 2.6]:
            rip = Ellipse(width=r_scale * 0.8, height=r_scale * 0.28,
                          color=ManimColor([0.5, 0.75, 1.0]),
                          fill_opacity=0, stroke_width=1.5,
                          stroke_opacity=0.6)
            rip.move_to([0, -0.15, 0])
            ripples.add(rip)

        self.play(
            FadeOut(drop, scale=0.3),
            LaggedStart(*[
                Succession(
                    FadeIn(r, scale=0.1),
                    r.animate.scale(3.5).set_stroke(opacity=0)
                )
                for r in ripples
            ], lag_ratio=0.25),
            run_time=1.4
        )

        film = Ellipse(width=0.3, height=0.12,
                       color=ManimColor([0.9, 0.7, 0.2]),
                       fill_opacity=0.35, stroke_width=0)
        film.move_to([0, -0.15, 0])
        self.add(film)

        self.play(
            film.animate.become(
                Ellipse(width=8.0, height=3.0,
                        color=ManimColor([0.7, 0.55, 0.15]),
                        fill_opacity=0.22, stroke_width=0)
                .move_to([0, -0.15, 0])
            ),
            run_time=1.8,
            rate_func=rate_functions.ease_out_cubic
        )

        caption = self._make_caption(
            "A thin oil film forms on water",
            size=22, text_color="#E8F4FF",
            bg_color="#020C1E", border_color="#5599DD",
            border_width=2.2
        )
        caption.to_edge(DOWN, buff=0.42)
        self.play(FadeIn(caption, shift=UP * 0.12), run_time=0.7)
        self.wait(1.5)
        self.play(FadeOut(VGroup(water_lines, water_bg, film, caption, *ripples)),
                  run_time=0.9)

    # ─────────────────────────────────────────────
    def part2_thickness_map(self):
        """6–15s  top-view thickness map."""

        cols, rows = 60, 36
        dx, dy = 14.0 / cols, 8.0 / rows
        grid = VGroup()

        thin_col  = np.array([0.15, 0.35, 1.0])
        mid_col   = np.array([0.1, 0.9, 0.35])
        thick_col = np.array([1.0, 0.2, 0.1])

        for j in range(rows):
            for i in range(cols):
                x = -7.0 + i * dx + dx / 2
                y = -4.0 + j * dy + dy / 2
                t = thickness_at(x * 0.55, y * 0.55)
                n = np.clip((t - 120e-9) / 300e-9, 0, 1)
                if n < 0.5:
                    col = thin_col * (1 - n * 2) + mid_col * (n * 2)
                else:
                    col = mid_col * (1 - (n - 0.5) * 2) + thick_col * ((n - 0.5) * 2)
                sq = Square(side_length=max(dx, dy) * 1.05,
                            color=ManimColor(list(col * 0.7)),
                            fill_opacity=0.88, stroke_width=0)
                sq.move_to([x, y, 0])
                grid.add(sq)

        self.play(FadeIn(grid, lag_ratio=0.001), run_time=2.0)

        legend_items = [("Thin", thin_col), ("Medium", mid_col), ("Thick", thick_col)]
        legend = VGroup()
        for k, (label, col) in enumerate(legend_items):
            dot = Circle(radius=0.13,
                         color=ManimColor(list(col * 0.85)),
                         fill_opacity=1.0, stroke_width=0)
            lbl_bg = RoundedRectangle(width=1.6, height=0.38, corner_radius=0.1,
                                      fill_color="#020C1E", fill_opacity=0.88,
                                      stroke_color=ManimColor(list(np.clip(col, 0, 1))),
                                      stroke_width=1.2)
            txt = Text(label, font="Liberation Sans", font_size=15, weight=BOLD,
                       color=ManimColor(list(np.clip(col * 1.1, 0, 1))))
            lbl_bg.move_to([5.0, 1.2 - k * 0.55, 0])
            txt.move_to(lbl_bg.get_center())
            dot.move_to([4.1, 1.2 - k * 0.55, 0])
            legend.add(dot, lbl_bg, txt)

        title = self._make_caption(
            "Film thickness varies continuously",
            size=20, text_color="#E8F4FF",
            bg_color="#020C1E", border_color="#4477BB",
            border_width=2.0
        )
        title.to_edge(DOWN, buff=0.42)

        self.play(FadeIn(legend), FadeIn(title), run_time=0.8)
        self.wait(5.0)
        self.play(FadeOut(VGroup(grid, legend, title)), run_time=1.0)

    # ─────────────────────────────────────────────
    def part3_light_interaction(self):
        """15–25s  white light hits film, two reflections shown."""

        top_surf = Line([-5.5, 0.7, 0], [5.5, 0.7, 0],
                        color=ManimColor([0.85, 0.72, 0.2]), stroke_width=2.2)
        bot_surf = Line([-5.5, -0.4, 0], [5.5, -0.4, 0],
                        color=ManimColor([0.25, 0.55, 0.85]), stroke_width=2.2)
        film_fill = Rectangle(width=11, height=1.1,
                              color=ManimColor([0.65, 0.52, 0.12]),
                              fill_opacity=0.18, stroke_width=0)
        film_fill.move_to([0, 0.15, 0])

        top_lbl = Text("Air / Oil surface", font="Liberation Sans",
                       font_size=14, color=ManimColor([0.9, 0.82, 0.5]))
        top_lbl.move_to([4.0, 1.05, 0])
        bot_lbl = Text("Oil / Water surface", font="Liberation Sans",
                       font_size=14, color=ManimColor([0.5, 0.75, 1.0]))
        bot_lbl.move_to([4.0, -0.75, 0])

        self.play(Create(film_fill), Create(top_surf), Create(bot_surf),
                  FadeIn(top_lbl), FadeIn(bot_lbl), run_time=1.0)

        inc = Arrow([-3.8, 3.2, 0], [-1.0, 0.7, 0],
                    color=WHITE, stroke_width=2.8, buff=0,
                    max_tip_length_to_length_ratio=0.08)
        self.play(GrowArrow(inc), run_time=0.7)

        r1 = Arrow([-1.0, 0.7, 0], [-3.8, -1.2, 0],
                   color=ManimColor([1.0, 0.92, 0.3]),
                   stroke_width=2.5, buff=0, max_tip_length_to_length_ratio=0.08)
        r1_lbl_bg = RoundedRectangle(width=1.9, height=0.42, corner_radius=0.1,
                                      fill_color="#020C1E", fill_opacity=0.9,
                                      stroke_color=ManimColor([1.0, 0.88, 0.2]),
                                      stroke_width=1.5)
        r1_lbl_bg.move_to([-3.5, 1.5, 0])
        r1_lbl = Text("Ray 1", font="Liberation Sans", font_size=16,
                      color=ManimColor([1.0, 0.92, 0.3]), weight=BOLD)
        r1_lbl.move_to(r1_lbl_bg.get_center())

        r2_down = Arrow([-1.0, 0.7, 0], [-0.4, -0.4, 0],
                        color=ManimColor([0.4, 0.7, 1.0]),
                        stroke_width=2.3, buff=0, max_tip_length_to_length_ratio=0.1)
        r2_up   = Arrow([-0.4, -0.4, 0], [0.2, 0.7, 0],
                        color=ManimColor([0.4, 0.7, 1.0]),
                        stroke_width=2.3, buff=0, max_tip_length_to_length_ratio=0.1)
        r2_exit = Arrow([0.2, 0.7, 0], [-2.2, 3.2, 0],
                        color=ManimColor([0.4, 0.7, 1.0]),
                        stroke_width=2.3, buff=0, max_tip_length_to_length_ratio=0.08)
        r2_lbl_bg = RoundedRectangle(width=1.9, height=0.42, corner_radius=0.1,
                                      fill_color="#020C1E", fill_opacity=0.9,
                                      stroke_color=ManimColor([0.3, 0.65, 1.0]),
                                      stroke_width=1.5)
        r2_lbl_bg.move_to([-1.8, 2.8, 0])
        r2_lbl = Text("Ray 2", font="Liberation Sans", font_size=16,
                      color=ManimColor([0.4, 0.7, 1.0]), weight=BOLD)
        r2_lbl.move_to(r2_lbl_bg.get_center())

        self.play(GrowArrow(r1), FadeIn(r1_lbl_bg), FadeIn(r1_lbl), run_time=0.6)
        self.play(GrowArrow(r2_down), run_time=0.4)
        self.play(GrowArrow(r2_up), run_time=0.4)
        self.play(GrowArrow(r2_exit), FadeIn(r2_lbl_bg), FadeIn(r2_lbl), run_time=0.5)

        path_note_bg = RoundedRectangle(width=3.5, height=0.88, corner_radius=0.14,
                                         fill_color="#020C1E", fill_opacity=0.94,
                                         stroke_color="#557799", stroke_width=1.5)
        path_note_bg.move_to([2.8, 0.15, 0])
        path_note = Text("Extra path = 2μt", font="Liberation Sans",
                         font_size=17, color=ManimColor([1.0, 0.82, 0.4]), weight=BOLD)
        path_note.move_to(path_note_bg.get_center())

        section = self._make_caption(
            "Light reflects from both surfaces",
            size=20, text_color="#E8F4FF",
            bg_color="#020C1E", border_color="#4477BB",
            border_width=2.0
        )
        section.to_edge(DOWN, buff=0.42)

        self.play(FadeIn(path_note_bg), FadeIn(path_note), run_time=0.6)
        self.play(FadeIn(section), run_time=0.5)
        self.wait(3.5)
        self.play(FadeOut(VGroup(
            top_surf, bot_surf, film_fill, top_lbl, bot_lbl,
            inc, r1, r1_lbl_bg, r1_lbl,
            r2_down, r2_up, r2_exit, r2_lbl_bg, r2_lbl,
            path_note_bg, path_note, section
        )), run_time=0.9)

    # ─────────────────────────────────────────────
    def part4_wavelength_separation(self):
        """25–40s  which thickness selects which wavelength."""

        caption = self._make_caption(
            "Different thickness selects different wavelengths",
            size=20, text_color="#E8F4FF",
            bg_color="#020C1E", border_color="#4477BB",
            border_width=2.0
        )
        caption.to_edge(DOWN, buff=0.42)
        self.play(FadeIn(caption), run_time=0.6)

        bar_w = 9.0
        bar = Rectangle(width=bar_w, height=0.55,
                        fill_color=BLACK, fill_opacity=0,
                        stroke_color="#334455", stroke_width=1.5)
        bar.move_to([0, 0.5, 0])

        n_segs = 80
        seg_w = bar_w / n_segs
        grad_group = VGroup()
        for i in range(n_segs):
            frac = i / (n_segs - 1)
            t = 120e-9 + frac * 300e-9
            col = interference_color(t)
            seg = Rectangle(width=seg_w * 1.02, height=0.55,
                            fill_color=col, fill_opacity=0.9, stroke_width=0)
            seg.move_to([-bar_w / 2 + i * seg_w + seg_w / 2, 0.5, 0])
            grad_group.add(seg)

        thin_lbl = Text("Thin", font="Liberation Sans", font_size=15, weight=BOLD,
                        color=ManimColor([0.6, 0.7, 1.0]))
        thin_lbl.move_to([-4.5, -0.1, 0])
        thick_lbl = Text("Thick", font="Liberation Sans", font_size=15, weight=BOLD,
                         color=ManimColor([1.0, 0.4, 0.2]))
        thick_lbl.move_to([4.5, -0.1, 0])
        t_axis_arrow = Arrow([-4.0, -0.15, 0], [4.0, -0.15, 0],
                              color="#445566", stroke_width=1.8, buff=0,
                              max_tip_length_to_length_ratio=0.05)
        t_axis_lbl = Text("Increasing thickness →", font="Liberation Sans",
                          font_size=14, color="#6688AA")
        t_axis_lbl.move_to([0, -0.55, 0])

        self.play(FadeIn(grad_group, lag_ratio=0.005),
                  Create(bar), run_time=1.5)
        self.play(FadeIn(thin_lbl), FadeIn(thick_lbl),
                  GrowArrow(t_axis_arrow), FadeIn(t_axis_lbl), run_time=0.7)

        regions = [
            (-3.2, "Blue\nconstructive",  ManimColor([0.3, 0.5, 1.0])),
            ( 0.0, "Green\nconstructive", ManimColor([0.2, 1.0, 0.4])),
            ( 3.2, "Red\nconstructive",   ManimColor([1.0, 0.3, 0.15])),
        ]
        ann_group = VGroup()
        for xp, txt, col in regions:
            marker = Line([xp, 0.22, 0], [xp, 1.5, 0],
                          color=col, stroke_width=1.6, stroke_opacity=0.8)
            dot = Dot([xp, 0.22, 0], radius=0.07, color=col)
            lbl_bg = RoundedRectangle(width=1.85, height=0.78, corner_radius=0.12,
                                       fill_color="#020C1E", fill_opacity=0.92,
                                       stroke_color=col, stroke_width=1.5)
            lbl_bg.move_to([xp, 2.1, 0])
            lbl = Text(txt, font="Liberation Sans", font_size=14, weight=BOLD,
                       color=col, line_spacing=0.9)
            lbl.move_to(lbl_bg.get_center())
            ann_group.add(marker, dot, lbl_bg, lbl)

        self.play(LaggedStart(*[FadeIn(el) for el in ann_group], lag_ratio=0.18),
                  run_time=1.8)
        self.wait(5.0)
        self.play(FadeOut(VGroup(grad_group, bar, thin_lbl, thick_lbl,
                                  t_axis_arrow, t_axis_lbl, ann_group, caption)),
                  run_time=1.0)

    # ─────────────────────────────────────────────
    def part5_color_formation(self):
        """40–55s  full interference color map over film shape."""

        cols, rows = 70, 42
        dx, dy = 13.0 / cols, 8.2 / rows
        film_grid = VGroup()

        for j in range(rows):
            for i in range(cols):
                x = -6.5 + i * dx + dx / 2
                y = -4.1 + j * dy + dy / 2
                if (x / 6.2) ** 2 + (y / 3.6) ** 2 > 1.0:
                    continue
                t = thickness_at(x * 0.6, y * 0.6, t_offset=0.0)
                col = interference_color(t)
                sq = Square(side_length=max(dx, dy) * 1.08,
                            fill_color=col, fill_opacity=0.92, stroke_width=0)
                sq.move_to([x, y, 0])
                film_grid.add(sq)

        glow = Ellipse(width=12.6, height=7.4,
                       color=ManimColor([0.7, 0.6, 0.2]),
                       fill_opacity=0, stroke_width=6, stroke_opacity=0.18)

        caption = self._make_caption(
            "Interference colors emerge across the film",
            size=21, text_color="#FFFFFF",
            bg_color="#010810", border_color="#55AAFF",
            border_width=2.5, padding_w=0.65, padding_h=0.32
        )
        caption.to_edge(DOWN, buff=0.42)

        self.play(FadeIn(film_grid, lag_ratio=0.0005), run_time=3.0)
        self.play(FadeIn(glow), run_time=0.6)
        self.play(FadeIn(caption, shift=UP * 0.12), run_time=0.7)
        self.wait(7.0)
        self.play(FadeOut(VGroup(film_grid, glow, caption)), run_time=1.2)

    # ─────────────────────────────────────────────
    def part6_dynamic_motion(self):
        """55–70s  ValueTracker animates shifting colors."""

        t_tracker = ValueTracker(0.0)
        cols, rows = 55, 34
        dx, dy = 13.0 / cols, 8.2 / rows

        def make_pixel(i, j):
            x = -6.5 + i * dx + dx / 2
            y = -4.1 + j * dy + dy / 2
            if (x / 6.2) ** 2 + (y / 3.6) ** 2 > 1.0:
                return None
            sq = Square(side_length=max(dx, dy) * 1.1,
                        fill_opacity=0.9, stroke_width=0)
            sq.move_to([x, y, 0])

            def updater(mob, xi=x, yi=y):
                tv = t_tracker.get_value()
                t = thickness_at(xi * 0.6, yi * 0.6, t_offset=tv)
                col = interference_color(t)
                mob.set_fill(col, opacity=0.9)

            sq.add_updater(updater)
            return sq

        pixels = VGroup()
        for j in range(rows):
            for i in range(cols):
                px = make_pixel(i, j)
                if px is not None:
                    pixels.add(px)

        caption = self._make_caption(
            "Changing thickness  →  changing colors",
            size=21, text_color="#FFFFFF",
            bg_color="#010810", border_color="#55AAFF",
            border_width=2.5, padding_w=0.65, padding_h=0.32
        )
        caption.to_edge(DOWN, buff=0.42)

        self.add(pixels)
        self.play(FadeIn(pixels, lag_ratio=0), run_time=0.5)
        self.play(FadeIn(caption, shift=UP * 0.1), run_time=0.6)

        self.play(t_tracker.animate.set_value(8.0),
                  run_time=12.0, rate_func=linear)

        for sq in pixels:
            sq.clear_updaters()
        self.play(FadeOut(VGroup(pixels, caption)), run_time=1.0)

    # ─────────────────────────────────────────────
    def part7_closeup(self):
        """70–80s  zoom into small region, micro ripples."""

        zoom_cols, zoom_rows = 50, 50
        patch_w, patch_h = 6.0, 6.0
        dx = patch_w / zoom_cols
        dy = patch_h / zoom_rows

        t_tracker = ValueTracker(0.0)
        pixels = VGroup()

        for j in range(zoom_rows):
            for i in range(zoom_cols):
                x = -patch_w / 2 + i * dx + dx / 2
                y = -patch_h / 2 + j * dy + dy / 2
                sq = Square(side_length=max(dx, dy) * 1.05,
                            fill_opacity=0.95, stroke_width=0)
                sq.move_to([x, y, 0])

                def updater(mob, xi=x, yi=y):
                    tv = t_tracker.get_value()
                    t = thickness_at(xi * 2.5, yi * 2.5, t_offset=tv,
                                     base=180e-9, scale=180e-9)
                    col = interference_color(t)
                    mob.set_fill(col, opacity=0.95)

                sq.add_updater(updater)
                pixels.add(sq)

        zoom_ring = Circle(radius=3.1, color=WHITE,
                           fill_opacity=0, stroke_width=1.5, stroke_opacity=0.35)

        zoom_lbl_bg = RoundedRectangle(width=1.6, height=0.42, corner_radius=0.1,
                                        fill_color="#010810", fill_opacity=0.92,
                                        stroke_color="#445566", stroke_width=1.5)
        zoom_lbl_bg.to_corner(UR, buff=0.35)
        zoom_lbl = Text("×8 zoom", font="Liberation Sans", font_size=14,
                        weight=BOLD, color=ManimColor([0.75, 0.85, 1.0]))
        zoom_lbl.move_to(zoom_lbl_bg.get_center())

        caption = self._make_caption(
            "Tiny thickness changes  →  rapid color shift",
            size=21, text_color="#FFFFFF",
            bg_color="#010810", border_color="#55AAFF",
            border_width=2.5, padding_w=0.65, padding_h=0.32
        )
        caption.to_edge(DOWN, buff=0.42)

        self.play(FadeIn(pixels, lag_ratio=0), FadeIn(zoom_ring),
                  FadeIn(zoom_lbl_bg), FadeIn(zoom_lbl),
                  FadeIn(caption), run_time=0.6)

        self.play(t_tracker.animate.set_value(6.0),
                  run_time=8.5, rate_func=linear)

        for sq in pixels:
            sq.clear_updaters()
        self.play(FadeOut(VGroup(pixels, zoom_ring, zoom_lbl_bg, zoom_lbl, caption)),
                  run_time=0.9)

    # ─────────────────────────────────────────────
    def part8_physics(self):
        """80–90s  formula overlay."""

        t_tracker = ValueTracker(0.0)
        cols, rows = 45, 28
        dx, dy = 14.0 / cols, 8.0 / rows
        bg_pixels = VGroup()

        for j in range(rows):
            for i in range(cols):
                x = -7.0 + i * dx + dx / 2
                y = -4.0 + j * dy + dy / 2
                sq = Square(side_length=max(dx, dy) * 1.06,
                            fill_opacity=0.5, stroke_width=0)
                sq.move_to([x, y, 0])

                def upd(mob, xi=x, yi=y):
                    tv = t_tracker.get_value()
                    t = thickness_at(xi * 0.5, yi * 0.5, t_offset=tv)
                    mob.set_fill(interference_color(t), opacity=0.45)

                sq.add_updater(upd)
                bg_pixels.add(sq)

        self.add(bg_pixels)
        self.play(FadeIn(bg_pixels, lag_ratio=0), run_time=0.5)

        panel = Rectangle(width=7.5, height=3.2,
                          fill_color="#020617", fill_opacity=0.85,
                          stroke_color=ManimColor([0.3, 0.45, 0.65]),
                          stroke_width=1.8)
        panel.move_to(ORIGIN)

        eq = MathTex(r"2\mu t = n\lambda", font_size=72,
                     color=ManimColor([0.95, 0.95, 1.0]))
        eq.move_to([0, 0.5, 0])

        sub_items = [
            (r"\mu", "refractive index of oil"),
            (r"t",   "film thickness"),
            (r"\lambda", "wavelength of light"),
            (r"n",   "interference order"),
        ]
        legend = VGroup()
        for k, (sym, desc) in enumerate(sub_items):
            s = MathTex(sym, font_size=22, color=ManimColor([0.8, 0.9, 1.0]))
            d = Text(desc, font="Liberation Sans", font_size=15,
                     color=ManimColor([0.7, 0.85, 1.0]))
            d.next_to(s, RIGHT, buff=0.2)
            item = VGroup(s, d)
            item.move_to([-1.2 + (k % 2) * 2.8, -0.55 - (k // 2) * 0.48, 0])
            legend.add(item)

        caption = self._make_caption(
            "Interference depends on thickness",
            size=20, text_color="#FFFFFF",
            bg_color="#010810", border_color="#55AAFF",
            border_width=2.5, padding_w=0.6, padding_h=0.3
        )
        caption.to_edge(DOWN, buff=0.42)

        self.play(FadeIn(panel), run_time=0.5)
        self.play(Write(eq), run_time=1.2)
        self.play(FadeIn(legend, lag_ratio=0.2), run_time=1.0)
        self.play(FadeIn(caption), run_time=0.5)

        self.play(t_tracker.animate.set_value(4.0),
                  run_time=6.0, rate_func=linear)

        for sq in bg_pixels:
            sq.clear_updaters()
        self.play(FadeOut(VGroup(bg_pixels, panel, eq, legend, caption)),
                  run_time=1.0)

    # ─────────────────────────────────────────────
    def part9_cinematic(self):
        """90–100s  full-screen flowing colors, no text."""

        t_tracker = ValueTracker(0.0)
        cols, rows = 65, 40
        dx, dy = 14.5 / cols, 9.0 / rows
        pixels = VGroup()

        for j in range(rows):
            for i in range(cols):
                x = -7.25 + i * dx + dx / 2
                y = -4.5 + j * dy + dy / 2
                sq = Square(side_length=max(dx, dy) * 1.04,
                            fill_opacity=1.0, stroke_width=0)
                sq.move_to([x, y, 0])

                def upd(mob, xi=x, yi=y):
                    tv = t_tracker.get_value()
                    t = thickness_at(xi * 0.45, yi * 0.45, t_offset=tv,
                                     base=100e-9, scale=380e-9)
                    col = interference_color(t)
                    mob.set_fill(col, opacity=1.0)

                sq.add_updater(upd)
                pixels.add(sq)

        self.add(pixels)
        self.play(FadeIn(pixels, lag_ratio=0), run_time=0.8)
        self.play(t_tracker.animate.set_value(10.0),
                  run_time=9.5, rate_func=linear)

        for sq in pixels:
            sq.clear_updaters()

        self.pixel_group_for_transition = pixels
        self.t_tracker_final = t_tracker

    # ─────────────────────────────────────────────
    def part10_transition(self):
        """100–110s  fade to wave, then summary flow chart."""

        pixels = self.pixel_group_for_transition
        self.play(pixels.animate.set_fill(opacity=0.0), run_time=2.0)
        self.remove(pixels)

        wave_lines = VGroup()
        for i in range(8):
            y_base = -1.75 + i * 0.5
            amplitude = 0.12 + 0.04 * np.sin(i * 0.9)
            pts = [[x, y_base + amplitude * np.sin(x * 2.8 + i * 0.5), 0]
                   for x in np.linspace(-7.5, 7.5, 150)]
            col_alpha = 0.15 + 0.35 * (1 - abs(i - 3.5) / 4.5)
            line = VMobject(
                color=ManimColor([0.25, 0.55, 0.85]),
                stroke_width=1.5,
                stroke_opacity=col_alpha
            )
            line.set_points_smoothly(pts)
            wave_lines.add(line)

        self.play(FadeIn(wave_lines, lag_ratio=0.12), run_time=1.8)
        self.wait(0.8)
        self.play(FadeOut(wave_lines), run_time=1.0)

        self._summary_flow()

    # ─────────────────────────────────────────────
    def _summary_flow(self):
        title = Text(
            "Oil Film Interference: Summary",
            font="Liberation Sans", font_size=36,
            color=ManimColor([1.0, 0.92, 0.45]),
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.55)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.8)

        steps = [
            ("Oil Film\nForms",
             ManimColor([0.18, 0.14, 0.04]),
             ManimColor([0.85, 0.68, 0.10]),
             ManimColor([1.00, 0.82, 0.25])),

            ("Thickness\nVaries",
             ManimColor([0.18, 0.10, 0.04]),
             ManimColor([0.90, 0.45, 0.10]),
             ManimColor([1.00, 0.58, 0.20])),

            ("Path\nDifference",
             ManimColor([0.18, 0.05, 0.05]),
             ManimColor([0.85, 0.22, 0.22]),
             ManimColor([1.00, 0.45, 0.45])),

            ("Wavelength\nSelection",
             ManimColor([0.04, 0.16, 0.10]),
             ManimColor([0.15, 0.80, 0.42]),
             ManimColor([0.30, 1.00, 0.60])),

            ("Constructive\nInterference",
             ManimColor([0.04, 0.12, 0.20]),
             ManimColor([0.18, 0.58, 0.90]),
             ManimColor([0.45, 0.78, 1.00])),

            ("Rainbow\nColors",
             ManimColor([0.08, 0.08, 0.22]),
             ManimColor([0.50, 0.45, 1.00]),
             ManimColor([0.72, 0.68, 1.00])),
        ]

        n = len(steps)
        box_w, box_h = 1.85, 1.22
        gap = 0.52
        total_w = n * box_w + (n - 1) * gap
        x_start = -total_w / 2 + box_w / 2
        y_center = -0.55

        boxes      = []
        arrow_list = []

        for k, (label, fill_col, stroke_col, text_col) in enumerate(steps):
            xp = x_start + k * (box_w + gap)

            box = RoundedRectangle(
                width=box_w, height=box_h,
                corner_radius=0.22,
                fill_color=fill_col, fill_opacity=1.0,
                stroke_color=stroke_col, stroke_width=2.8,
            )
            box.move_to([xp, y_center, 0])

            lbl = Text(
                label, font="Liberation Sans", font_size=19,
                color=text_col, weight=BOLD, line_spacing=0.88,
            )
            lbl.move_to(box.get_center())

            boxes.append(VGroup(box, lbl))

            if k > 0:
                x_prev = x_start + (k - 1) * (box_w + gap)
                arr = Arrow(
                    start=[x_prev + box_w / 2 + 0.06, y_center, 0],
                    end  =[xp    - box_w / 2 - 0.06, y_center, 0],
                    color=ManimColor([0.50, 0.58, 0.70]),
                    stroke_width=2.2,
                    buff=0,
                    max_tip_length_to_length_ratio=0.38,
                )
                arrow_list.append(arr)

        for k in range(n):
            anims = [FadeIn(boxes[k], shift=UP * 0.18, scale=0.88)]
            if k > 0:
                anims.append(GrowArrow(arrow_list[k - 1]))
            self.play(*anims, run_time=0.55)

        for k, bg in enumerate(boxes):
            glow = RoundedRectangle(
                width=box_w + 0.28, height=box_h + 0.28,
                corner_radius=0.30,
                fill_opacity=0,
                stroke_color=steps[k][2],
                stroke_width=3.5,
                stroke_opacity=0.75,
            )
            glow.move_to(bg.get_center())
            self.play(FadeIn(glow, scale=0.9), run_time=0.22)
            self.play(glow.animate.scale(1.12).set_stroke(opacity=0), run_time=0.32)
            self.remove(glow)

        self.wait(2.5)

        all_objs = VGroup(title, *boxes, *arrow_list)
        self.play(FadeOut(all_objs), run_time=1.4)