# CLAUDE.md — Web Lab
## Project Instructions, Architecture and Engineering Standards

**Project:** Web Lab  
**Purpose:** AI-assisted website development and website parsing laboratory  
**Primary AI agent:** OpenCode  
**Supported models:** Claude Haiku and other available free/included models  
**Primary execution hardware:** Raspberry Pi 5 (8 GB RAM, ARM64)  
**Secondary development machine:** Ubuntu PC  
**Primary language:** Python  
**Frontend:** HTML, CSS, vanilla JavaScript  
**Initial browser:** Firefox  
**Initial parsing target:** Avito.ru  
**Storage:** microSD on Raspberry Pi  
**Version control:** Git  
**Project status:** Research and development (DEV)  
**Current phase and status:** see DEVELOPMENT_PLAN.md (this file holds rules, not progress)

---

# 1. PROJECT MISSION

Web Lab is a unified environment for experimenting with, developing and operating two independent but interconnected AI capabilities:

1. Website Development.
2. Website Parsing.

Both capabilities share browser infrastructure, automation utilities, AI integration, networking, logging and testing infrastructure.

The project must be designed so that an AI agent can independently develop websites, inspect existing websites, create parsers, operate persistent browser sessions and request human assistance when necessary.

The long-term objective is to create two reliable AI-assisted workflows.

## 1.1 Website Development Agent

The agent must eventually be able to:

- Create complete websites from descriptions.
- Create backend applications using Python.
- Create traditional multipage websites.
- Develop HTML, CSS and JavaScript.
- Inspect existing websites.
- Understand website layouts and visual hierarchy.
- Inspect typography, spacing, colors and responsive behavior.
- Inspect HTML, CSS and JavaScript.
- Understand how particular visual components are implemented.
- Reproduce existing designs in new projects.
- Modify existing websites without unnecessarily breaking existing functionality.
- Debug JavaScript and backend errors.
- Run applications locally.
- Test applications in a real browser.
- Compare screenshots against reference websites.
- Improve implementations iteratively.

The initial preferred technology stack is:

- Python backend.
- HTML templates.
- Vanilla JavaScript.
- CSS.
- FastAPI, Flask or Django, to be evaluated.
- PostgreSQL, when justified by the project.

Do not introduce React, Vue, Angular or other frontend frameworks without a concrete reason.

The initial objective is to establish a capable traditional website development workflow, not to adopt the largest possible technology stack.

## 1.2 Website Parsing Agent

The agent must eventually be able to:

- Accept a website URL and extraction requirements.
- Inspect the website.
- Identify relevant information and page structure.
- Determine whether direct HTTP requests or browser automation are appropriate.
- Navigate JavaScript-heavy websites.
- Maintain permanent browser profiles.
- Reuse existing authenticated sessions.
- Extract structured information.
- Save extracted information in reusable formats.
- Handle pagination and multiple pages.
- Detect navigation failures.
- Detect authentication requirements and interactive challenges.
- Pause execution for human intervention.
- Resume after human intervention without losing browser state.
- Log extraction results and failures.
- Recover from interrupted tasks.

Initial target: Avito.ru.

Potential future targets include Wildberries and Ozon.

The parsing system must distinguish between:

- Static HTML extraction.
- JavaScript-rendered content.
- Data obtained from legitimate browser network requests.
- Browser-based extraction.
- Authenticated sessions.
- Human-assisted interaction.

The system must not assume that all websites can or should be parsed using the same method.

---

# 2. PROJECT PRINCIPLES

These principles apply to all agents, scripts, services and experiments.

## 2.1 Research before implementation

Do not install or implement a technology merely because it is popular.

For significant architectural decisions:

1. Identify the problem.
2. Identify possible solutions.
3. Investigate their compatibility with the Raspberry Pi.
4. Compare resource requirements.
5. Build small independent experiments.
6. Measure actual results.
7. Document conclusions.
8. Select the best practical solution.

Prefer measured results over assumptions.

## 2.2 Incremental development

Build the smallest working implementation first.

Do not build a sophisticated framework before proving that its essential components work.

Every major feature should have a minimal reproducible experiment.

Examples:

- Verify persistent Firefox profiles before implementing a browser manager.
- Verify remote browser control before implementing multiple OpenCode integrations.
- Verify Avito accessibility before developing a full parsing engine.
- Verify screenshot-based inspection before building sophisticated visual comparison tools.

## 2.3 Python-first architecture

Python is the default language for:

- Backend development.
- Browser automation.
- Parsing.
- Service orchestration.
- Data processing.
- Testing.
- Infrastructure utilities.
- OpenCode integration.

JavaScript is appropriate for frontend functionality and browser-side code.

Shell scripts are appropriate for system administration and installation tasks.

Avoid introducing Node.js-based infrastructure unless it provides a clear benefit.

## 2.4 Prefer simplicity

Prefer:

- Fewer dependencies.
- Small independent services.
- Standard protocols.
- Explicit configuration.
- Reproducible environments.
- Well-documented interfaces.
- Native Linux capabilities.
- Lightweight deployments.

