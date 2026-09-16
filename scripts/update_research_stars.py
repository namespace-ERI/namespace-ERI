#!/usr/bin/env python3
"""Refresh the combined-star badge in the profile README."""
import json
import os
import re
import urllib.request
from pathlib import Path

REPOSITORIES = (
    "VectorSpaceLab/AREX-Skill", "RUC-NLPIR/Arbor",
    "RUC-NLPIR/Awesome-Long-Horizon-Agents", "Shichun-Liu/Agent-Memory-Paper-List",
    "VincentZhao2002/OPOD", "ignorejjj/VeriGraph", "walkeralan123/MemoPilot",
    "RUC-NLPIR/ClawTrojan", "qhjqhj00/cabeza", "plageon/MemSifter",
)
def stars(repository: str) -> int:
    request = urllib.request.Request(f"https://api.github.com/repos/{repository}", headers={
        "Accept": "application/vnd.github+json", "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    with urllib.request.urlopen(request) as response:
        return int(json.load(response)["stargazers_count"])

def main() -> None:
    total = sum(stars(repository) for repository in REPOSITORIES)
    value = f"{total:,}"
    impact = Path("assets/research-impact.svg")
    content = impact.read_text()
    content, desc_count = re.subn(
        r"(<desc id=\"desc\">)[0-9,]+( repository stars)",
        rf"\g<1>{value}\2", content,
    )
    content, text_count = re.subn(
        r"(<text class=\"value\" x=\"51\" y=\"86\">)[0-9,]+(</text>)",
        rf"\g<1>{value}\2", content,
    )
    if desc_count != 1 or text_count != 1:
        raise RuntimeError("Could not find the research-star fields")
    impact.write_text(content)

    readme = Path("README.md")
    readme_content, alt_count = re.subn(
        r"(Research impact: )[0-9,]+( repository stars)",
        rf"\g<1>{value}\2", readme.read_text(),
    )
    if alt_count != 1:
        raise RuntimeError("Could not find the research-impact alt text")
    readme.write_text(readme_content)

if __name__ == "__main__":
    main()
