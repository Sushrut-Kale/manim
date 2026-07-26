
from manim import *
import numpy as np

# ── Palette ──────────────────────────────────────────────────────────────────
BG_COLOR      = "#050810"
WING_COLOR    = "#b0c4de"
LAMINAR_C     = "#40c4ff"
TURB1_C       = "#1976d2"
TURB2_C       = "#ffffff"
CONVECT_C     = "#ff6d00"
DIFFUSE_C     = "#00e676"
TEXT_MAIN     = "#e8eaf6"
TEXT_SUB      = "#90caf9"
HIGHLIGHT_BOX = "#ffd740"
VORTEX_C      = "#80d8ff"


# ── Helpers ──────────────────────────────────────────────────────────────────
def lerp_color(c1, c2, t):
    t = float(np.clip(t, 0, 1))
    r1, g1, b1 = color_to_rgb(c1)
    r2, g2, b2 = color_to_rgb(c2)
    return rgb_to_color([r1+(r2-r1)*t, g1+(g2-g1)*t, b1+(b2-b1)*t])

def title_text(txt, size=32, color=TEXT_MAIN):
    return Text(txt, font_size=size, color=color,
                font="Courier New", weight=BOLD)

def sub_text(txt, size=22, color=TEXT_SUB):
    return Text(txt, font_size=size, color=color, font="Courier New")

def eq_tex(src, size=34, color=TEXT_MAIN):
    return MathTex(src, font_size=size, color=color)


# ── Wing (NACA-style airfoil) ─────────────────────────────────────────────────
def make_airfoil(chord=5.5, thickness=0.55, angle_deg=8.0,
                 cx=0.0, cy=0.0, color=WING_COLOR):
    """
    Returns a VGroup containing a filled NACA-4-style airfoil polygon.
    chord     : length of the wing from leading to trailing edge
    thickness : max thickness (fraction of chord × chord)
    angle_deg : angle of attack (degrees, nose-up positive)
    cx, cy    : centre position in Manim world coords
    """
    N = 120
    t_arr = np.linspace(0, 1, N)

    # NACA 4-digit symmetric thickness distribution
    def naca_y(tc, t):
        return 5 * tc * (0.2969*np.sqrt(t)
                         - 0.1260*t
                         - 0.3516*t**2
                         + 0.2843*t**3
                         - 0.1015*t**4)

    tc = thickness / chord   # thickness-to-chord ratio
    half_t = np.array([naca_y(tc, t) * chord for t in t_arr])

    # Upper and lower surfaces in [0,chord] space
    upper = np.column_stack([t_arr * chord, half_t])
    lower = np.column_stack([t_arr * chord, -half_t])

    # Rotate by angle of attack
    aoa = np.radians(angle_deg)
    rot = np.array([[np.cos(aoa), -np.sin(aoa)],
                    [np.sin(aoa),  np.cos(aoa)]])
    all_pts = np.vstack([upper, lower[::-1]])
    # Centre at (chord/2, 0) before rotation
    all_pts[:, 0] -= chord / 2
    all_pts = (rot @ all_pts.T).T
    all_pts[:, 0] += cx
    all_pts[:, 1] += cy

    points_3d = np.column_stack([all_pts, np.zeros(len(all_pts))])
    polygon = Polygon(*points_3d,
                      fill_color=WING_COLOR,
                      fill_opacity=0.85,
                      stroke_color=lerp_color(WING_COLOR, WHITE, 0.3),
                      stroke_width=1.8)
    return polygon


# ── Streamline path helpers ───────────────────────────────────────────────────
def _stream_y_deflection(x, chord, cy, amplitude, phase_shift=0.0):
    """
    Smooth deflection that mirrors potential-flow behaviour:
    - upstream (x < -chord/2): gradual approach
    - over wing: parabolically displaced (lift)
    - downstream: return + optional oscillation (turbulence)
    """
    x0 = -chord / 2
    x1 =  chord / 2
    if x < x0:
        # upstream approach: small fore-deflection
        t = (x - x0) / chord
        return amplitude * np.exp(3.0 * t) * 0.12
    elif x <= x1:
        # over wing: smooth arc
        t = (x - x0) / chord   # 0 → 1
        return amplitude * 4 * t * (1 - t)
    else:
        # downstream: return with optional oscillation
        t = (x - x1) / chord
        decay = np.exp(-1.5 * t)
        osc   = np.sin(5.0 * t + phase_shift) * t
        return amplitude * decay * (1.0 - t * 0.6 + osc * phase_shift)


