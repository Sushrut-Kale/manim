
from manim import *
import numpy as np


# ─────────────────────────────────────────────────────────
#  Colour palette
# ─────────────────────────────────────────────────────────
C_BG        = "#03050D"
C_FLUID     = "#3A9EDB"
C_EQ        = "#FFFFFF"
C_CYAN      = "#3DD9A4"
C_AMBER     = "#F5A623"
C_DIM       = "#2A3A4A"
C_SUBTITLE  = "#7A9AB8"
C_CREDIT    = "#C8D8E8"


# ─────────────────────────────────────────────────────────
#  Helper: laminar flow arrow grid
# ─────────────────────────────────────────────────────────
def make_flow(n_rows=4, n_cols=8,
              x_range=(-5.2, 5.2), y_range=(-1.1, 1.1),
              speed=1.0, noise=0.0, color=C_FLUID) -> VGroup:
    arrows = VGroup()
    xs  = np.linspace(*x_range, n_cols)
    ys  = np.linspace(*y_range, n_rows)
    rng = np.random.default_rng(7)
    for y in ys:
        for x in xs:
            dy = rng.uniform(-noise, noise)
            dx = speed + rng.uniform(-noise * 0.2, noise * 0.2)
            length    = np.hypot(dx, dy) * 0.52
            direction = np.array([dx, dy, 0]) / (np.hypot(dx, dy) + 1e-9)
            arr = Arrow(
                start=np.array([x, y, 0]),
                end=np.array([x, y, 0]) + direction * length,
                buff=0, stroke_width=1.5,
                max_tip_length_to_length_ratio=0.28,
                tip_length=0.20, color=color,
            ).set_opacity(0.72)
            arrows.add(arr)
    return arrows


# ─────────────────────────────────────────────────────────
#  Text helpers
# ─────────────────────────────────────────────────────────
def T(text, scale=0.68, color=WHITE):
    return Text(text, font="Georgia", color=color).scale(scale)

def S(text, scale=0.44, color=C_SUBTITLE):
    return Text(text, font="Georgia", color=color).scale(scale)

def BIG(text, scale=1.05, color=WHITE):
    return Text(text, font="Georgia", color=color).scale(scale)


