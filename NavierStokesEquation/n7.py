
from manim import *
import numpy as np


class Scene7_DynamicForceBalance(Scene):
    def construct(self):
        BG         = "#0A0A18"
        FLUID_MID  = "#2E6FC4"
        FLUID_DARK = "#112244"
        PRES_HIGH  = "#CC2200"
        PRES_LOW   = "#2255CC"
        VISC_CLR   = "#44DD88"
        EXT_CLR    = "#FFD84D"
        ACCEL_CLR  = "#FF8C42"
        EQ_CLR     = WHITE
        CYAN_GLOW  = "#00EEFF"

        self.camera.background_color = BG

        # ── Background ribbons ───────────────────────────────────────────────
        def ribbon(y, amp, phase, alpha=0.07):
            return always_redraw(lambda: ParametricFunction(
                lambda t: np.array([
                    t,
                    y + amp * np.sin(1.6 * t + phase + self.renderer.time * 0.55),
                    0,
                ]),
                t_range=[-8, 8, 0.07],
                color=FLUID_MID,
                stroke_width=1.3,
                stroke_opacity=alpha,
            ))

        bg_ribbons = VGroup(
            ribbon(-3.3, 0.18, 0.0),
            ribbon(-1.8, 0.22, 1.2),
            ribbon(-0.3, 0.16, 2.4),
            ribbon( 1.2, 0.20, 3.6),
            ribbon( 2.7, 0.17, 4.8),
        )
        self.add(bg_ribbons)

        # ── Helpers ──────────────────────────────────────────────────────────
        def glow_box(mob, color=CYAN_GLOW, buff=0.10, width=2.5):
            return SurroundingRectangle(
                mob, color=color, buff=buff,
                corner_radius=0.08, stroke_width=width,
            )

        def make_arrow(start, end, color, tip=0.18, sw=2.5):
            return Arrow(start, end, color=color, buff=0,
                         stroke_width=sw, tip_length=tip)

        EL_X   = -2.80
        EQ_X   =  2.90
        EL_CY  =  0.00
        NOTE_Y = -3.10   # bottom label row

        # ════════════════════════════════════════════════════════════════════
        # PART 1 — Fluid element intro  (0–10 s)
        # ════════════════════════════════════════════════════════════════════
        field_dots = VGroup()
        rng = np.random.default_rng(42)
        for _ in range(55):
            d = Dot(radius=0.055,
                    color=interpolate_color(ManimColor(FLUID_DARK),
                                           ManimColor(FLUID_MID),
                                           rng.random()))
            d.move_to([rng.uniform(-7, 7), rng.uniform(-3.5, 3.5), 0])
            field_dots.add(d)

        self.play(FadeIn(field_dots, lag_ratio=0.02), run_time=1.2)
        self.wait(0.4)

        EL_W, EL_H = 1.60, 1.00
        fluid_elem = Rectangle(
            width=EL_W, height=EL_H,
            fill_color=FLUID_MID, fill_opacity=0.65,
            stroke_color=CYAN_GLOW, stroke_width=2.5,
        ).move_to(RIGHT * EL_X + UP * EL_CY)

        elem_glow = always_redraw(lambda: glow_box(fluid_elem, buff=0.14, width=3.0))

        intro_txt = Text("Let's track a small piece of fluid",
                         font_size=28, color=WHITE
                         ).to_edge(UP, buff=0.45)

        self.play(Write(intro_txt), run_time=1.0)
        self.play(Create(fluid_elem), run_time=1.0)
        self.add(elem_glow)
        self.play(fluid_elem.animate.scale(1.12), run_time=0.45, rate_func=smooth)
        self.play(fluid_elem.animate.scale(1/1.12), run_time=0.45, rate_func=smooth)
        self.wait(1.0)
        self.play(FadeOut(intro_txt), run_time=0.5)

        # ════════════════════════════════════════════════════════════════════
        # PART 2 — Forces one-by-one  (10–30 s)
        # Each force group is fully faded before the next appears
        # ════════════════════════════════════════════════════════════════════

        # ── STEP 1: Pressure ─────────────────────────────────────────────────
        N_STRIPS = 18
        BAR_W, BAR_H = EL_W * 2.2, 0.32
        bar_top_y = EL_CY + EL_H / 2 + 0.70

        pres_strips = VGroup()
        sw = BAR_W / N_STRIPS
        for i in range(N_STRIPS):
            frac = i / (N_STRIPS - 1)
            c = interpolate_color(ManimColor(PRES_HIGH), ManimColor(PRES_LOW), frac)
            pres_strips.add(Rectangle(
                width=sw, height=BAR_H,
                fill_color=c, fill_opacity=0.90, stroke_width=0,
            ).move_to(RIGHT * EL_X + LEFT * (BAR_W / 2 - sw * (i + 0.5))
                      + UP * bar_top_y))

        pres_border = SurroundingRectangle(pres_strips, buff=0,
                                           stroke_color=WHITE, stroke_width=1.2)
        lbl_hi = Text("High P", font_size=13, color=PRES_HIGH
                      ).next_to(pres_strips, LEFT, buff=0.12)
        lbl_lo = Text("Low P",  font_size=13, color=PRES_LOW
                      ).next_to(pres_strips, RIGHT, buff=0.12)
        pres_bar = VGroup(pres_strips, pres_border, lbl_hi, lbl_lo)

        pres_arrows = VGroup(*[
            make_arrow(
                fluid_elem.get_left() + UP * (-0.28 + k * 0.28) + LEFT * 0.55,
                fluid_elem.get_left() + UP * (-0.28 + k * 0.28),
                color=PRES_HIGH, tip=0.15, sw=2.2,
            )
            for k in range(3)
        ])

        # ── FIX: single reusable note label, swapped between steps ──────────
        note_lbl = Text("Pressure pushes fluid",
                        font_size=22, color=PRES_HIGH, weight=BOLD
                        ).move_to(RIGHT * EL_X + UP * NOTE_Y)

        self.play(FadeIn(pres_bar), run_time=0.8)
        self.play(LaggedStart(*[GrowArrow(a) for a in pres_arrows],
                              lag_ratio=0.15, run_time=1.0))
        self.play(Write(note_lbl), run_time=0.7)
        self.wait(1.2)

        # Fade ENTIRE pressure group (bar + arrows + label) before viscosity
        self.play(FadeOut(VGroup(pres_bar, pres_arrows, note_lbl)), run_time=0.6)

        # ── STEP 2: Viscosity ────────────────────────────────────────────────
        VIS_LAYER_W = EL_W * 1.8
        layer_up = Rectangle(
            width=VIS_LAYER_W, height=0.30,
            fill_color="#1A5FAA", fill_opacity=0.60, stroke_width=0,
        ).next_to(fluid_elem, UP, buff=0)
        layer_dn = Rectangle(
            width=VIS_LAYER_W, height=0.30,
            fill_color=FLUID_DARK, fill_opacity=0.80, stroke_width=0,
        ).next_to(fluid_elem, DOWN, buff=0)

        def layer_arrows(n, length, mob, color):
            grp = VGroup()
            xs = np.linspace(mob.get_left()[0] + 0.25,
                             mob.get_right()[0] - 0.25, n)
            cy = mob.get_center()[1]
            for x in xs:
                grp.add(make_arrow(
                    [x, cy, 0], [x + length, cy, 0],
                    color=color, tip=0.12, sw=1.8,
                ))
            return grp

        arr_up = layer_arrows(3, 0.55, layer_up, VISC_CLR)
        arr_dn = layer_arrows(3, 0.22, layer_dn, VISC_CLR)
        lbl_up = Text("fast", font_size=13, color=VISC_CLR
                      ).next_to(layer_up, LEFT, buff=0.14)
        lbl_dn = Text("slow", font_size=13, color=VISC_CLR
                      ).next_to(layer_dn, LEFT, buff=0.14)

        smooth_top = make_arrow(
            fluid_elem.get_top() + UP * 0.0,
            fluid_elem.get_top() + DOWN * 0.28,
            color=VISC_CLR, tip=0.14, sw=2.0,
        )
        smooth_bot = make_arrow(
            fluid_elem.get_bottom() + DOWN * 0.0,
            fluid_elem.get_bottom() + UP * 0.28,
            color=VISC_CLR, tip=0.14, sw=2.0,
        )

        visc_grp_vis = VGroup(layer_up, layer_dn, arr_up, arr_dn,
                              lbl_up, lbl_dn, smooth_top, smooth_bot)

        note_lbl = Text("Viscosity resists motion",
                        font_size=22, color=VISC_CLR, weight=BOLD
                        ).move_to(RIGHT * EL_X + UP * NOTE_Y)

        self.play(FadeIn(layer_up, layer_dn), run_time=0.7)
        self.play(LaggedStart(*[GrowArrow(a)
                                for a in list(arr_up) + list(arr_dn)],
                              lag_ratio=0.08, run_time=0.9))
        self.play(FadeIn(lbl_up, lbl_dn), run_time=0.4)
        self.play(GrowArrow(smooth_top), GrowArrow(smooth_bot), run_time=0.7)
        self.play(Write(note_lbl), run_time=0.7)
        self.wait(1.2)

        # Fade ENTIRE viscosity group before external force
        self.play(FadeOut(VGroup(visc_grp_vis, note_lbl)), run_time=0.6)

        # ── STEP 3: External force ───────────────────────────────────────────
        ext_arrow = make_arrow(
            fluid_elem.get_center() + UP * 0.10,
            fluid_elem.get_center() + DOWN * 0.55,
            color=EXT_CLR, tip=0.18, sw=3.0,
        )
        note_lbl = Text("External forces act on fluid",
                        font_size=22, color=EXT_CLR, weight=BOLD
                        ).move_to(RIGHT * EL_X + UP * NOTE_Y)

        self.play(GrowArrow(ext_arrow), run_time=0.8)
        self.play(Write(note_lbl), run_time=0.7)
        self.wait(1.2)

        # Fade external force before net force
        self.play(FadeOut(VGroup(ext_arrow, note_lbl)), run_time=0.5)

        # ════════════════════════════════════════════════════════════════════
        # PART 3 — Net force & acceleration  (30–40 s)
        # ════════════════════════════════════════════════════════════════════
        net_arrow = make_arrow(
            fluid_elem.get_center(),
            fluid_elem.get_center() + RIGHT * 0.80 + DOWN * 0.18,
            color=ACCEL_CLR, tip=0.20, sw=3.5,
        )
        net_lbl = VGroup(
            Text("Net Force", font_size=16, color=ACCEL_CLR),
            Text("→ Acceleration", font_size=16, color=WHITE),
        ).arrange(RIGHT, buff=0.12).next_to(net_arrow.get_end(), RIGHT, buff=0.12)

        accel_note = Text("Acceleration = result of all forces",
                          font_size=23, color=WHITE, weight=BOLD
                          ).move_to(RIGHT * EL_X + UP * NOTE_Y)

        self.play(GrowArrow(net_arrow), FadeIn(net_lbl), run_time=0.9)
        self.play(
            fluid_elem.animate.stretch(1.25, dim=0).shift(RIGHT * 0.12),
            run_time=0.9, rate_func=smooth,
        )
        self.play(Write(accel_note), run_time=0.8)
        self.wait(1.2)

        # ════════════════════════════════════════════════════════════════════
        # PART 4 — Equation + highlighted terms  (40–55 s)
        # ════════════════════════════════════════════════════════════════════
        # Clear all remaining force visuals cleanly
        self.play(FadeOut(VGroup(net_arrow, net_lbl, accel_note)), run_time=0.8)
        self.play(
            fluid_elem.animate.stretch(1/1.25, dim=0).shift(LEFT * 0.12),
            run_time=0.5,
        )

        ns = MathTex(
            r"\rho",
            r"\!\left(\frac{\partial \mathbf{v}}{\partial t}"
            r"+ \mathbf{v}\cdot\nabla\mathbf{v}\right)",
            r"=",
            r"-\nabla p",
            r"+\,\mu\nabla^2\mathbf{v}",
            r"+\,\mathbf{f}",
            font_size=34, color=EQ_CLR,
        ).move_to(RIGHT * EQ_X + UP * 1.80)

        eq_title = Text("Navier–Stokes Equation",
                        font_size=20, color=CYAN_GLOW
                        ).next_to(ns, UP, buff=0.22)

        self.play(FadeIn(eq_title), Write(ns), run_time=1.4)
        self.wait(0.4)

        SIDE_X   = RIGHT * EQ_X
        BELOW_EQ = UP * 0.80

        def highlight_term(idx, color, label_str, vis_mobs, label_pos):
            box = glow_box(ns[idx], color=color, buff=0.07, width=2.8)
            side_lbl = Text(label_str, font_size=19, color=color
                            ).move_to(label_pos)
            anims_in  = [Create(box), FadeIn(side_lbl)]
            anims_in += [FadeIn(m) for m in vis_mobs]
            anims_out = [FadeOut(box), FadeOut(side_lbl)]
            anims_out += [FadeOut(m) for m in vis_mobs]
            return anims_in, anims_out

        # −∇p → pressure arrows
        pres_mini = VGroup(*[
            make_arrow(
                fluid_elem.get_left() + UP * (-0.22 + k * 0.22) + LEFT * 0.50,
                fluid_elem.get_left() + UP * (-0.22 + k * 0.22),
                color=PRES_HIGH, tip=0.13, sw=2.0,
            )
            for k in range(3)
        ])
        ain_p, aout_p = highlight_term(
            3, PRES_HIGH, "Pressure gradient → pushes fluid",
            [pres_mini], SIDE_X + BELOW_EQ,
        )
        self.play(*ain_p, run_time=0.8)
        self.wait(1.2)
        self.play(*aout_p, run_time=0.6)

        # μ∇²v → viscosity
        sm_top = make_arrow(
            fluid_elem.get_top() + UP * 0.05,
            fluid_elem.get_top() + DOWN * 0.32,
            color=VISC_CLR, tip=0.13, sw=2.0,
        )
        sm_bot = make_arrow(
            fluid_elem.get_bottom() + DOWN * 0.05,
            fluid_elem.get_bottom() + UP * 0.32,
            color=VISC_CLR, tip=0.13, sw=2.0,
        )
        ain_v, aout_v = highlight_term(
            4, VISC_CLR, "Viscosity → smooths velocity",
            [sm_top, sm_bot], SIDE_X + BELOW_EQ,
        )
        self.play(*ain_v, run_time=0.8)
        self.wait(1.2)
        self.play(*aout_v, run_time=0.6)

        # +f → external force
        ext_mini = make_arrow(
            fluid_elem.get_center() + UP * 0.15,
            fluid_elem.get_center() + DOWN * 0.50,
            color=EXT_CLR, tip=0.16, sw=2.8,
        )
        ain_f, aout_f = highlight_term(
            5, EXT_CLR, "External forces (gravity, etc.)",
            [ext_mini], SIDE_X + BELOW_EQ,
        )
        self.play(*ain_f, run_time=0.8)
        self.wait(1.2)
        self.play(*aout_f, run_time=0.6)

        # LHS → acceleration
        acc_mini = make_arrow(
            fluid_elem.get_center(),
            fluid_elem.get_center() + RIGHT * 0.70 + DOWN * 0.15,
            color=ACCEL_CLR, tip=0.17, sw=3.0,
        )
        ain_a, aout_a = highlight_term(
            1, ACCEL_CLR, "→ Fluid acceleration (motion)",
            [acc_mini], SIDE_X + BELOW_EQ,
        )
        self.play(*ain_a, run_time=0.8)
        self.wait(1.4)
        self.play(*aout_a, run_time=0.6)

        self.wait(0.4)

        # ════════════════════════════════════════════════════════════════════
        # PART 5 — Real flow channel  (55–70 s)
        # ════════════════════════════════════════════════════════════════════
        self.play(
            FadeOut(ns, eq_title, fluid_elem, elem_glow),
            run_time=0.9,
        )

        CHAN_Y_TOP =  1.40
        CHAN_Y_BOT = -1.40
        wall_top = Line([-6.5, CHAN_Y_TOP, 0], [6.5, CHAN_Y_TOP, 0],
                        color="#334466", stroke_width=3.0)
        wall_bot = Line([-6.5, CHAN_Y_BOT, 0], [6.5, CHAN_Y_BOT, 0],
                        color="#334466", stroke_width=3.0)
        wall_lbl_t = Text("Channel wall", font_size=13, color="#334466"
                          ).next_to(wall_top, RIGHT, buff=0.15)
        wall_lbl_b = Text("Channel wall", font_size=13, color="#334466"
                          ).next_to(wall_bot, RIGHT, buff=0.15)

        self.play(
            Create(wall_top), Create(wall_bot),
            FadeIn(wall_lbl_t, wall_lbl_b),
            run_time=0.9,
        )

        CHAN_H = CHAN_Y_TOP - CHAN_Y_BOT
        X_STATIONS = np.linspace(-5.5, 5.5, 8)
        Y_SAMPLES  = np.linspace(CHAN_Y_BOT + 0.15, CHAN_Y_TOP - 0.15, 7)

        flow_arrows = VGroup()
        for x in X_STATIONS:
            for y in Y_SAMPLES:
                norm_y = (y - (CHAN_Y_TOP + CHAN_Y_BOT) / 2) / (CHAN_H / 2)
                speed  = 1.0 - norm_y ** 2
                length = 0.55 * speed
                if length < 0.05:
                    continue
                c = interpolate_color(ManimColor(FLUID_DARK),
                                      ManimColor(FLUID_MID), speed)
                flow_arrows.add(make_arrow(
                    [x, y, 0], [x + length, y, 0],
                    color=c, tip=0.10, sw=1.5,
                ))

        self.play(
            LaggedStart(*[GrowArrow(a) for a in flow_arrows],
                        lag_ratio=0.02, run_time=2.0),
        )

        chan_note = Text("Every point in the fluid follows this balance",
                         font_size=24, color=WHITE, weight=BOLD
                         ).to_edge(DOWN, buff=0.45)
        self.play(Write(chan_note), run_time=1.1)
        self.wait(1.8)

        # ════════════════════════════════════════════════════════════════════
        # PART 6 — Final insight  (70–75 s)
        # ════════════════════════════════════════════════════════════════════
        channel_grp = VGroup(wall_top, wall_bot, wall_lbl_t, wall_lbl_b,
                             flow_arrows, chan_note)
        self.play(FadeOut(channel_grp), run_time=0.9)

        final_line1 = Text(
            "The equation is not static —",
            font_size=32, color=WHITE,
        ).move_to(UP * 0.35)
        final_line2 = Text(
            "it continuously governs motion",
            font_size=32, color=CYAN_GLOW, weight=BOLD,
        ).next_to(final_line1, DOWN, buff=0.28)

        self.play(Write(final_line1), run_time=1.1)
        self.play(Write(final_line2), run_time=1.1)
        self.wait(2.0)

        self.play(FadeOut(final_line1, final_line2), run_time=1.0)
        self.wait(0.3)