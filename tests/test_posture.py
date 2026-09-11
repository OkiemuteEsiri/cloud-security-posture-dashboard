import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from src.ingest import load_findings
from src.models import Finding
from src.reporting import metrics, render_markdown
from src.risk_engine import assess, assess_all


BASE = {
    "finding_id": "T-1", "provider": "aws", "account": "a", "resource_id": "r",
    "title": "synthetic finding", "severity": "high", "control_family": "identity",
    "owner": "security", "detected_at": "2026-09-01T00:00:00Z", "due_at": "2026-09-02T00:00:00Z"
}


class PostureTests(unittest.TestCase):
    def test_invalid_provider_rejected(self):
        raw = dict(BASE, provider="other")
        with self.assertRaises(ValueError): Finding.from_dict(raw)

    def test_timezone_required(self):
        raw = dict(BASE, detected_at="2026-09-01T00:00:00")
        with self.assertRaises(ValueError): Finding.from_dict(raw)

    def test_context_increases_score(self):
        plain = Finding.from_dict(BASE)
        contextual = Finding.from_dict(dict(BASE, internet_exposed=True, privileged_identity=True))
        now = datetime(2026, 9, 1, tzinfo=timezone.utc)
        self.assertGreater(assess(contextual, now).score, assess(plain, now).score)

    def test_score_is_bounded(self):
        f = Finding.from_dict(dict(BASE, severity="critical", internet_exposed=True, privileged_identity=True, critical_asset=True, known_exploited_context=True, logging_enabled=False))
        self.assertEqual(assess(f, datetime(2026, 10, 1, tzinfo=timezone.utc)).score, 100)

    def test_decision_id_is_deterministic(self):
        f = Finding.from_dict(BASE)
        now = datetime(2026, 9, 1, tzinfo=timezone.utc)
        self.assertEqual(assess(f, now).decision_id, assess(f, now).decision_id)

    def test_duplicate_ids_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "f.json"
            p.write_text(json.dumps([BASE, BASE]), encoding="utf-8")
            with self.assertRaises(ValueError): load_findings(p)

    def test_assess_all_orders_highest_first(self):
        low = Finding.from_dict(dict(BASE, finding_id="L", severity="low"))
        high = Finding.from_dict(dict(BASE, finding_id="H", severity="critical"))
        results = assess_all([low, high], datetime(2026, 9, 1, tzinfo=timezone.utc))
        self.assertEqual(results[0].finding_id, "H")

    def test_metrics_count_logging_gap(self):
        f = Finding.from_dict(dict(BASE, logging_enabled=False))
        a = [assess(f, datetime(2026, 9, 1, tzinfo=timezone.utc))]
        self.assertEqual(metrics([f], a)["logging_gaps"], 1)

    def test_report_contains_finding(self):
        f = Finding.from_dict(BASE)
        a = [assess(f, datetime(2026, 9, 1, tzinfo=timezone.utc))]
        self.assertIn("T-1", render_markdown([f], a))

    def test_missing_required_field_rejected(self):
        raw = dict(BASE); raw.pop("owner")
        with self.assertRaises(ValueError): Finding.from_dict(raw)


if __name__ == "__main__": unittest.main()
