from manim import *
import numpy as np


# ═══════════════════════════════════════════════════════════
#  GLOBAL STYLE CONSTANTS
# ═══════════════════════════════════════════════════════════
BG_COLOR      = "#06070F"
FLUID_BLUE    = "#1E6FA8"
FLUID_LIGHT   = "#5BB8E8"
ARROW_COLOR   = "#7ABEDD"
WALL_COLOR    = "#D0E8FF"
BL_COLOR      = "#4FC3F7"       # boundary layer fill tint
BL_EDGE_COL   = "#00E5FF"       # boundary layer edge line
GRID_COLOR    = "#111E2A"
CYAN_GLOW     = "#00E5FF"
TEXT_WHITE    = WHITE
FADED_GRAY    = "#2E3E50"
HIGHLIGHT_YEL = "#FFE066"
DOMINANT_COL  = "#00E5FF"
REMOVED_COL   = "#253545"

# Layout constants — everything is built relative to these
WALL_Y        = -2.60           # y-position of the flat plate
PLATE_X_LEFT  = -6.50           # plate starts here
PLATE_X_RIGHT =  6.50           # plate ends here
BL_MAX_THICK  =  1.55           # visual boundary layer thickness at trailing edge
FREE_STREAM_Y =  1.80           # y of the undisturbed free-stream


# ═══════════════════════════════════════════════════════════
#  PHYSICS HELPERS
# ═══════════════════════════════════════════════════════════

def bl_thickness(x, x0=PLATE_X_LEFT, scale=BL_MAX_THICK):
    dist = max(x - x0, 0.0)
    plate_len = PLATE_X_RIGHT - x0
    return scale * np.sqrt(dist / plate_len)


def bl_velocity_u(y_above_wall, x, u_inf=1.0):
    delta = bl_thickness(x)
    if delta < 1e-4:
        return 0.0
    eta = y_above_wall / delta
    return u_inf * np.tanh(2.4 * eta)


def uniform_velocity(x, y):
    return np.array([1.0, 0.0, 0])


def plate_velocity(x, y):
    if x < PLATE_X_LEFT:
        return np.array([1.0, 0.0, 0])
    y_above = y - WALL_Y
    if y_above <= 0:
        return np.array([0.0, 0.0, 0])
    u = bl_velocity_u(y_above, x)
    return np.array([u, 0.0, 0])


def make_streamlines_plate(seeds, steps=180, dt=0.055,
                            stroke_w=1.3, opacity=0.50, color=FLUID_BLUE):
    lines = VGroup()
    for (sx, sy) in seeds:
        pts = []
        x, y = float(sx), float(sy)
        for _ in range(steps):
            pts.append([x, y, 0])
            v  = plate_velocity(x, y)
            nm = np.linalg.norm(v[:2]) + 1e-6
            x += v[0] / nm * dt
            y += v[1] / nm * dt
            if x > PLATE_X_RIGHT + 0.5 or y > 4.8 or y < WALL_Y:
                break
        if len(pts) < 3:
            continue
        path = VMobject()
        path.set_points_smoothly([np.array(p) for p in pts])
        path.set_stroke(color, width=stroke_w, opacity=opacity)
        lines.add(path)
    return lines


def profile_arrows_at_x(x_pos, n=10, max_height=2.5,
                         u_inf=1.0, scale=0.75, opacity=0.82):
    arrows = VGroup()
    ys = np.linspace(WALL_Y + 0.02, WALL_Y + max_height, n)
    for y in ys:
        y_above = y - WALL_Y
        u = bl_velocity_u(y_above, x_pos, u_inf)
        length = max(u * scale, 0.015)
        t = np.clip(u, 0, 1)
        col = interpolate_color(ManimColor(FADED_GRAY),
                                ManimColor(CYAN_GLOW), t)
        arr = Arrow(
            [x_pos, y, 0],
            [x_pos + length, y, 0],
            buff=0, stroke_width=1.6,
            tip_length=0.09, color=col,
        )
        arr.set_opacity(opacity)
        arrows.add(arr)
    return arrows


