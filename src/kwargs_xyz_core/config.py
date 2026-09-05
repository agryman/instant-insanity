"""This module defines manim configs."""

from typing import Any

from manim import WHITE

WHITE_CONFIG: dict[str, Any] = {
    "background_color": WHITE,
    "disable_caching": True,
    "preview": True,
}

LINEN_CONFIG: dict[str, Any] = {
    "background_color": "#ece6e2",
    "disable_caching": True,
    "preview": True,
}

PREVIEW_CONFIG: dict[str, Any] = {
    "disable_caching": True,
    "preview": True
}
