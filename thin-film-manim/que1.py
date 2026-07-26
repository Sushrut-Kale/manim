from manim import *
import numpy as np


class ThinFilmQuestion(Scene):
    def construct(self):

        BG       = "#0D0D1A"
        ACCENT   = "#00D4FF"
        GOLD     = "#FFD700"
        OPT_BG   = "#1A1A2E"
        WHITE    = "#FFFFFF"
        SUBTEXT  = "#B0B8CC"
        OK_COL   = "#00FF88"
        WARN_COL = "#FF6B35"
        PURPLE   = "#C084FC"

        self.camera.background_color = BG
        TOTAL = 60
        N_PTS = 200   # fixed point count for arc — never changes

        # ── Top bar ──────────────────────────────────────────────────────
        top_bar = Rectangle(width=14, height=0.06,
                            fill_color=ACCENT, fill_opacity=1,
                            stroke_width=0).to_edge(UP, buff=0.28)
        self.add(top_bar)

        badge_bg = RoundedRectangle(corner_radius=0.18, width=2.9, height=0.52,
                                    fill_color=ACCENT, fill_opacity=0.18,
                                    stroke_color=ACCENT, stroke_width=1.5)
        badge_txt = Text("QUESTION ", font="Courier New", font_size=17,
                         color=ACCENT, weight=BOLD).move_to(badge_bg)
        badge = VGroup(badge_bg, badge_txt)
        ctx = Text("Thin Film Interference  ·  Optics",
                   font="Georgia", font_size=16, color=SUBTEXT)
        header = VGroup(badge, ctx).arrange(RIGHT, buff=0.5)
        header.to_edge(UP, buff=0.55).to_edge(LEFT, buff=0.55)
        self.play(FadeIn(header, shift=DOWN * 0.25), run_time=0.7)

        # ── Question lines ───────────────────────────────────────────────
        line1 = MathTex(
            r"\text{A ray of light (}\lambda = 600\,\text{nm) hits a thin film of glass.}",
            font_size=36, color=WHITE)

        # Ray 1
        l2a = Text("Ray 1", font="Georgia", font_size=24, color=GOLD, weight=BOLD)
        l2b = Text(" reflects off the top surface (Air to Glass).",
                   font="Georgia", font_size=24, color=WHITE)
        line2 = VGroup(l2a, l2b).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)

        # Ray 2
        l3a = Text("Ray 2", font="Georgia", font_size=24, color=PURPLE, weight=BOLD)
        l3b = Text(" travels through the film and reflects off the",
                   font="Georgia", font_size=24, color=WHITE)
        line3 = VGroup(l3a, l3b).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)

        line3b = Text("bottom (Glass to Air).",
                      font="Georgia", font_size=24, color=WHITE)

        line4 = MathTex(
            r"\text{If the film thickness is exactly }"
            r"\textbf{150\,nm}"
            r"\text{ and the refractive index is }"
            r"\textbf{1.5}\text{,}",
            font_size=36, color=WHITE)

        line5 = MathTex(
            r"\text{what is the \textbf{total phase difference} between the two rays}",
            font_size=36, color=WHITE)

        line6 = MathTex(
            r"\text{when they meet?}",
            font_size=36, color=WHITE)

        q_lines = VGroup(line1, line2, line3, line3b, line4, line5, line6)
        q_lines.arrange(DOWN, buff=0.26, aligned_edge=LEFT)

        q_box = SurroundingRectangle(
            q_lines, corner_radius=0.22, buff=0.38,
            fill_color=OPT_BG, fill_opacity=0.6,
            stroke_color=ACCENT, stroke_width=1.4)

        q_group = VGroup(q_box, q_lines)
        q_group.move_to(UP * 0.4 + LEFT * 1.5)
        if q_group.width > 9.2:
            q_group.scale(9.2 / q_group.width)

        self.play(FadeIn(q_box), run_time=0.4)
        self.play(
            LaggedStart(
                Write(line1), Write(line2), Write(line3),
                Write(line3b), Write(line4), Write(line5), Write(line6),
                lag_ratio=0.28),
            run_time=3.2)

        # ══════════════════════════════════════════════════════════════════
        # TIMER — fixed N_PTS, add dynamically without FadeIn
        # ══════════════════════════════════════════════════════════════════
        RING_R   = 0.85
        RING_CTR = np.array([4.3, -0.6, 0.0])

        ring_bg = Circle(radius=RING_R, stroke_color="#2A2A40",
                         stroke_width=16, fill_opacity=0)
        ring_bg.move_to(RING_CTR)

        timer_label = Text("TIME", font="Courier New", font_size=17,
                           color=SUBTEXT, weight=BOLD)
        timer_label.move_to(RING_CTR + UP * (RING_R + 0.30))

        def make_arc_mob(frac, color):
            f = max(frac, 0.0001)
            angles = np.linspace(PI/2, PI/2 - TAU * f, N_PTS)
            pts = np.column_stack([
                RING_CTR[0] + RING_R * np.cos(angles),
                RING_CTR[1] + RING_R * np.sin(angles),
                np.zeros(N_PTS)
            ])
            mob = VMobject(stroke_color=color, stroke_width=16, fill_opacity=0)
            mob.set_points_smoothly(pts)
            return mob

        arc_mob = make_arc_mob(1.0, OK_COL)

        num_mob = Text("60", font="Courier New", font_size=50,
                       color=OK_COL, weight=BOLD)
        num_mob.move_to(RING_CTR + UP * 0.08)

        sec_mob = Text("sec", font="Courier New", font_size=15, color=SUBTEXT)
        sec_mob.move_to(RING_CTR + DOWN * 0.44)

        state = {"elapsed": 0.0, "active": True}

        def arc_updater(mob, dt):
            if not state["active"]:
                return
            state["elapsed"] = min(state["elapsed"] + dt, TOTAL)
            frac  = 1.0 - state["elapsed"] / TOTAL
            color = WARN_COL if (TOTAL - state["elapsed"]) <= 15 else OK_COL
            mob.become(make_arc_mob(frac, color))

        def num_updater(mob, dt):
            if not state["active"]:
                return
            remaining = max(0, TOTAL - int(state["elapsed"]))
            color = WARN_COL if remaining <= 15 else OK_COL
            new = Text(str(remaining), font="Courier New",
                       font_size=50, color=color, weight=BOLD)
            new.move_to(RING_CTR + UP * 0.08)
            mob.become(new)

        def sec_updater(mob, dt):
            if not state["active"]:
                return
            remaining = max(0, TOTAL - int(state["elapsed"]))
            color = WARN_COL if remaining <= 15 else OK_COL
            new = Text("sec", font="Courier New", font_size=15, color=color)
            new.move_to(RING_CTR + DOWN * 0.44)
            mob.become(new)

        # Static parts via FadeIn, dynamic parts via self.add()
        self.play(FadeIn(VGroup(timer_label, ring_bg), scale=0.85), run_time=0.6)
        self.add(arc_mob, num_mob, sec_mob)

        arc_mob.add_updater(arc_updater)
        num_mob.add_updater(num_updater)
        sec_mob.add_updater(sec_updater)

        # ── 44 s → show solution hint → 16 s ────────────────────────────
        self.wait(44)

        note_bg = RoundedRectangle(corner_radius=0.18, width=7.0, height=1.6,
                                   fill_color="#0D1F12", fill_opacity=0.92,
                                   stroke_color=OK_COL, stroke_width=1.4)
        note_title = Text("Key Relations:", font="Georgia", font_size=19,
                          color=OK_COL, weight=BOLD)
        note_m1 = MathTex(
            r"\delta_{\text{path}} = 2nt = 2(1.5)(150) = 450\,\text{nm}"
            r"\;\Rightarrow\;\phi_{\text{path}} = \frac{2\pi}{\lambda}\cdot 2nt = \frac{3\pi}{2}",
            font_size=28, color=WHITE)
        note_m2 = MathTex(
            r"\phi_{\text{reflection}} = \pi \text{ (Ray 1 only, denser medium)}"
            r"\;\Rightarrow\;\phi_{\text{total}} = \frac{3\pi}{2} + \pi = \frac{5\pi}{2}",
            font_size=28, color=GOLD)
        note_inner = VGroup(note_title, note_m1, note_m2).arrange(DOWN, buff=0.16)
        note_grp = VGroup(note_bg, note_inner).arrange(ORIGIN)
        note_grp.to_edge(DOWN, buff=0.28)
        self.play(FadeIn(note_grp, shift=UP * 0.15), run_time=0.7)
        self.wait(16)

        # ── Stop & flash ─────────────────────────────────────────────────
        state["active"] = False
        arc_mob.remove_updater(arc_updater)
        num_mob.remove_updater(num_updater)
        sec_mob.remove_updater(sec_updater)

        flash_bg  = Rectangle(width=14, height=8, fill_color=BLACK,
                              fill_opacity=0.7, stroke_width=0)
        flash_txt = Text("TIME'S UP!", font="Courier New", font_size=68,
                         color=WARN_COL, weight=BOLD)
        self.play(FadeIn(flash_bg), Write(flash_txt), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(flash_bg), FadeOut(flash_txt), run_time=0.5)
        self.wait(0.5)