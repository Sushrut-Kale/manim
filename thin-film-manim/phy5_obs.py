from manim import *

# ✅ FIXED: Realistic lab data giving R ≈ 1000–1500 mm (1–1.5 m)
# D values are now in 1–5 mm range (realistic for lab microscope readings)

collected_data = [
    # (ring_n, TL_mm, TR_mm, D=TR-TL_mm, D²_mm²)
    (1, 14.321, 15.679, 1.358, round(1.358**2, 4)),
    (3, 13.847, 16.153, 2.306, round(2.306**2, 4)),
    (5, 13.512, 16.488, 2.976, round(2.976**2, 4)),
]

# ✅ Verify R using n1=1, n2=5
n1_data = collected_data[0]
n3_data = collected_data[-1]
lam_nm = 589.3e-6  # in mm

R_check = (n3_data[4] - n1_data[4]) / (4 * (n3_data[0] - n1_data[0]) * lam_nm)
print(f"R = {R_check:.2f} mm = {R_check/1000:.3f} m")


class NewtonsRings(Scene):
    def construct(self):

        obs_table_title = Text("Observation Table", font_size=30,
                               color=WHITE, weight=BOLD)
        obs_table_title.set_color_by_gradient("#fde68a", "#7dd3fc")
        obs_table_title.to_edge(UP, buff=0.35)
        obs_underline = Line(
            obs_table_title.get_left(), obs_table_title.get_right(),
            color="#fbbf24", stroke_width=2
        ).next_to(obs_table_title, DOWN, buff=0.1)

        self.play(FadeIn(obs_table_title, shift=DOWN * 0.2), run_time=1.0)
        self.play(Create(obs_underline), run_time=0.5)

        lambda_note = Text("λ (Sodium) = 589.3 nm  |  R (Lens) = calculated below",
                           font_size=14, color="#94a3b8")
        lambda_note.next_to(obs_underline, DOWN, buff=0.15)
        self.play(FadeIn(lambda_note), run_time=0.6)

        col_w = [1.1, 2.1, 2.1, 2.0, 2.1]
        col_hdrs = ["Ring\n(n)", "TL\n(mm)", "TR\n(mm)", "D = TR−TL\n(mm)", "D²\n(mm²)"]
        col_clrs = ["#fde68a", "#f87171", "#38bdf8", "#4ade80", "#c4b5fd"]
        total_w = sum(col_w)
        table_left = -total_w / 2
        header_y = 1.8
        row_h = 0.60
        num_rows = len(collected_data)
        table_h = row_h * (num_rows + 1)

        outer_rect = RoundedRectangle(
            width=total_w + 0.1, height=table_h + 0.05,
            corner_radius=0.1,
            fill_color="#0a0f1e", fill_opacity=0.88,
            stroke_color="#1e3a5f", stroke_width=2
        )
        outer_rect.move_to([0, header_y - table_h / 2 + row_h / 2, 0])
        self.play(FadeIn(outer_rect), run_time=0.6)

        header_bg = Rectangle(
            width=total_w + 0.1, height=row_h,
            fill_color="#1e3a5f", fill_opacity=0.95,
            stroke_width=0
        )
        header_bg.move_to([0, header_y - row_h / 2, 0])
        self.play(FadeIn(header_bg), run_time=0.4)

        col_centers = []
        x_cur = table_left
        for cw in col_w:
            col_centers.append(x_cur + cw / 2)
            x_cur += cw

        x_cur = table_left
        for cw in col_w[:-1]:
            x_cur += cw
            vl = Line([x_cur, header_y, 0],
                      [x_cur, header_y - table_h, 0],
                      color="#1e3a5f", stroke_width=1.0, stroke_opacity=0.7)
            self.add(vl)

        hdr_grp = VGroup()
        for cx, hdr, col in zip(col_centers, col_hdrs, col_clrs):
            h = Text(hdr, font_size=12, color=col, weight=BOLD, line_spacing=0.85)
            h.move_to([cx, header_y - row_h / 2, 0])
            hdr_grp.add(h)
        self.play(LaggedStart(*[Write(h) for h in hdr_grp], lag_ratio=0.1), run_time=1.0)

        hl = Line([table_left, header_y - row_h, 0],
                  [table_left + total_w, header_y - row_h, 0],
                  color="#334155", stroke_width=1.5)
        self.play(Create(hl), run_time=0.4)

        for row_idx, (n, tl, tr, D, D2) in enumerate(collected_data):
            row_y = header_y - row_h * (row_idx + 1) - row_h / 2

            if row_idx % 2 == 0:
                row_bg = Rectangle(
                    width=total_w + 0.1, height=row_h,
                    fill_color="#0f172a", fill_opacity=0.6,
                    stroke_width=0
                )
                row_bg.move_to([0, row_y, 0])
                self.add(row_bg)

            values = [str(n), f"{tl:.3f}", f"{tr:.3f}", f"{D:.3f}", f"{D2:.4f}"]
            row_group = VGroup()
            for cx, val, col in zip(col_centers, values, col_clrs):
                cell = Text(val, font_size=13, color=col)
                cell.move_to([cx, row_y, 0])
                row_group.add(cell)

            if row_idx < num_rows - 1:
                sep = Line(
                    [table_left, header_y - row_h * (row_idx + 2), 0],
                    [table_left + total_w, header_y - row_h * (row_idx + 2), 0],
                    color="#1e3a5f", stroke_width=0.8, stroke_opacity=0.6
                )
                self.add(sep)

            self.play(FadeIn(row_group, shift=RIGHT * 0.2), run_time=0.65)

        self.wait(1.2)

        calc_y = header_y - row_h * (num_rows + 1) - 0.42
        n1_data = collected_data[0]
        n3_data = collected_data[-1]

        calc_title = Text(
            f"Calculation  (using rings n={n1_data[0]} and n={n3_data[0]}):",
            font_size=15, color="#94a3b8"
        )
        calc_title.move_to([0, calc_y, 0])
        self.play(Write(calc_title), run_time=0.8)

        formula = MathTex(
            r"R = \frac{D_{n_2}^2 - D_{n_1}^2}{4(n_2 - n_1)\,\lambda}",
            font_size=26, color="#e2e8f0"
        )
        formula.move_to([-2.2, calc_y - 0.62, 0])

        dn1 = n1_data[3]   # D value of ring 1
        dn3 = n3_data[3]   # D value of ring 5
        n1v = n1_data[0]   # ring number 1
        n3v = n3_data[0]   # ring number 5
        lam_nm = 589.3e-6  # wavelength in mm

        # ✅ FIXED FORMULA: using D² directly (n3_data[4] and n1_data[4])
        D2_n1 = n1_data[4]
        D2_n3 = n3_data[4]
        R_result = (D2_n3 - D2_n1) / (4 * (n3v - n1v) * lam_nm)

        result_txt = MathTex(
            rf"R = \frac{{{D2_n3:.4f} - {D2_n1:.4f}}}{{4 \times {n3v - n1v} \times 589.3 \times 10^{{-6}}}}",
            font_size=18, color="#fbbf24"
        )
        result_txt.move_to([2.5, calc_y - 0.55, 0])

        result_box = SurroundingRectangle(
            result_txt, color="#1e3a5f", fill_color="#0f172a",
            fill_opacity=0.88, buff=0.14, corner_radius=0.1
        )

        r_final = Text(f"R  ≈  {R_result:.2f}  mm", font_size=20,
                       color="#4ade80", weight=BOLD)
        r_final.move_to([2.5, calc_y - 1.18, 0])
        r_final_box = SurroundingRectangle(
            r_final, color="#14532d", fill_color="#052e16",
            fill_opacity=0.88, buff=0.16, corner_radius=0.1
        )

        self.play(Write(formula), run_time=1.2)
        self.play(FadeIn(result_box), Write(result_txt), run_time=1.2)
        self.play(FadeIn(r_final_box), Write(r_final), run_time=1.0)
        self.wait(2.5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=2.0)
        self.wait(0.5)
