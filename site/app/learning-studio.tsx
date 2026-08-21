"use client";

/* eslint-disable @next/next/no-img-element */

import { useEffect, useMemo, useState } from "react";
import rawData from "./course-data.json";

type Concept = [string, string, string, string];
type Lab = [string, string, string[], string];
type Check = [string, string[], number, string];
type Screen = [string, string, string, string[]];

type Module = {
  id: number;
  code: string;
  day: number;
  duration: string;
  lab_group?: string;
  lab_step?: number;
  title: string;
  subtitle: string;
  outcomes: string[];
  concepts: Concept[];
  lab: Lab;
  check: Check;
};

type ToolLab = {
  screen_title: string;
  screens: Screen[];
  click_path: string[];
  task: string;
  evidence: string;
};

type CourseData = {
  schedule: { day: number; theme: string; focus: string; modules: string }[];
  modules: Module[];
  assessment: [string, string[], number][];
  resources: [string, string, string][];
  toolLabs: Record<string, ToolLab>;
};

type Section = "home" | "curriculum" | "lab" | "assessment" | "resources" | "about" | "certificate";

const data = rawData as unknown as CourseData;
const PASS_SCORE = 14;
const STORAGE_KEY = "pradeep-power-bi-studio-v1";
const ANSWER_ORDERS = [
  [0, 1, 2, 3],
  [2, 0, 3, 1],
  [1, 3, 0, 2],
  [3, 2, 1, 0],
];
const ASSESSMENT_EXPLANATIONS = [
  "The supported standalone installer is PBIDesktopSetup_x64.exe. The 32-bit edition is no longer supported.",
  "Report view contains the canvas where visuals are created, positioned and formatted. Data and Model views serve different purposes.",
  "Transform Data opens Power Query Editor so the source can be inspected and cleaned before it enters the model; Load imports with the current preview settings.",
  "Keep Errors is a diagnostic filter: it retains only rows containing errors in the selected columns so the cause can be investigated. Remove the step after validation.",
  "Append stacks compatible tables vertically and preserves their rows. Merge joins columns by matching keys.",
  "A Left anti join returns rows from the first table that have no matching key in the second table, making it useful for exception testing.",
  "A fact table stores transaction-level numeric events such as quantity, sales and cost, while dimensions provide descriptive filtering attributes.",
  "The Product dimension is on the one side because ProductKey must be unique there; the Sales fact table can contain many rows for each product.",
  "A dedicated date table provides continuous dates, fiscal attributes and a consistent relationship for time-intelligence calculations.",
  "CALCULATE evaluates an expression under a modified filter context, which is central to most reusable DAX measures.",
  "DIVIDE handles a zero or blank denominator safely and can return an alternate result, unlike the plain division operator.",
  "A measure is evaluated when a visual queries the model, using the filter context created by slicers, rows, columns and relationships.",
  "A line chart makes sequential movement over time easy to read and compare, especially when the date axis is continuous.",
  "Drillthrough carries the selected entity or category context to a dedicated detail page, preserving a path from summary to evidence.",
  "The expression after the M `in` keyword is the value returned by the query; earlier named steps inside `let` support that result.",
  "A custom M function packages repeatable, parameterized transformation logic so the same cleaning process can be applied to many files or inputs.",
  "A Benford deviation is a risk indicator that identifies a population for investigation. It does not prove error or fraud by itself.",
  "An on-premises data gateway provides the managed bridge through which Power BI Service can reach supported local data sources during refresh.",
  "Row-level security filters which rows a user can see in the semantic model. It does not replace workspace permissions or source-system security.",
  "Before presenting the capstone, reconcile key totals and test filters, navigation, refresh and drillthrough so every conclusion can be traced to reliable evidence.",
];

const navItems: { id: Section; label: string }[] = [
  { id: "home", label: "Home" },
  { id: "curriculum", label: "Curriculum" },
  { id: "lab", label: "Lab studio" },
  { id: "assessment", label: "Assessment" },
  { id: "resources", label: "Resources" },
  { id: "about", label: "About" },
];

function Mark({ compact = false }: { compact?: boolean }) {
  return (
    <div className={`brand-mark ${compact ? "brand-mark--compact" : ""}`} aria-hidden="true">
      <span className="brand-mark__bar brand-mark__bar--one" />
      <span className="brand-mark__bar brand-mark__bar--two" />
      <span className="brand-mark__bar brand-mark__bar--three" />
    </div>
  );
}

function ArrowIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M5 12h13M13 6l6 6-6 6" />
    </svg>
  );
}

function DownloadIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 3v12m0 0 5-5m-5 5-5-5M5 21h14" />
    </svg>
  );
}

function SectionIntro({ eyebrow, title, copy }: { eyebrow: string; title: string; copy: string }) {
  return (
    <header className="section-intro">
      <p className="eyebrow">{eyebrow}</p>
      <h1>{title}</h1>
      <p>{copy}</p>
    </header>
  );
}

export function LearningStudio() {
  const [section, setSection] = useState<Section>("home");
  const [activeModuleId, setActiveModuleId] = useState(1);
  const [completed, setCompleted] = useState<number[]>([]);
  const [learnerName, setLearnerName] = useState("");
  const [quizAnswers, setQuizAnswers] = useState<Record<number, number>>({});
  const [assessmentAnswers, setAssessmentAnswers] = useState<Record<number, number>>({});
  const [assessmentIndex, setAssessmentIndex] = useState(0);
  const [assessmentFinished, setAssessmentFinished] = useState(false);
  const [mobileNav, setMobileNav] = useState(false);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    const frame = window.requestAnimationFrame(() => {
      const allowed = new Set(navItems.map((item) => item.id).concat(["certificate"]));
      const hash = window.location.hash.replace("#", "") as Section;
      if (allowed.has(hash)) setSection(hash);
      try {
        const saved = JSON.parse(window.localStorage.getItem(STORAGE_KEY) ?? "{}");
        if (Array.isArray(saved.completed)) setCompleted(saved.completed);
        if (typeof saved.learnerName === "string") setLearnerName(saved.learnerName);
        if (saved.assessmentAnswers) setAssessmentAnswers(saved.assessmentAnswers);
        if (saved.assessmentFinished) setAssessmentFinished(true);
      } catch {
        // A damaged local preference should never block the course.
      }
      setHydrated(true);
    });
    return () => window.cancelAnimationFrame(frame);
  }, []);

  useEffect(() => {
    if (!hydrated) return;
    window.localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({ completed, learnerName, assessmentAnswers, assessmentFinished }),
    );
  }, [completed, learnerName, assessmentAnswers, assessmentFinished, hydrated]);

  const navigate = (next: Section) => {
    setSection(next);
    setMobileNav(false);
    window.history.replaceState(null, "", `#${next}`);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const openModule = (id: number) => {
    setActiveModuleId(id);
    navigate("lab");
  };

  const assessmentScore = useMemo(
    () =>
      data.assessment.reduce(
        (score, question, index) => score + (assessmentAnswers[index] === question[2] ? 1 : 0),
        0,
      ),
    [assessmentAnswers],
  );

  const progress = Math.round((completed.length / data.modules.length) * 100);
  const certificateReady = completed.length === data.modules.length && assessmentScore >= PASS_SCORE && learnerName.trim().length > 1;

  return (
    <div className="site-shell">
      <header className="topbar">
        <button className="brand" onClick={() => navigate("home")} aria-label="Power BI Learning Studio home">
          <Mark compact />
          <span><strong>Power BI</strong><small>Learning Studio</small></span>
        </button>
        <nav className={mobileNav ? "main-nav main-nav--open" : "main-nav"} aria-label="Main navigation">
          {navItems.map((item) => (
            <button key={item.id} onClick={() => navigate(item.id)} aria-current={section === item.id ? "page" : undefined}>
              {item.label}
            </button>
          ))}
        </nav>
        <button className="progress-button" onClick={() => navigate("lab")}>
          <span>{progress}% complete</span>
          <i><b style={{ width: `${progress}%` }} /></i>
        </button>
        <button className="menu-button" onClick={() => setMobileNav((open) => !open)} aria-label="Toggle navigation" aria-expanded={mobileNav}>
          <span /><span /><span />
        </button>
      </header>

      <main>
        {section === "home" && <Home completed={completed} openModule={openModule} navigate={navigate} />}
        {section === "curriculum" && <Curriculum completed={completed} openModule={openModule} />}
        {section === "lab" && (
          <LabStudio
            activeModuleId={activeModuleId}
            setActiveModuleId={setActiveModuleId}
            completed={completed}
            setCompleted={setCompleted}
            quizAnswers={quizAnswers}
            setQuizAnswers={setQuizAnswers}
          />
        )}
        {section === "assessment" && (
          <Assessment
            answers={assessmentAnswers}
            setAnswers={setAssessmentAnswers}
            index={assessmentIndex}
            setIndex={setAssessmentIndex}
            finished={assessmentFinished}
            setFinished={setAssessmentFinished}
            score={assessmentScore}
            navigate={navigate}
          />
        )}
        {section === "resources" && <Resources />}
        {section === "about" && <About navigate={navigate} />}
        {section === "certificate" && (
          <Certificate
            name={learnerName}
            setName={setLearnerName}
            ready={certificateReady}
            completed={completed.length}
            score={assessmentScore}
          />
        )}
      </main>

      <footer className="footer">
        <div className="footer__brand"><Mark compact /><span><strong>Power BI Learning Studio</strong><small>Designed and delivered by CA Pradeep Gujaran</small></span></div>
        <p>Practical business intelligence learning for finance professionals.</p>
        <button onClick={() => navigate("certificate")}>Participation certificate →</button>
      </footer>
    </div>
  );
}

