
from manim import *
import numpy as np

# ── palette ─────────────────────────────────────────────────────────────────
BG_COLOR      = "#0a0d14"
PIPE_COLOR    = "#dce3f0"
FLUID_DARK    = "#0d47a1"
FLUID_MID     = "#1976d2"
FLUID_BRIGHT  = "#40c4ff"
PRESSURE_HIGH = "#c62828"
PRESSURE_LOW  = "#0d47a1"
HIGHLIGHT     = "#00e5ff"
WARN_COLOR    = "#ffd54f"
TEXT_COLOR    = "#dce3f0"


def lc(c1, c2, t):
    t = float(np.clip(t, 0, 1))
    r1, g1, b1 = color_to_rgb(c1)
    r2, g2, b2 = color_to_rgb(c2)
    return rgb_to_color([r1+(r2-r1)*t, g1+(g2-g1)*t, b1+(b2-b1)*t])

def hdr(txt, size=32, color=HIGHLIGHT):
    return Text(txt, font_size=size, color=color,
                font="Courier New", weight=BOLD)

def lbl(txt, size=24, color=TEXT_COLOR):
    return Text(txt, font_size=size, color=color, font="Courier New")


# ══════════════════════════════════════════════════════════════════════════════
#  LAYOUT  (Manim default frame: 14.22 wide × 8.0 tall)
#  ─────────────────────────────────────────────────────
#  TEXT ZONE:   y ∈ [ 2.0,  3.8]
#  PIPE ZONE:   y ∈ [-3.6,  1.6]
#
#  Horizontal pipe  (Part 1):
#    top  y =  1.3,  bottom y = -0.3,  centre y = 0.5
#    x: -6.5 → 6.5   (full width, open ended — NO side caps)
#
#  L-pipe (Parts 2-6):
#    horizontal: x ∈ [-6.0, 2.8],  same y walls
#    vertical:   x ∈ [1.8, 2.8],   y ∈ [-0.3, -3.4]
#    inner corner at (1.8, -0.3), outer at (2.8, 1.3)
#
#  Curved pipe (Part 7):
#    arc centre at (LP_XR - R_O, H_TOP - R_O)

H_TOP    =  1.3
H_BOT    = -0.3
PIPE_CY  =  0.5
PIPE_HW  =  0.72

# straight pipe x extents
SP_X0    = -6.5
SP_X1    =  6.5

# L-pipe x extents
LP_X0    = -6.0
LP_XR    =  2.8   # outer (right) wall of vertical
LP_XL    =  1.8   # inner (left)  wall of vertical
Y_BOT    = -3.4   # bottom of vertical pipe

TEXT_Y   =  3.1
SUB_Y    =  2.3


