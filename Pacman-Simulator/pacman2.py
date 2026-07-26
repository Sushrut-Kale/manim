from manim import *
import numpy as np

GRID_SIZE = 15
TILE_SPACING = 0.45
PACMAN_SPEED = 0.2
GHOST_SPEED = 0.3

MAZE_DATA = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,0,1,1,1,1,1,2,0],
    [0,1,0,0,1,0,1,0,1,0,1,0,0,1,0],
    [0,2,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,1,0,0,0,0,0,1,0,0,1,0],
    [0,1,1,1,1,1,1,0,1,1,1,1,1,1,0],
    [0,0,0,0,1,0,1,1,1,0,1,0,0,0,0],
    [0,1,1,1,1,0,1,0,1,0,1,1,1,1,0],
    [0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,1,0,0,0,0,0,1,0,0,1,0],
    [0,1,1,1,1,1,1,0,1,1,1,1,1,1,0],
    [0,1,0,0,1,0,1,0,1,0,1,0,0,1,0],
    [0,2,1,1,1,1,1,1,1,1,1,1,1,2,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]
class PacmanSimulation(Scene):
    def construct(self):
        self.score_val = 0
        score_label = Text("SCORE: ", font_size=32).to_edge(UL, buff=0.5)
        score_num = Integer(self.score_val).next_to(score_label, RIGHT)
        self.add(score_label, score_num)
        def grid_to_point(r, c):
            x = (c - GRID_SIZE // 2) * TILE_SPACING
            y = (GRID_SIZE // 2 - r) * TILE_SPACING
            return np.array([x, y, 0])
        pellets = {}
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                pos = grid_to_point(r, c)
                if MAZE_DATA[r][c] == 0:
                    self.add(Square(side_length=TILE_SPACING).set_fill(BLUE_E, 0.4).set_stroke(BLUE, 2).move_to(pos))
                elif MAZE_DATA[r][c] in [1, 2]:
                    rad = 0.05 if MAZE_DATA[r][c] == 1 else 0.12
                    pellets[(r, c)] = Dot(pos, radius=rad, color=WHITE)
        
        pellet_group = VGroup(*pellets.values())
        self.add(pellet_group)
        pac_pos = [1, 1]
        pacman = Sector(
            0.18, 
            angle=300*DEGREES, 
            start_angle=30*DEGREES,
            color=YELLOW,
            fill_opacity=1
        ).move_to(grid_to_point(*pac_pos))
        ghost_colors = [RED, PINK, ORANGE, GREEN]
        ghost_starts = [[1, 13], [13, 1], [7, 7], [13, 13]]
        ghosts = VGroup()
        for i in range(4):
            g = VGroup(
                Square(side_length=0.3, color=ghost_colors[i], fill_opacity=1),
                Dot(radius=0.04, color=WHITE).shift(UL*0.06),
                Dot(radius=0.04, color=WHITE).shift(UR*0.06)
            ).move_to(grid_to_point(*ghost_starts[i]))
            g.grid_pos = np.array(ghost_starts[i])
            g.last_pos = np.array(ghost_starts[i])
            ghosts.add(g)
        self.add(pacman, ghosts)
        def get_valid_moves(pos, avoid=None):
            r, c = pos
            moves = []
            for dr, dc in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and MAZE_DATA[nr][nc] != 0:
                    if avoid is None or not np.array_equal([nr, nc], avoid):
                        moves.append([dr, dc])
            return moves if moves else [[0, 0]]
        for _ in range(int(20 / PACMAN_SPEED)):
            p_opts = get_valid_moves(pac_pos)
            p_step = p_opts[np.random.randint(len(p_opts))]
            pac_pos[0] += p_step[0]
            pac_pos[1] += p_step[1]
            curr_tile = tuple(pac_pos)
            if curr_tile in pellets:
                self.score_val += 10
                score_num.set_value(self.score_val)
                self.remove(pellets.pop(curr_tile))
            ghost_anims = []
            for g in ghosts:
                g_opts = get_valid_moves(g.grid_pos, avoid=g.last_pos)
                g_step = g_opts[np.random.randint(len(g_opts))]
                g.last_pos = np.array(g.grid_pos)
                g.grid_pos += np.array(g_step)
                ghost_anims.append(g.animate(run_time=PACMAN_SPEED, rate_func=linear).move_to(grid_to_point(*g.grid_pos)))
                if np.array_equal(g.grid_pos, pac_pos):
                    self.score_val -= 100
                    score_num.set_value(self.score_val)
            self.play(
                pacman.animate(run_time=PACMAN_SPEED, rate_func=linear).move_to(grid_to_point(*pac_pos)),
                *ghost_anims
            )
        self.play(Write(Text("GAME OVER", color=RED).scale(2)))
        self.wait(2)