# ─────────────────────────────────────────────────────────
#  Main Scene
# ─────────────────────────────────────────────────────────
class Scene14_FinalClosure(Scene):

    def setup(self):
        self.camera.background_color = C_BG

    def show(self, mob, rt=0.8, **kw):
        self.play(FadeIn(mob, **kw), run_time=rt)

    def hide(self, mob, rt=0.6, **kw):
        self.play(FadeOut(mob, **kw), run_time=rt)

    def swap_text(self, old, new, rt=0.75):
        new.move_to(old.get_center())
        self.play(FadeOut(old, shift=UP * 0.1),
                  FadeIn(new,  shift=UP * 0.1), run_time=rt)

    # ─────────────────────────────────────────────────────
    def construct(self):

        # ══════════════════════════════════════════════════
        # PART 1 · Return to Origin  (0 – 10 s)
        # ══════════════════════════════════════════════════
        origin_q = T("It started with a simple question…",
                     scale=0.66, color=C_FLUID)
        origin_q.move_to(UP * 2.6)

        flow = make_flow(speed=0.9, noise=0.0, color=C_FLUID)
        flow.move_to(DOWN * 0.4)

        self.play(FadeIn(flow, lag_ratio=0.04), run_time=1.6)
        self.play(FadeIn(origin_q, shift=DOWN * 0.1), run_time=1.0)
        self.play(flow.animate.shift(RIGHT * 0.4).set_opacity(0.85),
                  rate_func=smooth, run_time=4.0)
        self.wait(1.5)

        self.play(FadeOut(flow), FadeOut(origin_q), run_time=1.0)
        self.wait(0.2)


        # ══════════════════════════════════════════════════
        # PART 2 · Journey Recap  (10 – 30 s)
        # ══════════════════════════════════════════════════
        recap_items = [
            ("flow",      "From flow…",        C_FLUID),
            ("eq_ns",     "To mathematics…",   C_EQ),
            ("eq_cd",     "To prediction…",    C_CYAN),
            ("text_ctrl", "To control…",       C_AMBER),
        ]

        def make_recap_visual(key):
            if key == "flow":
                grp = make_flow(n_rows=5, n_cols=9,
                                speed=1.0, noise=0.08, color=C_FLUID)
                grp.scale(0.85).move_to(DOWN * 0.5)
                return grp

            elif key == "eq_ns":
                eq = MathTex(
                    r"\rho\!\left(\frac{\partial\mathbf{v}}{\partial t}"
                    r"+ (\mathbf{v}\cdot\nabla)\mathbf{v}\right)"
                    r"= -\nabla p + \mu\nabla^2\mathbf{v} + \mathbf{f}",
                    color=WHITE,
                ).scale(0.70)
                eq.move_to(DOWN * 0.3)
                return eq

            elif key == "eq_cd":
                grp = VGroup()
                arr_c = Arrow(LEFT * 2, RIGHT * 0.2, color=C_FLUID,
                              stroke_width=2.5, tip_length=0.22)
                lbl_c = S("Convection", color=C_FLUID, scale=0.46)
                lbl_c.next_to(arr_c, UP, buff=0.12)
                arcs = VGroup(*[
                    Arc(radius=r, start_angle=-PI/2, angle=PI,
                        color=C_CYAN, stroke_width=1.4,
                        stroke_opacity=0.55)
                    for r in [0.35, 0.70, 1.05]
                ]).move_to(RIGHT * 2.5)
                lbl_d = S("Diffusion", color=C_CYAN, scale=0.46)
                lbl_d.next_to(arcs, UP, buff=0.12)
                grp.add(arr_c, lbl_c, arcs, lbl_d)
                grp.move_to(DOWN * 0.4)
                return grp

            elif key == "text_ctrl":
                grp = VGroup()
                wall = Line(LEFT * 3.5, RIGHT * 3.5,
                            stroke_width=2, color=C_SUBTITLE)
                bl = Polygon(
                    LEFT * 3.5 + DOWN * 0.01,
                    RIGHT * 3.5 + DOWN * 0.01,
                    RIGHT * 3.5 + UP * 0.55,
                    LEFT * 3.5 + UP * 0.02,
                    color=C_AMBER, fill_opacity=0.12,
                    stroke_width=1, stroke_opacity=0.5,
                )
                lbl_bl = S("Boundary Layer / Control",
                           color=C_AMBER, scale=0.46)
                lbl_bl.next_to(wall, UP, buff=0.70)
                grp.add(wall, bl, lbl_bl)
                grp.move_to(DOWN * 0.3)
                return grp

        recap_text_pos = UP * 2.65

        for key, txt, col in recap_items:
            vis  = make_recap_visual(key)
            lbl  = T(txt, scale=0.64, color=col).move_to(recap_text_pos)
            self.play(FadeIn(vis, lag_ratio=0.03),
                      FadeIn(lbl, shift=DOWN * 0.08), run_time=1.0)
            self.wait(2.5)
            self.play(FadeOut(vis), FadeOut(lbl), run_time=0.9)
            self.wait(0.15)


        # ══════════════════════════════════════════════════
        # PART 3 · The Equation Returns  (30 – 45 s)
        # ══════════════════════════════════════════════════
        lbl_one = T("One equation…", scale=0.64, color=WHITE)
        lbl_one.move_to(UP * 2.8)

        eq_base = MathTex(
            r"\rho\!\left(\frac{\partial\mathbf{v}}{\partial t}"
            r"+ (\mathbf{v}\cdot\nabla)\mathbf{v}\right)"
            r"= -\nabla p + \mu\nabla^2\mathbf{v} + \mathbf{f}",
            color=WHITE,
        ).scale(0.74)
        eq_base.move_to(UP * 0.3)

        self.play(Write(eq_base), run_time=2.0)
        self.play(FadeIn(lbl_one, shift=DOWN * 0.1), run_time=0.8)
        self.wait(1.5)

        eq_em = MathTex(
            r"\rho\!\left(\frac{\partial\mathbf{v}}{\partial t}"
            r"+ (\mathbf{v}\cdot\nabla)\mathbf{v}\right)"
            r"= -\nabla p + \mu\nabla^2\mathbf{v}"
            r"+ \mathbf{J}\times\mathbf{B}",
            color=WHITE,
        ).scale(0.74)
        eq_em.move_to(UP * 0.3)

        sub_f = S("f  any external force", color=C_SUBTITLE, scale=0.44)
        sub_f.next_to(eq_base, DOWN, buff=0.40)
        self.show(sub_f, rt=0.6)
        self.wait(1.2)
        self.hide(sub_f, rt=0.5)

        self.play(TransformMatchingShapes(eq_base, eq_em,
                                         run_time=1.8, rate_func=smooth))
        self.wait(0.5)

        sub_jb = S("J×B  electromagnetic forcing", color=C_CYAN, scale=0.44)
        sub_jb.next_to(eq_em, DOWN, buff=0.40)
        self.show(sub_jb, rt=0.6)
        self.wait(2.5)

        self.play(FadeOut(lbl_one), FadeOut(sub_jb), FadeOut(eq_em),
                  run_time=1.0)
        self.wait(0.2)


        # ══════════════════════════════════════════════════
        # PART 4 · Scale Expansion  (45 – 60 s)
        # ══════════════════════════════════════════════════
        scales = [
            ("Water",  C_FLUID,                  0.0),
            ("Air",    interpolate_color(ManimColor(C_FLUID),   ManimColor(C_EQ),   0.30), 0.04),
            ("Blood",  interpolate_color(ManimColor(C_AMBER),   ManimColor(C_EQ),   0.30), 0.06),
            ("Plasma", interpolate_color(ManimColor(C_AMBER),   ManimColor(C_EQ),   0.65), 0.12),
            ("Stars",  interpolate_color(ManimColor(C_CYAN),    ManimColor(C_EQ),   0.70), 0.20),
        ]

        lbl_everyday = T("From everyday flow…", scale=0.64, color=WHITE)
        lbl_universe = T("To the universe",      scale=0.72, color=C_CYAN)
        lbl_everyday.move_to(UP * 2.8)
        lbl_universe.move_to(UP * 2.8)

        self.show(lbl_everyday, rt=0.8)

        # Track ALL flow groups added to scene so we can remove every one
        all_flow_groups = []

        current_flow = None
        for i, (name, col, noise) in enumerate(scales):
            new_flow = make_flow(n_rows=5, n_cols=9,
                                 speed=1.0 + i * 0.3,
                                 noise=noise, color=col)
            new_flow.move_to(DOWN * 0.3)
            all_flow_groups.append(new_flow)

            scale_lbl = S(name, color=col, scale=0.50)
            scale_lbl.move_to(DOWN * 1.95)

            if current_flow is None:
                self.play(FadeIn(new_flow, lag_ratio=0.03),
                          FadeIn(scale_lbl), run_time=1.0)
            else:
                # ReplacementTransform replaces old with new cleanly in scene
                self.play(ReplacementTransform(current_flow, new_flow,
                                               rate_func=smooth),
                          FadeIn(scale_lbl), run_time=1.2)

            self.wait(0.55)
            self.play(FadeOut(scale_lbl), run_time=0.3)
            current_flow = new_flow

        self.swap_text(lbl_everyday, lbl_universe)
        self.wait(2.0)

        # ── Hard-remove ALL arrows from scene before ANY text appears ──
        # Use self.remove() to guarantee nothing lingers, then clear screen
        self.play(FadeOut(current_flow), FadeOut(lbl_universe), run_time=0.8)
        # Safety: remove every flow object directly from scene mobjects
        for fg in all_flow_groups:
            self.remove(fg)
        self.wait(0.4)


        # ══════════════════════════════════════════════════
        # PART 5 · Conclusion  (60 – 70 s)
        # Screen is CLEAR — no arrows behind text
        # ══════════════════════════════════════════════════
        conclusions = [
            ("Fluid motion is governed by the balance of forces",       WHITE,      0.62),
            ("Convection, diffusion, pressure, and external effects\ndefine behavior",
                                                                         C_SUBTITLE, 0.52),
            ("Through approximation, we make complex systems solvable", C_CYAN,     0.58),
            ("This equation connects engineering, physics,\nand the universe",
                                                                         WHITE,      0.60),
        ]

        for txt, col, sc in conclusions:
            mob = Text(txt, font="Georgia", color=col,
                       line_spacing=1.4).scale(sc)
            mob.move_to(ORIGIN)
            self.play(FadeIn(mob, shift=UP * 0.12), run_time=0.9)
            self.wait(2.0)
            self.play(FadeOut(mob, shift=UP * 0.12), run_time=0.7)
            self.wait(0.15)


        # ══════════════════════════════════════════════════
        # PART 6 · Outcome / Learning List  (70 – 80 s)
        # Clean dark screen — no arrows, outcomes visible
        # ══════════════════════════════════════════════════
        outcome_hdr = T("After this journey, we understand:",
                        scale=0.60, color=WHITE)
        outcome_hdr.to_edge(UP, buff=0.55)
        self.show(outcome_hdr, rt=0.8)

        outcomes = [
            "What a fluid is",
            "How flow is described mathematically",
            "Meaning of the Navier–Stokes equation",
            "Role of convection and diffusion",
            "Importance of the boundary layer",
            "Real-world applications",
            "Extension to electromagnetic systems",
            "Instability and complex behavior",
        ]

        col_left  = outcomes[:4]
        col_right = outcomes[4:]

        def bullet_col(items, x_anchor, color=C_CREDIT):
            grp = VGroup()
            for item in items:
                dot = Dot(radius=0.055, color=C_CYAN).set_opacity(0.9)
                txt = S("  " + item, scale=0.43, color=color)
                row = VGroup(dot, txt).arrange(RIGHT, buff=0.08)
                grp.add(row)
            grp.arrange(DOWN, aligned_edge=LEFT, buff=0.26)
            grp.move_to(np.array([x_anchor, -0.20, 0]))
            return grp

        left_col  = bullet_col(col_left,  -2.8)
        right_col = bullet_col(col_right,  2.2)

        self.play(
            FadeIn(left_col,  lag_ratio=0.28, shift=RIGHT * 0.1),
            FadeIn(right_col, lag_ratio=0.28, shift=RIGHT * 0.1),
            run_time=2.2,
        )
        self.wait(4.5)

        self.play(FadeOut(outcome_hdr),
                  FadeOut(left_col), FadeOut(right_col), run_time=1.0)
        self.wait(0.2)


        # ══════════════════════════════════════════════════
        # PART 7 · Final Statement  (80 – 86 s)
        # ══════════════════════════════════════════════════
        title_eq = BIG("Navier–Stokes Equation", scale=0.88, color=WHITE)
        title_eq.move_to(UP * 0.5)

        self.play(FadeIn(title_eq, shift=UP * 0.2), run_time=1.2)
        self.wait(2.2)

        tagline = BIG("One equation.  Infinite phenomena.",
                      scale=0.62, color=C_CYAN)
        tagline.next_to(title_eq, DOWN, buff=0.50)

        self.play(FadeIn(tagline, shift=UP * 0.15), run_time=1.0)
        self.wait(2.8)

        self.play(
            title_eq.animate.scale(0.85).set_opacity(0.0),
            tagline.animate.scale(0.85).set_opacity(0.0),
            run_time=1.4, rate_func=smooth,
        )
        self.wait(0.3)


        # ══════════════════════════════════════════════════
        # PART 8 · Credits  (86 – 100 s)
        # Creative: particle burst → radial lines → card reveal
        # ══════════════════════════════════════════════════

        # ── 1. Particle burst from centre ──
        NUM_SPARKS = 28
        sparks = VGroup()
        for k in range(NUM_SPARKS):
            angle   = k * TAU / NUM_SPARKS
            length  = np.random.default_rng(k).uniform(1.2, 3.8)
            end_pt  = np.array([np.cos(angle) * length,
                                 np.sin(angle) * length, 0])
            spark = Line(ORIGIN, end_pt * 0.05,
                         stroke_width=1.2,
                         stroke_opacity=0.0,
                         color=C_CYAN)
            sparks.add(spark)
        self.add(sparks)

        # animate sparks shooting outward
        self.play(
            *[sparks[k].animate
                .put_start_and_end_on(ORIGIN,
                    np.array([np.cos(k * TAU / NUM_SPARKS),
                              np.sin(k * TAU / NUM_SPARKS), 0])
                    * np.random.default_rng(k).uniform(1.2, 3.8))
                .set_stroke(opacity=0.55)
              for k in range(NUM_SPARKS)],
            run_time=0.9, rate_func=rush_into,
        )

        # fade sparks as rings pulse in
        rings = VGroup(*[
            Circle(radius=r, color=C_CYAN,
                   stroke_width=1.0 - r * 0.12,
                   stroke_opacity=0.0)
            for r in [0.6, 1.3, 2.1, 3.2]
        ])
        self.add(rings)
        self.play(
            FadeOut(sparks, run_time=0.7),
            *[rings[i].animate.set_stroke(opacity=0.18 - i * 0.03)
              for i in range(4)],
            run_time=0.8,
        )

        # ── 2. Animated equation dissolves into "Thank You" ──
        eq_ghost = MathTex(
            r"\rho\!\left(\frac{\partial\mathbf{v}}{\partial t}"
            r"+ (\mathbf{v}\cdot\nabla)\mathbf{v}\right)"
            r"= -\nabla p + \mu\nabla^2\mathbf{v} + \mathbf{f}",
            color=C_CYAN,
        ).scale(0.60).set_opacity(0.28)
        eq_ghost.move_to(ORIGIN)
        self.play(FadeIn(eq_ghost), run_time=0.5)

        # "Thank You" rises through the equation
        thank_you = Text("Thank You", font="Georgia",
                         color=WHITE).scale(1.40)
        thank_you.move_to(DOWN * 2.5)
        self.play(
            thank_you.animate.move_to(ORIGIN + UP * 0.1),
            FadeOut(eq_ghost),
            rate_func=smooth, run_time=1.4,
        )

        # colour sweep: white → cyan gradient shimmer effect
        self.play(
            thank_you.animate.set_color(C_CYAN).scale(1.05),
            rate_func=there_and_back, run_time=0.9,
        )
        self.wait(0.4)

        # ── 3. "Thank You" drifts up; geometric card assembles below ──
        self.play(
            thank_you.animate.move_to(UP * 2.65).scale(0.58),
            rate_func=smooth, run_time=1.0,
        )

        # Decorative corner accents (L-shaped brackets)
        def corner_accent(direction_x, direction_y, color=C_CYAN):
            size = 0.30
            h = Line(ORIGIN, RIGHT * direction_x * size,
                     stroke_width=1.6, color=color).set_opacity(0.7)
            v = Line(ORIGIN, UP * direction_y * size,
                     stroke_width=1.6, color=color).set_opacity(0.7)
            return VGroup(h, v)

        card_w, card_h = 5.8, 3.6
        card_rect = RoundedRectangle(
            width=card_w, height=card_h,
            corner_radius=0.18,
            stroke_color=C_CYAN, stroke_width=0.9,
            stroke_opacity=0.30, fill_opacity=0.0,
        ).move_to(DOWN * 0.3)

        # four bracket corners
        tl = corner_accent( 1,  1).move_to(card_rect.get_corner(UL) + RIGHT*0.15 + DOWN*0.15)
        tr = corner_accent(-1,  1).move_to(card_rect.get_corner(UR) + LEFT*0.15  + DOWN*0.15)
        bl = corner_accent( 1, -1).move_to(card_rect.get_corner(DL) + RIGHT*0.15 + UP*0.15)
        br = corner_accent(-1, -1).move_to(card_rect.get_corner(DR) + LEFT*0.15  + UP*0.15)
        corners = VGroup(tl, tr, bl, br)

        self.play(
            Create(card_rect, run_time=0.9),
            FadeIn(corners, run_time=0.6),
        )

        # glowing divider
        rule_l   = Line(LEFT * 0.1, LEFT * 2.0,
                        stroke_width=0.9, color=C_CYAN).set_opacity(0.55)
        rule_r   = Line(RIGHT * 0.1, RIGHT * 2.0,
                        stroke_width=0.9, color=C_CYAN).set_opacity(0.55)
        rule_dot = Dot(radius=0.060, color=C_CYAN).set_opacity(1.0)
        rule_grp = VGroup(rule_l, rule_dot, rule_r)
        rule_grp.move_to(UP * 2.10)
        self.play(Create(rule_l), Create(rule_r),
                  FadeIn(rule_dot), run_time=0.6)

        # ── 4. Content inside card ── staggered fade-in ──
        presented = S("presented by", scale=0.38, color=C_SUBTITLE)
        presented.move_to(UP * 1.55)
        self.play(FadeIn(presented, shift=UP * 0.07), run_time=0.45)

        # Author with subtle underline
        author = Text("Sushrut Kale", font="Georgia",
                      color=WHITE).scale(0.76)
        author.move_to(UP * 0.95)
        author_line = Line(
            author.get_left() + DOWN * 0.06,
            author.get_right() + DOWN * 0.06,
            stroke_width=0.8, color=C_CYAN,
        ).set_opacity(0.45)
        self.play(FadeIn(author, shift=UP * 0.10), run_time=0.65)
        self.play(Create(author_line), run_time=0.40)

        # Club in cyan with small decorative dots flanking
        club_dot_l = Dot(radius=0.04, color=C_CYAN).set_opacity(0.7)
        club_dot_r = Dot(radius=0.04, color=C_CYAN).set_opacity(0.7)
        club_txt   = Text("Vertex GDNA Club", font="Georgia",
                          color=C_CYAN).scale(0.48)
        club_grp   = VGroup(club_dot_l, club_txt, club_dot_r).arrange(RIGHT, buff=0.18)
        club_grp.next_to(author, DOWN, buff=0.25)
        self.play(FadeIn(club_grp, shift=UP * 0.08), run_time=0.55)

        # thin rule
        rule2 = Line(LEFT * 1.6, RIGHT * 1.6,
                     stroke_width=0.6, color=C_SUBTITLE).set_opacity(0.28)
        rule2.next_to(club_grp, DOWN, buff=0.28)
        self.play(Create(rule2), run_time=0.40)

        # Guidance block
        guidance_hdr = S("under the guidance of", scale=0.38, color=C_SUBTITLE)
        guidance_hdr.next_to(rule2, DOWN, buff=0.20)

        guide1 = S("Prof. Priti Shinde Ma'am", scale=0.46, color=C_CREDIT)
        guide2 = S("Prof. Azhar Shaikh Sir",   scale=0.46, color=C_CREDIT)
        guide1.next_to(guidance_hdr, DOWN, buff=0.16)
        guide2.next_to(guide1,       DOWN, buff=0.13)

        self.play(FadeIn(guidance_hdr, shift=UP * 0.07), run_time=0.45)
        self.play(FadeIn(guide1, shift=UP * 0.07), run_time=0.50)
        self.play(FadeIn(guide2, shift=UP * 0.07), run_time=0.50)

        self.wait(3.5)

        # ── 5. Creative exit: card collapses inward + sparks flicker out ──
        exit_sparks = VGroup(*[
            Line(
                np.array([np.cos(k * TAU / 16), np.sin(k * TAU / 16), 0]) * 3.0,
                np.array([np.cos(k * TAU / 16), np.sin(k * TAU / 16), 0]) * 3.4,
                stroke_width=0.8, color=C_CYAN, stroke_opacity=0.25,
            )
            for k in range(16)
        ])
        self.add(exit_sparks)

        all_credits = VGroup(
            rings, thank_you, rule_grp, rule2, card_rect, corners,
            presented, author, author_line, club_grp,
            guidance_hdr, guide1, guide2,
        )

        self.play(
            all_credits.animate.scale(0.05).set_opacity(0.0),
            FadeOut(exit_sparks),
            run_time=1.8, rate_func=smooth,
        )
        self.wait(0.5)