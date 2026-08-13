"""Course content for the three-day Power BI programme."""

SCHEDULE = [
    {"day": 1, "theme": "Connect, clean and shape", "focus": "Power BI foundations, data sources, Power Query and combining data", "modules": "1–4"},
    {"day": 2, "theme": "Model, calculate and communicate", "focus": "Data modelling, DAX, visual design and report experience", "modules": "5–8"},
    {"day": 3, "theme": "Automate, audit and publish", "focus": "M language, audit analytics, Power BI Service and capstone", "modules": "9–12"},
]

MODULES = [
    {
        "id": 1, "code": "D1.1", "day": 1, "duration": "60 min",
        "title": "Power BI and the analytics workflow",
        "subtitle": "Move from a finance question to a governed decision",
        "outcomes": ["Explain the roles of Desktop, Service and mobile", "Distinguish models, reports and dashboards", "Frame a decision-first analytics question"],
        "concepts": [
            ("The Power BI ecosystem", "Desktop is the authoring environment for connections, transformations, models and reports. The Service distributes, governs and refreshes content; mobile apps provide an optimized consumption experience.", "A finance analyst builds a margin model in Desktop, publishes it to a controlled Finance workspace and the CFO reviews it on a tablet.", "Desktop creates; the Service distributes and governs; mobile consumes."),
            ("Model, report and dashboard", "A semantic model contains tables, relationships and business calculations. A report contains interactive pages based on a model. A dashboard is a single Service canvas of pinned tiles and may combine several reports.", "One sales model can support management P&L, working-capital and executive reporting.", "These objects have different purposes—do not call every report page a dashboard."),
            ("Question-first analytics", "Define the decision, user, grain, measure, period and benchmark before selecting a visual.", "Replace ‘show sales’ with ‘Which country and product category caused the monthly margin shortfall versus budget?’", "A useful report makes a decision easier."),
        ],
        "lab": ("Map the reporting solution", "Retail invoice scenario", ["Write the decision and primary user", "Identify grain, measures, dimensions and refresh frequency", "Choose the correct Power BI artefacts", "Sketch the journey from source to action"], "A one-page solution map"),
        "check": ("Which Power BI component is primarily used to create the data model?", ["Power BI Desktop", "Power BI mobile", "A Service dashboard", "An email subscription"], 0, "Power BI Desktop is the main authoring environment for transformations, modelling and report design."),
    },
    {
        "id": 2, "code": "D1.2", "day": 1, "duration": "75 min",
        "title": "Connect to finance data",
        "subtitle": "Choose the right connector, grain and refresh approach",
        "outcomes": ["Connect to files, folders, databases and web sources", "Assess source grain and quality", "Select Import or DirectQuery deliberately"],
        "concepts": [
            ("Source and connector", "Connectors understand a source's authentication and structure. File, Folder, SQL Server, Web and SharePoint Folder connectors solve different ingestion patterns.", "Use Folder when monthly extracts share the same columns and must be appended automatically.", "Choose a connector for the source and operating process, not only today's file."),
            ("Grain and keys", "Grain describes what one row represents. A key identifies a row or business entity and enables reliable relationships.", "An invoice-header table has one row per invoice; an invoice-lines table has one row per product line.", "Never build a model until you can state each table's grain."),
            ("Import and DirectQuery", "Import copies data into the model for speed and flexibility. DirectQuery leaves data at source and sends queries during interaction, trading flexibility and performance for source-level immediacy.", "A modest monthly finance dataset normally suits Import; a very large governed warehouse with near-real-time needs may justify DirectQuery.", "Mode is an architectural choice, not a speed switch."),
        ],
        "lab": ("Profile a messy sales extract", "Country-wise sales workbooks", ["Connect to the supplied files", "Inspect column quality and distribution", "Confirm row grain and candidate keys", "Document errors, blanks and refresh assumptions"], "A source profiling note and connection plan"),
        "check": ("What should be confirmed before relating two tables?", ["Their page background", "Their grain and keys", "Their visual colours", "Their bookmark names"], 1, "Grain and keys determine whether a relationship is valid and how it will filter."),
    },
    {
        "id": 3, "code": "D1.3", "day": 1, "duration": "105 min",
        "title": "Power Query for reliable data",
        "subtitle": "Turn repeatable cleaning steps into an auditable pipeline",
        "outcomes": ["Use profiling tools and applied steps", "Set types and handle errors", "Reshape data with split, fill, unpivot and group"],
        "concepts": [
            ("Applied steps", "Power Query records each transformation in order. Clear names and a deliberate step sequence make the pipeline understandable and repeatable.", "Promote headers, set types, remove blank rows and rename fields once; refresh replays the process.", "Every manual edit that matters should become a repeatable transformation."),
            ("Data types and errors", "Types control sorting, arithmetic, relationships and date intelligence. Converting invalid values can expose errors that should be investigated rather than silently discarded.", "The text value ‘N/A’ in an Amount column should be replaced or flagged before converting to decimal.", "Type early enough to reveal quality issues, but after obvious cleanup."),
            ("Wide to tidy", "Unpivot converts repeating period columns into attribute-value rows, producing a scalable table for visuals and calculations.", "Transform Jan, Feb and Mar columns into Month and Amount rows.", "Tidy structures grow by rows, not new columns."),
        ],
        "lab": ("Build a refreshable cleaning query", "Messy journal and sales extracts", ["Enable column quality, profile and distribution", "Remove title rows and promote headers", "Standardize types and handle invalid values", "Unpivot period columns and rename steps"], "A documented, refreshable Power Query pipeline"),
        "check": ("Why is Unpivot valuable for monthly columns?", ["It creates one chart per month", "It converts repeating columns into scalable rows", "It removes all totals", "It encrypts the source"], 1, "Unpivot creates an attribute-value structure that supports filtering, calculation and future periods."),
    },
    {
        "id": 4, "code": "D1.4", "day": 1, "duration": "90 min",
        "title": "Combine data with append and merge",
        "subtitle": "Stack recurring extracts and enrich transactions safely",
        "outcomes": ["Differentiate append from merge", "Select join types using business meaning", "Validate row counts after combining data"],
        "concepts": [
            ("Append", "Append stacks tables vertically when they represent the same grain and broadly compatible columns.", "Stack January, February and March transaction exports into one Sales fact table.", "Append adds rows."),
            ("Merge", "Merge joins columns from a second table using matching keys and a selected join type.", "Enrich invoice lines with customer segment using CustomerKey.", "Merge adds columns, but duplicates in the lookup can multiply rows."),
            ("Join choice and validation", "Left outer keeps every row from the primary table; inner keeps matches only; anti joins isolate exceptions. Always reconcile row counts and unmatched keys.", "A left anti join between journal lines and the account master reveals unmapped account codes.", "A successful refresh is not proof of a correct join."),
        ],
        "lab": ("Create a consolidated sales table", "Regional sales files and masters", ["Append recurring sales files", "Merge product and customer attributes", "Use an anti join to locate unmatched keys", "Reconcile rows and totals before and after"], "A reconciled consolidated fact table"),
        "check": ("Which join isolates transaction keys missing from a master?", ["Left anti", "Full outer only", "Cross join", "Append"], 0, "A left anti join returns rows from the first table that have no match in the second."),
    },
    {
        "id": 5, "code": "D2.1", "day": 2, "duration": "90 min",
        "title": "Design a finance-ready data model",
        "subtitle": "Build a star schema with predictable filter flow",
        "outcomes": ["Separate facts from dimensions", "Create one-to-many relationships", "Use a dedicated date table"],
        "concepts": [
            ("Star schema", "A fact table stores events and numeric observations; dimensions describe the people, products, accounts, dates and entities used to group them.", "Sales sits at invoice-line grain and connects to Date, Product, Customer and Geography dimensions.", "A simple star usually produces simpler DAX and predictable filtering."),
            ("Cardinality and filter direction", "The dimension key is unique on the one side; repeated foreign keys appear on the many side. Single-direction filtering from dimension to fact is the safest default.", "One Product row filters many Sales rows through ProductKey.", "Many-to-many and bidirectional filters need a clear business reason."),
            ("Date table", "A complete, contiguous date table enables consistent year, quarter, month and time-intelligence calculations.", "Relate Date[Date] to Sales[InvoiceDate] and sort Month Name by Month Number.", "One governed calendar is better than several hidden date tables."),
        ],
        "lab": ("Model sales, budget and returns", "Sales, target, product and calendar tables", ["Classify fact and dimension tables", "Create unique dimension keys", "Build relationships and test filter flow", "Create and mark a date table"], "A clean star-schema model diagram"),
        "check": ("What is the preferred default filter direction in a star schema?", ["From fact to every dimension", "Both directions everywhere", "From dimension to fact", "No relationships"], 2, "Single-direction filtering from dimensions to facts is predictable and reduces ambiguity."),
    },
    {
        "id": 6, "code": "D2.2", "day": 2, "duration": "120 min",
        "title": "DAX measures and filter context",
        "subtitle": "Translate finance logic into reusable business calculations",
        "outcomes": ["Create explicit measures", "Explain row and filter context", "Use CALCULATE, iterators and safe division"],
        "concepts": [
            ("Measures versus calculated columns", "A calculated column is evaluated row by row during refresh and stored. A measure is evaluated at query time under the current filter context.", "Net Sales should normally be a measure because it must respond to country, product and date filters.", "Use columns for row attributes; use measures for aggregations."),
            ("CALCULATE", "CALCULATE evaluates an expression under a modified filter context. It is the foundation of ratios, period comparisons and conditional business logic.", "Prior Year Sales = CALCULATE([Sales], SAMEPERIODLASTYEAR('Date'[Date])).", "Read CALCULATE as: evaluate this expression under these filters."),
            ("Iterators and DIVIDE", "X-functions such as SUMX evaluate an expression row by row over a table. DIVIDE safely handles zero or blank denominators.", "Margin % = DIVIDE([Gross Margin], [Net Sales]).", "Correct totals depend on understanding evaluation context, not formatting."),
        ],
        "lab": ("Create a management measure pack", "Sales, cost, returns and budget model", ["Create base measures for sales, cost and quantity", "Calculate gross margin and margin percentage", "Add actual-versus-budget variance", "Validate totals under several filters"], "A documented library of reusable measures"),
        "check": ("Which function changes filter context before evaluating an expression?", ["FORMAT", "CALCULATE", "CONCATENATE", "RELATEDTABLE only"], 1, "CALCULATE evaluates an expression under modified filters."),
    },
    {
        "id": 7, "code": "D2.3", "day": 2, "duration": "75 min",
        "title": "Visual analytics that communicates",
        "subtitle": "Match visual form to the finance question",
        "outcomes": ["Choose visuals by analytical purpose", "Apply accessible formatting", "Avoid misleading scales and clutter"],
        "concepts": [
            ("Purpose before chart", "Use bars for comparison, lines for trends, cards for headline values, matrices for detailed statements and scatter plots for relationships.", "A monthly revenue trend belongs in a line chart; country variance comparisons belong in sorted bars.", "Choose the visual that makes the pattern easiest to see."),
            ("Visual hierarchy", "A page should guide attention from key outcomes to drivers and detail through position, size, spacing and limited accent colour.", "Place KPI cards and the primary variance visual in the first viewing area; keep reconciliation detail lower.", "Emphasis should reflect decision importance."),
            ("Honest design", "Use appropriate baselines, meaningful units, readable labels and accessible contrast. Avoid decorative elements that compete with data.", "A bar chart starting near the maximum exaggerates a small variance; a line chart may legitimately use a focused range when clearly labelled.", "Clarity is a control, not decoration."),
        ],
        "lab": ("Build an executive performance page", "Sales and budget model", ["Select one headline decision", "Create KPI, trend and driver visuals", "Apply consistent number formats and titles", "Test cross-filtering and mobile readability"], "A one-page executive performance report"),
        "check": ("Which visual is usually best for comparing variance across categories?", ["Sorted bar chart", "Gauge for every category", "Decorative map", "Unlabelled pie with many slices"], 0, "Sorted bars make category magnitude and rank easy to compare."),
    },
    {
        "id": 8, "code": "D2.4", "day": 2, "duration": "75 min",
        "title": "Design the report experience",
        "subtitle": "Create purposeful navigation, interaction and narrative",
        "outcomes": ["Control interactions and drill paths", "Use tooltips, bookmarks and buttons", "Design a coherent multi-page story"],
        "concepts": [
            ("Interaction design", "Cross-filtering, slicers and drillthrough should answer natural follow-up questions without creating unexpected state.", "Selecting a country filters the trend and category drivers; drillthrough opens its transaction detail.", "Every interaction should have an understandable result."),
            ("Bookmarks and buttons", "Bookmarks capture report state and can support navigation, reset actions and alternate views. Buttons make the action discoverable.", "A Reset Filters button returns the page to an approved default state.", "Use bookmarks for a user journey, not as a substitute for a sound model."),
            ("Narrative pages", "Give each page a specific audience and question. Use consistent navigation and progressive detail.", "Overview → Margin drivers → Customer exceptions → Transaction detail.", "One page, one primary question."),
        ],
        "lab": ("Turn pages into a guided report", "Executive dashboard PBIX", ["Define the question for each page", "Configure interactions and drillthrough", "Add tooltip and navigation pages", "Create reset and view-toggle bookmarks"], "A guided, testable report experience"),
        "check": ("What is a strong use for a bookmark?", ["Repairing broken relationships", "Capturing a reset or alternate report state", "Replacing source data", "Creating a database index"], 1, "Bookmarks capture report state and are useful for navigation, reset and alternate views."),
    },
    {
        "id": 9, "code": "D3.1", "day": 3, "duration": "75 min",
        "title": "Power Query M and reusable logic",
        "subtitle": "Read generated code and create maintainable transformations",
        "outcomes": ["Read let/in expressions", "Use variables and functions", "Create parameters for portable queries"],
        "concepts": [
            ("let and in", "An M query defines named steps inside a let block and returns the expression named after in. Each step can reference an earlier step.", "let Source = Excel.Workbook(...), Data = Source{[Item=\"Sales\"]}[Data] in Data", "The final in expression controls what the query returns."),
            ("Functions", "A custom function packages parameterized logic that can be invoked for many files or values.", "A TransformFile function applies the same column cleanup to every monthly workbook.", "Functions remove repeated manual transformation logic."),
            ("Parameters", "Parameters externalize changing values such as folder paths, cut-off dates and environment names.", "Switch a SourcePath parameter from the trainer folder to the learner folder without rewriting steps.", "Separate configuration from transformation logic."),
        ],
        "lab": ("Parameterize a folder ingestion query", "Monthly finance extracts", ["Open Advanced Editor and trace each step", "Create a folder-path parameter", "Convert cleanup logic into a function", "Invoke it across files and validate schema"], "A portable, reusable M query"),
        "check": ("In an M query, what does the expression after ‘in’ do?", ["Selects the returned step", "Creates a visual", "Publishes a workspace", "Changes DAX context"], 0, "The expression after in is the value returned by the query."),
    },
    {
        "id": 10, "code": "D3.2", "day": 3, "duration": "105 min",
        "title": "Audit analytics and anomaly detection",
        "subtitle": "Use Power BI to surface risk indicators without overstating evidence",
        "outcomes": ["Design exception tests", "Apply Benford analysis appropriately", "Separate indicators from conclusions"],
        "concepts": [
            ("Exception tests", "Rules can flag weekends, duplicates, round values, unusual users, missing masters or entries near approval limits.", "Flag journal entries posted on weekends with round amounts above a defined threshold.", "A flag prioritizes review; it does not prove wrongdoing."),
            ("Benford's Law", "In suitable naturally occurring datasets, leading digits often follow a predictable logarithmic distribution. Compare observed and expected frequencies, then investigate material deviations.", "Analyze the first digit of positive transaction amounts after excluding assigned numbers and constrained ranges.", "Suitability, population size and business context come before the chart."),
            ("Evidence trail", "An audit dashboard should allow reviewers to move from summary risk signals to the underlying transaction and document the test definition.", "A high-risk supplier count drills to invoices, approvers, dates and source identifiers.", "Reproducibility is part of audit quality."),
        ],
        "lab": ("Create an audit exception dashboard", "General ledger and payment transactions", ["Define risk questions and exclusion rules", "Build weekend, duplicate and round-value flags", "Compare observed leading digits with Benford expectations", "Create drillthrough to transaction evidence"], "An exception dashboard with a documented methodology"),
        "check": ("What does a Benford deviation establish by itself?", ["Fraud is proven", "The records must be deleted", "A population may warrant investigation", "The audit is complete"], 2, "A deviation is an analytical indicator that may justify further investigation; it is not proof."),
    },
    {
        "id": 11, "code": "D3.3", "day": 3, "duration": "75 min",
        "title": "Publish, secure and refresh",
        "subtitle": "Move from a desktop file to governed organisational use",
        "outcomes": ["Organize workspaces and apps", "Configure refresh and gateways", "Apply row-level security and lineage thinking"],
        "concepts": [
            ("Workspace and app", "A workspace is the collaboration and content-management area for developers. An app is a curated distribution package for consumers.", "Finance develops and validates in a controlled workspace, then publishes an app to managers.", "Separate authoring access from consumption access."),
            ("Refresh and gateway", "Cloud sources can often refresh directly. On-premises sources generally need a gateway that securely brokers queries without copying credentials into the report.", "A scheduled refresh accesses an on-premises SQL finance database through an enterprise gateway.", "Test credentials, privacy levels and refresh ownership before handover."),
            ("Security and governance", "Row-level security filters model rows by role or user. Sensitivity, endorsement, lineage and controlled permissions support trusted reuse.", "Regional managers see only their entities through a user-to-region mapping table.", "RLS controls rows; it is not a substitute for workspace permission design."),
        ],
        "lab": ("Prepare a deployment runbook", "Completed management report", ["Choose workspace roles and app audiences", "Define refresh ownership and gateway needs", "Design and test an RLS mapping", "Record endorsement, lineage and support responsibilities"], "A practical deployment and governance checklist"),
        "check": ("What is the usual purpose of a Power BI app?", ["Curated distribution to consumers", "Editing source CSV files", "Writing M without Desktop", "Replacing all workspace permissions"], 0, "An app distributes a curated collection of content to a defined audience."),
    },
    {
        "id": 12, "code": "D3.4", "day": 3, "duration": "120 min",
        "title": "Capstone: management and audit dashboard",
        "subtitle": "Integrate the complete workflow and present a defensible result",
        "outcomes": ["Deliver an end-to-end Power BI solution", "Reconcile outputs to source", "Explain design and control decisions"],
        "concepts": [
            ("End-to-end discipline", "A strong solution connects a defined decision to controlled ingestion, a sound model, validated measures and an intentional report experience.", "The team traces one KPI from source row through Power Query, relationship, DAX and final visual.", "The chain is only as reliable as its weakest link."),
            ("Validation", "Reconcile row counts, control totals, filter behaviour, edge cases and representative transactions. Record assumptions and known limitations.", "Net sales agrees to the supplied control total, including returns and blank product mappings.", "Validate both numbers and behaviour."),
            ("Presentation", "Explain the question, model, insight, recommended action and governance plan. Demonstrate drill paths and respond to challenge.", "Present the margin shortfall, isolate its drivers and show the evidence page supporting action.", "A dashboard presentation should end with a decision or next step."),
        ],
        "lab": ("Build and present the final solution", "Sales, returns, budget and audit datasets", ["Profile and transform the supplied data", "Create a star model and measure pack", "Design management and audit report pages", "Reconcile, peer review and present the recommendation"], "A complete PBIX solution and five-minute presentation"),
        "check": ("Which is the strongest final validation?", ["The colour theme looks consistent", "One card has the expected number", "Source totals, filter behaviour and transactions reconcile", "The PBIX opens without errors"], 2, "Reliable validation covers totals, behaviour and representative records, not only appearance."),
    },
]

