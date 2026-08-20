"""Export shared course data and assets to the static website.

Run from any working directory with:
    python scripts/sync_site_content.py
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"

sys.path.insert(0, str(ROOT))
import course_data  # noqa: E402


payload = {
    "schedule": course_data.SCHEDULE,
    "modules": course_data.MODULES,
    "assessment": course_data.ASSESSMENT,
    "resources": course_data.RESOURCES,
    "toolLabs": course_data.TOOL_LABS,
}

(SITE / "app" / "course-data.json").write_text(
    json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

for directory in ("screenshots", "downloads", "trainer"):
    shutil.copytree(
        ROOT / "assets" / directory,
        SITE / "public" / "assets" / directory,
        dirs_exist_ok=True,
    )

print(f"Synced {len(course_data.MODULES)} topics and {len(course_data.RESOURCES)} resources to {SITE}")
