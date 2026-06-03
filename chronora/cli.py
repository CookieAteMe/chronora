from __future__ import annotations

import argparse
from pathlib import Path
import sys

from chronora.restore import discover_restore_plan, render_restore_plan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="chronora", description="Chronora continuity tooling")
    subparsers = parser.add_subparsers(dest="command")

    restore_parser = subparsers.add_parser(
        "restore",
        help="Compute a restore plan from Chronora state files",
    )
    restore_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Project directory to inspect (defaults to current directory)",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command != "restore":
        parser.print_help()
        return 1

    project_root = Path(args.path)
    plan = discover_restore_plan(project_root)
    print(render_restore_plan(plan))

    if plan.state_dir is None:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