ASSESSMENT = [
    ("Which tool is the primary authoring environment?", ["Power BI Desktop", "Power BI Mobile", "PowerPoint", "A dashboard tile"], 0),
    ("What does table grain describe?", ["The colour palette", "What one row represents", "The refresh button", "The report owner"], 1),
    ("Which storage mode usually gives the fastest interactive experience for modest datasets?", ["Import", "DirectQuery", "Live screenshot", "CSV preview"], 0),
    ("What does Unpivot do?", ["Converts repeating columns into rows", "Deletes nulls", "Creates relationships", "Publishes an app"], 0),
    ("Which operation stacks monthly files vertically?", ["Merge", "Append", "Pivot chart", "Drillthrough"], 1),
    ("Which join returns unmatched rows from the first table?", ["Left anti", "Inner", "Cross", "Right outer only"], 0),
    ("In a star schema, where are transaction amounts normally stored?", ["Fact table", "Date dimension", "Tooltip page", "Workspace"], 0),
    ("The unique Product table sits on which side of a Product-to-Sales relationship?", ["Many", "One", "Inactive only", "Disconnected"], 1),
    ("Why use a dedicated date table?", ["To enable consistent time analysis", "To store passwords", "To replace all dimensions", "To make bars yellow"], 0),
    ("Which DAX function changes filter context?", ["CALCULATE", "UPPER", "FORMAT", "LEN"], 0),
    ("Which expression safely calculates a ratio?", ["DIVIDE([Margin], [Sales])", "[Margin] & [Sales]", "FORMAT([Margin])", "COUNTROWS([Margin])"], 0),
    ("A measure is evaluated primarily when?", ["At query time under filter context", "Only when typed", "Only during installation", "Inside Power Query"], 0),
    ("Which visual best shows a time trend?", ["Line chart", "Gauge", "Pie with 20 slices", "Single card"], 0),
    ("What can a drillthrough page provide?", ["Context-specific detail", "A new database", "Automatic source correction", "A gateway"], 0),
    ("What follows the `in` keyword in M?", ["The returned expression", "A DAX measure", "A workspace role", "A visual theme"], 0),
    ("A custom M function is useful for what?", ["Repeating parameterized transformations", "Assigning licences", "Creating RLS roles", "Drawing shapes"], 0),
    ("What does a Benford deviation prove?", ["Nothing by itself; it signals review", "Fraud", "A duplicate", "The model is correct"], 0),
    ("What usually connects on-premises data to scheduled refresh?", ["Gateway", "Bookmark", "Tooltip", "Mobile layout"], 0),
    ("What does row-level security control?", ["Which model rows a user can see", "Report colours", "Source file names", "Licence pricing"], 0),
    ("What is essential before presenting the capstone?", ["Reconcile totals and test behaviour", "Add animations", "Hide all assumptions", "Remove source identifiers"], 0),
]

