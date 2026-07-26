from manim import *
import numpy as np


class Scene6_Assumptions(Scene):
    def construct(self):
        # ── Palette ─────────────────────────────────────────────────────────
        BG_COLOR        = "#0D0D1A"
        FLUID_BLUE      = "#3A7BD5"
        FLUID_BLUE_DARK = "#1A3A6B"
        PANEL_BG        = "#12122A"
        NEWTONIAN_CLR   = "#FF8C42"
        INCOMP_CLR      = "#00D4FF"
        ISOTHERM_CLR    = "#FF5555"

        self.camera.background_color = BG_COLOR

        # ── Subtle animated background ribbons ──────────────────────────────
        def make_ribbon(y_pos, amp, phase, alpha=0.07):
            return always_redraw(lambda: ParametricFunction(
                lambda t: np.array([
                    t,
                    y_pos + amp * np.sin(1.8 * t + phase + self.renderer.time * 0.5),
                    0,
                ]),
                t_range=[-8, 8, 0.06],
                color=FLUID_BLUE,
                stroke_width=1.4,
                stroke_opacity=alpha,
            ))

        self.add(VGroup(
            make_ribbon(-3.2, 0.18, 0.0),
            make_ribbon(-1.6, 0.22, 1.1),
            make_ribbon( 0.0, 0.16, 2.3),
            make_ribbon( 1.6, 0.20, 3.4),
            make_ribbon( 3.2, 0.17, 4.6),
        ))

        # ════════════════════════════════════════════════════════════════════
        # PART 1  |  NS Equation intro
        # ════════════════════════════════════════════════════════════════════
        ns_eq = MathTex(
            r"\rho\!\left(\frac{\partial \mathbf{v}}{\partial t}"
            r"+ \mathbf{v}\cdot\nabla\mathbf{v}\right)"
            r"= -\nabla p + \mu\nabla^2\mathbf{v} + \mathbf{f}",
            color=WHITE,
        ).scale(0.78).move_to(ORIGIN)

        self.play(FadeIn(ns_eq), run_time=1.8)
        self.wait(2.0)   # was 0.6 — let viewers read the equation

        header = Text(
            "But this equation assumes something…",
            font_size=30, color=WHITE, slant=ITALIC,
        ).to_edge(UP, buff=0.55)

        self.play(
            ns_eq.animate.set_opacity(0.22).scale(0.82).shift(DOWN * 0.5),
            FadeIn(header, shift=DOWN * 0.15),
            run_time=1.8, rate_func=smooth,
        )
        self.wait(2.5)   # was 1.4 — give header time to sink in

        self.play(FadeOut(ns_eq, header), run_time=1.0)
        self.wait(0.5)

        # ════════════════════════════════════════════════════════════════════
        # PART 2  |  Three assumption panels
        # ════════════════════════════════════════════════════════════════════
        PANEL_TOP  = 3.30
        PANEL_W    = 3.80
        PANEL_H    = 0.90
        PANEL_GAP  = 0.22
        PANEL_XS   = [-(PANEL_W + PANEL_GAP), 0, +(PANEL_W + PANEL_GAP)]
        P_TITLES   = ["Newtonian Fluid", "Incompressible Flow", "Isothermal Flow"]
        P_COLORS   = [NEWTONIAN_CLR, INCOMP_CLR, ISOTHERM_CLR]

        def build_panel(title, clr, px):
            rect  = RoundedRectangle(
                corner_radius=0.16,
                width=PANEL_W, height=PANEL_H,
                fill_color=PANEL_BG, fill_opacity=0.90,
                stroke_color=clr, stroke_width=1.8,
            ).move_to(RIGHT * px + UP * PANEL_TOP)
            label = Text(title, font_size=20, color=clr, weight=BOLD
                         ).move_to(rect.get_center())
            return VGroup(rect, label)

        panels    = [build_panel(t, c, x)
                     for t, c, x in zip(P_TITLES, P_COLORS, PANEL_XS)]
        panels_vg = VGroup(*panels)

        self.play(
            LaggedStart(*[FadeIn(p, scale=0.90) for p in panels],
                        lag_ratio=0.30, run_time=2.2),   # was lag 0.22, run 1.6
        )
        self.wait(1.5)   # was 0.5

        # ── Panel helpers ────────────────────────────────────────────────────
        def activate_panel(idx):
            anims = []
            for i, p in enumerate(panels):
                rect, lbl = p[0], p[1]
                if i == idx:
                    anims += [
                        rect.animate.set_stroke(width=3.2).set_fill(opacity=0.96),
                        lbl.animate.set_opacity(1.0),
                    ]
                else:
                    anims += [
                        rect.animate.set_stroke(width=1.0).set_fill(opacity=0.30),
                        lbl.animate.set_opacity(0.28),
                    ]
            return anims

        def reset_panels():
            anims = []
            for p, c in zip(panels, P_COLORS):
                rect, lbl = p[0], p[1]
                anims += [
                    rect.animate.set_stroke(color=c, width=1.8).set_fill(opacity=0.90),
                    lbl.animate.set_opacity(1.0),
                ]
            return anims

        # ── Layout constants ──────────────────────────────────────────────────
        VIS_X   = -2.8
        TEXT_X  =  2.6
        VIS_TOP =  1.30
        NOTE_Y  = -2.55

        # ════════════════════════════════════════════════════════════════════
        # PART 3  |  Newtonian Fluid
        # ════════════════════════════════════════════════════════════════════
        self.play(*activate_panel(0), run_time=0.8, rate_func=smooth)
        self.wait(0.5)   # was 0.2

        # LEFT: two fluid layers
        LW, LH = 3.20, 0.52
        layer_top = Rectangle(width=LW, height=LH,
                               fill_color=FLUID_BLUE, fill_opacity=0.80,
                               stroke_width=0
                               ).move_to(RIGHT * VIS_X + UP * VIS_TOP)
        layer_bot = Rectangle(width=LW, height=LH,
                               fill_color=FLUID_BLUE_DARK, fill_opacity=0.90,
                               stroke_width=0
                               ).move_to(RIGHT * VIS_X + UP * (VIS_TOP - LH - 0.04))

        def row_arrows(n, length, y, color):
            grp = VGroup()
            xs  = np.linspace(VIS_X - LW / 2 + 0.35, VIS_X + LW / 2 - 0.35, n)
            for x in xs:
                grp.add(Arrow(
                    start=RIGHT * x + UP * y,
                    end  =RIGHT * x + UP * y + RIGHT * length,
                    color=color, buff=0,
                    stroke_width=2.2, tip_length=0.14,
                ))
            return grp

        arr_top = row_arrows(4, 0.72, VIS_TOP,            NEWTONIAN_CLR)
        arr_bot = row_arrows(4, 0.30, VIS_TOP - LH - 0.04, NEWTONIAN_CLR)

        lbl_fast = Text("fast", font_size=15, color=NEWTONIAN_CLR
                        ).next_to(layer_top, LEFT, buff=0.20)
        lbl_slow = Text("slow", font_size=15, color=NEWTONIAN_CLR
                        ).next_to(layer_bot, LEFT, buff=0.20)

        bar_h = LH * 2 + 0.15
        grad_bar = Rectangle(width=0.16, height=bar_h,
                              fill_color=NEWTONIAN_CLR, fill_opacity=0.50,
                              stroke_width=0
                              ).next_to(layer_top, LEFT, buff=0.65
                              ).shift(DOWN * (bar_h / 2 - LH / 2))
        grad_lbl = Text("du/dy", font_size=12, color=NEWTONIAN_CLR,
                        ).next_to(grad_bar, LEFT, buff=0.06)

        vis_newton = VGroup(layer_top, layer_bot, arr_top, arr_bot,
                            lbl_fast, lbl_slow, grad_bar, grad_lbl)

        # RIGHT: equation + legend
        stress_eq = MathTex(r"\tau = \mu\,\dfrac{du}{dy}",
                            color=NEWTONIAN_CLR, font_size=44
                            ).move_to(RIGHT * TEXT_X + UP * VIS_TOP)

        def leg_row(sym, desc, clr):
            return VGroup(
                MathTex(sym, color=clr, font_size=21),
                Text("—", font_size=17, color=WHITE),
                Text(desc, font_size=17, color=WHITE),
            ).arrange(RIGHT, buff=0.12)

        legend = VGroup(
            leg_row(r"\tau",  "internal force per area",       NEWTONIAN_CLR),
            leg_row(r"\mu",   "viscosity (fluid thickness)",   NEWTONIAN_CLR),
            leg_row(r"du/dy", "velocity change across layers", NEWTONIAN_CLR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18
                  ).next_to(stress_eq, DOWN, buff=0.30)

        contrast = VGroup(
            Text("Honey  →  high μ  (thick, slow)", font_size=17, color=NEWTONIAN_CLR),
            Text("Water  →  low  μ  (thin, fast)",  font_size=17, color="#99CCFF"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12
                  ).next_to(legend, DOWN, buff=0.22)

        note_newton = Text(
            "Viscosity is constant  →  Newtonian fluid",
            font_size=22, color=WHITE, weight=BOLD,
        ).move_to(UP * NOTE_Y)

        self.play(FadeIn(vis_newton),                          run_time=1.2)   # was 0.9
        self.wait(1.0)
        self.play(Write(stress_eq),                            run_time=1.5)   # was 1.0
        self.wait(1.0)
        self.play(FadeIn(legend,   shift=UP * 0.10),           run_time=1.2)   # was 0.9
        self.wait(1.2)   # new — let legend be read
        self.play(FadeIn(contrast),                            run_time=1.0)   # was 0.7
        self.wait(1.2)   # new — let contrast examples be read
        self.play(Write(note_newton),                          run_time=1.2)   # was 0.9
        self.wait(2.5)   # was 1.2 — key takeaway reading time

        newton_grp = VGroup(vis_newton, stress_eq, legend, contrast, note_newton)
        self.play(*activate_panel(1),
                  FadeOut(newton_grp), run_time=0.9, rate_func=smooth)

        # ════════════════════════════════════════════════════════════════════
        # PART 4  |  Incompressible Flow
        # ════════════════════════════════════════════════════════════════════
        self.wait(0.5)   # was 0.2

        # LEFT: control-volume box
        BOX_W, BOX_H = 2.00, 1.60
        ctrl_box = Rectangle(
            width=BOX_W, height=BOX_H,
            fill_color="#001A33", fill_opacity=0.70,
            stroke_color=INCOMP_CLR, stroke_width=2.2,
        ).move_to(RIGHT * VIS_X + UP * (VIS_TOP - BOX_H / 2))

        N = 5
        dy = BOX_H / (N + 1)
        box_y0 = ctrl_box.get_bottom()[1]

        def dot_col(side_sign, x_offset):
            col = VGroup()
            for k in range(N):
                y = box_y0 + dy * (k + 1)
                x = VIS_X + side_sign * (BOX_W / 2 + x_offset)
                col.add(Dot(radius=0.10, color=FLUID_BLUE
                            ).move_to(RIGHT * x + UP * y))
            return col

        in_dots  = dot_col(-1, 0.50)
        out_dots = dot_col(+1, 0.50)

        def flow_arrs(dots, sign):
            grp = VGroup()
            for d in dots:
                c = d.get_center()
                grp.add(Arrow(c + LEFT * 0.28 * sign, c + RIGHT * 0.28 * sign,
                              color=INCOMP_CLR, buff=0,
                              stroke_width=1.8, tip_length=0.12))
            return grp

        in_arr  = flow_arrs(in_dots,  +1)
        out_arr = flow_arrs(out_dots, +1)

        lbl_in  = Text("in",  font_size=16, color=INCOMP_CLR
                       ).next_to(in_dots,  LEFT,  buff=0.10)
        lbl_out = Text("out", font_size=16, color=INCOMP_CLR
                       ).next_to(out_dots, RIGHT, buff=0.10)
        lbl_eq_flow = Text("same count in & out", font_size=15, color=WHITE
                           ).next_to(ctrl_box, DOWN, buff=0.18)

        vis_incomp = VGroup(ctrl_box, in_dots, out_dots,
                            in_arr, out_arr, lbl_in, lbl_out, lbl_eq_flow)

        # RIGHT: ∇·v = 0
        div_eq = MathTex(r"\nabla \cdot \mathbf{v} = 0",
                         color=INCOMP_CLR, font_size=46
                         ).move_to(RIGHT * TEXT_X + UP * VIS_TOP)

        incomp_bullets = VGroup(
            Text("✓  No compression",        font_size=20, color=WHITE),
            Text("✓  No expansion",          font_size=20, color=WHITE),
            Text("✓  Volume stays constant", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22
                  ).next_to(div_eq, DOWN, buff=0.32)

        note_incomp = Text(
            "Density remains constant at every point",
            font_size=22, color=WHITE, weight=BOLD,
        ).move_to(UP * NOTE_Y)

        self.play(FadeIn(vis_incomp),                          run_time=1.2)   # was 0.9
        self.wait(1.0)
        self.play(Write(div_eq),                               run_time=1.5)   # was 1.0
        self.wait(1.0)
        self.play(FadeIn(incomp_bullets, shift=UP * 0.10),     run_time=1.2)   # was 0.9
        self.wait(1.5)   # new — let bullets be read
        self.play(Write(note_incomp),                          run_time=1.2)   # was 0.9
        self.wait(2.5)   # was 1.2

        incomp_grp = VGroup(vis_incomp, div_eq, incomp_bullets, note_incomp)
        self.play(*activate_panel(2),
                  FadeOut(incomp_grp), run_time=0.9, rate_func=smooth)

        # ════════════════════════════════════════════════════════════════════
        # PART 5  |  Isothermal Flow
        # ════════════════════════════════════════════════════════════════════
        self.wait(0.5)   # was 0.2

        # LEFT: hot-to-cold gradient → transforms to uniform blue
        GRAD_W, GRAD_H = 3.10, 1.10
        NS = 20
        grad_ctr = RIGHT * VIS_X + UP * (VIS_TOP - GRAD_H / 2)

        def make_grad_vg(left_hex, right_hex):
            strips = VGroup()
            sw = GRAD_W / NS
            for i in range(NS):
                frac = i / (NS - 1)
                c = interpolate_color(
                    ManimColor(left_hex), ManimColor(right_hex), frac)
                strips.add(Rectangle(
                    width=sw, height=GRAD_H,
                    fill_color=c, fill_opacity=0.88, stroke_width=0,
                ).move_to(grad_ctr + LEFT * (GRAD_W / 2 - sw * (i + 0.5))))
            border = SurroundingRectangle(
                strips, color=ISOTHERM_CLR, buff=0, stroke_width=2.0)
            return VGroup(strips, border)

        hot_grad  = make_grad_vg("#FF2200", "#3A7BD5")
        cold_grad = make_grad_vg("#3A7BD5", "#3A7BD5")

        temp_hot  = Text("Non-uniform temperature", font_size=16, color=WHITE
                         ).next_to(hot_grad,  DOWN, buff=0.16)
        temp_cold = Text("Uniform temperature",     font_size=16, color="#99CCFF"
                         ).next_to(cold_grad, DOWN, buff=0.16)

        # H/C legend dots
        hot_dot  = Dot(color="#FF2200", radius=0.11
                       ).next_to(hot_grad, LEFT, buff=0.30).shift(UP * 0.22)
        cold_dot = Dot(color="#3A7BD5", radius=0.11
                       ).next_to(hot_grad, LEFT, buff=0.30).shift(DOWN * 0.22)
        Line(hot_dot.get_center(), cold_dot.get_center(),
             color=WHITE, stroke_width=1.2)
        hot_t  = Text("Hot",  font_size=12, color="#FF8888"
                      ).next_to(hot_dot,  LEFT, buff=0.06)
        cold_t = Text("Cold", font_size=12, color="#99CCFF"
                      ).next_to(cold_dot, LEFT, buff=0.06)
        scale_vg = VGroup(hot_dot, cold_dot, hot_t, cold_t)

        vis_iso = VGroup(hot_grad, temp_hot, scale_vg)

        # RIGHT: isothermal explanation
        iso_title = Text("Temperature remains constant",
                         font_size=21, color=ISOTHERM_CLR, weight=BOLD
                         ).move_to(RIGHT * TEXT_X + UP * VIS_TOP)

        iso_bullets = VGroup(
            Text("✓  No heat transfer",           font_size=20, color=WHITE),
            Text("✓  No thermal expansion",       font_size=20, color=WHITE),
            Text("✓  Density unaffected by temp", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22
                  ).next_to(iso_title, DOWN, buff=0.32)

        note_iso = Text(
            "Isothermal  →  simplifies energy coupling",
            font_size=22, color=WHITE, weight=BOLD,
        ).move_to(UP * NOTE_Y)

        self.play(FadeIn(vis_iso),                             run_time=1.2)   # was 0.9
        self.wait(1.5)   # was 0.5 — let hot gradient be read
        self.play(
            Transform(hot_grad,  cold_grad,  run_time=2.0, rate_func=smooth),   # was 1.3
            Transform(temp_hot,  temp_cold,  run_time=2.0, rate_func=smooth),
            FadeOut(scale_vg,               run_time=1.2),
        )
        self.wait(1.0)   # pause after transform
        self.play(Write(iso_title),                            run_time=1.2)   # was 0.9
        self.wait(0.8)
        self.play(FadeIn(iso_bullets, shift=UP * 0.10),        run_time=1.2)   # was 0.9
        self.wait(1.5)   # new — let bullets be read
        self.play(Write(note_iso),                             run_time=1.2)   # was 0.9
        self.wait(2.5)   # was 1.2

        iso_grp = VGroup(hot_grad, temp_hot, scale_vg,
                         iso_title, iso_bullets, note_iso)
        self.play(FadeOut(iso_grp), run_time=1.0)

        # ════════════════════════════════════════════════════════════════════
        # PART 6  |  All panels + summary
        # ════════════════════════════════════════════════════════════════════
        self.play(*reset_panels(), run_time=0.9, rate_func=smooth)
        self.wait(0.8)   # was 0.3

        summary1 = Text(
            "These assumptions simplify the equation…",
            font_size=27, color=WHITE,
        ).move_to(UP * 0.40)
        summary2 = Text(
            "…while still describing many real-world flows",
            font_size=27, color=INCOMP_CLR,
        ).next_to(summary1, DOWN, buff=0.32)

        self.play(Write(summary1), run_time=1.8)   # was 1.2
        self.wait(1.2)   # new — pause between summary lines
        self.play(Write(summary2), run_time=1.8)   # was 1.2
        self.wait(3.0)   # was 1.5 — let both lines settle

        self.play(FadeOut(panels_vg, summary1, summary2), run_time=1.5)
        self.wait(0.6)