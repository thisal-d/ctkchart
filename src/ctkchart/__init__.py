"""
ctkchart: a library for create live update chart for customtkinter guis.
"""

from .CTkLineChart import CTkLineChart
from .CTkLine import CTkLine

# Constants for common string values
ENABLED = "enabled"
DISABLED = "disabled"

NORMAL = "normal"
DASHED = "dashed"
DOTTED = "dotted"

TOP = "top"
SIDE = "side"

AUTO = "auto"

__title__ = "ctkchart"
__version__ = "2.1.9"
__authors__ = ("Thisal Dilmith", "childeyouyu (有语)")

__all__ = [
    "CTkLineChart",
    "CTkLine",
    "ENABLED",
    "DISABLED",
    "NORMAL",
    "DASHED",
    "DOTTED",
    "TOP",
    "SIDE",
    "AUTO",
]
