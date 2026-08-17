"""Course content for the three-day Power BI programme."""

SCHEDULE = [
    {"day": 1, "theme": "Install, explore and import", "focus": "Power BI Desktop installation, interface tour, CSV import, error isolation and locale correction", "modules": "1–4"},
    {"day": 2, "theme": "Model, calculate and communicate", "focus": "Data modelling, DAX, visual design and report experience", "modules": "5–8"},
    {"day": 3, "theme": "Automate, audit and publish", "focus": "M language, audit analytics, Power BI Service and capstone", "modules": "9–12"},
]

MODULES = [
    {
        "id": 1, "code": "D1.1", "day": 1, "duration": "35 min",
        "title": "Install Power BI Desktop",
        "subtitle": "Use the Microsoft Store or the supported 64-bit installer",
        "outcomes": ["Choose between the Microsoft Store and direct-download routes", "Identify the supported 64-bit installer", "Launch Power BI Desktop and confirm the installation"],
        "concepts": [
            ("Microsoft Store route", "The Microsoft Store installs the latest Power BI Desktop and normally keeps it updated automatically. It also avoids a full installer download for every monthly update.", "Open the official Power BI Desktop Store page and select Install.", "Use the Store route when it is available and permitted on the learner's device."),
            ("Direct 64-bit route", "The official Microsoft Download Center provides PBIDesktopSetup_x64.exe for organizations or devices that use a standalone installer. The 32-bit edition is no longer supported.", "Select PBIDesktopSetup_x64.exe, download it and complete the setup wizard.", "Download only from Microsoft and choose the x64 installer."),
            ("Version readiness", "Power BI Desktop receives monthly updates. Keeping the trainer and learners on a recent version reduces file-compatibility and feature differences during the workshop.", "Open Help > About after installation and note the installed version.", "Use a current supported release and confirm the app opens before the lab begins."),
        ],
        "lab": ("Install and verify Power BI Desktop", "No dataset required", ["Open one of the official Microsoft download routes", "Install the Microsoft Store app or PBIDesktopSetup_x64.exe", "Launch Power BI Desktop", "Open Help > About and verify the version"], "A working Power BI Desktop installation"),
        "check": ("Which file should be selected on the direct-download route?", ["PBIDesktopSetup_x64.exe", "A 32-bit x86 installer", "A third-party repackaged installer", "Power BI Report Builder only"], 0, "The supported standalone Power BI Desktop installer is the 64-bit PBIDesktopSetup_x64.exe file."),
    },
    {
        "id": 2, "code": "D1.2", "day": 1, "duration": "45 min",
        "title": "Tour the Power BI Desktop interface",
        "subtitle": "Recognize the views, ribbon, canvas, panes and report pages",
        "outcomes": ["Locate the Home ribbon and common commands", "Switch between Report, Data and Model views", "Identify the report canvas, Filters, Visualizations and Data panes"],
        "concepts": [
            ("Ribbon and commands", "The ribbon organizes commands such as Get data, Transform data, New visual, New measure and Publish. Available commands can change with the selected object and view.", "Home > Get data begins the first CSV import; Home > Transform data opens Power Query Editor.", "Start by knowing where commands live, not by memorizing every button."),
            ("Report, Data and Model views", "The left rail switches between Report view for visual design, Data view for inspecting loaded tables and Model view for relationships.", "After Lab 1 is loaded, select Data view to confirm the data and Report view to begin building visuals.", "Each view answers a different development question."),
            ("Canvas, panes and pages", "The central canvas is the report design surface. Filters, Visualizations and Data panes control filtering, visual type, formatting and fields; page tabs organize the report.", "Drag a field from the Data pane to the canvas, then select a visual type from the Visualizations pane.", "Canvas in the centre, authoring panes on the right, pages at the bottom."),
        ],
        "lab": ("Identify the Power BI Desktop workspace", "Blank Power BI Desktop file", ["Locate the title bar and ribbon", "Select Report, Data and Model views on the left rail", "Point out the report canvas and the three authoring panes", "Add and rename a report page"], "A completed interface identification checklist"),
        "check": ("Where are report visuals arranged and designed?", ["On the Report view canvas", "Inside the Microsoft Store", "Only in Power Query Editor", "In the Windows download folder"], 0, "The Report view canvas is the main design surface for report visuals."),
    },
    {
        "id": 3, "code": "D1.3", "day": 1, "duration": "55 min",
        "title": "Lab 1: Import the retail CSV",
        "subtitle": "Connect to data.csv and open it in Power Query Editor",
        "outcomes": ["Import a comma-separated file with Text/CSV", "Read the preview and confirm the eight source columns", "Choose Transform Data so quality checks happen before loading"],
        "concepts": [
            ("Text/CSV connector", "Home > Get data > Text/CSV reads a delimited file and displays a preview before anything is loaded into the model.", "Select data.csv from the Lab 1 folder and verify that the first row contains the column names.", "Preview the file before accepting it."),
            ("Understand the source", "The original file contains 541,909 retail transaction rows and eight columns: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID and Country.", "One row represents one stock item appearing on an invoice.", "Know the row meaning and expected columns before transforming the data."),
            ("Transform instead of immediate Load", "Transform Data opens Power Query Editor so types and quality issues can be checked before the table reaches the model. Load bypasses that review step.", "Choose Transform Data because InvoiceDate must be validated and corrected first.", "For this lab, select Transform Data—not Load."),
        ],
        "lab": ("Import data.csv", "Lab 1 · Retail transactions", ["Home > Get data > Text/CSV", "Select data.csv", "Confirm comma delimiter, headers and eight columns in the preview", "Select Transform Data"], "The data query open in Power Query Editor"),
        "check": ("Which preview option should be selected for this lab?", ["Transform Data", "Load without inspection", "Cancel", "Publish"], 0, "Transform Data opens Power Query Editor so the date quality issue can be investigated before loading."),
    },
    {
        "id": 4, "code": "D1.4", "day": 1, "duration": "75 min",
        "title": "Lab 1: Find and fix the date error",
        "subtitle": "Use Keep Errors, locale-aware typing and Close & Apply",
        "outcomes": ["Use Keep Errors to isolate conversion failures", "Explain why US-formatted dates fail under a different locale", "Apply Date/Time with English (United States) locale and load the corrected query"],
        "concepts": [
            ("Keep Errors", "Home > Keep Rows > Keep Errors retains only rows whose selected column contains an error. It is a diagnostic step for understanding the problem rather than a permanent cleanup step.", "Select InvoiceDate and keep errors to expose values that could not be converted.", "Investigate errors before removing or replacing them."),
            ("The locale problem", "The source stores InvoiceDate as month/day/year. A value such as 1/13/2011 is valid in English (United States) but cannot be read as day/month/year because 13 is not a month.", "Change InvoiceDate to Date/Time using English (United States) locale.", "A date is not fully defined until its format and locale are known."),
            ("Apply types and load", "After the date is corrected, assign appropriate types to the remaining columns, keep InvoiceNo as text, remove the temporary Keep Errors step and use Close & Apply.", "Power Query replays Source, Promoted Headers, Changed Type with Locale and the remaining type assignments before loading the table.", "Close & Apply only after the query has no unexplained errors."),
        ],
        "lab": ("Diagnose, correct and load InvoiceDate", "Lab 1 · Retail transactions", ["Select InvoiceDate and change it to Date/Time to expose the locale error", "Home > Keep Rows > Keep Errors and inspect the failing values", "Delete the temporary error step, then Data type > Using Locale > Date/Time > English (United States)", "Assign the remaining data types and keep InvoiceNo as text", "Home > Close & Apply and confirm the table is available in Power BI Desktop"], "A loaded retail table with a valid InvoiceDate column"),
        "check": ("Which locale correctly interprets 1/13/2011 in this source?", ["English (United States)", "A day/month locale", "No locale is needed", "Currency locale only"], 0, "The source uses month/day/year, so English (United States) correctly interprets 1/13/2011 as 13 January 2011."),
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
    ("Which standalone Power BI Desktop installer is supported?", ["PBIDesktopSetup_x64.exe", "A 32-bit x86 installer", "A third-party package", "Power BI Report Builder"], 0),
    ("Which Power BI Desktop view is used to arrange report visuals?", ["Report view", "Microsoft Store view", "Power Query error view", "Download Center view"], 0),
    ("Which CSV preview action opens Power Query Editor before loading?", ["Transform Data", "Publish", "Load without inspection", "Cancel"], 0),
    ("What does Keep Errors do in Power Query?", ["Keeps only rows containing errors in the selected columns", "Silently fixes every error", "Publishes the table", "Changes all columns to text"], 0),
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
    ("Lab 1 · Original retail CSV", "The complete 541,909-row data.csv file used for importing, error detection and locale correction", "lab-1-importing-data-basics.zip"),
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
        "screen_title": "Install Power BI Desktop from Microsoft",
        "screens": [
            ("Microsoft Store", "00-power-bi-store-install.png", "The official Microsoft Store listing with the Install button highlighted. Source: Microsoft Learn.", ["Select Install on the official Power BI Desktop listing", "The Store route normally keeps Power BI Desktop updated automatically", "No third-party download site is required"]),
            ("Direct 64-bit installer", "00-power-bi-x64-download.png", "The Microsoft Download Center selection screen with PBIDesktopSetup_x64.exe selected. Source: Microsoft Learn.", ["Choose PBIDesktopSetup_x64.exe", "The 32-bit edition is no longer supported", "Run the downloaded installer and complete the setup wizard"]),
        ],
        "click_path": ["Preferred route: open the official Microsoft Store listing and select Install", "Alternative route: open the Microsoft Download Center", "Select PBIDesktopSetup_x64.exe and complete installation", "Launch Power BI Desktop and verify Help > About"],
        "task": "Install Power BI Desktop using one approved Microsoft route and confirm that the application opens successfully.",
        "evidence": "A working Power BI Desktop installation and the installed version number",
    },
    2: {
        "screen_title": "Locate the main Power BI Desktop components",
        "screens": [
            ("Power BI Desktop interface", "01-power-bi-desktop-interface.png", "A full Power BI Desktop Report view showing the ribbon, view rail, canvas, authoring panes and page tabs. Source: Microsoft Learn.", ["Ribbon and Get data commands are across the top", "Report, Data and Model views are on the left rail", "The report canvas occupies the centre", "Filters, Visualizations and Data panes are on the right", "Report pages appear along the bottom"]),
        ],
        "click_path": ["Select Home and identify Get data and Transform data", "Select Report view on the left rail", "Locate the report canvas and right-side authoring panes", "Select Data view and Model view", "Add and rename a report page at the bottom"],
        "task": "Use the screenshot and your open application to identify each major interface component without assistance.",
        "evidence": "A completed interface checklist covering ribbon, views, canvas, panes and pages",
    },
    3: {
        "screen_title": "Import data.csv and open Power Query Editor",
        "screens": [
            ("Get data from the Home ribbon", "01-power-bi-desktop-interface.png", "The Home ribbon contains Get data and Transform data. Source: Microsoft Learn.", ["Select Get data", "Choose Text/CSV", "Select data.csv", "Use the preview to verify the file before continuing"]),
            ("Power Query Editor", "03-power-query-editor.png", "The course data open in Power Query Editor with the ribbon, preview, formula bar and Applied Steps visible.", ["The query named data appears on the left", "The centre grid previews the eight source columns", "Applied Steps record each transformation", "The formula bar shows the generated M expression"]),
        ],
        "click_path": ["Power BI Desktop > Home > Get data > Text/CSV", "Browse to the Lab 1 CSV folder and select data.csv", "Confirm comma delimiter, headers and eight columns", "Select Transform Data", "Verify that the data query opens in Power Query Editor"],
        "task": "Import the original Lab 1 data.csv file and stop in Power Query Editor before loading it.",
        "evidence": "The data query visible in Power Query Editor with all eight source columns",
    },
    4: {
        "screen_title": "Diagnose the date error, correct the locale and load",
        "screens": [
            ("Changed Type with Locale", "03-power-query-editor.png", "The completed Lab 1 query shows InvoiceDate converted with a locale-aware step before the remaining column types are applied.", ["The formula bar contains Table.TransformColumnTypes", "Changed Type with Locale appears in Applied Steps", "InvoiceDate displays as a valid Date/Time value", "Close & Apply loads the cleaned table into Power BI Desktop"]),
        ],
        "click_path": ["Select InvoiceDate and convert it to Date/Time to expose the error", "Home > Keep Rows > Keep Errors and inspect values such as 1/13/2011", "Remove the temporary error-only step", "InvoiceDate > Data type > Using Locale > Date/Time > English (United States)", "Assign the remaining column types and keep InvoiceNo as text", "Home > Close & Apply and confirm the table appears in Power BI Desktop"],
        "task": "Use Keep Errors to diagnose the InvoiceDate problem, correct it with English (United States) locale and load the table.",
        "evidence": "A loaded data table with valid InvoiceDate values and no unexplained conversion errors",
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
