"""Validate feature_list.json. Exit 1 with one line per problem."""

import argparse
import json
import sys
from pathlib import Path

PHASES = {"S0", "S1", "S2", "S3", "S4", "S5", "cert"}
RULES = ("single_active_feature", "passing_requires_evidence", "do_not_skip_verification")
CERT_TAGS = {
    "mandatory:fastmcp",
    "mandatory:tool",
    "mandatory:hitl-prompt",
    "mandatory:public-repo",
    "mandatory:uv-py314",
    "mandatory:src-layout",
    "mandatory:readme",
    "mandatory:no-secrets",
    "custom:mcp-client",
    "custom:third-party-apis",
    "custom:resources",
    "custom:workflow-patterns",
    "custom:agentic-pattern",
    "custom:cag",
    "custom:rag",
    "custom:memory",
    "custom:hitl-ux",
    "custom:multi-agent",
    "custom:observability",
    "custom:evals",
    "custom:custom-data",
    "custom:multimodal",
    "custom:code-quality-ci-docker",
    "custom:auth",
    "custom:database",
    "custom:cloud-deploy",
    "custom:structured-outputs",
}
STR_FIELDS = ("id", "area", "title", "user_visible_behavior", "status", "notes")
LIST_FIELDS = ("verification", "evidence", "certification", "depends_on")


def validate(data: object) -> list[str]:
    if not isinstance(data, dict):
        return ["top level must be a JSON object: restore the structure from the template in docs/harness.md."]
    problems: list[str] = []
    for key in ("project", "last_updated"):
        if not isinstance(data.get(key), str) or not data[key]:
            problems.append(f"top-level '{key}' must be a non-empty string: add it.")
    rules = data.get("rules")
    if not isinstance(rules, dict):
        problems.append("top-level 'rules' must be an object: add the three boolean rules.")
    else:
        for rule in RULES:
            if rules.get(rule) is not True:
                problems.append(f"rules.{rule} must be true: do not disable harness rules.")
    legend = data.get("status_legend")
    if not isinstance(legend, dict) or not legend:
        problems.append("top-level 'status_legend' must be a non-empty object: add the four statuses.")
        legend = {}
    features = data.get("features")
    if not isinstance(features, list) or not features:
        return problems + ["top-level 'features' must be a non-empty list: add the features."]

    ids = [f.get("id") for f in features if isinstance(f, dict)]
    known = set(ids)
    in_progress: list[str] = []
    seen: set[str] = set()
    for index, feature in enumerate(features):
        if not isinstance(feature, dict):
            problems.append(f"features[{index}] must be an object: fix the entry.")
            continue
        fid = str(feature.get("id", f"features[{index}]"))
        for field in STR_FIELDS:
            if not isinstance(feature.get(field), str) or (field != "notes" and not feature[field]):
                problems.append(f"{fid}: '{field}' must be a non-empty string: set it.")
        for field in LIST_FIELDS:
            if not isinstance(feature.get(field), list):
                problems.append(f"{fid}: '{field}' must be a list: use [] when empty.")
        if not isinstance(feature.get("priority"), int) or isinstance(feature.get("priority"), bool):
            problems.append(f"{fid}: 'priority' must be an integer: set it (lower runs first).")
        if feature.get("phase") not in PHASES:
            problems.append(f"{fid}: 'phase' must be one of {sorted(PHASES)}: fix it.")
        if fid in seen:
            problems.append(f"{fid}: duplicate id: give each feature a unique id.")
        seen.add(fid)
        status = feature.get("status")
        if isinstance(status, str) and status not in legend:
            problems.append(f"{fid}: status '{status}' is not in status_legend: use {sorted(legend)}.")
        if status == "in_progress":
            in_progress.append(fid)
        if status == "passing" and not feature.get("evidence"):
            problems.append(
                f"{fid}: status is passing but evidence is empty: run the verification and record command and result, or set status back."
            )
        if not feature.get("verification"):
            problems.append(f"{fid}: 'verification' is empty: list the concrete commands or checks.")
        for dep in feature.get("depends_on") or []:
            if dep not in known:
                problems.append(f"{fid}: depends_on '{dep}' does not exist: fix the id or remove it.")
        for tag in feature.get("certification") or []:
            if tag not in CERT_TAGS:
                problems.append(f"{fid}: certification tag '{tag}' is not allowed: use one of the tags in scripts/check_feature_list.py.")
    if len(in_progress) > 1:
        problems.append(
            f"more than one feature is in_progress ({', '.join(in_progress)}): finish one or mark the others blocked or not_started."
        )
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args(argv)
    path = args.root / "feature_list.json"
    try:
        data = json.loads(path.read_text())
    except FileNotFoundError:
        print(f"{path} not found: create it from the template.")
        return 1
    except json.JSONDecodeError as error:
        print(f"{path} is not valid JSON ({error}): fix the syntax.")
        return 1
    problems = validate(data)
    for problem in problems:
        print(problem)
    if problems:
        return 1
    print(f"feature_list.json OK ({len(data['features'])} features)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