Avoid unnecessary abstraction, microservices, message brokers and complex orchestration.

The Raspberry Pi has limited resources and runs from microSD storage.

## 2.5 Preserve existing functionality

When modifying an existing project:

- Inspect the repository first.
- Understand its structure.
- Read existing documentation.
- Identify existing functionality.
- Avoid unnecessary rewrites.
- Preserve established interfaces.
- Run relevant tests after modifications.

Do not replace an existing working solution merely because another implementation looks cleaner.

## 2.6 Human approval during DEV

This project is currently in DEV mode.

The agent must not operate autonomously in the sense of making unrestricted changes to the host environment.

Require explicit approval before:

- Installing system packages.
- Removing packages.
- Changing system configurations.
- Modifying VPN routing.
- Changing firewall rules.
- Changing network interfaces.
- Modifying systemd services.
- Modifying permissions outside the project.
- Deleting files or databases.
- Changing persistent browser profiles.
- Deploying applications.
- Making production changes.
- Running destructive database operations.

The agent may independently:

- Inspect files.
- Read logs.
- Analyze configuration.
- Write proposed code.
- Create project-local files after authorization.
- Run non-destructive project tests.
- Produce implementation plans.

Never assume root privileges.

Never attempt to bypass approval requirements through alternative shell commands or indirect execution.

---

# 3. PROJECT ARCHITECTURE

The project is one overall project with two independent functional modules and shared infrastructure.

## 3.1 High-level architecture

    WEB LAB
    |
    +-- Website Development
    |   |
    |   +-- Website inspection
    |   +-- Design reconstruction
    |   +-- Backend development
    |   +-- Frontend development
    |   +-- Visual testing
    |   +-- Functional testing
    |
    +-- Website Parsing
    |   |
    |   +-- Website inspection
    |   +-- Extraction strategy
    |   +-- HTTP parsing
    |   +-- Browser extraction
    |   +-- Human intervention
    |   +-- Data processing
    |   +-- Storage
    |
    +-- Shared Infrastructure
        |
        +-- Firefox
        +-- Playwright
        +-- Browser management
        +-- VNC
        +-- Python utilities
        +-- Networking
        +-- Logging
        +-- OpenCode integration
        +-- Git

The modules must remain logically independent.

A failure in the parsing module must not automatically interrupt website development.

A development environment restart must not unnecessarily terminate a persistent parsing browser session.

Shared components must have documented interfaces.

## 3.2 Independent modules

Website Development and Website Parsing should have:

- Separate instructions.
- Separate OpenCode skills.
- Separate project workspaces.
- Separate dependencies where practical.
- Separate tests.
- Separate logs.
- Separate configuration.
- Separate permissions.

Shared infrastructure should not contain website-specific extraction or development logic.

## 3.3 Shared infrastructure

Shared infrastructure should provide:

- Browser lifecycle management.
- Browser profile management.
- Browser navigation.
- DOM inspection.
- Screenshot capture.
- Browser console inspection.
- Network inspection.
- Human intervention.
- Logging.
- Configuration management.
- Remote access.

Do not duplicate these capabilities inside individual modules.

---

# 4. HARDWARE AND EXECUTION ENVIRONMENT

## 4.1 Raspberry Pi

Known hardware and environment:

- Raspberry Pi 5.
- RAM: 8 GB.
- Architecture: ARM64 / aarch64.
- OS: Debian 13 (trixie). Verified 2026-11-25 (`/etc/os-release`).
- Kernel: 6.18.29+rpt-rpi-2712 (reported 2026-11-24).
- Storage: microSD.
- Cooling: active.
- Hostname: pi5home.
- User: bliss.
- Primary role: persistent execution server.
- Browser: Firefox.
- Remote administration: SSH.
- Human browser interaction: VNC.

The actual installed software versions must be discovered during the initial audit.

Do not assume that this environment exactly matches a generic Raspberry Pi installation.

## 4.2 Ubuntu PC

The secondary machine is an Ubuntu Linux PC.

Its responsibilities may include:

- Running OpenCode.
- Editing source code.
- Running local tests.
- Managing Git.
- Inspecting development results.
- Connecting to Raspberry Pi services.
- Controlling the remote browser.

The agent must not assume that the PC and Pi have identical software environments.

## 4.3 Dual OpenCode execution

OpenCode must be usable from both machines.

Both environments should work with the same remote Git repository.

Preferred model:

- Raspberry Pi owns persistent runtime services.
- Ubuntu PC provides an additional development environment.
- Both machines maintain independent Git working copies.
- Runtime state is not synchronized through Git.

Never assume that OpenCode running on one machine can directly access the other machine's local files.

Use documented interfaces such as:

- SSH.
- Git.
- HTTP APIs.
- MCP.
- Other explicitly configured remote tools.

## 4.4 Resource management

The Pi has 8 GB RAM and microSD storage.

Resource efficiency is important.

Avoid:

- Running unnecessary browser instances.
- Starting multiple browser profiles simultaneously without justification.
- Running multiple large AI-related services locally.
- Excessive browser tracing.
- Unbounded log files.
- Unnecessary container layers.
- Repeatedly downloading browser binaries.

