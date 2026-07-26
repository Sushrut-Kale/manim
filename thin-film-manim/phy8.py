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
    return ManimColor([min(r_sum / scale, 1.0), min(g_sum / scale, 1.0), min(b_sum / scale, 1.0)])


def thickness_at(x, y, t_offset=0.0, base=120e-9, scale=300e-9):
    r = np.sqrt(x**2 + y**2)
    ripple = (
        0.5 * np.sin(r * 2.2 - t_offset * 0.8)
        + 0.3 * np.cos(x * 1.5 + t_offset * 0.5)
        + 0.2 * np.sin(y * 1.8 - t_offset * 0.6)
    )
    norm = (ripple + 1.0) / 2.0
    return base + norm * scale


def make_wave_line(y_base, x_min=-7.5, x_max=7.5, freq=2.0, amp=0.18,
                   phase=0.0, color=None, opacity=0.5, sw=1.4):
    if color is None:
        color = ManimColor([0.25, 0.55, 0.85])
    pts = [[x, y_base + amp * np.sin(freq * x + phase), 0]
           for x in np.linspace(x_min, x_max, 200)]
    mob = VMobject(color=color, stroke_width=sw, stroke_opacity=opacity)
    mob.set_points_smoothly(pts)
    return mob


class FinalConclusionScene(Scene):
    def construct(self):
        self.camera.background_color = "#020617"
        self.part1_silent_recall()
        self.part2_rebuild_idea()
        self.part3_thin_film()
        self.part4_applications()
        self.part5_merge()
        self.part6_concept_statement()
        self.part7_final_wave()
        self.part8_end_title()
        self.part9_credits()
        self.part10_final_fade()

    # ── helpers ────────────────────────────────────────────────────────
    def _caption(self, txt, size=26, color="#E8F4FF",
                 bg="#020C1E", border="#4488CC", bw=2.0,
                 pw=0.6, ph=0.28):
        lbl = Text(txt, font="Liberation Sans", font_size=size,
                   color=color, weight=BOLD)
        bg_rect = RoundedRectangle(
            width=lbl.width + pw * 2, height=lbl.height + ph * 2,
            corner_radius=0.18, fill_color=bg, fill_opacity=0.92,
            stroke_color=border, stroke_width=bw,
        )
        bg_rect.move_to(lbl.get_center())
        return VGroup(bg_rect, lbl)

    def _wave_group(self, n=9, y_span=(-2.0, 2.0), amp=0.14,
                    freq=2.2, phase_step=0.7, opacity=0.38,
                    color=None, sw=1.3):
        grp = VGroup()
        for i in range(n):
            y = y_span[0] + i * (y_span[1] - y_span[0]) / max(n - 1, 1)
            grp.add(make_wave_line(y, amp=amp, freq=freq,
                                   phase=i * phase_step,
                                   color=color, opacity=opacity, sw=sw))
        return grp

    # ── PART 1 — SILENT RECALL (0–8s) ─────────────────────────────────
    def part1_silent_recall(self):
        waves = self._wave_group(n=11, y_span=(-3.2, 3.2),
                                 amp=0.10, freq=1.8, opacity=0.0,
                                 color=ManimColor([0.18, 0.38, 0.62]), sw=1.2)
        self.add(waves)
        self.play(
            *[w.animate.set_stroke(opacity=0.28) for w in waves],
            run_time=3.5, rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(4.5)

        self._recall_waves = waves

    # ── PART 2 — REBUILD THE IDEA (8–18s) ────────────────────────────
    def part2_rebuild_idea(self):
        old_waves = self._recall_waves

        # Bring two clean interference waves to center
        y1, y2 = 0.55, -0.55
        w1 = make_wave_line(y1, amp=0.30, freq=2.5, phase=0.0,
                             color=ManimColor([0.35, 0.65, 1.0]), opacity=0.0, sw=2.2)
        w2 = make_wave_line(y2, amp=0.30, freq=2.5, phase=1.1,
                             color=ManimColor([0.85, 0.55, 1.0]), opacity=0.0, sw=2.2)
        self.add(w1, w2)

        self.play(
            *[w.animate.set_stroke(opacity=0.12) for w in old_waves],
            w1.animate.set_stroke(opacity=0.85),
            w2.animate.set_stroke(opacity=0.85),
            run_time=2.2, rate_func=smooth
        )

        # Resultant (sum) wave
        def resultant_pts(y_base=0.0):
            xs = np.linspace(-7.5, 7.5, 300)
            ys = [y_base + 0.30 * np.sin(2.5 * x) + 0.30 * np.sin(2.5 * x + 1.1)
                  for x in xs]
            return [[x, y, 0] for x, y in zip(xs, ys)]

        wr = VMobject(color=ManimColor([1.0, 0.88, 0.35]),
                      stroke_width=2.8, stroke_opacity=0.0)
        wr.set_points_smoothly(resultant_pts())
        self.add(wr)
        self.play(wr.animate.set_stroke(opacity=0.9), run_time=1.4, rate_func=smooth)

        # Text
        cap = self._caption("When light waves meet…", size=27,
                             color="#E8F4FF", border="#5599DD", bw=2.2)
        cap.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.8)
        self.wait(3.5)
        self.play(
            FadeOut(VGroup(old_waves, w1, w2, wr, cap)),
            run_time=1.2
        )

    # ── PART 3 — CONNECT TO THIN FILM (18–28s) ────────────────────────
    def part3_thin_film(self):
        # Film surfaces
        top = Line([-5.5, 0.8, 0], [5.5, 0.8, 0],
                   color=ManimColor([0.85, 0.72, 0.2]), stroke_width=2.2)
        bot = Line([-5.5, -0.5, 0], [5.5, -0.5, 0],
                   color=ManimColor([0.25, 0.55, 0.85]), stroke_width=2.2)
        fill = Rectangle(width=11, height=1.3,
                         fill_color=ManimColor([0.55, 0.42, 0.10]),
                         fill_opacity=0.18, stroke_width=0)
        fill.move_to([0, 0.15, 0])

        tl = Text("Air / Oil", font="Liberation Sans", font_size=13,
                  color=ManimColor([0.9, 0.82, 0.5]))
        tl.move_to([4.5, 1.12, 0])
        bl = Text("Oil / Water", font="Liberation Sans", font_size=13,
                  color=ManimColor([0.5, 0.75, 1.0]))
        bl.move_to([4.5, -0.85, 0])

        self.play(
            FadeIn(fill), Create(top), Create(bot),
            FadeIn(tl), FadeIn(bl),
            run_time=1.2
        )

        # Incident ray and two reflections
        inc = Arrow([-4.0, 3.2, 0], [-1.2, 0.8, 0],
                    color=WHITE, stroke_width=2.5, buff=0,
                    max_tip_length_to_length_ratio=0.08)
        r1 = Arrow([-1.2, 0.8, 0], [-4.0, -1.5, 0],
                   color=ManimColor([1.0, 0.92, 0.3]),
                   stroke_width=2.2, buff=0, max_tip_length_to_length_ratio=0.08)
        r2d = Arrow([-1.2, 0.8, 0], [-0.6, -0.5, 0],
                    color=ManimColor([0.4, 0.75, 1.0]),
                    stroke_width=2.0, buff=0, max_tip_length_to_length_ratio=0.1)
        r2u = Arrow([-0.6, -0.5, 0], [0.0, 0.8, 0],
                    color=ManimColor([0.4, 0.75, 1.0]),
                    stroke_width=2.0, buff=0, max_tip_length_to_length_ratio=0.1)
        r2e = Arrow([0.0, 0.8, 0], [-2.5, 3.2, 0],
                    color=ManimColor([0.4, 0.75, 1.0]),
                    stroke_width=2.0, buff=0, max_tip_length_to_length_ratio=0.08)

        self.play(GrowArrow(inc), run_time=0.6)
        self.play(GrowArrow(r1), run_time=0.5)
        self.play(GrowArrow(r2d), GrowArrow(r2u), run_time=0.5)
        self.play(GrowArrow(r2e), run_time=0.4)

        cap = self._caption("Thin films create path differences", size=24,
                             color="#E8F4FF", border="#4477BB", bw=2.0)
        cap.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.7)
        self.wait(3.5)

        self.play(FadeOut(VGroup(
            fill, top, bot, tl, bl,
            inc, r1, r2d, r2u, r2e, cap
        )), run_time=1.0)

    # ── PART 4 — APPLICATIONS (28–45s) ────────────────────────────────
    def part4_applications(self):
        cap = self._caption("The same physics… everywhere", size=26,
                             color="#FFFBE8", border="#AA8833", bw=2.2)
        cap.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(cap), run_time=0.6)

        panels = VGroup()

        # ── 1. Newton's Rings ──────────────────────────────────────────
        nr_grp = VGroup()
        for k in range(1, 9):
            r = k * 0.38
            bright = k % 2 == 1
            ring = Circle(radius=r,
                          color=ManimColor([0.9, 0.85, 0.6]) if bright
                          else ManimColor([0.08, 0.08, 0.12]),
                          fill_opacity=0.0,
                          stroke_width=2.8 if bright else 2.0,
                          stroke_opacity=0.85 if bright else 0.45)
            nr_grp.add(ring)
        center_dot = Dot(ORIGIN, radius=0.07,
                         color=ManimColor([0.08, 0.08, 0.12]))
        nr_grp.add(center_dot)
        nr_grp.move_to([-4.5, 0.5, 0])
        nr_lbl_bg = RoundedRectangle(width=2.1, height=0.42, corner_radius=0.1,
                                      fill_color="#020C1E", fill_opacity=0.9,
                                      stroke_color=ManimColor([0.85, 0.78, 0.4]),
                                      stroke_width=1.4)
        nr_lbl = Text("Newton's Rings", font="Liberation Sans",
                       font_size=14, weight=BOLD,
                       color=ManimColor([1.0, 0.9, 0.5]))
        nr_lbl_bg.move_to([-4.5, -1.05, 0])
        nr_lbl.move_to(nr_lbl_bg.get_center())
        panels.add(nr_grp, nr_lbl_bg, nr_lbl)

        # ── 2. Lens Coating ────────────────────────────────────────────
        lc_grp = VGroup()
        lens_arc_top = Arc(radius=2.2, start_angle=PI + 0.38, angle=2 * 0.38,
                           color=ManimColor([0.6, 0.7, 0.9]), stroke_width=2.2)
        lens_arc_top.move_to([0, 0.5, 0])
        coat = Arc(radius=2.26, start_angle=PI + 0.38, angle=2 * 0.38,
                   color=ManimColor([0.1, 0.85, 0.55]), stroke_width=3.5,
                   stroke_opacity=0.7)
        coat.move_to([0, 0.5, 0])
        coat_lbl_bg = RoundedRectangle(width=2.1, height=0.42, corner_radius=0.1,
                                        fill_color="#020C1E", fill_opacity=0.9,
                                        stroke_color=ManimColor([0.1, 0.8, 0.5]),
                                        stroke_width=1.4)
        coat_lbl = Text("Lens Coating", font="Liberation Sans",
                         font_size=14, weight=BOLD,
                         color=ManimColor([0.3, 1.0, 0.65]))
        coat_lbl_bg.move_to([0, -1.05, 0])
        coat_lbl.move_to(coat_lbl_bg.get_center())
        lc_grp.add(lens_arc_top, coat)
        panels.add(lc_grp, coat_lbl_bg, coat_lbl)

        # ── 3. Oil Film ────────────────────────────────────────────────
        oil_grp = VGroup()
        n_segs = 22
        seg_w = 3.6 / n_segs
        for i in range(n_segs):
            frac = i / (n_segs - 1)
            t = 120e-9 + frac * 340e-9
            col = interference_color(t)
            seg = Rectangle(width=seg_w * 1.04, height=1.1,
                            fill_color=col, fill_opacity=0.88, stroke_width=0)
            seg.move_to([4.5 - 1.8 + i * seg_w + seg_w / 2, 0.5, 0])
            oil_grp.add(seg)
        oil_border = Rectangle(width=3.6, height=1.1,
                                fill_opacity=0, stroke_color="#445566",
                                stroke_width=1.2)
        oil_border.move_to([4.5, 0.5, 0])
        oil_grp.add(oil_border)
        oil_lbl_bg = RoundedRectangle(width=1.8, height=0.42, corner_radius=0.1,
                                       fill_color="#020C1E", fill_opacity=0.9,
                                       stroke_color=ManimColor([0.6, 0.45, 1.0]),
                                       stroke_width=1.4)
        oil_lbl = Text("Oil Film", font="Liberation Sans",
                        font_size=14, weight=BOLD,
                        color=ManimColor([0.75, 0.68, 1.0]))
        oil_lbl_bg.move_to([4.5, -1.05, 0])
        oil_lbl.move_to(oil_lbl_bg.get_center())
        panels.add(oil_grp, oil_lbl_bg, oil_lbl)

        # Animate panels in with stagger
        self.play(
            LaggedStart(
                FadeIn(VGroup(nr_grp, nr_lbl_bg, nr_lbl), shift=UP * 0.15),
                FadeIn(VGroup(lc_grp, coat_lbl_bg, coat_lbl), shift=UP * 0.15),
                FadeIn(VGroup(oil_grp, oil_lbl_bg, oil_lbl), shift=UP * 0.15),
                lag_ratio=0.35
            ),
            run_time=3.0
        )
        self.wait(8.0)
        self.play(FadeOut(VGroup(panels, cap)), run_time=1.2)

    # ── PART 5 — MERGE VISUALS (45–55s) ───────────────────────────────
    def part5_merge(self):
        # Build interference color ellipse (oil-film style) as merged visual
        cols, rows = 55, 34
        dx, dy = 11.0 / cols, 6.5 / rows
        merged = VGroup()
        for j in range(rows):
            for i in range(cols):
                x = -5.5 + i * dx + dx / 2
                y = -3.25 + j * dy + dy / 2
                if (x / 5.2) ** 2 + (y / 2.9) ** 2 > 1.0:
                    continue
                t = thickness_at(x * 0.55, y * 0.55)
                col = interference_color(t)
                sq = Square(side_length=max(dx, dy) * 1.06,
                            fill_color=col, fill_opacity=0.0, stroke_width=0)
                sq.move_to([x, y, 0])
                merged.add(sq)

        self.add(merged)
        self.play(
            *[sq.animate.set_fill(opacity=0.88) for sq in merged],
            run_time=3.5, rate_func=smooth
        )

        # Underlying wave lines
        waves = self._wave_group(n=13, y_span=(-3.8, 3.8),
                                  amp=0.10, freq=1.6, opacity=0.0,
                                  color=ManimColor([0.9, 0.9, 1.0]), sw=1.1)
        self.add(waves)
        self.play(
            *[w.animate.set_stroke(opacity=0.22) for w in waves],
            run_time=2.2, rate_func=smooth
        )
        self.wait(3.0)
        self.play(
            *[sq.animate.set_fill(opacity=0.0) for sq in merged],
            *[w.animate.set_stroke(opacity=0.0) for w in waves],
            run_time=2.0, rate_func=smooth
        )
        self.remove(merged, waves)

    # ── PART 6 — FINAL CONCEPT STATEMENT (55–65s) ─────────────────────
    def part6_concept_statement(self):
        line1 = Text("Path difference creates phase difference",
                     font="Liberation Sans", font_size=30,
                     color=ManimColor([0.75, 0.88, 1.0]), weight=BOLD)
        line2 = Text("Phase difference creates interference",
                     font="Liberation Sans", font_size=30,
                     color=ManimColor([1.0, 0.88, 0.45]), weight=BOLD)
        line1.move_to([0, 0.65, 0])
        line2.move_to([0, -0.55, 0])

        # Subtle wave bg
        waves = self._wave_group(n=7, y_span=(-3.2, 3.2), amp=0.08,
                                  freq=1.5, opacity=0.12,
                                  color=ManimColor([0.3, 0.5, 0.8]), sw=1.0)
        self.add(waves)

        self.play(Write(line1), run_time=1.6)
        self.wait(1.0)
        self.play(Write(line2), run_time=1.6)
        self.wait(4.5)
        self.play(FadeOut(VGroup(line1, line2, waves)), run_time=1.2)

    # ── PART 7 — FINAL WAVE SYMBOLISM (65–75s) ────────────────────────
    def part7_final_wave(self):
        t_val = ValueTracker(0.0)

        # Build a field of animating waves — rainbow colored
        wave_mobs = []
        colors_list = [
            ManimColor([0.4, 0.4, 1.0]),
            ManimColor([0.2, 0.8, 1.0]),
            ManimColor([0.2, 1.0, 0.5]),
            ManimColor([1.0, 0.9, 0.2]),
            ManimColor([1.0, 0.5, 0.2]),
            ManimColor([0.9, 0.2, 0.5]),
            ManimColor([0.6, 0.2, 1.0]),
        ]
        ys = np.linspace(-2.8, 2.8, 7)
        for idx, (y, col) in enumerate(zip(ys, colors_list)):
            mob = VMobject(color=col, stroke_width=2.5,
                           stroke_opacity=0.0)
            pts = [[x, y + 0.22 * np.sin(2.2 * x + idx * 0.6), 0]
                   for x in np.linspace(-7.5, 7.5, 200)]
            mob.set_points_smoothly(pts)

            def upd(m, yi=y, ph=idx * 0.6, c=col):
                tv = t_val.get_value()
                pts2 = [[x, yi + 0.22 * np.sin(2.2 * x + ph + tv * 1.2), 0]
                         for x in np.linspace(-7.5, 7.5, 200)]
                m.set_points_smoothly(pts2)

            mob.add_updater(upd)
            wave_mobs.append(mob)
            self.add(mob)

        self.play(
            *[w.animate.set_stroke(opacity=0.75) for w in wave_mobs],
            run_time=1.8, rate_func=smooth
        )
        self.play(t_val.animate.set_value(5.0),
                  run_time=6.0, rate_func=linear)
        self.play(
            *[w.animate.set_stroke(opacity=0.0) for w in wave_mobs],
            run_time=2.5, rate_func=smooth
        )
        for w in wave_mobs:
            w.clear_updaters()
            self.remove(w)

    # ── PART 8 — END TITLE (75–85s) ───────────────────────────────────
    def part8_end_title(self):
        main = Text("Thin Film Interference",
                    font="Liberation Sans", font_size=58,
                    color=ManimColor([1.0, 0.92, 0.45]), weight=BOLD)
        sub = Text("One principle. Infinite patterns.",
                   font="Liberation Sans", font_size=26,
                   color=ManimColor([0.68, 0.82, 1.0]), slant=ITALIC)
        main.move_to([0, 0.6, 0])
        sub.move_to([0, -0.45, 0])

        # Shimmer bar beneath
        n_segs = 80
        bar_w = 8.0
        seg_w = bar_w / n_segs
        shimmer = VGroup()
        for i in range(n_segs):
            frac = i / (n_segs - 1)
            t = 120e-9 + frac * 360e-9
            col = interference_color(t)
            seg = Rectangle(width=seg_w * 1.02, height=0.14,
                            fill_color=col, fill_opacity=0.0, stroke_width=0)
            seg.move_to([-bar_w / 2 + i * seg_w + seg_w / 2, -1.12, 0])
            shimmer.add(seg)

        self.play(FadeIn(main, shift=DOWN * 0.18), run_time=1.2)
        self.play(FadeIn(sub, shift=UP * 0.10), run_time=0.9)
        self.play(
            *[s.animate.set_fill(opacity=0.82) for s in shimmer],
            run_time=1.5, rate_func=smooth
        )
        self.wait(5.5)
        self.play(FadeOut(VGroup(main, sub, shimmer)), run_time=1.4)

    # ── PART 9 — CREDITS (85–100s) ────────────────────────────────────
    def part9_credits(self):
        by_lbl = Text("By", font="Liberation Sans", font_size=22,
                      color=ManimColor([0.55, 0.68, 0.85]), slant=ITALIC)
        names = ["Sushrut Kale", "Kunal Badgujar",
                 "Shourya Thorat", "Siddharth Kumbhar"]
        name_mobs = [
            Text(n, font="Liberation Sans", font_size=32,
                 color=ManimColor([0.88, 0.94, 1.0]), weight=BOLD)
            for n in names
        ]

        guide_line1 = Text("Under the guidance of",
                            font="Liberation Sans", font_size=18,
                            color=ManimColor([0.50, 0.60, 0.75]), slant=ITALIC)
        guide_line2 = Text("Dr. Ashish Itolikar Sir",
                            font="Liberation Sans", font_size=22,
                            color=ManimColor([0.70, 0.80, 1.0]), weight=BOLD)

        # Layout: stack vertically
        total_h = 0.45 + len(names) * 0.68 + 0.7 + 0.55 + 0.62
        y_top = total_h / 2

        by_lbl.move_to([0, y_top, 0])
        y_cur = y_top - 0.52
        for nm in name_mobs:
            nm.move_to([0, y_cur, 0])
            y_cur -= 0.68
        y_cur -= 0.30
        guide_line1.move_to([0, y_cur, 0])
        y_cur -= 0.52
        guide_line2.move_to([0, y_cur, 0])

        # Fade in from black — brief dark pause
        self.wait(0.4)
        self.play(FadeIn(by_lbl, shift=DOWN * 0.08), run_time=0.9)
        for nm in name_mobs:
            self.play(FadeIn(nm, shift=DOWN * 0.08), run_time=0.55)
        self.wait(1.0)
        self.play(
            FadeIn(guide_line1, shift=UP * 0.06),
            run_time=0.7
        )
        self.play(
            FadeIn(guide_line2, shift=UP * 0.06),
            run_time=0.7
        )
        self.wait(4.5)

        all_credits = VGroup(by_lbl, *name_mobs, guide_line1, guide_line2)
        self.play(FadeOut(all_credits), run_time=1.5)

    # ── PART 10 — FINAL FADE (100–105s) ───────────────────────────────
    def part10_final_fade(self):
        # Faint callback wave
        wave = make_wave_line(0.0, amp=0.12, freq=1.8, phase=0.0,
                               color=ManimColor([0.25, 0.48, 0.75]),
                               opacity=0.0, sw=1.6)
        self.add(wave)
        self.play(wave.animate.set_stroke(opacity=0.32),
                  run_time=1.5, rate_func=smooth)
        self.wait(1.5)
        self.play(wave.animate.set_stroke(opacity=0.0),
                  run_time=2.2, rate_func=rate_functions.ease_in_out_sine)
        self.remove(wave)
        self.wait(0.8)