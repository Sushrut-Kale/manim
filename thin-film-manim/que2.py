from manim import *
import numpy as np


class NewtonsRingsQuestion(Scene):
    def construct(self):

        BG       = "#0D0D1A"
        ACCENT   = "#00D4FF"
        GOLD     = "#FFD700"
        OPT_BG   = "#1A1A2E"
        WHITE    = "#FFFFFF"
        SUBTEXT  = "#B0B8CC"
        OK_COL   = "#00FF88"
        WARN_COL = "#FF6B35"

        self.camera.background_color = BG
        TOTAL    = 60
        N_PTS    = 200          # FIXED point count — never changes between frames

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
        ctx = Text("Newton's Rings  ·  Optics",
                   font="Georgia", font_size=16, color=SUBTEXT)
        header = VGroup(badge, ctx).arrange(RIGHT, buff=0.5)
        header.to_edge(UP, buff=0.55).to_edge(LEFT, buff=0.55)
        self.play(FadeIn(header, shift=DOWN * 0.25), run_time=0.7)

        # ── Question lines ───────────────────────────────────────────────
        line1 = Text(
            "In a Newton's Rings experiment, you measure",
            font="Georgia", font_size=25, color=WHITE)

        line2 = MathTex(
            r"\text{the diameter of the }",
            r"\textbf{4th}",
            r"\text{ dark ring }",
            r"\textbf{(D}_4\textbf{)}",
            r"\text{ to be }",
            r"\textbf{2 mm}\text{.}",
            font_size=40)
        line2.set_color(WHITE)
        line2[1].set_color(GOLD)
        line2[3].set_color(GOLD)
        line2[5].set_color(GOLD)

        line3 = Text(
            "Without moving anything, what should be",
            font="Georgia", font_size=25, color=WHITE)

        line4 = MathTex(
            r"\text{the exact diameter of the }",
            r"\textbf{16th}",
            r"\text{ dark ring }",
            r"\textbf{(D}_{16}\textbf{)}\text{?}",
            font_size=40)
        line4.set_color(WHITE)
        line4[1].set_color(ACCENT)
        line4[3].set_color(ACCENT)

        hint = MathTex(
            r"\text{Hint: } D_n \propto \sqrt{n}",
            font_size=36, color=SUBTEXT)

        q_lines = VGroup(line1, line2, line3, line4, hint)
        q_lines.arrange(DOWN, buff=0.30, aligned_edge=LEFT)

        q_box = SurroundingRectangle(
            q_lines, corner_radius=0.22, buff=0.38,
            fill_color=OPT_BG, fill_opacity=0.6,
            stroke_color=ACCENT, stroke_width=1.4)

        q_group = VGroup(q_box, q_lines)
        q_group.move_to(UP * 0.55 + LEFT * 1.6)
        if q_group.width > 9.2:
            q_group.scale(9.2 / q_group.width)

        self.play(FadeIn(q_box), run_time=0.4)
        self.play(
            LaggedStart(
                Write(line1), Write(line2), Write(line3),
                Write(line4), Write(hint), lag_ratio=0.35),
            run_time=2.8)

        # ══════════════════════════════════════════════════════════════════
        # TIMER
        # ══════════════════════════════════════════════════════════════════
        RING_R   = 0.85
        RING_CTR = np.array([4.2, -0.55, 0.0])

        # Static grey background ring
        ring_bg = Circle(radius=RING_R, stroke_color="#2A2A40",
                         stroke_width=16, fill_opacity=0)
        ring_bg.move_to(RING_CTR)

        timer_label = Text("TIME", font="Courier New", font_size=17,
                           color=SUBTEXT, weight=BOLD)
        timer_label.move_to(RING_CTR + UP * (RING_R + 0.30))

        # ── Arc builder — ALWAYS N_PTS points ────────────────────────────
        def make_arc_points(frac):
            """
            Return N_PTS points along a clockwise arc of `frac` turns.
            When frac < 1, remaining points collapse to the arc's endpoint
            so the point count is always exactly N_PTS.
            """
            if frac <= 0:
                frac = 0.0001
            angles = np.linspace(PI/2, PI/2 - TAU * frac, N_PTS)
            pts = np.column_stack([
                RING_CTR[0] + RING_R * np.cos(angles),
                RING_CTR[1] + RING_R * np.sin(angles),
                np.zeros(N_PTS)
            ])
            return pts

        def make_arc_mob(frac, color):
            pts = make_arc_points(frac)
            mob = VMobject(stroke_color=color, stroke_width=16, fill_opacity=0)
            mob.set_points_smoothly(pts)
            return mob

        # Build initial arc (full circle)
        arc_mob = make_arc_mob(1.0, OK_COL)

        # Number and sec — absolute positions
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

        # Add static elements first (these are safe to FadeIn together)
        static_timer = VGroup(timer_label, ring_bg)
        self.play(FadeIn(static_timer, scale=0.85), run_time=0.6)

        # Add dynamic elements directly (no FadeIn — avoids shape interpolation crash)
        self.add(arc_mob, num_mob, sec_mob)

        # NOW attach updaters (after adding to scene, after any animations)
        arc_mob.add_updater(arc_updater)
        num_mob.add_updater(num_updater)
        sec_mob.add_updater(sec_updater)

        # ── 44 s → reveal key relation → 16 s ───────────────────────────
        self.wait(44)

        note_bg = RoundedRectangle(corner_radius=0.18, width=6.4, height=1.45,
                                   fill_color="#0D1F12", fill_opacity=0.92,
                                   stroke_color=OK_COL, stroke_width=1.4)
        note_title = Text("Key Relation:", font="Georgia", font_size=20,
                          color=OK_COL, weight=BOLD)
        note_m1 = MathTex(
            r"D_{16} / D_4 = \sqrt{16/4} = \sqrt{4} = 2",
            font_size=34, color=WHITE)
        note_m2 = MathTex(
            r"\Rightarrow D_{16} = 2 \times 2\,\text{mm} = \mathbf{4\,mm}",
            font_size=34, color=GOLD)
        note_inner = VGroup(note_title, note_m1, note_m2).arrange(DOWN, buff=0.14)
        note_grp = VGroup(note_bg, note_inner).arrange(ORIGIN)
        note_grp.to_edge(DOWN, buff=0.35)
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