function Home({ completed, openModule, navigate }: { completed: number[]; openModule: (id: number) => void; navigate: (section: Section) => void }) {
  const next = data.modules.find((module) => !completed.includes(module.id)) ?? data.modules[0];
  const labGroups = ["Lab 1", "Lab 2", "Lab 3", "Lab 4"];

  return (
    <>
      <section className="hero">
        <div className="hero__copy">
          <p className="eyebrow">AICITSS · Power BI intensive</p>
          <h1>Turn raw business data into <em>decisions people trust.</em></h1>
          <p className="hero__lead">A rigorous three-day programme for finance professionals—built around repeatable Power Query workflows, sound models, useful DAX and evidence-led reporting.</p>
          <div className="hero__actions">
            <button className="button button--primary" onClick={() => openModule(next.id)}>{completed.length ? "Continue learning" : "Start the programme"}<ArrowIcon /></button>
            <button className="button button--quiet" onClick={() => navigate("curriculum")}>Explore curriculum</button>
          </div>
          <dl className="hero__stats">
            <div><dt>28</dt><dd>guided topics</dd></div>
            <div><dt>4</dt><dd>completed labs</dd></div>
            <div><dt>3</dt><dd>focused days</dd></div>
          </dl>
        </div>
        <div className="hero__visual" aria-label="Power BI workflow illustration">
          <div className="hero__dashboard">
            <picture>
              <source media="(min-width: 1800px)" srcSet="./assets/screenshots/homepage-dashboard-infographic-wide-v4.png" />
              <img
                src="./assets/screenshots/homepage-dashboard-infographic-v3.png"
                alt="Business intelligence infographic with aligned KPIs, trends, regional analysis and a data-to-insight workflow"
              />
            </picture>
          </div>
        </div>
      </section>

      <section className="programme-strip" aria-label="Programme promise">
        <p>From import to insight</p><span />
        <p>Built for finance teams</p><span />
        <p>Validated with real files</p>
      </section>

      <section className="home-section">
        <div className="home-section__heading">
          <div><p className="eyebrow">Hands-on progression</p><h2>Four labs. One connected workflow.</h2></div>
          <p>Each lab adds a real-world ingestion pattern and ends with a completed PBIX reference you can inspect.</p>
        </div>
        <div className="lab-grid">
          {labGroups.map((group, index) => {
            const modules = data.modules.filter((module) => module.lab_group === group);
            const done = modules.filter((module) => completed.includes(module.id)).length;
            return (
              <article className="lab-card" key={group}>
                <div className="lab-card__number">0{index + 1}</div>
                <p className="eyebrow">{group} · {modules.length} topics</p>
                <h3>{["Import and clean retail data", "Build a parameter-driven web query", "Reshape tables extracted from PDF", "Automate a folder of annual files"][index]}</h3>
                <p>{["Locale-aware typing, validation, custom columns and the M-versus-DAX decision.", "HTML extraction, a dynamic Date parameter and refresh controls.", "Staging queries, append, fill operations and receipt reconciliation.", "Combine & Transform, reusable helpers and automatic processing of 2014.xlsx."][index]}</p>
                <div className="lab-card__footer"><span>{done}/{modules.length} complete</span><button onClick={() => openModule(modules[0].id)}>Open lab <ArrowIcon /></button></div>
              </article>
            );
          })}
        </div>
      </section>

      <section className="method-section">
        <div className="method-section__quote"><span>“</span><blockquote>Good Power BI work is not a colourful report. It is a chain of evidence—from source, to transformation, to model, to decision.</blockquote><p>CA Pradeep Gujaran</p></div>
        <div className="method-section__steps">
          <p className="eyebrow">The teaching method</p>
          {[
            ["See it", "Inspect the real Power BI screen and understand the implication of each option."],
            ["Build it", "Follow a precise click path and reproduce the technique in Desktop."],
            ["Prove it", "Reconcile totals, validate errors and record evidence before moving on."],
          ].map(([title, copy], index) => <div key={title}><span>0{index + 1}</span><h3>{title}</h3><p>{copy}</p></div>)}
        </div>
      </section>
    </>
  );
}

