from manim import *
import numpy as np

# ─────────────────────────────────────────────
#  Style constants
# ─────────────────────────────────────────────
BG_COLOR    = "#0A0A0F"
FLUID_BLUE  = "#1E90FF"
FLUID_DARK  = "#0A2A6E"
ARROW_COL   = "#A8D8FF"
GRID_COL    = "#1A2A3A"
CYAN_GLOW   = "#00E5FF"
HIGH_PRES   = "#FF3030"
LOW_PRES    = "#1040C0"
VISC_GREEN  = "#90EE90"
EXT_YELLOW  = "#FFD700"
TEXT_COL    = WHITE
DIM_OPACITY = 0.60


# ─────────────────────────────────────────────
#  Velocity / flow helpers
# ─────────────────────────────────────────────
def smooth_flow(x, y):
    vx = 1.0 + 0.3 * np.sin(0.8 * y)
    vy = 0.15 * np.sin(1.2 * x + 0.5 * y)
    return np.array([vx, vy, 0])


def speed_col(speed, vmin=0.3, vmax=2.2):
    t = float(np.clip((speed - vmin) / (vmax - vmin), 0, 1))
    return interpolate_color(ManimColor(FLUID_DARK), ManimColor(CYAN_GLOW), t)


def pres_col(p, pmin=0.5, pmax=2.5):
    t = float(np.clip((p - pmin) / (pmax - pmin), 0, 1))
    return interpolate_color(ManimColor(LOW_PRES), ManimColor(HIGH_PRES), t)


def pressure_field(x, y):
    return 1.5 - 0.4 * x + 0.3 * np.sin(0.9 * y)


def make_bg_streams(opacity=0.30, stroke_w=1.2):
    seeds = [(-7, y) for y in np.linspace(-3.8, 3.8, 18)]
    lines = VGroup()
    for sx, sy in seeds:
        pts, x, y = [], sx, sy
        for _ in range(130):
            pts.append([x, y, 0])
            v  = smooth_flow(x, y)
            nm = max(np.linalg.norm(v[:2]), 1e-6)
            x += v[0] / nm * 0.065
            y += v[1] / nm * 0.065
            if abs(x) > 7.8 or abs(y) > 4.8:
                break
        if len(pts) < 3:
            continue
        path = VMobject()
        path.set_points_smoothly([np.array(p) for p in pts])
        path.set_stroke(ManimColor(FLUID_BLUE), width=stroke_w, opacity=opacity)
        lines.add(path)
    return lines


def make_arrow_grid(xs, ys, vel_func=smooth_flow,
                    scale=0.28, colored=False, opacity=0.60):
    group = VGroup()
    for x in xs:
        for y in ys:
            v   = vel_func(x, y)
            spd = np.linalg.norm(v[:2])
            if spd < 1e-4:
                continue
            d   = v / spd
            l   = float(np.clip(spd * scale, 0.05, 0.50))
            col = speed_col(spd) if colored else ManimColor(ARROW_COL)
            arr = Arrow(
                [x, y, 0], [x + d[0]*l, y + d[1]*l, 0],
                buff=0, stroke_width=1.8, tip_length=0.10, color=col,
            )
            arr.set_opacity(opacity)
            group.add(arr)
    return group


# ─────────────────────────────────────────────
#  Reusable UI helpers
# ─────────────────────────────────────────────
def dim_rect(opacity=DIM_OPACITY):
    return Rectangle(
        width=20, height=12,
        fill_color=BLACK, fill_opacity=opacity, stroke_opacity=0,
    )


def label_box(text, font_size=20, color=WHITE, max_width=9.0):
    txt = Text(text, font_size=font_size, color=color,
               line_spacing=1.25)
    txt.set_stroke(BLACK, width=3, background=True)
    if txt.width > max_width:
        txt.scale(max_width / txt.width)
    return txt


def term_label(tex_str, meaning, color=CYAN_GLOW, font_size=22):
    sym = MathTex(tex_str, color=ManimColor(color), font_size=font_size + 4)
    mng = Text(meaning, font_size=font_size, color=ManimColor(color))
    mng.set_stroke(BLACK, width=2, background=True)
    grp = VGroup(sym, mng).arrange(DOWN, buff=0.15)
    return grp


