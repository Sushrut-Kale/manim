from manim import *
import numpy as np


# ═══════════════════════════════════════════════════════════
#  GLOBAL STYLE CONSTANTS
# ═══════════════════════════════════════════════════════════
BG_COLOR      = "#06070F"
FLUID_BLUE    = "#1E6FA8"
FLUID_DARK    = "#0A1E3A"
ARROW_COLOR   = "#6AABCC"
GRID_COLOR    = "#111E2A"
CYAN_GLOW     = "#00E5FF"
TEXT_WHITE    = WHITE
FADED_GRAY    = "#3A4A5A"
HIGHLIGHT_YEL = "#FFE066"
OBJ_COLOR     = "#C0D8F0"
DOMINANT_COL  = "#00E5FF"    # bright cyan — important terms
NEGLIGIBLE    = "#2A3A4A"    # dark — terms we drop


# ═══════════════════════════════════════════════════════════
#  VELOCITY FIELD HELPERS
# ═══════════════════════════════════════════════════════════

def laminar_velocity(x, y):
    """Smooth leftward shear flow — used in calm parts of scene."""
    vx = 1.0 + 0.25 * np.sin(0.6 * y)
    vy = 0.10 * np.sin(0.9 * x + 0.3 * y)
    return np.array([vx, vy, 0])


def chaotic_velocity(x, y, t=0.0):
    """
    Turbulence-like velocity field — many frequencies,
    appears unpredictable. Used for Part 3.
    """
    vx = (  0.8 * np.sin(1.5 * y + 2.3)
          + 0.5 * np.cos(2.2 * x - 1.1)
          + 0.35 * np.sin(3.1 * x + 2.0 * y + t)
          + 0.2 * np.cos(4.0 * y - 0.7 * x))
    vy = (  0.7 * np.cos(1.3 * x + 1.8)
          + 0.45 * np.sin(2.4 * y + 0.5)
          + 0.3 * np.cos(3.3 * x - 1.9 * y + t)
          + 0.18 * np.sin(4.1 * x + 1.2))
    return np.array([vx, vy, 0])


def near_wall_velocity(x, y, y_wall=-2.5, delta=0.7):
    """
    Simple boundary-layer-like profile near y = y_wall.
    Outside boundary layer: uniform. Inside: parabolic growth.
    """
    dist = y - y_wall
    if dist <= 0:
        return np.array([0.0, 0.0, 0])
    if dist >= delta:
        vx = 1.0
    else:
        vx = (dist / delta) ** 0.4   # sub-linear boundary layer profile
    return np.array([vx, 0.0, 0])


def make_streamlines(vel_func, seeds,
                     steps=120, dt=0.065,
                     stroke_w=1.3, opacity=0.45):
    """Euler-integrate streamlines from seed list."""
    lines = VGroup()
    for (sx, sy) in seeds:
        pts = []
        x, y = float(sx), float(sy)
        for _ in range(steps):
            pts.append([x, y, 0])
            v  = vel_func(x, y)
            nm = np.linalg.norm(v[:2]) + 1e-6
            x += v[0] / nm * dt
            y += v[1] / nm * dt
            if abs(x) > 7.8 or abs(y) > 4.8:
                break
        if len(pts) < 3:
            continue
        path = VMobject()
        path.set_points_smoothly([np.array(p) for p in pts])
        path.set_stroke(FLUID_BLUE, width=stroke_w, opacity=opacity)
        lines.add(path)
    return lines


def make_arrow_grid(vel_func, xs, ys,
                    scale=0.28, opacity=0.55, color=ARROW_COLOR):
    """Velocity arrow grid for given x/y sample points."""
    arrows = VGroup()
    for x in xs:
        for y in ys:
            v   = vel_func(x, y)
            spd = np.linalg.norm(v[:2])
            if spd < 1e-4:
                continue
            d   = v / spd
            l   = np.clip(spd * scale, 0.05, 0.50)
            s   = np.array([x, y, 0])
            arr = Arrow(s, s + d * l, buff=0,
                        stroke_width=1.6, tip_length=0.09,
                        color=color)
            arr.set_opacity(opacity)
            arrows.add(arr)
    return arrows