function Curriculum({ completed, openModule }: { completed: number[]; openModule: (id: number) => void }) {
  return (
    <div className="page-wrap">
      <SectionIntro eyebrow="The full learning path" title="Curriculum built around the work" copy="Move from source control and Power Query to modelling, DAX, audit analytics and publication. Every topic has a task and an evidence requirement." />
      <div className="day-list">
        {data.schedule.map((day) => {
          const modules = data.modules.filter((module) => module.day === day.day);
          return (
            <section className="day-block" key={day.day}>
              <div className="day-block__intro"><span>Day {day.day}</span><h2>{day.theme}</h2><p>{day.focus}</p><small>Topics {day.modules}</small></div>
              <div className="topic-list">
                {modules.map((module) => (
                  <button key={module.id} onClick={() => openModule(module.id)} className={completed.includes(module.id) ? "topic-row topic-row--done" : "topic-row"}>
                    <span className="topic-row__code">{module.code}</span>
                    <span><strong>{module.title}</strong><small>{module.subtitle}</small></span>
                    <span className="topic-row__duration">{completed.includes(module.id) ? "Completed" : module.duration}</span>
                    <ArrowIcon />
                  </button>
                ))}
              </div>
            </section>
          );
        })}
      </div>
    </div>
  );
}

function LabStudio({ activeModuleId, setActiveModuleId, completed, setCompleted, quizAnswers, setQuizAnswers }: {
  activeModuleId: number;
  setActiveModuleId: (id: number) => void;
  completed: number[];
  setCompleted: (ids: number[]) => void;
  quizAnswers: Record<number, number>;
  setQuizAnswers: (answers: Record<number, number>) => void;
}) {
  const topic = data.modules.find((item) => item.id === activeModuleId) ?? data.modules[0];
  const topicIndex = data.modules.findIndex((item) => item.id === topic.id);
  const tool = data.toolLabs[String(topic.id)];
  const selectedAnswer = quizAnswers[topic.id];
  const isDone = completed.includes(topic.id);
  const [search, setSearch] = useState("");
  const visibleModules = data.modules.filter((item) => `${item.code} ${item.title} ${item.lab_group ?? ""}`.toLowerCase().includes(search.toLowerCase()));

  const toggleComplete = () => setCompleted(isDone ? completed.filter((id) => id !== topic.id) : [...completed, topic.id]);

  return (
    <div className="studio-layout">
      <aside className="topic-sidebar">
        <div className="topic-sidebar__heading"><p className="eyebrow">Guided lab studio</p><h2>Topics</h2><p>{completed.length} of {data.modules.length} complete</p></div>
        <label className="topic-search"><span>Search topics</span><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Power Query, DAX…" /></label>
        <div className="topic-sidebar__list">
          {visibleModules.map((item) => (
            <button key={item.id} onClick={() => setActiveModuleId(item.id)} className={item.id === topic.id ? "active" : ""}>
              <i className={completed.includes(item.id) ? "status-dot status-dot--done" : "status-dot"} />
              <span><small>{item.lab_group ? `${item.lab_group} · ` : ""}{item.code}</small><strong>{item.title}</strong></span>
            </button>
          ))}
        </div>
      </aside>

      <article className="topic-content">
        <header className="topic-hero">
          <div><p className="eyebrow">{topic.lab_group ? `${topic.lab_group} · Topic ${topic.lab_step}` : `Day ${topic.day} · ${topic.code}`}</p><h1>{topic.title}</h1><p>{topic.subtitle}</p></div>
          <div className="topic-hero__meta"><span>{topic.duration}</span><span>Day {topic.day}</span><span>{isDone ? "Completed" : "In progress"}</span></div>
        </header>

        <section className="content-section outcomes-panel"><p className="eyebrow">Learning outcomes</p><div>{topic.outcomes.map((outcome, index) => <p key={outcome}><span>{String(index + 1).padStart(2, "0")}</span>{outcome}</p>)}</div></section>

        {tool?.screens?.length ? (
          <section className="content-section"><div className="content-heading"><p className="eyebrow">Screen walkthrough</p><h2>{tool.screen_title}</h2></div>
            <div className="screen-stack">{tool.screens.map(([title, filename, caption, points]) => (
              <figure className="screen-card" key={filename}><div className="screen-card__image"><img src={`./assets/screenshots/${filename}`} alt={title} loading="lazy" /></div><figcaption><p className="eyebrow">{title}</p><p>{caption}</p><ul>{points.map((point) => <li key={point}>{point}</li>)}</ul></figcaption></figure>
            ))}</div>
          </section>
        ) : null}

        <section className="content-section"><div className="content-heading"><p className="eyebrow">Understand the idea</p><h2>Concepts before clicks</h2></div>
          <div className="concept-grid">{topic.concepts.map(([title, explanation, example, implication], index) => (
            <article className="concept-card" key={title}><span>0{index + 1}</span><h3>{title}</h3><p>{explanation}</p><div><small>Example</small><p>{example}</p></div><footer>{implication}</footer></article>
          ))}</div>
        </section>

        <section className="content-section lab-instructions"><div className="content-heading"><p className="eyebrow">Reproduce it in Power BI</p><h2>{topic.lab[0]}</h2><p>Starting point: {topic.lab[1]}</p></div>
          <ol>{(tool?.click_path ?? topic.lab[2]).map((step, index) => <li key={`${index}-${step}`}><span>{String(index + 1).padStart(2, "0")}</span><p>{step}</p></li>)}</ol>
          <div className="evidence-grid"><div><small>Student task</small><p>{tool?.task ?? topic.lab[0]}</p></div><div><small>Evidence to produce</small><p>{tool?.evidence ?? topic.lab[3]}</p></div></div>
        </section>

        <section className="content-section knowledge-check"><div><p className="eyebrow">Check your understanding</p><h2>{topic.check[0]}</h2></div>
          <div className="answer-grid">{topic.check[1].map((answer, index) => {
            const answered = selectedAnswer !== undefined;
            const correct = index === topic.check[2];
            const selected = selectedAnswer === index;
            const className = answered && correct ? "answer answer--correct" : answered && selected ? "answer answer--wrong" : "answer";
            return <button key={answer} className={className} onClick={() => setQuizAnswers({ ...quizAnswers, [topic.id]: index })} disabled={answered}><span>{String.fromCharCode(65 + index)}</span>{answer}</button>;
          })}</div>
          {selectedAnswer !== undefined && <p className={selectedAnswer === topic.check[2] ? "feedback feedback--correct" : "feedback feedback--wrong"}>{selectedAnswer === topic.check[2] ? "Correct. " : "Not quite. "}{topic.check[3]}</p>}
        </section>

        <div className="topic-actions">
          <button className="button button--quiet" disabled={topicIndex === 0} onClick={() => setActiveModuleId(data.modules[topicIndex - 1].id)}>← Previous topic</button>
          <button className={isDone ? "button button--completed" : "button button--primary"} onClick={toggleComplete}>{isDone ? "✓ Topic completed" : "Mark topic complete"}</button>
          <button className="button button--quiet" disabled={topicIndex === data.modules.length - 1} onClick={() => setActiveModuleId(data.modules[topicIndex + 1].id)}>Next topic →</button>
        </div>
      </article>
    </div>
  );
}