def pulse_glow(scene, mob, color=CYAN_GLOW, scale=1.06, run_time=0.55):
    glow = mob.copy().set_color(ManimColor(color)).set_opacity(0.55)
    scene.add(glow)
    scene.play(
        glow.animate.scale(scale).set_opacity(0),
        run_time=run_time, rate_func=smooth,
    )
    scene.remove(glow)


FULL_EQ_STR = (
    r"\rho \!\left("
    r"\frac{\partial \vec{v}}{\partial t}"
    r"+ (\vec{v} \cdot \nabla)\vec{v}"
    r"\right)"
    r"= -\nabla p"
    r"+ \mu \nabla^2 \vec{v}"
    r"+ \vec{f}"
)


# ═══════════════════════════════════════════════════════════
class Scene5_NavierStokesBreakdown(MovingCameraScene):
# ═══════════════════════════════════════════════════════════

    def construct(self):
        self.camera.background_color = BG_COLOR
        self._fw = self.camera.frame.width

        self._bg = make_bg_streams(opacity=0.28, stroke_w=1.1)
        self._bg_arrows = make_arrow_grid(
            np.linspace(-6, 6, 9), np.linspace(-3.5, 3.5, 6),
            scale=0.25, colored=True, opacity=0.40,
        )
        self.add(self._bg, self._bg_arrows)

        self._part1_full_equation()
        self._part2_lhs_breakdown()
        self._part3_newton_connection()
        self._part4_rhs_forces()
        self._part5_final_meaning()

    # ══════════════════════════════════════════
    #  PART 1 — Full Equation Appears  (0–8 s)
    # ══════════════════════════════════════════
    def _part1_full_equation(self):
        dim = dim_rect(0.55)
        self.play(FadeIn(dim), run_time=0.5)

        hdr = Text("Navier–Stokes Equation",
                   font_size=28, color=ManimColor(CYAN_GLOW), weight=BOLD)
        hdr.set_stroke(BLACK, width=3, background=True)
        hdr.to_edge(UP, buff=0.38)
        self.play(FadeIn(hdr, shift=DOWN*0.1), run_time=0.6)

        eq = MathTex(FULL_EQ_STR, color=WHITE, font_size=44)
        eq.set_stroke(BLACK, width=3, background=True)
        eq.move_to(ORIGIN)

        self.play(Write(eq), run_time=2.0, rate_func=smooth)
        pulse_glow(self, eq, run_time=0.7)
        self.wait(1.8)

        self._full_eq  = eq
        self._full_dim = dim
        self._full_hdr = hdr

    # ══════════════════════════════════════════
    #  PART 2 — LHS Breakdown  (8–25 s)
    # ══════════════════════════════════════════
    def _part2_lhs_breakdown(self):
        eq = self._full_eq

        self.play(
            eq.animate.scale(0.78).to_edge(UP, buff=1.1),
            self._full_hdr.animate.set_opacity(0.4),
            run_time=0.9, rate_func=smooth,
        )

        # ── STEP 1: ρ — Density ──────────────────────────────
        self._highlight_term(eq, color=CYAN_GLOW)

        rho_title = Text("ρ  —  Density", font_size=30,
                         color=ManimColor(CYAN_GLOW), weight=BOLD)
        rho_title.set_stroke(BLACK, width=3, background=True)
        rho_title.move_to(UP * 0.6)
        self.play(FadeIn(rho_title, shift=UP*0.08), run_time=0.6)

        water_col = Rectangle(width=1.1, height=2.2,
                              color=ManimColor(FLUID_BLUE), stroke_width=2)
        water_col.set_fill(ManimColor(FLUID_BLUE), opacity=0.35)
        water_col.move_to(LEFT * 2.5 + DOWN * 0.5)

        mercury_col = Rectangle(width=1.1, height=2.2,
                                color=ManimColor("#C0C0C0"), stroke_width=2)
        mercury_col.set_fill(ManimColor("#808090"), opacity=0.55)
        mercury_col.move_to(RIGHT * 2.5 + DOWN * 0.5)

        w_lbl = VGroup(
            Text("Water", font_size=18, color=ManimColor(FLUID_BLUE)),
            Text("ρ ≈ 1000 kg/m³", font_size=16, color=ManimColor(ARROW_COL)),
        ).arrange(DOWN, buff=0.08)
        w_lbl.next_to(water_col, DOWN, buff=0.18)

        m_lbl = VGroup(
            Text("Mercury", font_size=18, color=ManimColor("#C0C0C0")),
            Text("ρ ≈ 13 600 kg/m³", font_size=16, color=ManimColor("#C0C0C0")),
        ).arrange(DOWN, buff=0.08)
        m_lbl.next_to(mercury_col, DOWN, buff=0.18)

        def dot_fill(rect, n, color):
            dots = VGroup()
            cx, cy = rect.get_center()[:2]
            for _ in range(n):
                dx = np.random.uniform(-0.38, 0.38)
                dy = np.random.uniform(-0.88, 0.88)
                dots.add(Dot([cx+dx, cy+dy, 0], radius=0.055,
                             color=ManimColor(color)).set_opacity(0.75))
            return dots

        np.random.seed(7)
        w_dots = dot_fill(water_col, 8,  FLUID_BLUE)
        m_dots = dot_fill(mercury_col, 22, "#C0C0C0")

        rho_explain = label_box(
            "ρ = density of the fluid at a point\n(mass per unit volume)",
            font_size=21, color=ManimColor(CYAN_GLOW),
        ).to_edge(DOWN, buff=0.45)

        self.play(
            Create(water_col), Create(mercury_col),
            FadeIn(w_lbl), FadeIn(m_lbl),
            run_time=0.8,
        )
        self.play(FadeIn(w_dots, lag_ratio=0.05), FadeIn(m_dots, lag_ratio=0.03),
                  run_time=0.9)
        self.play(FadeIn(rho_explain, shift=UP*0.08), run_time=0.6)
        self.wait(2.0)

        rho_group = VGroup(rho_title, water_col, mercury_col,
                           w_lbl, m_lbl, w_dots, m_dots, rho_explain)
        self.play(FadeOut(rho_group), run_time=0.6)

        # ── STEP 2: ∂v/∂t — Local Acceleration ──────────────
        local_title = Text("∂v/∂t  —  Local Acceleration",
                           font_size=28, color=ManimColor(CYAN_GLOW), weight=BOLD)
        local_title.set_stroke(BLACK, width=3, background=True)
        local_title.move_to(UP * 1.2)
        self.play(FadeIn(local_title, shift=UP*0.08), run_time=0.6)

        pt = ORIGIN + DOWN * 0.3
        t_snaps = [0.0, 0.8, 1.8]
        arrow_snaps = []
        for t in t_snaps:
            vx = 0.9 + 0.5 * np.sin(t * 1.5)
            vy = 0.3 * np.cos(t * 1.2)
            spd = np.sqrt(vx**2 + vy**2)
            d   = np.array([vx, vy]) / spd
            arr = Arrow(
                pt, pt + np.array([d[0]*0.8, d[1]*0.8, 0]),
                buff=0, stroke_width=3.0, tip_length=0.18,
                color=ManimColor(CYAN_GLOW),
            )
            arrow_snaps.append(arr)

        fixed_dot = Dot(pt, radius=0.10, color=ManimColor(EXT_YELLOW))

        t_labels = VGroup(*[
            Text(f"t = {t}", font_size=17, color=ManimColor(ARROW_COL))
            .set_stroke(BLACK, width=2, background=True)
            for t in t_snaps
        ])

        # FIX 1: Move local_explain up so it's clearly visible (was to_edge DOWN)
        local_explain = label_box(
            "How velocity changes at a fixed point over time",
            font_size=21, color=ManimColor(CYAN_GLOW),
        ).move_to(DOWN * 1.8)

        self.play(FadeIn(fixed_dot), run_time=0.4)
        self.play(FadeIn(local_explain, shift=UP*0.08), run_time=0.5)

        cur_arrow = arrow_snaps[0].copy()
        self.play(GrowArrow(cur_arrow), run_time=0.7)
        for i, (arr, t) in enumerate(zip(arrow_snaps[1:], t_snaps[1:]), 1):
            t_lbl = t_labels[i].next_to(cur_arrow.get_end(), UR, buff=0.08)
            self.play(FadeIn(t_lbl), run_time=0.4)
            # FIX 1: Slowed down arrow transform from 0.9 → 1.4
            self.play(Transform(cur_arrow, arr), run_time=1.4, rate_func=smooth)
            self.wait(0.7)  # FIX 1: increased pause from 0.3 → 0.7

        self.wait(1.5)  # FIX 1: extra hold at end
        self.play(FadeOut(VGroup(local_title, fixed_dot, cur_arrow,
                                 t_labels, local_explain)), run_time=0.6)

        # ── STEP 3: (v·∇)v — Convection ───────────────────────
        conv_title = Text("(v·∇)v  —  Convection / Advection",
                          font_size=26, color=ManimColor(CYAN_GLOW), weight=BOLD)
        conv_title.set_stroke(BLACK, width=3, background=True)
        conv_title.move_to(UP * 1.2)
        self.play(FadeIn(conv_title, shift=UP*0.08), run_time=0.6)

        def conv_vel(x, y):
            vx = 0.5 + 1.0 / (1 + np.exp(-2.5 * x))
            vy = 0.20 * np.sin(1.5 * y)
            return np.array([vx, vy, 0])

        conv_xs = np.linspace(-4.5, 4.5, 9)
        conv_ys = np.linspace(-1.8, 1.8, 6)
        conv_arrows = make_arrow_grid(conv_xs, conv_ys, vel_func=conv_vel,
                                      scale=0.30, colored=True, opacity=0.75)
        self.play(FadeIn(conv_arrows, lag_ratio=0.02), run_time=1.0)

        tracer = Dot([-4.5, 0, 0], radius=0.10, color=ManimColor(EXT_YELLOW))
        tracer_trail = TracedPath(tracer.get_center, stroke_color=ManimColor(EXT_YELLOW),
                                  stroke_width=2, stroke_opacity=0.6)
        self.add(tracer_trail, tracer)
        # FIX 2: Slowed tracer from 2.5 → 4.0
        self.play(tracer.animate.move_to([4.5, 0, 0]),
                  run_time=4.0, rate_func=linear)
        self.wait(0.6)  # FIX 2: pause after tracer

        # FIX 2: Move conv_explain up so it's clearly visible
        conv_explain = label_box(
            "Change in velocity due to the movement of the fluid itself",
            font_size=21, color=ManimColor(CYAN_GLOW),
        ).move_to(DOWN * 1.8)
        self.play(FadeIn(conv_explain, shift=UP*0.08), run_time=0.6)
        self.wait(2.5)  # FIX 2: increased hold from 1.5 → 2.5

        total_acc = Text("= Total acceleration of the fluid",
                         font_size=24, color=WHITE, weight=BOLD)
        total_acc.set_stroke(BLACK, width=3, background=True)
        total_acc.move_to(DOWN * 0.6)
        self.play(FadeIn(total_acc, scale=1.05), run_time=0.7)
        self.wait(2.0)  # FIX 2: increased hold from 1.5 → 2.0

        self.play(
            FadeOut(VGroup(conv_title, conv_arrows, tracer, tracer_trail,
                           conv_explain, total_acc)),
            run_time=0.7,
        )

    # ══════════════════════════════════════════
    #  PART 3 — Newton's Law  (25–35 s)
    # ══════════════════════════════════════════
    def _part3_newton_connection(self):
        newton_title = Text("Newton's Second Law", font_size=28,
                            color=ManimColor(EXT_YELLOW), weight=BOLD)
        newton_title.set_stroke(BLACK, width=3, background=True)
        newton_title.move_to(UP * 1.5)
        self.play(FadeIn(newton_title, shift=UP*0.1), run_time=0.6)

        fma = MathTex(r"F = m\,a", color=WHITE, font_size=58)
        fma.set_stroke(BLACK, width=3, background=True)
        fma.move_to(UP * 0.35)
        self.play(Write(fma), run_time=1.0)
        pulse_glow(self, fma, color=EXT_YELLOW)
        self.wait(0.8)

        elem = Rectangle(width=1.8, height=1.4,
                         color=ManimColor(EXT_YELLOW), stroke_width=2.5)
        elem.set_fill(ManimColor(EXT_YELLOW), opacity=0.08)
        elem.move_to(DOWN * 0.8)
        e_lbl = Text("fluid element", font_size=17, color=ManimColor(EXT_YELLOW))
        e_lbl.set_stroke(BLACK, width=2, background=True)
        e_lbl.next_to(elem, DOWN, buff=0.14)
        self.play(Create(elem), FadeIn(e_lbl), run_time=0.7)

        pf = Arrow([-2.5, -0.8, 0], [-0.9, -0.8, 0], buff=0,
                   stroke_width=2.8, tip_length=0.16,
                   color=ManimColor(HIGH_PRES))
        vf = Arrow([2.5, -0.6, 0], [0.9, -0.6, 0], buff=0,
                   stroke_width=2.8, tip_length=0.16,
                   color=ManimColor(VISC_GREEN))
        pf_lbl = Text("pressure", font_size=16, color=ManimColor(HIGH_PRES))
        pf_lbl.next_to(pf, UP, buff=0.08).set_stroke(BLACK, width=2, background=True)
        vf_lbl = Text("viscosity", font_size=16, color=ManimColor(VISC_GREEN))
        vf_lbl.next_to(vf, UP, buff=0.08).set_stroke(BLACK, width=2, background=True)

        self.play(GrowArrow(pf), FadeIn(pf_lbl), run_time=0.7)
        self.play(GrowArrow(vf), FadeIn(vf_lbl), run_time=0.7)
        self.wait(0.6)

        rho_a = MathTex(
            r"\rho \cdot \mathbf{a} = \underbrace{-\nabla p + \mu\nabla^2\vec{v} + \vec{f}}_{\text{forces}}",
            color=WHITE, font_size=40,
        )
        rho_a.set_stroke(BLACK, width=3, background=True)
        rho_a.move_to(UP * 0.35)

        self.play(
            TransformMatchingShapes(fma, rho_a),
            run_time=1.3, rate_func=smooth,
        )
        pulse_glow(self, rho_a, color=CYAN_GLOW)
        self.wait(1.8)

        self.play(
            FadeOut(VGroup(newton_title, rho_a, elem, e_lbl,
                           pf, pf_lbl, vf, vf_lbl)),
            run_time=0.8,
        )

    # ══════════════════════════════════════════
    #  PART 4 — RHS Forces  (35–75 s)
    # ══════════════════════════════════════════
    def _part4_rhs_forces(self):
        eq = self._full_eq

        self.play(FadeOut(eq), run_time=0.6)

        # ── STEP 4: −∇p — Pressure Force ─────────────────────
        self._section_header("−∇p   Pressure Gradient Force",
                             color=HIGH_PRES)

        cells = VGroup()
        for px in np.linspace(-5.5, 5.5, 12):
            for py in np.linspace(-2.5, 2.5, 7):
                p   = pressure_field(px, py)
                col = pres_col(p)
                c   = Rectangle(width=0.95, height=0.73,
                                 fill_color=col, fill_opacity=0.32,
                                 stroke_opacity=0)
                c.move_to([px, py, 0])
                cells.add(c)
        self.play(FadeIn(cells, lag_ratio=0.004), run_time=1.0)

        p_arrows = VGroup()
        for px in np.linspace(-4.5, 4.5, 9):
            for py in np.linspace(-2.0, 2.0, 6):
                gx = -(-0.4 - 0.2 * np.sin(1.1 * px))
                gy = -(0.3 * np.cos(0.9 * py))
                mg = np.sqrt(gx**2 + gy**2) + 1e-6
                l  = 0.28
                a  = Arrow(
                    [px, py, 0],
                    [px + gx/mg*l, py + gy/mg*l, 0],
                    buff=0, stroke_width=1.8, tip_length=0.10,
                    color=ManimColor(HIGH_PRES),
                )
                a.set_opacity(0.65)
                p_arrows.add(a)

        self.play(FadeIn(p_arrows, lag_ratio=0.01), run_time=1.0)

        leg = self._pressure_legend()
        leg.to_corner(DR, buff=0.45)
        self.play(FadeIn(leg), run_time=0.5)

        # FIX 3: Centered on screen, WHITE color instead of HIGH_PRES red
        p_explain = label_box(
            "Fluid is pushed from HIGH pressure → LOW pressure\n"
            "−∇p : pressure force per unit volume",
            font_size=22, color=WHITE,
        ).move_to(ORIGIN)
        self.play(FadeIn(p_explain, shift=UP*0.08), run_time=0.6)
        self.wait(3.5)

        self.play(FadeOut(VGroup(cells, p_arrows, leg,
                                  self._cur_header, p_explain)), run_time=0.7)

        # ── STEP 5: μ∇²v — Viscosity / Diffusion ─────────────
        self._section_header("μ∇²v   Viscous Diffusion",
                             color=VISC_GREEN)

        def bar_profile(amplitude_func, n=12):
            bars = VGroup()
            xs = np.linspace(-3.5, 3.5, n)
            for x in xs:
                amp = amplitude_func(x)
                bar = Line([x, -0.05, 0], [x, amp, 0],
                           stroke_width=4.5,
                           color=ManimColor(VISC_GREEN))
                bar.set_opacity(0.80)
                bars.add(bar)
            return bars

        np.random.seed(3)
        rough_amps = np.abs(np.sin(np.linspace(0, 3*np.pi, 12))) \
                     + 0.3 * np.random.randn(12)
        rough_amps = np.clip(rough_amps, 0.1, 1.6)
        rough_bars = bar_profile(lambda x: rough_amps[int((x+3.5)/7*11.99)], n=12)

        smooth_bars = bar_profile(
            lambda x: 1.2 * (1 - (x/3.8)**2), n=12
        )

        rough_lbl = Text("rough flow (large ∇²v)",
                         font_size=18, color=ManimColor(VISC_GREEN))
        rough_lbl.set_stroke(BLACK, width=2, background=True)
        rough_lbl.next_to(rough_bars, UP, buff=0.30)

        smooth_lbl = Text("smooth flow (viscosity acts)",
                          font_size=18, color=ManimColor(VISC_GREEN))
        smooth_lbl.set_stroke(BLACK, width=2, background=True)
        smooth_lbl.next_to(smooth_bars, UP, buff=0.30)

        self.play(Create(rough_bars, lag_ratio=0.06), FadeIn(rough_lbl),
                  run_time=0.9)
        self.wait(1.2)  # FIX 4: extra pause before transform
        # FIX 4: Slowed transform from 1.8 → 2.5
        self.play(
            Transform(rough_bars, smooth_bars, replace_mobject_with_target_in_scene=False),
            FadeOut(rough_lbl), FadeIn(smooth_lbl),
            run_time=2.5, rate_func=smooth,
        )
        self.wait(1.2)  # FIX 4: increased from 0.5 → 1.2
        self.play(FadeOut(rough_bars), FadeOut(smooth_lbl), run_time=0.5)

        # FIX 4: Move mu_explain up (move_to UP instead of to_edge DOWN)
        mu_explain = label_box(
            "μ = dynamic viscosity — internal resistance of the fluid\n"
            "μ∇²v : viscosity smooths out velocity differences",
            font_size=21, color=ManimColor(VISC_GREEN),
        ).move_to(DOWN * 1.6)
        self.play(FadeIn(mu_explain, shift=UP*0.08), run_time=0.6)

        honey_lbl = Text("Honey  μ ≈ 10 Pa·s", font_size=18,
                         color=ManimColor(EXT_YELLOW))
        water_lbl = Text("Water  μ ≈ 0.001 Pa·s", font_size=18,
                         color=ManimColor(FLUID_BLUE))
        comp = VGroup(honey_lbl, water_lbl).arrange(RIGHT, buff=1.0)
        comp.move_to(DOWN * 0.3)
        comp.set_stroke(BLACK, width=2, background=True)
        self.play(FadeIn(comp, lag_ratio=0.5), run_time=0.8)
        self.wait(3.5)  # FIX 4: increased from 3.0 → 3.5

        self.play(FadeOut(VGroup(comp, mu_explain, self._cur_header,
                                  smooth_bars)), run_time=0.7)

        # ── STEP 6: f — External Forces ───────────────────────
        self._section_header("f   External Body Forces",
                             color=EXT_YELLOW)

        grav_arrows = VGroup()
        for gx in np.linspace(-4.5, 4.5, 9):
            for gy in np.linspace(-1.5, 2.0, 6):
                a = Arrow(
                    [gx, gy, 0], [gx, gy - 0.45, 0],
                    buff=0, stroke_width=2.0, tip_length=0.12,
                    color=ManimColor(EXT_YELLOW),
                )
                a.set_opacity(0.70)
                grav_arrows.add(a)

        g_lbl = Text("gravity  g = 9.8 m/s²  ↓",
                     font_size=22, color=ManimColor(EXT_YELLOW), weight=BOLD)
        g_lbl.set_stroke(BLACK, width=3, background=True)
        g_lbl.move_to(UP * 0.8)

        self.play(FadeIn(grav_arrows, lag_ratio=0.01),
                  FadeIn(g_lbl), run_time=1.0)

        f_explain = label_box(
            "External forces acting on the fluid\n"
            "(e.g., gravity, electromagnetic forces, buoyancy)",
            font_size=21, color=ManimColor(EXT_YELLOW),
        ).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(f_explain, shift=UP*0.08), run_time=0.6)
        self.wait(3.0)

        self.play(
            FadeOut(VGroup(grav_arrows, g_lbl, f_explain, self._cur_header)),
            run_time=0.7,
        )

        eq.scale(1 / 0.78).move_to(UP * 1.0)
        self.play(FadeIn(eq), run_time=0.9, rate_func=smooth)

    # ══════════════════════════════════════════
    #  PART 5 — Final Meaning  (75–90 s)
    # ══════════════════════════════════════════
    def _part5_final_meaning(self):
        eq = self._full_eq

        pulse_glow(self, eq, run_time=0.8)
        self.play(self._full_dim.animate.set_opacity(0.65), run_time=0.5)

        summary_lines = [
            ("Acceleration", CYAN_GLOW),
            ("= Pressure Force", HIGH_PRES),
            ("+ Viscous Force", VISC_GREEN),
            ("+ External Force", EXT_YELLOW),
        ]
        line_mobs = VGroup()
        for txt, col in summary_lines:
            t = Text(txt, font_size=26, color=ManimColor(col))
            t.set_stroke(BLACK, width=3, background=True)
            line_mobs.add(t)
        line_mobs.arrange(DOWN, buff=0.30)
        line_mobs.move_to(DOWN * 1.0)

        self.play(
            LaggedStart(
                *[FadeIn(l, shift=RIGHT*0.15) for l in line_mobs],
                lag_ratio=0.35,
            ),
            run_time=2.0, rate_func=smooth,
        )
        self.wait(1.2)

        highlight_data = [
            (CYAN_GLOW,   0.55),
            (HIGH_PRES,   0.55),
            (VISC_GREEN,  0.55),
            (EXT_YELLOW,  0.55),
        ]
        for col, rt in highlight_data:
            glow = eq.copy().set_color(ManimColor(col)).set_opacity(0.50)
            self.play(glow.animate.set_opacity(0), run_time=rt, rate_func=smooth)
            self.remove(glow)

        self.wait(1.0)

        closing = Text(
            "Fluid motion is fully described by this equation.",
            font_size=26, color=WHITE,
        )
        closing.set_stroke(BLACK, width=3, background=True)
        closing.next_to(line_mobs, DOWN, buff=0.45)
        self.play(FadeIn(closing, shift=UP*0.1), run_time=0.9)
        self.wait(2.5)

        self.play(
            FadeOut(VGroup(eq, self._full_hdr, self._full_dim,
                           line_mobs, closing,
                           self._bg, self._bg_arrows)),
            run_time=2.0, rate_func=smooth,
        )

    # ──────────────────────────────────────────
    #  Internal helpers
    # ──────────────────────────────────────────
    def _section_header(self, text, color=CYAN_GLOW):
        hdr = Text(text, font_size=27, color=ManimColor(color), weight=BOLD)
        hdr.set_stroke(BLACK, width=3, background=True)
        hdr.to_edge(UP, buff=1.35)
        self.play(FadeIn(hdr, shift=DOWN*0.08), run_time=0.55)
        self._cur_header = hdr

    def _highlight_term(self, eq, color=CYAN_GLOW, rt=0.55):
        glow = eq.copy().set_color(ManimColor(color)).set_opacity(0.55)
        self.play(glow.animate.scale(1.05).set_opacity(0),
                  run_time=rt, rate_func=smooth)
        self.remove(glow)

    def _pressure_legend(self):
        low_t  = Text("Low p", font_size=16, color=ManimColor(LOW_PRES))
        high_t = Text("High p", font_size=16, color=ManimColor(HIGH_PRES))
        bar    = Rectangle(width=1.3, height=0.15, stroke_opacity=0)
        bar.set_fill(color=[ManimColor(LOW_PRES), ManimColor(HIGH_PRES)], opacity=0.9)
        leg = VGroup(low_t, bar, high_t).arrange(RIGHT, buff=0.12)
        leg.set_stroke(BLACK, width=2, background=True)
        return leg