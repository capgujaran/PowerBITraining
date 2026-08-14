from __future__ import annotations

from datetime import date
from pathlib import Path
import math
import random

import pandas as pd
import streamlit as st
from PIL import Image

from course_data import ASSESSMENT, MODULES, RESOURCES, SCHEDULE, TOOL_LABS


APP_DIR = Path(__file__).parent
DOWNLOAD_DIR = APP_DIR / "assets" / "downloads"
SCREENSHOT_DIR = APP_DIR / "assets" / "screenshots"
PASS_SCORE = 14

st.set_page_config(
    page_title="Power BI Learning Studio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Libre+Baskerville:wght@400;700&display=swap');
        :root { --ink:#0c1b24; --ink-2:#132b37; --muted:#65737a; --gold:#c99652; --yellow:#f2c811; --cream:#f7f1e6; --line:#dce2df; --teal:#177c72; --surface:#ffffff; }
        * { box-sizing:border-box; }
        html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
        h1,h2,h3 { font-family:'Libre Baskerville',Georgia,serif !important; letter-spacing:-.035em; color:var(--ink); }
        .stApp { background:#f3f5f3; color:var(--ink); }
        [data-testid="stSidebar"] { background:var(--ink); border-right:1px solid rgba(255,255,255,.08); }
        [data-testid="stSidebar"] * { color:#f8f9fc; }
        [data-testid="stSidebar"] hr { border-color:rgba(255,255,255,.15); }
        [data-testid="stSidebar"] .stRadio label { padding:.68rem .78rem; margin:.14rem 0; border-radius:5px; transition:.18s ease; }
        [data-testid="stSidebar"] .stRadio label:hover { background:rgba(255,255,255,.05); }
        [data-testid="stSidebar"] .stRadio label:has(input:checked) { background:#1d3b45; box-shadow:inset 3px 0 var(--gold); }
        [data-testid="stSidebar"] .stTextInput input { background:#142d38; border-color:#294650; color:white; border-radius:6px; }
        .block-container { max-width:1440px; padding:3rem clamp(1.4rem,4vw,4.5rem) 5rem; }
        .sidebar-brand { display:flex; align-items:center; gap:.8rem; margin:.15rem .15rem 1rem; }
        .sidebar-brand__mark { width:48px; height:48px; display:flex; align-items:flex-end; justify-content:center; gap:3px; padding:9px 8px; background:var(--gold); clip-path:polygon(50% 0,100% 20%,100% 80%,50% 100%,0 80%,0 20%); }
        .sidebar-brand__mark i { display:block; width:7px; border-radius:2px 2px 0 0; background:var(--ink); }
        .sidebar-brand__mark i:nth-child(1){height:12px}.sidebar-brand__mark i:nth-child(2){height:20px}.sidebar-brand__mark i:nth-child(3){height:28px}
        .sidebar-brand strong,.sidebar-brand span { display:block; }
        .sidebar-brand strong { font-family:'Libre Baskerville'; font-size:1rem; color:white; }
        .sidebar-brand span { color:#96aaa8; margin-top:.18rem; font-size:.63rem; letter-spacing:.11em; text-transform:uppercase; }
        .eyebrow { display:block; color:var(--teal); font-size:.69rem; letter-spacing:.16em; text-transform:uppercase; font-weight:800; margin-bottom:.55rem; }
        .page-intro { display:flex; justify-content:space-between; align-items:flex-end; gap:2rem; margin-bottom:2rem; }
        .page-intro h1 { font-size:clamp(2.15rem,3vw,3.15rem); margin:.1rem 0 .6rem; line-height:1.14; }
        .page-intro p { color:var(--muted); max-width:820px; margin:0; line-height:1.65; }
        .hero { min-height:330px; display:grid; grid-template-columns:1.2fr .8fr; align-items:center; gap:2rem; background:radial-gradient(circle at 82% 28%,rgba(72,150,139,.3),transparent 32%),linear-gradient(135deg,#102933,var(--ink)); color:white; padding:3.4rem 4rem; border-radius:10px; overflow:hidden; position:relative; box-shadow:0 14px 38px rgba(12,27,36,.13); }
        .hero h1 { color:white; font-size:clamp(2.25rem,4vw,3.75rem); max-width:820px; margin:.55rem 0 1rem; line-height:1.08; }
        .hero p { color:#c0cecd; max-width:720px; font-size:1.04rem; line-height:1.7; margin:0; }
        .hero .pill { display:inline-block; padding:.34rem .58rem; border:1px solid rgba(255,255,255,.15); color:#d9e4e0; border-radius:4px; font-weight:700; font-size:.66rem; letter-spacing:.08em; margin-right:.35rem; }
        .journey-wheel { width:230px; height:230px; position:relative; border:1px solid rgba(255,255,255,.15); border-radius:50%; margin:auto; }
        .journey-wheel:after { content:''; position:absolute; inset:35px; border:1px dashed rgba(255,255,255,.15); border-radius:50%; }
        .journey-wheel__center { position:absolute; inset:72px; display:grid; place-content:center; text-align:center; background:#183743; border-radius:50%; z-index:2; }
        .journey-wheel__center strong { font-family:'Libre Baskerville'; font-size:2rem; color:white; }
        .journey-wheel__center span { color:#9bb1b1; font-size:.58rem; text-transform:uppercase; letter-spacing:.1em; }
        .journey-node { --angle:0deg; position:absolute; left:50%; top:50%; width:42px; height:42px; margin:-21px; display:grid; place-items:center; border-radius:50%; background:#1b3a44; border:2px solid var(--gold); color:white; font-size:.68rem; font-weight:800; transform:rotate(var(--angle)) translateY(-115px) rotate(calc(-1 * var(--angle))); z-index:3; }
        .metric-row { display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; margin:1.2rem 0 1.8rem; }
        .metric-card,.content-card { position:relative; background:white; border:1px solid #e4e8e5; border-radius:8px; padding:1.2rem 1.2rem 1.15rem 1.45rem; }
        .metric-card:before { content:''; position:absolute; left:0; top:0; bottom:0; width:5px; background:var(--teal); border-radius:8px 0 0 8px; }
        .metric-card:nth-child(2):before { background:var(--gold); }.metric-card:nth-child(3):before { background:#467d9d; }.metric-card:nth-child(4):before { background:#735a8b; }
        .metric-card strong { display:block; font-family:'Libre Baskerville'; font-size:1.55rem; color:var(--ink); }
        .metric-card span { color:var(--muted); font-size:.75rem; }
        .module-head { background:white; color:var(--ink); padding:2.2rem 2.5rem; border:1px solid #e0e5e2; border-radius:9px; margin-bottom:1.2rem; box-shadow:0 10px 28px rgba(23,41,51,.05); }
        .module-head h1 { color:var(--ink); margin:.7rem 0 .45rem; }
        .module-head p { color:var(--muted); margin:0; }
        .concept { border-left:3px solid var(--gold); background:white; padding:1.15rem 1.25rem; border-radius:0 8px 8px 0; margin:.8rem 0; border-block:1px solid #e8ece9; border-right:1px solid #e8ece9; }
        .concept h4 { margin:0 0 .35rem; color:var(--ink); }
        .example { color:#455b62; background:#f6f8f6; padding:.72rem .82rem; border-radius:6px; margin:.7rem 0; }
        .remember { color:#8a642f; font-weight:700; font-size:.86rem; }
        .lab { background:linear-gradient(155deg,#f3faf8,#fff); border:1px solid #bcd6cf; border-radius:8px; padding:1.3rem; }
        .badge { display:inline-block; background:#edf3f1; color:#3e625e; border-radius:4px; padding:.3rem .55rem; font-size:.7rem; font-weight:700; margin-right:.3rem; }
        .day-card { height:100%; background:white; border:1px solid var(--line); border-radius:8px; padding:1.35rem; border-top:4px solid var(--gold); transition:.2s ease; }
        .day-card:hover { transform:translateY(-3px); box-shadow:0 10px 28px rgba(23,41,51,.08); }
        .day-card h3 { margin:.3rem 0; }
        .day-card p { color:var(--muted); min-height:72px; }
        .credit { text-align:center; color:#8e97aa; font-size:.82rem; padding-top:2rem; }
        .certificate { background:#fffdf5; border:9px double var(--gold); padding:3rem; text-align:center; border-radius:4px; }
        .certificate .name { font-family:'Libre Baskerville'; color:var(--ink); font-size:2rem; border-bottom:1px solid #d9d1ad; display:inline-block; padding:0 2rem .4rem; }
        .small-note { color:var(--muted); font-size:.85rem; }
        .screen-note { background:#edf7f1; border:1px solid #c9ded4; border-radius:7px; padding:.9rem 1rem; margin:.7rem 0 1rem; }
        .screen-note b { color:var(--ink); }
        .tool-path { background:white; border:1px solid var(--line); border-radius:8px; padding:1.15rem 1.3rem; }
        .merge-flow { display:grid; grid-template-columns:1fr auto 1fr; align-items:center; gap:1rem; margin:.7rem 0 1.2rem; }
        .merge-source { background:white; border:1px solid #dfe4ef; border-radius:8px; padding:.95rem 1rem; }
        .merge-source.primary { border-left:7px solid #f2c811; }
        .merge-source.secondary { border-right:7px solid #4d8fe8; }
        .merge-source b { display:block; color:#0b1739; font-size:1.02rem; }
        .merge-source span { color:#64708b; font-size:.84rem; }
        .merge-arrows { text-align:center; color:#0b1739; font-weight:800; line-height:1.35; }
        .merge-arrows .arrow { color:#d3a800; font-size:1.6rem; letter-spacing:.08rem; }
        .merge-legend { display:flex; flex-wrap:wrap; gap:.55rem 1rem; margin:.4rem 0 1rem; color:#47536e; font-size:.86rem; }
        .legend-dot { display:inline-block; width:.75rem; height:.75rem; border-radius:3px; margin-right:.3rem; vertical-align:-.05rem; }
        .merge-callout { background:radial-gradient(circle at 88% 20%,rgba(72,150,139,.28),transparent 35%),linear-gradient(135deg,#102933,var(--ink)); color:white; padding:1.25rem 1.4rem; border-radius:9px; margin:.8rem 0 1.2rem; }
        .merge-callout b { color:#e1b978; }
        .retained-chart { display:flex; flex-direction:column; gap:1rem; background:white; border:1px solid var(--line); border-radius:8px; padding:1.15rem; min-height:250px; justify-content:center; }
        .retained-row__label { display:flex; justify-content:space-between; gap:1rem; color:#53656b; font-size:.74rem; font-weight:700; margin-bottom:.4rem; }
        .retained-row__label b { color:var(--ink); font-family:'Libre Baskerville'; font-size:.9rem; }
        .retained-track { height:13px; overflow:hidden; background:#edf0ee; border-radius:3px; }
        .retained-track span { display:block; height:100%; min-width:0; border-radius:3px; transition:width .25s ease; }
        div[data-testid="stProgress"] > div > div > div { background-color:var(--gold); }
        .stButton > button, .stDownloadButton > button { border-radius:6px; border:1px solid var(--line); font-weight:700; min-height:42px; }
        .stButton > button:hover, .stDownloadButton > button:hover { border-color:var(--teal); color:var(--teal); }
        .stButton > button[kind="primary"] { background:var(--teal); color:white; border-color:var(--teal); box-shadow:0 7px 18px rgba(23,124,114,.18); }
        .stTabs [data-baseweb="tab-list"] { gap:.25rem; background:white; border:1px solid var(--line); border-radius:7px; padding:.25rem; }
        .stTabs [data-baseweb="tab"] { border-radius:5px; padding:.55rem .9rem; }
        .stTabs [aria-selected="true"] { background:#eaf3f1; color:var(--teal); }
        div[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:7px; overflow:hidden; }
        div[data-baseweb="select"] > div, .stTextInput input, .stNumberInput input { border-radius:6px; }
        div[data-testid="stAlert"] { border-radius:7px; }
        @media(max-width:900px){.hero{grid-template-columns:1fr;padding:2.6rem}.journey-wheel{display:none}.metric-row{grid-template-columns:repeat(2,1fr)}.merge-flow{grid-template-columns:1fr}.merge-arrows{transform:rotate(90deg);padding:.25rem}}
        @media(max-width:560px){.metric-row{grid-template-columns:1fr}.block-container{padding:4.5rem 1rem 3rem}.hero{padding:2rem 1.35rem}.page-intro{display:block}.page-intro h1{font-size:2rem}}
        </style>
        """,
        unsafe_allow_html=True,
    )


def setup_state() -> None:
    defaults = {
        "learner_name": "",
        "completed": set(),
        "quiz_result": None,
        "nav": "Learning home",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def progress_value() -> float:
    return len(st.session_state.completed) / len(MODULES)


def sidebar() -> str:
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
              <div class="sidebar-brand__mark"><i></i><i></i><i></i></div>
              <div><strong>Power BI</strong><span>Learning Studio</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption("3-day programme · 10:00 AM–4:00 PM · Dubai")
        st.divider()
        name = st.text_input("Learner name", value=st.session_state.learner_name, placeholder="Enter your name")
        st.session_state.learner_name = name.strip()
        pct = int(progress_value() * 100)
        st.progress(progress_value(), text=f"Course progress · {pct}%")
        result = st.session_state.quiz_result
        if result is not None:
            st.caption(f"Assessment · {result}/20")
        pages = ["Learning home", "Curriculum", "Three-day plan", "Interactive lab", "Assessment", "Resources", "Certificate"]
        page = st.radio("Explore", pages, label_visibility="collapsed", key="nav")
        st.divider()
        st.caption("Developed by CA Pradeep Gujaran")
    return page


def page_header(kicker: str, title: str, copy: str) -> None:
    st.markdown(
        f'<div class="page-intro"><div><span class="eyebrow">{kicker}</span><h1>{title}</h1><p>{copy}</p></div></div>',
        unsafe_allow_html=True,
    )


def home() -> None:
    learner = st.session_state.learner_name or "CA learner"
    st.markdown(
        f"""
        <div class="hero">
          <div>
            <span class="pill">3 DAYS</span><span class="pill">18 CONTACT HOURS</span><span class="pill">12 MODULES</span>
            <h1>Power BI for finance, reporting and audit analytics</h1>
            <p>Welcome, {learner}. Move from raw files to a governed, decision-ready Power BI solution through guided concepts, visual laboratories, downloadable practice files and a management capstone.</p>
          </div>
          <div class="journey-wheel" aria-label="Three-day learning pathway">
            <div class="journey-wheel__center"><strong>3</strong><span>learning days</span></div>
            <span class="journey-node" style="--angle:0deg">D1</span>
            <span class="journey-node" style="--angle:120deg">D2</span>
            <span class="journey-node" style="--angle:240deg">D3</span>
          </div>
        </div>
        <div class="metric-row">
          <div class="metric-card"><strong>10–4</strong><span>Daily workshop timing</span></div>
          <div class="metric-card"><strong>12</strong><span>Guided learning modules</span></div>
          <div class="metric-card"><strong>11</strong><span>Downloadable lab resources</span></div>
          <div class="metric-card"><strong>70%</strong><span>Assessment pass mark</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.subheader("The learning journey")
    cols = st.columns(3)
    for col, item in zip(cols, SCHEDULE):
        with col:
            st.markdown(
                f'<div class="day-card"><span class="eyebrow">Day {item["day"]} · Modules {item["modules"]}</span><h3>{item["theme"]}</h3><p>{item["focus"]}</p><span class="badge">10:00 AM–4:00 PM</span></div>',
                unsafe_allow_html=True,
            )
    st.info("Start with **Curriculum** for the guided learning path. Use **Interactive lab** to test each idea, then complete the assessment and unlock your certificate.")


def module_card(module: dict) -> None:
    completed = module["id"] in st.session_state.completed
    status = "✓ Complete" if completed else "Start module"
    st.markdown(f"**{module['code']} · {module['title']}**  \n{module['subtitle']}  \n`{module['duration']}` · `{status}`")


def curriculum() -> None:
    page_header("Guided pathway", "Curriculum", "Twelve modules combine explanation, practical examples, guided labs and quick knowledge checks.")
    day_filter = st.segmented_control("Day", ["All", "Day 1", "Day 2", "Day 3"], default="All")
    filtered = MODULES if day_filter == "All" else [m for m in MODULES if m["day"] == int(day_filter[-1])]
    options = {f"{m['code']} · {m['title']}": m for m in filtered}
    for d in sorted({m["day"] for m in filtered}):
        with st.expander(f"Day {d} · {SCHEDULE[d-1]['theme']}", expanded=True):
            for m in [x for x in filtered if x["day"] == d]:
                module_card(m)
    selected_label = st.selectbox("Open a module", list(options))
    show_module(options[selected_label])


def show_module(module: dict) -> None:
    st.markdown(
        f'<div class="module-head"><span class="badge">{module["code"]}</span><span class="badge">Day {module["day"]}</span><span class="badge">{module["duration"]}</span><h1>{module["title"]}</h1><p>{module["subtitle"]}</p></div>',
        unsafe_allow_html=True,
    )
    left, right = st.columns([1.9, 1])
    with left:
        st.subheader("Learning outcomes")
        for outcome in module["outcomes"]:
            st.markdown(f"- {outcome}")
        st.subheader("Concept guide")
        for title, explanation, example, remember in module["concepts"]:
            st.markdown(
                f'<div class="concept"><h4>{title}</h4><div>{explanation}</div><div class="example"><b>Worked example</b><br>{example}</div><div class="remember">Remember · {remember}</div></div>',
                unsafe_allow_html=True,
            )
    with right:
        title, dataset, steps, deliverable = module["lab"]
        steps_html = "".join(f"<li>{s}</li>" for s in steps)
        st.markdown(f'<div class="lab"><div class="eyebrow">Guided lab</div><h3>{title}</h3><p><b>Dataset</b><br>{dataset}</p><ol>{steps_html}</ol><p><b>Deliverable</b><br>{deliverable}</p></div>', unsafe_allow_html=True)
        st.subheader("Knowledge check")
        question, choices, answer, explanation = module["check"]
        choice = st.radio(question, choices, index=None, key=f"check_{module['id']}")
        if st.button("Check answer", key=f"check_btn_{module['id']}"):
            if choice is None:
                st.warning("Choose an answer first.")
            elif choices.index(choice) == answer:
                st.success(f"Correct. {explanation}")
            else:
                st.error(f"Not quite. {explanation}")
        completed = module["id"] in st.session_state.completed
        if st.button("Mark as incomplete" if completed else "Mark module complete", type="primary", key=f"complete_{module['id']}"):
            updated = set(st.session_state.completed)
            updated.discard(module["id"]) if completed else updated.add(module["id"])
            st.session_state.completed = updated
            st.rerun()


def three_day_plan() -> None:
    page_header("Workshop rhythm", "Three-day plan", "Each day balances demonstration, guided practice, review and a deliverable that feeds the final capstone.")
    daily = [
        ("10:00–10:20", "Launch and retrieval practice", "Reconnect yesterday's ideas to today's business question."),
        ("10:20–11:30", "Concept and demonstration", "See the workflow performed with a finance example."),
        ("11:30–11:45", "Break", "Short reset."),
        ("11:45–1:00", "Guided lab", "Build the technique with checkpoints and reconciliation."),
        ("1:00–1:45", "Lunch", "Break."),
        ("1:45–3:15", "Applied challenge", "Use the technique in a less-structured business scenario."),
        ("3:15–3:30", "Break", "Short reset."),
        ("3:30–4:00", "Review and handoff", "Knowledge check, reflection and capstone progress."),
    ]
    for item in SCHEDULE:
        st.subheader(f"Day {item['day']} · {item['theme']}")
        st.caption(item["focus"])
        rows = []
        for time, activity, purpose in daily:
            rows.append({"Time": time, "Activity": activity, "Purpose": purpose})
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)


def show_course_image(path: Path, caption: str) -> None:
    """Show screenshots without enlarging small source images into a blur."""
    with Image.open(path) as source:
        source_width = source.width
    st.image(str(path), caption=caption, width=min(source_width, 1000))
    if source_width < 720:
        st.caption("Shown at its original width to preserve clarity. Use fullscreen to inspect the source capture.")


def merge_venn(join_type: str) -> str:
    highlights = {
        "Left Outer": '<circle cx="275" cy="150" r="120" fill="#f2c811" fill-opacity=".88"/>',
        "Right Outer": '<circle cx="445" cy="150" r="120" fill="#4d8fe8" fill-opacity=".82"/>',
        "Full Outer": '<circle cx="275" cy="150" r="120" fill="#f2c811" fill-opacity=".78"/><circle cx="445" cy="150" r="120" fill="#4d8fe8" fill-opacity=".68"/>',
        "Inner": '<circle cx="275" cy="150" r="120" fill="#19a39b" clip-path="url(#right-circle)"/>',
        "Left Anti": '<circle cx="275" cy="150" r="120" fill="#f2c811" mask="url(#left-only)"/>',
        "Right Anti": '<circle cx="445" cy="150" r="120" fill="#4d8fe8" mask="url(#right-only)"/>',
    }
    descriptions = {
        "Left Outer": "Primary only + matched rows",
        "Right Outer": "Matched rows + secondary only",
        "Full Outer": "Every key from both tables",
        "Inner": "Matched rows only",
        "Left Anti": "Primary rows with no match",
        "Right Anti": "Secondary rows with no match",
    }
    included = {
        "Left Outer": {"left", "match"},
        "Right Outer": {"match", "right"},
        "Full Outer": {"left", "match", "right"},
        "Inner": {"match"},
        "Left Anti": {"left"},
        "Right Anti": {"right"},
    }[join_type]
    segment_style = lambda name: "font-weight:800;fill:#0b1739" if name in included else "fill:#9aa3b6"
    return f"""
    <div style="font-family:DM Sans,Arial,sans-serif;background:#fff;border:1px solid #dce2df;border-radius:9px;padding:8px 12px;box-shadow:0 8px 24px rgba(12,27,36,.05)">
      <svg viewBox="0 0 720 330" style="display:block;width:100%;height:auto" role="img" aria-label="{join_type} join diagram">
        <defs>
          <clipPath id="right-circle"><circle cx="445" cy="150" r="120"/></clipPath>
          <mask id="left-only"><rect width="720" height="330" fill="white"/><circle cx="445" cy="150" r="120" fill="black"/></mask>
          <mask id="right-only"><rect width="720" height="330" fill="white"/><circle cx="275" cy="150" r="120" fill="black"/></mask>
          <marker id="arrowhead" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#0b1739"/></marker>
        </defs>
        <text x="360" y="25" text-anchor="middle" style="font-size:19px;font-weight:800;fill:#0b1739">{join_type}: {descriptions[join_type]}</text>
        <circle cx="275" cy="150" r="120" fill="#f2f4f8" stroke="#0b1739" stroke-width="3"/>
        <circle cx="445" cy="150" r="120" fill="#f2f4f8" stroke="#0b1739" stroke-width="3"/>
        {highlights[join_type]}
        <circle cx="275" cy="150" r="120" fill="none" stroke="#0b1739" stroke-width="3"/>
        <circle cx="445" cy="150" r="120" fill="none" stroke="#0b1739" stroke-width="3"/>
        <text x="215" y="132" text-anchor="middle" style="font-size:16px;{segment_style('left')}"><tspan x="215">Primary</tspan><tspan x="215" dy="19">only</tspan><tspan x="215" dy="21" style="font-size:13px">C01, C05</tspan></text>
        <text x="360" y="143" text-anchor="middle" style="font-size:14px;{segment_style('match')}"><tspan x="360">Matched</tspan><tspan x="360" dy="21" style="font-size:12px">C02–C04</tspan></text>
        <text x="505" y="132" text-anchor="middle" style="font-size:16px;{segment_style('right')}"><tspan x="505">Secondary</tspan><tspan x="505" dy="19">only</tspan><tspan x="505" dy="21" style="font-size:13px">C06, C07</tspan></text>
        <path d="M185 280 C185 250,205 238,225 224" fill="none" stroke="#0b1739" stroke-width="2" marker-end="url(#arrowhead)"/>
        <path d="M360 280 L360 226" fill="none" stroke="#0b1739" stroke-width="2" marker-end="url(#arrowhead)"/>
        <path d="M535 280 C535 250,515 238,495 224" fill="none" stroke="#0b1739" stroke-width="2" marker-end="url(#arrowhead)"/>
        <text x="185" y="305" text-anchor="middle" style="font-size:14px;{segment_style('left')}">{'KEPT' if 'left' in included else 'EXCLUDED'}</text>
        <text x="360" y="305" text-anchor="middle" style="font-size:14px;{segment_style('match')}">{'KEPT' if 'match' in included else 'EXCLUDED'}</text>
        <text x="535" y="305" text-anchor="middle" style="font-size:14px;{segment_style('right')}">{'KEPT' if 'right' in included else 'EXCLUDED'}</text>
      </svg>
    </div>
    """


def merge_result(join_type: str, primary: pd.DataFrame, secondary: pd.DataFrame) -> pd.DataFrame:
    how = {
        "Left Outer": "left",
        "Right Outer": "right",
        "Full Outer": "outer",
        "Inner": "inner",
        "Left Anti": "outer",
        "Right Anti": "outer",
    }[join_type]
    result = primary.merge(secondary, on="CustomerKey", how=how, indicator=True)
    if join_type == "Left Anti":
        result = result[result["_merge"] == "left_only"]
    elif join_type == "Right Anti":
        result = result[result["_merge"] == "right_only"]
    result["Match Status"] = result["_merge"].astype(str).map(
        {"left_only": "Primary only", "both": "Matched", "right_only": "Secondary only"}
    )
    result = result.sort_values("CustomerKey").drop(columns="_merge").reset_index(drop=True)
    return result


def merge_row_style(row: pd.Series) -> list[str]:
    colors = {
        "Primary only": "background-color:#fff3b0;color:#0b1739",
        "Matched": "background-color:#dff5ec;color:#0b1739",
        "Secondary only": "background-color:#e6f0ff;color:#0b1739",
    }
    return [colors.get(row.get("Match Status"), "") for _ in row]


def detailed_merge_lab() -> None:
    st.markdown(
        '<div class="merge-callout"><b>Interactive Merge Queries laboratory</b><br>Change the join kind below. The highlighted Venn regions, retained row groups, output count, result preview and Power Query formula all update together.</div>',
        unsafe_allow_html=True,
    )
    join_types = ["Left Outer", "Right Outer", "Full Outer", "Inner", "Left Anti", "Right Anti"]
    join_type = st.selectbox("Merge type", join_types, key="merge_join_type")

    st.markdown(
        """
        <div class="merge-flow">
          <div class="merge-source primary"><b>① Primary table · Sales Orders</b><span>First table selected in Merge Queries · key: CustomerKey</span></div>
          <div class="merge-arrows"><div class="arrow">→ ↔ ←</div>compare keys<br><span style="font-size:.72rem;color:#64708b">then retain rows</span></div>
          <div class="merge-source secondary"><b>② Secondary table · Customer Master</b><span>Second table selected in Merge Queries · key: CustomerKey</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    primary = pd.DataFrame(
        {
            "OrderID": ["SO-1001", "SO-1002", "SO-1003", "SO-1004", "SO-1005"],
            "CustomerKey": ["C01", "C02", "C03", "C04", "C05"],
            "NetAmount": [4200, 7800, 3150, 9600, 2750],
        }
    )
    secondary = pd.DataFrame(
        {
            "CustomerKey": ["C02", "C03", "C04", "C06", "C07"],
            "CustomerName": ["Desert Retail", "Marina Foods", "Creek Trading", "Oasis Services", "Falcon Stores"],
            "Segment": ["Retail", "Hospitality", "Wholesale", "Services", "Retail"],
        }
    )
    primary_view = primary.copy()
    primary_view["Match Status"] = primary_view["CustomerKey"].map(
        lambda key: "Matched" if key in set(secondary["CustomerKey"]) else "Primary only"
    )
    secondary_view = secondary.copy()
    secondary_view["Match Status"] = secondary_view["CustomerKey"].map(
        lambda key: "Matched" if key in set(primary["CustomerKey"]) else "Secondary only"
    )
    left, right = st.columns(2)
    with left:
        st.markdown("#### Primary table · Sales Orders")
        st.dataframe(primary_view.style.apply(merge_row_style, axis=1), hide_index=True, use_container_width=True)
    with right:
        st.markdown("#### Secondary table · Customer Master")
        st.dataframe(secondary_view.style.apply(merge_row_style, axis=1), hide_index=True, use_container_width=True)

    st.markdown(
        '<div class="merge-legend"><span><i class="legend-dot" style="background:#fff3b0"></i>Primary only</span><span><i class="legend-dot" style="background:#dff5ec"></i>Matched key in both tables</span><span><i class="legend-dot" style="background:#e6f0ff"></i>Secondary only</span></div>',
        unsafe_allow_html=True,
    )

    result = merge_result(join_type, primary, secondary)
    kept_groups = result["Match Status"].value_counts()
    explanations = {
        "Left Outer": "Keep every Sales Orders row. Bring Customer Master attributes where the key matches; C01 and C05 receive null customer attributes.",
        "Right Outer": "Keep every Customer Master row. Bring Sales Orders fields where the key matches; C06 and C07 have no order fields.",
        "Full Outer": "Keep every key from both tables. This is useful for reconciliation because both types of exception remain visible.",
        "Inner": "Keep only keys found in both tables: C02, C03 and C04. Every unmatched row is removed.",
        "Left Anti": "Return Sales Orders keys with no Customer Master match: C01 and C05. This is the standard exceptions query for unmapped transactions.",
        "Right Anti": "Return Customer Master keys with no Sales Orders match: C06 and C07. This identifies unused master records in this sample.",
    }
    m_names = {
        "Left Outer": "JoinKind.LeftOuter",
        "Right Outer": "JoinKind.RightOuter",
        "Full Outer": "JoinKind.FullOuter",
        "Inner": "JoinKind.Inner",
        "Left Anti": "JoinKind.LeftAnti",
        "Right Anti": "JoinKind.RightAnti",
    }

    st.markdown(f"### ③ Live result · {join_type}")
    st.markdown(merge_venn(join_type), unsafe_allow_html=True)
    st.info(explanations[join_type])
    metric_cols = st.columns(4)
    metric_cols[0].metric("Primary rows", len(primary))
    metric_cols[1].metric("Secondary rows", len(secondary))
    metric_cols[2].metric("Matched keys", 3)
    metric_cols[3].metric("Output rows", len(result))

    chart_col, output_col = st.columns([.8, 1.5])
    with chart_col:
        st.markdown("#### Rows retained by group")
        retained_specs = [
            ("Primary only", "#f2c811"),
            ("Matched", "#177c72"),
            ("Secondary only", "#4d8fe8"),
        ]
        retained_html = "".join(
            f'<div class="retained-row"><div class="retained-row__label"><span>{group}</span><b>{int(kept_groups.get(group, 0))}</b></div><div class="retained-track"><span style="width:{int(kept_groups.get(group, 0)) / 3 * 100:.0f}%;background:{color}"></span></div></div>'
            for group, color in retained_specs
        )
        st.markdown(f'<div class="retained-chart">{retained_html}</div>', unsafe_allow_html=True)
    with output_col:
        st.markdown("#### Expanded output preview")
        display_result = result.copy()
        display_result["NetAmount"] = display_result["NetAmount"].map(lambda value: "—" if pd.isna(value) else f"AED {value:,.0f}")
        display_result = display_result.fillna("—")
        st.dataframe(display_result.style.apply(merge_row_style, axis=1), hide_index=True, use_container_width=True)

    st.markdown("#### Power Query translation")
    st.code(
        f'Merged = Table.NestedJoin(SalesOrders, {{"CustomerKey"}}, CustomerMaster, {{"CustomerKey"}}, "Customer", {m_names[join_type]})',
        language="powerquery",
    )
    if "Anti" in join_type:
        st.caption("Anti joins are exception tests: they return non-matching rows from one side. There is normally nothing useful to expand from the other table.")
    else:
        st.caption("After the merge, select the expand icon on the new Customer column and keep only the attributes required for analysis.")


def interactive_lab() -> None:
    page_header("See it, then build it", "Power BI guided lab", "Choose a topic to study the relevant Power BI screen, follow the exact click path and reproduce the technique in the supplied practice file.")
    labels = {f"{m['code']} · {m['title']}": m for m in MODULES}
    selected = labels[st.selectbox("Interactive example", list(labels))]
    st.markdown(f"### {selected['title']}")
    lab_id = selected["id"]
    guide = TOOL_LABS[lab_id]
    if lab_id == 4:
        detailed_merge_lab()
        st.divider()
        st.subheader("Power BI screen reference")
        st.caption("The live vector lab above carries the detailed explanation; these source captures show where the commands appear in Power Query.")
    st.subheader(guide["screen_title"])
    screen_tabs = st.tabs([screen[0] for screen in guide["screens"]]) if len(guide["screens"]) > 1 else [st.container()]
    for tab, (label, filename, caption, notices) in zip(screen_tabs, guide["screens"]):
        with tab:
            path = SCREENSHOT_DIR / filename
            if path.exists():
                show_course_image(path, caption)
            else:
                st.warning(f"Course screenshot unavailable: {label}")
            notice_html = "".join(f"<li>{item}</li>" for item in notices)
            st.markdown(f'<div class="screen-note"><b>What to notice in this screen</b><ul>{notice_html}</ul></div>', unsafe_allow_html=True)

    path_html = "".join(f"<li>{step}</li>" for step in guide["click_path"])
    st.markdown(f'<div class="tool-path"><div class="eyebrow">Follow in Power BI</div><ol>{path_html}</ol><p><b>Student task</b><br>{guide["task"]}</p><p><b>Evidence to produce</b><br>{guide["evidence"]}</p></div>', unsafe_allow_html=True)
    reproduced = st.checkbox("I reproduced this screen or technique in Power BI Desktop", key=f"reproduced_{lab_id}")
    if reproduced:
        st.success("Practice recorded for this session. Compare your result with the screenshot and the evidence checklist above.")
    evidence_file = st.file_uploader("Optional: add a screenshot of your own completed work for self-review", type=["png", "jpg", "jpeg"], key=f"lab_evidence_{lab_id}")
    if evidence_file:
        st.image(evidence_file, caption="Your practice evidence", width="stretch")
    st.divider()
    st.subheader("Check your understanding")
    if lab_id == 1:
        question = st.text_input("Rewrite the business request", "Show me sales")
        grain = st.selectbox("Row grain", ["Invoice line", "Invoice header", "Monthly country total"])
        action = st.selectbox("Decision", ["Investigate margin shortfall", "Approve budget", "Review customer concentration"])
        st.success(f"Decision-ready framing: **At {grain.lower()} level, which drivers should management examine to {action.lower()}?**")
        st.caption(f"Original request: {question}")
    elif lab_id == 2:
        rows = st.slider("Estimated rows", 10_000, 10_000_000, 250_000, 10_000)
        realtime = st.toggle("Near-real-time visibility is essential")
        governed = st.toggle("Source is a governed analytical database")
        recommendation = "Consider DirectQuery and test performance" if rows > 2_000_000 and realtime and governed else "Import is the sensible starting point"
        st.metric("Recommended starting mode", recommendation)
    elif lab_id == 3:
        data = pd.DataFrame({"Account": ["4000", " 5000", "6000"], "Amount": ["1,250.00", "N/A", "875.50"], "Month": ["Jan", "Jan", None]})
        st.write("Source preview")
        st.dataframe(data, hide_index=True, use_container_width=True)
        trim = st.checkbox("Trim account codes")
        replace = st.checkbox("Replace invalid amount with null")
        fill = st.checkbox("Fill missing month down")
        cleaned = data.copy()
        if trim: cleaned["Account"] = cleaned["Account"].str.strip()
        if replace: cleaned["Amount"] = cleaned["Amount"].replace("N/A", None)
        if fill: cleaned["Month"] = cleaned["Month"].ffill()
        st.write("Result")
        st.dataframe(cleaned, hide_index=True, use_container_width=True)
    elif lab_id == 4:
        control_answer = st.radio(
            "Which join should an accountant use to list Sales Orders that have no Customer Master match?",
            ["Inner", "Left Outer", "Left Anti", "Right Anti"],
            index=None,
            horizontal=True,
        )
        if control_answer == "Left Anti":
            st.success("Correct. Left Anti keeps only non-matching rows from the primary table.")
        elif control_answer:
            st.warning("Review the highlighted regions above: the exception population is the primary-only region.")
    elif lab_id == 5:
        duplicate = st.toggle("Introduce a duplicate ProductKey in the Product dimension")
        st.write("Relationship: **Product (one) → Sales (many)**" if not duplicate else "Relationship cannot remain one-to-many because the dimension key is no longer unique.")
        st.success("Clean star schema: filtering is predictable.") if not duplicate else st.error("Control failed: deduplicate or create a valid business key before relating tables.")
    elif lab_id == 6:
        country = st.selectbox("Country filter", ["All", "UAE", "KSA", "Oman"])
        sales = {"All": 1_250_000, "UAE": 610_000, "KSA": 420_000, "Oman": 220_000}[country]
        margin_pct = st.slider("Margin %", 5, 45, 24)
        c1, c2 = st.columns(2)
        c1.metric("Net sales", f"AED {sales:,.0f}")
        c2.metric("Gross margin", f"AED {sales*margin_pct/100:,.0f}", f"{margin_pct}%")
        st.code("Gross Margin % = DIVIDE([Gross Margin], [Net Sales])", language="text")
    elif lab_id == 7:
        purpose = st.selectbox("Analytical purpose", ["Trend over time", "Compare categories", "Headline value", "Detailed statement", "Relationship between measures"])
        mapping = {"Trend over time": "Line chart", "Compare categories": "Sorted bar chart", "Headline value": "Card", "Detailed statement": "Matrix", "Relationship between measures": "Scatter plot"}
        st.metric("Best starting visual", mapping[purpose])
    elif lab_id == 8:
        view = st.radio("Report view", ["Executive overview", "Margin drivers", "Transaction evidence"], horizontal=True)
        st.info({"Executive overview": "KPI cards → trend → top drivers", "Margin drivers": "Variance tree → category bars → commentary", "Transaction evidence": "Drillthrough table → source identifiers → export"}[view])
        st.caption("This simulates a bookmark-driven navigation path.")
    elif lab_id == 9:
        source = st.text_input("Folder parameter", "C:/Training/Sales")
        st.code(f'''let\n    SourcePath = "{source}",\n    Source = Folder.Files(SourcePath),\n    VisibleFiles = Table.SelectRows(Source, each [Attributes]?[Hidden]? <> true)\nin\n    VisibleFiles''', language="powerquery")
        st.caption("Change the parameter without rewriting the transformation logic.")
    elif lab_id == 10:
        n = st.slider("Transactions", 300, 5000, 1200, 100)
        anomaly = st.slider("Extra concentration on digit 9", 0, 25, 8)
        expected = [math.log10(1 + 1/d) for d in range(1, 10)]
        rng = random.Random(42)
        counts = [0] * 9
        for _ in range(n):
            r = rng.random()
            cumulative = 0
            digit = 1
            for idx, p in enumerate(expected):
                cumulative += p
                if r <= cumulative:
                    digit = idx + 1
                    break
            if rng.random() < anomaly / 100:
                digit = 9
            counts[digit - 1] += 1
        chart = pd.DataFrame({"Digit": list(range(1, 10)), "Observed": [c/n for c in counts], "Expected": expected}).set_index("Digit")
        st.bar_chart(chart)
        st.warning("A deviation prioritizes investigation; it does not establish fraud.")
    elif lab_id == 11:
        source = st.selectbox("Source location", ["Cloud service", "On-premises SQL Server", "Local laptop file"])
        audience = st.selectbox("Audience", ["Finance developers", "Regional managers", "All employees"])
        gateway = source != "Cloud service"
        rls = audience == "Regional managers"
        st.write(f"**Gateway:** {'Likely required' if gateway else 'Usually not required'}")
        st.write(f"**Row-level security:** {'Design and test a region mapping' if rls else 'Assess based on data sensitivity'}")
    else:
        controls = ["Source totals reconciled", "Relationships tested", "Measures validated under filters", "Exceptions drill to evidence", "Assumptions documented", "Five-minute story rehearsed"]
        done = sum(st.checkbox(item, key=f"cap_{i}") for i, item in enumerate(controls))
        st.progress(done / len(controls), text=f"Capstone readiness · {done}/{len(controls)} controls")


def assessment() -> None:
    page_header("Knowledge check", "Final assessment", "Answer all 20 questions. A score of 14 or more unlocks the certificate.")
    with st.form("assessment_form"):
        answers = []
        for i, (question, options, _) in enumerate(ASSESSMENT, 1):
            answers.append(st.radio(f"{i}. {question}", options, index=None, key=f"assessment_{i}"))
        submitted = st.form_submit_button("Submit assessment", type="primary")
    if submitted:
        unanswered = sum(answer is None for answer in answers)
        if unanswered:
            st.warning(f"Please answer all questions. {unanswered} remaining.")
        else:
            score = sum(options.index(answer) == correct for answer, (_, options, correct) in zip(answers, ASSESSMENT))
            st.session_state.quiz_result = score
            if score >= PASS_SCORE:
                st.balloons()
                st.success(f"Passed · {score}/20. Your certificate is unlocked.")
            else:
                st.error(f"Score · {score}/20. Review the modules and try again; the pass mark is {PASS_SCORE}/20.")
    if st.session_state.quiz_result is not None:
        st.metric("Latest score", f"{st.session_state.quiz_result}/20", "Pass" if st.session_state.quiz_result >= PASS_SCORE else "Review required")


@st.cache_data(show_spinner=False)
def load_download(filename: str) -> bytes:
    return (DOWNLOAD_DIR / filename).read_bytes()


def resources() -> None:
    page_header("Practice library", "Course resources", "Download the lab packs, starter files and completed reference solutions used across the three days.")
    query = st.text_input("Search resources", placeholder="Try: DAX, audit, starter...").lower().strip()
    available = [r for r in RESOURCES if not query or query in (r[0] + " " + r[1] + " " + r[2]).lower()]
    if not available:
        st.info("No resources match that search.")
        return
    for title, description, filename in available:
        path = DOWNLOAD_DIR / filename
        c1, c2 = st.columns([4, 1])
        with c1:
            size = f"{path.stat().st_size / 1024 / 1024:.1f} MB" if path.exists() else "Unavailable"
            st.markdown(f"**{title}**  \n{description}  \n`{filename}` · {size}")
        with c2:
            if path.exists():
                st.download_button("Download", load_download(filename), file_name=filename, key=f"dl_{filename}", use_container_width=True)
            else:
                st.button("Unavailable", disabled=True, key=f"missing_{filename}", use_container_width=True)
        st.divider()
    st.caption("Completed PBIX files are reference solutions. Rebuild the exercise independently before comparing your approach.")


def certificate() -> None:
    page_header("Completion", "Course certificate", "Complete all 12 modules and pass the assessment to unlock your personalized certificate.")
    name = st.session_state.learner_name
    modules_done = len(st.session_state.completed)
    score = st.session_state.quiz_result or 0
    eligible = bool(name) and modules_done == len(MODULES) and score >= PASS_SCORE
    c1, c2, c3 = st.columns(3)
    c1.metric("Learner name", "Ready" if name else "Missing")
    c2.metric("Modules", f"{modules_done}/{len(MODULES)}")
    c3.metric("Assessment", f"{score}/20")
    if eligible:
        st.markdown(
            f'''<div class="certificate"><div class="eyebrow">Certificate of completion</div><h1>Power BI for Finance, Reporting and Audit Analytics</h1><p>This certifies that</p><div class="name">{name}</div><p>successfully completed the three-day learning programme<br>and demonstrated applied understanding of the full Power BI workflow.</p><p><b>{date.today().strftime("%d %B %Y")}</b> · Dubai</p><p>Developed by CA Pradeep Gujaran</p></div>''',
            unsafe_allow_html=True,
        )
        st.info("Use your browser's Print command and choose **Save as PDF** to retain a copy.")
    else:
        st.warning("Add your learner name in the sidebar, complete all modules and score at least 14/20 to unlock the certificate.")


inject_styles()
setup_state()
page = sidebar()
{
    "Learning home": home,
    "Curriculum": curriculum,
    "Three-day plan": three_day_plan,
    "Interactive lab": interactive_lab,
    "Assessment": assessment,
    "Resources": resources,
    "Certificate": certificate,
}[page]()
st.markdown('<div class="credit">Power BI Learning Studio · Developed by CA Pradeep Gujaran</div>', unsafe_allow_html=True)
