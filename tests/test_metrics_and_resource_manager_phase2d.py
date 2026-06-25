from __future__ import annotations

from core.metrics import get_metrics_collector
from core.resource_manager import ResourceManager


def test_metrics_collector_records_success(tmp_path):
    collector = get_metrics_collector()
    before = len(collector.events)

    with collector.track(operation="unit-test-metrics"):
        (tmp_path / "x").write_text("hi")

    after = len(collector.events)
    assert after == before + 1
    evt = collector.events[-1]
    assert evt.operation == "unit-test-metrics"
    assert evt.success is True


def test_resource_manager_cleans_up(tmp_path):
    p = tmp_path / "t.txt"
    p.write_text("x")
    assert p.exists()

    with ResourceManager() as mgr:
        mgr.register(p)
        assert p.exists()

    assert not p.exists()

