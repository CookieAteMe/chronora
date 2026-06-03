from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from chronora.restore import discover_restore_plan


class RestorePlanTests(unittest.TestCase):
    def test_current_only_project(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / ".claude"
            state_dir.mkdir()
            (state_dir / "current.md").write_text("# Current Project\n", encoding="utf-8")

            plan = discover_restore_plan(root)

            self.assertEqual([artifact.key for artifact in plan.restore_order], ["current"])
            self.assertIn("current.md", plan.recommended_prompt)

    def test_current_handoff_tasks_order(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / ".claude"
            state_dir.mkdir()
            for name in ("current.md", "handoff.md", "tasks.md"):
                (state_dir / name).write_text("content", encoding="utf-8")

            plan = discover_restore_plan(root)

            self.assertEqual(
                [artifact.key for artifact in plan.restore_order],
                ["current", "handoff", "tasks"],
            )

    def test_summary_present_prefers_project_named_file(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / ".claude"
            summaries = state_dir / "summaries"
            summaries.mkdir(parents=True)
            (state_dir / "current.md").write_text("content", encoding="utf-8")
            (summaries / "2026-06-01-daily.md").write_text("daily", encoding="utf-8")
            (summaries / "2026-06-02-project-summary.md").write_text("project", encoding="utf-8")

            plan = discover_restore_plan(root)

            self.assertEqual(plan.artifacts["summary"].path.name, "2026-06-02-project-summary.md")
            self.assertEqual([artifact.key for artifact in plan.restore_order], ["current", "summary"])

    def test_archives_present_selects_latest_directory(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / ".claude"
            sessions = state_dir / "sessions"
            sessions.mkdir(parents=True)
            (state_dir / "current.md").write_text("content", encoding="utf-8")
            (sessions / "2026-05-27_10-00-00-12345").mkdir()
            (sessions / "2026-05-28_09-00-00-99999").mkdir()

            plan = discover_restore_plan(root)

            self.assertEqual(plan.artifacts["archive"].path.name, "2026-05-28_09-00-00-99999")
            self.assertEqual([artifact.key for artifact in plan.restore_order], ["current", "archive"])

    def test_missing_current_emits_warning_and_degraded_plan(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / ".claude"
            state_dir.mkdir()
            (state_dir / "handoff.md").write_text("content", encoding="utf-8")

            plan = discover_restore_plan(root)

            self.assertTrue(any("current.md" in warning for warning in plan.warnings))
            self.assertEqual([artifact.key for artifact in plan.restore_order], ["handoff"])

    def test_no_chronora_state(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan = discover_restore_plan(root)

            self.assertIsNone(plan.state_dir)
            self.assertEqual(plan.restore_order, [])
            self.assertTrue(any("No Chronora state directory" in warning for warning in plan.warnings))

    def test_prompt_mentions_live_truth_and_fallback_evidence(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / ".claude"
            sessions = state_dir / "sessions"
            sessions.mkdir(parents=True)
            (state_dir / "current.md").write_text("content", encoding="utf-8")
            (sessions / "2026-05-28_09-00-00-99999").mkdir()

            plan = discover_restore_plan(root)

            self.assertIn("Treat current.md as live truth", plan.recommended_prompt)
            self.assertIn("Use archives only as fallback evidence", plan.recommended_prompt)


if __name__ == "__main__":
    unittest.main()
