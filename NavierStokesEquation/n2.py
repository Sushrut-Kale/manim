from manim import *
import numpy as np


# ═══════════════════════════════════════════════════════════
#  GLOBAL STYLE CONSTANTS
# ═══════════════════════════════════════════════════════════
BG_COLOR    = "#06070F"      # deep cinematic dark
FLUID_BLUE  = "#1E90FF"      # main stream lines
FLUID_DARK  = "#0A1E4E"      # dark blue fill
ARROW_COLOR = "#A8D8FF"      # velocity arrows
GRID_COLOR  = "#1A2A3A"      # faint grid lines
CYAN_GLOW   = "#00E5FF"      # highlight / accent
TEXT_WHITE  = WHITE
OBJ_COLOR   = "#D0E8FF"      # obstacle / object outlines
SLOW_COLOR  = "#1040A0"      # deep blue = slow
FAST_COLOR  = "#00E5FF"      # cyan = fast


# ═══════════════════════════════════════════════════════════
#  VELOCITY FIELD FUNCTIONS
# ═══════════════════════════════════════════════════════════

def base_velocity(x, y):
    """
    Simple rightward shear flow with a gentle wave pattern.
    Mimics a river or gentle wind field.
    """
    vx = 1.0 + 0.28 * np.sin(0.7 * y)
    vy = 0.12 * np.sin(1.1 * x + 0.4 * y)
    return np.array([vx, vy, 0])


def flow_around_circle(x, y, cx=0.0, cy=0.0, r=0.85):
    """
    Potential-flow (irrotational) solution around a circular cylinder.
    Based on the conformal mapping / dipole superposition formula.
    Gives physically accurate streamlines around a circular obstacle.
    """
    dx = x - cx
    dy = y - cy
    rr = dx**2 + dy**2 + 1e-6      # avoid divide-by-zero

    # Uniform flow + dipole correction for the circle
    vx = 1.0 * (1 - r**2 * (dx**2 - dy**2) / rr**2)
    vy = -1.0 * (-r**2 * 2 * dx * dy / rr**2)
    return np.array([vx, vy, 0])


def speed_color(speed, vmin=0.3, vmax=2.2):
    """Return interpolated color: SLOW_COLOR (blue) → FAST_COLOR (cyan)."""
    t = np.clip((speed - vmin) / (vmax - vmin), 0, 1)
    return interpolate_color(ManimColor(SLOW_COLOR), ManimColor(FAST_COLOR), t)


# ═══════════════════════════════════════════════════════════
#  HELPER: Build velocity arrow grid
# ═══════════════════════════════════════════════════════════

def make_arrow_grid(vel_func, x_range, y_range,
                    scale=0.32, colored=False, opacity=0.75):
    """
    Build a VGroup of Arrow objects sampling the velocity field
    on a regular (x_range × y_range) grid.

    Args:
        vel_func : callable (x, y) → np.array([vx, vy, 0])
        x_range  : iterable of x positions
        y_range  : iterable of y positions
        scale    : arrow length multiplier
        colored  : if True, color by speed; else use ARROW_COLOR
        opacity  : overall arrow opacity
    """
    arrows = VGroup()
    for x in x_range:
        for y in y_range:
            v   = vel_func(x, y)
            spd = np.linalg.norm(v[:2])
            if spd < 1e-4:
                continue
            direction = v / spd
            length    = np.clip(spd * scale, 0.06, 0.55)
            start     = np.array([x, y, 0])
            end       = start + direction * length
            col       = speed_color(spd) if colored else ARROW_COLOR
            arr = Arrow(
                start, end,
                buff         = 0,
                stroke_width = 1.8,
                tip_length   = 0.10,
                color        = col,
            )
            arr.set_opacity(opacity)
            arrows.add(arr)
    return arrows


# ═══════════════════════════════════════════════════════════
#  HELPER: Build streamlines by numerical integration
# ═══════════════════════════════════════════════════════════

