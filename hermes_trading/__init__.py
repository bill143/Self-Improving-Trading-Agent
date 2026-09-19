"""Hermes self-improving paper-trading worker.

The worker pulls market data, evaluates a versioned strategy, takes paper
trades, scores outcomes against a goal, and reflects to evolve the strategy
one variable at a time.

Paper mode only by default. Live execution is intentionally not importable
unless the operator explicitly opts in via environment flags.
"""

__version__ = "0.1.0"
