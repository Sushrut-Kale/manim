
from manim import *
import numpy as np


# ─────────────────────────────────────────────────────────
#  Colour palette
# ─────────────────────────────────────────────────────────
C_BG       = "#04060E"   # deep cinematic dark
C_STABLE   = "#3A9EDB"   # blue   – stable flow
C_ENERGY   = "#F5A623"   # amber  – energy input
C_DISSIP   = "#3DD9A4"   # teal   – dissipation
C_UNSTABLE = "#E84545"   # red    – instability
C_PLASMA   = "#FFFFFF"   # white  – plasma / titles
C_SUBTITLE = "#8FA8C0"   # muted steel-blue subtitles
C_DIM      = "#2A3A4A"   # dimmed colour for equation rest


# ─────────────────────────────────────────────────────────
#  Helper: grid of flow arrows
# ─────────────────────────────────────────────────────────
def make_flow_arrows(
    n_rows=5, n_cols=9,
    x_range=(-5.5, 5.5), y_range=(-1.4, 1.4),
    speed=1.0, noise=0.0,
    color=C_STABLE, tip_scale=0.22,
) -> VGroup:
    arrows = VGroup()
    xs  = np.linspace(*x_range, n_cols)
    ys  = np.linspace(*y_range, n_rows)
    rng = np.random.default_rng(42)
    for y in ys:
        for x in xs:
            dy = rng.uniform(-noise, noise)
            dx = speed + rng.uniform(-noise * 0.3, noise * 0.3)
            length    = np.hypot(dx, dy) * 0.55
            direction = np.array([dx, dy, 0]) / (np.hypot(dx, dy) + 1e-9)
            arr = Arrow(
                start=np.array([x, y, 0]),
                end=np.array([x, y, 0]) + direction * length,
                buff=0,
                stroke_width=1.6,
                max_tip_length_to_length_ratio=0.28,
                tip_length=tip_scale,
                color=color,
            ).set_opacity(0.78)
            arrows.add(arr)
    return arrows


# ─────────────────────────────────────────────────────────
#  Helper: vortex ring
# ─────────────────────────────────────────────────────────
def make_vortex(center=ORIGIN, radius=1.2, n=18,
                color=C_UNSTABLE, strength=1.0) -> VGroup:
    group = VGroup()
    for i in range(n):
        theta  = 2 * PI * i / n
        x      = center[0] + radius * np.cos(theta)
        y      = center[1] + radius * np.sin(theta)
        tx     = -np.sin(theta) * strength
        ty     =  np.cos(theta) * strength
        length = 0.4 * strength
        arr = Arrow(
            start=np.array([x, y, 0]),
            end=np.array([x + tx * length, y + ty * length, 0]),
            buff=0, stroke_width=1.8, tip_length=0.18, color=color,
        ).set_opacity(0.88)
        group.add(arr)
    return group


# ─────────────────────────────────────────────────────────
#  Text helpers
# ─────────────────────────────────────────────────────────
def H(text, scale=0.70, color=WHITE):
    """Heading text in Georgia serif."""
    return Text(text, font="Georgia", color=color).scale(scale)

def S(text, scale=0.46, color=C_SUBTITLE):
    """Subtitle text in Georgia serif."""
    return Text(text, font="Georgia", color=color).scale(scale)


