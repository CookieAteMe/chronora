from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class RestoreArtifact:
    key: str
    path: Path
    description: str


@dataclass(frozen=True)
class RestorePlan:
    project_root: Path
    state_dir: Path | None
    artifacts: dict[str, RestoreArtifact]
    restore_order: list[RestoreArtifact]
    suggested_files: list[RestoreArtifact]
    warnings: list[str] = field(default_factory=list)
    recommended_prompt: str = ""


def discover_restore_plan(project_root: Path) -> RestorePlan:
    project_root = project_root.resolve()
    state_dir = project_root / ".claude"

    artifacts: dict[str, RestoreArtifact] = {}
    warnings: list[str] = []

    if not state_dir.exists():
        warnings.append("No Chronora state directory found at .claude/.")
        plan = RestorePlan(
            project_root=project_root,
            state_dir=None,
            artifacts=artifacts,
            restore_order=[],
            suggested_files=[],
            warnings=warnings,
            recommended_prompt=_build_prompt([], warnings),
        )
        return plan

    current_file = state_dir / "current.md"
    handoff_file = state_dir / "handoff.md"
    tasks_file = state_dir / "tasks.md"
    summaries_dir = state_dir / "summaries"
    sessions_dir = state_dir / "sessions"

    if current_file.is_file():
        artifacts["current"] = RestoreArtifact(
            key="current",
            path=current_file,
            description="Canonical live truth",
        )
    else:
        warnings.append("Canonical live truth file is missing: .claude/current.md")

    if handoff_file.is_file():
        artifacts["handoff"] = RestoreArtifact(
            key="handoff",
            path=handoff_file,
            description="Immediate next-session baton",
        )

    if tasks_file.is_file():
        artifacts["tasks"] = RestoreArtifact(
            key="tasks",
            path=tasks_file,
            description="Operational task registry",
        )

    summary_artifact = _pick_summary(summaries_dir)
    if summary_artifact is not None:
        artifacts["summary"] = summary_artifact

    archive_artifact = _pick_latest_archive(sessions_dir)
    if archive_artifact is not None:
        artifacts["archive"] = archive_artifact

    restore_order: list[RestoreArtifact] = []
    for key in ("current", "handoff", "tasks", "summary", "archive"):
        artifact = artifacts.get(key)
        if artifact is not None:
            restore_order.append(artifact)

    if not restore_order and state_dir.exists():
        warnings.append("No recognized restore artifacts found under .claude/.")

    suggested_files = list(restore_order)
    prompt = _build_prompt(suggested_files, warnings)

    return RestorePlan(
        project_root=project_root,
        state_dir=state_dir,
        artifacts=artifacts,
        restore_order=restore_order,
        suggested_files=suggested_files,
        warnings=warnings,
        recommended_prompt=prompt,
    )


def render_restore_plan(plan: RestorePlan) -> str:
    lines: list[str] = []
    lines.append("Chronora Restore Plan")
    lines.append("=====================")
    lines.append(f"Project Root: {plan.project_root}")
    lines.append(f"State Directory: {plan.state_dir if plan.state_dir else '(not found)'}")
    lines.append("")

    lines.append("Detected State")
    lines.append("--------------")
    if plan.artifacts:
        for artifact in plan.artifacts.values():
            lines.append(f"- {artifact.key}: {artifact.path} ({artifact.description})")
    else:
        lines.append("- No restore artifacts detected")
    lines.append("")

    lines.append("Restore Order")
    lines.append("-------------")
    if plan.restore_order:
        for index, artifact in enumerate(plan.restore_order, start=1):
            lines.append(f"{index}. {artifact.path} — {artifact.description}")
    else:
        lines.append("- No restore order available")
    lines.append("")

    lines.append("Suggested Files to Read")
    lines.append("-----------------------")
    if plan.suggested_files:
        for artifact in plan.suggested_files:
            lines.append(f"- {artifact.path}")
    else:
        lines.append("- No files suggested")
    lines.append("")

    lines.append("Warnings")
    lines.append("--------")
    if plan.warnings:
        for warning in plan.warnings:
            lines.append(f"- {warning}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("Recommended Prompt")
    lines.append("------------------")
    lines.append(plan.recommended_prompt)
    return "\n".join(lines)


def _pick_summary(summaries_dir: Path) -> RestoreArtifact | None:
    if not summaries_dir.is_dir():
        return None

    files = sorted((path for path in summaries_dir.iterdir() if path.is_file()), key=lambda p: p.name)
    if not files:
        return None

    project_candidates = [path for path in files if "project" in path.stem.lower()]
    chosen = project_candidates[-1] if project_candidates else files[-1]
    return RestoreArtifact(
        key="summary",
        path=chosen,
        description="Highest-value summary context",
    )


def _pick_latest_archive(sessions_dir: Path) -> RestoreArtifact | None:
    if not sessions_dir.is_dir():
        return None

    dirs = sorted((path for path in sessions_dir.iterdir() if path.is_dir()), key=lambda p: p.name)
    if not dirs:
        return None

    chosen = dirs[-1]
    return RestoreArtifact(
        key="archive",
        path=chosen,
        description="Latest archive evidence fallback",
    )


def _build_prompt(artifacts: Iterable[RestoreArtifact], warnings: list[str]) -> str:
    lines = [
        "Read the project continuity files in the listed order.",
        "Treat current.md as live truth.",
        "Use handoff/tasks to understand immediate work and active blockers.",
        "Use summaries only as compressed historical context.",
        "Use archives only as fallback evidence when state is missing or ambiguous.",
        "Do not replay transcript history; continue from explicit project state.",
    ]
    file_paths = [str(artifact.path) for artifact in artifacts]
    if file_paths:
        lines.append("Files to read:")
        lines.extend(f"- {path}" for path in file_paths)
    if warnings:
        lines.append("Warnings:")
        lines.extend(f"- {warning}" for warning in warnings)
    return "\n".join(lines)
