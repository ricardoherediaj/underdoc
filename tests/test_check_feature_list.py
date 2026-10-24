import json

import check_feature_list


def feature(fid="a-1", **overrides):
    base = {
        "id": fid,
        "priority": 1,
        "phase": "S0",
        "area": "x",
        "title": "t",
        "user_visible_behavior": "b",
        "status": "not_started",
        "verification": ["cmd"],
        "evidence": [],
        "certification": [],
        "depends_on": [],
        "notes": "",
    }
    return {**base, **overrides}


def document(*features):
    return {
        "project": "p",
        "last_updated": "2026-10-24",
        "rules": {"single_active_feature": True, "passing_requires_evidence": True, "do_not_skip_verification": True},
        "status_legend": {"not_started": "", "in_progress": "", "blocked": "", "passing": ""},
        "features": list(features),
    }


def run(tmp_path, data, capsys):
    (tmp_path / "feature_list.json").write_text(json.dumps(data))
    code = check_feature_list.main(["--root", str(tmp_path)])
    return code, capsys.readouterr().out


def test_valid_list_passes(tmp_path, capsys):
    code, out = run(tmp_path, document(feature(), feature("a-2", depends_on=["a-1"])), capsys)
    assert code == 0 and "OK" in out


def test_passing_without_evidence_fails(tmp_path, capsys):
    code, out = run(tmp_path, document(feature(status="passing")), capsys)
    assert code == 1 and "evidence is empty" in out


def test_passing_with_evidence_passes(tmp_path, capsys):
    code, _ = run(tmp_path, document(feature(status="passing", evidence=["cmd: ok"])), capsys)
    assert code == 0


def test_two_in_progress_fails(tmp_path, capsys):
    code, out = run(tmp_path, document(feature(status="in_progress"), feature("a-2", status="in_progress")), capsys)
    assert code == 1 and "more than one feature is in_progress" in out


def test_bad_dependency_duplicate_and_tag_fail(tmp_path, capsys):
    code, out = run(tmp_path, document(feature(depends_on=["zzz"], certification=["custom:nope"]), feature()), capsys)
    assert code == 1
    assert "depends_on 'zzz'" in out and "duplicate id" in out and "custom:nope" in out