# ─────────────────────────────────────────────────────────
#  Main Scene
# ─────────────────────────────────────────────────────────
class Scene13_Instability(Scene):

    def setup(self):
        self.camera.background_color = C_BG

    # ── convenience wrappers ─────────────────────────────
    def show(self, mob, rt=0.7, **kw):
        self.play(FadeIn(mob, **kw), run_time=rt)

    def hide(self, mob, rt=0.55, **kw):
        self.play(FadeOut(mob, **kw), run_time=rt)

    def swap(self, old, new, pos=UP * 3.15, rt=0.75):
        """Crossfade one label for another at the same position."""
        new.move_to(pos)
        self.play(
            FadeOut(old, shift=UP * 0.12),
            FadeIn(new,  shift=UP * 0.12),
            run_time=rt,
        )

    # ─────────────────────────────────────────────────────
    def construct(self):

        # ══════════════════════════════════════════════════
        # INTRO  (0 – 8 s) — Title card
        # ══════════════════════════════════════════════════
        title1 = H("Instability & Blow-up", scale=0.92, color=WHITE)
        title2 = H("Energy vs Dissipation",  scale=0.62, color=C_SUBTITLE)
        title1.move_to(UP * 0.40)
        title2.next_to(title1, DOWN, buff=0.20)

        rule = Line(LEFT * 3.0, RIGHT * 3.0,
                    stroke_width=0.8, color=C_SUBTITLE).set_opacity(0.35)
        rule.next_to(title2, DOWN, buff=0.26)

        tagline = S("How fluids transition from calm to chaotic",
                    scale=0.43, color=C_SUBTITLE)
        tagline.next_to(rule, DOWN, buff=0.22)

        self.play(FadeIn(title1,   shift=UP    * 0.2),  run_time=1.2)
        self.play(FadeIn(title2, shift=UP * 0.1),
                  Create(rule),                          run_time=0.9)
        self.play(FadeIn(tagline, shift=UP * 0.1),       run_time=0.8)
        self.wait(2.8)

        self.play(
            FadeOut(title1),
            FadeOut(title2),    FadeOut(rule),
            FadeOut(tagline),
            run_time=1.0,
        )
        self.wait(0.3)


        # ══════════════════════════════════════════════════
        # PART 1 · Stable Flow  (8 – 18 s)
        # ══════════════════════════════════════════════════
        lbl = H("Flow can remain stable", color=C_STABLE)
        lbl.to_edge(UP, buff=0.45)

        flow = make_flow_arrows(speed=1.0, noise=0.0, color=C_STABLE)
        flow.shift(DOWN * 0.3)

        self.play(FadeIn(flow, lag_ratio=0.03), run_time=1.4)
        self.show(lbl)
        self.wait(0.8)
        # gentle rightward drift — laminar advection
        self.play(flow.animate.shift(RIGHT * 0.5).set_opacity(0.88),
                  rate_func=smooth, run_time=3.2)
        self.wait(1.5)


        # ══════════════════════════════════════════════════
        # PART 2 · Energy Input  (18 – 32 s)
        # ══════════════════════════════════════════════════
        lbl2 = H("Energy is added to the system", color=C_ENERGY)
        lbl2.to_edge(UP, buff=0.45)
        self.swap(lbl, lbl2); lbl = lbl2

        # external forcing arrows on left edge
        force = VGroup(*[
            Arrow(np.array([-6.8, y, 0]), np.array([-5.5, y, 0]),
                  buff=0, stroke_width=2.4, tip_length=0.22,
                  color=C_ENERGY).set_opacity(0.9)
            for y in [-1.1, 0.0, 1.1]
        ])
        flow_e = make_flow_arrows(speed=1.7, noise=0.12, color=C_ENERGY)
        flow_e.shift(DOWN * 0.3 + RIGHT * 0.5)

        self.play(Transform(flow, flow_e, rate_func=smooth),
                  FadeIn(force, shift=RIGHT * 0.25), run_time=2.0)
        self.wait(1.2)

        flow_e2 = make_flow_arrows(speed=2.1, noise=0.20, color=C_ENERGY)
        flow_e2.shift(DOWN * 0.3 + RIGHT * 0.5)
        self.play(Transform(flow, flow_e2, rate_func=smooth), run_time=2.2)
        self.wait(1.8)
        self.hide(force)


        # ══════════════════════════════════════════════════
        # PART 3 · Dissipation  (32 – 46 s)
        # ══════════════════════════════════════════════════
        lbl3 = H("Viscosity removes energy", color=C_DISSIP)
        lbl3.to_edge(UP, buff=0.45)
        self.swap(lbl, lbl3); lbl = lbl3

        sub3 = S("Dissipation = loss of motion into heat", color=C_DISSIP)
        sub3.next_to(lbl, DOWN, buff=0.20)
        self.show(sub3)

        flow_d = make_flow_arrows(speed=1.0, noise=0.04, color=C_DISSIP)
        flow_d.shift(DOWN * 0.3 + RIGHT * 0.5)
        self.play(Transform(flow, flow_d, rate_func=smooth), run_time=3.2)
        self.wait(3.0)
        self.hide(sub3)


        # ══════════════════════════════════════════════════
        # PART 4 · Balance  (46 – 60 s)
        # ══════════════════════════════════════════════════
        lbl4 = H("Energy input  ≈  Dissipation", color=WHITE)
        lbl4.to_edge(UP, buff=0.45)
        self.swap(lbl, lbl4); lbl = lbl4

        sub4 = S("System stays stable", color=C_SUBTITLE)
        sub4.next_to(lbl, DOWN, buff=0.20)
        self.show(sub4)

        mid_color = interpolate_color(
            ManimColor(C_STABLE), ManimColor(C_DISSIP), 0.4)
        flow_b = make_flow_arrows(speed=1.3, noise=0.06, color=mid_color)
        flow_b.shift(DOWN * 0.3 + RIGHT * 0.5)
        self.play(Transform(flow, flow_b, rate_func=smooth), run_time=2.2)
        self.wait(5.0)
        self.hide(sub4)


        # ══════════════════════════════════════════════════
        # PART 5 · Instability Onset  (60 – 74 s)
        # ══════════════════════════════════════════════════
        lbl5 = H("Energy input  >  Dissipation", color=C_ENERGY)
        lbl5.to_edge(UP, buff=0.45)
        self.swap(lbl, lbl5); lbl = lbl5

        sub5 = S("Disturbances start growing", color=C_SUBTITLE)
        sub5.next_to(lbl, DOWN, buff=0.20)
        self.show(sub5)

        for noise_level, spd in [(0.25, 1.8), (0.52, 2.3), (0.88, 2.9)]:
            alpha  = noise_level / 0.88
            col    = interpolate_color(
                ManimColor(C_ENERGY), ManimColor(C_UNSTABLE), alpha)
            flow_u = make_flow_arrows(n_rows=6, n_cols=10,
                                      speed=spd, noise=noise_level, color=col)
            flow_u.shift(DOWN * 0.3 + RIGHT * 0.5)
            self.play(Transform(flow, flow_u, rate_func=smooth), run_time=1.8)
            self.wait(0.4)

        self.wait(1.2)
        self.hide(sub5)


        # ══════════════════════════════════════════════════
        # PART 6 · Blow-up  (74 – 88 s)
        # ══════════════════════════════════════════════════
        lbl6 = H("Rapid growth of motion", color=C_UNSTABLE)
        lbl6.to_edge(UP, buff=0.45)
        self.swap(lbl, lbl6); lbl = lbl6

        sub6 = S("Blow-up = instability, not necessarily explosion",
                  color=C_SUBTITLE)
        sub6.next_to(lbl, DOWN, buff=0.20)
        self.show(sub6)

        v_col_r = interpolate_color(
            ManimColor(C_UNSTABLE), ManimColor(C_ENERGY), 0.45)
        vL = make_vortex(LEFT  * 2.8, radius=1.1, n=18,
                         color=C_UNSTABLE, strength=1.3)
        vR = make_vortex(RIGHT * 2.6, radius=1.0, n=18,
                         color=v_col_r,    strength=1.1)
        vC = make_vortex(DOWN  * 0.3, radius=0.7, n=14,
                         color=C_ENERGY,   strength=0.9)

        self.play(FadeOut(flow),
                  FadeIn(vL, lag_ratio=0.04),
                  FadeIn(vR, lag_ratio=0.04),
                  FadeIn(vC, lag_ratio=0.04), run_time=1.8)

        self.play(
            vL.animate.scale(1.18).set_opacity(1.0),
            vR.animate.scale(1.15).set_opacity(1.0),
            vC.animate.scale(1.25).set_opacity(1.0),
            rate_func=there_and_back_with_pause,
            run_time=3.5,
        )
        self.wait(1.8)
        self.hide(sub6)
        self.play(FadeOut(vL), FadeOut(vR), FadeOut(vC), run_time=0.9)
        self.hide(lbl)


        # ══════════════════════════════════════════════════
        # PART 7 · Equation  (88 – 104 s)
        # ══════════════════════════════════════════════════
        #
        #  KEY FIX: split the equation into 5 SEPARATE substrings.
        #  Each substring becomes eq[0], eq[1] … eq[4].
        #  We colour / box them by index — zero ambiguity, zero white squares.
        #
        #  eq[0]  →  ρ (∂v/∂t
        #  eq[1]  →  + (v·∇)v )       ← nonlinear term
        #  eq[2]  →  = −∇p
        #  eq[3]  →  + μ∇²v            ← dissipation term
        #  eq[4]  →  + J × B           ← EM forcing term

        eq = MathTex(
            r"\rho \!\left(\frac{\partial \mathbf{v}}{\partial t}",   # [0]
            r"+ (\mathbf{v}\cdot\nabla)\mathbf{v} \right)",           # [1]
            r"= -\nabla p",                                            # [2]
            r"+ \mu \nabla^2 \!\mathbf{v}",                           # [3]
            r"+ \mathbf{J} \times \mathbf{B}",                        # [4]
            color=WHITE,
        ).scale(0.76)
        eq.move_to(UP * 0.5)

        eq_title = H("The Navier–Stokes Equation", scale=0.60, color=WHITE)
        eq_title.to_edge(UP, buff=0.45)

        self.show(eq_title)
        self.play(Write(eq), run_time=2.2)
        self.wait(0.6)

        # ── highlight helper ─────────────────────────────
        def highlight_term(part_idx, hi_color, label_text, label_above=False):
            """
            Dim all other parts, highlight part_idx,
            draw a clean box, show label, then restore everything.
            No index numbers ever shown.
            """
            # Step 1: dim rest, brighten target
            dim_anims = [
                eq[i].animate.set_color(C_DIM)
                for i in range(5) if i != part_idx
            ]
            self.play(*dim_anims,
                      eq[part_idx].animate.set_color(hi_color),
                      run_time=0.65)

            # Step 2: bounding box (SurroundingRectangle on the VGroup part)
            box = SurroundingRectangle(
                eq[part_idx],
                color=hi_color,
                buff=0.10,
                stroke_width=2.2,
                corner_radius=0.06,
            )

            # Step 3: label placed clear of the box
            lbl_eq = S(label_text, color=hi_color, scale=0.47)
            if label_above:
                lbl_eq.next_to(box, UP,   buff=0.20)
            else:
                lbl_eq.next_to(box, DOWN, buff=0.20)

            self.play(Create(box),
                      FadeIn(lbl_eq, shift=UP * 0.08),
                      run_time=0.80)
            self.wait(1.8)

            # Step 4: remove box and label, restore all to white
            self.play(FadeOut(box), FadeOut(lbl_eq), run_time=0.45)
            self.play(
                *[eq[i].animate.set_color(WHITE) for i in range(5)],
                run_time=0.45,
            )
            self.wait(0.3)

        # Highlight each term in sequence
        highlight_term(1, C_UNSTABLE, "nonlinear growth")
        highlight_term(3, C_DISSIP,   "dissipation / viscosity")
        highlight_term(4, C_ENERGY,   "J×B  —  electromagnetic energy input")

        # Summary line
        summary = S(
            "Instability arises from imbalance of these three effects",
            color=C_SUBTITLE, scale=0.47,
        )
        summary.next_to(eq, DOWN, buff=0.50)
        self.play(FadeIn(summary, shift=UP * 0.1), run_time=0.8)
        self.wait(2.2)

        self.play(FadeOut(eq), FadeOut(summary), FadeOut(eq_title),
                  run_time=1.0)


        # ══════════════════════════════════════════════════
        # PART 8 · Astrophysical Extension  (104 – 112 s)
        # ══════════════════════════════════════════════════
        lbl_a = H("In extreme systems like stars…", color=C_PLASMA)
        lbl_a.to_edge(UP, buff=0.45)
        self.show(lbl_a)

        plasma_col = interpolate_color(
            ManimColor(C_ENERGY), ManimColor(C_PLASMA), 0.60)
        plasma = make_flow_arrows(n_rows=6, n_cols=10,
                                  speed=2.6, noise=0.58,
                                  color=plasma_col, tip_scale=0.20)
        plasma.shift(DOWN * 0.4)

        arc_col = interpolate_color(
            ManimColor(C_ENERGY), ManimColor(C_PLASMA), 0.50)
        arcs = VGroup(*[
            Arc(radius=r, start_angle=PI * 0.1, angle=PI * 0.8,
                color=arc_col, stroke_width=1.2,
                stroke_opacity=0.40).shift(DOWN * 0.4)
            for r in [0.85, 1.5, 2.2, 3.0]
        ])

        self.play(FadeIn(plasma, lag_ratio=0.02),
                  FadeIn(arcs,  lag_ratio=0.10), run_time=1.5)

        sub_a = S("Energy release leads to powerful phenomena",
                  color=C_SUBTITLE)
        sub_a.next_to(lbl_a, DOWN, buff=0.20)
        self.show(sub_a)
        self.wait(0.8)

        lbl_final = H("Same physics — different scale",
                      color=C_PLASMA, scale=0.76)
        lbl_final.to_edge(DOWN, buff=0.65)
        self.play(FadeIn(lbl_final, shift=UP * 0.15), run_time=1.0)
        self.wait(2.8)

        # Clean fade-out
        self.play(
            FadeOut(lbl_a), FadeOut(sub_a),
            FadeOut(plasma), FadeOut(arcs),
            FadeOut(lbl_final),
            run_time=1.8,
        )
        self.wait(0.4)