RESOURCES = [
    ("Day 1 · Data preparation labs", "Queries, cleaning, folder ingestion and combining exercises", "day-1-data-preparation-labs.zip"),
    ("Day 2 · Model and DAX labs", "Model-building, calculations and report-design exercises", "day-2-model-dax-labs.zip"),
    ("Day 3 · Audit analytics labs", "Audit tests, Benford analysis and capstone inputs", "day-3-audit-analytics-labs.zip"),
    ("Course reference · Power BI module", "Detailed reference material supporting the learning pathway", "icai-aicitss-module-2-power-bi.pdf"),
    ("Sales dashboard · Starter PBIX", "Starter file for guided modelling and visual exercises", "sales-dashboard-starter.pbix"),
    ("Sales dashboard · Reference PBIX", "Completed reference solution for comparison", "sales-dashboard-reference.pbix"),
    ("Sales and returns · Reference PBIX", "Model with sales and returns analysis", "sales-and-returns-reference.pbix"),
    ("Merge lab · Reference PBIX", "Compact completed merge example", "merge-lab-reference.pbix"),
    ("Executive dashboard · Completed PBIX", "Completed dashboard for report-experience practice", "power-bi-dashboard-completed.pbix"),
    ("Benford audit · Reference PBIX", "Completed leading-digit analysis example", "benford-audit-reference.pbix"),
    ("Bonus business challenge", "Additional datasets and open-ended tasks", "bonus-business-challenge-pack.zip"),
]