Prefer one active browser automation task at a time during initial experiments.

Measure:

- CPU utilization.
- RAM utilization.
- Swap utilization.
- Browser memory consumption.
- Disk consumption.
- Disk I/O.
- Temperature.
- Task duration.

Do not assume that an application is lightweight merely because it is written in Python.

## 4.5 microSD considerations

The microSD card is the current primary storage.

Minimize unnecessary writes.

Pay particular attention to:

- Browser cache.
- Browser profile data.
- Playwright traces.
- Screenshots.
- Logs.
- Temporary downloads.
- Database writes.
- Docker storage.

Implement log rotation.

Avoid continuously recording full browser traces.

Do not store large volumes of screenshots unless they are needed for a benchmark or debugging task.

SSD migration may be considered later, but must not be a prerequisite for the initial implementation.

---

# 5. NETWORKING AND VPN

## 5.1 Existing VPN

The Raspberry Pi already has a working VPN connection.

Avito currently appears to be accessible through the Pi's VPN connection.

The VPN configuration must be inspected rather than modified blindly.

The eventual requirement is selective routing:

- Necessary destinations should be excluded from VPN routing when appropriate.
- Other traffic should retain its intended VPN behavior.
- The behavior must be verified with actual connectivity tests.

Do not invent VPN interface names, routes, gateways or DNS settings.

Discover the current configuration first.

## 5.2 Networking rules

Before changing networking:

1. Inspect interfaces.
2. Inspect routes.
3. Inspect DNS configuration.
4. Inspect VPN configuration.
5. Identify the current default route.
6. Determine how routing changes affect SSH and VNC.
7. Propose the intended changes.
8. Obtain explicit approval.
9. Apply changes carefully.
10. Verify connectivity and provide rollback instructions.

Never make network changes that could unexpectedly disconnect the user from the Pi.

## 5.3 Website-specific connectivity

Different websites may require different network behavior.

The parsing architecture should allow website-specific network configuration.

Do not implement a global VPN routing change merely to accommodate one website.

Prefer explicit, documented routing policies.

---

# 6. BROWSER INFRASTRUCTURE

Browser infrastructure is one of the most important components of Web Lab.

The browser must be independent of the AI agent's lifecycle.

## 6.1 Initial browser

Firefox is the first browser to investigate and implement.

Chromium may be added as an alternative for comparison and development testing.

Do not assume Firefox is universally superior.

The initial objective is a reliable Firefox environment on Raspberry Pi ARM64.

## 6.2 Persistent browser profiles

Persistent profiles are a critical requirement.

There should be one permanent profile per website.

Proposed structure:

    browser-data/
    |
    +-- profiles/
    |   |
    |   +-- avito/
    |   +-- wildberries/
    |   +-- ozon/
    |   +-- development/
    |
    +-- downloads/
    +-- screenshots/
    +-- logs/
    +-- traces/

The actual browser profile directories must be outside Git.

Never commit:

- Cookies.
- Authentication tokens.
- Session identifiers.
- Passwords.
- Browser databases.
- Local storage.
- Profile configuration containing secrets.

Profile rules:

1. A profile belongs to one website or clearly defined website group.
2. A profile must not be recreated for every task.
3. Browser restarts should reuse the existing profile.
4. OpenCode restarts must not unnecessarily restart Firefox.
5. Browser profiles must not be simultaneously opened by multiple independent Firefox processes.
6. Profile backup and restoration follow section 6.7.
7. Profile access must be protected.

Do not synchronize active Firefox profiles through Git.

## 6.3 Browser automation candidates

Investigate:

- Playwright Python.
- Firefox automation.
- Chromium + Playwright.
- Chrome DevTools Protocol where applicable.
- Playwright MCP.
- Direct browser control through a Python service.

The first implementation should use Python as the primary orchestration language.

The exact browser control mechanism must be verified on the actual ARM64 installation.

## 6.4 Browser service

The preferred architectural direction is a persistent browser service.

Potential responsibilities:

- Start and stop browser processes.
- Select profiles.
- Open URLs.
- Navigate.
- Read page content.
- Inspect DOM.
- Execute JavaScript.
- Take screenshots.
- Retrieve browser console errors.
- Retrieve navigation information.
- Detect browser failures.
- Pause and resume tasks.
- Report browser status.

The browser service should expose a documented interface.

Potential initial interface:

    GET  /health
    GET  /browser/status
    POST /browser/start
    POST /browser/navigate
    POST /browser/screenshot
    POST /browser/inspect
    POST /browser/pause
    POST /browser/resume
    POST /browser/stop

These are proposed interface names, not existing endpoints.

Implement only the endpoints that are actually needed.

## 6.5 Browser ownership and concurrency

Persistent profiles require explicit ownership.

A browser profile must have only one active controlling task at a time.

Implement:

- Profile-level locks.
- Task identifiers.
- Browser ownership information.
- Operation timeouts.
- Explicit release of locks.
- Recovery of abandoned locks.

