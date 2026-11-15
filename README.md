# Spore Evolution Simulation

A modular, Spore-inspired life simulation modeling the interaction between a **Predator** and **Prey** along a 1D infinite ray (`0 -> ∞`).

## Overview

Each simulation run consists of three distinct phases:
1. **Evolution Phase:** Randomly generates a Predator at position `0` and a Prey at a random position in `[0, 1000]` with evolved physical traits (legs, wings, claws, and teeth).
2. **Chase Phase:** The Predator pursues the Prey across the world using stamina-constrained movement capabilities (`Crawling`, `Hopping`, `Walking`, `Running`, `Flying`) until it either catches the Prey or runs out of stamina.
3. **Fight Phase:** If caught, both creatures exchange attacks modified by their evolved traits until one runs out of health.

## Architecture & Design Principles

The codebase is structured around **Single Responsibility (SRP)** and **Open-Closed (OCP)** principles, applying classic behavioral, structural, and creational design patterns:
- **Strategy:** Swappable movement decision algorithms during chase/escape.
- **Chain of Responsibility:** Dynamic movement capability resolution based on limbs and available stamina.
- **Decorator:** Composable attack power modifiers (`Teeth` additive bonuses and `Claws` multipliers).
- **Abstract Factory:** Decoupled creature generation for stochastic simulations and deterministic testing.
- **Iterator:** Step-by-step execution across 100 simulation runs.
- **Adapter:** Separation of core simulation domain events from console output formatting.

## Tech Stack & Quality Checks

- **Python:** `3.13+`
- **Formatting & Linting:** `ruff`
- **Static Type Checking:** `mypy`

### Running Locally

```bash
# Run the simulation (100 iterations)
python -m spore_sim.main

# Format, lint, and type-check
ruff format .
ruff check .
mypy .
