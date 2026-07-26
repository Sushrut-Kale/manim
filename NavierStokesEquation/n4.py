from manim import *
import numpy as np

# ─────────────────────────────────────────────
#  Global style constants
# ─────────────────────────────────────────────
BG_COLOR    = "#0A0A0F"
FLUID_BLUE  = "#1E90FF"
FLUID_DARK  = "#0A2A6E"
ARROW_COLOR = "#A8D8FF"
GRID_COLOR  = "#1A2A3A"
CYAN_GLOW   = "#00E5FF"
TEXT_COLOR  = WHITE
HIGH_PRES   = "#FF3030"   # red   → high pressure
LOW_PRES    = "#1040C0"   # blue  → low pressure
HIGHLIGHT   = "#FFD700"   # gold  → element highlight


# ─────────────────────────────────────────────
#  Velocity field helpers
# ─────────────────────────────────────────────
def smooth_flow(x, y, t=0.0):
    """Gentle laminar base flow."""
    vx = 1.0 + 0.3 * np.sin(0.8 * y + t)
    vy = 0.15 * np.sin(1.2 * x + 0.5 * y + t)
    return np.array([vx, vy, 0])


def turbulent_flow(x, y, t=0.0, strength=1.0):
    """Laminar flow + multi-scale turbulent perturbations."""
    vx = 1.0 + 0.3 * np.sin(0.8 * y + t)
    vy = 0.15 * np.sin(1.2 * x + 0.5 * y + t)
    # Add turbulent kicks
    vx += strength * (0.4 * np.sin(2.3 * x + 1.7 * y + t * 1.3)
                    + 0.25 * np.sin(4.1 * x - 2.9 * y + t * 2.1))
    vy += strength * (0.35 * np.cos(1.9 * x + 3.1 * y + t * 1.7)
                    + 0.20 * np.cos(3.7 * x - 1.5 * y + t * 2.5))
    return np.array([vx, vy, 0])


def pressure_field(x, y):
    """Fake pressure scalar: higher on left, lower on right + variation."""
    return 1.5 - 0.4 * x + 0.3 * np.sin(0.9 * y) + 0.2 * np.cos(1.1 * x)


def speed_color_ns(speed, vmin=0.3, vmax=2.5):
    t = float(np.clip((speed - vmin) / (vmax - vmin), 0, 1))
    return interpolate_color(ManimColor(FLUID_DARK), ManimColor(CYAN_GLOW), t)


def pressure_color(p, pmin=0.5, pmax=2.5):
    t = float(np.clip((p - pmin) / (pmax - pmin), 0, 1))
    return interpolate_color(ManimColor(LOW_PRES), ManimColor(HIGH_PRES), t)


# ─────────────────────────────────────────────
#  Reusable builders
# ─────────────────────────────────────────────
def make_arrows(vel_func, xs, ys, scale=0.30, colored=False, t=0.0, opacity=0.75):
    group = VGroup()
    for x in xs:
        for y in ys:
            v   = vel_func(x, y, t) if callable(vel_func) else vel_func(x, y)
            spd = np.linalg.norm(v[:2])
            if spd < 1e-4:
                continue
            d   = v / spd
            l   = float(np.clip(spd * scale, 0.05, 0.55))
            col = speed_color_ns(spd) if colored else ManimColor(ARROW_COLOR)
            arr = Arrow(
                [x, y, 0], [x + d[0]*l, y + d[1]*l, 0],
                buff=0, stroke_width=1.8, tip_length=0.10, color=col,
            )
            arr.set_opacity(opacity)
            group.add(arr)
    return group


