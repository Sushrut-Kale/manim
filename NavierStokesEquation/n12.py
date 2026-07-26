
from manim import *
import numpy as np


# ─────────────────────────────────────────────────────────────────────────────
# Color palette
# ─────────────────────────────────────────────────────────────────────────────
FLUID_BLUE     = "#4FC3F7"
ELEC_YELLOW    = "#FFD54F"
MAG_PURPLE     = "#CE93D8"
LORENTZ_WHITE  = "#FFFFFF"
EQ_WHITE       = "#ECEFF1"
HIGHLIGHT_CYAN = "#00E5FF"
DIM_GRAY       = "#37474F"
LABEL_ORANGE   = "#FFAB40"
BG_COLOR       = "#050A10"


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def make_fluid_streamline(y_offset: float, color=FLUID_BLUE,
                           stroke_width=2.0) -> VMobject:
    return ParametricFunction(
        lambda t: np.array([t, y_offset + 0.15 * np.sin(2 * t), 0]),
        t_range=[-6.5, 6.5],
        color=color,
        stroke_width=stroke_width,
    )


def make_arrow_field(direction: np.ndarray, rows: int, cols: int,
                     spacing: float, color: str,
                     arrow_len: float = 0.4) -> VGroup:
    group = VGroup()
    x_start = -(cols - 1) * spacing / 2
    y_start = -(rows - 1) * spacing / 2
    for r in range(rows):
        for c in range(cols):
            origin = np.array([x_start + c * spacing,
                                y_start + r * spacing, 0])
            tip = origin + arrow_len * direction
            arr = Arrow(origin, tip, buff=0, color=color,
                        stroke_width=1.5,
                        max_tip_length_to_length_ratio=0.4)
            group.add(arr)
    return group


def make_circular_field_lines(n_circles: int = 5, color=MAG_PURPLE,
                               center=ORIGIN) -> VGroup:
    group = VGroup()
    for i in range(1, n_circles + 1):
        r = 0.45 * i
        c = Circle(radius=r, color=color,
                   stroke_width=max(0.5, 2.0 - i * 0.25),
                   stroke_opacity=max(0.2, 0.85 - i * 0.08))
        c.move_to(center)
        group.add(c)
    dot = Dot(center, radius=0.06, color=color)
    group.add(dot)
    return group


# ─────────────────────────────────────────────────────────────────────────────
# Main Scene
# ─────────────────────────────────────────────────────────────────────────────