Two OpenCode instances may connect to the same browser infrastructure, but they must not simultaneously manipulate the same profile.

The browser service should reject conflicting operations or place them in a controlled queue.

## 6.6 Browser lifecycle

Expected behavior:

1. Browser starts.
2. Profile is loaded.
3. Browser remains available.
4. Agent executes a task.
5. Task finishes.
6. Browser remains open.
7. Another task can reuse the browser.

The default behavior is to keep the browser open after task completion.

Do not automatically clear cookies, storage or browser data.

Provide an explicit shutdown operation.

## 6.7 Backup of browser profiles and collected data

**Current status: deferred.** Web Lab is a testing environment and holds no live data worth saving. Until that changes, no backups are required and none should be set up. Profiles and collected data are disposable test artifacts.

This section becomes active when either of these happens, and the agent must then raise it with the user instead of waiting:

- A browser profile contains a real login session that would be costly to recreate.
- Collected data has value beyond a test run.

Once active, two kinds of data are not recoverable from Git and must be backed up:

1. Persistent browser profiles (login sessions, cookies, local storage).
2. Collected data (parser output, extracted datasets).

Rules:

1. Backups are never stored inside the Git repository and are never committed.
2. Do not copy a profile while Firefox is using it. Stop the browser cleanly first, or use a method that guarantees a consistent copy. Never leave a profile half-copied.
3. Backing up a profile requires an explicit Firefox shutdown, which interrupts the persistent session. Obtain approval before doing it (section 2.6).
4. Backups must be stored on a device other than the Pi's microSD card. A backup on the same card does not protect against card failure.
5. Backups contain authentication data. Protect them with the same permissions as the live profile (section 12.3).
6. Keep a small number of recent backups and remove older ones. Do not let backups grow without limit (section 4.5).
7. A backup is not valid until a restore has been tested at least once. Document the restore procedure.
8. Collected data has its own backup schedule, independent of profiles. Backing it up must not require stopping the browser.
9. Automatic backup jobs (cron, systemd timers) count as system changes and need approval (section 2.6).

The backup destination, schedule and retention period are decided when this section becomes active, and recorded in DEVELOPMENT_PLAN.md. Do not invent them.

---

# 7. HUMAN INTERVENTION

Human intervention through VNC is a fundamental requirement.

The agent must support the following workflow.

## 7.1 Standard workflow

1. Agent starts a browser task.
2. Browser navigates to the website.
3. An interactive obstacle is detected.
4. Agent pauses the current task.
5. Browser remains open.
6. Agent records the current URL and task state.
7. Agent notifies the user that assistance is required.
8. User connects through VNC.
9. User performs the necessary legitimate interaction.
10. User confirms completion or the agent detects the expected page state.
11. Agent continues the task.

Possible intervention reasons:

- Login.
- CAPTCHA.
- Session expiration.
- Consent dialog.
- Manual confirmation.
- Other interactive obstacles.

Do not automatically close or recreate the browser during intervention.

## 7.2 Pause state

A paused task should preserve:

- Task ID.
- Website.
- Browser profile.
- Current URL.
- Current browser state where practical.
- Pause reason.
- Timestamp.
- Last successful operation.
- Resume instructions.

Do not rely exclusively on an in-memory Python variable to preserve task state.

Use a durable task-state mechanism if experiments show that recovery across service restarts is required.

## 7.3 Resume behavior

After human intervention:

- Verify that the expected page is accessible.
- Verify that the session is still valid.
- Verify that the required content is available.
- Continue from the last safe operation.

Do not blindly repeat operations that may have already succeeded.

## 7.4 Notifications

Initially, logging and clear terminal output are sufficient.

A notification mechanism may be introduced later.

Possible future integrations:

- Telegram.
- Desktop notification.
- Web interface.
- OpenCode interaction.

Do not build a notification system before the basic pause/resume workflow works.

---

# 8. WEBSITE PARSING MODULE

## 8.1 Parsing strategy

Do not automatically use a browser for every request.

The agent must evaluate the target website and select an appropriate method.

Candidate approaches:

1. HTTPX + BeautifulSoup.
2. HTTPX + lxml.
3. Scrapy.
4. Playwright.
5. Scrapy + Playwright.
6. Browser-based extraction.

Evaluate them against real requirements.

## 8.2 Initial target: Avito

Avito is the first target.

The agent must first investigate:

- Whether the website is reachable from the Pi.
- Whether the VPN is required.
- Whether normal HTTP requests work.
- Whether browser rendering is required.
- Which information is present in the rendered DOM.
- Whether pagination is available.
- How navigation behaves.
- Whether authentication is required.
- Whether session state affects results.
- Whether content changes between visits.

Do not assume that the website is accessible through the Ubuntu PC.

The Pi is the initial reference environment.

## 8.3 Anti-bot and access restrictions

The goal is reliable and maintainable access to permitted website content.

The agent may investigate:

- Browser compatibility.
- JavaScript rendering.
- Session persistence.
- Normal browser behavior.
- Authentication.
- Human-assisted CAPTCHA completion.
- Rate limiting.
- Retry strategies.
- Request scheduling.
- Website-provided APIs and permitted data interfaces.

