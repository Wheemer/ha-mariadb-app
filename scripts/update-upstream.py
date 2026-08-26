#!/usr/bin/env python3
"""Update pinned MariaDB app dependencies and bump the app version."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DOCKERFILE = ROOT / "mariadb" / "Dockerfile"
CONFIG = ROOT / "mariadb" / "config.yaml"
CHANGELOG = ROOT / "mariadb" / "CHANGELOG.md"


def github_json(path: str):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "ha-app-updater"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(f"https://api.github.com/{path}", headers=headers), timeout=30) as response:
        return json.load(response)


def version_tuple(value: str) -> tuple[int, ...]:
    match = re.fullmatch(r"v?(\d+(?:\.\d+){2,3})", value)
    return tuple(map(int, match.group(1).split("."))) if match else ()


def latest_tag(repository: str) -> str:
    tags = github_json(f"repos/{repository}/tags?per_page=100")
    stable = [item["name"] for item in tags if version_tuple(item["name"])]
    return max(stable, key=version_tuple)


def bump_app_version() -> str:
    text = CONFIG.read_text(encoding="utf-8")
    match = re.search(r"^version:\s*(\d+)\.(\d+)\.(\d+)\s*$", text, re.MULTILINE)
    if not match:
        raise RuntimeError("Could not find app version in config.yaml")
    version = f"{match.group(1)}.{match.group(2)}.{int(match.group(3)) + 1}"
    CONFIG.write_text(text[: match.start()] + f"version: {version}" + text[match.end() :], encoding="utf-8")
    return version


parser = argparse.ArgumentParser()
parser.add_argument("--mariadb-version", required=True)
args = parser.parse_args()

dockerfile = DOCKERFILE.read_text(encoding="utf-8")
changes: list[str] = []

dependencies = [
    ("BASHIO_VERSION", latest_tag("hassio-addons/bashio")),
    ("S6_OVERLAY_VERSION", latest_tag("just-containers/s6-overlay").lstrip("v")),
    ("TEMPIO_VERSION", latest_tag("home-assistant/tempio").lstrip("v")),
]

for argument, latest in dependencies:
    current = re.search(rf"^ARG {argument}=(\S+)$", dockerfile, re.MULTILINE).group(1)
    if version_tuple(latest) > version_tuple(current):
        dockerfile = dockerfile.replace(f"ARG {argument}={current}", f"ARG {argument}={latest}")
        changes.append(f"{argument} {current} -> {latest}")

current_mariadb = re.search(r"mariadb-server=1:(\S+)", dockerfile).group(1)
if version_tuple(args.mariadb_version.split("-")[0]) > version_tuple(current_mariadb.split("-")[0]) or args.mariadb_version != current_mariadb:
    for package in ("mariadb-server", "mariadb-client", "mariadb-backup"):
        dockerfile = re.sub(rf"{package}=1:\S+", f"{package}=1:{args.mariadb_version}", dockerfile)
    changes.append(f"MariaDB packages {current_mariadb} -> {args.mariadb_version}")

if changes:
    DOCKERFILE.write_text(dockerfile, encoding="utf-8")
    version = bump_app_version()
    changelog = CHANGELOG.read_text(encoding="utf-8")
    entry = f"\n## {version}\n\n" + "\n".join(f"- {change}." for change in changes) + "\n"
    CHANGELOG.write_text(changelog.replace("# Changelog\n", "# Changelog\n" + entry, 1), encoding="utf-8")
else:
    version = re.search(r"^version:\s*(\S+)$", CONFIG.read_text(encoding="utf-8"), re.MULTILINE).group(1)

output = os.environ.get("GITHUB_OUTPUT")
if output:
    with open(output, "a", encoding="utf-8") as handle:
        handle.write(f"changed={'true' if changes else 'false'}\n")
        handle.write(f"version={version}\n")

print("; ".join(changes) if changes else "Pinned upstream releases are current.")