function Assessment({ answers, setAnswers, index, setIndex, finished, setFinished, score, navigate }: {
  answers: Record<number, number>;
  setAnswers: (answers: Record<number, number>) => void;
  index: number;
  setIndex: (index: number) => void;
  finished: boolean;
  setFinished: (finished: boolean) => void;
  score: number;
  navigate: (section: Section) => void;
}) {
  const question = data.assessment[index];
  const answered = Object.keys(answers).length;
  const passed = score >= PASS_SCORE;
  const selectedAnswer = answers[index];
  const optionOrder = ANSWER_ORDERS[index % ANSWER_ORDERS.length];
  const explanation = ASSESSMENT_EXPLANATIONS[index];

  if (finished) {
    return <div className="page-wrap assessment-results"><SectionIntro eyebrow="Assessment complete" title={`${score} out of ${data.assessment.length}`} copy={passed ? "You have reached the assessment threshold. Complete every learning topic to unlock your participation certificate." : "Review the missed concepts in the Lab studio, then retake the assessment when ready."} />
      <div className={passed ? "result-band result-band--pass" : "result-band"}><span>{Math.round((score / data.assessment.length) * 100)}%</span><div><p className="eyebrow">{passed ? "Threshold achieved" : "Review recommended"}</p><h2>{passed ? "Strong evidence of understanding" : "Use the feedback as your next study plan"}</h2></div></div>
      <div className="result-actions"><button className="button button--quiet" onClick={() => { setAnswers({}); setIndex(0); setFinished(false); }}>Retake assessment</button><button className="button button--primary" onClick={() => navigate(passed ? "certificate" : "lab")}>{passed ? "View certificate status" : "Return to lab studio"}<ArrowIcon /></button></div>
    </div>;
  }

  return <div className="page-wrap assessment-page">
    <SectionIntro eyebrow="Final knowledge check" title="Prove the full workflow" copy="Work through one focused question at a time. Your answers are saved on this device, so you can continue without a server session." />
    <div className="assessment-progress"><span>Question {index + 1} of {data.assessment.length}</span><div><i style={{ width: `${((index + 1) / data.assessment.length) * 100}%` }} /></div><span>{answered} answered</span></div>
    <section className="question-card"><p className="eyebrow">Select one answer</p><h2>{question[0]}</h2><div className="answer-grid answer-grid--assessment">{optionOrder.map((originalIndex, displayIndex) => {
      const isCorrect = originalIndex === question[2];
      const isSelected = selectedAnswer === originalIndex;
      const className = selectedAnswer !== undefined && isCorrect
        ? "answer answer--correct"
        : selectedAnswer !== undefined && isSelected
          ? "answer answer--wrong"
          : "answer";
      return <button key={question[1][originalIndex]} className={className} disabled={selectedAnswer !== undefined} onClick={() => setAnswers({ ...answers, [index]: originalIndex })}><span>{String.fromCharCode(65 + displayIndex)}</span>{question[1][originalIndex]}</button>;
    })}</div>
      {selectedAnswer !== undefined && <p className={selectedAnswer === question[2] ? "feedback feedback--correct" : "feedback feedback--wrong"}><strong>{selectedAnswer === question[2] ? "Correct. " : "Incorrect. "}</strong>{explanation}</p>}
    </section>
    <div className="assessment-actions"><button className="button button--quiet" disabled={index === 0} onClick={() => setIndex(index - 1)}>← Previous</button><div className="question-dots">{data.assessment.map((_, itemIndex) => <button key={itemIndex} className={itemIndex === index ? "active" : answers[itemIndex] !== undefined ? "answered" : ""} onClick={() => setIndex(itemIndex)} aria-label={`Question ${itemIndex + 1}`} />)}</div>{index < data.assessment.length - 1 ? <button className="button button--primary" disabled={answers[index] === undefined} onClick={() => setIndex(index + 1)}>Next question <ArrowIcon /></button> : <button className="button button--primary" disabled={answered < data.assessment.length} onClick={() => setFinished(true)}>Finish assessment <ArrowIcon /></button>}</div>
  </div>;
}