def make_smooth_stream(y_base, chord=5.5, x_start=-6.5, x_end=6.5,
                       n_pts=180, amplitude=0.0, phase=0.0,
                       color=LAMINAR_C, stroke_w=1.4, cx=0.0, cy=0.0):
    """Single smooth streamline VMobject."""
    xs = np.linspace(x_start, x_end, n_pts)
    pts = []
    for x in xs:
        defl = _stream_y_deflection(x - cx, chord, cy,
                                    amplitude=amplitude * (1 - abs(y_base) / 1.8),
                                    phase_shift=phase)
        pts.append([x, y_base + defl, 0])
    curve = VMobject(color=color, stroke_width=stroke_w, stroke_opacity=0.85)
    curve.set_points_as_corners(pts)
    curve.make_smooth()
    return curve


def make_disturbed_stream(y_base, chord=5.5, x_start=-6.5, x_end=6.5,
                          n_pts=220, amplitude=0.18, phase=0.0,
                          disturbance_start=0.0, disturbance_amp=0.0,
                          color=LAMINAR_C, stroke_w=1.4, cx=0.0, cy=0.0):
    """Streamline with growing oscillation after disturbance_start."""
    xs = np.linspace(x_start, x_end, n_pts)
    pts = []
    for x in xs:
        base_defl = _stream_y_deflection(x - cx, chord, cy,
                                         amplitude=amplitude * (1 - abs(y_base) / 1.8),
                                         phase_shift=phase)
        # Growing sinusoidal disturbance past disturbance_start
        if x > disturbance_start:
            t = (x - disturbance_start) / (x_end - disturbance_start)
            growth = np.exp(1.8 * t) - 1.0
            noise  = disturbance_amp * growth * np.sin(
                8.0 * t + phase + y_base * 2.5
            )
        else:
            noise = 0.0
        pts.append([x, y_base + base_defl + noise, 0])
    curve = VMobject(color=color, stroke_width=stroke_w, stroke_opacity=0.88)
    curve.set_points_as_corners(pts)
    curve.make_smooth()
    return curve


def make_vortex(cx, cy, radius=0.38, n_turns=2.5, n_pts=260,
                color=VORTEX_C, stroke_w=1.6, decay=0.55):
    """Spiral vortex centred at (cx, cy)."""
    thetas = np.linspace(0, n_turns * 2 * np.pi, n_pts)
    pts = []
    for th in thetas:
        r = radius * (1.0 - th / (n_turns * 2 * np.pi) * decay)
        r = max(r, 0.015)
        pts.append([cx + r * np.cos(th), cy + r * np.sin(th), 0])
    spiral = VMobject(color=color, stroke_width=stroke_w, stroke_opacity=0.9)
    spiral.set_points_as_corners(pts)
    spiral.make_smooth()
    return spiral


def make_velocity_arrow(x, y, vx=0.55, vy=0.0, color=LAMINAR_C, sw=1.8):
    return Arrow(start=[x, y, 0], end=[x + vx, y + vy, 0],
                 color=color, buff=0, stroke_width=sw,
                 max_tip_length_to_length_ratio=0.28)