# ═══════════════════════════════════════════════════════════
#  MAIN SCENE
# ═══════════════════════════════════════════════════════════

class Scene9_Approximation(MovingCameraScene):
    """
    Scene 9 — Approximation: From Unsolved Equation to Practical Use.

    Flow of ideas:
      Full N-S equation → can't solve in 3D → chaos of turbulence →
      need to simplify → dominant vs negligible terms →
      simplified equation → boundary layer region → next scene.
    """

    def construct(self):
        self.camera.background_color = BG_COLOR
        self._base_width = self.camera.frame.width

        self._part1_full_equation()       #  0–10 s
        self._part2_hard_truth()          # 10–20 s
        self._part3_chaos()               # 20–30 s
        self._part4_turning_point()       # 30–40 s
        self._part5_dominance()           # 40–55 s
        self._part6_simplify()            # 55–70 s
        self._part7_near_wall()           # 70–80 s
        self._part8_bridge()              # 80–85 s

    # ╔══════════════════════════════════════════════════════╗
    # ║  PART 1 — Full Equation  (0–10 s)                   ║
    # ╚══════════════════════════════════════════════════════╝
    def _part1_full_equation(self):
        """
        Reveal the full Navier–Stokes equation with a calm fluid
        background. Let it breathe — this is the centrepiece.
        """
        # ── Background: calm laminar streamlines ──────────────
        seeds = [(-7, y) for y in np.linspace(-4.0, 4.0, 22)]
        self._bg_streams = make_streamlines(
            laminar_velocity, seeds,
            steps=140, dt=0.065, stroke_w=1.3, opacity=0.38,
        )
        self.add(self._bg_streams)

        # ── Context line ──────────────────────────────────────
        context = Text(
            "The equation that governs all fluid motion:",
            font_size=24, color=ARROW_COLOR, slant=ITALIC,
        ).to_edge(UP, buff=0.45)
        context.set_stroke(BLACK, width=3, background=True)
        self.play(FadeIn(context, shift=DOWN * 0.1), run_time=1.0)

        # ── Navier–Stokes equation ────────────────────────────
        # Split into labelled groups so we can highlight each term later
        ns_eq = MathTex(
            r"\rho",                             # [0]  density
            r"\left(",
            r"\frac{\partial \vec{v}}{\partial t}",   # [2]  unsteady
            r"+",
            r"(\vec{v} \cdot \nabla)\vec{v}",   # [4]  convection
            r"\right)",
            r"=",
            r"-\nabla p",                        # [7]  pressure
            r"+",
            r"\mu \nabla^2 \vec{v}",             # [9]  viscosity
            r"+",
            r"\vec{f}",                          # [11] body force
            color=WHITE,
            font_size=40,
        )
        ns_eq.move_to(ORIGIN + UP * 0.3)
        ns_eq.set_stroke(BLACK, width=3, background=True)

        # Glow box behind equation
        glow_box = SurroundingRectangle(
            ns_eq, corner_radius=0.18,
            color=CYAN_GLOW, stroke_width=0.9, buff=0.22,
        )
        glow_box.set_fill(BLACK, opacity=0.45)

        self.play(FadeIn(glow_box), run_time=0.5)
        self.play(Write(ns_eq), run_time=2.5, rate_func=smooth)

        # ── Brief caption ─────────────────────────────────────
        caption1 = Text(
            "This equation describes fluid motion everywhere…",
            font_size=22, color=TEXT_WHITE, slant=ITALIC,
        ).to_edge(DOWN, buff=0.50)
        caption1.set_stroke(BLACK, width=3, background=True)

        self.play(FadeIn(caption1, shift=UP * 0.1), run_time=0.9)
        self.wait(2.8)

        # Save references
        self._ns_eq    = ns_eq
        self._glow_box = glow_box
        self._caption1 = caption1
        self._context  = context

    # ╔══════════════════════════════════════════════════════╗
    # ║  PART 2 — Hard Truth  (10–20 s)                     ║
    # ╚══════════════════════════════════════════════════════╝
    def _part2_hard_truth(self):
        """
        State the problem plainly: unsolved in 3D.
        The equation dims slightly — feels heavier.
        A small 'Millennium Prize' tag appears as a quiet detail.
        """
        self.play(FadeOut(self._caption1), FadeOut(self._context), run_time=0.5)

        # Shift equation up to make room for text
        self.play(
            self._ns_eq.animate.shift(UP * 0.6),
            self._glow_box.animate.shift(UP * 0.6),
            run_time=0.8, rate_func=smooth,
        )

        # Two-line statement below the equation
        truth1 = Text(
            "But we cannot solve it in general…",
            font_size=26, color=TEXT_WHITE,
        ).next_to(self._ns_eq, DOWN, buff=0.55)
        truth1.set_stroke(BLACK, width=3, background=True)

        self.play(FadeIn(truth1, shift=UP * 0.1), run_time=1.0)
        self.wait(1.2)

        truth2 = Text(
            "In 3D, a complete solution remains unknown.",
            font_size=26, color=HIGHLIGHT_YEL,
        ).next_to(truth1, DOWN, buff=0.35)
        truth2.set_stroke(BLACK, width=3, background=True)

        self.play(FadeIn(truth2, shift=UP * 0.1), run_time=1.0)
        self.wait(1.0)

        # Small subtle Millennium Prize tag
        prize_tag = Text(
            "[ Millennium Prize Problem — $1,000,000 unsolved ]",
            font_size=20, color=FADED_GRAY, slant=ITALIC,
            ).to_edge(DOWN, buff=0.6)  # slightly lower start
        prize_tag.set_stroke(BLACK, width=2, background=True)
        # move slightly upward while appearin
        self.play(
            FadeIn(prize_tag, shift=UP * 0.2),
            prize_tag.animate.shift(UP * 0.25),
            run_time=1
            )
            # highlight effect
            self.play(
                prize_tag.animate.set_color(YELLOW).set_stroke(YELLOW, width=3),
                run_time=0.6
                )
                # subtle pulse
                self.play(
                    prize_tag.animate.scale(1.05),
                    rate_func=there_and_back,
                    run_time=0.5
                    )
                self.wait(2.5)

       

        # Slight dim on equation to signal "weight"
        self.play(
            self._ns_eq.animate.set_opacity(0.70),
            self._glow_box.animate.set_stroke(opacity=0.45),
            run_time=1.0,
        )

        self._truth1    = truth1
        self._truth2    = truth2
        self._prize_tag = prize_tag

    # ╔══════════════════════════════════════════════════════╗
    # ║  PART 3 — Chaos Visualised  (20–30 s)               ║
    # ╚══════════════════════════════════════════════════════╝
    def _part3_chaos(self):
        """
        Replace calm streamlines with a chaotic turbulent field.
        Arrows become unpredictable. Caption: 'Too complex to solve directly.'
        """
        self.play(
            FadeOut(self._truth1),
            FadeOut(self._truth2),
            FadeOut(self._prize_tag),
            run_time=0.6,
        )

        # Fade out calm background
        self.play(FadeOut(self._bg_streams), run_time=0.8)

        # ── Chaotic streamlines ───────────────────────────────
        chaotic_seeds = [(-7, y) for y in np.linspace(-4.0, 4.0, 26)]
        chaotic_streams = make_streamlines(
            chaotic_velocity, chaotic_seeds,
            steps=110, dt=0.055, stroke_w=1.2, opacity=0.42,
        )

        # ── Dense chaotic arrows ──────────────────────────────
        xs = np.linspace(-6, 6, 14)
        ys = np.linspace(-3.5, 3.5, 9)
        chaotic_arrows = make_arrow_grid(
            chaotic_velocity, xs, ys,
            scale=0.22, opacity=0.55, color=ARROW_COLOR,
        )

        self.play(
            Create(chaotic_streams, lag_ratio=0.020),
            run_time=2.2, rate_func=smooth,
        )
        self.play(
            FadeIn(chaotic_arrows, lag_ratio=0.015),
            run_time=1.5,
        )

        chaos_cap = Text(
            "Too complex to solve directly.",
            font_size=27, color=TEXT_WHITE, slant=ITALIC,
        ).to_edge(DOWN, buff=0.50)
        chaos_cap.set_stroke(BLACK, width=3, background=True)

        self.play(FadeIn(chaos_cap, shift=UP * 0.1), run_time=0.8)
        self.wait(2.8)

        self.play(
            FadeOut(chaotic_streams),
            FadeOut(chaotic_arrows),
            FadeOut(chaos_cap),
            run_time=1.2,
        )

    # ╔══════════════════════════════════════════════════════╗
    # ║  PART 4 — Turning Point  (30–40 s)                  ║
    # ╚══════════════════════════════════════════════════════╝
    def _part4_turning_point(self):
        """
        Brief pause. Two-word answer: 'We simplify.'
        This is the emotional and conceptual pivot of the scene.
        """
        # Restore laminar background faintly
        seeds = [(-7, y) for y in np.linspace(-4.0, 4.0, 18)]
        calm_bg = make_streamlines(
            laminar_velocity, seeds,
            steps=130, dt=0.065, stroke_w=1.2, opacity=0.28,
        )
        self.play(FadeIn(calm_bg), run_time=1.0)

        # Question
        question = Text(
            "So what do we do?",
            font_size=38, color=TEXT_WHITE,
        ).move_to(UP * 0.6)
        question.set_stroke(BLACK, width=4, background=True)

        self.play(FadeIn(question, shift=UP * 0.1), run_time=1.0)
        self.wait(1.8)

        # Answer — "We simplify." in cyan
        answer = Text(
            "We simplify.",
            font_size=46, color=CYAN_GLOW, weight=BOLD,
        ).next_to(question, DOWN, buff=0.55)
        answer.set_stroke(BLACK, width=4, background=True)

        self.play(FadeIn(answer, scale=1.06), run_time=1.2)
        self.wait(2.8)

        self.play(
            FadeOut(question),
            FadeOut(answer),
            FadeOut(calm_bg),
            run_time=1.0,
        )

        # Restore equation to full opacity
        self.play(
            self._ns_eq.animate.set_opacity(1.0).shift(DOWN * 0.6),
            self._glow_box.animate.shift(DOWN * 0.6).set_stroke(opacity=0.9),
            run_time=0.8, rate_func=smooth,
        )

    # ╔══════════════════════════════════════════════════════╗
    # ║  PART 5 — Dominance Highlighted  (40–55 s)          ║
    # ╚══════════════════════════════════════════════════════╝
    def _part5_dominance(self):
        """
        Walk through the equation term by term.
        Some terms glow cyan (dominant), others dim to gray (negligible).
        Labels appear beneath each term explaining what it means physically.
        """
        setup_text = Text(
            "In real situations, some effects dominate.",
            font_size=23, color=TEXT_WHITE, slant=ITALIC,
        ).to_edge(DOWN, buff=0.50)
        setup_text.set_stroke(BLACK, width=3, background=True)
        self.play(FadeIn(setup_text, shift=UP * 0.1), run_time=0.8)
        self.wait(0.8)

        # ── Zoom camera in slightly so equation fills frame ────
        self.play(
            self.camera.frame.animate
                .scale(0.78)
                .move_to(self._ns_eq.get_center() + DOWN * 0.15),
            run_time=1.5, rate_func=smooth,
        )

        # ns_eq indices:
        #   [0]  ρ           density (scalar, just context)
        #   [2]  ∂v/∂t       unsteady term
        #   [4]  (v·∇)v      convective acceleration
        #   [7]  -∇p         pressure gradient
        #   [9]  μ∇²v        viscous diffusion
        #   [11] f            body force

        # Term metadata: (index, label, is_dominant)
        terms = [
            (2,  "Unsteady\n(time changes)",          True),
            (4,  "Convection\n(inertia)",              True),
            (7,  "Pressure\n(driving force)",          True),
            (9,  "Viscosity\n(friction)",              True),
            (11, "Body force\n(gravity etc.)",         False),
        ]

        label_group = VGroup()
        self.play(FadeOut(setup_text), run_time=0.4)

        for idx, meaning, dominant in terms:
            col = DOMINANT_COL if dominant else FADED_GRAY

            # Glow the term
            self.play(
                self._ns_eq[idx].animate.set_color(col),
                run_time=0.5, rate_func=smooth,
            )

            # Small label beneath the term
            lbl = Text(meaning, font_size=13, color=col, line_spacing=1.1)
            lbl.next_to(self._ns_eq[idx], DOWN, buff=0.28)
            lbl.set_stroke(BLACK, width=2, background=True)

            self.play(FadeIn(lbl, shift=UP * 0.08), run_time=0.45)
            label_group.add(lbl)
            self.wait(0.35)

        dom_caption = Text(
            "Some terms dominate — others become negligible.",
            font_size=20, color=TEXT_WHITE, slant=ITALIC,
        )
        dom_caption.to_edge(DOWN, buff=0.30)
        dom_caption.set_stroke(BLACK, width=3, background=True)
        self.play(FadeIn(dom_caption, shift=UP * 0.1), run_time=0.7)
        self.wait(2.5)

        self._label_group = label_group
        self._dom_caption = dom_caption

    # ╔══════════════════════════════════════════════════════╗
    # ║  PART 6 — Weak Terms Fade  (55–70 s)                ║
    # ╚══════════════════════════════════════════════════════╝
    def _part6_simplify(self):
        """
        Animate the removal of negligible terms from the equation.
        Body force (f) shrinks and fades first.
        Then unsteady term (∂v/∂t) fades for steady-flow case.
        A simplified equation remains — clean and readable.
        """
        self.play(
            FadeOut(self._dom_caption),
            FadeOut(self._label_group),
            run_time=0.5,
        )

        ignore_cap = Text(
            "We ignore small effects…",
            font_size=24, color=HIGHLIGHT_YEL, slant=ITALIC,
        ).to_edge(DOWN, buff=0.50)
        ignore_cap.set_stroke(BLACK, width=3, background=True)
        self.play(FadeIn(ignore_cap, shift=UP * 0.1), run_time=0.7)
        self.wait(0.6)

        # ── Step 1: Fade body force (index 10='+', 11='f') ─────
        self.play(
            self._ns_eq[10].animate.set_opacity(0.08),
            self._ns_eq[11].animate.set_opacity(0.08),
            run_time=1.2, rate_func=smooth,
        )
        self.wait(0.5)

        # ── Step 2: Fade unsteady term (steady flow assumption) ─
        # indices 1='(', 2='∂v/∂t', 3='+', 5=')' … fade 2 & 3
        self.play(
            self._ns_eq[2].animate.set_opacity(0.08),
            self._ns_eq[3].animate.set_opacity(0.08),
            run_time=1.2, rate_func=smooth,
        )
        self.wait(0.5)

        focus_cap = Text(
            "…to focus on the dominant physics.",
            font_size=24, color=TEXT_WHITE, slant=ITALIC,
        ).to_edge(DOWN, buff=0.50)
        focus_cap.set_stroke(BLACK, width=3, background=True)

        self.play(
            FadeOut(ignore_cap),
            FadeIn(focus_cap, shift=UP * 0.1),
            run_time=0.7,
        )

        # ── Pulse-glow remaining dominant terms ───────────────
        dominant_indices = [0, 1, 4, 5, 6, 7, 8, 9]
        pulses = [
            self._ns_eq[i].animate.set_color(CYAN_GLOW)
            for i in dominant_indices
        ]
        self.play(*pulses, run_time=1.0, rate_func=smooth)
        self.wait(1.5)

        # Show what remains as a clean simplified equation
        simplified = MathTex(
            r"\rho \,(\vec{v} \cdot \nabla)\vec{v}",
            r"=",
            r"-\nabla p",
            r"+",
            r"\mu \nabla^2 \vec{v}",
            color=WHITE,
            font_size=42,
        )
        simplified.next_to(self._ns_eq, DOWN, buff=0.65)
        simplified.set_stroke(BLACK, width=3, background=True)

        simp_label = Text(
            "Steady-state, no body force — much more tractable.",
            font_size=18, color=CYAN_GLOW, slant=ITALIC,
        ).next_to(simplified, DOWN, buff=0.28)
        simp_label.set_stroke(BLACK, width=2, background=True)

        self.play(
            FadeIn(simplified, shift=UP * 0.1),
            run_time=1.2, rate_func=smooth,
        )
        self.play(FadeIn(simp_label, shift=UP * 0.08), run_time=0.7)
        self.wait(3.0)

        self.play(
            FadeOut(focus_cap),
            FadeOut(simp_label),
            run_time=0.6,
        )

        self._simplified = simplified

    # ╔══════════════════════════════════════════════════════╗
    # ║  PART 7 — Near-Wall Region  (70–80 s)               ║
    # ╚══════════════════════════════════════════════════════╝
    def _part7_near_wall(self):
        """
        Fade the equation away and show a physical picture:
        flow above a flat plate.  A thin highlighted band near the wall
        shows the region where viscosity dominates — the boundary layer.
        """
        # Restore camera to full view
        self.play(
            self.camera.frame.animate
                .set_width(self._base_width)
                .move_to(ORIGIN),
            FadeOut(self._ns_eq),
            FadeOut(self._glow_box),
            FadeOut(self._simplified),
            run_time=1.5, rate_func=smooth,
        )

        region_text = Text(
            "In certain regions, simplification becomes extremely powerful.",
            font_size=23, color=TEXT_WHITE, slant=ITALIC,
        ).to_edge(UP, buff=0.45)
        region_text.set_stroke(BLACK, width=3, background=True)
        self.play(FadeIn(region_text, shift=DOWN * 0.1), run_time=0.9)

        # ── Flat plate (wall) ──────────────────────────────────
        wall_y = -2.4
        wall = Line(
            [-7.0, wall_y, 0], [7.0, wall_y, 0],
            color=OBJ_COLOR, stroke_width=3.0,
        )
        wall_fill = Rectangle(
            width=14, height=0.6,
            color=FLUID_DARK, stroke_width=0,
        )
        wall_fill.set_fill(FLUID_DARK, opacity=0.9)
        wall_fill.move_to([0, wall_y - 0.30, 0])

        self.play(
            FadeIn(wall_fill),
            Create(wall),
            run_time=1.0,
        )

        # ── Near-wall streamlines ──────────────────────────────
        seeds_wall = [(-6.8, wall_y + 0.05 + k)
                      for k in np.linspace(0.05, 4.2, 18)]
        wall_streams = make_streamlines(
            lambda x, y: near_wall_velocity(x, y, y_wall=wall_y),
            seeds_wall,
            steps=140, dt=0.07, stroke_w=1.3, opacity=0.50,
        )
        self.play(Create(wall_streams, lag_ratio=0.025), run_time=2.0)

        # ── Velocity profile arrows at x = 1.5 ────────────────
        profile_x = 1.5
        prof_arrows = VGroup()
        for r in np.linspace(0.06, 1.8, 12):
            dist = r
            if dist < 0.7:
                vx = (dist / 0.7) ** 0.4
            else:
                vx = 1.0
            col = interpolate_color(
                ManimColor(CYAN_GLOW), ManimColor(FLUID_BLUE),
                np.clip(dist / 1.8, 0, 1),
            )
            arr = Arrow(
                [profile_x, wall_y + dist, 0],
                [profile_x + vx * 0.65, wall_y + dist, 0],
                buff=0, stroke_width=1.5, tip_length=0.09, color=col,
            )
            arr.set_opacity(0.82)
            prof_arrows.add(arr)

        self.play(FadeIn(prof_arrows, lag_ratio=0.05), run_time=1.2)

        # ── Highlight the boundary layer band ─────────────────
        bl_height = 0.70      # boundary layer thickness (visual)
        bl_band = Rectangle(
            width=13.5, height=bl_height,
            color=HIGHLIGHT_YEL, stroke_width=1.2,
        )
        bl_band.set_fill(HIGHLIGHT_YEL, opacity=0.10)
        bl_band.move_to([0, wall_y + bl_height / 2, 0])

        bl_label = Text(
            "Boundary Layer",
            font_size=18, color=HIGHLIGHT_YEL, weight=BOLD,
        ).next_to(bl_band, RIGHT, buff=0.25)
        bl_label.set_stroke(BLACK, width=2, background=True)

        self.play(
            FadeIn(bl_band),
            FadeIn(bl_label),
            run_time=1.0,
        )

        power_text = Text(
            "Here, viscous effects dominate — and the equations simplify greatly.",
            font_size=21, color=TEXT_WHITE, slant=ITALIC,
        ).to_edge(DOWN, buff=0.50)
        power_text.set_stroke(BLACK, width=3, background=True)
        self.play(FadeIn(power_text, shift=UP * 0.1), run_time=0.8)
        self.wait(3.5)

        self.play(FadeOut(power_text), FadeOut(region_text), run_time=0.5)

        # Save refs for Part 8
        self._wall           = wall
        self._wall_fill      = wall_fill
        self._wall_streams   = wall_streams
        self._prof_arrows    = prof_arrows
        self._bl_band        = bl_band
        self._bl_label       = bl_label
        self._wall_y         = wall_y

    # ╔══════════════════════════════════════════════════════╗
    # ║  PART 8 — Bridge to Boundary Layer  (80–85 s)       ║
    # ╚══════════════════════════════════════════════════════╝
    def _part8_bridge(self):
        """
        Camera zooms into the thin yellow boundary layer region.
        Closing text bridges to the next scene: boundary layer theory.
        Elegant fade to black.
        """
        bridge_text = Text(
            "This leads to boundary layer theory.",
            font_size=34, color=CYAN_GLOW, weight=BOLD,
        )
        bridge_text.set_stroke(BLACK, width=4, background=True)
        bridge_text.to_edge(UP, buff=0.42)

        self.play(FadeIn(bridge_text, shift=DOWN * 0.1), run_time=0.9)

        # Zoom into the boundary layer band
        bl_centre = self._bl_band.get_center()
        self.play(
            self.camera.frame.animate
                .scale(0.38)
                .move_to(bl_centre + UP * 0.15),
            run_time=2.5, rate_func=smooth,
        )
        self.wait(1.5)

        # Final closing caption
        closing = Text(
            "A thin layer. Immense physics.",
            font_size=28, color=HIGHLIGHT_YEL, slant=ITALIC,
        )
        closing.set_stroke(BLACK, width=4, background=True)
        closing.move_to(bl_centre + UP * 0.55)

        self.play(FadeIn(closing, scale=1.04), run_time=1.0)
        self.wait(2.0)

        # Fade everything to black
        self.play(
            FadeOut(closing),
            FadeOut(bridge_text),
            FadeOut(self._bl_band),
            FadeOut(self._bl_label),
            FadeOut(self._wall_streams),
            FadeOut(self._prof_arrows),
            FadeOut(self._wall),
            FadeOut(self._wall_fill),
            run_time=2.5, rate_func=smooth,
        )
        self.wait(0.4)