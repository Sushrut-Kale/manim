
from manim import *
import numpy as np


# ─────────────────────────────────────────────
#  GLOBAL PALETTE
# ─────────────────────────────────────────────
FLUID_BASE       = "#1A3A6E"
FLUID_HIGHLIGHT  = "#2B6CB0"
PATCH_COLOR      = "#E53E3E"          # red blob
CONV_COLOR       = "#FF4500"          # convection / "bad guy"
DIFF_COLOR       = "#00CED1"          # diffusion / "good guy"
BG_COLOR         = "#0A0A12"          # near-black cinematic bg
TEXT_COLOR       = WHITE
LABEL_CONV       = "#FF6B35"
LABEL_DIFF       = "#48BB78"


# ─────────────────────────────────────────────
#  HELPER: Glow-outline stick figure
# ─────────────────────────────────────────────
def make_stick_figure(color: str, scale: float = 1.0) -> VGroup:
    """
    Minimal glowing-outline stick figure built from VMobject primitives.
    color  – glow / stroke color
    scale  – overall scale multiplier
    """
    stroke_w = 3

    # Head (circle)
    head = Circle(radius=0.18, stroke_color=color, stroke_width=stroke_w,
                  fill_opacity=0)

    # Torso
    torso = Line(ORIGIN, DOWN * 0.55, stroke_color=color, stroke_width=stroke_w)

    # Arms – slightly angled
    arm_l = Line(ORIGIN + LEFT  * 0.25 + UP * 0.08,
                 ORIGIN + LEFT  * 0.55 + DOWN * 0.2,
                 stroke_color=color, stroke_width=stroke_w)
    arm_r = Line(ORIGIN + RIGHT * 0.25 + UP * 0.08,
                 ORIGIN + RIGHT * 0.55 + DOWN * 0.2,
                 stroke_color=color, stroke_width=stroke_w)

    # Legs
    leg_l = Line(ORIGIN + DOWN * 0.55,
                 ORIGIN + LEFT  * 0.3 + DOWN * 1.0,
                 stroke_color=color, stroke_width=stroke_w)
    leg_r = Line(ORIGIN + DOWN * 0.55,
                 ORIGIN + RIGHT * 0.3 + DOWN * 1.0,
                 stroke_color=color, stroke_width=stroke_w)

    # Assemble – shift so feet are at origin, head is up
    parts = VGroup(head, torso, arm_l, arm_r, leg_l, leg_r)
    # centre = head + torso span ≈ 1.18 in height; place head at top
    head.move_to(ORIGIN + UP * 0.18)
    torso.put_start_and_end_on(ORIGIN, DOWN * 0.55)
    arm_l.put_start_and_end_on(LEFT  * 0.22 + DOWN * 0.12,
                               LEFT  * 0.52 + DOWN * 0.38)
    arm_r.put_start_and_end_on(RIGHT * 0.22 + DOWN * 0.12,
                               RIGHT * 0.52 + DOWN * 0.38)
    leg_l.put_start_and_end_on(DOWN * 0.55, LEFT  * 0.28 + DOWN * 1.0)
    leg_r.put_start_and_end_on(DOWN * 0.55, RIGHT * 0.28 + DOWN * 1.0)

    fig = VGroup(head, torso, arm_l, arm_r, leg_l, leg_r)
    fig.scale(scale)
    return fig


# ─────────────────────────────────────────────
#  HELPER: Fluid streamlines
# ─────────────────────────────────────────────
def make_streamlines(n_lines: int = 7,
                     x_range: tuple = (-7, 7),
                     y_spread: float = 2.5,
                     color: str = FLUID_HIGHLIGHT,
                     opacity: float = 0.55) -> VGroup:
    """Horizontal sinusoidal streamlines to simulate laminar flow."""
    lines = VGroup()
    ys = np.linspace(-y_spread, y_spread, n_lines)
    for y in ys:
        pts = [np.array([x, y + 0.08 * np.sin(2 * x + y), 0])
               for x in np.linspace(x_range[0], x_range[1], 120)]
        path = VMobject(stroke_color=color, stroke_width=1.4,
                        stroke_opacity=opacity)
        path.set_points_smoothly(pts)
        lines.add(path)
    return lines