# ═══════════════════════════════════════════════════════════
#  MAIN SCENE
# ═══════════════════════════════════════════════════════════

class Scene10_BoundaryLayer(MovingCameraScene):

    def construct(self):
        self.camera.background_color = BG_COLOR
        self._base_width = self.camera.frame.width

        self._part1_uniform_approach()
        self._part2_no_slip()
        self._part3_bl_formation()
        self._part4_delta_over_L()
        self._part5_gradient_insight()
        self._part6_equation_reduction()
        self._part7_final()

    # ─────────────────────────────────────────────────────
    #  Shared geometry builders
    # ─────────────────────────────────────────────────────

    def _make_wall(self):
        wall_line = Line(
            [PLATE_X_LEFT, WALL_Y, 0],
            [PLATE_X_RIGHT, WALL_Y, 0],
            color=WALL_COLOR, stroke_width=3.0,
        )
        wall_fill = Rectangle(
            width=PLATE_X_RIGHT - PLATE_X_LEFT + 0.2,
            height=0.55,
            stroke_width=0,
        )
        wall_fill.set_fill("#0A1520", opacity=1.0)
        wall_fill.move_to([0, WALL_Y - 0.275, 0])
        return wall_line, wall_fill

    def _make_bl_edge_curve(self, x_samples=80):
        xs = np.linspace(PLATE_X_LEFT, PLATE_X_RIGHT, x_samples)
        pts = []
        for x in xs:
            delta = bl_thickness(x)
            pts.append([x, WALL_Y + delta, 0])
        curve = VMobject()
        curve.set_points_smoothly([np.array(p) for p in pts])
        curve.set_stroke(BL_EDGE_COL, width=2.2, opacity=0.85)
        return curve

    def _make_bl_fill(self, x_samples=80):
        xs = np.linspace(PLATE_X_LEFT, PLATE_X_RIGHT, x_samples)
        top_pts = [[x, WALL_Y + bl_thickness(x), 0] for x in xs]
        bot_pts = [[x, WALL_Y, 0] for x in reversed(xs)]
        all_pts = top_pts + bot_pts
        fill = VMobject()
        fill.set_points_smoothly([np.array(p) for p in all_pts])
        fill.close_path()
        fill.set_fill(BL_COLOR, opacity=0.14)
        fill.set_stroke(width=0)
        return fill

    # ╔══════════════════════════════════════════════════════╗
    # ║  PART 1 — Uniform Approach  (0–12 s)                ║
    # ╚══════════════════════════════════════════════════════╝
    def _part1_uniform_approach(self):
        cap = Text(
            "Fluid approaches a surface.",
            font_size=26, color=TEXT_WHITE, slant=ITALIC,
        ).to_edge(UP, buff=0.45)
        cap.set_stroke(BLACK, width=3, background=True)

        # Uniform streamlines — full screen width
        uniform_seeds = [(-7, y) for y in np.linspace(WALL_Y + 0.18, 3.6, 18)]
        unif_streams = VGroup()
        for sx, sy in uniform_seeds:
            pts = [[x, sy, 0] for x in np.linspace(sx, 7.2, 160)]
            path = VMobject()
            path.set_points_smoothly([np.array(p) for p in pts])
            path.set_stroke(FLUID_BLUE, width=1.3, opacity=0.45)
            unif_streams.add(path)

        self.play(
            FadeIn(cap, shift=DOWN * 0.1),
            Create(unif_streams, lag_ratio=0.02),
            run_time=2.0, rate_func=smooth,
        )

        wall_line, wall_fill = self._make_wall()
        self.play(
            FadeIn(wall_fill),
            Create(wall_line),
            run_time=1.0,
        )

        # FIX: arrows spread across FULL plate width and FULL height
        xs_unif = np.linspace(PLATE_X_LEFT + 0.3, PLATE_X_RIGHT - 0.3, 10)
        ys_unif = np.linspace(WALL_Y + 0.32, 3.2, 7)
        unif_arrows = VGroup()
        for x in xs_unif:
            for y in ys_unif:
                arr = Arrow(
                    [x, y, 0], [x + 0.50, y, 0],
                    buff=0, stroke_width=1.6,
                    tip_length=0.09, color=ARROW_COLOR,
                )
                arr.set_opacity(0.68)
                unif_arrows.add(arr)

        self.play(
            FadeIn(unif_arrows, lag_ratio=0.015),
            run_time=1.8, rate_func=smooth,
        )
        self.wait(3.5)
        self.play(FadeOut(cap), run_time=0.5)

        self._unif_streams = unif_streams
        self._unif_arrows  = unif_arrows
        self._wall_line    = wall_line
        self._wall_fill    = wall_fill

    # ╔══════════════════════════════════════════════════════╗
    # ║  PART 2 — No-Slip Condition  (12–25 s)              ║
    # ╚══════════════════════════════════════════════════════╝
    def _part2_no_slip(self):
        cap1 = Text(
            "Velocity at surface = 0",
            font_size=28, color=HIGHLIGHT_YEL, weight=BOLD,
        ).to_edge(UP, buff=0.45)
        cap1.set_stroke(BLACK, width=3, background=True)
        self.play(FadeIn(cap1, shift=DOWN * 0.1), run_time=0.8)

        # Profile arrows at a comfortable x position
        prof_x = PLATE_X_LEFT + 1.5
        prof_arrows_early = profile_arrows_at_x(prof_x, n=12,
                                                 max_height=2.2, scale=0.70)
        self.play(
            FadeIn(prof_arrows_early, lag_ratio=0.08),
            run_time=1.8, rate_func=smooth,
        )

        # u=0 label placed clearly below wall, not overlapping plate
        zero_label = MathTex(r"u = 0", font_size=26, color=HIGHLIGHT_YEL)
        zero_label.move_to([prof_x - 0.3, WALL_Y - 0.38, 0])
        zero_label.set_stroke(BLACK, width=2, background=True)
        self.play(FadeIn(zero_label, shift=UP * 0.1), run_time=0.6)

        # No-slip box — placed on right side away from profile arrows
        noslip_box = RoundedRectangle(
            width=3.1, height=0.60,
            corner_radius=0.14, color=CYAN_GLOW, stroke_width=1.0,
        )
        noslip_box.set_fill(BLACK, opacity=0.55)
        noslip_box.move_to([3.5, WALL_Y - 0.55, 0])
        noslip_lbl = Text(
            "No-slip condition", font_size=19, color=CYAN_GLOW,
        ).move_to(noslip_box)
        noslip_lbl.set_stroke(BLACK, width=2, background=True)

        self.play(
            FadeIn(noslip_box),
            FadeIn(noslip_lbl),
            run_time=0.8,
        )

        explain = Text(
            "The fluid sticks to the surface — viscosity holds it.",
            font_size=21, color=TEXT_WHITE, slant=ITALIC,
        ).to_edge(DOWN, buff=0.50)
        explain.set_stroke(BLACK, width=3, background=True)
        self.play(FadeIn(explain, shift=UP * 0.1), run_time=0.8)
        self.wait(4.5)

        self.play(
            FadeOut(cap1),
            FadeOut(explain),
            run_time=0.5,
        )

        self._prof_arrows_early = prof_arrows_early
        self._zero_label        = zero_label
        self._noslip_box        = noslip_box
        self._noslip_lbl        = noslip_lbl

    # ╔══════════════════════════════════════════════════════╗
    # ║  PART 3 — Boundary Layer Formation  (25–40 s)       ║
    # ╚══════════════════════════════════════════════════════╝
    def _part3_bl_formation(self):
        self.play(
            FadeOut(self._unif_streams),
            FadeOut(self._unif_arrows),
            FadeOut(self._prof_arrows_early),
            FadeOut(self._zero_label),
            run_time=0.8,
        )

        cap_bl = Text(
            "A thin region forms near the surface.",
            font_size=26, color=TEXT_WHITE, slant=ITALIC,
        ).to_edge(UP, buff=0.45)
        cap_bl.set_stroke(BLACK, width=3, background=True)
        self.play(FadeIn(cap_bl, shift=DOWN * 0.1), run_time=0.8)

        seeds_full = [(-7, WALL_Y + 0.08 + k)
                      for k in np.linspace(0.06, 4.0, 20)]
        full_streams = make_streamlines_plate(
            seeds_full, steps=200, dt=0.055,
            stroke_w=1.3, opacity=0.45,
        )
        self.play(
            Create(full_streams, lag_ratio=0.025),
            run_time=2.2, rate_func=smooth,
        )

        bl_fill  = self._make_bl_fill()
        bl_curve = self._make_bl_edge_curve()

        self.play(FadeIn(bl_fill), run_time=1.0)
        self.play(Create(bl_curve), run_time=1.2, rate_func=smooth)

        # δ brace at right edge
        brace_x = PLATE_X_RIGHT - 0.5
        delta_thick = bl_thickness(brace_x)
        brace = BraceBetweenPoints(
            [brace_x, WALL_Y, 0],
            [brace_x, WALL_Y + delta_thick, 0],
            direction=RIGHT,
        )
        brace.set_color(BL_EDGE_COL)
        delta_lbl = MathTex(r"\delta", font_size=30, color=BL_EDGE_COL)
        delta_lbl.next_to(brace, RIGHT, buff=0.15)
        delta_lbl.set_stroke(BLACK, width=2, background=True)

        self.play(Create(brace), FadeIn(delta_lbl), run_time=0.8)

        # Profile columns at 3 x positions
        profile_xs = [PLATE_X_LEFT + 1.5,
                      PLATE_X_LEFT + 3.5,
                      PLATE_X_LEFT + 5.5]
        all_profiles = VGroup()
        for px in profile_xs:
            prof = profile_arrows_at_x(px, n=11,
                                        max_height=BL_MAX_THICK + 0.6,
                                        scale=0.65)
            all_profiles.add(prof)

        self.play(
            LaggedStart(*[FadeIn(p, lag_ratio=0.06)
                          for p in all_profiles],
                        lag_ratio=0.35),
            run_time=2.5, rate_func=smooth,
        )

        # FIX: "Boundary Layer" label moved to centre of BL region,
        # shifted right so it doesn't sit on the left where profiles cluster
        bl_name_lbl = Text(
            "Boundary Layer", font_size=20, color=BL_EDGE_COL, weight=BOLD,
        )
        bl_name_lbl.move_to([2.5, WALL_Y + BL_MAX_THICK * 0.55, 0])
        bl_name_lbl.set_stroke(BLACK, width=3, background=True)
        self.play(FadeIn(bl_name_lbl, shift=UP * 0.08), run_time=0.7)
        self.wait(3.0)

        self.play(FadeOut(cap_bl), run_time=0.4)

        self._full_streams  = full_streams
        self._bl_fill       = bl_fill
        self._bl_curve      = bl_curve
        self._brace         = brace
        self._delta_lbl     = delta_lbl
        self._all_profiles  = all_profiles
        self._bl_name_lbl   = bl_name_lbl

    # ╔══════════════════════════════════════════════════════╗
    # ║  PART 4 — δ/L ≪ 1  (40–50 s)                       ║
    # ╚══════════════════════════════════════════════════════╝
    def _part4_delta_over_L(self):
        self.play(
            FadeOut(self._all_profiles),
            FadeOut(self._noslip_box),
            FadeOut(self._noslip_lbl),
            run_time=0.6,
        )

        L_arrow = DoubleArrow(
            [PLATE_X_LEFT, WALL_Y - 0.70, 0],
            [PLATE_X_RIGHT, WALL_Y - 0.70, 0],
            buff=0, stroke_width=1.8,
            tip_length=0.14, color=WALL_COLOR,
        )
        L_lbl = MathTex(r"L", font_size=28, color=WALL_COLOR)
        L_lbl.next_to(L_arrow, DOWN, buff=0.15)
        L_lbl.set_stroke(BLACK, width=2, background=True)

        self.play(Create(L_arrow), FadeIn(L_lbl), run_time=1.0)

        self.play(
            self._delta_lbl.animate.scale(1.25).set_color(HIGHLIGHT_YEL),
            run_time=0.6,
        )
        self.play(
            self._delta_lbl.animate.scale(1/1.25).set_color(BL_EDGE_COL),
            run_time=0.4,
        )

        # FIX: ratio equation placed on LEFT side to stay within frame
        ratio_eq = MathTex(
            r"\frac{\delta}{L}",
            r"\ll",
            r"1",
            font_size=46, color=WHITE,
        )
        ratio_eq.move_to(UP * 2.0 + LEFT * 2.5)
        ratio_eq.set_stroke(BLACK, width=3, background=True)

        ratio_box = SurroundingRectangle(
            ratio_eq, corner_radius=0.16,
            color=CYAN_GLOW, stroke_width=1.0, buff=0.22,
        )
        ratio_box.set_fill(BLACK, opacity=0.50)

        self.play(FadeIn(ratio_box), Write(ratio_eq), run_time=1.2)

        lbl_delta = Text("boundary layer thickness",
                         font_size=16, color=BL_EDGE_COL)
        lbl_L     = Text("plate length",
                         font_size=16, color=WALL_COLOR)
        lbl_delta.next_to(ratio_eq, DOWN, buff=0.35).shift(LEFT * 0.4)
        lbl_L.next_to(lbl_delta, DOWN, buff=0.22).align_to(lbl_delta, LEFT)
        lbl_delta.set_stroke(BLACK, width=2, background=True)
        lbl_L.set_stroke(BLACK, width=2, background=True)

        self.play(FadeIn(lbl_delta), run_time=0.5)
        self.play(FadeIn(lbl_L),     run_time=0.5)
        self.wait(3.5)

        self.play(
            FadeOut(L_arrow), FadeOut(L_lbl),
            FadeOut(lbl_delta), FadeOut(lbl_L),
            run_time=0.6,
        )

        self._ratio_eq  = ratio_eq
        self._ratio_box = ratio_box

    # ╔══════════════════════════════════════════════════════╗
    # ║  PART 5 — Gradient Insight  (50–60 s)               ║
    # ╚══════════════════════════════════════════════════════╝
    def _part5_gradient_insight(self):
        self.play(
            FadeOut(self._ratio_eq),
            FadeOut(self._ratio_box),
            run_time=0.5,
        )

        # FIX: Use two separate captions on opposite sides so they don't overlap
        grad_cap = Text(
            "Flow changes rapidly across the layer…",
            font_size=24, color=TEXT_WHITE, slant=ITALIC,
        ).to_edge(UP, buff=0.45)
        grad_cap.set_stroke(BLACK, width=3, background=True)
        self.play(FadeIn(grad_cap, shift=DOWN * 0.1), run_time=0.8)

        # FIX: vertical gradient arrow on LEFT side, well separated from BL label
        x_show = PLATE_X_LEFT + 1.0
        delta_here = bl_thickness(x_show)
        v_grad_arrow = Arrow(
            [x_show, WALL_Y + 0.05, 0],
            [x_show, WALL_Y + delta_here, 0],
            buff=0, stroke_width=2.4,
            tip_length=0.14, color=CYAN_GLOW,
        )
        # Label to the RIGHT of left-side arrow so it doesn't go off-screen
        v_grad_lbl = MathTex(
            r"\frac{\partial u}{\partial y} \ \text{large}",
            font_size=22, color=CYAN_GLOW,
        )
        v_grad_lbl.next_to(v_grad_arrow, RIGHT, buff=0.20)
        v_grad_lbl.set_stroke(BLACK, width=2, background=True)

        self.play(Create(v_grad_arrow), FadeIn(v_grad_lbl), run_time=1.0)
        self.wait(1.2)

        grad_cap2 = Text(
            "…but slowly along the surface.",
            font_size=24, color=ARROW_COLOR, slant=ITALIC,
        ).next_to(grad_cap, DOWN, buff=0.25)
        grad_cap2.set_stroke(BLACK, width=3, background=True)
        self.play(FadeIn(grad_cap2, shift=DOWN * 0.1), run_time=0.7)

        # FIX: horizontal gradient arrow placed in FREE STREAM area (above BL),
        # centred horizontally, label ABOVE it — well away from BL label
        y_free = WALL_Y + BL_MAX_THICK + 1.0   # clearly above BL edge
        h_grad_arrow = Arrow(
            [-1.5, y_free, 0],
            [1.5, y_free, 0],
            buff=0, stroke_width=1.6,
            tip_length=0.10, color=FADED_GRAY,
        )
        h_grad_lbl = MathTex(
            r"\frac{\partial u}{\partial x} \ \text{small}",
            font_size=22, color=FADED_GRAY,
        )
        # FIX: label set to WHITE-ish so it is visible on dark background
        h_grad_lbl.set_color("#8899AA")
        h_grad_lbl.next_to(h_grad_arrow, UP, buff=0.22)
        h_grad_lbl.set_stroke(BLACK, width=2, background=True)

        self.play(Create(h_grad_arrow), FadeIn(h_grad_lbl), run_time=1.0)
        self.wait(3.5)

        implication = Text(
            "This asymmetry is what makes simplification possible.",
            font_size=21, color=HIGHLIGHT_YEL, slant=ITALIC,
        ).to_edge(DOWN, buff=0.50)
        implication.set_stroke(BLACK, width=3, background=True)
        self.play(FadeIn(implication, shift=UP * 0.1), run_time=0.8)
        self.wait(2.0)

        self.play(
            FadeOut(grad_cap), FadeOut(grad_cap2),
            FadeOut(v_grad_arrow), FadeOut(v_grad_lbl),
            FadeOut(h_grad_arrow), FadeOut(h_grad_lbl),
            FadeOut(implication),
            run_time=0.8,
        )

    # ╔══════════════════════════════════════════════════════╗
    # ║  PART 6 — Equation Reduction  (60–80 s)             ║
    # ╚══════════════════════════════════════════════════════╝
    def _part6_equation_reduction(self):
        self.play(
            self._full_streams.animate.set_opacity(0.12),
            self._bl_fill.animate.set_opacity(0.06),
            self._bl_curve.animate.set_opacity(0.20),
            self._brace.animate.set_opacity(0.20),
            self._delta_lbl.animate.set_opacity(0.20),
            self._bl_name_lbl.animate.set_opacity(0.20),
            run_time=1.0,
        )

        eq_cap = Text(
            "Now let us simplify the Navier–Stokes equation.",
            font_size=24, color=TEXT_WHITE, slant=ITALIC,
        ).to_edge(UP, buff=0.45)
        eq_cap.set_stroke(BLACK, width=3, background=True)
        self.play(FadeIn(eq_cap, shift=DOWN * 0.1), run_time=0.8)

        # Full Navier–Stokes — font 28 to ensure it fits within frame width
        full_ns = MathTex(
            r"\rho",
            r"\!\left(",
            r"\frac{\partial u}{\partial t}",
            r"+",
            r"(\vec{v} \cdot \nabla)u",
            r"\right)",
            r"=",
            r"-\frac{\partial p}{\partial x}",
            r"+",
            r"\mu\!\left(",
            r"\frac{\partial^2 u}{\partial x^2}",
            r"+",
            r"\frac{\partial^2 u}{\partial y^2}",
            r"\right)",
            font_size=28, color=WHITE,
        )
        full_ns.move_to(UP * 1.2)
        # Ensure the equation doesn't exceed frame width
        if full_ns.width > 12.5:
            full_ns.scale(12.5 / full_ns.width)
        full_ns.set_stroke(BLACK, width=3, background=True)

        ns_box = SurroundingRectangle(
            full_ns, corner_radius=0.15,
            color=CYAN_GLOW, stroke_width=0.9, buff=0.20,
        )
        ns_box.set_fill(BLACK, opacity=0.50)

        self.play(FadeIn(ns_box), run_time=0.4)
        self.play(Write(full_ns), run_time=2.0, rate_func=smooth)
        self.wait(0.8)

        # Camera zoom in on equation
        self.play(
            self.camera.frame.animate
                .scale(0.82)
                .move_to(full_ns.get_center() + DOWN * 0.3),
            run_time=1.2, rate_func=smooth,
        )

        # Step 1: drop ∂u/∂t
        step1_lbl = Text(
            "Steady flow → drop time derivative",
            font_size=18, color=FADED_GRAY, slant=ITALIC,
        ).to_edge(DOWN, buff=0.40)
        step1_lbl.set_stroke(BLACK, width=2, background=True)
        self.play(FadeIn(step1_lbl, shift=UP * 0.08), run_time=0.6)

        self.play(
            full_ns[2].animate.set_color(REMOVED_COL).set_opacity(0.18),
            full_ns[3].animate.set_color(REMOVED_COL).set_opacity(0.18),
            run_time=1.0, rate_func=smooth,
        )
        self.wait(1.0)

        # Step 2: drop ∂²u/∂x²
        self.play(FadeOut(step1_lbl), run_time=0.3)
        step2_lbl = Text(
            "δ/L ≪ 1  →  ∂²u/∂x²  negligible vs  ∂²u/∂y²",
            font_size=17, color=FADED_GRAY, slant=ITALIC,
        ).to_edge(DOWN, buff=0.40)
        step2_lbl.set_stroke(BLACK, width=2, background=True)
        self.play(FadeIn(step2_lbl, shift=UP * 0.08), run_time=0.6)

        self.play(
            full_ns[12].animate.set_color(DOMINANT_COL),
            run_time=0.7,
        )
        self.wait(0.5)

        self.play(
            full_ns[10].animate.set_color(REMOVED_COL).set_opacity(0.18),
            full_ns[11].animate.set_color(REMOVED_COL).set_opacity(0.18),
            run_time=1.0, rate_func=smooth,
        )
        self.wait(1.2)

        for idx in [0, 1, 4, 5, 6, 7, 8, 9, 12, 13]:
            full_ns[idx].set_color(DOMINANT_COL)

        self.play(FadeOut(step2_lbl), run_time=0.3)

        # Final boundary layer equation
        bl_eq = MathTex(
            r"u\frac{\partial u}{\partial x}",
            r"+",
            r"v\frac{\partial u}{\partial y}",
            r"=",
            r"-\frac{1}{\rho}\frac{\partial p}{\partial x}",
            r"+",
            r"\nu\frac{\partial^2 u}{\partial y^2}",
            font_size=34, color=WHITE,
        )
        bl_eq.next_to(full_ns, DOWN, buff=0.55)
        # FIX: clamp width so it stays within the zoomed frame
        if bl_eq.width > 10.0:
            bl_eq.scale(10.0 / bl_eq.width)
        bl_eq.set_stroke(BLACK, width=3, background=True)

        arr_implies = Arrow(
            full_ns.get_bottom() + DOWN * 0.08,
            bl_eq.get_top() + UP * 0.08,
            buff=0.08, stroke_width=1.8,
            tip_length=0.12, color=CYAN_GLOW,
        )

        # FIX: "Boundary layer equation" label placed BELOW the eq, not to the
        # right where it clips off-screen
        eq_cap2 = Text(
            "Boundary layer equation",
            font_size=19, color=CYAN_GLOW, weight=BOLD,
        )
        eq_cap2.next_to(bl_eq, DOWN, buff=0.22)
        eq_cap2.set_stroke(BLACK, width=2, background=True)

        self.play(GrowArrow(arr_implies), run_time=0.7)
        self.play(Write(bl_eq), run_time=1.8, rate_func=smooth)
        self.play(FadeIn(eq_cap2, shift=UP * 0.1), run_time=0.6)
        self.wait(0.5)

        # Term labels for BL equation — arranged in a compact row below
        term_lbls_data = [
            (0, "u (x-vel)", DOMINANT_COL),
            (2, "v (y-vel)", DOMINANT_COL),
            (4, "pressure gradient", HIGHLIGHT_YEL),
            (6, "ν (viscosity)", CYAN_GLOW),
        ]
        term_lbls = VGroup()
        for idx, meaning, col in term_lbls_data:
            bl_eq[idx].set_color(col)
            lbl = Text(meaning, font_size=13, color=col)
            lbl.next_to(bl_eq[idx], DOWN, buff=0.55)
            lbl.set_stroke(BLACK, width=2, background=True)
            self.play(FadeIn(lbl, shift=UP * 0.06), run_time=0.35)
            term_lbls.add(lbl)

        self.wait(3.0)
        self.play(
            FadeOut(eq_cap),
            FadeOut(term_lbls),
            FadeOut(eq_cap2),
            run_time=0.6,
        )

        self._full_ns     = full_ns
        self._ns_box      = ns_box
        self._bl_eq       = bl_eq
        self._arr_implies = arr_implies

    # ╔══════════════════════════════════════════════════════╗
    # ║  PART 7 — Final Understanding  (80–92 s)            ║
    # ╚══════════════════════════════════════════════════════╝
    def _part7_final(self):
        # Restore camera to full view
        self.play(
            self.camera.frame.animate
                .set_width(self._base_width)
                .move_to(ORIGIN),
            self._full_streams.animate.set_opacity(0.35),
            self._bl_fill.animate.set_opacity(0.13),
            self._bl_curve.animate.set_opacity(0.70),
            self._brace.animate.set_opacity(0.80),
            self._delta_lbl.animate.set_opacity(0.90),
            run_time=2.0, rate_func=smooth,
        )

        # Shift equations to right side
        eq_group = VGroup(
            self._full_ns, self._ns_box,
            self._bl_eq, self._arr_implies,
        )
        self.play(
            eq_group.animate.scale(0.72).to_edge(RIGHT, buff=0.30).shift(UP * 0.4),
            run_time=1.2, rate_func=smooth,
        )

        close1 = Text(
            "Viscosity dominates near the surface.",
            font_size=26, color=TEXT_WHITE, weight=BOLD,
        ).to_edge(UP, buff=0.45)
        close1.set_stroke(BLACK, width=3, background=True)

        close2 = Text(
            "Flow can now be simplified and solved.",
            font_size=26, color=CYAN_GLOW, weight=BOLD,
        ).next_to(close1, DOWN, buff=0.30)
        close2.set_stroke(BLACK, width=3, background=True)

        self.play(FadeIn(close1, shift=DOWN * 0.1), run_time=0.9)
        self.play(FadeIn(close2, shift=DOWN * 0.1), run_time=0.9)
        self.wait(1.5)

        # Final summary box
        summary_lines = VGroup(
            Text("Physics first:  no-slip → gradient → thin layer",
                 font_size=18, color=ARROW_COLOR),
            Text("Math follows:  ∂²u/∂x² disappears,  ∂²u/∂y² dominates",
                 font_size=18, color=ARROW_COLOR),
            Text("Result: a tractable equation for real engineering.",
                 font_size=18, color=HIGHLIGHT_YEL),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)

        summary_box = SurroundingRectangle(
            summary_lines, corner_radius=0.16,
            color=FADED_GRAY, stroke_width=0.8, buff=0.28,
        )
        summary_box.set_fill(BLACK, opacity=0.60)

        summary_group = VGroup(summary_box, summary_lines)
        summary_group.to_edge(DOWN, buff=0.40)
        summary_group.set_stroke(BLACK, width=2, background=True)

        self.play(FadeIn(summary_box), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(l, shift=UP * 0.08) for l in summary_lines],
                        lag_ratio=0.30),
            run_time=1.5,
        )
        self.wait(3.5)

        # Fade everything to black
        all_objects = VGroup(
            close1, close2,
            summary_group,
            eq_group,
            self._full_streams,
            self._bl_fill,
            self._bl_curve,
            self._brace,
            self._delta_lbl,
            self._bl_name_lbl,
            self._wall_line,
            self._wall_fill,
        )
        self.play(
            FadeOut(all_objects),
            run_time=2.5, rate_func=smooth,
        )
        self.wait(0.5)