def make_streamlines(vel_func, seeds,
                     steps=130, dt=0.065,
                     stroke_w=1.4, opacity=0.5, colored=False):
    """
    Integrate streamlines forward from seed points using Euler steps.
    Returns a VGroup of VMobject paths.

    Args:
        vel_func : callable (x, y) → np.array([vx, vy, 0])
        seeds    : list of (sx, sy) starting points
        steps    : max integration steps per streamline
        dt       : step size (smaller = smoother curve)
        stroke_w : line stroke width
        opacity  : line opacity
        colored  : if True, color by midpoint speed
    """
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
            # Stop if we leave the visible canvas
            if abs(x) > 7.8 or abs(y) > 4.8:
                break

        if len(pts) < 3:
            continue

        path = VMobject()
        path.set_points_smoothly([np.array(p) for p in pts])

        if colored and len(pts) > 2:
            mid = pts[len(pts) // 2]
            mid_v = vel_func(mid[0], mid[1])
            col   = speed_color(np.linalg.norm(mid_v[:2]))
        else:
            col = FLUID_BLUE

        path.set_stroke(col, width=stroke_w, opacity=opacity)
        lines.add(path)
    return lines


# ═══════════════════════════════════════════════════════════
#  HELPER: Airfoil shape (NACA-style)
# ═══════════════════════════════════════════════════════════

def make_airfoil(pos, chord=2.6, thickness=0.44):
    """
    Draw a NACA 0012-like symmetric airfoil as a closed VMobject.

    Args:
        pos       : np.array centre position [x, y, 0]
        chord     : horizontal length of the wing
        thickness : max thickness scaling factor
    """
    n  = 60
    xc = np.linspace(0, 1, n)

    # NACA 00XX thickness distribution
    yt = thickness * (
          0.2969 * np.sqrt(xc)
        - 0.1260 * xc
        - 0.3516 * xc**2
        + 0.2843 * xc**3
        - 0.1015 * xc**4
    )

    # Upper and lower surface point arrays
    upper = np.column_stack([xc * chord - chord/2,  yt * chord, np.zeros(n)])
    lower = np.column_stack([xc[::-1] * chord - chord/2, -yt[::-1] * chord, np.zeros(n)])

    pts = np.vstack([upper, lower])
    pts[:, :2] += pos[:2]

    shape = VMobject()
    shape.set_points_smoothly([np.array(p) for p in pts])
    shape.close_path()
    shape.set_stroke(OBJ_COLOR, width=2.0)
    shape.set_fill(FLUID_DARK, opacity=0.9)
    return shape


# ═══════════════════════════════════════════════════════════
#  MAIN SCENE
# ═══════════════════════════════════════════════════════════

class CombinedFlowScene(MovingCameraScene):
    """
    Combined Scene 2 + 3:
        Scene 2 — 'What is Flow?'        (Parts 1–5)
        Scene 3 — 'Can We Control It?'   (Parts 6–10)

    Runs as a single continuous, cinematic animation.
    Designed to be accessible to complete beginners — no jargon, no jumps.
    """

    def construct(self):
        self.camera.background_color = BG_COLOR
        # Remember default camera width for zoom-out restoration
        self._base_width = self.camera.frame.width

        # ── SCENE 2 ──────────────────────────────────────────
        self._part1_gentle_intro()        #  0– 8 s  fluid intro
        self._part2_grid_overlay()        #  8–15 s  grid appears
        self._part3_velocity_arrows()     # 15–25 s  arrows appear
        self._part4_local_zoom()          # 25–32 s  zoom into detail
        self._part5_equation()            # 32–42 s  v(x,y,z,t)

        # ── SCENE 3 ──────────────────────────────────────────
        self._part6_big_question()        # 42–48 s  "Can we control flow?"
        self._part7_obstacle()            # 48–58 s  obstacle bends flow
        self._part8_applications()        # 58–72 s  wing / pipe / vessel
        self._part9_speed_colors()        # 72–80 s  color-coded speed
        self._part10_bridge_to_math()     # 80–88 s  equations await

    # ╔══════════════════════════════════════════════════════╗
    # ║  SCENE 2 — "What is Flow?"                          ║
    # ╚══════════════════════════════════════════════════════╝

    # ── Part 1: Gentle fluid intro (0–8 s) ──────────────────
    def _part1_gentle_intro(self):
        """
        Open with poetic context — rivers, air, blood.
        Then reveal the flowing streamlines to show 'flow' visually.
        """
        # Opening title card
        intro_title = Text(
            "What is Flow?",
            font_size=52, color=TEXT_WHITE, weight=BOLD,
        )
        intro_title.set_stroke(BLACK, width=4, background=True)

        intro_sub = Text(
            "Rivers flow. Air moves. Blood circulates.",
            font_size=24, color=ARROW_COLOR, slant=ITALIC,
        )
        intro_sub.next_to(intro_title, DOWN, buff=0.4)
        intro_sub.set_stroke(BLACK, width=3, background=True)

        self.play(FadeIn(intro_title, shift=UP * 0.2), run_time=1.5)
        self.play(FadeIn(intro_sub,   shift=UP * 0.15), run_time=1.0)
        self.wait(1.2)

        # Fade title out and bring in streamlines
        self.play(FadeOut(intro_title), FadeOut(intro_sub), run_time=1.0)

        # Create background streamlines (the "fluid")
        seeds = [(-7, y) for y in np.linspace(-4.0, 4.0, 24)]
        self._streams = make_streamlines(
            base_velocity, seeds,
            steps=150, dt=0.065, stroke_w=1.5, opacity=0.48,
        )
        self.play(
            Create(self._streams, lag_ratio=0.025),
            run_time=2.5, rate_func=smooth,
        )

        # Small subtitle at bottom
        hint = Text(
            "Motion defined at every point in space.",
            font_size=20, color=ARROW_COLOR, slant=ITALIC,
        ).to_edge(DOWN, buff=0.45)
        hint.set_stroke(BLACK, width=3, background=True)
        self.play(FadeIn(hint, shift=UP * 0.1), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(hint), run_time=0.5)

    # ── Part 2: Grid overlay (8–15 s) ──────────────────────
    def _part2_grid_overlay(self):
        """
        Fade in a faint measurement grid over the flowing fluid.
        This shows that space itself can be structured and measured.
        """
        self._grid = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": GRID_COLOR,
                "stroke_width": 0.8,
                "stroke_opacity": 0.55,
            },
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=0,
        )
        self._grid.set_opacity(0)

        # Grid appears gently while flow continues
        grid_label = Text(
            "Space can be measured at every point.",
            font_size=22, color=ARROW_COLOR, slant=ITALIC,
        ).to_edge(DOWN, buff=0.45)
        grid_label.set_stroke(BLACK, width=3, background=True)

        self.add(self._grid)
        self.play(
            self._grid.animate.set_opacity(1),
            run_time=2.0, rate_func=smooth,
        )
        self.play(FadeIn(grid_label, shift=UP * 0.1), run_time=0.8)
        self.wait(2.5)
        self.play(FadeOut(grid_label), run_time=0.6)

    # ── Part 3: Velocity arrows appear (15–25 s) ────────────
    def _part3_velocity_arrows(self):
        """
        Place velocity arrows at grid intersections.
        Arrows appear progressively (lag_ratio) to feel alive.
        Arrows point in the direction of flow and vary in length by speed.
        """
        arrow_label = Text(
            "At each point: a direction and a speed.",
            font_size=22, color=ARROW_COLOR, slant=ITALIC,
        ).to_edge(DOWN, buff=0.45)
        arrow_label.set_stroke(BLACK, width=3, background=True)

        xs = np.linspace(-6.0, 6.0, 11)    # 11 columns
        ys = np.linspace(-3.5, 3.5,  8)    # 8 rows
        self._arrows = make_arrow_grid(base_velocity, xs, ys,
                                       scale=0.30, opacity=0.72)

        # Arrows fade in staggered (lag_ratio gives wave-like appearance)
        self.play(
            FadeIn(self._arrows, lag_ratio=0.04),
            run_time=3.0, rate_func=smooth,
        )
        self.play(FadeIn(arrow_label, shift=UP * 0.1), run_time=0.7)
        self.wait(2.5)
        self.play(FadeOut(arrow_label), run_time=0.6)

    # ── Part 4: Zoom in on local region (25–32 s) ───────────
    def _part4_local_zoom(self):
        """
        Camera zooms into a small region so the viewer can see
        that each individual point has its OWN unique arrow.
        Emphasises local variation in velocity.
        """
        zoom_label = Text(
            "Each point has its own unique velocity.",
            font_size=26, color=TEXT_WHITE, slant=ITALIC,
        ).to_edge(DOWN, buff=0.45)
        zoom_label.set_stroke(BLACK, width=3, background=True)

        # Camera zooms into left-centre region
        self.play(
            self.camera.frame.animate
                .scale(0.50)
                .move_to([-1.2, 0.5, 0]),
            run_time=2.2, rate_func=smooth,
        )

        # Denser local arrows in zoomed region
        xs_loc = np.linspace(-4.0, 1.5, 14)
        ys_loc = np.linspace(-2.0, 2.5, 11)
        local_arrows = make_arrow_grid(base_velocity, xs_loc, ys_loc,
                                       scale=0.20, opacity=0.80)
        self.play(
            FadeIn(local_arrows, lag_ratio=0.01),
            run_time=1.2, rate_func=smooth,
        )
        self.play(FadeIn(zoom_label, shift=UP * 0.1), run_time=0.7)
        self.wait(2.0)

        # Zoom back out to full view
        self.play(
            self.camera.frame.animate
                .set_width(self._base_width)
                .move_to(ORIGIN),
            FadeOut(zoom_label),
            FadeOut(local_arrows),
            run_time=2.0, rate_func=smooth,
        )

    # ── Part 5: Equation reveal (32–42 s) ───────────────────
    def _part5_equation(self):
        """
        Introduce the mathematical notation v(x, y, z, t).
        Each symbol appears and is immediately labelled in plain English.
        A glow box highlights the equation as the central idea.
        """
        # Glow box behind equation
        eq_bg = RoundedRectangle(
            width=4.2, height=1.1,
            corner_radius=0.2,
            color=CYAN_GLOW, stroke_width=1.2,
        )
        eq_bg.set_fill(BLACK, opacity=0.55)
        eq_bg.to_corner(UL, buff=0.4)

        # Main equation
        eq = MathTex(
            r"\vec{v}",
            r"(x, y, z,",
            r"t)",
            color=WHITE,
            font_size=46,
        )
        eq.to_corner(UL, buff=0.55)
        eq_bg.move_to(eq.get_center()).set_width(eq.width + 0.6)

        self.play(FadeIn(eq_bg), Write(eq), run_time=1.5)

        # Labels for each part of the equation
        term_data = [
            (0, r"\vec{v}",     "velocity — speed + direction",  CYAN_GLOW),
            (1, r"x, y, z",     "position in 3D space",          ARROW_COLOR),
            (2, r"t",           "time — flow changes moment to moment", "#FFA040"),
        ]

        label_group = VGroup()
        for idx, sym, meaning, col in term_data:
            # Highlight the term in the equation
            eq[idx].set_color(col)

            lbl = Text(
                f"  {meaning}",
                font_size=17, color=col,
            )
            lbl.next_to(eq, DOWN, buff=0.30 + idx * 0.40).align_to(eq, LEFT)
            lbl.set_stroke(BLACK, width=2, background=True)

            self.play(
                FadeIn(lbl, shift=RIGHT * 0.1),
                run_time=0.65,
            )
            label_group.add(lbl)
            self.wait(0.3)

        # Bottom summary line
        summary = Text(
            "Flow is a field — every point has its own motion.",
            font_size=21, color=TEXT_WHITE, slant=ITALIC,
        ).to_edge(DOWN, buff=0.45)
        summary.set_stroke(BLACK, width=3, background=True)
        self.play(FadeIn(summary, shift=UP * 0.1), run_time=0.8)
        self.wait(2.5)
        self.play(FadeOut(summary), run_time=0.6)

        # Keep eq visible but dim it for the scene transition
        self._eq          = eq
        self._eq_bg       = eq_bg
        self._label_group = label_group

    # ╔══════════════════════════════════════════════════════╗
    # ║  SCENE 3 — "Can We Control It?"                     ║
    # ╚══════════════════════════════════════════════════════╝

    # ── Part 6: Big question (42–48 s) ──────────────────────
    def _part6_big_question(self):
        """
        Bridge Scene 2 → Scene 3.
        Dim the equation UI and ask the big question in the centre.
        A slight camera zoom in creates dramatic tension.
        """
        # Dim scene-2 elements so they don't compete
        self.play(
            self._eq.animate.set_opacity(0.20),
            self._eq_bg.animate.set_opacity(0.12),
            self._label_group.animate.set_opacity(0.12),
            run_time=0.8,
        )

        question = Text(
            "Can we control flow?",
            font_size=52, color=CYAN_GLOW, weight=BOLD,
        )
        question.set_stroke(BLACK, width=5, background=True)

        sub_q = Text(
            "What happens when we change conditions?",
            font_size=24, color=ARROW_COLOR, slant=ITALIC,
        )
        sub_q.next_to(question, DOWN, buff=0.45)
        sub_q.set_stroke(BLACK, width=3, background=True)

        # Gentle zoom-in during question reveal
        self.play(
            self.camera.frame.animate.scale(0.92),
            FadeIn(question, scale=1.08),
            run_time=1.8, rate_func=smooth,
        )
        self.play(FadeIn(sub_q, shift=UP * 0.1), run_time=0.8)
        self.wait(2.5)

        self.play(
            FadeOut(question),
            FadeOut(sub_q),
            self.camera.frame.animate.set_width(self._base_width).move_to(ORIGIN),
            run_time=1.2, rate_func=smooth,
        )

        self._obstacle = None  # will be set in Part 7

    # ── Part 7: Obstacle bends flow (48–58 s) ───────────────
    def _part7_obstacle(self):
        """
        Place a circular obstacle in the flow path.
        Streamlines update to show flow bending around the object.
        This visually answers: 'Yes — conditions change flow.'
        """
        # Fade out scene-2 overlays
        self.play(
            FadeOut(self._arrows),
            self._eq.animate.set_opacity(0),
            self._eq_bg.animate.set_opacity(0),
            self._label_group.animate.set_opacity(0),
            run_time=0.8,
        )

        # Informational subtitle
        obs_label = Text(
            "An obstacle changes the path of every nearby point.",
            font_size=22, color=TEXT_WHITE, slant=ITALIC,
        ).to_edge(DOWN, buff=0.45)
        obs_label.set_stroke(BLACK, width=3, background=True)
        self.play(FadeIn(obs_label, shift=UP * 0.1), run_time=0.7)

        # Draw the circular obstacle
        obstacle = Circle(radius=0.88)
        obstacle.set_stroke(OBJ_COLOR, width=2.5)
        obstacle.set_fill(BG_COLOR, opacity=1.0)
        obstacle.move_to(ORIGIN)

        self.play(Create(obstacle), run_time=1.0)
        self._obstacle = obstacle

        # Replace old streamlines with potential-flow solution
        seeds_obs = [(-7, y) for y in np.linspace(-4.0, 4.0, 30)]
        obs_streams = make_streamlines(
            flow_around_circle, seeds_obs,
            steps=170, dt=0.058, stroke_w=1.5, opacity=0.55,
        )
        self.play(
            FadeOut(self._streams),
            run_time=0.7,
        )
        self.play(
            Create(obs_streams, lag_ratio=0.022),
            run_time=2.8, rate_func=smooth,
        )

        # Add arrows around the obstacle (colored by speed)
        xs = np.linspace(-6, 6, 11)
        ys = np.linspace(-3.5, 3.5, 8)
        obs_arrows = make_arrow_grid(
            flow_around_circle, xs, ys,
            scale=0.30, colored=True, opacity=0.72,
        )
        self.play(FadeIn(obs_arrows, lag_ratio=0.025), run_time=1.5)
        self.wait(1.5)

        self.play(FadeOut(obs_label), run_time=0.5)
        self._streams      = obs_streams
        self._arrows       = obs_arrows

    # ── Part 8: Three real-world applications (58–72 s) ──────
    def _part8_applications(self):
        """
        Fade the abstract field into three concrete mini-panels:
        1. Aircraft wing  — aerodynamic lift
        2. Pipe flow      — Poiseuille parabolic profile
        3. Blood vessel   — biological pulsatile flow

        Each panel is minimal and stylised, consistent color theme.
        """
        # Clear the current field visual
        self.play(
            FadeOut(self._streams),
            FadeOut(self._arrows),
            FadeOut(self._obstacle),
            FadeOut(self._grid),
            run_time=1.0,
        )

        app_title = Text(
            "Flow shapes the world around us.",
            font_size=30, color=CYAN_GLOW, weight=BOLD,
        ).to_edge(UP, buff=0.35)
        app_title.set_stroke(BLACK, width=3, background=True)
        self.play(FadeIn(app_title), run_time=0.7)

        # Build the three panels
        panel_data = [
            (0, LEFT  * 4.4, "Aircraft Wing"),
            (1, ORIGIN,       "Pipe Flow"),
            (2, RIGHT * 4.4, "Blood Vessel"),
        ]
        panels = VGroup()
        for idx, pos, title in panel_data:
            p = self._build_app_panel(idx, pos, w=3.9, h=2.7, title=title)
            panels.add(p)

        panels.scale(0.90)

        self.play(
            LaggedStart(
                *[FadeIn(p, shift=UP * 0.15) for p in panels],
                lag_ratio=0.30,
            ),
            run_time=2.8, rate_func=smooth,
        )

        caption = Text(
            "By changing conditions, we change flow behaviour.",
            font_size=21, color=TEXT_WHITE, slant=ITALIC,
        ).to_edge(DOWN, buff=0.45)
        caption.set_stroke(BLACK, width=3, background=True)
        self.play(FadeIn(caption, shift=UP * 0.1), run_time=0.8)
        self.wait(4.0)

        self.play(
            FadeOut(panels),
            FadeOut(app_title),
            FadeOut(caption),
            run_time=1.2,
        )

    def _build_app_panel(self, idx, pos, w, h, title):
        """Build a single application mini-panel at position `pos`."""
        panel = VGroup()
        cx, cy = pos[0], pos[1]

        # Panel border
        border = RoundedRectangle(
            width=w, height=h, corner_radius=0.22,
            color=ARROW_COLOR, stroke_width=1.2,
        )
        border.set_fill(BG_COLOR, opacity=0.85)
        border.move_to(pos)
        panel.add(border)

        # Title label
        lbl = Text(title, font_size=18, color=TEXT_WHITE, weight=BOLD)
        lbl.move_to(pos + UP * (h / 2 - 0.28))
        panel.add(lbl)

        inner_y = cy - 0.08   # centre of inner drawing area

        if idx == 0:
            # ─── Aircraft Wing ───────────────────────────────
            wing = make_airfoil(
                pos=np.array([cx, inner_y - 0.05, 0]),
                chord=2.4, thickness=0.42,
            )
            panel.add(wing)
            # Streamlines curving over and under the wing
            for dy in np.linspace(-0.80, 0.80, 9):
                sy = inner_y + dy
                pts = []
                x, y = cx - 2.0, sy
                for _ in range(80):
                    dx_ = x - cx
                    dy_ = y - (inner_y - 0.05)
                    rr  = dx_**2 + (dy_ * 2.1)**2 + 0.04
                    vx_ = 1.0 + 0.4 * (0.38**2) * (dx_**2 - (dy_*2.1)**2) / rr**2
                    vy_ = -0.4 * 0.3 * dx_ * dy_ / (rr + 0.01)
                    spd = max(np.sqrt(vx_**2 + vy_**2), 0.01)
                    x  += vx_ / spd * 0.04
                    y  += vy_ / spd * 0.04
                    pts.append([x, y, 0])
                    if x > cx + 2.1:
                        break
                if len(pts) < 4:
                    continue
                sl = VMobject()
                sl.set_points_smoothly([np.array(p) for p in pts])
                t = (dy + 0.80) / 1.60
                col = interpolate_color(ManimColor(FLUID_DARK), ManimColor(CYAN_GLOW), t)
                sl.set_stroke(col, width=1.0, opacity=0.70)
                panel.add(sl)

        elif idx == 1:
            # ─── Pipe Flow ───────────────────────────────────
            pr = 0.70        # pipe radius
            top_wall = Line([cx-1.9, inner_y+pr, 0], [cx+1.9, inner_y+pr, 0],
                            color=OBJ_COLOR, stroke_width=2.0)
            bot_wall = Line([cx-1.9, inner_y-pr, 0], [cx+1.9, inner_y-pr, 0],
                            color=OBJ_COLOR, stroke_width=2.0)
            panel.add(top_wall, bot_wall)

            # Parabolic velocity profile arrows (Poiseuille flow)
            for r in np.linspace(-0.62, 0.62, 8):
                vx = max(0.04, 1.0 - (r / pr)**2)   # parabola
                y_pos = inner_y + r
                col   = speed_color(vx, vmin=0.0, vmax=1.05)
                arr = Arrow(
                    [cx - 0.15, y_pos, 0],
                    [cx - 0.15 + vx * 0.55, y_pos, 0],
                    buff=0, stroke_width=1.5,
                    tip_length=0.09, color=col,
                )
                arr.set_opacity(0.82)
                panel.add(arr)

        else:
            # ─── Blood Vessel ─────────────────────────────────
            ves_r = 0.58
            vessel = Ellipse(
                width=3.8, height=ves_r * 2,
                color=OBJ_COLOR, stroke_width=2.0,
            )
            vessel.set_fill("#1A0010", opacity=0.65)
            vessel.move_to([cx, inner_y, 0])
            panel.add(vessel)

            # Blood-cell dots scattered inside vessel
            rng = np.random.default_rng(42)    # fixed seed for reproducibility
            for _ in range(20):
                px  = cx + rng.uniform(-1.5, 1.5)
                r   = rng.uniform(0, ves_r * 0.85)
                ang = rng.uniform(0, 2 * np.pi)
                py  = inner_y + r * np.sin(ang) * 0.38
                spd = max(0.05, 1.0 - (r / ves_r)**2)
                col = speed_color(spd, vmin=0.0, vmax=1.05)
                dot = Dot([px, py, 0], radius=0.055, color=col)
                dot.set_opacity(0.88)
                panel.add(dot)

            # Flow arrows through the vessel centre
            for xp in np.linspace(cx - 1.1, cx + 1.0, 4):
                arr = Arrow(
                    [xp, inner_y, 0], [xp + 0.38, inner_y, 0],
                    buff=0, stroke_width=1.4,
                    tip_length=0.10, color=FLUID_BLUE,
                )
                arr.set_opacity(0.78)
                panel.add(arr)

        return panel

    # ── Part 9: Color-coded speed mapping (72–80 s) ──────────
    def _part9_speed_colors(self):
        """
        Bring back the abstract field with color-coded arrows.
        This shows the viewer how speed varies spatially —
        fast (cyan) near the obstacle, slow (deep blue) far from it.
        Includes a simple legend.
        """
        # Restore grid
        grid2 = NumberPlane(
            x_range=[-8, 8, 1], y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": GRID_COLOR,
                "stroke_width": 0.6,
                "stroke_opacity": 0.40,
            },
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=0,
        )

        # Restore obstacle
        obstacle2 = Circle(radius=0.88)
        obstacle2.set_stroke(OBJ_COLOR, width=2.5)
        obstacle2.set_fill(BG_COLOR, opacity=1.0)
        obstacle2.move_to(ORIGIN)

        # Color-coded streamlines
        seeds2 = [(-7, y) for y in np.linspace(-4.0, 4.0, 32)]
        col_streams = make_streamlines(
            flow_around_circle, seeds2,
            steps=165, dt=0.055, stroke_w=1.6, opacity=0.58, colored=True,
        )

        # Color-coded arrows
        xs = np.linspace(-6, 6, 13)
        ys = np.linspace(-3.5, 3.5, 9)
        col_arrows = make_arrow_grid(
            flow_around_circle, xs, ys,
            scale=0.30, colored=True, opacity=0.70,
        )

        self.play(
            FadeIn(grid2),
            Create(obstacle2),
            run_time=1.0, rate_func=smooth,
        )
        self.play(
            Create(col_streams, lag_ratio=0.020),
            run_time=2.5, rate_func=smooth,
        )
        self.play(
            FadeIn(col_arrows, lag_ratio=0.02),
            run_time=1.2,
        )

        # Speed legend (bottom-right)
        slow_lbl   = Text("slow", font_size=17, color=SLOW_COLOR)
        fast_lbl   = Text("fast", font_size=17, color=FAST_COLOR)
        arr_legend = Arrow(
            LEFT * 0.55, RIGHT * 0.55,
            buff=0, stroke_width=2.5,
            color=CYAN_GLOW, tip_length=0.14,
        )
        legend = VGroup(slow_lbl, arr_legend, fast_lbl)
        legend.arrange(RIGHT, buff=0.18)
        legend.to_corner(DR, buff=0.50)
        legend.set_stroke(BLACK, width=2, background=True)

        speed_text = Text(
            "Flow speed varies at every point.",
            font_size=21, color=TEXT_WHITE, slant=ITALIC,
        ).to_edge(DOWN, buff=0.45)
        speed_text.set_stroke(BLACK, width=3, background=True)

        self.play(
            FadeIn(legend),
            FadeIn(speed_text, shift=UP * 0.1),
            run_time=0.8,
        )
        self.wait(3.0)

        self.play(
            FadeOut(col_arrows),
            FadeOut(speed_text),
            FadeOut(legend),
            run_time=0.8,
        )

        # Save for Part 10 cleanup
        self._grid2       = grid2
        self._obstacle2   = obstacle2
        self._col_streams = col_streams

    # ── Part 10: Bridge to mathematics (80–88 s) ─────────────
    def _part10_bridge_to_math(self):
        """
        Final scene: zoom out gently, fade to a quiet field,
        then present the closing message that mathematics is next.
        Leaves the viewer curious and ready for the next video.
        """
        # Fade obstacle, keep gentle streams
        self.play(
            FadeOut(self._obstacle2),
            self._col_streams.animate.set_opacity(0.22),
            self._grid2.animate.set_opacity(0.30),
            run_time=1.2,
        )

        # Gentle zoom-out to feel expansive
        self.play(
            self.camera.frame.animate
                .set_width(self._base_width * 1.10)
                .move_to(ORIGIN),
            run_time=1.5, rate_func=smooth,
        )

        # Closing statement — two lines for rhythm
        closing_top = Text(
            "To understand and control flow,",
            font_size=38, color=TEXT_WHITE, weight=BOLD,
        )
        closing_bot = Text(
            "we need mathematics.",
            font_size=38, color=CYAN_GLOW, weight=BOLD,
        )
        closing_bot.next_to(closing_top, DOWN, buff=0.30)
        closing = VGroup(closing_top, closing_bot)
        closing.move_to(ORIGIN)
        closing.set_stroke(BLACK, width=5, background=True)

        self.play(
            FadeIn(closing, scale=1.04),
            run_time=1.8, rate_func=smooth,
        )
        self.wait(3.0)

        # Graceful fade to black
        self.play(
            FadeOut(closing),
            FadeOut(self._col_streams),
            FadeOut(self._grid2),
            self.camera.frame.animate.set_width(self._base_width),
            run_time=2.5, rate_func=smooth,
        )
        self.wait(0.5)