function Resources() {
  const labs = data.resources.filter((resource) => /Lab [1-4]/i.test(resource[0]));
  const references = data.resources.filter((resource) => !labs.includes(resource));
  return <div className="page-wrap resources-page"><SectionIntro eyebrow="Course library" title="Files for practice and proof" copy="Download source packs before a lab and use completed PBIX files only after you have validated your own result." />
    <ResourceGroup title="Labs 1–4" resources={labs} />
    <ResourceGroup title="Reference library" resources={references} />
  </div>;
}

function ResourceGroup({ title, resources }: { title: string; resources: [string, string, string][] }) {
  return <section className="resource-group"><div className="resource-group__title"><p className="eyebrow">Download collection</p><h2>{title}</h2></div><div className="resource-list">{resources.map(([name, description, filename]) => <article key={filename}><div className="file-type">{filename.split(".").pop()?.toUpperCase()}</div><div><h3>{name}</h3><p>{description}</p></div><a href={`./assets/downloads/${filename}`} download><DownloadIcon /><span>Download</span></a></article>)}</div></section>;
}

function About({ navigate }: { navigate: (section: Section) => void }) {
  const awards = [
    ["2026", "UAE IAA — LPIA Award, IT Category", "Recognition with the Khalifa University audit team for the Intelligent Audit Assistant."],
    ["2025", "OpenAI × Khalifa University Code-Athon", "Recognised as a top performer in the ChatGPT Edu Code-Athon."],
    ["2024", "DDS × CODE Summit — 2nd Place", "Second among 103 participants for CertifyMe AI, built end-to-end in 72 hours."],
    ["2023", "BNI Continental — Award of Excellence", "Recognised as New Member Rockstar for outstanding contribution and referrals."],
    ["2021", "Innovation Award — Barakat Group", "Recognised for RPA and analytics-led audit automation."],
    ["2020", "Pat on the Back — Barakat Group", "Awarded for exceptional contribution to internal audit and process improvement."],
  ];
  const experience = [
    ["2024 — Present", "Senior Auditor — IT & Audit Analytics", "Khalifa University, Office of Internal Audit. Builds AI-enabled audit workflows, analytics and Power BI solutions."],
    ["2022 — 2024", "Risk advisory, analytics and automation leadership", "Associate Partner with RHMC Management Consultants and Smart InfoPark Technologies, followed by independent consulting engagements."],
    ["2016 — 2022", "Internal audit and finance automation", "Leadership roles with Al Ghurair and Barakat Group, including 30+ RPA solutions and advanced Power BI analytics."],
    ["2011 — 2016", "Audit management across major industries", "Internal audit roles with The Leela Hotels, Godrej & Boyce and Altisource."],
    ["2006 — 2011", "Articleship and audit consulting", "SNB Associates, covering statutory, tax, internal, interim and management audits."],
  ];
  const training = [
    ["Power BI", "Financial analysis and audit analytics", "Hands-on workshops for professional bodies, enterprise finance teams and internal audit functions."],
    ["Enterprise enablement", "From source files to decision-ready reports", "Power BI delivery for Al Futtaim Internal Audit and other cross-functional business teams."],
    ["Automation", "RPA, Python and Power Automate", "Practical programmes linking repetitive finance processes to scalable automation."],
    ["Applied AI", "AI for finance and audit professionals", "Sessions on LLM workflows, analytics acceleration, governance and responsible adoption."],
  ];
  const expertise = [
    ["Audit & analytics", "Internal audit, IT audit, continuous controls monitoring, risk management and audit automation."],
    ["Power BI", "Power Query, dimensional modelling, DAX, report design, deployment and governance."],
    ["Data & AI", "Python, SQL, applied machine learning, LLM APIs, document processing and analytics tools."],
    ["Automation", "UiPath, Power Automate and workflow design across finance, sales, procurement and reporting."],
    ["Business storytelling", "Turning reconciled measures and exceptions into clear management decisions."],
    ["Leadership", "Project delivery, public speaking, professional training and technology adoption."],
  ];

  return <div className="about-page">
    <section className="about-hero">
      <div className="about-hero__image"><img src="./assets/trainer/pradeep-portrait.png" alt="CA Pradeep Gujaran" /></div>
      <div className="about-hero__copy"><p className="eyebrow">Where finance meets technology</p><h1>A Chartered Accountant who codes.</h1><p className="about-role">Senior Auditor — IT & Audit Analytics · Trainer · AI builder</p><p>Pradeep qualified as a Chartered Accountant with ICAI in 2011 and has more than 18 years of experience spanning finance, internal audit, IT audit, risk advisory, data analytics and emerging technology.</p><p>His teaching style combines business context with hands-on construction. Learners do not only follow Power BI clicks: they learn how to define data grain, build dependable models, write measures, investigate exceptions and communicate decisions.</p><div className="trainer-links"><a href="https://www.linkedin.com/in/pradeep-gujaran-botguy/" target="_blank" rel="noreferrer">LinkedIn profile ↗</a><a href="https://github.com/capgujaran" target="_blank" rel="noreferrer">GitHub portfolio ↗</a></div><button className="button button--primary" onClick={() => navigate("curriculum")}>Explore the programme <ArrowIcon /></button></div>
    </section>

    <section className="trainer-stats" aria-label="Trainer profile highlights"><article><strong>18+</strong><span>Years across audit, finance and technology</span></article><article><strong>30+</strong><span>Analytics, AI and automation tools designed</span></article><article><strong>2011</strong><span>Qualified Chartered Accountant with ICAI</span></article><article><strong>Power BI</strong><span>Certified trainer for finance and audit teams</span></article></section>

    <section className="profile-section"><div className="profile-heading"><p className="eyebrow">Selected recognition</p><h2>Awards across audit innovation, AI and analytics.</h2></div><div className="award-grid">{awards.map(([year, title, copy]) => <article key={title}><span>{year}</span><h3>{title}</h3><p>{copy}</p></article>)}</div></section>

    <section className="profile-section profile-columns"><div><div className="profile-heading"><p className="eyebrow">Professional journey</p><h2>Experience at a glance</h2></div><div className="experience-list">{experience.map(([period, title, copy]) => <article key={period}><span>{period}</span><h3>{title}</h3><p>{copy}</p></article>)}</div></div><div><div className="profile-heading"><p className="eyebrow">Knowledge transfer</p><h2>Training experience</h2></div><div className="experience-list">{training.map(([area, title, copy]) => <article key={area}><span>{area}</span><h3>{title}</h3><p>{copy}</p></article>)}</div></div></section>

    <section className="profile-section"><div className="profile-heading"><p className="eyebrow">Course perspective</p><h2>Expertise brought into this programme</h2></div><div className="expertise-grid">{expertise.map(([title, copy], index) => <article key={title}><span>0{index + 1}</span><h3>{title}</h3><p>{copy}</p></article>)}</div><p className="profile-note">This profile is drawn from CA Pradeep Gujaran’s professional portfolio and adapted specifically for this Power BI learning programme.</p></section>
  </div>;
}