# ══════════════════════════════════════════════════════════════════════════════
class Scene11_PipeBend(MovingCameraScene):

    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        self._fw = self.camera.frame.get_width()   # ≈ 14.22
        self._fh = self.camera.frame.get_height()  # ≈  8.0
        self.part1_straight_flow()
        self.part2_introduce_bend()
        self.part3_velocity_increase()
        self.part4_pressure_drop()
        self.part5_extreme_case()
        self.part6_boundary_layer()
        self.part7_engineering_insight()

    # =========================================================================
    # PART 1 — Straight pipe (0-15 s)
    # =========================================================================
    def part1_straight_flow(self):
        # Open-ended pipe: only top and bottom walls, no side caps
        pipe_top = Line([SP_X0, H_TOP, 0], [SP_X1, H_TOP, 0],
                        color=PIPE_COLOR, stroke_width=2.5)
        pipe_bot = Line([SP_X0, H_BOT, 0], [SP_X1, H_BOT, 0],
                        color=PIPE_COLOR, stroke_width=2.5)
        pipe = VGroup(pipe_top, pipe_bot)

        title = hdr("Flow in a straight pipe is stable", size=30)
        title.move_to([0, TEXT_Y, 0])

        # Arrows: 8 columns across full pipe length
        arrows = self._para_arrows(
            xs=np.linspace(SP_X0 + 0.5, SP_X1 - 1.2, 8),
            cy=PIPE_CY, hw=PIPE_HW
        )

        # ── FIX 1: Labels anchored LEFT, fully inside the frame ──────────────
        # Longest label width ≈ 3.6 world units at size 20.
        # Place left edge at x = -5.0 so label stays well inside [-6.5, 6.5].
        # Bold bright label inside the pipe — larger font + BOLD weight
        lbl_c = Text("center → high velocity", font_size=26, color=WHITE,
                     font="Courier New", weight=BOLD)
        lbl_w = Text("wall → low velocity (no-slip)", font_size=22,
                     color=lc(FLUID_BRIGHT, WHITE, 0.55),
                     font="Courier New", weight=BOLD)

        lbl_c.move_to([-1.0, PIPE_CY + 0.02, 0])
        lbl_w.move_to([-1.0, H_BOT - 0.42, 0])

        self.play(Create(pipe), run_time=1.0)
        self.play(FadeIn(title, shift=DOWN*0.15), run_time=0.7)
        self.play(*[GrowArrow(a) for a in arrows], run_time=1.5, rate_func=smooth)
        self.play(FadeIn(lbl_c), FadeIn(lbl_w), run_time=0.7)
        self._drift(arrows, RIGHT, 5.5)

        self._p1_pipe   = pipe
        self._p1_arrows = arrows
        self._p1_title  = title
        self._p1_lbls   = VGroup(lbl_c, lbl_w)

    # =========================================================================
    # PART 2 — Introduce the 90° bend (15-30 s)
    # =========================================================================
    def part2_introduce_bend(self):
        self.play(
            FadeOut(self._p1_title), FadeOut(self._p1_lbls),
            *[FadeOut(a) for a in self._p1_arrows],
            FadeOut(self._p1_pipe), run_time=0.9
        )

        l_pipe = self._l_pipe()
        l_pipe.set_z_index(2)
        self.play(Create(l_pipe), run_time=1.8, rate_func=smooth)

        q = hdr("What happens when flow turns sharply?", size=28)
        q.move_to([0, TEXT_Y, 0])
        self.play(FadeIn(q, shift=DOWN*0.15), run_time=0.7)

        streams = self._l_streams()
        for s in streams:
            s.set_z_index(1)
        self.play(*[Create(s) for s in streams], run_time=2.5, rate_func=smooth)

        sq = Square(side_length=0.5, color=HIGHLIGHT, stroke_width=1.8)
        sq.move_to([LP_XL + 0.25, H_BOT + 0.25, 0])
        sq.set_stroke(opacity=0.8).set_z_index(3)
        self.play(Create(sq), run_time=0.4)
        self.play(sq.animate.scale(1.4).set_stroke(opacity=0.0),
                  run_time=0.7, rate_func=smooth)
        self.play(FadeOut(sq), run_time=0.2)
        self.wait(0.8)

        self._l_pipe_obj  = l_pipe
        self._l_streams   = streams
        self._p2_title    = q

    # =========================================================================
    # PART 3 — Velocity increase (30-45 s)
    # =========================================================================
    def part3_velocity_increase(self):
        self.play(FadeOut(self._p2_title), run_time=0.4)

        t = hdr("Velocity increases in tight regions", size=30)
        t.move_to([0, TEXT_Y, 0])
        self.play(FadeIn(t, shift=DOWN*0.15), run_time=0.6)

        v_in   = self._inlet_arrows()
        v_bend = self._bend_arrows()
        self.play(*[GrowArrow(a) for a in v_in],  run_time=1.0)
        self.play(*[GrowArrow(a) for a in v_bend], run_time=0.9)
        self.play(
            *[a.animate.scale(1.65).set_color(HIGHLIGHT) for a in v_bend],
            run_time=1.2, rate_func=smooth
        )

        sub = lbl("Flow compresses → accelerates", size=22, color=HIGHLIGHT)
        sub.move_to([0, SUB_Y, 0])
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(2.5)

        self._p3_t = t; self._p3_s = sub
        self._v_in = v_in; self._v_bend = v_bend

    # =========================================================================
    # PART 4 — Pressure drop (45-60 s)
    # =========================================================================
    def part4_pressure_drop(self):
        self.play(
            FadeOut(self._p3_t), FadeOut(self._p3_s),
            *[FadeOut(a) for a in self._v_in],
            *[FadeOut(a) for a in self._v_bend], run_time=0.7
        )

        t = hdr("Higher velocity → lower pressure", size=30)
        t.move_to([0, TEXT_Y, 0])
        self.play(FadeIn(t, shift=DOWN*0.15), run_time=0.6)

        eq = MathTex(r"p + \tfrac{1}{2}\rho v^2 = \mathrm{const}",
                     color=TEXT_COLOR, font_size=36)
        eq.move_to([0, SUB_Y, 0])
        self.play(Write(eq), run_time=1.3)

        pmap = self._pressure_map()
        for pm in pmap:
            pm.set_z_index(-1)
        self.play(*[FadeIn(pm) for pm in pmap], run_time=1.1)

        lhi = lbl("HIGH pressure", size=19, color=PRESSURE_HIGH)
        llo = lbl("LOW pressure",  size=19, color=lc(FLUID_BRIGHT, WHITE, 0.3))
        lhi.move_to([LP_X0 + 2.0, H_BOT - 0.5, 0])
        # Shift LOW pressure label to the right, below vertical pipe section
        llo.move_to([LP_XR + 1.6, H_BOT - 1.5, 0])
        self.play(FadeIn(lhi), FadeIn(llo), run_time=0.6)
        self.wait(4.0)

        self._p4_t = t; self._p4_eq = eq
        self._pmap = pmap; self._p4_lbls = VGroup(lhi, llo)

    # =========================================================================
    # PART 5 — Extreme case (60-70 s)
    # =========================================================================
    def part5_extreme_case(self):
        self.play(
            FadeOut(self._p4_t), FadeOut(self._p4_eq),
            FadeOut(self._p4_lbls),
            *[FadeOut(pm) for pm in self._pmap], run_time=0.7
        )

        t = hdr("In ideal models…", size=32, color=PRESSURE_HIGH)
        t.move_to([0, TEXT_Y, 0])
        self.play(FadeIn(t, shift=DOWN*0.15), run_time=0.6)

        lines = VGroup(
            lbl("Velocity can become extremely large", size=26, color=HIGHLIGHT),
            lbl("Pressure can drop very low", size=26,
                color=lc(FLUID_BRIGHT, PRESSURE_LOW, 0.4)),
        ).arrange(DOWN, buff=0.32).move_to([0, SUB_Y - 0.15, 0])
        self.play(FadeIn(lines[0], shift=LEFT*0.2), run_time=0.6)
        self.play(FadeIn(lines[1], shift=LEFT*0.2), run_time=0.6)

        ext = self._extreme_arrows()
        self.play(*[GrowArrow(a) for a in ext], run_time=0.8)
        self.play(
            *[a.animate.set_color(PRESSURE_HIGH).scale(1.35) for a in ext],
            run_time=0.6, rate_func=there_and_back
        )

        warn_txt = Text(
            "  Not truly infinite in reality  \n"
            "  Viscosity & geometry limit extremes  ",
            font_size=20, color=WARN_COLOR, font="Courier New"
        )
        warn_box = SurroundingRectangle(warn_txt, color=WARN_COLOR,
                                        stroke_width=1.3, buff=0.16,
                                        corner_radius=0.07)
        warn = VGroup(warn_txt, warn_box).move_to([0, Y_BOT + 0.5, 0])
        self.play(FadeIn(warn, shift=UP*0.1), run_time=0.6)
        self.wait(1.5)

        self._p5_t = t; self._p5_lines = lines
        self._p5_ext = ext; self._p5_warn = warn

    # =========================================================================
    # PART 6 — Boundary layer zoom (70-82 s)   ← FIX 2
    # =========================================================================
    def part6_boundary_layer(self):
        self.play(
            FadeOut(self._p5_t), FadeOut(self._p5_lines),
            FadeOut(self._p5_warn),
            *[FadeOut(a) for a in self._p5_ext], run_time=0.6
        )

        # Zoom target: inner corner of the 90° bend
        zoom_pt = np.array([LP_XL + 0.55, H_BOT - 0.55, 0])
        zoom_w  = self._fw * 0.36          # 36 % of full width ≈ 5.1 world units

        self.play(
            self.camera.frame.animate
                .set_width(zoom_w)
                .move_to(zoom_pt),
            run_time=1.5, rate_func=smooth
        )

        # After zoom, compute camera frame corners in world space
        half_w = zoom_w / 2
        half_h = zoom_w / 2 * (self._fh / self._fw)  # maintain aspect

        # ── Boundary layer: two thin filled rects (NOT a cross) ───────────────
        # Vertical strip — along inner vertical wall (x = LP_XL), going downward
        bl_v = Rectangle(
            width=0.10, height=0.60,
            fill_color=HIGHLIGHT, fill_opacity=0.55, stroke_width=0
        ).move_to([LP_XL + 0.05, H_BOT - 0.30, 0])

        # Horizontal strip — along pipe bottom wall (y = H_BOT), going rightward
        bl_h = Rectangle(
            width=0.60, height=0.10,
            fill_color=HIGHLIGHT, fill_opacity=0.55, stroke_width=0
        ).move_to([LP_XL + 0.30, H_BOT - 0.05, 0])

        self.play(FadeIn(bl_v), FadeIn(bl_h), run_time=0.8)

        # ── All text in WORLD COORDS, offset from zoom_pt ────────────────────
        # Keep font sizes very small so they fit inside the zoomed viewport.
        # Zoomed half-width ≈ 2.55 world units; text must stay within ±2.3 of zoom_pt.

        # Title: pushed higher above the pipe corner to avoid overlap
        t = Text("Boundary layer limits extremes", font_size=13,
                 color=HIGHLIGHT, font="Courier New", weight=BOLD)
        t.move_to(zoom_pt + UP * (half_h * 0.88))

        self.play(FadeIn(t), run_time=0.5)

        # Small slow arrows along the vertical boundary-layer strip
        bl_arrows = []
        for dy in np.linspace(0.0, -0.40, 4):
            arr = Arrow(
                start=[LP_XL + 0.25, H_BOT + dy,        0],
                end  =[LP_XL + 0.25, H_BOT + dy - 0.11, 0],
                color=lc(FLUID_DARK, FLUID_MID, 0.6),
                buff=0, stroke_width=1.0,
                max_tip_length_to_length_ratio=0.45
            )
            bl_arrows.append(arr)
        self.play(*[GrowArrow(a) for a in bl_arrows], run_time=0.7)

        # Explain text: pushed well below, bold white so it pops against the dark bg
        exp = VGroup(
            Text("Viscosity prevents infinite accel.", font_size=12,
                 color=WHITE, font="Courier New", weight=BOLD),
            Text("Flow separates & dissipates energy", font_size=12,
                 color=WHITE, font="Courier New", weight=BOLD),
        ).arrange(DOWN, buff=0.12).move_to(zoom_pt + DOWN * (half_h * 0.84))

        self.play(FadeIn(exp, shift=UP*0.06), run_time=0.6)
        self.wait(2.5)

        self._p6_t = t; self._p6_bl = VGroup(bl_v, bl_h)
        self._p6_arrows = bl_arrows; self._p6_exp = exp

    # =========================================================================
    # PART 7 — Engineering insight (82-92 s)   ← FIX 3
    # =========================================================================
    def part7_engineering_insight(self):
        self.play(
            FadeOut(self._p6_t), FadeOut(self._p6_bl),
            FadeOut(self._p6_exp),
            *[FadeOut(a) for a in self._p6_arrows], run_time=0.5
        )
        # Restore full view
        self.play(
            self.camera.frame.animate
                .set_width(self._fw)
                .move_to(ORIGIN),
            run_time=1.3, rate_func=smooth
        )

        t = hdr("Sharp bends cause losses and damage", size=30,
                color=PRESSURE_HIGH)
        t.move_to([0, TEXT_Y, 0])
        sub = lbl("Engineers design smooth curves instead", size=24,
                  color=HIGHLIGHT)
        sub.move_to([0, SUB_Y, 0])
        self.play(FadeIn(t, shift=DOWN*0.15), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)

        curved, AC, R_O, R_I = self._curved_pipe()
        self.play(
            FadeOut(self._l_pipe_obj),
            *[FadeOut(s) for s in self._l_streams], run_time=0.6
        )
        self.play(Create(curved), run_time=1.8, rate_func=smooth)

        sm = self._smooth_streams(AC, R_O, R_I)
        self.play(*[Create(s, rate_func=smooth) for s in sm], run_time=2.0)

        glow = curved.copy().set_stroke(HIGHLIGHT, width=5, opacity=0.4)
        self.play(FadeIn(glow), run_time=0.4)
        self.play(glow.animate.set_stroke(opacity=0.0), run_time=1.0)

        note = lbl("Smooth geometry → stable flow → longer pipe life",
                   size=21, color=lc(TEXT_COLOR, HIGHLIGHT, 0.35))
        note.move_to([0, Y_BOT + 0.42, 0])
        self.play(FadeIn(note, shift=UP*0.1), run_time=0.6)
        self.wait(2.2)

    # =========================================================================
    # ─────────────────────────  GEOMETRY  ────────────────────────────────────
    # =========================================================================

    def _para_arrows(self, xs, cy, hw):
        out = []
        for x in xs:
            for yf in np.linspace(-1.0, 1.0, 7):
                v   = max(1.0 - yf**2, 0.04)
                col = lc(FLUID_DARK, FLUID_BRIGHT, v)
                out.append(Arrow(
                    start=[x,          cy + yf*hw, 0],
                    end  =[x + v*0.48, cy + yf*hw, 0],
                    color=col, buff=0, stroke_width=1.6,
                    max_tip_length_to_length_ratio=0.30,
                ))
        return out

    def _drift(self, arrows, direction, total_time):
        d = direction * 0.50
        for _ in range(2):
            self.play(*[a.animate.shift(d) for a in arrows],
                      run_time=total_time/2, rate_func=linear)
            for a in arrows:
                a.shift(-d)

    def _l_pipe(self):
        segs = [
            Line([LP_X0,  H_TOP,  0], [LP_XR,  H_TOP,  0]),
            Line([LP_X0,  H_BOT,  0], [LP_XL,  H_BOT,  0]),
            Line([LP_XR,  H_TOP,  0], [LP_XR,  Y_BOT,  0]),
            Line([LP_XL,  H_BOT,  0], [LP_XL,  Y_BOT,  0]),
            Line([LP_XL,  Y_BOT,  0], [LP_XR,  Y_BOT,  0]),
            Line([LP_X0,  H_BOT,  0], [LP_X0,  H_TOP,  0]),
        ]
        return VGroup(*[s.set_stroke(color=PIPE_COLOR, width=2.5) for s in segs])

    def _l_streams(self):
        out   = []
        n     = 5
        y_pos = np.linspace(H_BOT + 0.12, H_TOP - 0.12, n)
        x_trn = np.linspace(LP_XL + 0.12, LP_XR - 0.12, n)
        cols  = [lc(FLUID_MID, FLUID_BRIGHT, i/(n-1)) for i in range(n)]

        for cy, xt, col in zip(y_pos, x_trn, cols):
            p0 = np.array([LP_X0 + 0.2, cy, 0])
            p1 = np.array([xt - 0.35,   cy, 0])
            p2 = np.array([xt,           cy, 0])
            p3 = np.array([xt,           cy - 0.40, 0])
            p4 = np.array([xt,           Y_BOT + 0.12, 0])

            out.append(Line(p0, p1, color=col, stroke_width=1.5))
            out.append(CubicBezier(
                p1, p1 + RIGHT*0.30,
                p3 + UP*0.30, p3,
                color=col, stroke_width=1.5
            ))
            out.append(Line(p3, p4, color=col, stroke_width=1.5))
        return out

    def _inlet_arrows(self):
        out = []
        for yf in np.linspace(-1.0, 1.0, 5):
            v   = max(1.0 - yf**2, 0.10)
            col = lc(FLUID_DARK, FLUID_BRIGHT, v)
            y   = PIPE_CY + yf * PIPE_HW
            out.append(Arrow(
                start=[LP_X0 + 1.0, y, 0],
                end  =[LP_X0 + 1.0 + v*0.70, y, 0],
                color=col, buff=0, stroke_width=2.0,
                max_tip_length_to_length_ratio=0.28
            ))
        return out

    def _bend_arrows(self):
        out = []
        xs  = np.linspace(LP_XL + 0.18, LP_XR - 0.18, 3)
        for x in xs:
            f   = (x - LP_XL) / (LP_XR - LP_XL)
            v   = 0.85 - 0.38 * f
            col = lc(HIGHLIGHT, FLUID_MID, f)
            out.append(Arrow(
                start=[x, H_BOT - 0.08, 0],
                end  =[x, H_BOT - 0.08 - v*0.60, 0],
                color=col, buff=0, stroke_width=2.0,
                max_tip_length_to_length_ratio=0.27
            ))
        return out

    def _pressure_map(self):
        rects = []
        xs = np.linspace(LP_X0, LP_XL, 9)
        for i in range(len(xs)-1):
            t   = i / (len(xs)-2)
            r   = Rectangle(
                width=xs[i+1]-xs[i], height=H_TOP-H_BOT,
                fill_color=lc(PRESSURE_HIGH, PRESSURE_LOW, t),
                fill_opacity=0.28, stroke_width=0
            ).move_to([(xs[i]+xs[i+1])/2, (H_TOP+H_BOT)/2, 0])
            rects.append(r)
        ys = np.linspace(H_BOT, Y_BOT, 7)
        for j in range(len(ys)-1):
            t   = j / (len(ys)-2)
            r   = Rectangle(
                width=LP_XR-LP_XL, height=abs(ys[j+1]-ys[j]),
                fill_color=lc(PRESSURE_LOW, lc(PRESSURE_LOW, BG_COLOR, 0.45), t),
                fill_opacity=0.28, stroke_width=0
            ).move_to([(LP_XL+LP_XR)/2, (ys[j]+ys[j+1])/2, 0])
            rects.append(r)
        return rects

    def _extreme_arrows(self):
        out = []
        for x in np.linspace(LP_XL + 0.18, LP_XR - 0.18, 3):
            out.append(Arrow(
                start=[x, H_BOT - 0.08, 0],
                end  =[x, H_BOT - 0.82, 0],
                color=HIGHLIGHT, buff=0, stroke_width=2.2,
                max_tip_length_to_length_ratio=0.24
            ))
        return out

    # ── Curved elbow pipe  ← FIX 3 ──────────────────────────────────────────
    def _curved_pipe(self):
        """
        Outer arc radius R_O, inner arc radius R_I.
        Arc centre AC chosen so:
          outer arc starts at (LP_X0 side): horizontal top wall ends at
            x = AC[0], y = H_TOP  (arc at angle PI/2)
          outer arc ends at:
            x = AC[0]+R_O, y = AC[1]  (arc at angle 0  → vertical wall)
          inner arc (same centre):
            starts at (AC[0], AC[1]+R_I) == (AC[0], H_BOT) → so AC[1] = H_BOT - R_I
            ends at   (AC[0]+R_I, AC[1])

        For AC[1]+R_O = H_TOP  →  AC[1] = H_TOP - R_O
        For AC[1]+R_I = H_BOT  →  AC[1] = H_BOT - R_I

        We need both to hold. Choose R_O and R_I to satisfy:
            H_TOP - R_O = H_BOT - R_I
            R_O - R_I   = H_TOP - H_BOT = 1.6

        Pick R_I = 0.4  → R_O = 2.0
        Then AC[1] = H_TOP - R_O = 1.3 - 2.0 = -0.7
        AC[0] can be anything; keep vertical pipe at same x as L-pipe:
            outer vert wall at x = AC[0]+R_O = LP_XR  → AC[0] = LP_XR - R_O
            inner vert wall at x = AC[0]+R_I = LP_XL  → AC[0] = LP_XL - R_I
        Both must agree: LP_XR - R_O = LP_XL - R_I
            2.8 - 2.0 = 0.8,  1.8 - 0.4 = 1.4  (don't agree with LP_X values)

        Solution: derive AC[0] from outer wall position and accept that inner
        wall x = AC[0]+R_I may differ slightly from LP_XL (cosmetically fine).
        Use LP_XR as the reference for the outer wall.
        """
        R_O  = 2.0
        R_I  = 0.4
        # AC[1]: outer arc must touch H_TOP at PI/2 → AC[1] + R_O = H_TOP
        AC_y = H_TOP - R_O          # = 1.3 - 2.0 = -0.7
        # outer vert wall = LP_XR → AC[0] + R_O = LP_XR
        AC_x = LP_XR - R_O          # = 2.8 - 2.0 = 0.8
        AC   = np.array([AC_x, AC_y, 0])

        # Derived wall x positions
        x_outer_vert = AC_x + R_O   # = LP_XR = 2.8  ✓
        x_inner_vert = AC_x + R_I   # = 1.2  (slightly different from LP_XL=1.8)

        # Horizontal walls meet arc at:
        #   outer: (AC_x, AC_y + R_O) = (AC_x, H_TOP)
        #   inner: (AC_x, AC_y + R_I) = (AC_x, AC_y + 0.4) = (AC_x, -0.3) = H_BOT ✓
        h_inner_join_y = AC_y + R_I  # should equal H_BOT

        segs = []
        # Horizontal top wall
        segs.append(Line([LP_X0, H_TOP, 0], [AC_x, H_TOP, 0],
                         color=PIPE_COLOR, stroke_width=2.5))
        # Horizontal bottom wall
        segs.append(Line([LP_X0, H_BOT, 0], [AC_x, h_inner_join_y, 0],
                         color=PIPE_COLOR, stroke_width=2.5))
        # Outer arc: PI/2 → 0
        arc_o = Arc(radius=R_O, start_angle=PI/2, angle=-PI/2,
                    color=PIPE_COLOR, stroke_width=2.5)
        arc_o.move_arc_center_to(AC)
        segs.append(arc_o)
        # Inner arc: PI/2 → 0
        arc_i = Arc(radius=R_I, start_angle=PI/2, angle=-PI/2,
                    color=PIPE_COLOR, stroke_width=2.5)
        arc_i.move_arc_center_to(AC)
        segs.append(arc_i)
        # Outer vertical wall
        segs.append(Line([x_outer_vert, AC_y, 0], [x_outer_vert, Y_BOT, 0],
                         color=PIPE_COLOR, stroke_width=2.5))
        # Inner vertical wall
        segs.append(Line([x_inner_vert, AC_y, 0], [x_inner_vert, Y_BOT, 0],
                         color=PIPE_COLOR, stroke_width=2.5))
        # Bottom cap
        segs.append(Line([x_inner_vert, Y_BOT, 0], [x_outer_vert, Y_BOT, 0],
                         color=PIPE_COLOR, stroke_width=2.5))
        # Inlet cap
        segs.append(Line([LP_X0, H_BOT, 0], [LP_X0, H_TOP, 0],
                         color=PIPE_COLOR, stroke_width=2.5))

        return VGroup(*segs), AC, R_O, R_I

    def _smooth_streams(self, AC, R_O, R_I):
        """
        Streamlines at radii between R_I and R_O from arc centre AC.
        Each: horizontal entry → quarter-circle arc → vertical drop.
        """
        out  = []
        n    = 5
        gap  = 0.06
        radii = np.linspace(R_I + gap, R_O - gap, n)
        cols  = [lc(FLUID_MID, FLUID_BRIGHT, i/(n-1)) for i in range(n)]

        for r, col in zip(radii, cols):
            hy  = AC[1] + r     # y of horizontal entry line
            vx  = AC[0] + r     # x of vertical drop line
            # Horizontal entry from left edge to arc join
            seg_h = Line([LP_X0 + 0.2, hy, 0], [AC[0], hy, 0],
                         color=col, stroke_width=1.5)
            # Quarter-circle arc PI/2 → 0
            arc = Arc(radius=r, start_angle=PI/2, angle=-PI/2,
                      color=col, stroke_width=1.5)
            arc.move_arc_center_to(AC)
            # Vertical drop from arc end to bottom
            seg_v = Line([vx, AC[1], 0], [vx, Y_BOT + 0.12, 0],
                         color=col, stroke_width=1.5)
            out.extend([seg_h, arc, seg_v])
        return out