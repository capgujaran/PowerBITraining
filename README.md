# Power BI Learning Studio

An interactive three-day Power BI learning programme for finance professionals, developed by CA Pradeep Gujaran. The repository now contains two front ends during the migration period:

- The original Streamlit app in `app.py`.
- The new static, no-sleep personal learning website in `site/`.

Both versions use the same course content, screenshots, lab packs and completed PBIX files.

## Run the static website

Node.js 22.13 or later is required.

```bash
cd site
pnpm install
pnpm dev
```

Open `http://localhost:3000`. A production check is available with:

```bash
pnpm test
```

The static website stores learner name, topic completion and assessment progress in browser local storage. It does not require a Python server, database or always-on paid service.

## Add a new lab

1. Add the new module entries, assessment questions and resource entries to `course_data.py`.
2. Add screenshots under `assets/screenshots` and downloads under `assets/downloads`.
3. Add each topic's screen walkthrough to `TOOL_LABS` in `course_data.py`.
4. Run `python scripts/sync_site_content.py` from the repository root.
5. Run `cd site` and `pnpm test` before deployment.

The website reads a generated `site/app/course-data.json`, so new labs automatically appear in the curriculum and Lab studio when their module records include `lab_group` and `lab_step`.

## Run the legacy Streamlit app

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```
