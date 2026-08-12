from __future__ import annotations

from datetime import date
from pathlib import Path
import math
import random

import pandas as pd
import streamlit as st

from course_data import ASSESSMENT, MODULES, RESOURCES, SCHEDULE


APP_DIR = Path(__file__).parent
DOWNLOAD_DIR = APP_DIR / "assets" / "downloads"
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
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
        :root { --ink:#0b1739; --muted:#64708b; --yellow:#f2c811; --cream:#fbfaf6; --line:#e5e8ef; --teal:#19a39b; }
        html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
        h1,h2,h3 { font-family:'Manrope',sans-serif !important; letter-spacing:-.035em; color:var(--ink); }
        .stApp { background:linear-gradient(180deg,#ffffff 0,#fbfaf6 60%,#f6f3ea 100%); color:var(--ink); }
        [data-testid="stSidebar"] { background:#0b1739; border-right:1px solid rgba(255,255,255,.08); }
        [data-testid="stSidebar"] * { color:#f8f9fc; }
        [data-testid="stSidebar"] hr { border-color:rgba(255,255,255,.15); }
        [data-testid="stSidebar"] .stRadio label { padding:.4rem .3rem; }
        .block-container { max-width:1250px; padding-top:2rem; padding-bottom:4rem; }
        .eyebrow { color:#8b6f00; font-size:.75rem; letter-spacing:.16em; text-transform:uppercase; font-weight:800; }
        .hero { background:var(--ink); color:white; padding:2.2rem; border-radius:24px; overflow:hidden; position:relative; box-shadow:0 18px 50px rgba(11,23,57,.16); }
        .hero:after { content:''; position:absolute; width:260px; height:260px; border-radius:50%; right:-70px; top:-90px; background:rgba(242,200,17,.14); border:46px solid rgba(242,200,17,.08); }
        .hero h1 { color:white; font-size:3rem; max-width:760px; margin:.3rem 0 .6rem; line-height:1.04; }
        .hero p { color:#c7cee0; max-width:720px; font-size:1.05rem; }
        .hero .pill { display:inline-block; padding:.38rem .7rem; background:var(--yellow); color:var(--ink); border-radius:999px; font-weight:800; font-size:.78rem; margin-right:.4rem; }
        .metric-row { display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; margin:1.2rem 0 1.8rem; }
        .metric-card,.content-card { background:rgba(255,255,255,.91); border:1px solid var(--line); border-radius:18px; padding:1.15rem; box-shadow:0 8px 30px rgba(11,23,57,.05); }
        .metric-card strong { display:block; font-family:'Manrope'; font-size:1.7rem; color:var(--ink); }
        .metric-card span { color:var(--muted); font-size:.84rem; }
        .module-head { background:linear-gradient(135deg,#0b1739,#172a5e); color:white; padding:1.7rem; border-radius:20px; margin-bottom:1rem; }
        .module-head h1 { color:white; margin:.25rem 0; }
        .module-head p { color:#c7cee0; margin:0; }
        .concept { border-left:4px solid var(--yellow); background:white; padding:1rem 1.1rem; border-radius:0 14px 14px 0; margin:.75rem 0; box-shadow:0 5px 20px rgba(11,23,57,.05); }
        .concept h4 { margin:0 0 .35rem; color:var(--ink); }
        .example { color:#47536e; background:#f6f7fa; padding:.65rem .75rem; border-radius:9px; margin:.6rem 0; }
        .remember { color:#6e5900; font-weight:700; font-size:.9rem; }
        .lab { background:#fff8d8; border:1px solid #f0d85e; border-radius:18px; padding:1.2rem; }
        .badge { display:inline-block; background:#eef1f7; color:#35415d; border-radius:999px; padding:.25rem .6rem; font-size:.75rem; font-weight:700; margin-right:.3rem; }
        .day-card { height:100%; background:white; border:1px solid var(--line); border-radius:18px; padding:1.2rem; border-top:5px solid var(--yellow); }
        .day-card h3 { margin:.3rem 0; }
        .day-card p { color:var(--muted); min-height:72px; }
        .credit { text-align:center; color:#8e97aa; font-size:.82rem; padding-top:2rem; }
        .certificate { background:#fffdf5; border:9px double #d7b313; padding:3rem; text-align:center; border-radius:4px; }
        .certificate .name { font-family:'Manrope'; color:#0b1739; font-size:2rem; border-bottom:1px solid #d9d1ad; display:inline-block; padding:0 2rem .4rem; }
        .small-note { color:var(--muted); font-size:.85rem; }
        div[data-testid="stProgress"] > div > div > div { background-color:var(--yellow); }
        .stButton > button, .stDownloadButton > button { border-radius:10px; border:1px solid #d7b313; font-weight:700; }
        .stButton > button[kind="primary"] { background:var(--yellow); color:var(--ink); border-color:var(--yellow); }
        @media(max-width:800px){.metric-row{grid-template-columns:repeat(2,1fr)}.hero h1{font-size:2.2rem}}
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
        st.markdown("## POWER BI\n### Learning Studio")
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
    st.markdown(f'<div class="eyebrow">{kicker}</div>', unsafe_allow_html=True)
    st.title(title)
    st.write(copy)


def home() -> None:
    learner = st.session_state.learner_name or "CA learner"
    st.markdown(
        f"""
        <div class="hero">
          <span class="pill">3 DAYS</span><span class="pill">18 CONTACT HOURS</span><span class="pill">12 MODULES</span>
          <h1>Power BI for finance, reporting and audit analytics</h1>
          <p>Welcome, {learner}. Follow a practical path from raw files to a governed, decision-ready Power BI solution—with guided concepts, interactive examples, downloadable labs and a capstone.</p>
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


def interactive_lab() -> None:
    page_header("Try it", "Interactive lab", "Choose a module and manipulate a small finance example before working in Power BI Desktop.")
    labels = {f"{m['code']} · {m['title']}": m for m in MODULES}
    selected = labels[st.selectbox("Interactive example", list(labels))]
    st.markdown(f"### {selected['title']}")
    lab_id = selected["id"]
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
        join = st.selectbox("Join type", ["Left outer", "Inner", "Left anti", "Full outer"])
        outcomes = {"Left outer": (5, "Keep all five transactions; unmatched product is null"), "Inner": (4, "Keep only the four matched transactions"), "Left anti": (1, "Return the one unmapped transaction for investigation"), "Full outer": (6, "Keep all transactions and all master records")}
        count, copy = outcomes[join]
        st.metric("Result rows", count)
        st.info(copy)
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
