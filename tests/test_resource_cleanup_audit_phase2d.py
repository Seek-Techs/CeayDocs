from __future__ import annotations

from core.resource_manager import ResourceManager


def test_resource_manager_cleanup_multiple_files(tmp_path):
    p1 = tmp_path / "a.tmp"
    p2 = tmp_path / "b.tmp"
    p1.write_text("a")
    p2.write_text("b")

    with ResourceManager() as mgr:
        mgr.register(p1)
        mgr.register(p2)
        assert p1.exists()
        assert p2.exists()

    assert not p1.exists()
    assert not p2.exists()