Do not:

- Circumvent access controls.
- Defeat CAPTCHA systems through unauthorized automated solving.
- Forge identities or impersonate users.
- Evade explicit access restrictions.
- Ignore website terms or applicable legal requirements.
- Continue aggressive requests after rate limiting or blocking.

When access is denied, stop and report the situation.

Prefer official APIs, authorized access and user-assisted authentication.

## 8.4 Extraction architecture

Keep extraction logic independent of browser automation.

A parser should have logically separate responsibilities:

    Parser
    |
    +-- Target configuration
    |
    +-- Navigation
    |
    +-- Page inspection
    |
    +-- Data extraction
    |
    +-- Normalization
    |
    +-- Validation
    |
    +-- Storage
    |
    +-- Logging

Do not put all logic in one large script.

## 8.5 Structured output

The parser must produce structured data.

Potential formats:

- JSON.
- JSONL.
- CSV.
- PostgreSQL.

PostgreSQL is a candidate, but its implementation is intentionally deferred until the initial parsing experiments establish the data model and persistence requirements.

Use a clearly defined schema for extracted information.

Distinguish:

- Source values.
- Normalized values.
- Derived values.
- Extraction timestamps.
- Source URLs.
- Extraction errors.

Store only the fields defined in the extraction schema. The purpose of Avito parsing is to collect data for analysis and research, so the schema is defined by the research questions, not by what the page happens to contain.

Do not save full raw HTML pages or full page snapshots by default. Keep raw pages only temporarily, for debugging a specific extraction problem, and delete them afterwards.

Do not silently drop a field that is in the schema. If a field not in the schema looks useful, propose adding it to the schema and ask, instead of saving raw pages "just in case".

## 8.6 Data quality

A successful HTTP request does not mean a successful parsing task.

Validate:

- Required fields.
- Data types.
- Missing values.
- Duplicate records.
- Pagination completeness.
- Source URLs.
- Extraction timestamps.
- Unexpected changes in page structure.

Record partial results and errors separately.

---

# 9. WEBSITE DEVELOPMENT MODULE

## 9.1 Initial technology stack

Preferred starting stack:

- Python.
- FastAPI, Flask or Django.
- HTML.
- CSS.
- Vanilla JavaScript.
- Jinja2 where appropriate.
- SQLite for simple prototypes.
- PostgreSQL when justified.

The choice between FastAPI, Flask and Django should be based on the project requirements and comparative experiments.

Do not automatically select the most complex framework.

## 9.2 Website inspection

The development agent must be able to inspect an existing website.

The inspection process should include:

1. Open the reference website.
2. Capture screenshots.
3. Inspect page dimensions.
4. Identify major layout regions.
5. Inspect HTML structure.
6. Inspect relevant CSS.
7. Inspect computed styles.
8. Inspect fonts.
9. Identify colors and spacing.
10. Inspect JavaScript behavior.
11. Identify responsive breakpoints.
12. Identify reusable components.

The agent should produce a concise inspection report before attempting a complex reconstruction.

## 9.3 Design reproduction

When reproducing a reference design:

- Preserve visual hierarchy.
- Match major layout proportions.
- Match typography.
- Match spacing.
- Match colors.
- Match responsive behavior.
- Match relevant interactive behavior.

Use screenshots to evaluate the result.

Do not claim visual similarity without comparing the actual rendered pages.

## 9.4 Existing website modification

Before changing an existing website:

1. Inspect its project structure.
2. Identify the framework and dependencies.
3. Identify relevant files.
4. Understand the existing behavior.
5. Establish a baseline.
6. Make targeted modifications.
7. Run relevant tests.
8. Compare screenshots where appropriate.
9. Report changes and remaining issues.

Avoid rewriting working components without a clear reason.

## 9.5 Visual testing

Investigate:

- Playwright screenshots.
- Multiple viewport sizes.
- Full-page screenshots.
- Browser console inspection.
- Network failures.
- Responsive testing.
- Visual regression comparison.

Visual comparison should be repeatable.

Keep reference screenshots and test screenshots separate.

---

# 10. OPENCODE INTEGRATION

OpenCode is the primary AI orchestration environment.

It may run on either the Raspberry Pi or Ubuntu PC.

## 10.1 Responsibilities

OpenCode should:

- Understand project instructions.
- Select the correct module.
- Read relevant skills.
- Inspect existing code.
- Plan changes.
- Execute approved tasks.
- Use browser infrastructure.
- Run tests.
- Analyze results.
- Document findings.

## 10.2 Skills

Create separate skills for major capabilities.

Proposed skills:

    skills/
    |
    +-- browser-control/
    +-- website-inspection/
    +-- website-development/
    +-- website-parsing/
    +-- human-intervention/
    +-- visual-testing/
    +-- environment-audit/

These are proposed skills.

Do not create all skills immediately.

Build them when the underlying functionality has been tested.

Each skill should be focused and concise.

Avoid duplicating the entire CLAUDE.md in every skill.