# ═════════════════════════════════════════════════════════════════════════════
class Scene11_0_AircraftTurbulence(MovingCameraScene):

    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        self._fw = self.camera.frame.get_width()   # ≈ 14.22
        self._fh = self.camera.frame.get_height()  # ≈  8.0

        # Wing geometry constants (shared across parts)
        self.CHORD  = 5.5
        self.WX     = 0.0     # wing centre x
        self.WY     = 0.0     # wing centre y
        self.AOA    = 8.0     # angle of attack (degrees)

        # y positions for streamlines (above & below wing)
        self.stream_ys = [-1.55, -1.10, -0.68, -0.32,
                           0.32,  0.68,  1.10,  1.55]

        self.part0_intro()
        self.part1_smooth_flight()
        self.part2_onset_disturbance()
        self.part3_instability_growth()
        self.part4_turbulence_formation()
        self.part5_competition()
        self.part6_energy_cascade()
        self.part7_prediction_insight()

    # ─────────────────────────────────────────────────────────────────────────
    # SHARED: build the wing mobject (recreated each part that needs it)
    # ─────────────────────────────────────────────────────────────────────────
    def _wing(self):
        return make_airfoil(chord=self.CHORD, thickness=0.55,
                            angle_deg=self.AOA,
                            cx=self.WX, cy=self.WY)

    # ─────────────────────────────────────────────────────────────────────────
    # PART 0 — Cinematic intro  (0–8 s)
    # ─────────────────────────────────────────────────────────────────────────
    def part0_intro(self):
        """
        A short cinematic hook before the physics begins.
        Shows the aviation industry context with a bold title card.
        """
        # Top tagline
        tag = sub_text("A real-world application of fluid dynamics",
                       size=21, color=lerp_color(TEXT_SUB, WHITE, 0.2))
        tag.move_to([0, 3.0, 0])

        # Main bold title
        main = title_text("Aviation Industry", size=52, color=TEXT_MAIN)
        main.move_to([0, 1.4, 0])

        # Sub-headline
        sub1 = title_text("How turbulence threatens flight —",
                           size=26, color=lerp_color(CONVECT_C, WHITE, 0.25))
        sub1.move_to([0, 0.30, 0])
        sub2 = title_text("and what the math says about it.",
                           size=26, color=lerp_color(CONVECT_C, WHITE, 0.25))
        sub2.move_to([0, -0.28, 0])

        # Decorative horizontal rule lines
        rule_top = Line([-5.5, 0.85, 0], [5.5, 0.85, 0],
                        color=lerp_color(TEXT_SUB, BG_COLOR, 0.4),
                        stroke_width=0.8)
        rule_bot = Line([-5.5, -0.82, 0], [5.5, -0.82, 0],
                        color=lerp_color(TEXT_SUB, BG_COLOR, 0.4),
                        stroke_width=0.8)

        # Animate in with staggered reveals
        self.play(FadeIn(tag, shift=DOWN*0.12), run_time=0.7)
        self.play(
            FadeIn(main, shift=UP*0.18),
            Create(rule_top), Create(rule_bot),
            run_time=1.0, rate_func=smooth
        )
        self.play(FadeIn(sub1, shift=LEFT*0.15), run_time=0.6)
        self.play(FadeIn(sub2, shift=LEFT*0.15), run_time=0.6)
        self.wait(2.8)

        # Fade everything out cleanly
        intro_grp = VGroup(tag, main, sub1, sub2, rule_top, rule_bot)
        self.play(FadeOut(intro_grp, shift=UP*0.2), run_time=0.9)
        self.wait(0.3)

    # ─────────────────────────────────────────────────────────────────────────
    # PART 1 — Smooth laminar flow  (0–15 s)
    # ─────────────────────────────────────────────────────────────────────────
    def part1_smooth_flight(self):
        wing = self._wing()
        wing.set_z_index(5)

        # Smooth streamlines: slight upward deflection over the wing
        streams = VGroup(*[
            make_smooth_stream(y, chord=self.CHORD, amplitude=0.22,
                               cx=self.WX, cy=self.WY,
                               color=lerp_color(LAMINAR_C, TURB1_C,
                                                abs(y) / 2.0))
            for y in self.stream_ys
        ])
        streams.set_z_index(2)

        # Uniform upstream velocity arrows
        arrow_xs = [-5.5, -4.5]
        arrows = VGroup(*[
            make_velocity_arrow(ax, ay, vx=0.5)
            for ax in arrow_xs
            for ay in self.stream_ys
        ])
        arrows.set_z_index(3)

        # Text
        t_title = title_text("Flow around the aircraft is smooth", size=28)
        t_title.move_to([0, 3.2, 0])
        t_lam   = sub_text("Laminar flow", size=24, color=LAMINAR_C)
        t_lam.move_to([-4.2, -2.8, 0])

        # Laminar label line
        lam_line = Line([-3.0, -2.65, 0], [-1.8, -1.5, 0],
                        color=LAMINAR_C, stroke_width=1.0, stroke_opacity=0.6)

        # Animate
        self.play(Create(wing), run_time=1.2, rate_func=smooth)
        self.play(FadeIn(t_title, shift=DOWN*0.15), run_time=0.6)
        self.play(
            *[Create(s, rate_func=smooth) for s in streams],
            run_time=2.5
        )
        self.play(
            *[GrowArrow(a) for a in arrows],
            run_time=1.2, rate_func=smooth
        )
        self.play(FadeIn(t_lam), Create(lam_line), run_time=0.6)
        self.wait(4.5)

        # Store for next part
        self._wing_obj  = wing
        self._wing_base_y = self.WY   # remember baseline y for bounce
        self._p1_objs   = VGroup(streams, arrows, t_title, t_lam, lam_line)

    # ─────────────────────────────────────────────────────────────────────────
    # PART 2 — Onset of disturbance  (15–30 s)
    # ─────────────────────────────────────────────────────────────────────────
    def part2_onset_disturbance(self):
        self.play(FadeOut(self._p1_objs), run_time=0.8)

        wing = self._wing_obj   # reuse

        t_title = title_text("Small disturbances appear", size=30)
        t_title.move_to([0, 3.2, 0])
        self.play(FadeIn(t_title, shift=DOWN*0.15), run_time=0.6)

        # Slightly wobbly streamlines – small disturbance amplitude
        streams_w = VGroup(*[
            make_disturbed_stream(
                y, chord=self.CHORD, amplitude=0.22,
                disturbance_start=self.WX + self.CHORD * 0.3,
                disturbance_amp=0.06,
                phase=i * 1.1,
                cx=self.WX, cy=self.WY,
                color=lerp_color(LAMINAR_C, WHITE, 0.15)
            )
            for i, y in enumerate(self.stream_ys)
        ])
        streams_w.set_z_index(2)

        # Small oscillation indicator dots on trailing edge
        indicator_dots = VGroup(*[
            Dot(point=[self.WX + self.CHORD * 0.45, y * 0.9, 0],
                radius=0.06, color=HIGHLIGHT_BOX, fill_opacity=0.8)
            for y in self.stream_ys[2:6]
        ])
        indicator_dots.set_z_index(6)

        self.play(
            *[Create(s, rate_func=smooth) for s in streams_w],
            run_time=2.8
        )
        self.play(FadeIn(indicator_dots), run_time=0.5)
        self.play(
            indicator_dots.animate.set_fill(opacity=0.2),
            run_time=0.6, rate_func=there_and_back
        )
        self.play(
            indicator_dots.animate.set_fill(opacity=0.9).scale(1.3),
            run_time=0.5
        )
        self.wait(4.0)

        self._p2_streams = streams_w
        self._p2_title   = t_title
        self._p2_dots    = indicator_dots

    # ─────────────────────────────────────────────────────────────────────────
    # PART 3 — Growth of instability  (30–45 s)
    # ─────────────────────────────────────────────────────────────────────────
    def part3_instability_growth(self):
        self.play(
            FadeOut(self._p2_title), FadeOut(self._p2_dots),
            run_time=0.6
        )

        t_title = title_text("Disturbances amplify", size=30,
                              color=lerp_color(TEXT_MAIN, CONVECT_C, 0.4))
        t_title.move_to([0, 3.2, 0])
        self.play(FadeIn(t_title, shift=DOWN*0.15), run_time=0.6)

        # Replace wobbly streams with strongly disturbed ones + early vortices
        streams_d = VGroup(*[
            make_disturbed_stream(
                y, chord=self.CHORD, amplitude=0.22,
                disturbance_start=self.WX + self.CHORD * 0.1,
                disturbance_amp=0.16,
                phase=i * 0.9,
                cx=self.WX, cy=self.WY,
                color=lerp_color(LAMINAR_C, CONVECT_C, 0.25 + abs(y)*0.1)
            )
            for i, y in enumerate(self.stream_ys)
        ])
        streams_d.set_z_index(2)

        self.play(
            Transform(self._p2_streams, streams_d, rate_func=smooth),
            run_time=2.0
        )

        # Nascent vortices just past the trailing edge
        vortex_positions = [
            (self.WX + self.CHORD * 0.62,  0.38),
            (self.WX + self.CHORD * 0.62, -0.38),
            (self.WX + self.CHORD * 0.90,  0.15),
        ]
        vortices = VGroup(*[
            make_vortex(vx, vy, radius=0.30, n_turns=2.2,
                        color=lerp_color(VORTEX_C, CONVECT_C, 0.3),
                        stroke_w=1.5)
            for vx, vy in vortex_positions
        ])
        vortices.set_z_index(3)
        self.play(*[Create(v, rate_func=smooth) for v in vortices],
                  run_time=1.8)

        # ── Convection term ────────────────────────────────────────────────
        eq_conv = MathTex(r"(\mathbf{v} \cdot \nabla)\mathbf{v}",
                          font_size=40, color=CONVECT_C)
        eq_conv.move_to([0, 2.35, 0])
        lbl_conv = sub_text("Convection (nonlinear) amplifies motion",
                            size=20, color=CONVECT_C)
        lbl_conv.move_to([0, 1.78, 0])

        conv_box = SurroundingRectangle(eq_conv, color=CONVECT_C,
                                        stroke_width=1.5, buff=0.14,
                                        corner_radius=0.07)

        self.play(Write(eq_conv), run_time=1.2)
        self.play(Create(conv_box), run_time=0.5)
        self.play(FadeIn(lbl_conv), run_time=0.5)
        self.wait(3.5)

        self._p3_streams  = self._p2_streams
        self._p3_vortices = vortices
        self._p3_title    = t_title
        self._p3_eq       = VGroup(eq_conv, conv_box, lbl_conv)

    # ─────────────────────────────────────────────────────────────────────────
    # PART 4 — Turbulence formation  (45–60 s)
    # ─────────────────────────────────────────────────────────────────────────
    def part4_turbulence_formation(self):
        self.play(
            FadeOut(self._p3_title), FadeOut(self._p3_eq),
            run_time=0.6
        )

        t_title = title_text("Turbulence forms", size=32,
                              color=lerp_color(CONVECT_C, WHITE, 0.2))
        t_title.move_to([0, 3.2, 0])
        self.play(FadeIn(t_title, shift=DOWN*0.15), run_time=0.6)

        # Chaotic streams — high disturbance, random phases
        rng = np.random.default_rng(42)
        chaos_streams = VGroup(*[
            make_disturbed_stream(
                y, chord=self.CHORD, amplitude=0.22,
                disturbance_start=self.WX - self.CHORD * 0.1,
                disturbance_amp=0.28 + rng.uniform(0, 0.08),
                phase=rng.uniform(0, 2*np.pi),
                cx=self.WX, cy=self.WY,
                color=lerp_color(LAMINAR_C, TURB2_C, rng.uniform(0.1, 0.5)),
                stroke_w=1.2
            )
            for y in self.stream_ys
        ])
        chaos_streams.set_z_index(2)

        # Many vortices in wake
        wake_vortices = []
        positions = [
            (3.5,  0.55, 0.42), (4.2, -0.42, 0.35),
            (4.9,  0.20, 0.28), (5.5, -0.25, 0.22),
            (3.8, -0.70, 0.30), (4.6,  0.70, 0.25),
        ]
        for vx, vy, vr in positions:
            wake_vortices.append(
                make_vortex(vx, vy, radius=vr, n_turns=2.8,
                            color=lerp_color(VORTEX_C, TURB2_C,
                                             rng.uniform(0.2, 0.7)),
                            stroke_w=1.3)
            )
        wake_group = VGroup(*wake_vortices)
        wake_group.set_z_index(3)

        self.play(
            Transform(self._p3_streams,  chaos_streams, rate_func=smooth),
            Transform(self._p3_vortices, wake_group,    rate_func=smooth),
            run_time=2.2
        )

        # Irregular velocity arrows in wake
        irr_arrows = []
        for i, (ax, ay) in enumerate([
            (3.5,  0.55), (4.2, -0.42), (4.9,  0.20),
            (3.8, -0.70), (4.6,  0.70),
        ]):
            angle = rng.uniform(-0.8, 0.8)
            vx =  0.45 * np.cos(angle)
            vy =  0.45 * np.sin(angle)
            irr_arrows.append(
                make_velocity_arrow(ax, ay, vx=vx, vy=vy,
                                    color=lerp_color(LAMINAR_C, CONVECT_C, 0.4),
                                    sw=1.6)
            )
        irr_grp = VGroup(*irr_arrows)
        irr_grp.set_z_index(4)
        self.play(*[GrowArrow(a) for a in irr_arrows], run_time=1.0)

        # ── Turbulence effect: wing bounces up/down like real aircraft ────────
        # Simulate buffeting — 4 quick jolts of varying amplitude
        bounce_sequence = [
            ( 0.18,  0.35),   # up
            (-0.22,  0.30),   # down (bigger jolt)
            ( 0.14,  0.28),   # up
            (-0.10,  0.25),   # settle down
            ( 0.06,  0.22),   # small up
            ( 0.00,  0.25),   # return to centre
        ]
        for dy, rt in bounce_sequence:
            self.play(
                self._wing_obj.animate.shift(UP * dy),
                run_time=rt, rate_func=there_and_back if dy == 0.0 else smooth
            )

        # ── Viscosity term ─────────────────────────────────────────────────
        eq_visc = MathTex(r"\mu \nabla^2 \mathbf{v}",
                          font_size=40, color=DIFFUSE_C)
        eq_visc.move_to([0, 2.35, 0])
        lbl_visc = sub_text("Viscosity tries to smooth flow",
                            size=20, color=DIFFUSE_C)
        lbl_visc.move_to([0, 1.78, 0])
        visc_box = SurroundingRectangle(eq_visc, color=DIFFUSE_C,
                                         stroke_width=1.5, buff=0.14,
                                         corner_radius=0.07)

        self.play(Write(eq_visc), run_time=1.1)
        self.play(Create(visc_box), FadeIn(lbl_visc), run_time=0.6)
        self.wait(3.5)

        self._p4_chaos   = self._p3_streams
        self._p4_vort    = self._p3_vortices
        self._p4_arrows  = irr_grp
        self._p4_title   = t_title
        self._p4_eq      = VGroup(eq_visc, visc_box, lbl_visc)

    # ─────────────────────────────────────────────────────────────────────────
    # PART 5 — Convection vs Diffusion  (60–75 s)
    # ─────────────────────────────────────────────────────────────────────────
    def part5_competition(self):
        self.play(
            FadeOut(self._p4_title), FadeOut(self._p4_eq),
            FadeOut(self._p4_arrows), run_time=0.6
        )

        t_title = title_text("Convection  vs  Diffusion", size=30)
        t_title.move_to([0, 3.2, 0])
        self.play(FadeIn(t_title, shift=DOWN*0.15), run_time=0.6)

        # Two side-by-side labels with contrast arrows
        conv_lbl = Text("Convection\n(amplifies)", font_size=22,
                        color=CONVECT_C, font="Courier New", weight=BOLD)
        conv_lbl.move_to([-2.8, 2.45, 0])
        diff_lbl = Text("Diffusion\n(smooths)", font_size=22,
                        color=DIFFUSE_C, font="Courier New", weight=BOLD)
        diff_lbl.move_to([2.8, 2.45, 0])

        vs_lbl = title_text("vs", size=28, color=TEXT_MAIN)
        vs_lbl.move_to([0, 2.45, 0])

        self.play(FadeIn(conv_lbl), FadeIn(diff_lbl), FadeIn(vs_lbl),
                  run_time=0.7)

        # "When convection dominates…"
        dom_txt = sub_text("When convection dominates…", size=24,
                           color=lerp_color(CONVECT_C, WHITE, 0.3))
        dom_txt.move_to([0, 1.65, 0])
        uns_txt = sub_text("Flow becomes unstable", size=24,
                           color=lerp_color(CONVECT_C, TEXT_MAIN, 0.2))
        uns_txt.move_to([0, 1.18, 0])

        self.play(FadeIn(dom_txt, shift=LEFT*0.2), run_time=0.6)
        self.play(FadeIn(uns_txt, shift=LEFT*0.2), run_time=0.5)

        # Reynolds number equation — placed BELOW the wing to avoid overlap
        re_eq = MathTex(r"\mathrm{Re} = \frac{\rho V L}{\mu}",
                        font_size=38, color=HIGHLIGHT_BOX)
        re_eq.move_to([0, -1.85, 0])
        re_lbl = sub_text("High Reynolds number → turbulence",
                          size=20, color=HIGHLIGHT_BOX)
        re_lbl.move_to([0, -2.55, 0])
        re_box = SurroundingRectangle(re_eq, color=HIGHLIGHT_BOX,
                                      stroke_width=1.6, buff=0.16,
                                      corner_radius=0.08)
        self.play(Write(re_eq), run_time=1.3)
        self.play(Create(re_box), FadeIn(re_lbl), run_time=0.6)
        self.wait(4.5)

        self._p5_title = t_title
        self._p5_objs  = VGroup(conv_lbl, diff_lbl, vs_lbl,
                                 dom_txt, uns_txt, re_eq, re_box, re_lbl)

    # ─────────────────────────────────────────────────────────────────────────
    # PART 6 — Energy cascade  (75–85 s)
    # ─────────────────────────────────────────────────────────────────────────
    def part6_energy_cascade(self):
        self.play(
            FadeOut(self._p5_title), FadeOut(self._p5_objs),
            run_time=0.7
        )

        t_title = title_text("Energy transfers to smaller scales", size=28)
        t_title.move_to([0, 3.2, 0])
        self.play(FadeIn(t_title, shift=DOWN*0.15), run_time=0.6)

        # Cascade: large vortex → medium → small
        cascade_specs = [
            # (x, y, radius, turns, color_t)
            (2.2,  0.0,  0.60, 2.0, 0.1),
            (3.4,  0.45, 0.38, 2.4, 0.3),
            (3.4, -0.45, 0.38, 2.4, 0.3),
            (4.4,  0.70, 0.22, 2.8, 0.55),
            (4.4,  0.20, 0.22, 2.8, 0.55),
            (4.4, -0.30, 0.22, 2.8, 0.55),
            (5.2,  0.85, 0.13, 3.2, 0.75),
            (5.2,  0.42, 0.13, 3.2, 0.75),
            (5.2, -0.05, 0.13, 3.2, 0.75),
            (5.2, -0.50, 0.13, 3.2, 0.75),
        ]
        cascade_vorts = VGroup(*[
            make_vortex(vx, vy, radius=vr, n_turns=nt,
                        color=lerp_color(VORTEX_C, CONVECT_C, ct),
                        stroke_w=max(0.9, 1.8 - ct))
            for vx, vy, vr, nt, ct in cascade_specs
        ])
        cascade_vorts.set_z_index(4)

        # Arrows indicating cascade direction
        casc_arrow1 = Arrow([2.4, -1.0, 0], [3.6, -1.0, 0],
                            color=CONVECT_C, buff=0, stroke_width=2.0,
                            max_tip_length_to_length_ratio=0.25)
        casc_arrow2 = Arrow([3.6, -1.0, 0], [4.6, -1.0, 0],
                            color=lerp_color(CONVECT_C, DIFFUSE_C, 0.5),
                            buff=0, stroke_width=1.6,
                            max_tip_length_to_length_ratio=0.25)
        casc_arrow3 = Arrow([4.6, -1.0, 0], [5.4, -1.0, 0],
                            color=DIFFUSE_C, buff=0, stroke_width=1.2,
                            max_tip_length_to_length_ratio=0.25)
        casc_lbl = sub_text("Large → medium → small eddies",
                            size=19, color=lerp_color(TEXT_MAIN, VORTEX_C, 0.3))
        casc_lbl.move_to([4.0, -1.42, 0])

        # Animate cascade appearing in size order (large first)
        for i, v in enumerate(cascade_vorts):
            self.play(Create(v, rate_func=smooth),
                      run_time=0.28 + 0.04 * i)

        self.play(
            GrowArrow(casc_arrow1), GrowArrow(casc_arrow2),
            GrowArrow(casc_arrow3), run_time=0.8
        )
        self.play(FadeIn(casc_lbl), run_time=0.5)
        self.wait(3.5)

        self._p6_title = t_title
        self._p6_objs  = VGroup(cascade_vorts, casc_arrow1, casc_arrow2,
                                 casc_arrow3, casc_lbl)

    # ─────────────────────────────────────────────────────────────────────────
    # PART 7 — Prediction insight + full NS  (85–95 s)
    # ─────────────────────────────────────────────────────────────────────────
    def part7_prediction_insight(self):
        self.play(
            FadeOut(self._p6_title), FadeOut(self._p6_objs),
            FadeOut(self._p4_chaos), FadeOut(self._p4_vort),
            run_time=0.7
        )

        # ── Two-line insight ──────────────────────────────────────────────
        line1 = title_text("Turbulence is difficult to predict…",
                           size=27, color=TEXT_MAIN)
        line2 = title_text("…because of nonlinear interactions",
                           size=27, color=lerp_color(CONVECT_C, TEXT_MAIN, 0.3))
        line1.move_to([0,  3.1, 0])
        line2.move_to([0,  2.5, 0])
        self.play(FadeIn(line1, shift=DOWN*0.1), run_time=0.6)
        self.play(FadeIn(line2, shift=DOWN*0.1), run_time=0.6)

        # ── Full Navier–Stokes equation ───────────────────────────────────
        ns_full = MathTex(
            r"\rho",
            r"\left(\frac{\partial \mathbf{v}}{\partial t}",
            r"+",
            r"(\mathbf{v} \cdot \nabla)\mathbf{v}",
            r"\right)",
            r"=",
            r"-\nabla p",
            r"+",
            r"\mu \nabla^2 \mathbf{v}",
            r"+",
            r"\mathbf{f}",
            font_size=34, color=TEXT_MAIN
        )
        ns_full.move_to([0, 0.95, 0])

        # Colour each term semantically
        ns_full[3].set_color(CONVECT_C)   # convection term
        ns_full[8].set_color(DIFFUSE_C)   # viscosity term

        ns_box = SurroundingRectangle(
            ns_full, color=lerp_color(TEXT_MAIN, HIGHLIGHT_BOX, 0.25),
            stroke_width=1.4, buff=0.20, corner_radius=0.09
        )

        self.play(Write(ns_full), run_time=2.5)
        self.play(Create(ns_box), run_time=0.6)

        # Highlight convection term with a glow pulse
        conv_hl = SurroundingRectangle(
            ns_full[3], color=CONVECT_C, stroke_width=2.2, buff=0.08,
            corner_radius=0.05
        )
        # Label placed well below the equation box — no overlap
        nl_lbl = sub_text("Nonlinear — causes chaos", size=19,
                           color=CONVECT_C)
        nl_lbl.move_to([0, -2.55, 0])

        self.play(Create(conv_hl), FadeIn(nl_lbl), run_time=0.6)
        self.play(
            conv_hl.animate.set_stroke(opacity=0.2),
            run_time=0.5, rate_func=there_and_back
        )
        self.play(
            conv_hl.animate.set_stroke(opacity=1.0),
            run_time=0.4
        )

        # Closing message
        close_txt = sub_text(
            "Navier–Stokes captures the physics — but prediction remains hard",
            size=19, color=lerp_color(TEXT_SUB, WHITE, 0.2)
        )
        close_txt.move_to([0, -2.8, 0])
        self.play(FadeIn(close_txt, shift=UP*0.1), run_time=0.7)
        self.wait(3.5)