from manim import *
import numpy as np


class NonReflectiveCoatingQuestion(Scene):
    def construct(self):

        BG       = "#0D0D1A"
        ACCENT   = "#00D4FF"
        GOLD     = "#FFD700"
        GREEN    = "#00FF88"
        OPT_BG   = "#1A1A2E"
        WHITE    = "#FFFFFF"
        SUBTEXT  = "#B0B8CC"
        OK_COL   = "#00FF88"
        WARN_COL = "#FF6B35"

        self.camera.background_color = BG
        TOTAL = 60
        N_PTS = 200

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
        ctx = Text("Non-Reflective Coating  ·  Thin Film  ·  Optics",
                   font="Georgia", font_size=16, color=SUBTEXT)
        header = VGroup(badge, ctx).arrange(RIGHT, buff=0.5)
        header.to_edge(UP, buff=0.55).to_edge(LEFT, buff=0.55)
        self.play(FadeIn(header, shift=DOWN * 0.25), run_time=0.7)

        # ── Question lines ───────────────────────────────────────────────
        line1 = MathTex(
            r"\text{You want to design a non-reflective coating }(\mu = 1.25)",
            font_size=37, color=WHITE)

        line2 = MathTex(
            r"\text{for a lens to cancel out }"
            r"\textbf{Green light}"
            r"\text{ }(\lambda = 500\,\text{nm})\text{.}",
            font_size=37)
        line2.set_color(WHITE)
        # colour "Green light" submobject — index 1
        line2[0][16:27].set_color(GREEN)

        line3 = MathTex(
            r"\text{What is the \textbf{minimum thickness} the coating}",
            font_size=37, color=WHITE)

        line4 = MathTex(
            r"\text{must be to ensure the reflected rays are }",
            font_size=37, color=WHITE)

        line5 = MathTex(
            r"\textbf{180}^\circ\text{ out of phase?}",
            font_size=37, color=GOLD)

        q_lines = VGroup(line1, line2, line3, line4, line5)
        q_lines.arrange(DOWN, buff=0.30, aligned_edge=LEFT)

        q_box = SurroundingRectangle(
            q_lines, corner_radius=0.22, buff=0.38,
            fill_color=OPT_BG, fill_opacity=0.6,
            stroke_color=ACCENT, stroke_width=1.4)

        q_group = VGroup(q_box, q_lines)
        q_group.move_to(UP * 0.55 + LEFT * 1.5)
        if q_group.width > 9.2:
            q_group.scale(9.2 / q_group.width)

        self.play(FadeIn(q_box), run_time=0.4)
        self.play(
            LaggedStart(
                Write(line1), Write(line2), Write(line3),
                Write(line4), Write(line5), lag_ratio=0.30),
            run_time=2.8)

        # ══════════════════════════════════════════════════════════════════
        # TIMER
        # ══════════════════════════════════════════════════════════════════
        RING_R   = 0.85
        RING_CTR = np.array([4.3, -0.65, 0.0])

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
            if not state["active"]: return
            state["elapsed"] = min(state["elapsed"] + dt, TOTAL)
            frac  = 1.0 - state["elapsed"] / TOTAL
            color = WARN_COL if (TOTAL - state["elapsed"]) <= 15 else OK_COL
            mob.become(make_arc_mob(frac, color))

        def num_updater(mob, dt):
            if not state["active"]: return
            remaining = max(0, TOTAL - int(state["elapsed"]))
            color = WARN_COL if remaining <= 15 else OK_COL
            new = Text(str(remaining), font="Courier New",
                       font_size=50, color=color, weight=BOLD)
            new.move_to(RING_CTR + UP * 0.08)
            mob.become(new)

        def sec_updater(mob, dt):
            if not state["active"]: return
            remaining = max(0, TOTAL - int(state["elapsed"]))
            color = WARN_COL if remaining <= 15 else OK_COL
            new = Text("sec", font="Courier New", font_size=15, color=color)
            new.move_to(RING_CTR + DOWN * 0.44)
            mob.become(new)

        self.play(FadeIn(VGroup(timer_label, ring_bg), scale=0.85), run_time=0.6)
        self.add(arc_mob, num_mob, sec_mob)
        arc_mob.add_updater(arc_updater)
        num_mob.add_updater(num_updater)
        sec_mob.add_updater(sec_updater)

        # ── 44 s → show solution hint → 16 s ────────────────────────────
        self.wait(44)

        note_bg = RoundedRectangle(corner_radius=0.18, width=7.2, height=1.55,
                                   fill_color="#0D1220", fill_opacity=0.93,
                                   stroke_color=OK_COL, stroke_width=1.4)
        note_title = Text("Key Formula:", font="Georgia", font_size=19,
                          color=OK_COL, weight=BOLD)
        note_m1 = MathTex(
            r"\text{Both reflections shift by }\pi"
            r"\;\Rightarrow\;"
            r"\text{net reflection phase} = 0",
            font_size=28, color=WHITE)
        note_m2 = MathTex(
            r"2\mu t = \frac{\lambda}{2}"
            r"\;\Rightarrow\;"
            r"t = \frac{\lambda}{4\mu} = \frac{500}{4 \times 1.25} = \mathbf{100\,nm}",
            font_size=30, color=GOLD)
        note_inner = VGroup(note_title, note_m1, note_m2).arrange(DOWN, buff=0.16)
        note_grp = VGroup(note_bg, note_inner).arrange(ORIGIN)
        note_grp.to_edge(DOWN, buff=0.30)
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