## 10.3 Model selection

No additional paid model expenditure is intended.

Use models available through the user's existing OpenCode account and genuinely free alternatives.

Do not assume that a model is free because it appears in a model list.

Verify:

- Availability.
- Usage limits.
- Context window.
- Tool calling.
- Coding performance.
- Reliability.
- Speed.

Do not hardcode one model as the permanent project requirement.

## 10.4 Model benchmarks

Give candidate models identical tasks.

Record:

- Model identifier.
- Task description.
- Initial conditions.
- Completion status.
- Number of iterations.
- Errors.
- Token usage, if available.
- Time to completion.
- Quality assessment.
- Required human intervention.

A model should not be judged solely by its ability to generate plausible code.

Actual execution and test results matter more.

---

# 11. GIT AND MULTI-MACHINE WORKFLOW

## 11.1 Git is the synchronization mechanism

The Raspberry Pi and Ubuntu PC should have independent working copies.

Both use the same remote repository.

Preferred workflow:

1. Pull before starting work.
2. Use a dedicated branch for substantial changes.
3. Commit completed logical changes.
4. Push to the remote repository.
5. Pull changes on the other machine.

Avoid simultaneous editing of the same files on both machines.

Do not use Git to synchronize runtime state.

## 11.2 Never commit runtime data

Exclude:

- Browser profiles.
- Cookies.
- Authentication data.
- Browser caches.
- Logs.
- Temporary screenshots.
- Downloads.
- Database files.
- Collected datasets.
- Backups of profiles or data.
- Virtual environments.
- Secrets.
- Environment files containing credentials.
- Temporary test output.

Use `.gitignore` from the beginning.

## 11.3 Configuration

Use example configuration files.

For example:

    .env.example

Actual credentials must be stored outside Git.

Do not hardcode:

- Passwords.
- API keys.
- Tokens.
- Proxy credentials.
- Database passwords.
- VPN credentials.

## 11.4 Concurrent OpenCode instances

Two OpenCode instances may operate on the same overall project.

However:

- Avoid simultaneous changes to the same working copy.
- Avoid concurrent control of the same browser profile.
- Avoid concurrent database migrations.
- Use Git branches for parallel code development.
- Use explicit locks for shared runtime resources.

---

# 12. SECURITY AND PERMISSIONS

Security must be considered from the beginning.

## 12.1 Development mode

Current project mode: DEV.

Default assumptions:

- Human approval required for consequential operations.
- No unrestricted system modifications.
- No automatic production deployment.
- No unrestricted database writes.
- No automatic credential changes.
- No autonomous installation of system packages.

## 12.2 Secrets

Never:

- Print passwords in logs.
- Commit secrets.
- Include authentication cookies in reports.
- Send browser profile data to AI models.
- Expose browser-control endpoints publicly.
- Expose VNC directly to the public internet.

Remote browser services should be accessible only through a controlled local network or authenticated secure connection.

## 12.3 Browser isolation

Do not mix development experiments with authenticated parsing profiles.

Use separate profiles.

Avoid opening the same profile simultaneously in different processes.

Protect browser profile directories with appropriate filesystem permissions.

## 12.4 Future LIVE mode

Autonomy is a future objective.

Before LIVE mode:

- Define permitted operations.
- Define forbidden operations.
- Define resource limits.
- Define network restrictions.
- Define database permissions.
- Define rollback mechanisms.
- Test failure recovery.
- Verify logging.
- Verify backups.

Never interpret a request for autonomous operation as permission to ignore security boundaries.

---

# 13. TESTING AND BENCHMARKING

Every important component must have a measurable test.

## 13.1 Browser benchmarks

Test:

- Browser startup.
- Browser navigation.
- DOM inspection.
- JavaScript execution.
- Screenshots.
- Persistent profiles.
- Session reuse.
- VNC interaction.
- Browser recovery.
- OpenCode restart.
- Browser service restart.
- Pi reboot recovery.

## 13.2 Parsing benchmarks

Test:

- Static HTML extraction.
- JavaScript-rendered content.
- Pagination.
- Session persistence.
- Human intervention.
- Duplicate detection.
- Data validation.
- Partial failures.
- Retry behavior.
- Resource consumption.

## 13.3 Development benchmarks

Test:

- New website generation.
- Existing website inspection.
- Design reproduction.
- CSS modification.
- JavaScript modification.
- Backend implementation.
- Responsive design.
- Functional browser testing.
- Error recovery.

## 13.4 Resource benchmarks

Record:

- RAM before task.
- RAM during task.
- Peak RAM.
- CPU utilization.
- Disk usage.
- Task duration.
- Browser process count.
- Network usage where measurable.

## 13.5 Benchmark reporting

Every experiment should produce a report.

Suggested format:

    # Experiment: Firefox persistent profile

    Date:
    Hardware:
    OS:
    Software versions:

    ## Objective

    ## Configuration

    ## Procedure

    ## Results

    ## Resource consumption

    ## Problems

    ## Comparison

    ## Conclusion

    ## Next experiment

Distinguish facts from assumptions.

