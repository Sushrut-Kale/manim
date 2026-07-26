from manim import *
import random

PAC_YELLOW = YELLOW
GHOST_COLORS = [RED, PINK, BLUE, ORANGE]
class Pacman(VGroup):
    def __init__(self):
        super().__init__()
        self.body = Circle(radius=0.3, color=PAC_YELLOW, fill_opacity=1)
        self.add(self.body)
class Ghost(VGroup):
    def __init__(self, color):
        super().__init__()
        self.body = Square(0.5, color=color, fill_opacity=1)
        self.add(self.body)
class PacmanLearning(Scene):
    def construct(self):
        self.grid_size = 8
        self.cell_size = 0.8
        self.trial_scores = []
        self.create_maze()
        self.create_pellets()
        self.create_ghosts()
        self.create_pacman()
        self.create_score()
        self.run_trial("TRIAL 1", steps=30, smart=False)
        self.loading()
        self.run_trial("TRIAL 100", steps=40, smart=True)
        self.loading()
        self.run_trial("TRIAL 500", steps=60, smart=True, optimized=True)
        self.show_graph()
    def create_maze(self):
        self.paths = []
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                pos = self.grid_to_pos(i, j)
                sq = Square(self.cell_size, color=BLUE)
                sq.move_to(pos).shift(LEFT*3)
                self.add(sq)
                self.paths.append((i, j))
    def create_pellets(self):
        self.pellets = {}
        for cell in self.paths:
            dot = Dot(radius=0.05, color=WHITE)
            dot.move_to(self.grid_to_pos(*cell) + LEFT*3)
            self.add(dot)
            self.pellets[cell] = dot
    def create_ghosts(self):
        self.ghosts = []
        positions = [(1,1),(6,6),(1,6),(6,1)]
        for pos, color in zip(positions, GHOST_COLORS):
            g = Ghost(color)
            g.move_to(self.grid_to_pos(*pos) + LEFT*3)
            self.add(g)
            self.ghosts.append((g, pos))
    def create_pacman(self):
        self.pacman = Pacman()
        self.pac_pos = (0,0)
        self.pacman.move_to(self.grid_to_pos(*self.pac_pos) + LEFT*3)
        self.add(self.pacman)
    def create_score(self):
        self.score = 0
        self.score_text = always_redraw(lambda: Text(f"SCORE: {self.score}").scale(0.5).to_corner(UL))
        self.add(self.score_text)
    def grid_to_pos(self, i, j):
        return np.array([i - self.grid_size/2, j - self.grid_size/2, 0]) * self.cell_size
    def get_neighbors(self, pos):
        i, j = pos
        moves = [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]
        return [m for m in moves if m in self.paths]
    def move_pacman(self, new_pos):
        self.pac_pos = new_pos
        self.play(self.pacman.animate.move_to(self.grid_to_pos(*new_pos) + LEFT*3), run_time=0.2)
        if new_pos in self.pellets:
            self.remove(self.pellets[new_pos])
            del self.pellets[new_pos]
            self.score += 10
        for ghost, gpos in self.ghosts:
            if gpos == new_pos:
                self.score -= 100
    def run_trial(self, label, steps=30, smart=False, optimized=False):
        title = Text(label).to_edge(UP)
        self.play(FadeIn(title))
        for _ in range(steps):
            neighbors = self.get_neighbors(self.pac_pos)
            pellet_cells = [n for n in neighbors if n in self.pellets]
            safe_cells = [n for n in neighbors if n not in [g[1] for g in self.ghosts]]
            if smart:
                if pellet_cells:
                    next_pos = random.choice(pellet_cells)
                elif safe_cells:
                    next_pos = random.choice(safe_cells)
                else:
                    next_pos = random.choice(neighbors)
            else:
                if pellet_cells and random.random() < 0.6:
                    next_pos = random.choice(pellet_cells)
                else:
                    next_pos = random.choice(neighbors)
            if optimized:
                safe = [n for n in neighbors if n not in [g[1] for g in self.ghosts]]
                if safe:
                    next_pos = random.choice(safe)
            self.move_pacman(next_pos)
        self.trial_scores.append(self.score)
        self.play(FadeOut(title))
        self.play(Write(Text("GAME OVER", color=RED)))
        self.wait(1)
        self.clear()
        self.create_maze()
        self.create_pellets()
        self.create_ghosts()
        self.create_pacman()
        self.create_score()
    def loading(self):
        txt = Text("LOADING NEXT TRIAL...")
        self.play(Write(txt))
        self.wait(1)
        self.play(FadeOut(txt))
    def show_graph(self):
        axes = Axes(
            x_range=[0, 3, 1],
            y_range=[0, max(self.trial_scores)+50, 50],
            x_length=5,
            y_length=4,
        ).to_edge(RIGHT)
        labels = axes.get_axis_labels(x_label="Trial", y_label="Score")
        points = [axes.coords_to_point(i+1, score) for i, score in enumerate(self.trial_scores)]
        dots = VGroup(*[Dot(p) for p in points])
        lines = VGroup(*[Line(points[i], points[i+1]) for i in range(len(points)-1)])
        self.play(Create(axes), Write(labels))
        self.play(FadeIn(dots))
        self.play(Create(lines))
        self.wait(2)
