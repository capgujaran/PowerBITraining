# Power BI Learning Studio website

The no-sleep, static learning website for CA Pradeep Gujaran's Power BI programme.

## Commands

```bash
pnpm install
pnpm dev
pnpm test
```

The production output is Cloudflare Worker compatible. Course progress is stored only in the learner's browser; the site requires no database or environment variables.

Course content is generated from the repository-level `course_data.py`. Run `python scripts/sync_site_content.py` from the repository root after adding a lab or replacing a screenshot/download.
