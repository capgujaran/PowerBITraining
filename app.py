from __future__ import annotations

from datetime import date
from html import escape
from io import BytesIO
from pathlib import Path
import base64
import math
import random
from zipfile import ZIP_DEFLATED, ZipFile

import pandas as pd
import streamlit as st
from PIL import Image

from course_data import ASSESSMENT, MODULES, RESOURCES, SCHEDULE, TOOL_LABS


APP_DIR = Path(__file__).parent
DOWNLOAD_DIR = APP_DIR / "assets" / "downloads"
SCREENSHOT_DIR = APP_DIR / "assets" / "screenshots"
PASS_SCORE = 14
ASSESSMENT_EXPLANATIONS = [
    "Power BI Desktop is the primary authoring environment for connections, transformations, modelling, DAX and report design.",
    "Grain states exactly what one row represents. It must be understood before keys, relationships or calculations are designed.",
    "Import stores a compressed copy in the Power BI model and is normally the fastest interactive starting point for modest datasets.",
    "Unpivot reshapes repeating columns into attribute-value rows, producing a scalable analytical structure.",
    "Append stacks compatible tables vertically and therefore adds rows; Merge matches keys to add related columns.",
    "A Left Anti join returns rows from the first, or primary, table that have no matching key in the second table.",
    "Transaction amounts and other event-level numeric observations normally belong in the fact table.",
    "A dimension key must be unique on the one side; the Sales fact table can repeat that ProductKey on the many side.",
    "A complete dedicated date table supports consistent calendar filtering, sorting and time-intelligence calculations.",
    "CALCULATE evaluates an expression after modifying filter context.",
    "DIVIDE handles zero or blank denominators safely and is preferred to the division operator for business ratios.",
    "A measure is calculated at query time within the filter context created by the report, visual and user selections.",
    "A line chart preserves sequence and makes change over time easy to compare.",
    "Drillthrough carries the selected entity or category context to a page designed for supporting detail.",
    "In a Power Query let/in expression, the expression after `in` is the value returned by the query.",
    "A custom M function packages repeatable transformation logic and accepts parameters for reuse across files or entities.",
    "Benford deviation is a risk signal that prioritises investigation; it does not prove fraud or error by itself.",
    "An enterprise gateway securely connects the Power BI Service to supported on-premises sources for refresh or query execution.",
    "Row-level security filters the model rows available to a user or role; it does not replace workspace permissions.",
    "A defensible capstone requires reconciliation of totals, filter behaviour, edge cases and representative transactions.",
]

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
        .certificate { position:relative; overflow:hidden; background:radial-gradient(circle at 50% 8%,rgba(201,150,82,.13),transparent 30%),#fffdf7; border:9px double var(--gold); padding:clamp(2rem,4vw,3.5rem); text-align:center; border-radius:4px; box-shadow:0 16px 38px rgba(35,42,46,.09); }
        .certificate:before,.certificate:after { content:''; position:absolute; width:90px; height:90px; border:1px solid rgba(201,150,82,.28); transform:rotate(45deg); }
        .certificate:before { left:-54px; top:-54px; }.certificate:after { right:-54px; bottom:-54px; }
        .certificate .certificate-kicker { color:#9a6c30; font-size:.68rem; font-weight:800; letter-spacing:.22em; text-transform:uppercase; }
        .certificate h1 { margin:.7rem 0 .45rem; font-size:clamp(2rem,3.4vw,3.25rem); }
        .certificate .programme { color:#516269; font-family:'Libre Baskerville'; font-size:1.05rem; margin:0 auto 1.5rem; }
        .certificate .presented-to { color:#7a8589; font-size:.72rem; letter-spacing:.14em; text-transform:uppercase; }
        .certificate .name { font-family:'Libre Baskerville'; color:var(--ink); font-size:clamp(1.65rem,2.8vw,2.35rem); border-bottom:1px solid #d9d1ad; display:inline-block; min-width:min(520px,85%); padding:.35rem 2rem .45rem; }
        .certificate .participation-copy { color:#46585f; line-height:1.65; max-width:760px; margin:1.25rem auto; }
        .certificate .certificate-meta { display:flex; justify-content:center; flex-wrap:wrap; gap:.35rem 1.5rem; color:#53656b; font-size:.78rem; margin:1.15rem 0; }
        .certificate .trainer-signoff { color:var(--ink); font-weight:700; margin:.8rem 0 0; }
        .certificate .disclaimer { max-width:940px; margin:1.25rem auto 0; padding-top:.7rem; border-top:1px solid #e4dcc8; color:#808487; font-size:.5rem; line-height:1.35; letter-spacing:.005em; }
        .certificate .sample-watermark { position:absolute; left:50%; top:48%; transform:translate(-50%,-50%) rotate(-20deg); color:rgba(139,104,59,.075); font-family:'Libre Baskerville'; font-size:clamp(4rem,11vw,9rem); font-weight:700; letter-spacing:.08em; pointer-events:none; white-space:nowrap; }
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
        .append-flow { background:white; border:1px solid var(--line); border-radius:9px; padding:1.15rem; margin:.8rem 0 1.2rem; }
        .append-sources { display:grid; grid-template-columns:repeat(3,1fr); gap:.7rem; }
        .append-source { position:relative; min-height:92px; background:#f7f9f7; border:1px solid var(--line); border-top:5px solid var(--source-color,#177c72); border-radius:7px; padding:.8rem .9rem; }
        .append-source b,.append-target b { display:block; color:var(--ink); margin-bottom:.25rem; }
        .append-source span,.append-target span { color:var(--muted); font-size:.75rem; line-height:1.35; }
        .append-source.inactive { opacity:.32; border-top-color:#aab3b1; }
        .append-down { text-align:center; color:var(--ink); font-weight:800; padding:.65rem 0 .5rem; }
        .append-down .arrow { display:block; color:var(--gold); font-size:1.75rem; line-height:1; }
        .append-target { max-width:620px; margin:auto; background:#eef6f4; border:2px solid #7fb4aa; border-radius:8px; padding:.9rem 1rem; text-align:center; }
        .schema-map { display:grid; grid-template-columns:1fr auto 1fr; gap:.75rem; align-items:center; margin:.6rem 0 1rem; }
        .schema-box { background:white; border:1px solid var(--line); border-radius:7px; padding:.8rem .9rem; min-height:92px; }
        .schema-box b { display:block; color:var(--ink); margin-bottom:.3rem; }
        .schema-box span { display:inline-block; background:#eef3f1; color:#49615d; padding:.18rem .32rem; margin:.12rem; border-radius:3px; font-size:.68rem; }
        .schema-box span.mismatch { background:#fff0e8; color:#9a4e32; }
        .schema-arrow { text-align:center; color:var(--teal); font-size:1.55rem; font-weight:800; }
        .append-warning { background:#fff7e7; border-left:4px solid var(--gold); color:#6d5632; padding:.8rem .9rem; margin:.65rem 0; border-radius:0 6px 6px 0; }
        .lab-process { display:flex; align-items:stretch; gap:.45rem; margin:.8rem 0 1.15rem; }
        .lab-process__node { flex:1; min-width:0; background:white; border:1px solid var(--line); border-top:4px solid var(--teal); border-radius:7px; padding:.75rem .8rem; }
        .lab-process__node.active { background:#eef6f4; border-color:#83b7ae; }
        .lab-process__node.warning { background:#fff7e7; border-top-color:var(--gold); }
        .lab-process__node b { display:block; color:var(--ink); font-size:.82rem; margin-bottom:.2rem; }
        .lab-process__node span { display:block; color:var(--muted); font-size:.7rem; line-height:1.35; }
        .lab-process__arrow { display:grid; place-content:center; color:var(--gold); font-size:1.25rem; font-weight:800; }
        .lab-summary { background:white; border:1px solid var(--line); border-left:5px solid var(--teal); border-radius:7px; padding:.9rem 1rem; margin:.7rem 0 1rem; }
        .lab-summary b { color:var(--ink); }.lab-summary p { color:var(--muted); margin:.25rem 0 0; line-height:1.5; }
        .model-map { display:grid; grid-template-columns:repeat(4,1fr); gap:.65rem; margin:.8rem 0 1.1rem; }
        .model-table { background:white; border:1px solid var(--line); border-top:4px solid #7892a5; border-radius:7px; padding:.8rem; text-align:center; }
        .model-table.fact { grid-column:1/-1; max-width:520px; width:100%; margin:auto; border-top-color:var(--gold); background:#fffaf0; }
        .model-table b { display:block; color:var(--ink); }.model-table span { color:var(--muted); font-size:.7rem; }
        .context-strip { display:flex; flex-wrap:wrap; gap:.4rem; margin:.65rem 0 1rem; }
        .context-strip span { background:#eaf3f1; color:#315c57; border:1px solid #c8ded8; border-radius:4px; padding:.32rem .48rem; font-size:.72rem; font-weight:700; }
        .report-path { display:grid; grid-template-columns:repeat(3,1fr); gap:.55rem; margin:.7rem 0 1rem; }
        .report-path div { position:relative; background:white; border:1px solid var(--line); border-radius:7px; padding:.8rem; color:var(--muted); text-align:center; }
        .report-path div.active { background:#183743; color:white; border-color:#183743; }
        .report-path b { display:block; color:inherit; }
        .governance-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:.55rem; margin:.7rem 0 1rem; }
        .governance-step { background:white; border:1px solid var(--line); border-top:4px solid var(--teal); border-radius:7px; padding:.75rem; }
        .governance-step.warning { border-top-color:var(--gold); background:#fffaf0; }
        .governance-step b { display:block; color:var(--ink); font-size:.8rem; }.governance-step span { color:var(--muted); font-size:.68rem; line-height:1.35; }
        .retained-chart { display:flex; flex-direction:column; gap:1rem; background:white; border:1px solid var(--line); border-radius:8px; padding:1.15rem; min-height:250px; justify-content:center; }
        .retained-row__label { display:flex; justify-content:space-between; gap:1rem; color:#53656b; font-size:.74rem; font-weight:700; margin-bottom:.4rem; }
        .retained-row__label b { color:var(--ink); font-family:'Libre Baskerville'; font-size:.9rem; }
        .retained-track { height:13px; overflow:hidden; background:#edf0ee; border-radius:3px; }
        .retained-track span { display:block; height:100%; min-width:0; border-radius:3px; transition:width .25s ease; }
        .assessment-hero { display:grid; grid-template-columns:1.25fr .75fr; gap:2rem; align-items:center; background:radial-gradient(circle at 88% 18%,rgba(201,150,82,.24),transparent 34%),linear-gradient(135deg,#102933,var(--ink)); color:white; padding:2.1rem 2.35rem; border-radius:10px; margin-bottom:1.35rem; box-shadow:0 14px 34px rgba(12,27,36,.12); }
        .assessment-hero h2 { color:white; margin:.3rem 0 .65rem; font-size:clamp(1.65rem,2.4vw,2.45rem); }
        .assessment-hero p { color:#bfd0cf; margin:0; line-height:1.6; }
        .assessment-kpis { display:grid; grid-template-columns:repeat(2,1fr); gap:.65rem; }
        .assessment-kpi { background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.12); border-radius:7px; padding:.8rem .9rem; }
        .assessment-kpi strong { display:block; color:#f3d8ae; font-family:'Libre Baskerville'; font-size:1.25rem; }
        .assessment-kpi span { color:#aebfbe; font-size:.68rem; text-transform:uppercase; letter-spacing:.09em; }
        .question-status { display:flex; justify-content:space-between; gap:1rem; align-items:center; padding:.8rem 1rem; background:#edf3f1; border-left:4px solid var(--teal); border-radius:0 6px 6px 0; margin-bottom:1rem; color:#47615f; font-size:.83rem; }
        .question-status b { color:var(--ink); }
        .question-card-head { padding:1.15rem 1.2rem .55rem; background:white; border:1px solid var(--line); border-bottom:0; border-radius:8px 8px 0 0; }
        .question-card-head h2 { font-size:1.45rem; line-height:1.42; margin:.35rem 0 .25rem; }
        .question-card-head span { color:var(--teal); font-size:.68rem; font-weight:800; letter-spacing:.13em; text-transform:uppercase; }
        [data-testid="stMain"] [data-testid="stRadio"] > div { gap:.32rem; }
        [data-testid="stMain"] [data-testid="stRadio"] label { background:white; border:1px solid var(--line); border-radius:6px; padding:.72rem .9rem; margin:.12rem 0; transition:.16s ease; }
        [data-testid="stMain"] [data-testid="stRadio"] label:hover { border-color:#8bb8b1; background:#f7fbfa; }
        [data-testid="stMain"] [data-testid="stRadio"] label:has(input:checked) { border-color:var(--teal); background:#eaf4f1; box-shadow:inset 3px 0 var(--teal); }
        .answer-feedback { padding:1rem 1.1rem; margin:.85rem 0; border-radius:7px; border:1px solid; }
        .answer-feedback strong { display:block; margin-bottom:.3rem; }
        .answer-feedback.correct { background:#edf8f1; border-color:#aad2bb; color:#245d3e; }
        .answer-feedback.incorrect { background:#fff4ef; border-color:#e8bdad; color:#863d2b; }
        .answer-feedback p { color:#526468; margin:.35rem 0 0; line-height:1.55; }
        .result-panel { display:grid; grid-template-columns:auto 1fr; gap:1.8rem; align-items:center; background:linear-gradient(135deg,#102933,var(--ink)); color:white; border-radius:10px; padding:2rem 2.3rem; margin-bottom:1.3rem; }
        .result-ring { width:132px; height:132px; display:grid; place-content:center; text-align:center; border:8px solid var(--gold); border-radius:50%; background:#183743; }
        .result-ring strong { display:block; color:white; font-family:'Libre Baskerville'; font-size:2rem; line-height:1; }
        .result-ring span { color:#b7c8c7; font-size:.7rem; text-transform:uppercase; letter-spacing:.1em; margin-top:.35rem; }
        .result-panel h2 { color:white; margin:.2rem 0 .45rem; }
        .result-panel p { color:#bfd0cf; margin:0; }
        .day-result-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:.8rem; margin:1rem 0 1.4rem; }
        .day-result { background:white; border:1px solid var(--line); border-top:4px solid var(--teal); border-radius:7px; padding:1rem; }
        .day-result strong { display:block; color:var(--ink); font-family:'Libre Baskerville'; font-size:1.25rem; }
        .day-result span { color:var(--muted); font-size:.75rem; }
        .trainer-hero { display:grid; grid-template-columns:.78fr 1.42fr; gap:1.25rem; align-items:stretch; }
        .trainer-photo { background:#e9edeb; border:1px solid var(--line); border-radius:10px; overflow:hidden; min-height:520px; }
        .trainer-photo img { display:block; width:100%; height:100%; min-height:520px; object-fit:cover; object-position:center top; }
        .trainer-copy { background:radial-gradient(circle at 90% 10%,rgba(201,150,82,.22),transparent 35%),linear-gradient(135deg,#102933,var(--ink)); color:white; padding:2.35rem 2.45rem; border-radius:10px; min-height:100%; }
        .trainer-copy h2 { color:white; font-size:clamp(2rem,3vw,3.2rem); line-height:1.08; margin:.55rem 0 1rem; }
        .trainer-copy p { color:#bfd0cf; line-height:1.7; }
        .trainer-copy .trainer-role { color:#f3d8ae; font-weight:700; }
        .trainer-links { display:flex; flex-wrap:wrap; gap:.55rem; margin-top:1.25rem; }
        .trainer-links a { color:white !important; text-decoration:none; border:1px solid rgba(255,255,255,.22); border-radius:5px; padding:.62rem .78rem; font-size:.76rem; font-weight:700; }
        .trainer-links a:hover { color:#f3d8ae !important; border-color:var(--gold); }
        .trainer-stat-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:.8rem; margin:1.4rem 0 2rem; }
        .trainer-stat { background:white; border:1px solid var(--line); border-top:4px solid var(--gold); border-radius:7px; padding:1rem; }
        .trainer-stat strong { display:block; color:var(--ink); font-family:'Libre Baskerville'; font-size:1.55rem; }
        .trainer-stat span { color:var(--muted); font-size:.73rem; line-height:1.35; }
        .award-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:.85rem; margin:.9rem 0 2rem; }
        .award-card { position:relative; background:white; border:1px solid var(--line); border-radius:8px; padding:1.15rem 1.15rem 1.15rem 4.7rem; min-height:118px; }
        .award-year { position:absolute; left:1rem; top:1.15rem; color:var(--gold); font-family:'Libre Baskerville'; font-size:1.3rem; }
        .award-card b { color:var(--ink); display:block; margin-bottom:.35rem; }
        .award-card p { color:var(--muted); font-size:.79rem; line-height:1.45; margin:0; }
        .experience-line { border-left:2px solid #c8d8d4; margin:.8rem 0 2rem .55rem; padding-left:1.4rem; }
        .experience-item { position:relative; padding:.2rem 0 1.15rem; }
        .experience-item:before { content:''; position:absolute; width:11px; height:11px; border-radius:50%; background:var(--gold); left:-1.82rem; top:.48rem; box-shadow:0 0 0 4px #f3f5f3; }
        .experience-item b { color:var(--ink); }
        .experience-item span { display:block; color:var(--teal); font-size:.7rem; font-weight:800; letter-spacing:.1em; text-transform:uppercase; margin-bottom:.22rem; }
        .experience-item p { color:var(--muted); font-size:.83rem; margin:.25rem 0 0; line-height:1.5; }
        .expertise-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:.8rem; margin:.9rem 0 1.5rem; }
        .expertise-card { background:white; border:1px solid var(--line); border-radius:7px; padding:1rem; }
        .expertise-card b { color:var(--ink); display:block; margin-bottom:.35rem; }
        .expertise-card p { color:var(--muted); font-size:.78rem; line-height:1.45; margin:0; }
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
        @media(max-width:900px){.hero,.assessment-hero,.trainer-hero{grid-template-columns:1fr}.hero,.assessment-hero{padding:2.6rem}.journey-wheel{display:none}.metric-row,.trainer-stat-grid{grid-template-columns:repeat(2,1fr)}.merge-flow,.schema-map{grid-template-columns:1fr}.merge-arrows,.schema-arrow{transform:rotate(90deg);padding:.25rem}.append-sources,.model-map,.report-path,.governance-grid{grid-template-columns:1fr}.model-table.fact{grid-column:auto}.lab-process{flex-direction:column}.lab-process__arrow{transform:rotate(90deg)}.expertise-grid{grid-template-columns:1fr}.award-grid{grid-template-columns:1fr}.trainer-photo,.trainer-photo img{min-height:0;max-height:520px}}
        @media(max-width:560px){.metric-row,.trainer-stat-grid,.day-result-grid{grid-template-columns:1fr}.block-container{padding:4.5rem 1rem 3rem}.hero,.assessment-hero,.trainer-copy{padding:2rem 1.35rem}.page-intro{display:block}.page-intro h1{font-size:2rem}.result-panel{grid-template-columns:1fr;text-align:center}.result-ring{margin:auto}.award-card{padding-left:1rem;padding-top:3.6rem}.award-year{top:1rem}}
        @media print {[data-testid="stSidebar"],header,[data-testid="stToolbar"],.page-intro,.metric-row,.small-note,.credit,.stAlert{display:none!important}.block-container{max-width:none;padding:0}.certificate{box-shadow:none;min-height:92vh;display:flex;flex-direction:column;justify-content:center}}
        </style>
        """,
        unsafe_allow_html=True,
    )


def setup_state() -> None:
    defaults = {
        "learner_name": "",
        "completed": set(),
        "quiz_result": None,
        "assessment_latest_score": None,
        "assessment_answers": {},
        "assessment_index": 0,
        "assessment_complete": False,
        "assessment_history": [],
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
            st.caption(f"Best assessment · {result}/20")
        pages = ["Learning home", "Curriculum", "Three-day plan", "Interactive lab", "Assessment", "About the Trainer", "Resources", "Certificate"]
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


def sample_model_tables() -> dict[str, pd.DataFrame]:
    products = pd.DataFrame(
        {
            "ProductKey": ["P01", "P02", "P03"],
            "Product": ["Business Laptop", "Monitor", "Advisory Service"],
            "Category": ["Hardware", "Hardware", "Services"],
            "UnitPrice": [4200, 1350, 2500],
            "UnitCost": [3350, 900, 1050],
        }
    )
    customers = pd.DataFrame(
        {
            "CustomerKey": ["C01", "C02", "C03", "C04", "C05", "C06"],
            "Customer": ["Desert Retail", "Marina Foods", "Creek Trading", "Oasis Services", "Falcon Stores", "Harbour Group"],
            "Region": ["Dubai", "Sharjah", "Dubai", "Ajman", "Sharjah", "Ajman"],
            "Segment": ["Retail", "Hospitality", "Wholesale", "Services", "Retail", "Corporate"],
        }
    )
    sales = pd.DataFrame(
        {
            "InvoiceID": [f"INV-{1000 + i}" for i in range(1, 16)],
            "InvoiceDate": pd.to_datetime(
                ["2026-01-05", "2026-01-09", "2026-01-15", "2026-01-24", "2026-01-29", "2026-02-04", "2026-02-10", "2026-02-15", "2026-02-21", "2026-02-27", "2026-03-03", "2026-03-09", "2026-03-16", "2026-03-22", "2026-03-28"]
            ),
            "CustomerKey": ["C01", "C02", "C03", "C04", "C05", "C06", "C01", "C03", "C04", "C02", "C05", "C06", "C01", "C04", "C03"],
            "ProductKey": ["P01", "P02", "P03", "P02", "P01", "P03", "P02", "P01", "P03", "P02", "P01", "P03", "P01", "P02", "P03"],
            "Quantity": [2, 4, 3, 2, 1, 4, 5, 2, 2, 3, 2, 3, 1, 6, 4],
        }
    )
    sales = sales.merge(products[["ProductKey", "UnitPrice", "UnitCost"]], on="ProductKey", how="left")
    sales["NetAmount"] = sales["Quantity"] * sales["UnitPrice"]
    sales["CostAmount"] = sales["Quantity"] * sales["UnitCost"]
    sales["GrossMargin"] = sales["NetAmount"] - sales["CostAmount"]
    dates = pd.DataFrame({"Date": pd.date_range("2026-01-01", "2026-03-31", freq="D")})
    dates["Month"] = dates["Date"].dt.strftime("%b")
    dates["MonthNumber"] = dates["Date"].dt.month
    budgets = pd.DataFrame({"Region": ["Dubai", "Sharjah", "Ajman"], "Budget": [52000, 40000, 34000]})
    return {"Sales": sales, "Product": products, "Customer": customers, "Date": dates, "Budget": budgets}


def dataframes_zip(tables: list[tuple[str, pd.DataFrame]]) -> bytes:
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
        for filename, table in tables:
            archive.writestr(filename, table.to_csv(index=False))
    return buffer.getvalue()


def lab_banner(title: str, copy: str) -> None:
    st.markdown(f'<div class="merge-callout"><b>{title}</b><br>{copy}</div>', unsafe_allow_html=True)


def process_strip(nodes: list[tuple[str, str, str]]) -> None:
    parts = []
    for index, (title, subtitle, state) in enumerate(nodes):
        if index:
            parts.append('<div class="lab-process__arrow">→</div>')
        parts.append(f'<div class="lab-process__node {state}"><b>{title}</b><span>{subtitle}</span></div>')
    st.markdown(f'<div class="lab-process">{"".join(parts)}</div>', unsafe_allow_html=True)


def detailed_workflow_lab() -> None:
    lab_banner("Interactive analytics workflow laboratory", "Turn a vague reporting request into a decision-ready Power BI solution. The question, filtered dataset, KPIs and delivery path respond together.")
    model = sample_model_tables()
    sales = model["Sales"].merge(model["Product"][["ProductKey", "Product", "Category"]], on="ProductKey").merge(model["Customer"][["CustomerKey", "Customer", "Region"]], on="CustomerKey")
    question = st.selectbox(
        "Management question",
        ["Which region drives sales and margin?", "Which product category is underperforming?", "Which customers need management attention?"],
        key="workflow_question",
    )
    audience = st.selectbox("Primary audience", ["CFO", "Finance manager", "Internal auditor"], key="workflow_audience")
    region = st.selectbox("Analysis scope", ["All regions", "Dubai", "Sharjah", "Ajman"], key="workflow_region")
    filtered = sales if region == "All regions" else sales[sales["Region"] == region]
    decision_map = {
        "Which region drives sales and margin?": "Reallocate commercial focus and challenge regional performance",
        "Which product category is underperforming?": "Review pricing, cost and product-mix decisions",
        "Which customers need management attention?": "Prioritise account review and concentration risk",
    }
    st.markdown(f'<div class="lab-summary"><b>Decision-ready requirement</b><p>{audience} needs to answer “{question}” for {region.lower()} so the team can {decision_map[question].lower()}.</p></div>', unsafe_allow_html=True)
    process_strip(
        [
            ("Business question", "Decision, audience, grain and benchmark", "active"),
            ("Power BI Desktop", "Transform, model, calculate and design", "active"),
            ("Power BI Service", "Publish, refresh, secure and distribute", "active"),
            (audience, "Consume insight and take action", "active"),
        ]
    )
    metrics = st.columns(3)
    metrics[0].metric("Net sales", f"AED {filtered['NetAmount'].sum():,.0f}")
    metrics[1].metric("Gross margin", f"AED {filtered['GrossMargin'].sum():,.0f}")
    metrics[2].metric("Transactions", len(filtered))
    group_field = "Region" if "region" in question.lower() else "Category" if "product" in question.lower() else "Customer"
    summary = filtered.groupby(group_field, as_index=False)[["NetAmount", "GrossMargin"]].sum().set_index(group_field)
    st.bar_chart(summary)
    with st.expander("Inspect the transaction grain and business keys"):
        st.dataframe(filtered[["InvoiceID", "InvoiceDate", "CustomerKey", "ProductKey", "Quantity", "NetAmount", "GrossMargin"]], hide_index=True, use_container_width=True)
        st.caption("Grain: one row per invoice-product transaction. InvoiceID identifies the transaction; CustomerKey and ProductKey connect descriptive dimensions.")
    st.download_button("Download workflow sample data (.csv)", filtered.to_csv(index=False), "analytics-workflow-sample.csv", "text/csv", key="workflow_download", use_container_width=True)


def detailed_connection_lab() -> None:
    lab_banner("Interactive source and connection laboratory", "Change the operating requirement to see the connector, storage mode, profiling checks and refresh architecture update.")
    source = st.selectbox("Source pattern", ["Monthly Excel files", "Governed SQL Server", "SharePoint document library", "Web API"], key="connection_source")
    row_volume = st.select_slider("Estimated data volume", options=[50_000, 250_000, 1_000_000, 5_000_000, 20_000_000], value=250_000, key="connection_rows")
    latency = st.selectbox("Required freshness", ["Monthly", "Daily", "Hourly", "Near real time"], key="connection_latency")
    mapping = {
        "Monthly Excel files": ("Folder", "Import", "Retain file name and standardise every monthly schema"),
        "Governed SQL Server": ("SQL Server", "DirectQuery" if latency == "Near real time" and row_volume >= 5_000_000 else "Import", "Use a curated view and confirm query folding"),
        "SharePoint document library": ("SharePoint Folder", "Import", "Filter the folder path before combining files"),
        "Web API": ("Web", "Import", "Plan authentication, pagination and rate-limit handling"),
    }
    connector, mode, control = mapping[source]
    process_strip(
        [
            (source, f"{row_volume:,} estimated rows", "active"),
            (connector, "Authenticate and preview in Navigator", "active"),
            (mode, f"Refresh target: {latency}", "active"),
            ("Power Query", control, "warning" if source != "Governed SQL Server" else "active"),
        ]
    )
    cols = st.columns(3)
    cols[0].metric("Recommended connector", connector)
    cols[1].metric("Starting mode", mode)
    cols[2].metric("Expected grain", "Invoice line")
    profile = pd.DataFrame(
        [
            ["InvoiceID", "Text", "0%", "Candidate transaction key"],
            ["InvoiceDate", "Date", "0%", "Required for time analysis"],
            ["CustomerKey", "Text", "0%", "Dimension foreign key"],
            ["NetAmount", "Decimal", "0.6%", "Investigate blanks before aggregation"],
        ],
        columns=["Column", "Expected type", "Sample null rate", "Profiling decision"],
    )
    st.dataframe(profile, hide_index=True, use_container_width=True)
    if mode == "DirectQuery":
        st.warning("DirectQuery is justified only after source performance, concurrency and report interactions are tested. Near-real-time need alone is not enough.")
    else:
        st.info("Import is the recommended starting point because it provides fast interaction and modelling flexibility for this requirement.")
    sample_sales = sample_model_tables()["Sales"]
    st.download_button("Download source profiling sample (.csv)", sample_sales.to_csv(index=False), "connection-source-sample.csv", "text/csv", key="connection_download", use_container_width=True)


def detailed_power_query_lab() -> None:
    lab_banner("Interactive Power Query transformation laboratory", "Apply repeatable steps to a deliberately messy finance extract. The preview, quality counts, row structure and M translation update after every selection.")
    messy = pd.DataFrame(
        {
            "Account": [" 4000", "5000 ", " 6000", "7000"],
            "Region": ["Dubai", "", "Sharjah", "Ajman"],
            "Jan": ["12500", "8200", "N/A", "4100"],
            "Feb": ["13100", "", "7600", "invalid"],
            "Mar": ["14000", "9100", "7900", "4500"],
        }
    )
    steps = ["Trim account codes", "Fill missing region", "Convert amounts and replace errors", "Unpivot month columns"]
    selected_steps = st.multiselect("Applied steps", steps, default=steps[:2], key="pq_steps")
    cleaned = messy.copy()
    if steps[0] in selected_steps:
        cleaned["Account"] = cleaned["Account"].str.strip()
    if steps[1] in selected_steps:
        cleaned["Region"] = cleaned["Region"].replace("", None).ffill()
    if steps[2] in selected_steps:
        for column in ["Jan", "Feb", "Mar"]:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")
    if steps[3] in selected_steps:
        cleaned = cleaned.melt(id_vars=["Account", "Region"], var_name="Month", value_name="Amount")
    nodes = [(step, "Applied and refreshable" if step in selected_steps else "Not yet applied", "active" if step in selected_steps else "") for step in steps]
    process_strip(nodes)
    before_col, after_col = st.columns(2)
    with before_col:
        st.markdown("#### Source preview")
        st.dataframe(messy, hide_index=True, use_container_width=True)
    with after_col:
        st.markdown("#### Live query result")
        st.dataframe(cleaned.fillna("—"), hide_index=True, use_container_width=True)
    invalid_values = int(messy[["Jan", "Feb", "Mar"]].isin(["N/A", "invalid", ""]).sum().sum())
    remaining_errors = 0 if steps[2] in selected_steps else invalid_values
    metrics = st.columns(3)
    metrics[0].metric("Output rows", len(cleaned))
    metrics[1].metric("Invalid source values", invalid_values)
    metrics[2].metric("Unresolved conversion risks", remaining_errors)
    m_steps = ['Source = Csv.Document(File.Contents(SourcePath))']
    if steps[0] in selected_steps:
        m_steps.append('Trimmed = Table.TransformColumns(Source, {{"Account", Text.Trim}})')
    if steps[1] in selected_steps:
        m_steps.append('FilledRegion = Table.FillDown(Trimmed, {"Region"})')
    if steps[2] in selected_steps:
        m_steps.append('TypedAmounts = Table.TransformColumnTypes(FilledRegion, {{"Jan", type number}, {"Feb", type number}, {"Mar", type number}})')
    if steps[3] in selected_steps:
        m_steps.append('Unpivoted = Table.Unpivot(TypedAmounts, {"Jan", "Feb", "Mar"}, "Month", "Amount")')
    st.code("let\n    " + ",\n    ".join(m_steps) + f"\nin\n    {m_steps[-1].split(' = ')[0]}", language="powerquery")
    st.download_button("Download messy Power Query sample (.csv)", messy.to_csv(index=False), "messy-finance-extract.csv", "text/csv", key="pq_download", use_container_width=True)


def append_sample_tables(scenario: str, normalize_headers: bool, inject_duplicate: bool) -> list[tuple[str, str, pd.DataFrame]]:
    january = pd.DataFrame(
        {
            "InvoiceID": ["INV-1001", "INV-1002", "INV-1003", "INV-1004"],
            "InvoiceDate": ["2026-01-05", "2026-01-12", "2026-01-19", "2026-01-27"],
            "Region": ["Dubai", "Sharjah", "Dubai", "Ajman"],
            "NetAmount": [4200, 6400, 3150, 5800],
        }
    )
    february = pd.DataFrame(
        {
            "InvoiceID": ["INV-2001", "INV-2002", "INV-2003"],
            "InvoiceDate": ["2026-02-04", "2026-02-14", "2026-02-25"],
            "Region": ["Dubai", "Ajman", "Sharjah"],
            "NetAmount": [7100, 2950, 8300],
        }
    )
    march = pd.DataFrame(
        {
            "InvoiceID": ["INV-3001", "INV-3002", "INV-3003"],
            "InvoiceDate": ["2026-03-03", "2026-03-16", "2026-03-28"],
            "Region": ["Sharjah", "Dubai", "Ajman"],
            "NetAmount": [5100, 9250, 3600],
        }
    )
    if scenario == "Schema mismatch · revised February file":
        february = february.rename(columns={"NetAmount": "SalesAmount"})
        february["Channel"] = ["Retail", "Online", "Retail"]
        if normalize_headers:
            february = february.rename(columns={"SalesAmount": "NetAmount"})
        tables = [
            ("January Sales", "January_Sales.csv", january),
            ("February Revised", "February_Revised.csv", february),
        ]
    elif scenario == "Three tables · January + February + March":
        tables = [
            ("January Sales", "January_Sales.csv", january),
            ("February Sales", "February_Sales.csv", february),
            ("March Sales", "March_Sales.csv", march),
        ]
    else:
        tables = [
            ("January Sales", "January_Sales.csv", january),
            ("February Sales", "February_Sales.csv", february),
        ]

    if inject_duplicate:
        label, filename, last_table = tables[-1]
        repeated = {
            "InvoiceID": "INV-1002",
            "InvoiceDate": "2026-01-12",
            "Region": "Sharjah",
            "NetAmount": 6400,
            "SalesAmount": 6400,
            "Channel": "Retail",
        }
        duplicate_row = pd.DataFrame([{column: repeated[column] for column in last_table.columns}])
        tables[-1] = (label, filename, pd.concat([last_table, duplicate_row], ignore_index=True))
    return tables


def append_result(tables: list[tuple[str, str, pd.DataFrame]]) -> pd.DataFrame:
    prepared = []
    for label, _, table in tables:
        part = table.copy()
        part.insert(0, "Source Table", label)
        prepared.append(part)
    return pd.concat(prepared, ignore_index=True, sort=False)


def append_row_style(row: pd.Series) -> list[str]:
    colors = {
        "January Sales": "background-color:#fff3b0;color:#0b1739",
        "February Sales": "background-color:#dff5ec;color:#0b1739",
        "February Revised": "background-color:#dff5ec;color:#0b1739",
        "March Sales": "background-color:#e6f0ff;color:#0b1739",
    }
    return [colors.get(row.get("Source Table"), "") for _ in row]


def append_practice_zip(tables: list[tuple[str, str, pd.DataFrame]]) -> bytes:
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
        for _, filename, table in tables:
            archive.writestr(filename, table.to_csv(index=False))
    return buffer.getvalue()


def detailed_append_lab() -> None:
    st.markdown(
        '<div class="merge-callout"><b>Interactive Append Queries laboratory</b><br>Change the append scenario below. The source tables, schema comparison, row-flow diagram, combined output, reconciliation metrics and Power Query formula update together.</div>',
        unsafe_allow_html=True,
    )
    scenarios = [
        "Two tables · January + February",
        "Three tables · January + February + March",
        "Schema mismatch · revised February file",
    ]
    scenario = st.selectbox("Append scenario", scenarios, key="append_scenario")
    normalize_headers = False
    if scenario == "Schema mismatch · revised February file":
        normalize_headers = st.toggle("Rename SalesAmount to NetAmount before appending", key="append_normalize_headers")
    inject_duplicate = st.toggle("Inject a repeated invoice to test duplicate controls", key="append_inject_duplicate")
    tables = append_sample_tables(scenario, normalize_headers, inject_duplicate)
    result = append_result(tables)

    source_colors = ["#f2c811", "#177c72", "#4d8fe8"]
    source_cards = []
    for index in range(3):
        if index < len(tables):
            label, _, table = tables[index]
            source_cards.append(
                f'<div class="append-source" style="--source-color:{source_colors[index]}"><b>{index + 1}. {label}</b><span>{len(table)} rows · {len(table.columns)} columns<br>{" · ".join(table.columns)}</span></div>'
            )
        else:
            source_cards.append('<div class="append-source inactive"><b>3. Optional additional table</b><span>Select the three-table scenario to include March.</span></div>')
    st.markdown(
        f'''<div class="append-flow"><div class="append-sources">{"".join(source_cards)}</div><div class="append-down"><span class="arrow">↓</span>match columns by name, then stack every row</div><div class="append-target"><b>Combined Sales</b><span>{len(result)} output rows · {len(result.columns) - 1} business columns · same transaction grain</span></div></div>''',
        unsafe_allow_html=True,
    )

    first_columns = list(tables[0][2].columns)
    comparison_columns = sorted(set().union(*(set(table.columns) for _, _, table in tables[1:])))
    common_columns = set(first_columns).intersection(comparison_columns)
    first_tags = "".join(
        f'<span class="{"" if column in common_columns else "mismatch"}">{column}</span>' for column in first_columns
    )
    comparison_tags = "".join(
        f'<span class="{"" if column in common_columns else "mismatch"}">{column}</span>' for column in comparison_columns
    )
    schema_heading = "Other table schema" if len(tables) == 2 else "February and March schema"
    st.markdown(
        f'''<div class="schema-map"><div class="schema-box"><b>January schema</b>{first_tags}</div><div class="schema-arrow">→<br><span style="font-size:.65rem">column-name alignment</span></div><div class="schema-box"><b>{schema_heading}</b>{comparison_tags}</div></div>''',
        unsafe_allow_html=True,
    )
    if scenario == "Schema mismatch · revised February file" and not normalize_headers:
        st.markdown('<div class="append-warning"><b>Watch the mismatch:</b> NetAmount and SalesAmount are treated as different columns. January rows receive blanks under SalesAmount; February rows receive blanks under NetAmount.</div>', unsafe_allow_html=True)
    elif scenario == "Schema mismatch · revised February file":
        st.success("SalesAmount now aligns with NetAmount. Channel remains an additional column, so January rows correctly receive blank Channel values.")
    else:
        st.info("Every source uses the same column names and transaction grain, so the output row count should equal the sum of the inputs.")

    source_tabs = st.tabs([label for label, _, _ in tables])
    for tab, (label, _, table) in zip(source_tabs, tables):
        with tab:
            st.dataframe(table, hide_index=True, use_container_width=True)
            st.caption(f"{label}: one row represents one invoice. Append keeps these rows and places them below the earlier source rows.")

    input_rows = sum(len(table) for _, _, table in tables)
    duplicate_ids = int(result["InvoiceID"].duplicated(keep=False).groupby(result["InvoiceID"]).any().sum()) if result["InvoiceID"].duplicated(keep=False).any() else 0
    metrics = st.columns(4)
    metrics[0].metric("Source tables", len(tables))
    metrics[1].metric("Input rows", input_rows)
    metrics[2].metric("Output rows", len(result), "Reconciled" if len(result) == input_rows else "Investigate")
    metrics[3].metric("Duplicate invoice IDs", duplicate_ids, "Review" if duplicate_ids else "Clear")

    chart_col, output_col = st.columns([.78, 1.62])
    with chart_col:
        st.markdown("#### Rows contributed by source")
        max_rows = max(len(table) for _, _, table in tables)
        bars = "".join(
            f'<div class="retained-row"><div class="retained-row__label"><span>{label}</span><b>{len(table)}</b></div><div class="retained-track"><span style="width:{len(table) / max_rows * 100:.0f}%;background:{source_colors[index]}"></span></div></div>'
            for index, (label, _, table) in enumerate(tables)
        )
        st.markdown(f'<div class="retained-chart">{bars}</div>', unsafe_allow_html=True)
    with output_col:
        st.markdown("#### Live appended output")
        display_result = result.copy()
        for amount_column in [column for column in ["NetAmount", "SalesAmount"] if column in display_result.columns]:
            display_result[amount_column] = display_result[amount_column].map(lambda value: "—" if pd.isna(value) else f"AED {value:,.0f}")
        display_result = display_result.fillna("—")
        st.dataframe(display_result.style.apply(append_row_style, axis=1), hide_index=True, use_container_width=True)

    st.markdown(
        '<div class="merge-legend"><span><i class="legend-dot" style="background:#fff3b0"></i>January rows</span><span><i class="legend-dot" style="background:#dff5ec"></i>February rows</span><span><i class="legend-dot" style="background:#e6f0ff"></i>March rows</span></div>',
        unsafe_allow_html=True,
    )
    if duplicate_ids:
        duplicated = ", ".join(sorted(result.loc[result["InvoiceID"].duplicated(keep=False), "InvoiceID"].unique()))
        st.error(f"Duplicate control triggered: {duplicated} appears in more than one source. Append does not remove duplicates automatically.")

    st.markdown("#### Power Query translation")
    query_names = [filename.removesuffix(".csv") for _, filename, _ in tables]
    if scenario == "Schema mismatch · revised February file" and normalize_headers:
        st.code(
            'February_Normalized = Table.RenameColumns(February_Revised, {{"SalesAmount", "NetAmount"}}),\nCombinedSales = Table.Combine({January_Sales, February_Normalized})',
            language="powerquery",
        )
    else:
        st.code(f'CombinedSales = Table.Combine({{{", ".join(query_names)}}})', language="powerquery")
    st.caption("Table.Combine uses column names, not column position. It preserves every input row and creates nulls where a source does not contain an output column.")
    st.download_button(
        "Download the current append practice files (.zip)",
        data=append_practice_zip(tables),
        file_name="append-queries-practice-files.zip",
        mime="application/zip",
        key=f"append_download_{scenario}_{normalize_headers}_{inject_duplicate}",
        use_container_width=True,
    )


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


def detailed_model_lab() -> None:
    lab_banner("Interactive star-schema laboratory", "Test relationship design with a realistic Sales fact and four dimensions. Duplicate keys, filter direction and output rows respond together.")
    model = sample_model_tables()
    products = model["Product"].copy()
    introduce_duplicate = st.toggle("Introduce a duplicate ProductKey in the Product dimension", key="model_duplicate_key")
    bidirectional = st.toggle("Use bidirectional filtering everywhere", key="model_bidirectional")
    if introduce_duplicate:
        duplicate = products.iloc[[0]].copy()
        duplicate["Product"] = "Business Laptop · duplicate master row"
        products = pd.concat([products, duplicate], ignore_index=True)
    relation_state = "warning" if introduce_duplicate else "active"
    filter_label = "Both directions · ambiguity risk" if bidirectional else "Dimension → fact · recommended"
    st.markdown(
        f'''<div class="model-map">
          <div class="model-table"><b>Date dimension</b><span>Date is unique · 1 → *</span></div>
          <div class="model-table {relation_state}"><b>Product dimension</b><span>{"Duplicate P01 · relationship invalid" if introduce_duplicate else "ProductKey unique · 1 → *"}</span></div>
          <div class="model-table"><b>Customer dimension</b><span>CustomerKey unique · 1 → *</span></div>
          <div class="model-table"><b>Budget table</b><span>Region target · separate grain</span></div>
          <div class="model-table fact"><b>Sales fact</b><span>One row per invoice-product transaction · repeated foreign keys · {filter_label}</span></div>
        </div>''',
        unsafe_allow_html=True,
    )
    category = st.selectbox("Filter from Product dimension", ["All categories", "Hardware", "Services"], key="model_category")
    valid_product_keys = model["Product"]["ProductKey"] if category == "All categories" else model["Product"].loc[model["Product"]["Category"] == category, "ProductKey"]
    filtered_sales = model["Sales"][model["Sales"]["ProductKey"].isin(valid_product_keys)]
    joined = model["Sales"].merge(products[["ProductKey", "Product", "Category"]], on="ProductKey", how="left")
    metrics = st.columns(4)
    metrics[0].metric("Fact rows", len(model["Sales"]))
    metrics[1].metric("Rows after master join", len(joined), f"{len(joined)-len(model['Sales']):+d}")
    metrics[2].metric("Visible sales", f"AED {filtered_sales['NetAmount'].sum():,.0f}")
    metrics[3].metric("Product key status", "Duplicate" if introduce_duplicate else "Unique")
    if introduce_duplicate:
        st.error("Relationship control failed: ProductKey is no longer unique on the one side. Joining P01 multiplies matching Sales rows and can overstate totals.")
    elif bidirectional:
        st.warning("The keys are valid, but bidirectional filtering everywhere can create ambiguous paths. Use single-direction dimension-to-fact filtering unless a tested requirement justifies otherwise.")
    else:
        st.success("Valid star schema: unique dimension keys filter repeated fact keys in one predictable direction.")
    dimension_tab, fact_tab, joined_tab = st.tabs(["Product dimension", "Sales fact", "Joined diagnostic"])
    with dimension_tab:
        st.dataframe(products, hide_index=True, use_container_width=True)
    with fact_tab:
        st.dataframe(model["Sales"], hide_index=True, use_container_width=True)
    with joined_tab:
        st.dataframe(joined[["InvoiceID", "ProductKey", "Product", "Quantity", "NetAmount"]], hide_index=True, use_container_width=True)
    st.download_button(
        "Download star-schema practice tables (.zip)",
        dataframes_zip([(f"{name}.csv", table) for name, table in model.items()]),
        "star-schema-practice.zip",
        "application/zip",
        key="model_download",
        use_container_width=True,
    )


def detailed_dax_lab() -> None:
    lab_banner("Interactive DAX and filter-context laboratory", "Change slicers and measures to see the same reusable DAX expression recalculate under a different filter context.")
    model = sample_model_tables()
    sales = model["Sales"].merge(model["Product"][["ProductKey", "Product", "Category"]], on="ProductKey").merge(model["Customer"][["CustomerKey", "Region"]], on="CustomerKey")
    region = st.selectbox("Region filter", ["All regions", "Dubai", "Sharjah", "Ajman"], key="dax_region")
    category = st.selectbox("Category filter", ["All categories", "Hardware", "Services"], key="dax_category")
    measure = st.selectbox("Measure", ["Net Sales", "Gross Margin", "Gross Margin %", "Average Invoice Value"], key="dax_measure")
    filtered = sales.copy()
    if region != "All regions":
        filtered = filtered[filtered["Region"] == region]
    if category != "All categories":
        filtered = filtered[filtered["Category"] == category]
    values = {
        "Net Sales": filtered["NetAmount"].sum(),
        "Gross Margin": filtered["GrossMargin"].sum(),
        "Gross Margin %": filtered["GrossMargin"].sum() / filtered["NetAmount"].sum() if filtered["NetAmount"].sum() else 0,
        "Average Invoice Value": filtered.groupby("InvoiceID")["NetAmount"].sum().mean() if len(filtered) else 0,
    }
    dax = {
        "Net Sales": "Net Sales = SUM(Sales[NetAmount])",
        "Gross Margin": "Gross Margin = SUM(Sales[GrossMargin])",
        "Gross Margin %": "Gross Margin % = DIVIDE([Gross Margin], [Net Sales])",
        "Average Invoice Value": "Average Invoice Value = AVERAGEX(VALUES(Sales[InvoiceID]), [Net Sales])",
    }
    region_chip = region.replace("All regions", "All")
    category_chip = category.replace("All categories", "All")
    st.markdown(f'<div class="context-strip"><span>Report filter · {region_chip}</span><span>Visual filter · {category_chip}</span><span>Measure · {measure}</span><span>Rows visible · {len(filtered)}</span></div>', unsafe_allow_html=True)
    display_value = f"{values[measure]:.1%}" if measure == "Gross Margin %" else f"AED {values[measure]:,.0f}"
    c1, c2 = st.columns([.55, 1.45])
    with c1:
        st.metric(measure, display_value)
        st.code(dax[measure], language="text")
        st.caption("The measure definition stays unchanged; the result changes because the filter context changes.")
    with c2:
        product_summary = filtered.groupby("Product", as_index=False)[["NetAmount", "GrossMargin"]].sum().set_index("Product")
        st.bar_chart(product_summary)
    st.dataframe(filtered[["InvoiceID", "InvoiceDate", "Region", "Product", "Quantity", "NetAmount", "GrossMargin"]], hide_index=True, use_container_width=True)
    st.download_button("Download DAX practice model (.zip)", dataframes_zip([("Sales.csv", model["Sales"]), ("Product.csv", model["Product"]), ("Customer.csv", model["Customer"])]), "dax-filter-context-practice.zip", "application/zip", key="dax_download", use_container_width=True)


def detailed_visual_lab() -> None:
    lab_banner("Interactive visual-selection laboratory", "Start with the business question, test a visual type and compare it with the recommended analytical form using the same finance dataset.")
    model = sample_model_tables()
    sales = model["Sales"].merge(model["Product"][["ProductKey", "Product", "Category"]], on="ProductKey").merge(model["Customer"][["CustomerKey", "Customer", "Region"]], on="CustomerKey")
    question = st.selectbox(
        "Business question",
        ["How is sales changing over time?", "Which product contributes most?", "What is total gross margin?", "Which transactions support the total?", "Is higher sales associated with higher margin?"],
        key="visual_question",
    )
    recommendations = {
        "How is sales changing over time?": "Line chart",
        "Which product contributes most?": "Sorted bar chart",
        "What is total gross margin?": "Card",
        "Which transactions support the total?": "Matrix / table",
        "Is higher sales associated with higher margin?": "Scatter plot",
    }
    visual = st.selectbox("Visual to test", ["Line chart", "Sorted bar chart", "Card", "Matrix / table", "Scatter plot"], index=["Line chart", "Sorted bar chart", "Card", "Matrix / table", "Scatter plot"].index(recommendations[question]), key="visual_choice")
    st.markdown(f'<div class="lab-summary"><b>Recommended starting point · {recommendations[question]}</b><p>Choose a visual because its structure matches the analytical question, not because it is visually decorative.</p></div>', unsafe_allow_html=True)
    if visual == "Line chart":
        monthly = sales.assign(Month=sales["InvoiceDate"].dt.to_period("M").astype(str)).groupby("Month", as_index=True)[["NetAmount", "GrossMargin"]].sum()
        st.line_chart(monthly)
    elif visual == "Sorted bar chart":
        by_product = sales.groupby("Product", as_index=False)["NetAmount"].sum().sort_values("NetAmount").set_index("Product")
        st.bar_chart(by_product)
    elif visual == "Card":
        st.metric("Gross margin", f"AED {sales['GrossMargin'].sum():,.0f}", f"{sales['GrossMargin'].sum()/sales['NetAmount'].sum():.1%} of sales")
    elif visual == "Matrix / table":
        matrix = pd.pivot_table(sales, index="Region", columns="Category", values="NetAmount", aggfunc="sum", fill_value=0, margins=True)
        st.dataframe(matrix.style.format("AED {:,.0f}"), use_container_width=True)
    else:
        customers = sales.groupby("Customer", as_index=False).agg(NetSales=("NetAmount", "sum"), GrossMargin=("GrossMargin", "sum"), Transactions=("InvoiceID", "nunique"))
        st.scatter_chart(customers, x="NetSales", y="GrossMargin", size="Transactions", color="#177c72")
        st.dataframe(customers, hide_index=True, use_container_width=True)
    if visual == recommendations[question]:
        st.success("The selected visual fits the question's comparison structure.")
    else:
        st.warning(f"This visual can display the data, but {recommendations[question]} is the clearer starting point for the selected question.")
    st.download_button("Download visual-design sample (.csv)", sales.to_csv(index=False), "visual-design-practice.csv", "text/csv", key="visual_download", use_container_width=True)


def detailed_report_experience_lab() -> None:
    lab_banner("Interactive report-experience laboratory", "Move from executive overview to performance driver to transaction evidence while preserving the selected business context.")
    model = sample_model_tables()
    sales = model["Sales"].merge(model["Product"][["ProductKey", "Product", "Category"]], on="ProductKey").merge(model["Customer"][["CustomerKey", "Customer", "Region"]], on="CustomerKey")
    page = st.segmented_control("Report page", ["Executive overview", "Margin drivers", "Transaction evidence"], default="Executive overview", key="report_page")
    region = st.selectbox("Persistent region filter", ["All regions", "Dubai", "Sharjah", "Ajman"], key="report_region")
    filtered = sales if region == "All regions" else sales[sales["Region"] == region]
    pages = ["Executive overview", "Margin drivers", "Transaction evidence"]
    path_html = "".join(f'<div class="{"active" if item == page else ""}"><b>{index + 1}. {item}</b><span>{"Current page" if item == page else "Available next step"}</span></div>' for index, item in enumerate(pages))
    st.markdown(f'<div class="report-path">{path_html}</div>', unsafe_allow_html=True)
    if page == "Executive overview":
        metrics = st.columns(3)
        metrics[0].metric("Net sales", f"AED {filtered['NetAmount'].sum():,.0f}")
        metrics[1].metric("Gross margin", f"AED {filtered['GrossMargin'].sum():,.0f}")
        metrics[2].metric("Margin %", f"{filtered['GrossMargin'].sum()/filtered['NetAmount'].sum():.1%}")
        monthly = filtered.assign(Month=filtered["InvoiceDate"].dt.to_period("M").astype(str)).groupby("Month", as_index=True)["NetAmount"].sum()
        st.line_chart(monthly)
        st.info("Overview answers what happened. Select Margin drivers to explain why, then Transaction evidence to validate the detail.")
    elif page == "Margin drivers":
        drivers = filtered.groupby(["Category", "Product"], as_index=False)[["NetAmount", "GrossMargin"]].sum().sort_values("GrossMargin")
        st.bar_chart(drivers.set_index("Product")[["NetAmount", "GrossMargin"]])
        st.dataframe(drivers, hide_index=True, use_container_width=True)
        st.info("Driver analysis compares contribution and margin. The selected region filter remains active across the page journey.")
    else:
        customers = ["All customers"] + sorted(filtered["Customer"].unique().tolist())
        customer = st.selectbox("Drillthrough customer", customers, key="report_customer")
        evidence = filtered if customer == "All customers" else filtered[filtered["Customer"] == customer]
        st.dataframe(evidence[["InvoiceID", "InvoiceDate", "Customer", "Region", "Product", "Quantity", "NetAmount", "GrossMargin"]], hide_index=True, use_container_width=True)
        st.caption(f"Drillthrough context: {region} · {customer}. Export retains the visible evidence population.")
    st.download_button("Download report-experience practice data (.csv)", sales.to_csv(index=False), "report-experience-practice.csv", "text/csv", key="report_download", use_container_width=True)


def detailed_m_lab() -> None:
    lab_banner("Interactive M language and parameter laboratory", "Change the folder parameter and transformation function to see how one reusable query processes a recurring set of files.")
    files = [
        ("Sales_Jan.csv", pd.DataFrame({"InvoiceID": ["J-101", "J-102"], "Region": ["Dubai", "Sharjah"], "Amount": [4200, 6100], "InternalNote": ["review", "ok"]})),
        ("Sales_Feb.csv", pd.DataFrame({"InvoiceID": ["F-201", "F-202", "F-203"], "Region": ["Ajman", "Dubai", "Sharjah"], "Amount": [2900, 7400, 5300], "InternalNote": ["ok", "priority", "ok"]})),
        ("Sales_Mar.csv", pd.DataFrame({"InvoiceID": ["M-301", "M-302"], "Region": ["Dubai", "Ajman"], "Amount": [8800, 3600], "InternalNote": ["priority", "review"]})),
    ]
    folder_path = st.text_input("Folder parameter", "C:/PowerBITraining/MonthlySales", key="m_folder_path")
    use_function = st.toggle("Invoke a reusable TransformFile function for every file", value=True, key="m_use_function")
    keep_columns = st.multiselect("Columns returned by the function", ["InvoiceID", "Region", "Amount", "InternalNote"], default=["InvoiceID", "Region", "Amount"], key="m_keep_columns")
    processed = []
    for filename, table in files if use_function else files[:1]:
        part = table[keep_columns].copy() if keep_columns else pd.DataFrame(index=table.index)
        part.insert(0, "Source.Name", filename)
        processed.append(part)
    combined = pd.concat(processed, ignore_index=True) if processed else pd.DataFrame()
    process_strip(
        [
            ("Folder parameter", folder_path, "active"),
            ("Folder.Files", f"{len(files)} visible CSV files", "active"),
            ("TransformFile", "Invoked per binary" if use_function else "Not invoked · first file only", "active" if use_function else "warning"),
            ("Combined query", f"{len(combined)} rows returned", "active"),
        ]
    )
    inventory = pd.DataFrame({"Name": [name for name, _ in files], "Rows": [len(table) for _, table in files], "Extension": [".csv"] * len(files), "Hidden": [False] * len(files)})
    left, right = st.columns([.8, 1.2])
    with left:
        st.markdown("#### Folder inventory")
        st.dataframe(inventory, hide_index=True, use_container_width=True)
    with right:
        st.markdown("#### Live combined output")
        st.dataframe(combined, hide_index=True, use_container_width=True)
    m_code = f'''let
    SourcePath = "{folder_path}",
    Source = Folder.Files(SourcePath),
    VisibleFiles = Table.SelectRows(Source, each [Attributes]?[Hidden]? <> true),
    Transformed = Table.AddColumn(VisibleFiles, "Data", each TransformFile([Content])),
    Combined = Table.Combine(Transformed[Data])
in
    Combined'''
    st.code(m_code, language="powerquery")
    st.info("The parameter makes the source portable; the custom function guarantees that the same transformation is applied to every current and future file.")
    st.download_button("Download M folder practice files (.zip)", dataframes_zip(files), "m-language-folder-practice.zip", "application/zip", key="m_download", use_container_width=True)


def detailed_audit_analytics_lab() -> None:
    lab_banner("Interactive audit analytics laboratory", "Adjust the anomaly concentration and investigation threshold. The Benford comparison, risk signals and transaction evidence update together.")
    transaction_count = st.select_slider("Transaction population", options=[300, 600, 1200, 2400], value=600, key="audit_population")
    anomaly = st.slider("Injected concentration on first digit 9", 0, 30, 8, key="audit_anomaly")
    threshold = st.slider("Investigation threshold · percentage-point deviation", 2.0, 10.0, 4.0, 0.5, key="audit_threshold")
    expected = {digit: math.log10(1 + 1 / digit) for digit in range(1, 10)}
    rng = random.Random(420 + transaction_count + anomaly)
    vendors = ["Alpha Supplies", "Beacon LLC", "Crescent Trading", "Delta Services", "Emirates Office"]
    rows = []
    probabilities = list(expected.values())
    digits = list(expected)
    for index in range(transaction_count):
        digit = rng.choices(digits, weights=probabilities, k=1)[0]
        if rng.random() < anomaly / 100:
            digit = 9
        magnitude = rng.choice([10, 100, 1000, 10000])
        amount = digit * magnitude + rng.uniform(0, magnitude - 0.01)
        rows.append([f"TX-{index + 1:05d}", rng.choice(vendors), round(amount, 2), digit])
    transactions = pd.DataFrame(rows, columns=["TransactionID", "Vendor", "Amount", "FirstDigit"])
    observed = transactions["FirstDigit"].value_counts(normalize=True).reindex(range(1, 10), fill_value=0)
    comparison = pd.DataFrame({"Observed": observed, "Expected": pd.Series(expected)})
    comparison.index.name = "First digit"
    comparison["Deviation_pp"] = (comparison["Observed"] - comparison["Expected"]) * 100
    flagged_digits = comparison.index[comparison["Deviation_pp"].abs() >= threshold].tolist()
    transactions["RiskSignal"] = transactions["FirstDigit"].map(lambda digit: "Review" if digit in flagged_digits else "Normal range")
    process_strip(
        [
            ("Population", f"{transaction_count:,} transactions", "active"),
            ("First digit", "Derived from absolute amount", "active"),
            ("Expected pattern", "Benford distribution", "active"),
            ("Investigation", f"{len(flagged_digits)} digits above threshold", "warning" if flagged_digits else "active"),
        ]
    )
    chart_col, table_col = st.columns([1.05, .95])
    with chart_col:
        st.markdown("#### Observed versus expected distribution")
        st.bar_chart(comparison[["Observed", "Expected"]])
        st.dataframe(comparison.style.format({"Observed": "{:.1%}", "Expected": "{:.1%}", "Deviation_pp": "{:+.1f}"}), use_container_width=True)
    with table_col:
        st.markdown("#### Transaction evidence")
        digit_filter = st.selectbox("Inspect first digit", ["Flagged digits"] + list(range(1, 10)), key="audit_digit")
        if digit_filter == "Flagged digits":
            evidence = transactions[transactions["FirstDigit"].isin(flagged_digits)]
        else:
            evidence = transactions[transactions["FirstDigit"] == digit_filter]
        st.dataframe(evidence.head(80), hide_index=True, use_container_width=True)
        st.caption(f"Evidence rows shown: {min(len(evidence),80)} of {len(evidence)}. A risk signal prioritises review; it does not prove fraud or error.")
    st.download_button("Download current audit population (.csv)", transactions.to_csv(index=False), "benford-audit-population.csv", "text/csv", key="audit_download", use_container_width=True)


def detailed_governance_lab() -> None:
    lab_banner("Interactive deployment, refresh and RLS laboratory", "Choose a source and user role to simulate the gateway path, workspace deployment and rows visible after row-level security.")
    model = sample_model_tables()
    sales = model["Sales"].merge(model["Customer"][["CustomerKey", "Customer", "Region"]], on="CustomerKey")
    source = st.selectbox("Production source", ["Cloud data warehouse", "On-premises SQL Server", "Local network file"], key="gov_source")
    role = st.selectbox("Test as role", ["Finance Admin", "Dubai Manager", "Sharjah Manager", "Ajman Manager", "Unassigned Viewer"], key="gov_role")
    refresh = st.selectbox("Refresh frequency", ["Daily at 6 AM", "Every 4 hours", "Manual only"], key="gov_refresh")
    needs_gateway = source != "Cloud data warehouse"
    role_region = {"Dubai Manager": "Dubai", "Sharjah Manager": "Sharjah", "Ajman Manager": "Ajman"}.get(role)
    visible = sales if role == "Finance Admin" else sales[sales["Region"] == role_region] if role_region else sales.iloc[0:0]
    steps = [
        ("Source", source, "warning" if needs_gateway else ""),
        ("Gateway", "Required and must be online" if needs_gateway else "Cloud connection · no gateway", "warning" if needs_gateway else ""),
        ("Workspace", f"Semantic model · {refresh}", ""),
        ("RLS role", f"{role} · {len(visible)} visible rows", "warning" if role == "Unassigned Viewer" else ""),
    ]
    governance_html = "".join(f'<div class="governance-step {state}"><b>{title}</b><span>{subtitle}</span></div>' for title, subtitle, state in steps)
    st.markdown(f'<div class="governance-grid">{governance_html}</div>', unsafe_allow_html=True)
    metrics = st.columns(3)
    metrics[0].metric("Gateway", "Required" if needs_gateway else "Not required")
    metrics[1].metric("Rows visible", len(visible), f"of {len(sales)}")
    metrics[2].metric("Visible net sales", f"AED {visible['NetAmount'].sum():,.0f}")
    mapping = pd.DataFrame({"Role": ["Finance Admin", "Dubai Manager", "Sharjah Manager", "Ajman Manager"], "Region filter": ["All", "Dubai", "Sharjah", "Ajman"], "Example assignment": ["finance-admins@company.com", "dubai-managers@company.com", "sharjah-managers@company.com", "ajman-managers@company.com"]})
    map_tab, visible_tab = st.tabs(["Security mapping", "View as role · visible rows"])
    with map_tab:
        st.dataframe(mapping, hide_index=True, use_container_width=True)
    with visible_tab:
        st.dataframe(visible[["InvoiceID", "InvoiceDate", "Customer", "Region", "NetAmount"]], hide_index=True, use_container_width=True)
    if role == "Unassigned Viewer":
        st.warning("The test user has no approved region mapping and therefore sees zero rows. Workspace access and RLS assignment must both be validated before release.")
    else:
        st.info("Use View as role in Desktop, then test assigned users in the Service. RLS controls model rows; workspace permission controls access to the content.")
    st.download_button("Download governance and RLS practice pack (.zip)", dataframes_zip([("Sales.csv", sales), ("SecurityMapping.csv", mapping)]), "governance-rls-practice.zip", "application/zip", key="gov_download", use_container_width=True)


def detailed_capstone_lab() -> None:
    lab_banner("Interactive management capstone laboratory", "Bring transformation, modelling, DAX, visual analysis, controls and management storytelling into one reconciled delivery.")
    model = sample_model_tables()
    sales = model["Sales"].merge(model["Customer"][["CustomerKey", "Customer", "Region"]], on="CustomerKey").merge(model["Product"][["ProductKey", "Product", "Category"]], on="ProductKey")
    region = st.selectbox("Management scope", ["All regions", "Dubai", "Sharjah", "Ajman"], key="capstone_region")
    inject_difference = st.toggle("Introduce an unreconciled AED 750 adjustment", key="capstone_difference")
    controls = ["Sources transformed", "Star schema validated", "Measures tested", "Exceptions traced", "Totals reconciled", "Management story rehearsed"]
    st.markdown("**Completed delivery controls**")
    completed_controls = []
    control_columns = st.columns(2)
    for index, control in enumerate(controls):
        if control_columns[index % 2].checkbox(control, value=index < 3, key=f"capstone_control_{index}"):
            completed_controls.append(control)
    visible = sales if region == "All regions" else sales[sales["Region"] == region]
    source_total = visible["NetAmount"].sum()
    model_total = source_total - (750 if inject_difference else 0)
    reconciliation_difference = source_total - model_total
    actual_by_region = sales.groupby("Region", as_index=False)["NetAmount"].sum().rename(columns={"NetAmount": "Actual"})
    performance = actual_by_region.merge(model["Budget"], on="Region", how="left")
    performance["Variance"] = performance["Actual"] - performance["Budget"]
    process_strip(
        [
            ("Prepare", "Power Query and source controls", "active" if controls[0] in completed_controls else ""),
            ("Model", "Relationships and DAX", "active" if controls[1] in completed_controls and controls[2] in completed_controls else ""),
            ("Validate", f"Difference AED {reconciliation_difference:,.0f}", "warning" if reconciliation_difference else "active"),
            ("Present", "Five-minute management story", "active" if controls[-1] in completed_controls else ""),
        ]
    )
    metrics = st.columns(4)
    metrics[0].metric("Net sales", f"AED {model_total:,.0f}")
    metrics[1].metric("Gross margin", f"AED {visible['GrossMargin'].sum():,.0f}")
    metrics[2].metric("Reconciliation difference", f"AED {reconciliation_difference:,.0f}")
    metrics[3].metric("Readiness", f"{len(completed_controls)}/{len(controls)}")
    left, right = st.columns([1.05, .95])
    with left:
        st.markdown("#### Actual versus budget")
        st.bar_chart(performance.set_index("Region")[["Actual", "Budget"]])
        st.dataframe(performance.style.format({"Actual": "AED {:,.0f}", "Budget": "AED {:,.0f}", "Variance": "AED {:+,.0f}"}), hide_index=True, use_container_width=True)
    with right:
        st.markdown("#### Management narrative")
        top = performance.sort_values("Variance", ascending=False).iloc[0]
        weak = performance.sort_values("Variance").iloc[0]
        st.markdown(f'<div class="lab-summary"><b>Headline</b><p>{top["Region"]} has the strongest variance at AED {top["Variance"]:+,.0f}; {weak["Region"]} requires attention at AED {weak["Variance"]:+,.0f}. Management should validate product mix, margin contribution and the supporting transactions before action.</p></div>', unsafe_allow_html=True)
        st.dataframe(visible[["InvoiceID", "InvoiceDate", "Customer", "Region", "Product", "NetAmount", "GrossMargin"]], hide_index=True, use_container_width=True)
    if reconciliation_difference:
        st.error("Capstone control failed: the model does not reconcile to the filtered source total. Resolve the AED 750 difference before presenting any conclusion.")
    elif len(completed_controls) < len(controls):
        st.warning("Totals reconcile, but the delivery checklist is incomplete. Finish the remaining controls before sign-off.")
    else:
        st.success("Capstone ready: the model reconciles, evidence is traceable and the management story has been rehearsed.")
    st.download_button("Download capstone practice pack (.zip)", dataframes_zip([(f"{name}.csv", table) for name, table in model.items()]), "power-bi-capstone-practice.zip", "application/zip", key="capstone_download", use_container_width=True)


def detailed_module_lab(lab_id: int) -> None:
    labs = {
        1: detailed_workflow_lab,
        2: detailed_connection_lab,
        3: detailed_power_query_lab,
        5: detailed_model_lab,
        6: detailed_dax_lab,
        7: detailed_visual_lab,
        8: detailed_report_experience_lab,
        9: detailed_m_lab,
        10: detailed_audit_analytics_lab,
        11: detailed_governance_lab,
        12: detailed_capstone_lab,
    }
    if lab_id == 4:
        append_tab, merge_tab = st.tabs(["Append Queries · Stack rows", "Merge Queries · Match keys"])
        with append_tab:
            detailed_append_lab()
        with merge_tab:
            detailed_merge_lab()
    else:
        labs[lab_id]()


def interactive_lab() -> None:
    page_header("See it, then build it", "Power BI guided lab", "Choose a topic to study the relevant Power BI screen, follow the exact click path and reproduce the technique in the supplied practice file.")
    labels = {f"{m['code']} · {m['title']}": m for m in MODULES}
    selected = labels[st.selectbox("Interactive example", list(labels))]
    st.markdown(f"### {selected['title']}")
    lab_id = selected["id"]
    guide = TOOL_LABS[lab_id]
    detailed_module_lab(lab_id)
    st.divider()
    st.subheader("Power BI screen reference")
    if lab_id == 4:
        st.caption("The interactive labs above carry the detailed explanation; these source captures show where both commands appear in Power Query.")
    else:
        st.caption("The live laboratory above explains the concept with sample data; this source capture shows where the corresponding feature appears in Power BI.")
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
        append_check, merge_check = st.tabs(["Append check", "Merge check"])
        with append_check:
            append_answer = st.radio(
                "January and February invoice files have the same grain and columns. Which operation creates one consolidated sales table?",
                ["Append Queries", "Merge Queries", "Create relationship", "Group By"],
                index=None,
                horizontal=True,
                key="append_control_answer",
            )
            if append_answer == "Append Queries":
                st.success("Correct. Append stacks the February rows below the January rows.")
            elif append_answer:
                st.warning("Review the row-flow diagram: the files describe the same kind of transaction, so they should be stacked vertically.")
        with merge_check:
            control_answer = st.radio(
                "Which join should an accountant use to list Sales Orders that have no Customer Master match?",
                ["Inner", "Left Outer", "Left Anti", "Right Anti"],
                index=None,
                horizontal=True,
                key="merge_control_answer",
            )
            if control_answer == "Left Anti":
                st.success("Correct. Left Anti keeps only non-matching rows from the primary table.")
            elif control_answer:
                st.warning("Review the highlighted regions above: the exception population is the primary-only region.")
    elif lab_id == 5:
        duplicate = st.toggle("Introduce a duplicate ProductKey in the Product dimension")
        st.write("Relationship: **Product (one) → Sales (many)**" if not duplicate else "Relationship cannot remain one-to-many because the dimension key is no longer unique.")
        if duplicate:
            st.error("Control failed: deduplicate or create a valid business key before relating tables.")
        else:
            st.success("Clean star schema: filtering is predictable.")
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


def assessment_grade(percentage: int) -> str:
    if percentage >= 90:
        return "Distinction"
    if percentage >= 80:
        return "Excellent"
    if percentage >= 70:
        return "Pass"
    return "Needs review"


def reset_assessment() -> None:
    st.session_state.assessment_answers = {}
    st.session_state.assessment_index = 0
    st.session_state.assessment_complete = False
    st.session_state.assessment_latest_score = None
    for key in list(st.session_state):
        if key.startswith("assessment_choice_"):
            del st.session_state[key]


def assessment_results() -> None:
    answers = st.session_state.assessment_answers
    score = st.session_state.assessment_latest_score or 0
    percentage = round(score / len(ASSESSMENT) * 100)
    grade = assessment_grade(percentage)
    passed = score >= PASS_SCORE
    message = "Certificate threshold achieved" if passed else "Review the missed concepts, then try again"
    st.markdown(
        f"""
        <div class="result-panel">
          <div class="result-ring"><strong>{percentage}%</strong><span>{score} of {len(ASSESSMENT)}</span></div>
          <div><span class="eyebrow">Assessment complete</span><h2>{grade}</h2><p>{message}. Your best score remains available in the sidebar and certificate area.</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if passed:
        st.success("You passed the assessment. Complete every learning module to unlock the personalized certificate.")
    else:
        st.error(f"The pass mark is {PASS_SCORE}/{len(ASSESSMENT)}. Use the review below to target your next attempt.")

    day_ranges = [("Day 1 · Prepare", 0, 6), ("Day 2 · Model", 6, 14), ("Day 3 · Scale", 14, 20)]
    cards = []
    for label, start, end in day_ranges:
        day_score = sum(answers.get(i) == ASSESSMENT[i][2] for i in range(start, end))
        cards.append(f'<div class="day-result"><strong>{day_score}/{end-start}</strong><span>{label}</span></div>')
    st.markdown(f'<div class="day-result-grid">{"".join(cards)}</div>', unsafe_allow_html=True)

    wrong = [i for i in range(len(ASSESSMENT)) if answers.get(i) != ASSESSMENT[i][2]]
    st.subheader("Answer review")
    if not wrong:
        st.info("Perfect score — every answer was correct.")
    else:
        for i in wrong:
            question, options, correct = ASSESSMENT[i]
            chosen = options[answers[i]]
            with st.expander(f"Question {i + 1} · {question}"):
                st.markdown(f"**Your answer:** {chosen}  \n**Correct answer:** {options[correct]}")
                st.info(ASSESSMENT_EXPLANATIONS[i])

    attempts = len(st.session_state.assessment_history)
    st.caption(f"Attempts completed in this learning session · {attempts}")
    c1, c2 = st.columns(2)
    if c1.button("Retake assessment", type="primary", use_container_width=True):
        reset_assessment()
        st.rerun()
    if c2.button("Review curriculum", use_container_width=True):
        st.session_state.nav = "Curriculum"
        st.rerun()


def assessment() -> None:
    page_header("Knowledge check", "Final assessment", "Work through one focused question at a time. Each answer is locked and explained immediately so the assessment also becomes a learning experience.")
    if st.session_state.assessment_complete:
        assessment_results()
        return

    answers = dict(st.session_state.assessment_answers)
    current = int(st.session_state.assessment_index)
    total = len(ASSESSMENT)
    answered = len(answers)
    st.markdown(
        f"""
        <div class="assessment-hero">
          <div><span class="eyebrow">CAP-style assessment studio</span><h2>Prove the full Power BI workflow</h2><p>Select one answer, study the immediate explanation, then continue. A score of {PASS_SCORE}/{total} unlocks the assessment requirement for your certificate.</p></div>
          <div class="assessment-kpis">
            <div class="assessment-kpi"><strong>{answered}/{total}</strong><span>Answered</span></div>
            <div class="assessment-kpi"><strong>{PASS_SCORE}/{total}</strong><span>Pass target</span></div>
            <div class="assessment-kpi"><strong>3</strong><span>Course days</span></div>
            <div class="assessment-kpi"><strong>Locked</strong><span>After selection</span></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(answered / total, text=f"Assessment progress · {answered} of {total} answered")

    nav_col, question_col = st.columns([0.72, 2.28], gap="large")
    with nav_col:
        st.markdown("#### Question navigator")
        st.caption("A check mark means the answer is locked. Select any number to revisit its explanation.")
        for row_start in range(0, total, 4):
            row = st.columns(4)
            for offset, col in enumerate(row):
                i = row_start + offset
                if i >= total:
                    continue
                label = f"✓{i + 1}" if i in answers else str(i + 1)
                if col.button(label, key=f"assessment_nav_{i}", type="primary" if i == current else "secondary", use_container_width=True):
                    st.session_state.assessment_index = i
                    st.rerun()
        remaining = total - answered
        st.markdown(
            f'<div class="question-status"><span><b>{remaining}</b> remaining</span><span><b>{answered}</b> locked</span></div>',
            unsafe_allow_html=True,
        )

    with question_col:
        question, options, correct = ASSESSMENT[current]
        day = 1 if current < 6 else 2 if current < 14 else 3
        st.markdown(
            f'<div class="question-card-head"><span>Day {day} · Question {current + 1} of {total}</span><h2>{question}</h2></div>',
            unsafe_allow_html=True,
        )
        stored = answers.get(current)
        selected = st.radio(
            "Choose one answer",
            options,
            index=stored if stored is not None else None,
            key=f"assessment_choice_{current}",
            disabled=stored is not None,
            label_visibility="collapsed",
        )
        if selected is not None and stored is None:
            answers[current] = options.index(selected)
            st.session_state.assessment_answers = answers
            st.rerun()

        if stored is not None:
            is_correct = stored == correct
            tone = "correct" if is_correct else "incorrect"
            heading = "Correct — well reasoned" if is_correct else f"Not quite — correct answer: {options[correct]}"
            st.markdown(
                f'<div class="answer-feedback {tone}"><strong>{heading}</strong><p>{ASSESSMENT_EXPLANATIONS[current]}</p></div>',
                unsafe_allow_html=True,
            )
        else:
            st.caption("Select an answer to reveal the explanation. Your first selection is final for this attempt.")

        previous_col, next_col = st.columns(2)
        if previous_col.button("← Previous", disabled=current == 0, use_container_width=True):
            st.session_state.assessment_index = current - 1
            st.rerun()
        if current < total - 1:
            if next_col.button("Next question →", disabled=stored is None, type="primary", use_container_width=True):
                st.session_state.assessment_index = current + 1
                st.rerun()
        elif answered < total:
            first_unanswered = next(i for i in range(total) if i not in answers)
            if next_col.button("Go to first unanswered", type="primary", use_container_width=True):
                st.session_state.assessment_index = first_unanswered
                st.rerun()
        elif next_col.button("Finish assessment", type="primary", use_container_width=True):
            score = sum(answers[i] == ASSESSMENT[i][2] for i in range(total))
            st.session_state.assessment_latest_score = score
            best = st.session_state.quiz_result
            st.session_state.quiz_result = max(score, best) if best is not None else score
            st.session_state.assessment_history.append({"score": score, "percentage": round(score / total * 100), "grade": assessment_grade(round(score / total * 100))})
            st.session_state.assessment_complete = True
            if score >= PASS_SCORE:
                st.balloons()
            st.rerun()


@st.cache_data(show_spinner=False)
def load_download(filename: str) -> bytes:
    return (DOWNLOAD_DIR / filename).read_bytes()


def trainer_profile() -> None:
    page_header(
        "Meet your trainer",
        "About CA Pradeep Gujaran",
        "A finance and audit leader who turns real business problems into practical learning experiences with Power BI, analytics, automation and applied AI.",
    )
    portrait = APP_DIR / "assets" / "trainer" / "pradeep-portrait.png"
    portrait_data = base64.b64encode(portrait.read_bytes()).decode("ascii") if portrait.exists() else ""
    photo_html = f'<div class="trainer-photo"><img src="data:image/png;base64,{portrait_data}" alt="CA Pradeep Gujaran portrait"></div>' if portrait_data else ""
    st.markdown(
        f"""
        <div class="trainer-hero">
          {photo_html}
          <div class="trainer-copy">
            <span class="eyebrow">Where finance meets technology</span>
            <h2>A Chartered Accountant who codes.</h2>
            <p class="trainer-role">Senior Auditor — IT & Audit Analytics · Trainer · AI builder</p>
            <p>Pradeep qualified as a Chartered Accountant with ICAI in 2011 and has more than 18 years of experience spanning finance, internal audit, IT audit, risk advisory, data analytics and emerging technology.</p>
            <p>His teaching style combines business context with hands-on construction. Learners do not only follow Power BI clicks: they learn how to define data grain, build dependable models, write measures, investigate exceptions and communicate decisions.</p>
            <div class="trainer-links"><a href="https://www.linkedin.com/in/pradeep-gujaran-botguy/" target="_blank">LinkedIn profile ↗</a><a href="https://github.com/capgujaran" target="_blank">GitHub portfolio ↗</a></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="trainer-stat-grid">
          <div class="trainer-stat"><strong>18+</strong><span>Years across audit, finance and technology</span></div>
          <div class="trainer-stat"><strong>30+</strong><span>Analytics, AI and automation tools designed</span></div>
          <div class="trainer-stat"><strong>2011</strong><span>Qualified Chartered Accountant with ICAI</span></div>
          <div class="trainer-stat"><strong>Power BI</strong><span>Certified trainer for finance and audit teams</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Selected awards and recognition")
    st.caption("Recognitions across audit innovation, AI, analytics and professional leadership.")
    awards = [
        ("2026", "UAE IAA — LPIA Award, IT Category", "Recognition with the Khalifa University audit team for the Intelligent Audit Assistant."),
        ("2025", "OpenAI × Khalifa University Code-Athon", "Recognised as a top performer in the ChatGPT Edu Code-Athon."),
        ("2024", "DDS × CODE Summit — 2nd Place", "Second among 103 participants for CertifyMe AI, built end-to-end in 72 hours."),
        ("2023", "BNI Continental — Award of Excellence", "Recognised as New Member Rockstar for outstanding contribution and referrals."),
        ("2021", "Innovation Award — Barakat Group", "Recognised for RPA and analytics-led audit automation."),
        ("2020", "Pat on the Back — Barakat Group", "Awarded for exceptional contribution to internal audit and process improvement."),
    ]
    award_html = "".join(
        f'<div class="award-card"><span class="award-year">{year}</span><b>{title}</b><p>{description}</p></div>'
        for year, title, description in awards
    )
    st.markdown(f'<div class="award-grid">{award_html}</div>', unsafe_allow_html=True)

    experience_col, training_col = st.columns([1.08, 0.92], gap="large")
    with experience_col:
        st.subheader("Experience at a glance")
        st.markdown(
            """
            <div class="experience-line">
              <div class="experience-item"><span>2024 — Present</span><b>Senior Auditor — IT & Audit Analytics</b><p>Khalifa University, Office of Internal Audit. Builds AI-enabled audit workflows, analytics and Power BI solutions.</p></div>
              <div class="experience-item"><span>2022 — 2024</span><b>Risk advisory, analytics and automation leadership</b><p>Associate Partner with RHMC Management Consultants and Smart InfoPark Technologies, followed by independent consulting engagements.</p></div>
              <div class="experience-item"><span>2016 — 2022</span><b>Internal audit and finance automation</b><p>Leadership roles with Al Ghurair and Barakat Group, including 30+ RPA solutions and advanced Power BI analytics.</p></div>
              <div class="experience-item"><span>2011 — 2016</span><b>Audit management across major industries</b><p>Internal audit roles with The Leela Hotels, Godrej & Boyce and Altisource.</p></div>
              <div class="experience-item"><span>2006 — 2011</span><b>Articleship and audit consulting</b><p>SNB Associates, covering statutory, tax, internal, interim and management audits.</p></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with training_col:
        st.subheader("Training experience")
        st.markdown(
            """
            <div class="experience-line">
              <div class="experience-item"><span>Power BI</span><b>Financial analysis and audit analytics</b><p>Hands-on workshops for professional bodies, enterprise finance teams and internal audit functions.</p></div>
              <div class="experience-item"><span>Enterprise enablement</span><b>From source files to decision-ready reports</b><p>Power BI delivery for Al Futtaim Internal Audit and other cross-functional business teams.</p></div>
              <div class="experience-item"><span>Automation</span><b>RPA, Python and Power Automate</b><p>Practical programmes linking repetitive finance processes to scalable automation.</p></div>
              <div class="experience-item"><span>Applied AI</span><b>AI for finance and audit professionals</b><p>Sessions on LLM workflows, analytics acceleration, governance and responsible adoption.</p></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("Expertise brought into this course")
    expertise = [
        ("Audit & analytics", "Internal audit, IT audit, continuous controls monitoring, risk management and audit automation."),
        ("Power BI", "Power Query, dimensional modelling, DAX, report design, deployment and governance."),
        ("Data & AI", "Python, SQL, applied machine learning, LLM APIs, document processing and analytics tools."),
        ("Automation", "UiPath, Power Automate and workflow design across finance, sales, procurement and reporting."),
        ("Business storytelling", "Turning reconciled measures and exceptions into clear management decisions."),
        ("Leadership", "Project delivery, public speaking, professional training and technology adoption."),
    ]
    expertise_html = "".join(f'<div class="expertise-card"><b>{title}</b><p>{body}</p></div>' for title, body in expertise)
    st.markdown(f'<div class="expertise-grid">{expertise_html}</div>', unsafe_allow_html=True)
    st.info("This profile is drawn from CA Pradeep Gujaran’s professional portfolio and adapted specifically for this Power BI learning programme.")


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


def certificate_document(learner_name: str, sample: bool = False) -> None:
    safe_name = escape(learner_name)
    watermark = '<div class="sample-watermark">SAMPLE</div>' if sample else ""
    st.markdown(
        f'''<div class="certificate">
        {watermark}
        <div class="certificate-kicker">Independent learning workshop</div>
        <h1>Certificate of Participation</h1>
        <div class="programme">Power BI for Finance, Reporting and Audit Analytics</div>
        <div class="presented-to">Presented to</div>
        <div class="name">{safe_name}</div>
        <p class="participation-copy">This acknowledges participation in the independent three-day workshop and completion of its guided learning activities covering data preparation, modelling, DAX, visual analysis and reporting.</p>
        <div class="certificate-meta"><span><b>{date.today().strftime("%d %B %Y")}</b></span><span>Dubai, United Arab Emirates</span><span>Three-day workshop</span></div>
        <p class="trainer-signoff">Developed and delivered by CA Pradeep Gujaran</p>
        <div class="disclaimer"><b>Disclaimer:</b> This document is issued solely as a record of participation in an independently delivered educational workshop. It is not an accredited academic or professional qualification, licence, certification or evidence of professional competency, and it carries no CPE or CPD credit unless separately approved in writing by the relevant professional body. Unless expressly confirmed through separate written authorization, it is not accredited, attested, sponsored or endorsed by any government authority, educational regulator, professional body, awarding organisation or software vendor. Power BI is a Microsoft product. This workshop is independently delivered and is neither affiliated with, nor authorized, sponsored or approved by Microsoft Corporation.</div>
        </div>''',
        unsafe_allow_html=True,
    )


def certificate() -> None:
    page_header("Participation record", "Certificate of participation", "This document records participation in the independent workshop. It is not an accredited qualification or professional certification.")
    name = st.session_state.learner_name
    modules_done = len(st.session_state.completed)
    score = st.session_state.quiz_result or 0
    eligible = bool(name) and modules_done == len(MODULES) and score >= PASS_SCORE
    c1, c2, c3 = st.columns(3)
    c1.metric("Learner name", "Ready" if name else "Missing")
    c2.metric("Modules", f"{modules_done}/{len(MODULES)}")
    c3.metric("Assessment", f"{score}/20")
    if eligible:
        certificate_document(name)
        st.info("Use your browser's Print command and choose **Save as PDF** to retain this participation record.")
    else:
        st.warning("The personalized participation record becomes available after adding your name, completing all modules and finishing the assessment. The preview below is watermarked as a sample.")
        st.subheader("Sample certificate")
        certificate_document(name or "Sample Learner", sample=True)
    st.caption("The assessment supports learning and feedback; its score is intentionally not printed on the participation document.")


inject_styles()
setup_state()
page = sidebar()
{
    "Learning home": home,
    "Curriculum": curriculum,
    "Three-day plan": three_day_plan,
    "Interactive lab": interactive_lab,
    "Assessment": assessment,
    "About the Trainer": trainer_profile,
    "Resources": resources,
    "Certificate": certificate,
}[page]()
st.markdown('<div class="credit">Power BI Learning Studio · Developed by CA Pradeep Gujaran</div>', unsafe_allow_html=True)