def make_chaotic_streamlines(n_lines: int = 7,
                              x_range: tuple = (-7, 7),
                              color: str = CONV_COLOR,
                              opacity: float = 0.6) -> VGroup:
    """Wavy, distorted streamlines for convection-dominated region."""
    lines = VGroup()
    ys = np.linspace(-2.5, 2.5, n_lines)
    for i, y in enumerate(ys):
        phase = i * 0.8
        pts = [np.array([x,
                         y + 0.45 * np.sin(1.8 * x + phase)
                           + 0.20 * np.cos(3.5 * x - phase),
                         0])
               for x in np.linspace(x_range[0], x_range[1], 180)]
        path = VMobject(stroke_color=color, stroke_width=1.6,
                        stroke_opacity=opacity)
        path.set_points_smoothly(pts)
        lines.add(path)
    return lines


def make_smooth_streamlines(n_lines: int = 7,
                             x_range: tuple = (-7, 7),
                             color: str = DIFF_COLOR,
                             opacity: float = 0.6) -> VGroup:
    """Nearly flat streamlines for diffusion-dominated region."""
    lines = VGroup()
    ys = np.linspace(-2.5, 2.5, n_lines)
    for y in ys:
        pts = [np.array([x, y + 0.02 * np.sin(0.4 * x), 0])
               for x in np.linspace(x_range[0], x_range[1], 80)]
        path = VMobject(stroke_color=color, stroke_width=1.6,
                        stroke_opacity=opacity)
        path.set_points_smoothly(pts)
        lines.add(path)
    return lines


# ─────────────────────────────────────────────
#  HELPER: Colored patch (blob)
# ─────────────────────────────────────────────
def make_patch(color: str = PATCH_COLOR, opacity: float = 0.75) -> Ellipse:
    blob = Ellipse(width=1.2, height=0.7,
                   fill_color=color, fill_opacity=opacity,
                   stroke_width=0)
    return blob


