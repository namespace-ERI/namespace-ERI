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
START = "<!-- RESEARCH_STARS_START -->"
END = "<!-- RESEARCH_STARS_END -->"

def stars(repository: str) -> int:
    request = urllib.request.Request(f"https://api.github.com/repos/{repository}", headers={
        "Accept": "application/vnd.github+json", "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    with urllib.request.urlopen(request) as response:
        return int(json.load(response)["stargazers_count"])

def main() -> None:
    total = sum(stars(repository) for repository in REPOSITORIES)
    total_url = f"{total:,}".replace(",", "%2C")
    block = f'''{START}
<p>
  <img src="https://img.shields.io/badge/Research_repositories-{len(REPOSITORIES)}-0F766E?style=for-the-badge" alt="{len(REPOSITORIES)} research repositories" />
  <img src="https://img.shields.io/badge/Combined_stars-{total_url}-F59E0B?style=for-the-badge&logo=github&logoColor=white" alt="{total:,} combined stars" />
</p>
{END}'''
    readme = Path("README.md")
    updated, replacements = re.subn(rf"{re.escape(START)}.*?{re.escape(END)}", block, readme.read_text(), flags=re.DOTALL)
    if replacements != 1:
        raise RuntimeError("Could not find a unique research-star block")
    readme.write_text(updated)

if __name__ == "__main__":
    main()
