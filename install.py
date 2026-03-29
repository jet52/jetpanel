#!/usr/bin/env python3
"""Cross-platform installer for the jetpanel skill."""

import shutil
from pathlib import Path

SKILL_NAME = "jetpanel"
SCRIPT_DIR = Path(__file__).resolve().parent
INSTALL_DIR = Path.home() / ".claude" / "skills" / SKILL_NAME


def main():
    version_file = SCRIPT_DIR / "VERSION"
    version = version_file.read_text().strip() if version_file.exists() else "unknown"
    print(f"Installing {SKILL_NAME} skill v{version}...")

    # If install dir is a symlink (e.g., from dev setup), remove it first
    if INSTALL_DIR.is_symlink():
        INSTALL_DIR.unlink()

    # Clean and recreate target directory
    if INSTALL_DIR.exists():
        shutil.rmtree(INSTALL_DIR)

    # Copy skill directory wholesale
    skill_src = SCRIPT_DIR / "skill"
    shutil.copytree(skill_src, INSTALL_DIR)

    # Copy VERSION
    shutil.copy2(version_file, INSTALL_DIR / "VERSION")

    print(f"Installed to {INSTALL_DIR}")

    # Check for jetmemo (optional integration)
    jetmemo_dir = Path.home() / ".claude" / "skills" / "jetmemo"
    if jetmemo_dir.exists():
        print(f"jetmemo skill found at {jetmemo_dir} — integration available.")
    else:
        print("jetmemo skill not found — standalone mode only.")

    # Check for ~/refs/ (optional but improves authority lookup)
    refs_dir = Path.home() / "refs"
    if refs_dir.is_dir():
        print(f"~/refs/ directory found — local authority lookup available.")
    else:
        print("~/refs/ not found — will use web lookups for authority.")

    print("Done.")


if __name__ == "__main__":
    main()
