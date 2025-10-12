---
applyTo: '*'
description: 'Canonical list of platforms, languages, and tools used by the team for task scoping, suggestions, and code generation context.'
---

# Technologies Stack (Authoritative)

## Azure Services
Azure Synapse; Azure Storage Accounts; Azure Functions; Azure Logic Apps; Azure Analysis Services; Databricks; Azure Data Factory; SQL Server; Azure DevOps; Power BI

## Programming Languages
Python; SQL; DAX; HTML; JavaScript; C#

## Core Tools
Visual Studio Code; GitHub; DAX Studio; Tabular Editor; Microsoft SQL Server Management Studio; Postman; draw.io; Microsoft Teams; OneNote

## Usage Guidance
- Prefer Azure-native services when designing new data workflows (Data Factory / Synapse / Functions / Logic Apps).
- BI & semantic layer tasks: Power BI + Analysis Services (DAX focus).
- Heavy data processing / notebooks: Databricks or Synapse (decide based on existing pipeline locality & cost/latency considerations).
- Web integration or lightweight service glue: Azure Functions (serverless) or small web component (React) + optional Django backend.

## Task Authoring Rules
1. Include a `Technologies:` line in new task files when the scope depends on a specific platform or language (e.g., `Technologies: Azure Data Factory, Python`).
2. When deciding between Synapse vs Databricks, document the rationale (cost, performance, ecosystem, skill alignment).
3. For BI tasks involving DAX, explicitly state required performance or model optimization acceptance criteria.
4. For serverless workloads, specify trigger type (Timer, HTTP, Event Grid, etc.).

## Execution-Time Guidance (For Copilot)
- Infer missing technology tags based on task description and suggest adding them.
- Recommend Azure service alignment (e.g., ADF for orchestration, Functions for event-driven compute).
- Prompt for data quality validation steps in pipeline tasks.
- Suggest performance validation (e.g., DAX query timings, pipeline throughput) when absent in acceptance criteria.

## Prohibited Assumptions
- Do not introduce unlisted technologies without explicit task-driven justification.
- Do not assume migration between platforms (e.g., Databricks -> Synapse) unless directed.

---