Use these labels:

- FACT
- OBSERVATION
- INFERENCE
- ASSUMPTION
- UNKNOWN

Do not present assumptions as established facts.

---

# 14. PROPOSED REPOSITORY STRUCTURE

The following is the target structure, not an instruction to create every directory immediately.

    web-lab/
    |
    +-- CLAUDE.md
    +-- AGENTS.md
    +-- DEVELOPMENT_PLAN.md
    +-- README.md
    +-- .gitignore
    |
    +-- shared/
    |   |
    |   +-- browser/
    |   +-- networking/
    |   +-- logging/
    |   +-- utilities/
    |
    +-- development/
    |   |
    |   +-- skills/
    |   +-- tools/
    |   +-- templates/
    |   +-- benchmarks/
    |
    +-- parsing/
    |   |
    |   +-- skills/
    |   +-- engines/
    |   +-- extractors/
    |   +-- storage/
    |   +-- benchmarks/
    |
    +-- infrastructure/
    |   |
    |   +-- browser/
    |   +-- vnc/
    |   +-- services/
    |   +-- scripts/
    |   +-- docker/
    |
    +-- projects/
    |   |
    |   +-- avito/
    |   +-- wildberries/
    |   +-- websites/
    |
    +-- tests/
    |
    +-- benchmarks/
    |
    +-- docs/
        |
        +-- architecture/
        +-- installation/
        +-- experiments/
        +-- decisions/

The repository structure may change based on actual implementation needs.

Do not create empty directories simply to match this diagram.

---

# 15. IMPLEMENTATION ROADMAP

Work through the following phases.

Do not skip phases without documenting why.

## PHASE 0 — ENVIRONMENT AUDIT

Objective: understand the existing Raspberry Pi and Ubuntu environments.

Inspect:

- OS.
- Kernel.
- Architecture.
- CPU.
- RAM.
- Storage.
- Python.
- Git.
- Docker.
- Firefox.
- Playwright.
- VNC.
- OpenCode.
- Network interfaces.
- VPN.
- DNS.
- Routing.
- Avito connectivity.

Requirements:

- Read-only inspection initially.
- Do not install packages.
- Do not modify network configuration.
- Do not change existing services.

Deliverables:

- Raspberry Pi audit report.
- Ubuntu audit report.
- Existing software inventory.
- Network overview.
- Identified limitations.
- Proposed installation plan.

## PHASE 1 — BROWSER LABORATORY

Objective: establish persistent browser functionality.

Experiments:

1. Firefox installation verification.
2. Firefox profile creation.
3. Persistent profile testing.
4. Playwright Python compatibility.
5. Browser control.
6. Screenshot capture.
7. DOM inspection.
8. VNC interaction.
9. Browser lifecycle.
10. Recovery after OpenCode restart.

Deliverable:

A persistent Firefox session on Raspberry Pi that can be controlled remotely.

## PHASE 2 — OPENCode INTEGRATION

Objective: make the browser accessible to both OpenCode installations.

Experiments:

- Local OpenCode control.
- Remote OpenCode control.
- MCP integration.
- Python API integration.
- Browser profile locking.
- Concurrent access prevention.
- Error reporting.

Deliverable:

Both computers can use the same browser infrastructure without conflicting control.

## PHASE 3 — AVITO PARSING

Objective: establish the first functional parsing workflow.

Experiments:

- Connectivity.
- VPN behavior.
- Browser rendering.
- DOM inspection.
- Data identification.
- HTTP extraction.
- Browser extraction.
- Pagination.
- Human intervention.
- Structured output.

Deliverable:

A reproducible Avito parser using the persistent browser when required.

## PHASE 4 — WEBSITE DEVELOPMENT

Objective: establish the website development workflow.

Experiments:

- Python backend frameworks.
- HTML templating.
- Vanilla JavaScript.
- CSS.
- Website inspection.
- Screenshot comparison.
- Design reproduction.
- Existing website modification.
- Functional testing.

Deliverable:

An AI-assisted development workflow capable of creating and modifying working websites.

## PHASE 5 — OPTIMIZATION

Objective: select the best technologies.

Compare:

- Reliability.
- Performance.
- Resource consumption.
- Complexity.
- Maintenance.
- Model compatibility.
- Browser compatibility.
- Cost.

Deliverable:

Documented technology decisions and stable project architecture.

## PHASE 6 — CONTROLLED AUTONOMY

Objective: gradually enable autonomous operations.

Only begin after the development and parsing workflows have passed their tests.

Introduce:

- Explicit permission profiles.
- Task isolation.
- Resource limits.
- Automated tests.
- Error recovery.
- Logging.
- Backup procedures.
- Rollback.

Deliverable:

A controlled autonomous development and parsing environment.

---

# 16. DEFINITION OF DONE

A component is not complete merely because its code has been written.

## Browser infrastructure is complete when:

- Firefox runs on the Pi.
- Persistent profiles work.
- Browser state survives OpenCode restarts.
- Browser remains open after task completion.
- VNC interaction works.
- Browser can be controlled from Ubuntu.
- Conflicting profile access is prevented.
- Errors are logged.
- Recovery behavior is documented.