function Certificate({ name, setName, ready, completed, score }: { name: string; setName: (name: string) => void; ready: boolean; completed: number; score: number }) {
  return <div className="page-wrap certificate-page"><SectionIntro eyebrow="Participation record" title="Your course certificate" copy="Add your name, complete all 28 topics and score at least 14/20 in the assessment. Progress remains stored on this device." />
    <label className="name-field"><span>Learner name</span><input value={name} onChange={(event) => setName(event.target.value)} placeholder="Enter your full name" /></label>
    <div className="unlock-status"><div className={name.trim().length > 1 ? "done" : ""}><span>{name.trim().length > 1 ? "✓" : "1"}</span><p><strong>Add your name</strong><small>Personalises the participation record</small></p></div><div className={completed === data.modules.length ? "done" : ""}><span>{completed === data.modules.length ? "✓" : "2"}</span><p><strong>Complete every topic</strong><small>{completed}/{data.modules.length} completed</small></p></div><div className={score >= PASS_SCORE ? "done" : ""}><span>{score >= PASS_SCORE ? "✓" : "3"}</span><p><strong>Pass the assessment</strong><small>{score}/{data.assessment.length} · target {PASS_SCORE}</small></p></div></div>
    <section className={ready ? "certificate certificate--ready" : "certificate certificate--locked"}><div className="certificate__frame"><Mark /><p className="eyebrow">Certificate of participation</p><h2>This acknowledges that</h2><h3>{name.trim() || "Learner name"}</h3><p>has completed the three-day <strong>Power BI Learning Studio</strong> programme covering data preparation, modelling, DAX, reporting, audit analytics and publication.</p><div className="certificate__signatures"><div><span>CA Pradeep Gujaran</span><small>Programme trainer</small></div><div><span>{ready ? new Date().toLocaleDateString("en-GB", { day: "2-digit", month: "long", year: "numeric" }) : "Completion date"}</span><small>Date</small></div></div><p className="certificate__disclaimer"><strong>Disclaimer:</strong> This document is issued solely as a record of participation in an independently delivered educational workshop. It is not an accredited academic or professional qualification, licence, certification or evidence of professional competency, and it carries no CPE or CPD credit unless separately approved in writing by the relevant professional body. Unless expressly confirmed through separate written authorization, it is not accredited, attested, sponsored or endorsed by any government authority, educational regulator, professional body, awarding organisation or software vendor. Power BI is a Microsoft product. This workshop is independently delivered and is neither affiliated with, nor authorized, sponsored or approved by Microsoft Corporation.</p>{!ready && <div className="certificate__watermark">Preview</div>}</div></section>
    <button className="button button--primary print-button" disabled={!ready} onClick={() => window.print()}>Print participation record</button>
  </div>;
}