# ─────────────────────────────────────────────
#  HELPER: Arrow clusters simulating push
# ─────────────────────────────────────────────
def make_push_arrows(origin, direction, n=5,
                     color=CONV_COLOR, spread=0.4) -> VGroup:
    arrows = VGroup()
    for i in range(n):
        offset = np.array([0, (i - n // 2) * spread, 0])
        arr = Arrow(start=origin + offset,
                    end=origin + offset + direction,
                    buff=0, stroke_color=color,
                    stroke_width=2, tip_length=0.18,
                    max_stroke_width_to_length_ratio=999)
        arr.set_color(color)
        arrows.add(arr)
    return arrows


# ─────────────────────────────────────────────
#  MAIN SCENE
# ─────────────────────────────────────────────
class Scene8_ConvectionDiffusionBattle(Scene):
    """
    Scene 8 – Convection vs Diffusion: The Visual Battle
    Duration: ~80 seconds
    """

    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── RUN ALL PARTS ──────────────────────────────────────────────
        self.part1_neutral_flow()       #  0 – 10 s
        self.part2_convection_entry()   # 10 – 25 s
        self.part3_diffusion_entry()    # 25 – 45 s
        self.part4_battle_sequence()    # 45 – 65 s
        self.part5_outcome()            # 65 – 80 s
        self.part6_transition()         # 80 – 85 s

    # ══════════════════════════════════════════════════════════════════
    # PART 1 — Neutral Flow  (0–10 s)
    # ══════════════════════════════════════════════════════════════════
    def part1_neutral_flow(self):
        """Establish calm laminar flow with a red patch."""

        # --- Streamlines ---
        streams = make_streamlines(n_lines=9, opacity=0.5)

        # --- Patch ---
        patch = make_patch()
        patch.move_to(LEFT * 3.5)

        # --- Title text ---
        title = Text("Inside every flow, two effects compete",
                     font_size=30, color=TEXT_COLOR,
                     font="Georgia")
        title.to_edge(UP, buff=0.5)

        # Animate
        self.play(Create(streams, run_time=2, rate_func=smooth))
        self.play(FadeIn(patch, scale=0.5, run_time=1))
        self.play(FadeIn(title, run_time=1))

        # Drift patch rightward slowly — baseline flow
        self.play(patch.animate.shift(RIGHT * 1.5),
                  run_time=3, rate_func=smooth)

        self.wait(1)

        # Store for handoff
        self._streams_base = streams
        self._patch        = patch
        self._title_p1     = title

    # ══════════════════════════════════════════════════════════════════
    # PART 2 — Convection Entry  (10–25 s)
    # ══════════════════════════════════════════════════════════════════
    def part2_convection_entry(self):
        """Introduce the bad-guy convection stick figure."""

        streams = self._streams_base
        patch   = self._patch

        # --- Fade previous title ---
        self.play(FadeOut(self._title_p1, run_time=0.6))

        # --- Convection equation highlight ---
        eq_conv = MathTex(r"(\mathbf{v} \cdot \nabla)\mathbf{v}",
                          font_size=44, color=CONV_COLOR)
        eq_conv.to_corner(UL, buff=0.6)

        # --- Labels: anchor to screen left edge so they never clip ---
        lbl_conv = Text("Convection = transport by motion",
                        font_size=24, color=LABEL_CONV)
        lbl_conv.to_edge(LEFT, buff=0.3)
        lbl_conv.set_y(eq_conv.get_bottom()[1] - 0.45)

        sub_conv = Text("Carries and distorts fluid",
                        font_size=19, color=CONV_COLOR, slant=ITALIC)
        sub_conv.to_edge(LEFT, buff=0.3)
        sub_conv.set_y(lbl_conv.get_bottom()[1] - 0.35)

        # --- Bad-guy stick figure (convection = ORANGE/RED, on LEFT side) ---
        # Convection enters from the LEFT and aggressively pushes fluid RIGHT
        bad_guy = make_stick_figure(color=CONV_COLOR, scale=1.1)
        bad_guy.move_to(LEFT * 4.5 + DOWN * 0.3)
        bad_guy.set_stroke(opacity=0.9)

        # Glow effect: duplicate slightly blurred (Manim faux-glow)
        bad_glow = bad_guy.copy()
        bad_glow.set_stroke(color=CONV_COLOR, width=8, opacity=0.25)
        bad_glow_grp = VGroup(bad_glow, bad_guy)

        self.play(FadeIn(eq_conv, run_time=1),
                  FadeIn(lbl_conv, run_time=1))
        self.play(FadeIn(sub_conv, run_time=0.8))
        self.play(FadeIn(bad_glow_grp, scale=0.6, run_time=1.2))

        # --- Stick man strides RIGHT (aggressive, toward patch in center) ---
        self.play(bad_glow_grp.animate.shift(RIGHT * 1.3),
                  run_time=1.2, rate_func=rush_into)

        # --- Push arrows fire RIGHT from bad guy toward the patch ---
        push_orig_x = bad_glow_grp.get_center()[0] + 0.6
        push_orig   = np.array([push_orig_x, bad_glow_grp.get_center()[1], 0])
        push_dir    = RIGHT * 1.5
        push_arrows = make_push_arrows(push_orig, push_dir,
                                       n=5, color=CONV_COLOR, spread=0.32)

        self.play(Create(push_arrows, run_time=0.8))

        # --- Patch stretches and distorts (convection effect) ---
        chaotic_streams = make_chaotic_streamlines(n_lines=9, opacity=0.55)

        distorted_patch = Ellipse(width=3.2, height=0.35,
                                  fill_color=PATCH_COLOR,
                                  fill_opacity=0.65, stroke_width=0)
        # Patch gets pushed RIGHT by convection (bad guy is on left)
        distorted_patch.move_to(patch.get_center() + RIGHT * 0.4)

        self.play(
            Transform(streams, chaotic_streams, run_time=2, rate_func=smooth),
            Transform(patch, distorted_patch,    run_time=2, rate_func=smooth),
        )
        self.play(
            patch.animate.shift(LEFT * 0.8 + UP * 0.3),
            bad_glow_grp.animate.shift(RIGHT * 0.3),
            run_time=1, rate_func=there_and_back
        )

        self.wait(1)
        self.play(FadeOut(push_arrows, run_time=0.6))

        # Store
        self._bad_glow_grp   = bad_glow_grp
        self._chaotic_streams = chaotic_streams
        self._streams_now    = streams
        self._eq_conv        = eq_conv
        self._lbl_conv       = lbl_conv
        self._sub_conv       = sub_conv

    # ══════════════════════════════════════════════════════════════════
    # PART 3 — Diffusion Entry  (25–45 s)
    # ══════════════════════════════════════════════════════════════════
    def part3_diffusion_entry(self):
        """Introduce the good-guy diffusion stick figure."""

        streams = self._streams_now
        patch   = self._patch

        # --- Diffusion equation highlight ---
        eq_diff = MathTex(r"\mu \nabla^2 \mathbf{v}",
                          font_size=44, color=DIFF_COLOR)
        eq_diff.to_corner(UR, buff=0.6)

        # --- Labels: anchor to screen right edge, right-aligned ---
        lbl_diff = Text("Diffusion = smoothing by viscosity",
                        font_size=24, color=LABEL_DIFF)
        lbl_diff.to_edge(RIGHT, buff=0.3)
        lbl_diff.set_y(eq_diff.get_bottom()[1] - 0.45)

        sub_diff = Text("Reduces differences",
                        font_size=19, color=DIFF_COLOR, slant=ITALIC)
        sub_diff.to_edge(RIGHT, buff=0.3)
        sub_diff.set_y(lbl_diff.get_bottom()[1] - 0.35)

        # --- Good-guy stick figure (diffusion = CYAN, on RIGHT side) ---
        # Diffusion enters from the RIGHT and calmly pushes back LEFT to smooth the flow
        good_guy = make_stick_figure(color=DIFF_COLOR, scale=1.1)
        good_guy.move_to(RIGHT * 4.5 + DOWN * 0.3)
        good_glow = good_guy.copy()
        good_glow.set_stroke(color=DIFF_COLOR, width=8, opacity=0.25)
        good_glow_grp = VGroup(good_glow, good_guy)

        self.play(FadeIn(eq_diff, run_time=1),
                  FadeIn(lbl_diff, run_time=1))
        self.play(FadeIn(sub_diff, run_time=0.8))
        self.play(FadeIn(good_glow_grp, scale=0.6, run_time=1.2))

        # Good guy walks in calmly from right toward center
        self.play(good_glow_grp.animate.shift(LEFT * 1.3),
                  run_time=1.8, rate_func=smooth)

        # --- Calming arrows fire LEFT from good guy (pushing back against convection) ---
        push_left_x     = good_glow_grp.get_center()[0] - 0.6
        push_right_orig = np.array([push_left_x, good_glow_grp.get_center()[1], 0])
        calm_arrows = make_push_arrows(push_right_orig, LEFT * 1.4,
                                       n=5, color=DIFF_COLOR, spread=0.32)
        self.play(Create(calm_arrows, run_time=0.8))

        # --- Smooth out streams and patch ---
        smooth_streams = make_smooth_streamlines(n_lines=9, opacity=0.55)
        calm_patch = Ellipse(width=1.8, height=0.9,
                             fill_color="#7B61FF",   # blended purple
                             fill_opacity=0.60, stroke_width=0)
        calm_patch.move_to(ORIGIN)

        self.play(
            Transform(streams, smooth_streams, run_time=2.5, rate_func=smooth),
            Transform(patch,   calm_patch,     run_time=2.5, rate_func=smooth),
        )

        # Gentle bob
        self.play(patch.animate.shift(UP * 0.15),
                  run_time=0.8, rate_func=there_and_back)

        self.wait(1)
        self.play(FadeOut(calm_arrows, run_time=0.6))

        # Store
        self._good_glow_grp  = good_glow_grp
        self._smooth_streams = smooth_streams
        self._eq_diff        = eq_diff
        self._lbl_diff       = lbl_diff
        self._sub_diff       = sub_diff

    # ══════════════════════════════════════════════════════════════════
    # PART 4 — Battle Sequence  (45–65 s)
    # ══════════════════════════════════════════════════════════════════
    def part4_battle_sequence(self):
        """Both figures interact; fluid alternates chaos / smooth."""

        streams  = self._streams_now
        patch    = self._patch
        bad_grp  = self._bad_glow_grp
        good_grp = self._good_glow_grp

        # Clear side labels to give room
        self.play(
            FadeOut(self._lbl_conv, self._sub_conv,
                    self._lbl_diff, self._sub_diff,
                    run_time=0.8)
        )

        # Reposition fighters — bad guy LEFT, good guy RIGHT, safe for ±0.4 lunges
        self.play(
            bad_grp.animate.move_to(LEFT  * 3.2 + DOWN * 0.3),
            good_grp.animate.move_to(RIGHT * 3.2 + DOWN * 0.3),
            run_time=1.2, rate_func=smooth
        )

        # --- Dividing line ---
        divider = DashedLine(UP * 3, DOWN * 3,
                             stroke_color=GREY, stroke_width=1.5,
                             dash_length=0.18)
        divider.move_to(ORIGIN)

        # --- Zone labels — CHAOTIC on left (convection side), SMOOTH on right (diffusion side) ---
        chaos_lbl  = Text("CHAOTIC",  font_size=22, color=CONV_COLOR)
        smooth_lbl = Text("SMOOTH",   font_size=22, color=DIFF_COLOR)
        chaos_lbl.move_to(LEFT  * 2.8 + UP * 2.8)
        smooth_lbl.move_to(RIGHT * 2.8 + UP * 2.8)

        self.play(Create(divider, run_time=0.8),
                  FadeIn(chaos_lbl), FadeIn(smooth_lbl))

        # --- Battle text ---
        battle_text = Text("Flow behavior depends on who dominates",
                           font_size=28, color=TEXT_COLOR, font="Georgia")
        battle_text.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(battle_text, run_time=1))

        # --- 3 rounds of alternating dominance ---
        chaotic_s = make_chaotic_streamlines(n_lines=9, opacity=0.55)
        smooth_s  = make_smooth_streamlines(n_lines=9,  opacity=0.55)

        for _ in range(3):
            # Convection dominates — bad guy (LEFT) lunges RIGHT
            distorted = Ellipse(width=3.0, height=0.3,
                                fill_color=CONV_COLOR,
                                fill_opacity=0.55, stroke_width=0)
            distorted.move_to(patch.get_center() + RIGHT * 0.5)

            self.play(
                bad_grp.animate.shift(RIGHT * 0.4),
                Transform(streams, chaotic_s, run_time=1, rate_func=rush_into),
                Transform(patch, distorted,   run_time=1, rate_func=rush_into),
            )
            self.play(bad_grp.animate.shift(LEFT * 0.4),
                      run_time=0.4, rate_func=smooth)

            # Diffusion pushes back — good guy (RIGHT) steps LEFT
            calmed = Ellipse(width=1.6, height=0.85,
                             fill_color=DIFF_COLOR,
                             fill_opacity=0.50, stroke_width=0)
            calmed.move_to(ORIGIN)

            self.play(
                good_grp.animate.shift(LEFT * 0.4),
                Transform(streams, smooth_s, run_time=1.2, rate_func=smooth),
                Transform(patch, calmed,     run_time=1.2, rate_func=smooth),
            )
            self.play(good_grp.animate.shift(RIGHT * 0.4),
                      run_time=0.4, rate_func=smooth)

        self.wait(0.5)

        # Store
        self._divider      = divider
        self._battle_text  = battle_text
        self._chaos_lbl    = chaos_lbl
        self._smooth_lbl   = smooth_lbl

    # ══════════════════════════════════════════════════════════════════
    # PART 5 — Outcome  (65–80 s)
    # ══════════════════════════════════════════════════════════════════
    def part5_outcome(self):
        """Explain Reynolds number — convection vs diffusion balance."""

        bad_grp  = self._bad_glow_grp
        good_grp = self._good_glow_grp

        # Dim the fighters
        self.play(
            bad_grp.animate.set_stroke(opacity=0.35),
            good_grp.animate.set_stroke(opacity=0.35),
            FadeOut(self._divider,
                    self._battle_text,
                    self._chaos_lbl,
                    self._smooth_lbl,
                    run_time=0.8)
        )

        # --- Outcome cards ---
        # Bad guy (convection) is on LEFT → convection label goes LEFT
        # Good guy (diffusion) is on RIGHT → diffusion label goes RIGHT
        conv_outcome = VGroup(
            Text("Convection dominates", font_size=24, color=CONV_COLOR),
            Text("→  Turbulence",        font_size=20, color=LABEL_CONV,
                 slant=ITALIC)
        ).arrange(DOWN, buff=0.15)
        conv_outcome.move_to(LEFT * 3.5 + UP * 1.5)

        diff_outcome = VGroup(
            Text("Diffusion dominates", font_size=24, color=DIFF_COLOR),
            Text("→  Smooth flow",      font_size=20, color=LABEL_DIFF,
                 slant=ITALIC)
        ).arrange(DOWN, buff=0.15)
        diff_outcome.move_to(RIGHT * 3.5 + UP * 1.5)

        self.play(FadeIn(conv_outcome, shift=UP * 0.3, run_time=1.2),
                  FadeIn(diff_outcome, shift=UP * 0.3, run_time=1.2))

        # --- Reynolds Number — shifted up to leave room for interpretation line ---
        re_eq = MathTex(
            r"\mathrm{Re} = \frac{\rho\, V\, L}{\mu}",
            font_size=42, color=TEXT_COLOR
        )
        re_eq.move_to(DOWN * 0.8)

        re_label = Text("Balance between convection and diffusion",
                        font_size=19, color=GREY_B)
        re_label.next_to(re_eq, DOWN, buff=0.20)

        self.play(Write(re_eq, run_time=2))
        self.play(FadeIn(re_label, run_time=1))

        self.wait(0.8)

        # --- Re = Convection / Diffusion interpretation ---
        re_interp = MathTex(
            r"\mathrm{Re}",
            r"=",
            r"\frac{\text{Convection}}{\text{Diffusion}}",
            font_size=38
        )
        re_interp[0].set_color(TEXT_COLOR)
        re_interp[1].set_color(TEXT_COLOR)
        re_interp[2][0:10].set_color(CONV_COLOR)   # "Convection" numerator
        re_interp[2][10:].set_color(DIFF_COLOR)    # "Diffusion" denominator
        re_interp.next_to(re_label, DOWN, buff=0.28)

        self.play(Write(re_interp, run_time=1.8))
        self.wait(2)

        # Store for fade-out
        self._outcome_objs = VGroup(conv_outcome, diff_outcome,
                                    re_eq, re_label, re_interp)

    # ══════════════════════════════════════════════════════════════════
    # PART 6 — Transition back to physics  (80–85 s)
    # ══════════════════════════════════════════════════════════════════
    def part6_transition(self):
        """Fade figures, keep only fluid. Final line."""

        bad_grp  = self._bad_glow_grp
        good_grp = self._good_glow_grp

        self.play(
            FadeOut(bad_grp,  run_time=1.5),
            FadeOut(good_grp, run_time=1.5),
            FadeOut(self._outcome_objs, run_time=1.2),
            FadeOut(self._eq_conv, self._eq_diff, run_time=1.2),
        )

        # Re-draw clean neutral streamlines
        final_streams = make_streamlines(n_lines=9, opacity=0.65)
        self.play(
            Transform(self._streams_now, final_streams, run_time=2, rate_func=smooth)
        )

        # Final patch — serene circular blob
        final_patch = Circle(radius=0.5,
                             fill_color="#8B5CF6",
                             fill_opacity=0.5, stroke_width=0)
        final_patch.move_to(self._patch.get_center())
        self.play(Transform(self._patch, final_patch, run_time=1.5, rate_func=smooth))

        # Closing text
        closing = Text("This is not a fight…  it is physics",
                       font_size=36, color=TEXT_COLOR, font="Georgia")
        closing.move_to(ORIGIN + UP * 0.3)

        self.play(Write(closing, run_time=2))
        self.wait(3)

        # Fade to black
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )
        self.wait(0.5)