## Parsing module is complete when:

- A URL can be supplied as input.
- The agent can inspect the website.
- An appropriate extraction method can be selected.
- Data can be extracted.
- Output is structured.
- Failures are reported.
- Human intervention works.
- The browser session is preserved.
- Repeated execution is reliable.

## Development module is complete when:

- The agent can create a working Python website.
- The agent can inspect an existing website.
- The agent can reproduce a reference design.
- The agent can modify existing HTML/CSS/JS.
- JavaScript functionality is tested.
- Backend functionality is tested.
- Screenshots can be compared.
- Existing functionality is preserved.

## Overall project is mature when:

- Both modules operate independently.
- Shared infrastructure is stable.
- OpenCode works on both machines.
- Git synchronization is reliable.
- Runtime data is protected.
- Resource consumption is understood.
- Operations are documented.
- Recovery procedures have been tested.

---

# 17. DOCUMENTATION STANDARDS

Every significant implementation should have documentation.

Maintain:

- README.md — project overview and entry point.
- CLAUDE.md — project-wide AI instructions.
- AGENTS.md — OpenCode agent instructions.
- DEVELOPMENT_PLAN.md — current phase, completed and verified steps, next steps, open decisions.
- Architecture documentation.
- Installation documentation.
- Experiment reports.
- Technology decision records.
- Troubleshooting documentation.

For significant architectural decisions, create a decision record:

    # ADR-001: Browser automation architecture

    Status: Proposed / Accepted / Rejected

    ## Context

    ## Options

    ## Evaluation criteria

    ## Experiments

    ## Decision

    ## Consequences

    ## Reconsideration conditions

Do not silently change an established architectural decision.

Document the reason for changes.

---

# 18. GENERAL AGENT BEHAVIOR

When working on this project, the AI agent must follow this workflow.

## Before starting a task

1. Read this CLAUDE.md.
2. Read DEVELOPMENT_PLAN.md for the current phase, status and open decisions.
3. Read relevant module instructions.
4. Inspect the current repository.
5. Inspect relevant existing implementations.
6. Identify assumptions and missing information.
7. Formulate a plan.
8. Obtain approval when required.

## During implementation

1. Make small changes.
2. Preserve existing functionality.
3. Avoid unnecessary dependencies.
4. Use Python by default.
5. Follow existing coding conventions.
6. Test each logical change.
7. Record errors.
8. Avoid unrelated modifications.

## After implementation

1. Run relevant tests.
2. Verify actual behavior.
3. Report changed files.
4. Report test results.
5. Report known limitations.
6. Update documentation.
7. Update DEVELOPMENT_PLAN.md: mark only what was actually verified as done.
8. Identify the next logical experiment.

## When encountering problems

Do not immediately rewrite the system.

Instead:

1. Capture the error.
2. Inspect logs.
3. Reproduce the failure.
4. Identify the responsible component.
5. Check whether the problem is environmental or code-related.
6. Test a minimal fix.
7. Verify that the fix works.

## When uncertain

Ask the user.

Do not invent:

- Installed software versions.
- Network configurations.
- Browser behavior.
- Website access mechanisms.
- Credentials.
- API availability.
- Model quotas.
- Test results.

Clearly distinguish verified facts from hypotheses.

---

# 19. IMMEDIATE PRIORITIES

At the start of the project, prioritize these objectives:

1. Audit the Raspberry Pi.
2. Audit the Ubuntu PC.
3. Understand the existing VPN and Avito connectivity.
4. Verify Firefox and VNC.
5. Test persistent Firefox profiles.
6. Test Playwright on ARM64.
7. Establish remote browser control.
8. Establish OpenCode integration.
9. Implement the first human-intervention workflow.
10. Begin Avito parsing experiments.
11. Begin website development experiments.

Do not start PostgreSQL installation before its need is established.

Do not introduce multiple browser engines before the initial Firefox experiments are complete.

Do not build an elaborate orchestration framework before proving the basic browser workflow.

---

# 20. FINAL PROJECT DIRECTIVE

Web Lab is an experimental engineering project.

The goal is not to use a particular framework, browser or AI model.

The goal is to discover and implement the most reliable, maintainable and resource-efficient architecture for AI-assisted website development and parsing.

The Raspberry Pi is the persistent browser and execution server.

The Ubuntu PC is an additional development and control environment.

OpenCode is the primary AI orchestration layer.

Python is the primary implementation language.

Firefox is the initial persistent browser.

Avito is the first parsing target.

Website Development and Website Parsing are separate functional modules sharing common infrastructure.

Human intervention through VNC is a required capability.

Git is the source-code synchronization mechanism.

PostgreSQL is a future storage candidate.

Autonomous operation is a future objective, not a current permission.

**The agent must prioritize verified functionality, reproducibility, security, low resource consumption and clear documentation over architectural complexity.**

Never confuse an implemented feature with a tested feature.

Never confuse a successful experiment with a production-ready solution.

Always document what has actually been verified.