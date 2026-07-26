# Pathfinding Simulation in a Discrete Grid through PACMAN Game Visualization

---

## Math Topic

**Graph Theory • Pathfinding Algorithms • Reinforcement Learning • Grid-Based Search**

---

## About the Video

**Pathfinding Simulation in a Discrete Grid through PACMAN Game Visualization** is a mathematical and algorithmic visualization developed using **Manim Community Edition**. The project demonstrates how search algorithms and intelligent decision-making can be represented inside the classic Pac-Man maze through smooth, cinematic animations.

Rather than focusing on gameplay, the animation visualizes the gradual construction of the entire game environment—from an empty screen to a fully functional maze. The maze, pellets, Pac-Man, and ghosts are introduced step by step, allowing viewers to understand both the underlying geometry and the logical structure behind the simulation.

The visualization highlights concepts such as discrete grids, pathfinding, coordinate systems, collision detection, object transformations, and reinforcement learning principles. Through synchronized animations and structured storytelling, the project presents algorithmic thinking in a visually engaging and intuitive manner.

---

## Mathematical Model

The simulation represents the maze as a **discrete two-dimensional grid**, where each cell corresponds to a valid position in the environment.

The agent moves according to

<p align="center">

$$
s_{t+1}=T(s_t,a_t)
$$

</p>

where

- **\(s_t\)** — Current state
- **\(a_t\)** — Selected action
- **\(T\)** — State transition function

The reinforcement learning objective is to maximize the cumulative discounted reward

<p align="center">

$$
R=\sum_{t=0}^{\infty}\gamma^t r_t
$$

</p>

The Q-values are updated using the Bellman Equation

<p align="center">

$$
Q(s,a)\leftarrow
Q(s,a)+
\alpha
\left[
r+\gamma\max_{a'}Q(s',a')
-
Q(s,a)
\right]
$$

</p>

where

- **Q(s,a)** — Expected utility of taking action **a** in state **s**
- **α** — Learning rate
- **γ** — Discount factor
- **r** — Immediate reward
- **s′** — Next state

---

## Objectives

- Demonstrate pathfinding within a discrete grid environment.
- Visualize search algorithms through cinematic animation.
- Explain reinforcement learning concepts using Pac-Man.
- Illustrate coordinate-based movement and collision detection.
- Present algorithmic decision-making in an intuitive manner.
- Combine mathematics, animation, and storytelling for educational visualization.

---

## Key Concepts Covered

- Discrete Grid Representation
- Coordinate Systems
- Pathfinding
- Search Algorithms
- Reinforcement Learning
- Markov Decision Process (MDP)
- Q-Learning
- Bellman Equation
- State Space
- Reward System
- Collision Detection
- Object Transformations
- Animation Synchronization
- Procedural Scene Generation

---

## Educational Significance

This project demonstrates how mathematical concepts, artificial intelligence, and computer graphics can be combined to create educational visualizations. It introduces learners to graph traversal, reinforcement learning, and intelligent decision-making while showcasing how algorithmic behavior can be represented through structured animations.

The project serves as an accessible introduction to pathfinding algorithms and reinforcement learning by transforming abstract computational concepts into engaging visual demonstrations.

---

## Video Highlights

- Step-by-step maze construction
- Procedural generation of pellets and obstacles
- Smooth Pac-Man movement
- Dynamic ghost movement
- Pellet consumption animation
- Grid-based navigation
- Reinforcement learning concepts
- Cinematic transitions and camera effects
- Clean vector graphics rendered with Manim

---

## Applications

- Artificial Intelligence
- Reinforcement Learning
- Robotics Navigation
- Autonomous Path Planning
- Computer Graphics
- Educational Animation
- Algorithm Visualization
- Game AI
- Grid-Based Search Problems

---

## Final Video

**Google Drive Link**

https://drive.google.com/file/d/1ztGzblT325IMRDbg3iF9Lanx1BCKe9UX/view?usp=sharing

---

## Conclusion

**Pathfinding Simulation in a Discrete Grid through PACMAN Game Visualization** combines mathematical modeling, reinforcement learning, and cinematic animation to demonstrate intelligent navigation inside a grid-based environment. By visualizing search algorithms and decision-making rather than traditional gameplay, the project provides an engaging educational experience that connects graph theory, artificial intelligence, and computer animation through clear, structured storytelling.