TOOL_LABS = {
    1: {
        "screen_title": "Recognise the Power BI workspace",
        "screens": [
            ("Power BI Service", "01-power-bi-service.jpeg", "A published dashboard in the Power BI Service, with navigation, tiles and the online workspace visible.", ["Left navigation for workspaces and content", "Dashboard tiles used for monitoring", "The online Service is a consumption and governance surface"]),
        ],
        "click_path": ["Open Power BI Desktop and identify Report, Data and Model views on the left rail", "Open an existing PBIX and locate the report pages, canvas and panes", "Use Home > Publish only after confirming the target workspace"],
        "task": "Write down which part of your solution belongs in Desktop and which part belongs in the Service. Use one finance reporting example.",
        "evidence": "A two-column Desktop vs Service solution note",
    },
    2: {
        "screen_title": "Connect through Get Data",
        "screens": [
            ("Connector gallery", "02-get-data-connectors.jpeg", "The Get Data dialog groups file, database, Azure, online-service and other connectors.", ["The connector controls authentication and navigation", "Choose the connector that matches the operating process", "Select More to search the full connector catalogue"]),
            ("Database connection", "02-sql-connection.png", "A SQL Server connection dialog showing server, database and connectivity settings.", ["Server and database identify the source", "Import and DirectQuery have different operating consequences", "Advanced SQL should be governed and documented"]),
        ],
        "click_path": ["Home > Get data > More", "Choose the source type and enter its connection details", "Use Navigator to confirm the table names and preview", "Choose Transform Data instead of Load when quality work is required"],
        "task": "Connect to one supplied file, state its row grain and identify its candidate business key before loading it.",
        "evidence": "A source profile containing grain, key, row count and refresh assumption",
    },
    3: {
        "screen_title": "Work inside Power Query Editor",
        "screens": [
            ("Power Query Editor", "03-power-query-editor.png", "A working Power Query Editor window with the ribbon, data preview, formula bar and Applied Steps visible.", ["Queries are listed on the left", "The centre grid previews the selected query", "Applied Steps on the right record the transformation sequence", "The formula bar reveals the M expression behind a selected step"]),
        ],
        "click_path": ["Home > Transform data", "View > enable Formula bar, Column quality, Column distribution and Column profile", "Select a column and inspect type, valid values, errors and blanks", "Rename each important Applied Step so another reviewer can follow the logic", "Home > Close & Apply only after reconciliation"],
        "task": "Clean the supplied journal or sales extract, then select each Applied Step and explain what changed and why.",
        "evidence": "A refreshable query with descriptive step names and no unexplained errors",
    },
    4: {
        "screen_title": "Append rows and merge attributes",
        "screens": [
            ("Append Queries", "04-append-queries.jpeg", "The Append dialog used to stack compatible tables vertically.", ["Append adds rows", "Column names and data types should be aligned", "Use Append as New when the source queries should remain available"]),
            ("Merge Queries", "04-merge-queries.jpeg", "The Merge dialog used to match two tables by one or more selected keys.", ["Merge adds columns", "The selected key sequence must match", "Join kind determines which matched and unmatched rows survive"]),
        ],
        "click_path": ["Power Query Home > Append Queries > Append Queries as New for recurring extracts", "Select the tables and verify aligned columns", "Home > Merge Queries > Merge Queries as New for enrichment", "Select the key in both previews and choose the join kind", "Expand only the required columns, then reconcile rows and totals"],
        "task": "Append the regional sales files, merge the product master, and use a Left Anti join to isolate unmapped products.",
        "evidence": "A consolidated fact query plus an exceptions query for unmatched keys",
    },
    5: {
        "screen_title": "Build and inspect the model",
        "screens": [
            ("Star schema", "05-model-star-schema.png", "Model view showing a central fact table connected to descriptive dimensions.", ["Fact table sits at the transaction grain", "Dimensions filter the fact through one-to-many relationships", "A dedicated Date table supports consistent time analysis"]),
            ("Relationship paths", "05-model-relationships.png", "A more developed model showing active relationship paths across several tables.", ["Solid lines are active relationships", "Arrow direction shows filter propagation", "Technical bridge tables should solve a defined modelling problem"]),
        ],
        "click_path": ["Select Model view on the left rail", "Place fact tables centrally and dimensions around them", "Drag a unique dimension key to the matching fact foreign key", "Open relationship properties and verify cardinality and cross-filter direction", "Use Manage relationships to inspect inactive or ambiguous paths"],
        "task": "Create the Date, Product, Customer and Geography relationships, then test that each dimension filters Sales correctly.",
        "evidence": "A clean model diagram with one-to-many, single-direction relationships",
    },
    6: {
        "screen_title": "Write DAX in the formula bar",
        "screens": [
            ("DAX calculation", "06-dax-formula.png", "Model view with the DAX formula bar active while a calculated table is being defined.", ["The formula bar is where DAX is authored", "Field and table references must be unambiguous", "A calculation belongs in the model, not in a visual title or manual spreadsheet"]),
        ],
        "click_path": ["Modeling > New measure", "Enter a base measure such as Net Sales = SUM(Sales[NetAmount])", "Add Gross Margin and Gross Margin % using DIVIDE", "Place the measure in a table visual", "Apply country and date filters and confirm the result changes correctly"],
        "task": "Create Net Sales, Gross Margin, Margin %, Budget Variance and Prior Year Sales as explicit measures.",
        "evidence": "A measure table with business-friendly names, formats and validated totals",
    },
    7: {
        "screen_title": "Build a visual from the report canvas",
        "screens": [
            ("Visualizations pane", "07-visualizations-pane.jpeg", "A report visual selected with its field wells and available visual types visible.", ["Select visual type by analytical purpose", "Place fields in the correct wells", "Formatting should clarify hierarchy rather than decorate the page"]),
        ],
        "click_path": ["Select Report view", "Choose a visual from the Visualizations pane", "Drag dimensions and measures into the relevant field wells", "Sort, format numbers and write a question-led title", "Use Format > Edit interactions to test cross-filter behaviour"],
        "task": "Build one KPI, one monthly trend and one sorted category-variance visual. Explain why each visual fits its question.",
        "evidence": "A clean analysis page with consistent titles, units and accessible contrast",
    },
    8: {
        "screen_title": "Turn visuals into a report experience",
        "screens": [
            ("Multi-visual report page", "08-report-experience.png", "A completed report page combining KPIs, trends and drivers into a guided analytical view.", ["Headline values are visible first", "Trend and driver visuals answer natural follow-up questions", "Page and visual state should remain understandable after interaction"]),
        ],
        "click_path": ["Create Overview, Drivers and Transaction Detail pages", "Insert > Buttons > Navigator > Page navigator", "Add a drillthrough field to the detail page", "View > Bookmarks and Selection to create a Reset Filters state", "Test the path from headline KPI to underlying transactions"],
        "task": "Create a three-page navigation path and a drillthrough page that retains the selected entity context.",
        "evidence": "A report journey that moves from overview to driver to transaction evidence",
    },
    9: {
        "screen_title": "Read the M code behind the query",
        "screens": [
            ("Advanced Editor", "09-advanced-editor.jpeg", "The Power Query Advanced Editor displaying a let/in expression created from transformation steps.", ["Named expressions appear between let and in", "Each step can reference an earlier step", "The expression after in is the query result"]),
        ],
        "click_path": ["Power Query Editor > View > Advanced Editor", "Locate the let block and the expression after in", "Rename one generated step and observe the code change", "Home > Manage Parameters > New Parameter", "Replace the hard-coded source path with the parameter"],
        "task": "Parameterize the folder path and convert the repeated file-cleaning sequence into a reusable function.",
        "evidence": "A portable query with a readable let/in structure and no hard-coded learner path",
    },
    10: {
        "screen_title": "Review an audit analytics report",
        "screens": [
            ("Benford first-digit analysis", "10-benford-analysis.png", "A Power BI report comparing observed first-digit frequencies with the expected Benford distribution and listing transactions for review.", ["Observed and expected patterns are compared visually", "The transaction table supports investigation", "A deviation is a risk indicator, not a conclusion of fraud"]),
        ],
        "click_path": ["Create a First Digit column from absolute transaction amount", "Create observed count and observed percentage measures", "Create or relate an expected Benford table", "Plot observed and expected percentages by first digit", "Add drillthrough or a detail table for the flagged population"],
        "task": "Build the first-digit comparison and investigate the largest deviations using the supplied transaction detail.",
        "evidence": "A documented exception report with population rules and transaction-level evidence",
    },
    11: {
        "screen_title": "Configure refresh and security",
        "screens": [
            ("Gateway management", "11-gateway-settings.jpeg", "Power BI Service settings showing the gateway management entry point.", ["Gateways connect the Service to supported on-premises sources", "Refresh ownership and credentials require deliberate handover", "Gateway availability must be tested before go-live"]),
            ("Row-level security", "11-row-level-security.png", "A row-level security role being defined for a model table.", ["A role contains the filter rule", "Users or groups are assigned after publishing", "Use View as role in Desktop before distribution"]),
        ],
        "click_path": ["Desktop > Modeling > Manage roles and define the row filter", "Modeling > View as to test every role", "Home > Publish and choose the controlled workspace", "Service > semantic model settings > configure credentials and refresh", "Service > Security > assign the approved users or groups"],
        "task": "Design a regional-manager role and a deployment checklist covering workspace access, refresh owner and gateway dependency.",
        "evidence": "A tested RLS role and a practical deployment runbook",
    },
    12: {
        "screen_title": "Study the completed capstone pattern",
        "screens": [
            ("Management dashboard", "12-capstone-dashboard.png", "A completed Power BI dashboard combining KPIs, category analysis, maps, trends and detail views.", ["KPIs answer the opening management question", "Drivers and trends explain performance", "Detailed visuals preserve a path to evidence", "The whole page uses a consistent visual language"]),
        ],
        "click_path": ["Transform and reconcile the supplied source files", "Create the star schema and explicit measure pack", "Build Overview, Performance Drivers and Audit Exceptions pages", "Add navigation, drillthrough and reset interactions", "Reconcile control totals and present a five-minute recommendation"],
        "task": "Rebuild the capstone from the starter PBIX, then compare your choices with the reference solution only after validation.",
        "evidence": "A complete PBIX, reconciliation note and five-minute management presentation",
    },
}
