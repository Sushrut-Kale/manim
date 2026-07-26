from manim import *
import numpy as np

class LensCoatingScene(Scene):
    def construct(self):
        self.camera.background_color = "#020617"
        
        # TITLE FRAME
        self.title_frame()
        
        # PART 1: Real-world problem (0-8s)
        self.part1_glare_problem()
        
        # PART 2: Introduce coating (8-14s)
        self.part2_introduce_coating()
        
        # PART 3: Ray interference mechanism (14-24s)
        self.part3_ray_mechanism()
        
        # PART 4: Destructive interference (24-32s)
        self.part4_destructive_interference()
        
        # PART 5: Mathematical condition (32-40s)
        self.part5_math_condition()
        
        # PART 6: Rainbow effect (40-55s)
        self.part6_rainbow_effect()
        
        # PART 7: Before vs After (55-65s)
        self.part7_before_after()
        
        # PART 8: Real-world connection (65-75s)
        self.part8_real_world()
        
        # PART 9: Mini summary (75-80s)
        self.part9_summary()

    def clean_text(self, text, size=24, color=WHITE, bold=False):
        """Helper to create clean, readable text with consistent font"""
        weight = BOLD if bold else NORMAL
        return Text(text, font="Liberation Sans", font_size=size, color=color, weight=weight)

    def title_frame(self):
        """Opening title card"""
        bg_rect = Rectangle(width=16, height=9, color="#020617", fill_opacity=1, stroke_width=0)
        
        # Decorative line
        top_line = Line([-5, 0.8, 0], [5, 0.8, 0], color="#55FFAA", stroke_width=1.5)
        bot_line = Line([-5, -0.8, 0], [5, -0.8, 0], color="#55FFAA", stroke_width=1.5)
        
        title_main = Text("Anti-Reflection", font="Liberation Sans", font_size=52,
                           color="#E8F4FF", weight=BOLD)
        title_sub = Text("Lens Coating", font="Liberation Sans", font_size=52,
                          color="#55FFAA", weight=BOLD)
        title_main.shift(UP * 0.25)
        title_sub.shift(DOWN * 0.45)
        
        subtitle = Text("How thin films eliminate unwanted reflections",
                         font="Liberation Sans", font_size=20, color="#8899CC")
        subtitle.shift(DOWN * 1.5)
        
        scene_label = Text("Scene 6 — Thin Film Interference", font="Liberation Sans",
                            font_size=16, color="#445566")
        scene_label.to_edge(DOWN, buff=0.4)
        
        self.play(
            FadeIn(title_main, shift=UP*0.3),
            run_time=0.8
        )
        self.play(
            FadeIn(title_sub, shift=UP*0.3),
            run_time=0.8
        )
        self.play(
            Create(top_line), Create(bot_line),
            FadeIn(subtitle),
            FadeIn(scene_label),
            run_time=0.8
        )
        self.wait(2)
        self.play(
            FadeOut(VGroup(title_main, title_sub, top_line, bot_line, subtitle, scene_label)),
            run_time=0.8
        )

    def create_lens(self, center=ORIGIN, width=2.5, height=3.5, color="#88CCFF", opacity=0.25):
        lens = Ellipse(width=width, height=height, color=color, fill_opacity=opacity, stroke_width=2)
        lens.move_to(center)
        lens_glow = Ellipse(width=width+0.15, height=height+0.15, color=color,
                             fill_opacity=0.07, stroke_width=0)
        lens_glow.move_to(center)
        return VGroup(lens_glow, lens)

    def create_coating_layer(self, center=ORIGIN, width=2.5, height=3.5):
        coating = Ellipse(width=width+0.22, height=height+0.22, color="#AAFFCC",
                          fill_opacity=0.18, stroke_color="#55FFAA", stroke_width=1.5)
        coating.move_to(center)
        return coating

    def part1_glare_problem(self):
        # Section header — top left, small, not overlapping scene
        section_label = Text("Part 1 — The Glare Problem", font="Liberation Sans",
                              font_size=17, color="#556677")
        section_label.to_corner(UL, buff=0.25)
        self.play(FadeIn(section_label), run_time=0.4)

        lens = self.create_lens(center=ORIGIN)
        self.play(FadeIn(lens), run_time=1)

        # Incoming white light rays
        incoming_rays = VGroup()
        for offset in [-0.6, 0, 0.6]:
            ray = Arrow(start=[-4.5, 2.5+offset*0.3, 0], end=[-0.9, offset, 0],
                        color=WHITE, stroke_width=2.5, buff=0,
                        max_tip_length_to_length_ratio=0.08)
            incoming_rays.add(ray)

        self.play(LaggedStart(*[GrowArrow(r) for r in incoming_rays], lag_ratio=0.2),
                  run_time=1.2)

        # Strong reflection rays
        reflected_rays = VGroup()
        glare_colors = ["#FFFFFF", "#FFFCEE", "#FFF8DD"]
        for i, offset in enumerate([-0.6, 0, 0.6]):
            ray = Arrow(start=[-0.9, offset, 0], end=[-4.5, -1.5+offset*0.3, 0],
                        color=glare_colors[i], stroke_width=3, buff=0,
                        max_tip_length_to_length_ratio=0.08)
            reflected_rays.add(ray)

        glare_glow = Circle(radius=1.2, color="#FFFFFF", fill_opacity=0.08, stroke_width=0)
        glare_glow.move_to([-1.5, 0, 0])

        self.play(
            LaggedStart(*[GrowArrow(r) for r in reflected_rays], lag_ratio=0.15),
            FadeIn(glare_glow),
            run_time=1.2
        )

        # Flash
        flash = Rectangle(width=16, height=9, color=WHITE, fill_opacity=0.18, stroke_width=0)
        self.play(FadeIn(flash), run_time=0.2)
        self.play(FadeOut(flash), run_time=0.4)

        # Caption — bottom center, clear area
        glare_text = Text("Light is lost due to reflection", font="Liberation Sans",
                           font_size=22, color="#FF9966")
        glare_text.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(glare_text, shift=UP*0.1), run_time=0.6)
        self.wait(1.8)

        self.play(FadeOut(VGroup(incoming_rays, reflected_rays, glare_glow,
                                  glare_text, section_label)), run_time=0.8)
        self.lens_group = lens

    def part2_introduce_coating(self):
        section_label = Text("Part 2 — The Coating Solution", font="Liberation Sans",
                              font_size=17, color="#556677")
        section_label.to_corner(UL, buff=0.25)
        self.play(FadeIn(section_label), run_time=0.4)

        coating = self.create_coating_layer(center=ORIGIN)
        self.play(DrawBorderThenFill(coating), run_time=1.2)

        # Label to the RIGHT of the lens, vertically centered — no overlap
        coating_label = Text("Anti-Reflection Coating", font="Liberation Sans",
                              font_size=19, color="#55FFAA", weight=BOLD)
        coating_label.move_to([3.5, 1.2, 0])
        arrow_to_coating = Arrow([3.0, 1.0, 0], [1.5, 0.2, 0],
                                  color="#55FFAA", stroke_width=1.8, buff=0.1,
                                  max_tip_length_to_length_ratio=0.15)

        self.play(FadeIn(coating_label), GrowArrow(arrow_to_coating), run_time=0.8)

        # Thickness note below
        thickness_note = Text("Thickness ~ 100 nm  (tuned to wavelength)",
                               font="Liberation Sans", font_size=17, color="#AACCBB")
        thickness_note.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(thickness_note), run_time=0.6)

        # Shimmer
        shimmer = Ellipse(width=2.8, height=3.8, color="#AAFFCC",
                           fill_opacity=0, stroke_color="#AAFFCC", stroke_width=1)
        self.play(Create(shimmer), run_time=0.5)
        self.play(shimmer.animate.scale(1.06).set_stroke(opacity=0), run_time=0.5)
        self.remove(shimmer)

        self.wait(1.5)
        self.coating = coating
        self.play(FadeOut(VGroup(coating_label, arrow_to_coating,
                                  thickness_note, section_label)), run_time=0.6)

    def part3_ray_mechanism(self):
        section_label = Text("Part 3 — Ray Interference Mechanism",
                              font="Liberation Sans", font_size=17, color="#556677")
        section_label.to_corner(UL, buff=0.25)
        self.play(FadeIn(section_label), run_time=0.4)

        # Fade out the curved lens, work with flat surfaces for clarity
        self.play(FadeOut(VGroup(self.lens_group, self.coating)), run_time=0.5)

        # Flat surface representation — horizontal lines
        glass_line = Line([-5.5, -0.5, 0], [5.5, -0.5, 0],
                           color="#88CCFF", stroke_width=2.5)
        coating_top_line = Line([-5.5, 0.5, 0], [5.5, 0.5, 0],
                                 color="#55FFAA", stroke_width=2.5)

        # Fill between surfaces
        coating_fill = Rectangle(width=11, height=1.0, color="#55FFAA",
                                  fill_opacity=0.1, stroke_width=0)
        coating_fill.move_to([0, 0, 0])

        # Surface labels — RIGHT side, staggered vertically
        glass_surf_label = Text("Glass Surface", font="Liberation Sans",
                                 font_size=16, color="#88CCFF")
        glass_surf_label.move_to([3.8, -0.9, 0])
        coating_surf_label = Text("Coating Surface", font="Liberation Sans",
                                   font_size=16, color="#55FFAA")
        coating_surf_label.move_to([3.8, 0.9, 0])

        self.play(
            Create(coating_fill),
            Create(glass_line),
            Create(coating_top_line),
            FadeIn(glass_surf_label),
            FadeIn(coating_surf_label),
            run_time=1.0
        )

        # Incoming ray — from upper left
        inc_ray = Arrow([-4.5, 3.0, 0], [-1.5, 0.5, 0], color=WHITE, stroke_width=2.8,
                         buff=0, max_tip_length_to_length_ratio=0.09)
        self.play(GrowArrow(inc_ray), run_time=0.7)

        # RAY 1: reflects off coating top surface
        ray1 = Arrow([-1.5, 0.5, 0], [-4.5, -1.5, 0], color="#FFD700", stroke_width=2.8,
                      buff=0, max_tip_length_to_length_ratio=0.09)
        # Label for Ray 1 — above and LEFT, clear of other text
        ray1_label_bg = Rectangle(width=1.8, height=0.45, color="#020617",
                                   fill_opacity=0.85, stroke_width=0)
        ray1_label_bg.move_to([-4.0, 1.2, 0])
        ray1_label = Text("Ray 1", font="Liberation Sans", font_size=17, color="#FFD700", weight=BOLD)
        ray1_label.move_to([-4.0, 1.2, 0])

        self.play(GrowArrow(ray1), run_time=0.6)
        self.play(FadeIn(ray1_label_bg), FadeIn(ray1_label), run_time=0.4)

        # RAY 2: through coating, reflects off glass, comes back out
        # Into coating
        ray2_down = Arrow([-1.5, 0.5, 0], [-0.8, -0.5, 0], color="#00BFFF", stroke_width=2.8,
                           buff=0, max_tip_length_to_length_ratio=0.09)
        # Reflects off glass
        ray2_up = Arrow([-0.8, -0.5, 0], [-0.1, 0.5, 0], color="#00BFFF", stroke_width=2.8,
                         buff=0, max_tip_length_to_length_ratio=0.09)
        # Exits coating
        ray2_exit = Arrow([-0.1, 0.5, 0], [-3.0, 3.0, 0], color="#00BFFF", stroke_width=2.8,
                           buff=0, max_tip_length_to_length_ratio=0.09)

        ray2_label_bg = Rectangle(width=1.8, height=0.45, color="#020617",
                                   fill_opacity=0.85, stroke_width=0)
        ray2_label_bg.move_to([-2.5, 2.7, 0])
        ray2_label = Text("Ray 2", font="Liberation Sans", font_size=17, color="#00BFFF", weight=BOLD)
        ray2_label.move_to([-2.5, 2.7, 0])

        self.play(GrowArrow(ray2_down), run_time=0.5)
        self.play(GrowArrow(ray2_up), run_time=0.5)
        self.play(GrowArrow(ray2_exit), FadeIn(ray2_label_bg), FadeIn(ray2_label), run_time=0.5)

        # Path difference annotation — RIGHT side of diagram, no overlap
        path_label_bg = Rectangle(width=3.2, height=0.9, color="#020617",
                                   fill_opacity=0.9, stroke_width=0)
        path_label_bg.move_to([2.5, 0, 0])
        path_line1 = Text("Extra path = 2\u03bct", font="Liberation Sans",
                           font_size=17, color="#FFAA44")
        path_line1.move_to([2.5, 0.18, 0])
        path_line2 = Text("(optical path difference)", font="Liberation Sans",
                           font_size=14, color="#AA8833")
        path_line2.move_to([2.5, -0.22, 0])

        self.play(FadeIn(path_label_bg), FadeIn(path_line1), FadeIn(path_line2), run_time=0.7)

        self.wait(2.0)

        self.ray_scene_elements = VGroup(
            glass_line, coating_top_line, coating_fill,
            glass_surf_label, coating_surf_label,
            inc_ray, ray1, ray1_label_bg, ray1_label,
            ray2_down, ray2_up, ray2_exit, ray2_label_bg, ray2_label,
            path_label_bg, path_line1, path_line2
        )
        self.play(FadeOut(self.ray_scene_elements), FadeOut(section_label), run_time=0.8)

    def part4_destructive_interference(self):
        section_label = Text("Part 4 — Destructive Interference",
                              font="Liberation Sans", font_size=17, color="#556677")
        section_label.to_corner(UL, buff=0.25)
        self.play(FadeIn(section_label), run_time=0.4)

        # Wave labels — well separated vertically
        label_w1 = Text("Ray 1  (from coating surface)", font="Liberation Sans",
                         font_size=17, color="#FFD700")
        label_w1.to_edge(LEFT, buff=0.5).shift(UP*2.8)

        label_w2 = Text("Ray 2  (from glass surface)", font="Liberation Sans",
                         font_size=17, color="#00BFFF")
        label_w2.to_edge(LEFT, buff=0.5).shift(UP*0.5)

        self.play(FadeIn(label_w1), FadeIn(label_w2), run_time=0.6)

        def make_wave(x_start, x_end, amplitude, phase, color, n=220):
            x_vals = np.linspace(x_start, x_end, n)
            pts = [[x, amplitude * np.sin(2*PI*(x - x_start)/2.5 + phase), 0] for x in x_vals]
            w = VMobject(color=color, stroke_width=2.8)
            w.set_points_smoothly(pts)
            return w

        wave1 = make_wave(-3.8, 3.8, 0.55, 0, "#FFD700")
        wave1.shift(UP * 1.8)
        wave2 = make_wave(-3.8, 3.8, 0.55, PI, "#00BFFF")
        wave2.shift(UP * -0.5)

        self.play(Create(wave1), run_time=1)
        self.play(Create(wave2), run_time=1)

        # Phase shift note — upper RIGHT, isolated
        phase_bg = Rectangle(width=2.2, height=1.0, color="#020617",
                               fill_opacity=0.92, stroke_color="#FF8844", stroke_width=1)
        phase_bg.to_corner(UR, buff=0.4)
        phase_text = Text("\u03c0 phase\nshift", font="Liberation Sans", font_size=17, color="#FF8844")
        phase_text.move_to(phase_bg.get_center())
        self.play(FadeIn(phase_bg), FadeIn(phase_text), run_time=0.6)

        self.wait(0.6)

        # Cancellation — morph both waves into flat line
        flat_line = Line([-3.8, 0.65, 0], [3.8, 0.65, 0], color="#FF4444", stroke_width=2.5)
        # "ghost" flat for wave2 position
        flat_line2 = Line([-3.8, -0.5, 0], [3.8, -0.5, 0], color="#FF4444", stroke_width=0.3)

        self.play(
            Transform(wave1, flat_line),
            Transform(wave2, flat_line2),
            run_time=1.5
        )

        # Result — centered, below the waves, background box for clarity
        result_bg = Rectangle(width=5.5, height=0.7, color="#020617",
                               fill_opacity=0.95, stroke_color="#FF6644", stroke_width=1.5)
        result_bg.shift(DOWN*1.4)
        result_text = Text("Almost zero reflected light", font="Liberation Sans",
                            font_size=20, color="#FF6644")
        result_text.move_to(result_bg.get_center())

        destruct_bg = Rectangle(width=4.6, height=0.7, color="#020617",
                                 fill_opacity=0.95, stroke_color="#FF8866", stroke_width=1.5)
        destruct_bg.shift(DOWN*2.3)
        destruct_text = Text("Destructive Interference", font="Liberation Sans",
                              font_size=22, color="#FF8866", weight=BOLD)
        destruct_text.move_to(destruct_bg.get_center())

        self.play(FadeIn(result_bg), FadeIn(result_text), run_time=0.6)
        self.play(FadeIn(destruct_bg), FadeIn(destruct_text), run_time=0.6)

        self.wait(2.0)
        self.play(FadeOut(VGroup(wave1, wave2, label_w1, label_w2,
                                  phase_bg, phase_text, flat_line, flat_line2,
                                  result_bg, result_text, destruct_bg, destruct_text,
                                  section_label)), run_time=0.8)

    def part5_math_condition(self):
        section_label = Text("Part 5 — Optimal Coating Thickness",
                              font="Liberation Sans", font_size=17, color="#556677")
        section_label.to_corner(UL, buff=0.25)
        self.play(FadeIn(section_label), run_time=0.4)

        # Title — top, isolated
        opt_label = Text("Optimal Coating Thickness Condition",
                          font="Liberation Sans", font_size=22, color="#FFCC55", weight=BOLD)
        opt_label.to_edge(UP, buff=0.7)
        self.play(FadeIn(opt_label, shift=DOWN*0.2), run_time=0.6)

        # Equations — stacked, left-center
        eq1 = MathTex(r"2\mu t = \frac{\lambda}{2}", font_size=56, color="#E8F4FF")
        eq1.shift(LEFT*1.5 + UP*0.5)
        eq2 = MathTex(r"\Rightarrow \quad t = \frac{\lambda}{4\mu}", font_size=56, color="#AADDFF")
        eq2.shift(LEFT*1.5 + DOWN*0.9)

        self.play(Write(eq1), run_time=1.2)
        self.play(Write(eq2), run_time=1.0)

        # Legend — right column, stacked with clear spacing
        legend_items = [
            ("\u03bc = refractive index of coating", "#88CCBB"),
            ("t  = thickness of coating", "#88CCBB"),
            ("\u03bb = wavelength of light", "#88CCBB"),
        ]
        legend_group = VGroup()
        for i, (txt, col) in enumerate(legend_items):
            bg = Rectangle(width=4.0, height=0.42, color="#0A1525",
                            fill_opacity=0.9, stroke_width=0)
            lbl = Text(txt, font="Liberation Sans", font_size=16, color=col)
            bg.move_to([3.5, 0.6 - i*0.65, 0])
            lbl.move_to([3.5, 0.6 - i*0.65, 0])
            legend_group.add(bg, lbl)

        self.play(FadeIn(legend_group), run_time=0.7)

        # Visual thickness bar
        thickness_bg = Rectangle(width=0.35, height=1.4, color="#55FFAA",
                                  fill_opacity=0.25, stroke_color="#55FFAA", stroke_width=2)
        thickness_bg.shift(RIGHT*0.5 + UP*0.5)
        t_arrow = DoubleArrow(
            thickness_bg.get_bottom() + DOWN*0.05,
            thickness_bg.get_top() + UP*0.05,
            color="#FFDD88", stroke_width=2, buff=0.0,
            max_tip_length_to_length_ratio=0.3
        )
        t_arrow.next_to(thickness_bg, RIGHT, buff=0.15)
        t_note = Text("~100 nm", font="Liberation Sans", font_size=15, color="#FFDD88")
        t_note.next_to(t_arrow, RIGHT, buff=0.12)

        self.play(FadeIn(thickness_bg), GrowArrow(t_arrow), FadeIn(t_note), run_time=0.8)
        self.wait(2.2)

        self.play(FadeOut(VGroup(opt_label, eq1, eq2, legend_group,
                                  thickness_bg, t_arrow, t_note, section_label)), run_time=0.8)

    def part6_rainbow_effect(self):
        section_label = Text("Part 6 — Wavelength-Dependent Interference",
                              font="Liberation Sans", font_size=17, color="#556677")
        section_label.to_corner(UL, buff=0.25)
        self.play(FadeIn(section_label), run_time=0.4)

        # Subtitle — top center, isolated
        info_bg = Rectangle(width=6.5, height=0.55, color="#020617",
                              fill_opacity=0.95, stroke_color="#6688AA", stroke_width=1)
        info_bg.to_edge(UP, buff=0.65)
        info_text = Text("Different wavelengths interfere differently",
                          font="Liberation Sans", font_size=19, color="#DDDDFF")
        info_text.move_to(info_bg.get_center())
        self.play(FadeIn(info_bg), FadeIn(info_text), run_time=0.6)

        # Vertical surfaces — LEFT side
        lens_line = Line([-1.5, -2.5, 0], [-1.5, 2.5, 0], color="#88CCFF", stroke_width=2.5)
        coating_line = Line([-1.9, -2.5, 0], [-1.9, 2.5, 0], color="#55FFAA", stroke_width=2.5)

        glass_lbl = Text("Glass", font="Liberation Sans", font_size=15, color="#88CCFF")
        glass_lbl.move_to([-1.0, -2.1, 0])
        coat_lbl = Text("Coating", font="Liberation Sans", font_size=15, color="#55FFAA")
        coat_lbl.move_to([-2.5, -2.1, 0])

        self.play(Create(coating_line), Create(lens_line),
                  FadeIn(glass_lbl), FadeIn(coat_lbl), run_time=0.7)

        # Incoming white ray
        white_ray = Arrow([-5.5, 2.2, 0], [-1.9, 0, 0], color=WHITE, stroke_width=3,
                           buff=0, max_tip_length_to_length_ratio=0.08)
        white_lbl_bg = Rectangle(width=2.2, height=0.42, color="#020617",
                                  fill_opacity=0.9, stroke_width=0)
        white_lbl_bg.move_to([-4.5, 2.7, 0])
        white_lbl = Text("White Light", font="Liberation Sans", font_size=17, color=WHITE)
        white_lbl.move_to([-4.5, 2.7, 0])
        self.play(GrowArrow(white_ray), FadeIn(white_lbl_bg), FadeIn(white_lbl), run_time=0.7)

        # Wavelength data: color, label_text, reflect_alpha, transmit_width, y_pos
        wavelength_data = [
            ("#FF3333", "Red  — partial reflection",   0.7,  2.0,  1.2),
            ("#44FF44", "Green — cancelled (tuned)",   0.08, 3.5, -0.1),
            ("#4499FF", "Blue  — partial reflection",  0.55, 2.2, -1.4),
        ]

        all_wl_elements = VGroup()
        for color, label_text, refl_alpha, trans_width, ypos in wavelength_data:
            # Reflected ray — going left/up
            refl = Arrow([-1.9, ypos, 0], [-5.0, ypos + 1.8, 0],
                          color=color, stroke_width=2.5 * refl_alpha + 0.3,
                          buff=0, max_tip_length_to_length_ratio=0.1)
            refl.set_opacity(max(refl_alpha, 0.2))

            # Transmitted ray — going right
            trans = Arrow([-1.5, ypos, 0], [5.0, ypos * 0.6, 0],
                           color=color, stroke_width=trans_width,
                           buff=0, max_tip_length_to_length_ratio=0.07)
            trans.set_opacity(0.85)

            # Label — RIGHT side, with background box, staggered
            lbl_bg = Rectangle(width=4.0, height=0.42, color="#020617",
                                 fill_opacity=0.92, stroke_color=color, stroke_width=0.8)
            lbl_bg.move_to([3.2, ypos + 0.55, 0])
            lbl = Text(label_text, font="Liberation Sans", font_size=15, color=color)
            lbl.move_to([3.2, ypos + 0.55, 0])

            all_wl_elements.add(refl, trans, lbl_bg, lbl)

        self.play(
            LaggedStart(*[FadeIn(el) for el in all_wl_elements], lag_ratio=0.15),
            run_time=2.0
        )

        # Rainbow shimmer on coating line
        rainbow_shimmer = Line([-1.9, -2.5, 0], [-1.9, 2.5, 0],
                                color=color_gradient([RED, YELLOW, GREEN, BLUE, PURPLE], 30),
                                stroke_width=5)
        self.play(Create(rainbow_shimmer), run_time=0.7)

        # Rainbow tint note — bottom, isolated box
        rainbow_note_bg = Rectangle(width=4.8, height=0.55, color="#020617",
                                     fill_opacity=0.95, stroke_color="#AAAACC", stroke_width=1)
        rainbow_note_bg.to_edge(DOWN, buff=0.45)
        rainbow_note = Text("Faint rainbow tint visible on coated lenses",
                             font="Liberation Sans", font_size=17, color="#CCCCFF")
        rainbow_note.move_to(rainbow_note_bg.get_center())

        self.play(FadeIn(rainbow_note_bg), FadeIn(rainbow_note), run_time=0.6)
        self.wait(2.5)

        self.play(FadeOut(VGroup(info_bg, info_text, lens_line, coating_line,
                                  glass_lbl, coat_lbl, white_ray, white_lbl_bg, white_lbl,
                                  all_wl_elements, rainbow_shimmer,
                                  rainbow_note_bg, rainbow_note, section_label)),
                  run_time=0.8)

    def part7_before_after(self):
        section_label = Text("Part 7 — Before vs After",
                              font="Liberation Sans", font_size=17, color="#556677")
        section_label.to_corner(UL, buff=0.25)
        self.play(FadeIn(section_label), run_time=0.4)

        divider = Line(UP*3.8, DOWN*3.8, color="#334455", stroke_width=1.5)

        left_title = Text("No Coating", font="Liberation Sans", font_size=21,
                           color="#FF7766", weight=BOLD)
        left_title.move_to([-3.5, 3.0, 0])
        right_title = Text("With Coating", font="Liberation Sans", font_size=21,
                            color="#44FF99", weight=BOLD)
        right_title.move_to([3.5, 3.0, 0])

        self.play(Create(divider), FadeIn(left_title), FadeIn(right_title), run_time=0.7)

        # LEFT: uncoated
        lens_l = Ellipse(width=1.4, height=2.4, color="#88CCFF",
                          fill_opacity=0.2, stroke_width=2)
        lens_l.shift(LEFT*3.5)
        inc_l = Arrow([-6.0, 1.8, 0], [-4.3, 0.2, 0], color=WHITE,
                       stroke_width=2.5, buff=0, max_tip_length_to_length_ratio=0.1)
        refl_l = Arrow([-4.3, 0.2, 0], [-6.0, -1.5, 0], color="#FFFFFF",
                        stroke_width=3.2, buff=0, max_tip_length_to_length_ratio=0.1)
        trans_l = Arrow([-2.8, 0.2, 0], [-1.5, 0.1, 0], color=WHITE,
                         stroke_width=1.0, buff=0, max_tip_length_to_length_ratio=0.1)

        strong_bg = Rectangle(width=2.5, height=0.45, color="#020617",
                               fill_opacity=0.92, stroke_width=0)
        strong_bg.move_to([-4.8, -2.3, 0])
        strong_label = Text("Strong Reflection", font="Liberation Sans",
                             font_size=15, color="#FF9966")
        strong_label.move_to([-4.8, -2.3, 0])

        weak_bg = Rectangle(width=2.2, height=0.42, color="#020617",
                              fill_opacity=0.92, stroke_width=0)
        weak_bg.move_to([-1.9, -2.3, 0])
        weak_label = Text("Weak Transmission", font="Liberation Sans",
                           font_size=15, color="#AAAAAA")
        weak_label.move_to([-1.9, -2.3, 0])

        # RIGHT: coated
        lens_r = Ellipse(width=1.4, height=2.4, color="#88CCFF",
                          fill_opacity=0.2, stroke_width=2)
        coating_r = Ellipse(width=1.6, height=2.6, color="#55FFAA",
                             fill_opacity=0.12, stroke_color="#55FFAA", stroke_width=1.5)
        lens_r.shift(RIGHT*3.5)
        coating_r.shift(RIGHT*3.5)

        inc_r = Arrow([1.2, 1.8, 0], [2.7, 0.2, 0], color=WHITE,
                       stroke_width=2.5, buff=0, max_tip_length_to_length_ratio=0.1)
        refl_r = Arrow([2.7, 0.2, 0], [1.2, -1.5, 0], color="#4466AA",
                        stroke_width=1.0, buff=0, max_tip_length_to_length_ratio=0.1)
        trans_r = Arrow([4.3, 0.2, 0], [6.0, 0.1, 0], color=WHITE,
                         stroke_width=3.5, buff=0, max_tip_length_to_length_ratio=0.1)

        min_bg = Rectangle(width=2.4, height=0.45, color="#020617",
                             fill_opacity=0.92, stroke_width=0)
        min_bg.move_to([2.2, -2.3, 0])
        min_label = Text("Minimal Reflection", font="Liberation Sans",
                          font_size=15, color="#44FF99")
        min_label.move_to([2.2, -2.3, 0])

        more_bg = Rectangle(width=2.4, height=0.45, color="#020617",
                              fill_opacity=0.92, stroke_width=0)
        more_bg.move_to([5.3, -2.3, 0])
        more_label = Text("Strong Transmission", font="Liberation Sans",
                           font_size=15, color="#44DDFF")
        more_label.move_to([5.3, -2.3, 0])

        self.play(FadeIn(VGroup(lens_l, lens_r, coating_r)), run_time=0.6)
        self.play(GrowArrow(inc_l), GrowArrow(inc_r), run_time=0.6)
        self.play(GrowArrow(refl_l), GrowArrow(refl_r), run_time=0.6)
        self.play(GrowArrow(trans_l), GrowArrow(trans_r), run_time=0.6)
        self.play(
            FadeIn(strong_bg), FadeIn(strong_label),
            FadeIn(weak_bg), FadeIn(weak_label),
            FadeIn(min_bg), FadeIn(min_label),
            FadeIn(more_bg), FadeIn(more_label),
            run_time=0.6
        )

        self.wait(2.5)
        self.play(FadeOut(VGroup(
            divider, left_title, right_title,
            lens_l, lens_r, coating_r,
            inc_l, inc_r, refl_l, refl_r, trans_l, trans_r,
            strong_bg, strong_label, weak_bg, weak_label,
            min_bg, min_label, more_bg, more_label, section_label
        )), run_time=0.8)

    def part8_real_world(self):
        section_label = Text("Part 8 — Real-World Applications",
                              font="Liberation Sans", font_size=17, color="#556677")
        section_label.to_corner(UL, buff=0.25)
        self.play(FadeIn(section_label), run_time=0.4)

        real_bg = Rectangle(width=5.0, height=0.6, color="#020617",
                              fill_opacity=0.95, stroke_color="#6688AA", stroke_width=1)
        real_bg.to_edge(UP, buff=0.65)
        real_title = Text("Used in all precision optics", font="Liberation Sans",
                           font_size=22, color="#EEEEFF", weight=BOLD)
        real_title.move_to(real_bg.get_center())
        self.play(FadeIn(real_bg), FadeIn(real_title), run_time=0.6)

        # Three icon groups
        def optic_icon(name, pos, color="#88CCFF"):
            body = Ellipse(width=1.1, height=1.8, color=color,
                            fill_opacity=0.2, stroke_width=2.2)
            coat = Ellipse(width=1.25, height=1.95, color="#55FFAA",
                            fill_opacity=0.1, stroke_color="#55FFAA", stroke_width=1.3)
            lbl_bg = Rectangle(width=2.2, height=0.42, color="#020617",
                                 fill_opacity=0.9, stroke_width=0)
            lbl = Text(name, font="Liberation Sans", font_size=17, color="#AACCEE")
            lbl_bg.next_to(body, DOWN, buff=0.25)
            lbl.move_to(lbl_bg.get_center())
            return VGroup(coat, body, lbl_bg, lbl).move_to(pos)

        glasses   = optic_icon("Eyeglasses",    LEFT*4.2 + DOWN*0.2, "#AACCFF")
        camera    = optic_icon("Camera Lens",   ORIGIN  + DOWN*0.2, "#FFCCAA")
        scope     = optic_icon("Microscope",    RIGHT*4.2 + DOWN*0.2, "#AAFFDD")

        self.play(
            LaggedStart(FadeIn(glasses), FadeIn(camera), FadeIn(scope), lag_ratio=0.3),
            run_time=1.2
        )

        note_bg = Rectangle(width=7.5, height=0.55, color="#020617",
                              fill_opacity=0.95, stroke_color="#445566", stroke_width=1)
        note_bg.to_edge(DOWN, buff=0.45)
        note = Text("Iridescent tint on lenses is characteristic of quality AR coatings",
                     font="Liberation Sans", font_size=16, color="#8899BB")
        note.move_to(note_bg.get_center())
        self.play(FadeIn(note_bg), FadeIn(note), run_time=0.6)

        self.wait(2.5)
        self.play(FadeOut(VGroup(real_bg, real_title, glasses, camera, scope,
                                  note_bg, note, section_label)), run_time=0.8)

    def part9_summary(self):
        # Summary title
        sum_title = Text("Summary — How AR Coating Works", font="Liberation Sans",
                          font_size=22, color="#EEEEFF", weight=BOLD)
        sum_title.to_edge(UP, buff=0.55)
        self.play(FadeIn(sum_title, shift=DOWN*0.2), run_time=0.7)

        steps = [
            ("Thin Film\nCoating",          "#55FFAA"),
            ("Optical Path\nDifference",    "#FFDD66"),
            ("Destructive\nInterference",   "#FF8866"),
            ("Reduced\nReflection",         "#66CCFF"),
        ]
        xpos = [-5.2, -1.8, 1.8, 5.2]

        boxes = VGroup()
        arr_group = VGroup()

        for i, ((lbl, col), xp) in enumerate(zip(steps, xpos)):
            box = RoundedRectangle(width=2.6, height=1.6, corner_radius=0.22,
                                    color=col, fill_color=col, fill_opacity=0.12,
                                    stroke_width=2.2)
            box.move_to([xp, -0.2, 0])
            txt = Text(lbl, font="Liberation Sans", font_size=17, color=col)
            txt.move_to(box.get_center())
            boxes.add(VGroup(box, txt))

            if i < len(steps) - 1:
                mid_x = (xpos[i] + xpos[i+1]) / 2
                arr = Arrow([xp + 1.3, -0.2, 0], [xpos[i+1] - 1.3, -0.2, 0],
                             color="#556677", stroke_width=2.2,
                             buff=0, max_tip_length_to_length_ratio=0.3)
                arr_group.add(arr)

        self.play(
            LaggedStart(*[FadeIn(b, shift=UP*0.15) for b in boxes], lag_ratio=0.2),
            run_time=1.5
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in arr_group], lag_ratio=0.2),
            run_time=0.8
        )

        final_bg = Rectangle(width=6.5, height=0.6, color="#020617",
                               fill_opacity=0.95, stroke_color="#4455AA", stroke_width=1)
        final_bg.shift(DOWN*2.1)
        final_text = Text("This is how real lenses work — and now you know the physics.",
                           font="Liberation Sans", font_size=18, color="#AADDFF", slant=ITALIC)
        final_text.move_to(final_bg.get_center())
        self.play(FadeIn(final_bg), FadeIn(final_text, shift=UP*0.15), run_time=0.8)

        self.wait(2.5)
        self.play(FadeOut(VGroup(sum_title, boxes, arr_group,
                                  final_bg, final_text)), run_time=1.2)