class Scene12_ElectromagneticExtension(Scene):
    """Electromagnetic Extension — From Fluid to Magnetohydrodynamics."""

    def construct(self):
        self.camera.background_color = BG_COLOR
        self._opening_title()
        self._part1_fluid_recap()
        self._part2_electric_field()
        self._part3_magnetic_field()
        self._part4_lorentz_force()
        self._part5_replace_force()
        self._part6_maxwell_coupling()
        self._part7_physical_demo()

    # ═══════════════════════════════════════════════════════════════════════
    # OPENING TITLE — cinematic hook
    # ═══════════════════════════════════════════════════════════════════════
    def _opening_title(self):
        top_line = Line(LEFT * 5.5, RIGHT * 5.5,
                        color=HIGHLIGHT_CYAN, stroke_width=1.5).move_to(UP * 3.1)
        bot_line = Line(LEFT * 5.5, RIGHT * 5.5,
                        color=HIGHLIGHT_CYAN, stroke_width=1.5).move_to(DOWN * 3.1)

        q1 = Text("In Navier–Stokes, the body force  f",
                  font="Courier New", font_size=28, color=EQ_WHITE)
        q2 = Text("drives all non-pressure, non-viscous effects.",
                  font="Courier New", font_size=28, color=EQ_WHITE)
        q3 = Text("What happens when we replace",
                  font="Courier New", font_size=30, color=EQ_WHITE)

        replace_eq = MathTex(
            r"\mathbf{f}  \;\longrightarrow\;  "
            r"\rho_e \mathbf{E} + \mathbf{J} \times \mathbf{B}",
            font_size=46, color=HIGHLIGHT_CYAN,
        )

        q4 = Text("with the Lorentz electromagnetic force?",
                  font="Courier New", font_size=30, color=EQ_WHITE)

        answer = Text(
            "→  Fluid dynamics becomes Magnetohydrodynamics",
            font="Courier New", font_size=28, color=ELEC_YELLOW,
        )

        content = VGroup(q1, q2, q3, replace_eq, q4, answer).arrange(
            DOWN, buff=0.35, aligned_edge=LEFT
        )
        content.move_to(ORIGIN + LEFT * 0.2)

        self.play(
            Create(top_line, rate_func=smooth),
            Create(bot_line, rate_func=smooth),
            run_time=0.8,
        )
        self.play(
            LaggedStart(
                FadeIn(q1, shift=RIGHT * 0.3),
                FadeIn(q2, shift=RIGHT * 0.3),
                lag_ratio=0.5,
            ),
            run_time=1.2,
        )
        self.wait(0.3)
        self.play(FadeIn(q3, shift=UP * 0.2), run_time=0.6)
        self.play(Write(replace_eq, rate_func=smooth), run_time=1.4)
        self.play(FadeIn(q4, shift=UP * 0.2), run_time=0.6)
        self.wait(0.3)
        self.play(FadeIn(answer, scale=1.04, rate_func=smooth), run_time=0.9)
        self.wait(2.5)

        self.play(
            FadeOut(top_line), FadeOut(bot_line),
            FadeOut(q1), FadeOut(q2), FadeOut(q3),
            FadeOut(replace_eq), FadeOut(q4), FadeOut(answer),
            run_time=1.0,
        )

    # ═══════════════════════════════════════════════════════════════════════
    # PART 1 — Normal Fluid Recap
    # ═══════════════════════════════════════════════════════════════════════
    def _part1_fluid_recap(self):
        title = Text("Electromagnetic Extension",
                     font="Courier New", font_size=34, color=HIGHLIGHT_CYAN)
        sub = Text("From Fluid to Magnetohydrodynamics",
                   font="Courier New", font_size=20, color=EQ_WHITE)
        VGroup(title, sub).arrange(DOWN, buff=0.22).move_to(UP * 2.9)

        # Streamlines in the vertical band -1.2 to +1.2
        streamlines = VGroup(
            *[make_fluid_streamline(y, stroke_width=2.0 + 0.3 * abs(y))
              for y in np.linspace(-1.2, 1.2, 6)]
        )

        flow_arrows = VGroup()
        for y in np.linspace(-1.0, 1.0, 3):
            for x in [-3, 0, 3]:
                arr = Arrow(
                    np.array([x - 0.4, y + 0.15 * np.sin(2*(x-0.4)), 0]),
                    np.array([x + 0.4, y + 0.15 * np.sin(2*(x+0.4)), 0]),
                    buff=0, color=FLUID_BLUE, stroke_width=1.5,
                    max_tip_length_to_length_ratio=0.35,
                )
                flow_arrows.add(arr)

        # NS equation sits in the negative half, well below streamlines
        ns_eq = MathTex(
            r"\rho\!\left(\frac{\partial \mathbf{v}}{\partial t} + "
            r"(\mathbf{v}\cdot\nabla)\mathbf{v}\right) = "
            r"-\nabla p + \mu\nabla^2\mathbf{v}",
            color=EQ_WHITE, font_size=27,
        )
        ns_eq.move_to(DOWN * 2.1)

        caption = Text("Fluid motion is governed by Navier–Stokes",
                       font="Courier New", font_size=26, color=EQ_WHITE)
        caption.move_to(DOWN * 3.2)

        self.play(FadeIn(title, shift=UP*0.3), FadeIn(sub, shift=UP*0.2),
                  run_time=1.2)
        self.play(Create(streamlines, rate_func=smooth), run_time=1.8)
        self.play(FadeIn(flow_arrows, rate_func=smooth), run_time=0.8)
        self.play(FadeIn(caption), run_time=0.7)
        self.play(Write(ns_eq, rate_func=smooth), run_time=1.5)
        self.wait(1.5)

        # Save for Part 2/3
        self._streamlines = streamlines
        self._flow_arrows  = flow_arrows

        self.play(
            FadeOut(title), FadeOut(sub),
            FadeOut(caption), FadeOut(ns_eq),
            run_time=0.8,
        )

    # ═══════════════════════════════════════════════════════════════════════
    # PART 2 — Introduce Electric Field
    # ═══════════════════════════════════════════════════════════════════════
    def _part2_electric_field(self):
        self._streamlines.set_opacity(0.3)

        # E-field arrow grid — constrained rows/cols to avoid screen edges
        e_field = make_arrow_field(
            direction=RIGHT, rows=4, cols=7, spacing=1.6,
            color=ELEC_YELLOW, arrow_len=0.45,
        )

        # Particles — fixed positions, moderate count
        p_pos = [
            [-3.2, -0.6], [-1.4, 0.7], [0.4, -0.5],
            [2.2,  0.8],  [-2.0, 0.1], [1.2, -0.8],
        ]
        particles = VGroup(
            *[Dot(np.array([x, y, 0]), radius=0.08, color=FLUID_BLUE)
              for x, y in p_pos]
        )

        # Caption — top, well clear of field arrows
        caption = Text("Electric field influences charged particles",
                       font="Courier New", font_size=26, color=EQ_WHITE)
        caption.move_to(UP * 3.2)

        # Label block — bottom zone
        label_E = MathTex(r"\mathbf{E}", color=ELEC_YELLOW, font_size=34)
        desc_E  = Text("electric field  (force per unit charge)",
                       font="Courier New", font_size=21, color=ELEC_YELLOW)
        lblock_E = VGroup(label_E, desc_E).arrange(RIGHT, buff=0.22)
        lblock_E.move_to(DOWN * 3.1)

        self.play(Create(e_field, rate_func=smooth), run_time=2.0)
        self.play(FadeIn(particles), run_time=0.5)
        self.play(
            *[p.animate.shift(RIGHT * 1.3) for p in particles],
            run_time=1.8, rate_func=smooth,
        )
        self.play(FadeIn(caption), run_time=0.6)
        self.play(Write(label_E), FadeIn(desc_E), run_time=1.0)
        self.wait(2.0)

        # ── Full cleanup ─────────────────────────────────────────────────
        self.play(
            FadeOut(e_field), FadeOut(particles),
            FadeOut(caption), FadeOut(lblock_E),
            run_time=0.8,
        )
        self._streamlines.set_opacity(1.0)

    # ═══════════════════════════════════════════════════════════════════════
    # PART 3 — Introduce Magnetic Field
    # ═══════════════════════════════════════════════════════════════════════
    def _part3_magnetic_field(self):
        b_centers = [LEFT * 3.5, ORIGIN, RIGHT * 3.5]
        b_fields  = VGroup(
            *[make_circular_field_lines(4, color=MAG_PURPLE, center=c)
              for c in b_centers]
        )

        caption = Text("Magnetic field alters motion of moving charges",
                       font="Courier New", font_size=26, color=EQ_WHITE)
        caption.move_to(UP * 3.2)

        label_B = MathTex(r"\mathbf{B}", color=MAG_PURPLE, font_size=34)
        desc_B  = Text("magnetic field",
                       font="Courier New", font_size=21, color=MAG_PURPLE)
        lblock_B = VGroup(label_B, desc_B).arrange(RIGHT, buff=0.22)
        lblock_B.move_to(DOWN * 3.1)

        p_pos = [
            [-3.2, -0.5], [-1.0, 0.7], [0.6, -0.6],
            [2.6,  0.5],  [-2.0, 0.1], [1.5, 0.8],
        ]
        particles = VGroup(
            *[Dot(np.array([x, y, 0]), radius=0.08, color=FLUID_BLUE)
              for x, y in p_pos]
        )

        self.play(
            FadeOut(self._streamlines),
            FadeOut(self._flow_arrows),
            run_time=0.5,
        )
        self.play(Create(b_fields, rate_func=smooth), run_time=2.0)
        self.play(FadeIn(particles), run_time=0.4)
        self.play(FadeIn(caption), run_time=0.6)
        self.play(Write(label_B), FadeIn(desc_B), run_time=1.0)

        # Lorentz deflection preview
        angles = [PI/3, -PI/3, PI/4, -PI/4, PI/2.5, -PI/2.5]
        self.play(
            *[Rotate(p, angle=a,
                     about_point=p.get_center() + UP * 0.9,
                     rate_func=smooth)
              for p, a in zip(particles, angles)],
            run_time=2.0,
        )
        self.wait(1.5)

        # ── Full cleanup ─────────────────────────────────────────────────
        self.play(
            FadeOut(b_fields), FadeOut(particles),
            FadeOut(caption), FadeOut(lblock_B),
            run_time=0.8,
        )

    # ═══════════════════════════════════════════════════════════════════════
    # PART 4 — Lorentz Force Equation
    # ═══════════════════════════════════════════════════════════════════════
    def _part4_lorentz_force(self):
        """
        FIX: Annotations in TWO separate rows (not one line).
        Force arrows placed at screen RIGHT — zero equation overlap.
        """
        caption = Text("Lorentz force density acting on the fluid",
                       font="Courier New", font_size=26, color=EQ_WHITE)
        caption.move_to(UP * 3.2)

        # ── Main equation — upper centre ─────────────────────────────────
        lorentz_eq = MathTex(
            r"\mathbf{f} = \rho_e \mathbf{E} + \mathbf{J} \times \mathbf{B}",
            color=LORENTZ_WHITE, font_size=48,
        )
        lorentz_eq.set_color_by_tex(r"\mathbf{E}", ELEC_YELLOW)
        lorentz_eq.set_color_by_tex(r"\mathbf{B}", MAG_PURPLE)
        lorentz_eq.move_to(UP * 1.6)

        # ── Annotation ROW 1: ρₑ  and  E  ──────────────────────────────
        ann_rho = self._make_ann(
            r"\rho_e", "charge density  (charge / volume)", LABEL_ORANGE)
        ann_E   = self._make_ann(
            r"\mathbf{E}", "electric field  (force / charge)", ELEC_YELLOW)
        row1 = VGroup(ann_rho, ann_E).arrange(RIGHT, buff=1.2)
        row1.move_to(UP * 0.2)

        # ── Annotation ROW 2: J  and  B  ────────────────────────────────
        ann_J = self._make_ann(
            r"\mathbf{J}", "current density  (flow of charge)", LABEL_ORANGE)
        ann_B = self._make_ann(
            r"\mathbf{B}", "magnetic field", MAG_PURPLE)
        row2 = VGroup(ann_J, ann_B).arrange(RIGHT, buff=1.2)
        row2.move_to(DOWN * 0.9)

        # ── Cross-product note ───────────────────────────────────────────
        cross_note = Text(
            "×  cross product  →  force perpendicular to J and B",
            font="Courier New", font_size=19, color=EQ_WHITE,
        )
        cross_note.move_to(DOWN * 2.0)

        # ── Demo particles + force arrows — RIGHT side, clear of equation
        demo_dots = VGroup(
            *[Dot(np.array([5.2, y, 0]), radius=0.08, color=FLUID_BLUE)
              for y in [-0.9, 0.0, 0.9]]
        )
        demo_arrows = VGroup(
            *[Arrow(
                d.get_center(),
                d.get_center() + UP * 0.65 + LEFT * 0.15,
                buff=0, color=LORENTZ_WHITE,
                stroke_width=2.5,
                max_tip_length_to_length_ratio=0.4,
            )
              for d in demo_dots]
        )

        # ── Animate ──────────────────────────────────────────────────────
        self.play(FadeIn(caption), run_time=0.6)
        self.play(Write(lorentz_eq, rate_func=smooth), run_time=2.0)
        self.wait(0.4)
        self.play(
            LaggedStart(
                FadeIn(row1, shift=UP * 0.1),
                FadeIn(row2, shift=UP * 0.1),
                FadeIn(cross_note, shift=UP * 0.1),
                lag_ratio=0.35,
            ),
            run_time=1.8,
        )
        self.wait(0.3)
        self.play(FadeIn(demo_dots), run_time=0.4)
        self.play(
            LaggedStart(
                *[GrowArrow(fa) for fa in demo_arrows],
                lag_ratio=0.3,
            ),
            run_time=1.2,
        )
        self.wait(1.5)

        # Save for Part 5
        self._lorentz_eq = lorentz_eq

        self.play(
            FadeOut(caption),
            FadeOut(row1), FadeOut(row2), FadeOut(cross_note),
            FadeOut(demo_dots), FadeOut(demo_arrows),
            run_time=0.8,
        )

    # ═══════════════════════════════════════════════════════════════════════
    # PART 5 — Replace f in Navier–Stokes
    # ═══════════════════════════════════════════════════════════════════════
    def _part5_replace_force(self):
        """
        FIX: NS original shown at top (y ≈ +1.9).
        Replacement arrow + text between the two equations.
        MHD equation shown at centre (y ≈ -0.3).
        No two equations overlap at any point.
        """
        question = Text(
            "What if we replace  f  with the Lorentz force?",
            font="Courier New", font_size=26, color=HIGHLIGHT_CYAN,
        )
        question.move_to(UP * 3.3)

        # Original NS with generic f — placed near top
        ns_orig = MathTex(
            r"\rho\!\left(\frac{\partial \mathbf{v}}{\partial t} "
            r"+ (\mathbf{v}\cdot\nabla)\mathbf{v}\right)"
            r"= -\nabla p + \mu\nabla^2\mathbf{v} + \mathbf{f}",
            color=EQ_WHITE, font_size=29,
        )
        ns_orig.move_to(UP * 1.8)

        # Brace under f in ns_orig
        brace_f       = Brace(ns_orig[-1], direction=DOWN, color=HIGHLIGHT_CYAN)
        brace_f_label = Text("body force", font="Courier New",
                              font_size=19, color=HIGHLIGHT_CYAN)
        brace_f_label.next_to(brace_f, DOWN, buff=0.08)

        # Slide old Lorentz equation out of the way
        self.play(
            self._lorentz_eq.animate.move_to(DOWN * 3.6).scale(0.0),
            run_time=0.5,
        )
        self.play(FadeIn(question), run_time=0.6)
        self.play(Write(ns_orig, rate_func=smooth), run_time=1.8)
        self.play(Create(brace_f, rate_func=smooth),
                  FadeIn(brace_f_label), run_time=0.7)
        self.wait(0.8)

        # Replacement label + arrow between the two equations (y ≈ +0.6)
        replace_txt = Text("f  →  ρₑE + J×B",
                            font="Courier New", font_size=22,
                            color=HIGHLIGHT_CYAN)
        replace_arrow = Arrow(LEFT * 0.4, RIGHT * 0.4,
                               buff=0, color=HIGHLIGHT_CYAN,
                               stroke_width=2,
                               max_tip_length_to_length_ratio=0.35)
        repl_group = VGroup(replace_arrow, replace_txt).arrange(RIGHT, buff=0.2)
        repl_group.move_to(UP * 0.6)

        self.play(
            FadeOut(brace_f), FadeOut(brace_f_label),
            FadeIn(repl_group, shift=DOWN * 0.2),
            run_time=0.7,
        )

        # MHD NS — placed at centre, safely below ns_orig
        ns_mhd = MathTex(
            r"\rho\!\left(\frac{\partial \mathbf{v}}{\partial t} "
            r"+ (\mathbf{v}\cdot\nabla)\mathbf{v}\right)"
            r"= -\nabla p + \mu\nabla^2\mathbf{v}"
            r"+ \rho_e\mathbf{E} + \mathbf{J}\times\mathbf{B}",
            color=EQ_WHITE, font_size=27,
        )
        ns_mhd.set_color_by_tex(r"\mathbf{E}", ELEC_YELLOW)
        ns_mhd.set_color_by_tex(r"\mathbf{B}", MAG_PURPLE)
        ns_mhd.set_color_by_tex(r"\rho_e",     HIGHLIGHT_CYAN)
        ns_mhd.set_color_by_tex(r"\mathbf{J}", HIGHLIGHT_CYAN)
        ns_mhd.move_to(DOWN * 0.5)        # clear gap below ns_orig

        self.play(Write(ns_mhd, rate_func=smooth), run_time=2.2)
        self.wait(0.3)

        # Highlight box around the full MHD equation
        h_box = SurroundingRectangle(
            ns_mhd, color=HIGHLIGHT_CYAN, buff=0.12,
            corner_radius=0.06, stroke_width=1.8,
        )

        # Brace only under EM terms (last 4 tokens)
        em_slice = VGroup(*ns_mhd[-4:])
        brace_em       = Brace(em_slice, direction=DOWN, color=ELEC_YELLOW)
        brace_em_label = Text("Lorentz force", font="Courier New",
                               font_size=19, color=ELEC_YELLOW)
        brace_em_label.next_to(brace_em, DOWN, buff=0.08)

        caption = Text(
            "Fluid motion now depends on electromagnetic forces",
            font="Courier New", font_size=25, color=EQ_WHITE,
        )
        caption.move_to(DOWN * 2.6)

        self.play(Create(h_box, rate_func=smooth), run_time=0.8)
        self.play(Create(brace_em, rate_func=smooth),
                  FadeIn(brace_em_label), run_time=0.7)
        self.play(FadeIn(caption), run_time=0.6)
        self.wait(2.0)

        self._ns_mhd = ns_mhd
        self.play(
            FadeOut(question), FadeOut(ns_orig),
            FadeOut(repl_group),
            FadeOut(h_box),
            FadeOut(brace_em), FadeOut(brace_em_label),
            FadeOut(caption),
            run_time=0.9,
        )

    # ═══════════════════════════════════════════════════════════════════════
    # PART 6 — Coupling with Maxwell
    # ═══════════════════════════════════════════════════════════════════════
    def _part6_maxwell_coupling(self):
        self.play(
            self._ns_mhd.animate.scale(0.70).move_to(UP * 3.1),
            run_time=0.8,
        )

        intro1 = Text("To fully describe the system…",
                      font="Courier New", font_size=25, color=EQ_WHITE)
        intro2 = Text("We must include electromagnetic equations",
                      font="Courier New", font_size=23, color=EQ_WHITE)
        VGroup(intro1, intro2).arrange(DOWN, buff=0.28).move_to(UP * 1.9)

        div_E  = MathTex(
            r"\nabla \cdot \mathbf{E} = \frac{\rho_e}{\varepsilon_0}",
            color=ELEC_YELLOW, font_size=23)
        div_B  = MathTex(
            r"\nabla \cdot \mathbf{B} = 0",
            color=MAG_PURPLE,  font_size=23)
        curl_E = MathTex(
            r"\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}",
            color=ELEC_YELLOW, font_size=23)
        curl_B = MathTex(
            r"\nabla \times \mathbf{B} = \mu_0\!\left("
            r"\mathbf{J} + \varepsilon_0"
            r"\frac{\partial \mathbf{E}}{\partial t}\right)",
            color=MAG_PURPLE, font_size=23)

        maxwell_grid = VGroup(div_E, curl_E, div_B, curl_B).arrange_in_grid(
            rows=2, cols=2, buff=(1.0, 0.45)
        )
        maxwell_grid.move_to(DOWN * 0.6)

        maxwell_title = Text("Maxwell's Equations",
                              font="Courier New", font_size=21,
                              color=HIGHLIGHT_CYAN)
        maxwell_title.next_to(maxwell_grid, UP, buff=0.28)

        mhd_line = Text("Navier–Stokes  +  Electromagnetism",
                         font="Courier New", font_size=27, color=EQ_WHITE)
        mhd_line.move_to(DOWN * 2.55)

        final_label = Text("This is Magnetohydrodynamics",
                            font="Courier New", font_size=32,
                            color=HIGHLIGHT_CYAN)
        final_label.move_to(DOWN * 3.2)

        self.play(
            LaggedStart(
                FadeIn(intro1, shift=DOWN * 0.2),
                FadeIn(intro2, shift=DOWN * 0.2),
                lag_ratio=0.5,
            ),
            run_time=1.0,
        )
        self.wait(0.3)
        self.play(FadeIn(maxwell_title), run_time=0.5)
        self.play(
            LaggedStart(
                *[Write(eq, rate_func=smooth) for eq in maxwell_grid],
                lag_ratio=0.3,
            ),
            run_time=2.5,
        )
        self.wait(0.4)
        self.play(FadeIn(mhd_line), run_time=0.6)
        self.play(FadeIn(final_label, scale=1.06, rate_func=smooth),
                  run_time=1.0)
        self.wait(2.0)

        self.play(
            FadeOut(intro1), FadeOut(intro2),
            FadeOut(maxwell_grid), FadeOut(maxwell_title),
            FadeOut(mhd_line), FadeOut(final_label),
            FadeOut(self._ns_mhd),
            run_time=1.0,
        )

    # ═══════════════════════════════════════════════════════════════════════
    # PART 7 — Physical Demonstration
    # ═══════════════════════════════════════════════════════════════════════
    def _part7_physical_demo(self):
        ch_top = Line(LEFT*5 + UP*1.15,  RIGHT*5 + UP*1.15,
                      color=DIM_GRAY, stroke_width=2)
        ch_bot = Line(LEFT*5 + DOWN*1.15, RIGHT*5 + DOWN*1.15,
                      color=DIM_GRAY, stroke_width=2)

        straight = VGroup(
            *[Line(LEFT*5 + UP*y, RIGHT*5 + UP*y,
                   color=FLUID_BLUE,
                   stroke_width=2.0 + 0.6*(1 - abs(y)),
                   stroke_opacity=0.75)
              for y in np.linspace(-0.85, 0.85, 7)]
        )

        b_above = VGroup(
            *[MathTex(r"\otimes", color=MAG_PURPLE, font_size=22
                      ).move_to(UP*1.8 + RIGHT*x)
              for x in np.linspace(-4, 4, 9)]
        )
        b_below = VGroup(
            *[MathTex(r"\odot", color=MAG_PURPLE, font_size=22
                      ).move_to(DOWN*1.8 + RIGHT*x)
              for x in np.linspace(-4, 4, 9)]
        )
        b_label = Text("B applied  (perpendicular to flow)",
                        font="Courier New", font_size=21, color=MAG_PURPLE)
        b_label.move_to(UP * 2.6)

        def deflected_stream(y_offset):
            return ParametricFunction(
                lambda t: np.array([
                    t,
                    y_offset + 0.38 * np.exp(-t**2 / 9)
                               * np.sign(y_offset + 0.01),
                    0,
                ]),
                t_range=[-5, 5],
                color=FLUID_BLUE,
                stroke_width=2.0 + 0.6*(1 - abs(y_offset)),
                stroke_opacity=0.75,
            )

        deflected = VGroup(
            *[deflected_stream(y) for y in np.linspace(-0.85, 0.85, 7)]
        )

        cap1 = Text("Fields can control fluid motion",
                     font="Courier New", font_size=27, color=EQ_WHITE)
        cap1.move_to(DOWN * 2.65)
        cap2 = Text("Conducting fluid (plasma / salt water) deflected by B",
                     font="Courier New", font_size=19, color=EQ_WHITE)
        cap2.move_to(DOWN * 3.25)

        self.play(Create(ch_top), Create(ch_bot), run_time=0.7)
        self.play(Create(straight, rate_func=smooth), run_time=1.4)
        self.play(FadeIn(b_above), FadeIn(b_below),
                  FadeIn(b_label), run_time=0.9)
        self.wait(0.5)
        self.play(
            Transform(straight, deflected, rate_func=smooth), run_time=2.5
        )
        self.play(FadeIn(cap1), run_time=0.7)
        self.play(FadeIn(cap2), run_time=0.7)
        self.wait(1.5)

        self.play(
            FadeOut(ch_top), FadeOut(ch_bot), FadeOut(straight),
            FadeOut(b_above), FadeOut(b_below), FadeOut(b_label),
            FadeOut(cap1), FadeOut(cap2),
            run_time=0.9,
        )

        # ── Final banner ──────────────────────────────────────────────────
        bg_rect = Rectangle(
            width=10.8, height=3.2,
            fill_color=BG_COLOR, fill_opacity=0.96,
            stroke_color=HIGHLIGHT_CYAN, stroke_width=1.5,
        ).move_to(ORIGIN)
        final_title = Text("Magnetohydrodynamics",
                            font="Courier New", font_size=44,
                            color=HIGHLIGHT_CYAN)
        final_sub = Text("Navier–Stokes  ·  Maxwell  ·  Lorentz",
                          font="Courier New", font_size=25, color=EQ_WHITE)
        VGroup(final_title, final_sub).arrange(DOWN, buff=0.35).move_to(ORIGIN)

        self.play(FadeIn(bg_rect), run_time=0.4)
        self.play(Write(final_title, rate_func=smooth), run_time=1.5)
        self.play(FadeIn(final_sub, shift=UP * 0.2), run_time=0.8)
        self.wait(3.0)
        self.play(
            FadeOut(bg_rect), FadeOut(final_title), FadeOut(final_sub),
            run_time=1.2,
        )

    # ═══════════════════════════════════════════════════════════════════════
    # Utility
    # ═══════════════════════════════════════════════════════════════════════
    @staticmethod
    def _make_ann(symbol: str, description: str, color=LABEL_ORANGE) -> VGroup:
        """Compact annotation: coloured LaTeX symbol + plain description text."""
        sym  = MathTex(symbol, color=color, font_size=26)
        desc = Text(description, font="Courier New", font_size=18, color=color)
        return VGroup(sym, desc).arrange(RIGHT, buff=0.16)