def make_streamlines(vel_func, seeds, steps=120, dt=0.065,
                     stroke_w=1.4, opacity=0.50, colored=False, t=0.0):
    lines = VGroup()
    for sx, sy in seeds:
        pts = []
        x, y = sx, sy
        for _ in range(steps):
            pts.append([x, y, 0])
            v  = vel_func(x, y, t) if callable(vel_func) else vel_func(x, y)
            nm = max(np.linalg.norm(v[:2]), 1e-6)
            x += v[0] / nm * dt
            y += v[1] / nm * dt
            if abs(x) > 7.8 or abs(y) > 4.8:
                break
        if len(pts) < 3:
            continue
        path = VMobject()
        path.set_points_smoothly([np.array(p) for p in pts])
        if colored and len(pts) > 2:
            mid = pts[len(pts)//2]
            v   = vel_func(mid[0], mid[1], t) if callable(vel_func) else vel_func(mid[0], mid[1])
            col = speed_color_ns(np.linalg.norm(v[:2]))
        else:
            col = ManimColor(FLUID_BLUE)
        path.set_stroke(col, width=stroke_w, opacity=opacity)
        lines.add(path)
    return lines


def subtitle(text, size=24, color=TEXT_COLOR, italic=True):
    """Helper: styled subtitle with background stroke."""
    t = Text(text, font_size=size, color=color,
             slant=ITALIC if italic else NORMAL)
    t.set_stroke(BLACK, width=3, background=True)
    return t


# ─────────────────────────────────────────────
#  Main Scene
# ─────────────────────────────────────────────
class Scene4_MathToEquation(MovingCameraScene):

    def construct(self):
        self.camera.background_color = BG_COLOR
        self._fw = self.camera.frame.width   # default frame width

        self._part1_complexity()        #  0–12 s
        self._part2_overwhelming()      # 12–20 s
        self._part3_fields()            # 20–30 s
        self._part4_mass_conservation() # 30–40 s
        self._part5_newtons_law()       # 40–50 s
        self._part6_navier_stokes()     # 50–60 s

    # ══════════════════════════════════════════════
    #  PART 1 — Complexity of Flow  (0–12 s)
    # ══════════════════════════════════════════════
    def _part1_complexity(self):
        seeds = [(-7, y) for y in np.linspace(-3.8, 3.8, 20)]
        xs = np.linspace(-6, 6, 10)
        ys = np.linspace(-3.5, 3.5, 7)

        # Start with smooth laminar flow
        streams_smooth = make_streamlines(smooth_flow, seeds, opacity=0.45)
        arrows_smooth  = make_arrows(smooth_flow, xs, ys, scale=0.28)

        self.play(
            Create(streams_smooth, lag_ratio=0.03),
            run_time=2.0, rate_func=smooth,
        )
        self.play(FadeIn(arrows_smooth, lag_ratio=0.02), run_time=1.0)

        # Line 1
        t1 = subtitle("This motion is complex.").to_edge(DOWN, buff=0.5)
        self.play(FadeIn(t1, shift=UP*0.1), run_time=0.7)
        self.wait(1.2)

        # Transition: smooth → turbulent (morph streamlines + arrows)
        streams_turb = make_streamlines(
            lambda x, y, t=0: turbulent_flow(x, y, t=0, strength=0.5),
            seeds, steps=130, dt=0.06, opacity=0.45,
        )
        arrows_turb = make_arrows(
            lambda x, y, t=0: turbulent_flow(x, y, t=0, strength=0.5),
            xs, ys, scale=0.28, colored=True,
        )

        self.play(
            FadeOut(streams_smooth),
            FadeOut(arrows_smooth),
            run_time=0.6,
        )
        self.play(
            Create(streams_turb, lag_ratio=0.03),
            FadeIn(arrows_turb, lag_ratio=0.02),
            run_time=2.0, rate_func=smooth,
        )

        # Line 2
        t2 = subtitle("It changes everywhere…").to_edge(DOWN, buff=0.5)
        self.play(FadeOut(t1), FadeIn(t2, shift=UP*0.1), run_time=0.7)
        self.wait(1.0)

        # More turbulent snapshot (t=1.5)
        streams_turb2 = make_streamlines(
            lambda x, y, t=0: turbulent_flow(x, y, t=1.5, strength=0.8),
            seeds, steps=130, dt=0.06, opacity=0.45,
        )
        arrows_turb2 = make_arrows(
            lambda x, y, t=0: turbulent_flow(x, y, t=1.5, strength=0.8),
            xs, ys, scale=0.28, colored=True,
        )
        self.play(
            FadeOut(streams_turb), FadeOut(arrows_turb),
            run_time=0.5,
        )
        self.play(
            Create(streams_turb2, lag_ratio=0.03),
            FadeIn(arrows_turb2, lag_ratio=0.02),
            run_time=1.5, rate_func=smooth,
        )

        # Line 3
        t3 = subtitle("It changes every moment…").to_edge(DOWN, buff=0.5)
        self.play(FadeOut(t2), FadeIn(t3, shift=UP*0.1), run_time=0.7)
        self.wait(1.5)

        self.play(FadeOut(t3), run_time=0.5)

        # Store for next part
        self._streams = streams_turb2
        self._arrows  = arrows_turb2

    # ══════════════════════════════════════════════
    #  PART 2 — Overwhelming Visual  (12–20 s)
    # ══════════════════════════════════════════════
    def _part2_overwhelming(self):
        seeds_dense = [(-7, y) for y in np.linspace(-3.8, 3.8, 32)]
        xs_dense = np.linspace(-6, 6, 13)
        ys_dense = np.linspace(-3.5, 3.5, 10)

        streams_dense = make_streamlines(
            lambda x, y, t=0: turbulent_flow(x, y, t=2.0, strength=0.9),
            seeds_dense, steps=130, dt=0.055,
            stroke_w=1.2, opacity=0.40, colored=True,
        )
        arrows_dense = make_arrows(
            lambda x, y, t=0: turbulent_flow(x, y, t=2.0, strength=0.9),
            xs_dense, ys_dense, scale=0.26, colored=True, opacity=0.70,
        )

        self.play(
            FadeOut(self._streams), FadeOut(self._arrows),
            run_time=0.5,
        )
        self.play(
            Create(streams_dense, lag_ratio=0.02),
            FadeIn(arrows_dense, lag_ratio=0.01),
            run_time=2.5, rate_func=smooth,
        )

        # Central question — large, glowing
        q = Text(
            "How do we describe this?",
            font_size=38, color=CYAN_GLOW, weight=BOLD,
        )
        q.set_stroke(BLACK, width=4, background=True)
        q.move_to(UP * 0.15)

        # Dim background first
        dimmer = Rectangle(
            width=16, height=10,
            fill_color=BLACK, fill_opacity=0.55, stroke_opacity=0,
        )
        self.play(FadeIn(dimmer), run_time=0.5)
        self.play(FadeIn(q, scale=1.05), run_time=1.0)
        self.wait(2.5)
        self.play(FadeOut(q), FadeOut(dimmer), run_time=0.8)

        # Clean up to sparse flow for Part 3
        self._streams = streams_dense
        self._arrows  = arrows_dense

    # ══════════════════════════════════════════════
    #  PART 3 — Introduce Fields  (20–30 s)
    # ══════════════════════════════════════════════
    def _part3_fields(self):
        # Reduce to clean sparse flow
        seeds_clean = [(-7, y) for y in np.linspace(-3.8, 3.8, 18)]
        xs = np.linspace(-6, 6, 10)
        ys = np.linspace(-3.5, 3.5, 7)

        streams_clean = make_streamlines(
            smooth_flow, seeds_clean, opacity=0.40, stroke_w=1.3,
        )
        arrows_clean = make_arrows(smooth_flow, xs, ys, scale=0.28,
                                   colored=True, opacity=0.70)

        self.play(
            FadeOut(self._streams), FadeOut(self._arrows),
            run_time=0.5,
        )
        self.play(
            Create(streams_clean, lag_ratio=0.03),
            FadeIn(arrows_clean, lag_ratio=0.02),
            run_time=1.5, rate_func=smooth,
        )

        # ── Velocity field label (top-left) ──
        vel_label = VGroup(
            Line(LEFT*0.3, RIGHT*0.3, color=ManimColor(CYAN_GLOW), stroke_width=2),
            Text("Velocity field  v(x,y,z,t)",
                 font_size=19, color=ManimColor(CYAN_GLOW)),
        ).arrange(RIGHT, buff=0.18)
        vel_label.to_corner(UL, buff=0.45)
        vel_label.set_stroke(BLACK, width=2, background=True)
        self.play(FadeIn(vel_label, shift=RIGHT*0.1), run_time=0.8)

        # ── Pressure field overlay — colored rectangles on a coarse grid ──
        pressure_cells = VGroup()
        cell_w, cell_h = 1.1, 0.85
        px_range = np.linspace(-5.5, 5.5, 11)
        py_range = np.linspace(-3.5, 3.5, 8)
        for px in px_range:
            for py in py_range:
                p   = pressure_field(px, py)
                col = pressure_color(p)
                cell = Rectangle(
                    width=cell_w, height=cell_h,
                    fill_color=col, fill_opacity=0.28,
                    stroke_opacity=0,
                )
                cell.move_to([px, py, 0])
                pressure_cells.add(cell)

        self.play(FadeIn(pressure_cells, lag_ratio=0.005), run_time=1.5,
                  rate_func=smooth)

        # Pressure gradient arrows (from high → low pressure)
        pgrad_arrows = VGroup()
        for px in np.linspace(-4.5, 4.5, 8):
            for py in np.linspace(-3.0, 3.0, 6):
                # Numerical gradient of pressure (negative = force direction)
                dp_dx = -(-0.4 + 0.2 * (-np.sin(1.1 * px)))
                dp_dy = -(0.3 * np.cos(0.9 * py))
                mag   = np.sqrt(dp_dx**2 + dp_dy**2) + 1e-6
                l     = 0.22
                arr = Arrow(
                    [px, py, 0],
                    [px + dp_dx/mag*l, py + dp_dy/mag*l, 0],
                    buff=0, stroke_width=1.4, tip_length=0.09,
                    color=ManimColor(HIGH_PRES),
                )
                arr.set_opacity(0.55)
                pgrad_arrows.add(arr)

        self.play(FadeIn(pgrad_arrows, lag_ratio=0.01), run_time=1.0)

        # ── Pressure label + color legend ──
        pres_label = Text("Pressure field  p(x,y,z,t)",
                          font_size=19, color=ManimColor(HIGH_PRES))
        pres_label.set_stroke(BLACK, width=2, background=True)
        pres_label.to_corner(UR, buff=0.45)

        legend_low  = Text("low", font_size=16, color=ManimColor(LOW_PRES))
        legend_high = Text("high", font_size=16, color=ManimColor(HIGH_PRES))
        legend_bar  = Rectangle(width=1.2, height=0.14, stroke_opacity=0)
        legend_bar.set_fill(
            color=[ManimColor(LOW_PRES), ManimColor(HIGH_PRES)],
            opacity=0.9,
        )
        legend = VGroup(legend_low, legend_bar, legend_high).arrange(RIGHT, buff=0.12)
        legend.next_to(pres_label, DOWN, buff=0.18).align_to(pres_label, RIGHT)
        legend.set_stroke(BLACK, width=2, background=True)

        self.play(FadeIn(pres_label), FadeIn(legend), run_time=0.8)
        self.wait(2.5)

        # Fade pressure overlay, keep velocity field
        self.play(
            FadeOut(pressure_cells),
            FadeOut(pgrad_arrows),
            FadeOut(pres_label),
            FadeOut(legend),
            run_time=1.0,
        )

        self._streams      = streams_clean
        self._arrows       = arrows_clean
        self._vel_label    = vel_label

    # ══════════════════════════════════════════════
    #  PART 4 — Mass Conservation  (30–40 s)
    # ══════════════════════════════════════════════
    def _part4_mass_conservation(self):
        # Dim background slightly
        dimmer = Rectangle(
            width=16, height=10,
            fill_color=BLACK, fill_opacity=0.45, stroke_opacity=0,
        )
        self.play(
            FadeIn(dimmer),
            FadeOut(self._vel_label),
            run_time=0.6,
        )

        # ── Control volume box ──
        box = Rectangle(
            width=2.8, height=2.2,
            color=ManimColor(CYAN_GLOW), stroke_width=2.2,
        )
        box.set_fill(ManimColor(CYAN_GLOW), opacity=0.07)
        box.move_to(ORIGIN)
        self.play(Create(box), run_time=0.8)

        # "Fluid entering" arrows on left face
        in_arrows = VGroup(*[
            Arrow(
                [-2.9, y, 0], [-1.4, y, 0],
                buff=0, stroke_width=2.2, tip_length=0.14,
                color=ManimColor(FLUID_BLUE),
            )
            for y in np.linspace(-0.7, 0.7, 4)
        ])
        # "Fluid exiting" arrows on right face
        out_arrows = VGroup(*[
            Arrow(
                [1.4, y, 0], [2.9, y, 0],
                buff=0, stroke_width=2.2, tip_length=0.14,
                color=ManimColor(CYAN_GLOW),
            )
            for y in np.linspace(-0.7, 0.7, 4)
        ])

        in_lbl  = Text("in", font_size=20, color=ManimColor(FLUID_BLUE))
        out_lbl = Text("out", font_size=20, color=ManimColor(CYAN_GLOW))
        in_lbl.next_to(in_arrows, LEFT, buff=0.1)
        out_lbl.next_to(out_arrows, RIGHT, buff=0.1)

        self.play(
            LaggedStart(
                FadeIn(in_arrows, lag_ratio=0.2),
                FadeIn(out_arrows, lag_ratio=0.2),
                lag_ratio=0.4,
            ),
            FadeIn(in_lbl), FadeIn(out_lbl),
            run_time=1.5, rate_func=smooth,
        )

        # Particle animation: dots travel through box
        def make_particles(color, x_start, x_end, count=5):
            dots = VGroup(*[
                Dot(
                    point=[x_start, np.random.uniform(-0.65, 0.65), 0],
                    radius=0.07, color=color,
                ).set_opacity(0.85)
                for _ in range(count)
            ])
            return dots

        np.random.seed(42)
        p_in  = make_particles(ManimColor(FLUID_BLUE), -2.0, 1.3)
        p_out = make_particles(ManimColor(CYAN_GLOW),  -1.3, 2.0)
        self.add(p_in, p_out)
        self.play(
            p_in.animate.shift(RIGHT * 3.3),
            p_out.animate.shift(RIGHT * 3.3),
            run_time=1.8, rate_func=linear,
        )
        self.remove(p_in, p_out)

        # ── Display ∇·v = 0 ──
        div_eq = MathTex(
            r"\nabla \cdot \vec{v} = 0",
            color=WHITE, font_size=52,
        )
        div_eq.set_stroke(BLACK, width=3, background=True)
        div_eq.to_edge(UP, buff=0.55)

        self.play(Write(div_eq), run_time=1.2)

        # Glow pulse on equation
        div_glow = div_eq.copy().set_color(ManimColor(CYAN_GLOW)).set_opacity(0.5)
        self.play(
            div_glow.animate.scale(1.05).set_opacity(0),
            run_time=0.8, rate_func=smooth,
        )
        self.remove(div_glow)

        # Explanation text
        exp1 = subtitle("No accumulation.", size=22, color=ManimColor(ARROW_COLOR))
        exp2 = subtitle("No disappearance.", size=22, color=ManimColor(ARROW_COLOR))
        mass_text = subtitle("Mass is conserved.", size=28, color=WHITE, italic=False)
        exp1.next_to(div_eq, DOWN, buff=0.35)
        exp2.next_to(exp1, DOWN, buff=0.22)
        mass_text.next_to(exp2, DOWN, buff=0.35)

        for txt in [exp1, exp2, mass_text]:
            self.play(FadeIn(txt, shift=UP*0.08), run_time=0.55)
        self.wait(1.8)

        self.play(
            FadeOut(VGroup(box, in_arrows, out_arrows, in_lbl, out_lbl)),
            FadeOut(VGroup(exp1, exp2, mass_text)),
            FadeOut(div_eq),
            FadeOut(dimmer),
            run_time=1.0,
        )

    # ══════════════════════════════════════════════
    #  PART 5 — Newton's Second Law  (40–50 s)
    # ══════════════════════════════════════════════
    def _part5_newtons_law(self):
        dimmer2 = Rectangle(
            width=16, height=10,
            fill_color=BLACK, fill_opacity=0.50, stroke_opacity=0,
        )
        self.play(FadeIn(dimmer2), run_time=0.5)

        # ── Fluid element (highlighted box) ──
        elem = Rectangle(
            width=1.6, height=1.2,
            color=ManimColor(HIGHLIGHT), stroke_width=2.5,
        )
        elem.set_fill(ManimColor(HIGHLIGHT), opacity=0.10)
        elem.move_to(ORIGIN)

        elem_lbl = Text("fluid element", font_size=18, color=ManimColor(HIGHLIGHT))
        elem_lbl.next_to(elem, DOWN, buff=0.18)
        elem_lbl.set_stroke(BLACK, width=2, background=True)

        self.play(Create(elem), FadeIn(elem_lbl), run_time=0.8)

        # Pressure force arrow (pushes right)
        p_force = Arrow(
            [-1.5, 0.2, 0], [-0.8, 0.2, 0],
            buff=0, stroke_width=2.5, tip_length=0.15,
            color=ManimColor(HIGH_PRES),
        )
        p_lbl = Text("pressure", font_size=17, color=ManimColor(HIGH_PRES))
        p_lbl.next_to(p_force, UP, buff=0.08)
        p_lbl.set_stroke(BLACK, width=2, background=True)

        # Viscosity resistance arrow (opposes motion)
        v_force = Arrow(
            [1.5, -0.2, 0], [0.8, -0.2, 0],
            buff=0, stroke_width=2.5, tip_length=0.15,
            color=ManimColor(ARROW_COLOR),
        )
        v_lbl = Text("viscosity", font_size=17, color=ManimColor(ARROW_COLOR))
        v_lbl.next_to(v_force, DOWN, buff=0.08)
        v_lbl.set_stroke(BLACK, width=2, background=True)

        self.play(
            GrowArrow(p_force), FadeIn(p_lbl),
            run_time=0.8,
        )
        self.play(
            GrowArrow(v_force), FadeIn(v_lbl),
            run_time=0.8,
        )
        self.wait(0.8)

        # ── F = ma  (Newton's 2nd) ──
        fma = MathTex(r"F = m\,a", color=WHITE, font_size=54)
        fma.set_stroke(BLACK, width=3, background=True)
        fma.to_edge(UP, buff=0.55)
        self.play(Write(fma), run_time=1.0)
        self.wait(0.8)

        # Transform to ρ · a = forces
        rho_a = MathTex(
            r"\rho \times \text{acceleration} = \text{forces}",
            color=WHITE, font_size=38,
        )
        rho_a.set_stroke(BLACK, width=3, background=True)
        rho_a.to_edge(UP, buff=0.55)

        self.play(
            TransformMatchingShapes(fma, rho_a),
            run_time=1.2, rate_func=smooth,
        )
        self.wait(1.5)

        self.play(
            FadeOut(VGroup(elem, elem_lbl, p_force, p_lbl, v_force, v_lbl)),
            FadeOut(rho_a),
            FadeOut(dimmer2),
            run_time=1.0,
        )

    # ══════════════════════════════════════════════
    #  PART 6 — Navier–Stokes Term by Term  (50–60s)
    # ══════════════════════════════════════════════
    def _part6_navier_stokes(self):
        # Dim everything behind the equation
        bg_dim = Rectangle(
            width=16, height=10,
            fill_color=BLACK, fill_opacity=0.65, stroke_opacity=0,
        )
        self.play(FadeIn(bg_dim), run_time=0.6)

        # ── Section header ──
        hdr = Text("Navier–Stokes Equation", font_size=26,
                   color=ManimColor(CYAN_GLOW), weight=BOLD)
        hdr.set_stroke(BLACK, width=3, background=True)
        hdr.to_edge(UP, buff=0.40)
        self.play(FadeIn(hdr, shift=DOWN*0.1), run_time=0.7)

        # ── Build equation term by term ──
        # We render each stage as a separate MathTex and cross-fade.
        # Terms:
        #   LHS: ρ (∂v/∂t + (v·∇)v)
        #   RHS: -∇p + μ∇²v + f

        cfg = {"color": WHITE, "font_size": 46}

        # Stage 0: just ρ ∂v/∂t
        eq0 = MathTex(
            r"\rho \frac{\partial \vec{v}}{\partial t}",
            **cfg,
        )

        # Stage 1: add advection term
        eq1 = MathTex(
            r"\rho \!\left(\frac{\partial \vec{v}}{\partial t}"
            r"+ (\vec{v} \cdot \nabla)\vec{v}\right)",
            **cfg,
        )

        # Stage 2: add equals sign + pressure term
        eq2 = MathTex(
            r"\rho \!\left(\frac{\partial \vec{v}}{\partial t}"
            r"+ (\vec{v} \cdot \nabla)\vec{v}\right)"
            r"= -\nabla p",
            **cfg,
        )

        # Stage 3: add viscosity term
        eq3 = MathTex(
            r"\rho \!\left(\frac{\partial \vec{v}}{\partial t}"
            r"+ (\vec{v} \cdot \nabla)\vec{v}\right)"
            r"= -\nabla p + \mu \nabla^2 \vec{v}",
            **cfg,
        )

        # Stage 4: full equation with body force
        eq4 = MathTex(
            r"\rho \!\left(\frac{\partial \vec{v}}{\partial t}"
            r"+ (\vec{v} \cdot \nabla)\vec{v}\right)"
            r"= -\nabla p + \mu \nabla^2 \vec{v} + \vec{f}",
            **cfg,
        )

        # Term annotations (appear below, fading)
        annotations = [
            (r"\rho \frac{\partial \vec{v}}{\partial t}",
             "density × rate of change of velocity",  CYAN_GLOW),
            (r"(\vec{v} \cdot \nabla)\vec{v}",
             "advection — carried by its own flow",    ARROW_COLOR),
            (r"-\nabla p",
             "pressure gradient force",                HIGH_PRES),
            (r"\mu \nabla^2 \vec{v}",
             "viscous diffusion",                      "#90EE90"),
            (r"\vec{f}",
             "external body forces",                   HIGHLIGHT),
        ]

        # Position all equations centered, slightly above mid
        for eq in [eq0, eq1, eq2, eq3, eq4]:
            eq.set_stroke(BLACK, width=3, background=True)
            eq.move_to(UP * 0.3)

        # ── Stage 0 ──
        ann0 = self._make_annotation(annotations[0])
        self.play(FadeIn(eq0, scale=0.95), run_time=0.9)
        self._glow_eq(eq0)
        self.play(FadeIn(ann0, shift=UP*0.08), run_time=0.5)
        self.wait(0.9)

        # ── Stage 1 ──
        ann1 = self._make_annotation(annotations[1])
        self.play(
            FadeOut(ann0),
            TransformMatchingShapes(eq0, eq1),
            run_time=1.1, rate_func=smooth,
        )
        self._glow_eq(eq1)
        self.play(FadeIn(ann1, shift=UP*0.08), run_time=0.5)
        self.wait(0.9)

        # ── Stage 2 ──
        ann2 = self._make_annotation(annotations[2])
        self.play(
            FadeOut(ann1),
            TransformMatchingShapes(eq1, eq2),
            run_time=1.1, rate_func=smooth,
        )
        self._glow_eq(eq2)
        self.play(FadeIn(ann2, shift=UP*0.08), run_time=0.5)
        self.wait(0.9)

        # ── Stage 3 ──
        ann3 = self._make_annotation(annotations[3])
        self.play(
            FadeOut(ann2),
            TransformMatchingShapes(eq2, eq3),
            run_time=1.1, rate_func=smooth,
        )
        self._glow_eq(eq3)
        self.play(FadeIn(ann3, shift=UP*0.08), run_time=0.5)
        self.wait(0.9)

        # ── Stage 4 — Full equation ──
        ann4 = self._make_annotation(annotations[4])
        self.play(
            FadeOut(ann3),
            TransformMatchingShapes(eq3, eq4),
            run_time=1.1, rate_func=smooth,
        )
        self._glow_eq(eq4)
        self.play(FadeIn(ann4, shift=UP*0.08), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(ann4), run_time=0.4)

        # ── Slight camera zoom toward equation ──
        self.play(
            self.camera.frame.animate
                .set_width(self._fw * 0.80)
                .move_to(eq4.get_center()),
            run_time=1.5, rate_func=smooth,
        )
        self.wait(1.5)

        # Closing text beneath
        closing = subtitle(
            "This is the Navier–Stokes equation.\nIt governs all viscous fluid motion.",
            size=24, italic=False, color=WHITE,
        )
        closing.next_to(eq4, DOWN, buff=0.55)
        self.play(FadeIn(closing, shift=UP*0.1), run_time=1.0)
        self.wait(2.5)

        # ── Fade everything out ──
        self.play(
            FadeOut(VGroup(eq4, hdr, closing, bg_dim,
                           self._streams, self._arrows)),
            self.camera.frame.animate
                .set_width(self._fw)
                .move_to(ORIGIN),
            run_time=2.0, rate_func=smooth,
        )

    # ──────────────────────────────────────────
    #  Helpers
    # ──────────────────────────────────────────
    def _make_annotation(self, ann_tuple):
        """Create a small annotation line below the equation."""
        _, meaning, color = ann_tuple
        txt = Text(f"↑  {meaning}", font_size=20, color=ManimColor(color))
        txt.set_stroke(BLACK, width=2, background=True)
        txt.move_to(DOWN * 1.8)
        return txt

    def _glow_eq(self, eq, color=CYAN_GLOW):
        """Brief cyan glow flash on an equation."""
        glow = eq.copy().set_color(ManimColor(color)).set_opacity(0.6)
        self.play(
            glow.animate.scale(1.04).set_opacity(0),
            run_time=0.55, rate_func=smooth,
        )
        self.remove(glow)