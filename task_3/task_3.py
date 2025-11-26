import argparse
import sys
from dataclasses import dataclass, field
from typing import Dict, List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Solve the Tower of Hanoi and log each move.",
    )
    parser.add_argument(
        "disks",
        type=int,
        nargs="?",
        default=3,
        help="Number of disks (positive integer). Default: 3.",
    )
    return parser.parse_args()


@dataclass
class TowerOfHanoi:
    disks: int
    rods: Dict[str, List[int]] = field(init=False)

    def __post_init__(self):
        if self.disks <= 0:
            raise ValueError("Number of disks must be positive.")
        self.rods = {"A": list(range(self.disks, 0, -1)), "B": [], "C": []}

    def solve(self):
        print(f"Initial state: {self.rods}")
        self._move(self.disks, "A", "C", "B")
        print(f"Final state: {self.rods}")

    def _move(self, n: int, source: str, target: str, auxiliary: str):
        if n == 0:
            return
        self._move(n - 1, source, auxiliary, target)
        self._move_disk(source, target)
        self._move(n - 1, auxiliary, target, source)

    def _move_disk(self, source: str, target: str):
        disk = self.rods[source].pop()
        self.rods[target].append(disk)
        print(f"Move disk from {source} to {target}: {disk}")
        print(f"State: {self.rods}")


def main():
    args = parse_args()
    try:
        hanoi = TowerOfHanoi(disks=args.disks)
        hanoi.solve()
    except Exception as error:  # noqa: BLE001
        print(f"Failed to solve: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
