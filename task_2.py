import argparse
import math
import sys
import turtle
from dataclasses import dataclass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Draw a Koch snowflake at a chosen recursion level.",
    )
    parser.add_argument(
        "level",
        type=int,
        nargs="?",
        default=3,
        help="Recursion level (non-negative integer). Default: 3.",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=300,
        help="Side length in pixels for the base triangle. Default: 300.",
    )
    return parser.parse_args()


@dataclass
class KochSnowflake:
    level: int
    size: float

    def __post_init__(self):
        if self.level < 0:
            raise ValueError("Level must be non-negative.")
        self.turtle = turtle.Turtle(visible=False)
        self.screen = turtle.Screen()
        self.screen.title(f"Koch Snowflake (level {self.level})")
        self.turtle.speed(0)
        self.turtle.penup()
        self._center_start()
        self.turtle.pendown()

    def draw(self):
        for _ in range(3):
            self._draw_side(self.size, self.level)
            self.turtle.right(120)
        self.screen.mainloop()

    def _draw_side(self, length: float, level: int):
        if level == 0:
            self.turtle.forward(length)
            return
        segment = length / 3
        self._draw_side(segment, level - 1)
        self.turtle.left(60)
        self._draw_side(segment, level - 1)
        self.turtle.right(120)
        self._draw_side(segment, level - 1)
        self.turtle.left(60)
        self._draw_side(segment, level - 1)

    def _center_start(self):
        height = math.sqrt(3) / 2 * self.size
        self.turtle.setheading(0)
        self.turtle.goto(-self.size / 2, -height / 3)


def main():
    args = parse_args()
    try:
        snowflake = KochSnowflake(level=args.level, size=args.size)
        snowflake.draw()
    except Exception as error:  # noqa: BLE001
        print(f"Failed to draw snowflake: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
