# Project Setup Instructions

> Use these instructions with GitHub Copilot to automatically recreate the full project template from only the `.github` folder. This will restore all folders and files as described below, with exact content for each file.

## 1. Create `.vscode` folder and its contents

- Create folder: `.vscode`
- Create file: `.vscode/settings.json` with three color values for:
  - `titleBar.activeBackground`
  - `titleBar.inactiveBackground`
  - `statusBar.background`

**Choose the three colors arbitrarily, but ensure they are from the same theme (e.g., all pastel, all dark, all vibrant, etc.) so they look nice together.**

Example (replace with your own theme-matching colors):

```jsonc
{
  "workbench.colorCustomizations": {
    "titleBar.activeBackground": "#A3CEF1",
    "titleBar.inactiveBackground": "#5390D9",
    "statusBar.background": "#29335C"
  }
}
```

## 2. Create `.github` folder structure and prompt files

- Create folder: `.github/prompts` (if not exists)
- Create folder: `.github/instructions` (if not exists)

- Create file: `.github/prompts/task-creator.prompt.md`:

```markdown
# Task Creator Prompt 

## Purpose 

Guide the creation of new task files in `/docs/tasks` and ensure they are properly cataloged for execution. 

## Instructions 

1. **Receive Task Intention** 

  - You will be provided with a description or intention for a new task. 

  - If the intention is unclear or lacks necessary details, ask for clarification before proceeding. 


2. **MANDATORY STEP: Retrieve and Display Timestamp**

  - Before creating the task file, retrieve and display the current local date and time in the format `YYYYMMDD-HHmm`. You should execute a command to get the current local date and time of the machine you are running on.
  - Confirm this value in your response and use it in the filename.
  - Do not proceed until you have displayed and confirmed the exact timestamp.

3. **Create Task File** 

  - Use the confirmed timestamp to create a new file in `docs/tasks` following the format: `T-YYYYMMDD-HHmm-short-description.task.md`. 

    - `YYYYMMDD`: Current date (year, month, day). 
    - `HHmm`: Current time (24-hour format, hours and minutes). Be sure you have taken the current local time of the machine you are running on.
    - `short-description`: Brief summary of the task's purpose, using hyphens to separate words. 

  - The task file must include: 

    - A clear and concise title. 
    - A detailed description of what needs to be done. 
    - Any specific requirements or constraints. 
    - Acceptance criteria to define when the task is considered complete. 

  - Ensure the task is actionable and can be completed independently. 

4. **Update Tasks Catalog**
- After creating the task file, update the `docs/tasks-catalog.md` file to include the new task with a status of `not-started`.

4. **Additional Guidelines**
- Make sure to follow the existing format and style used in the `docs/tasks-catalog.md` file.
- Do not modify any other files or content outside of creating the new task file and updating the tasks catalog.
- If the text provided is unclear or lacks necessary details, ask for clarification before proceeding.
```

- Create file: `.github/prompts/task-executor.prompt.md`:

```markdown
# Task Executor Prompt

## Purpose
Automate the process of checking for new tasks in `/docs/tasks`, updating `tasks-catalog.md`, and executing not-started tasks in chronological order.

## Instructions
   - Read the `docs/tasks-catalog.md` file to identify existing tasks and their statuses.
   - Ensure the table with the tasks is sorted by date and time from the filename.
   - Find the first by time task with status `not-started` and follow the next instructions for it.
   - Change its status to `in-progress` in `docs/tasks-catalog.md`.
   - Open the corresponding task file in `docs/tasks/`.
   - Read the task definition and follow the instructions to execute the task.
   - If the task description is unclear or lacks necessary details, ask for clarification before proceeding.
   - First create a detailed plan for completing the task and write it down at the end of the task definition file in a new section `## Execution Plan`.
   - Then start executing the task step-by-step, documenting each step in an execution log written in the same task file under new `## Execution Log` section. 
   - In this execution log section, write: 
     - Each step taken, including details, decisions, and references found. 
     - The flow of execution, status of tests, and any encountered issues or resolutions. 
     - Any additional information relevant to the execution. 
   - At the end of the task create tests to verify the task completion and document their results in a new section `## Test Results`. In this section, write: 
     - The tests created to verify the task completion. 
     - The results of each test (pass/fail) and any relevant details. 
   - If the task needs to be executed again, create a new log entry with a new timestamp in the same task file. 
   - Save the execution log in the same task file under the `## Execution Log` section. 
   - After completion, update status to `done` in `tasks-catalog.md`. 
   - Make sure that the task row in `tasks-catalog.md` is moved in the section of completed tasks, maintaining the chronological order.
   - If in the section with the completed tasks there is at least one real task, remove the example row from that section.
   - If the section with active tasks is empty, add an example row to that section.

   - Proceed to the next not-started task in chronological order. 

## Notes
- Only one task should be `in-progress` at a time.
- All actions must be logged in `tasks-catalog.md`.
- Task execution should follow the instructions in each task file.
```

- Create file: `.github/instructions/task-creator-instructions.instructions.md`:

```markdown
---
applyTo: '**/**/docs/tasks/T-*.task.md'
---

- **VERY IMPORTANT**: Do not perform any changes to the codebase or documentation (except creation of tasks themselves) without this to be asked in a task file in docs/tasks/ folder. You should only suggest changes if you are asked to do so in a task file. Read the instructions in /.github/instructions/task-creator-instructions.instructions.md carefully and follow them exactly.
```

- Create file: `.github/instructions/python.instructions.md`:

```markdown
---
description: 'Python coding conventions and guidelines'
applyTo: '**/*.py'
---

# Python Coding Conventions

## Python Instructions

- Write clear and concise comments for each function.
- Ensure functions have descriptive names and include type hints.
- Provide docstrings following PEP 257 conventions.
- Use the `typing` module for type annotations (e.g., `List[str]`, `Dict[str, int]`).
- Break down complex functions into smaller, more manageable functions.

## General Instructions

- Always prioritize readability and clarity.
- For algorithm-related code, include explanations of the approach used.
- Write code with good maintainability practices, including comments on why certain design decisions were made.
- Handle edge cases and write clear exception handling.
- For libraries or external dependencies, mention their usage and purpose in comments.
- Use consistent naming conventions and follow language-specific best practices.
- Write concise, efficient, and idiomatic code that is also easily understandable.

## Code Style and Formatting

- Follow the **PEP 8** style guide for Python.
- Maintain proper indentation (use 4 spaces for each level of indentation).
- Ensure lines do not exceed 79 characters.
- Place function and class docstrings immediately after the `def` or `class` keyword.
- Use blank lines to separate functions, classes, and code blocks where appropriate.

## Edge Cases and Testing

- Always include test cases for critical paths of the application.
- Account for common edge cases like empty inputs, invalid data types, and large datasets.
- Include comments for edge cases and the expected behavior in those cases.
- Write unit tests for functions and document them with docstrings explaining the test cases.

## Example of Proper Documentation

```python
def calculate_area(radius: float) -> float:
    """
    Calculate the area of a circle given the radius.
    
    Parameters:
    radius (float): The radius of the circle.
    
    Returns:
    float: The area of the circle, calculated as π * radius^2.
    """
    import math
    return math.pi * radius ** 2
```
```

- Create file: `.github/instructions/devops-core-principles.instructions.md`:

```markdown
---
applyTo: '*'
description: 'Foundational instructions covering core DevOps principles, culture (CALMS), and key metrics (DORA) to guide GitHub Copilot in understanding and promoting effective software delivery.'
---

# DevOps Core Principles

## Your Mission

As GitHub Copilot, you must understand and advocate for the core principles of DevOps. Your goal is to guide developers in adopting a collaborative, automated, and continuously improving software delivery culture. When generating or reviewing code, always consider how it aligns with these foundational principles.

## What is DevOps?

DevOps is a set of practices that combines software development (Dev) and IT operations (Ops) to shorten the systems development life cycle while delivering features, fixes, and updates frequently in close alignment with business objectives. It's a cultural, philosophical, and technical shift aimed at increasing an organization's ability to deliver applications and services at high velocity.

It emphasizes communication, collaboration, integration, and automation to improve the flow of work between development and operations teams. This leads to faster time to market, increased reliability, improved security, and greater customer satisfaction. DevOps is not a methodology like Agile, but rather a set of principles and practices that can be applied to various methodologies.

## The CALMS Framework (Pillars of DevOps)

CALMS is an acronym that represents the five key pillars of a successful DevOps culture. You should always consider these when analyzing or generating DevOps-related code or advice. This framework provides a holistic view of what's needed to truly embed DevOps principles within an organization.

### 1. **C - Culture**
- **Principle:** Foster a collaborative, blameless culture that prioritizes shared responsibility, trust, and continuous learning.
- **Deeper Dive:**
    - **Breaking Down Silos:** Encourage communication and empathy between development, operations, security, and even business teams. Promote cross-functional understanding of challenges and goals.
    - **Shared Responsibility:** Shift from "it's ops' problem" or "it's dev's bug" to "we own this together." This includes owning the code from commit to production and beyond.
    - **Blameless Post-Mortems:** When incidents occur, focus on identifying systemic issues and learning opportunities rather than assigning blame. This encourages transparency and psychological safety.
    - **Continuous Learning & Improvement:** Promote a growth mindset. Encourage experimentation, knowledge sharing, and adapting to new tools and practices.
    - **Feedback Loops:** Establish fast and clear feedback channels between all stages of the software delivery lifecycle and between teams.
- **Guidance for Copilot:**
    - When discussing code reviews, suggest adding context about the 'why' behind changes, fostering understanding.
    - In problem-solving scenarios, suggest investigating across the entire pipeline, not just the code.
    - When generating documentation, emphasize clarity and accessibility for both developers and operations personnel.
    - Recommend communication tools or practices (e.g., daily stand-ups, shared chat channels) where appropriate in a team context.
    - Advise on creating runbooks that are clear and executable by anyone in the team, not just experts.
- **Key Takeaway:** People and their interactions are paramount. Technology is an enabler, not the solution itself. A strong DevOps culture is the foundation upon which all other pillars stand.

### 2. **A - Automation**
- **Principle:** Automate everything possible across the software delivery lifecycle to reduce manual effort, increase speed, and minimize human error.
- **Deeper Dive:**
    - **CI/CD Pipelines:** Automate the build, test, integrate, and deploy stages. This is the backbone of fast, reliable releases.
    - **Infrastructure as Code (IaC):** Manage and provision infrastructure through code (e.g., Terraform, Ansible, Pulumi) rather than manual processes. This ensures consistency, repeatability, and version control.
    - **Configuration Management:** Automate the configuration of servers and application environments (e.g., Ansible, Puppet, Chef).
    - **Automated Testing:** Implement a robust testing strategy including unit, integration, end-to-end, performance, and security tests. Automate their execution in the pipeline.
    - **Monitoring & Alerting:** Automate the collection of metrics, logs, and traces, and set up automated alerts for anomalies.
    - **Security Automation:** Integrate security scans (SAST, DAST, SCA) directly into the CI/CD pipeline.
- **Guidance for Copilot:**
    - When generating CI/CD pipelines (e.g., GitHub Actions workflows), prioritize automation of builds, tests, deployments, and security scans.
    - Suggest automation for infrastructure provisioning (IaC) and configuration management snippets (e.g., basic Terraform, Ansible playbooks).
    - Recommend automating repetitive operational tasks (e.g., log analysis scripts, auto-scaling configurations).
    - Highlight the benefits of comprehensive automated testing (unit, integration, E2E) and help generate test cases.
    - When asked about deployment, suggest fully automated blue/green or canary deployments where feasible.
- **Key Takeaway:** If a task is repeatable, it should be automated. This frees up engineers for more complex problems, reduces human error, and ensures consistency. Automation accelerates feedback loops and increases delivery velocity.

### 3. **L - Lean**
- **Principle:** Apply lean manufacturing principles to software development, focusing on eliminating waste, maximizing flow, and delivering value continuously.
- **Deeper Dive:**
    - **Eliminating Waste:** Identify and remove non-value-adding activities (e.g., excessive documentation, unnecessary approvals, waiting times, manual handoffs, defect re-work).
    - **Maximizing Flow:** Ensure a smooth, continuous flow of value from idea to production. This involves reducing batch sizes (smaller commits, smaller PRs, frequent deployments).
    - **Value Stream Mapping:** Understand the entire process of delivering software to identify bottlenecks and areas for improvement.
    - **Build Quality In:** Integrate quality checks throughout the development process, rather than relying solely on end-of-cycle testing. This reduces the cost of fixing defects.
    - **Just-in-Time Delivery:** Deliver features and fixes as soon as they are ready, rather than waiting for large release cycles.
- **Guidance for Copilot:**
    - Suggest breaking down large features or tasks into smaller, manageable chunks (e.g., small, frequent PRs, iterative deployments).
    - Advocate for minimal viable products (MVPs) and iterative development.
    - Help identify and suggest removal of bottlenecks in the pipeline by analyzing the flow of work.
    - Promote continuous improvement loops based on fast feedback and data analysis.
    - When writing code, emphasize modularity and testability to reduce future waste (e.g., easier refactoring, fewer bugs).
- **Key Takeaway:** Focus on delivering value quickly and iteratively, minimizing non-value-adding activities. A lean approach enhances agility and responsiveness.

### 4. **M - Measurement**
- **Principle:** Measure everything relevant across the delivery pipeline and application lifecycle to gain insights, identify bottlenecks, and drive continuous improvement.
- **Deeper Dive:**
    - **Key Performance Indicators (KPIs):** Track metrics related to delivery speed, quality, and operational stability (e.g., DORA metrics).
    - **Monitoring & Logging:** Collect comprehensive application and infrastructure metrics, logs, and traces. Centralize them for easy access and analysis.
    - **Dashboards & Visualizations:** Create clear, actionable dashboards to visualize the health and performance of systems and the delivery pipeline.
    - **Alerting:** Configure effective alerts for critical issues, ensuring teams are notified promptly.
    - **Experimentation & A/B Testing:** Use metrics to validate hypotheses and measure the impact of changes.
    - **Capacity Planning:** Use resource utilization metrics to anticipate future infrastructure needs.
- **Guidance for Copilot:**
    - When designing systems or pipelines, suggest relevant metrics to track (e.g., request latency, error rates, deployment frequency, lead time, mean time to recovery, change failure rate).
    - Recommend robust logging and monitoring solutions, including examples of structured logging or tracing instrumentation.
    - Encourage setting up dashboards and alerts based on common monitoring tools (e.g., Prometheus, Grafana).
    - Emphasize using data to validate changes, identify areas for optimization, and justify architectural decisions.
    - When debugging, suggest looking at relevant metrics and logs first.
- **Key Takeaway:** You can't improve what you don't measure. Data-driven decisions are essential for identifying areas for improvement, demonstrating value, and fostering a culture of continuous learning.

### 5. **S - Sharing**
- **Principle:** Promote knowledge sharing, collaboration, and transparency across teams.
- **Deeper Dive:**
    - **Tooling & Platforms:** Share common tools, platforms, and practices across teams to ensure consistency and leverage collective expertise.
    - **Documentation:** Create clear, concise, and up-to-date documentation for systems, processes, and architectural decisions (e.g., runbooks, architectural decision records).
    - **Communication Channels:** Establish open and accessible communication channels (e.g., Slack, Microsoft Teams, shared wikis).
    - **Cross-Functional Teams:** Encourage developers and operations personnel to work closely together, fostering mutual understanding and empathy.
    - **Pair Programming & Mob Programming:** Promote collaborative coding practices to spread knowledge and improve code quality.
    - **Internal Meetups & Workshops:** Organize sessions for sharing best practices and lessons learned.
- **Guidance for Copilot:**
    - Suggest documenting processes, architectural decisions, and runbooks (e.g., generating markdown templates for ADRs or runbooks).
    - Advocate for shared tools and platforms by suggesting their integration into workflows.
    - Highlight the value of cross-training and pairing by recommending such practices in project setup advice.
    - Recommend clear communication channels and feedback mechanisms within team structures.
    - When generating code, include comments and internal documentation that explain complex logic for better sharing.
- **Key Takeaway:** Breaking down silos and fostering open communication is crucial for collective success. Sharing knowledge and experiences accelerates learning and builds a stronger, more resilient organization.

## The Four Key Metrics of DevOps (DORA Metrics)

These metrics, identified by the DevOps Research and Assessment (DORA) team, are strong indicators of software delivery performance and organizational performance. You should strive to help teams improve these. These metrics are empirically linked to higher organizational performance, including profitability, productivity, and market share.

### 1. **Deployment Frequency (DF)**
- **Definition:** How often an organization successfully releases to production. This measures the speed of delivery.
- **Deeper Dive:**
    - **High Frequency:** Elite performers deploy multiple times per day. This reduces the risk of each deployment, makes debugging easier, and allows for faster feedback.
    - **Small Batches:** High deployment frequency is enabled by deploying small, incremental changes rather than large, infrequent ones.
- **Guidance for Copilot:**
    - When generating CI/CD pipelines, design them for frequent, small, and safe deployments. Suggest automation to reduce deployment friction (e.g., automated testing, blue/green deployments).
    - Advise on breaking down large features into smaller, independently deployable units.
    - Suggest using feature flags to decouple deployment from release, allowing code to be deployed frequently even if features are not yet exposed to users.
- **Goal:** High (Elite performers deploy multiple times per day).
- **Impact:** Faster time to market, quicker feedback, reduced risk per change.

### 2. **Lead Time for Changes (LTFC)**
- **Definition:** The time it takes for a commit to get into production. This measures the speed from development to delivery.
- **Deeper Dive:**
    - **Full Value Stream:** This metric encompasses the entire development process, from code commit to successful deployment in production.
    - **Bottleneck Identification:** A high lead time often indicates bottlenecks in the development, testing, or deployment phases.
- **Guidance for Copilot:**
    - Suggest ways to reduce bottlenecks in the development and delivery process (e.g., smaller PRs, automated testing, faster build times, efficient code review processes).
    - Advise on streamlining approval processes and eliminating manual handoffs.
    - Recommend continuous integration practices to ensure code is merged and tested frequently.
    - Help optimize build and test phases by suggesting caching strategies in CI/CD.
- **Goal:** Low (Elite performers have LTFC less than one hour).
- **Impact:** Rapid response to market changes, faster defect resolution, increased developer productivity.

### 3. **Change Failure Rate (CFR)**
- **Definition:** The percentage of deployments causing a degradation in service (e.g., leading to rollback, hotfix, or outage). This measures the quality of delivery.
- **Deeper Dive:**
    - **Lower is Better:** A low change failure rate indicates high quality and stability in deployments.
    - **Causes:** High CFR can be due to insufficient testing, lack of automated checks, poor rollback strategies, or complex deployments.
- **Guidance for Copilot:**
    - Emphasize robust testing (unit, integration, E2E), automated rollbacks, comprehensive monitoring, and secure coding practices to reduce failures.
    - Suggest integrating static analysis, dynamic analysis, and security scanning tools into the CI/CD pipeline.
    - Advise on implementing pre-deployment health checks and post-deployment validation.
    - Help design resilient architectures (e.g., circuit breakers, retries, graceful degradation).
- **Goal:** Low (Elite performers have CFR of 0-15%).
- **Impact:** Increased system stability, reduced downtime, improved customer trust.

### 4. **Mean Time to Recovery (MTTR)**
- **Definition:** How long it takes to restore service after a degradation or outage. This measures the resilience and recovery capability.
- **Deeper Dive:**
    - **Fast Recovery:** A low MTTR indicates that an organization can quickly detect, diagnose, and resolve issues, minimizing the impact of failures.
    - **Observability:** Strong MTTR relies heavily on effective monitoring, alerting, centralized logging, and tracing.
- **Guidance for Copilot:**
    - Suggest implementing clear monitoring and alerting (e.g., dashboards for key metrics, automated notifications for anomalies).
    - Recommend automated incident response mechanisms and well-documented runbooks for common issues.
    - Advise on efficient rollback strategies (e.g., easy one-click rollbacks).
    - Emphasize building applications with observability in mind (e.g., structured logging, metrics exposition, distributed tracing).
    - When debugging, guide users to leverage logs, metrics, and traces to quickly pinpoint root causes.
- **Goal:** Low (Elite performers have MTTR less than one hour).
- **Impact:** Minimized business disruption, improved customer satisfaction, enhanced operational confidence.

## Conclusion

DevOps is not just about tools or automation; it's fundamentally about culture and continuous improvement driven by feedback and metrics. By adhering to the CALMS principles and focusing on improving the DORA metrics, you can guide developers towards building more reliable, scalable, and efficient software delivery pipelines. This foundational understanding is crucial for all subsequent DevOps-related guidance you provide. Your role is to be a continuous advocate for these principles, ensuring that every piece of code, every infrastructure change, and every pipeline modification aligns with the goal of delivering high-quality software rapidly and reliably.

---

<!-- End of DevOps Core Principles Instructions -->
```

- Create file: `.github/instructions/sql-sp-generation.instructions.md`:

```markdown
---
description: 'Guidelines for generating SQL statements and stored procedures'
applyTo: '**/*.sql'
---

# SQL Development

## Database schema generation
- all table names should be in singular form
- all column names should be in singular form
- all tables should have a primary key column named `id`
- all tables should have a column named `created_at` to store the creation timestamp
- all tables should have a column named `updated_at` to store the last update timestamp

## Database schema design
- all tables should have a primary key constraint
- all foreign key constraints should have a name
- all foreign key constraints should be defined inline
- all foreign key constraints should have `ON DELETE CASCADE` option
- all foreign key constraints should have `ON UPDATE CASCADE` option
- all foreign key constraints should reference the primary key of the parent table

## SQL Coding Style
- use uppercase for SQL keywords (SELECT, FROM, WHERE)
- use consistent indentation for nested queries and conditions
- include comments to explain complex logic
- break long queries into multiple lines for readability
- organize clauses consistently (SELECT, FROM, JOIN, WHERE, GROUP BY, HAVING, ORDER BY)

## SQL Query Structure
- use explicit column names in SELECT statements instead of SELECT *
- qualify column names with table name or alias when using multiple tables
- limit the use of subqueries when joins can be used instead
- include LIMIT/TOP clauses to restrict result sets
- use appropriate indexing for frequently queried columns
- avoid using functions on indexed columns in WHERE clauses

## Stored Procedure Naming Conventions
- prefix stored procedure names with 'usp_'
- use PascalCase for stored procedure names
- use descriptive names that indicate purpose (e.g., usp_GetCustomerOrders)
- include plural noun when returning multiple records (e.g., usp_GetProducts)
- include singular noun when returning single record (e.g., usp_GetProduct)

## Parameter Handling
- prefix parameters with '@'
- use camelCase for parameter names
- provide default values for optional parameters
- validate parameter values before use
- document parameters with comments
- arrange parameters consistently (required first, optional later)


## Stored Procedure Structure
- include header comment block with description, parameters, and return values
- return standardized error codes/messages
- return result sets with consistent column order
- use OUTPUT parameters for returning status information
- prefix temporary tables with 'tmp_'


## SQL Security Best Practices
- parameterize all queries to prevent SQL injection
- use prepared statements when executing dynamic SQL
- avoid embedding credentials in SQL scripts
- implement proper error handling without exposing system details
- avoid using dynamic SQL within stored procedures

## Transaction Management
- explicitly begin and commit transactions
- use appropriate isolation levels based on requirements
- avoid long-running transactions that lock tables
- use batch processing for large data operations
- include SET NOCOUNT ON for stored procedures that modify data
```

- Create file: `.github/copilot-instructions.md`:

```markdown
# RULES

- Do not perform any changes to the codebase or documentation (except creation of tasks themselves) without this to be asked in a task file in docs/tasks/ folder. You should only suggest changes if you are asked to do so. 

- During execution of each task update README.md files with the relevant general information suitable for README.md
- During execution of each task update docs/requirements.md file with the relevant general information suitable for requirements.md
- During execution of each task update docs/developer-guide.md file with the relevant general information suitable for developer-guide.md
- During execution of each task update docs/user-guide.md file with the relevant general information suitable for user-guide.md
- During execution of each task update docs/architecture.md file with the relevant general information suitable for architecture.md
- During execution of each task update docs/folder-structure.md file with the relevant general information suitable for folder-structure.md

- Write clean, modular, and well-documented code to facilitate future maintenance and updates.


# INSTRUCTIONS

Refer to the following files and instructions for all requirements, rules, and structure:

- `docs/folder-structure.md`: File and folder structure specification
- `docs/requirements/functional.requirements.md`: Functional requirements
- `docs/requirements/technical.requirements.md`: Technical requirements and constraints
- `docs/developer-guide.md`: Developer instructions
- `docs/user-guide.md`: User instructions
- `docs/architecture.md`: Architecture and design
- `docs/tasks-catalog.md`: List of all tasks and their status
- `docs/tasks/`: All individual task files
- `.github/prompts/developer.prompt.md`: Main game development prompt
- `.github/prompts/task-executor.prompt.md`: Task execution automation prompt
```

## 3. Create `docs` folder and all subfolders/files

- Create folder: `docs`
- Create file: `docs/architecture.md`:

```markdown
# Architecture

> This is a template file. Replace with your project's architecture documentation.

## System Overview
- [Provide high-level description of the system]
- [Define main components and their interactions]
- [Specify system boundaries and interfaces]

## Architecture Patterns
- [Describe architectural patterns used (MVC, microservices, etc.)]
- [Explain design principles and patterns]
- [Document architectural decisions and rationale]

## Component Architecture
- [Detail major system components]
- [Define component responsibilities and interfaces]
- [Show component relationships and dependencies]

## Data Architecture
- [Describe data models and schemas]
- [Define data flow and storage patterns]
- [Specify data management strategies]

## Deployment Architecture
- [Define deployment topology]
- [Specify infrastructure components]
- [Document scaling and availability strategies]
```

- Create file: `docs/developer-guide.md`:

```markdown
# Developer Guide

> This is a template file. Replace with your project's developer guide.

## Getting Started
- [Prerequisites and setup instructions]
- [Installation and configuration steps]
- [First-time setup and validation]

## Development Environment
- [Required tools and IDEs]
- [Environment setup and configuration]
- [Local development workflow]

## Project Structure
See [docs/folder-structure.md](folder-structure.md) for a complete description of the file and folder organization.

## Coding Standards
- [Code style and formatting guidelines]
- [Naming conventions and best practices]
- [Documentation requirements]

## Testing
- [Testing framework and tools]
- [Test organization and structure]
- [Running and debugging tests]

## Build and Deployment
- [Build process and scripts]
- [Deployment procedures]
- [Environment-specific configurations]

## Contributing
- [Contributing guidelines and process]
- [Code review requirements]
- [Issue reporting and feature requests]
```

- Create file: `docs/folder-structure.md`:

```markdown
# File and Folder Structure

> This template provides a standard project structure for web applications.

## Project Root
- `README.md`: Project overview and setup instructions
- `.github/`: GitHub-specific files (workflows, templates, etc.)
- `docs/`: All project documentation

## src/
The main source code directory
- `assets/`: Static assets (images, fonts, data files, etc.)
- `components/`: Reusable UI components and modules
- `utils/`: Utility functions and helper modules

## docs/
Project documentation and planning
- `requirements/`: Requirements specification
  - `functional.requirements.md`: User and business requirements
  - `technical.requirements.md`: Technical constraints and requirements
- `architecture.md`: System architecture and design
- `developer-guide.md`: Development setup and guidelines
- `user-guide.md`: End-user documentation
- `folder-structure.md`: This file describing project organization
- `tasks/`: Individual task documentation (*.task.md files)
- `tasks-catalog.md`: Overview of all project tasks
- `task-execution-logs/`: Historical task execution records

## Customization
- Modify this structure based on your project's specific needs
- Add additional directories for frameworks, testing, build tools, etc.
- Maintain clear separation between source code, documentation, and configuration
```

- Create file: `docs/requirements/functional.requirements.md`:

```markdown
# Functional Requirements

> This is a template file. Replace with your project's functional requirements.

## User Requirements
- [List what the users need from this application]
- [Define user stories and use cases]
- [Specify target audience and user experience goals]

## Feature Requirements  
- [Define core features and functionality]
- [Specify user interactions and workflows]
- [Define success criteria and acceptance criteria]

## Business Requirements
- [List business objectives and goals]
- [Define scope and constraints]
- [Specify compliance and regulatory requirements]
```

- Create file: `docs/requirements/technical.requirements.md`:

```markdown
# Technical Requirements

> This is a template file. Replace with your project's technical requirements.

## Technology Stack
- [Specify programming languages, frameworks, and libraries]
- [Define browser/platform compatibility requirements]
- [List development tools and build systems]

## Performance Requirements
- [Define response time and throughput requirements]
- [Specify resource usage limits]
- [Set scalability requirements]

## Security Requirements
- [Define authentication and authorization requirements]
- [Specify data protection and privacy requirements]
- [List compliance requirements]

## Infrastructure Requirements
- [Define hosting and deployment requirements]
- [Specify database and storage requirements]
- [List third-party service dependencies]
```

- Create file: `docs/tasks/T-20250929-1854-template.task.md`:

```markdown
# Task Template: Project Setup

**Task ID**: T-YYYYMMDD-NNNN-project-setup  
**Created**: [Date]  
**Assigned**: [Developer Name]  
**Status**: not-started  

## Description
This is a template task file. Replace this content with your actual task details.

## Objectives
- [ ] Define what needs to be accomplished
- [ ] Break down the task into smaller, actionable items
- [ ] Set clear acceptance criteria

## Requirements
- List any prerequisites or dependencies
- Specify any constraints or limitations
- Define success criteria

## Implementation Plan
1. Step-by-step approach to complete the task
2. Include any design decisions or technical considerations
3. Identify potential risks or challenges

## Testing
- How will this task be validated?
- What tests need to be created or updated?
- Definition of "done"

## Notes
- Additional context or considerations
- Links to relevant documentation
- Dependencies on other tasks

## Status Updates
- [Date] - Task created
- [Date] - Status update or progress notes
```

- Create file: `docs/tasks-catalog.md`:

```markdown
# Tasks Catalog

> This is a template file. Replace with your project's task catalog.

## Overview
This file tracks all project tasks, their current status, and provides links to detailed task documentation.

## Active Tasks
| Task ID | Title | Status | Assigned | Due Date |
|---------|-------|--------|----------|----------|
| [Example] | [Task description] | [not-started/in-progress/completed] | [Developer] | [Date] |

## Completed Tasks
| Task ID | Title | Completed Date | Notes |
|---------|-------|----------------|-------|
| [Example] | [Task description] | [Date] | [Completion notes] |

## Task Status Guide
- **not-started**: Task has been identified but work has not begun
- **in-progress**: Task is currently being worked on
- **completed**: Task has been finished and verified
- **blocked**: Task cannot proceed due to dependencies or issues

## Task Management
- All detailed task documentation should be stored in `docs/tasks/`
- Use the format `T-YYYYMMDD-NNNN-short-description.task.md` for task files
- Update this catalog whenever task status changes
```

- Create file: `docs/user-guide.md`:

```markdown
# User Guide

> This is a template file. Replace with your project's user guide.

## Getting Started
- [How to access and start using the application]
- [Initial setup and configuration for users]
- [Overview of main features and capabilities]

## Basic Usage
- [Step-by-step instructions for common tasks]
- [User interface overview and navigation]
- [Core workflows and user journeys]

## Features
- [Detailed description of all features]
- [Use cases and examples]
- [Tips and best practices]

## Troubleshooting
- [Common issues and solutions]
- [Error messages and their meanings]
- [How to get help and support]

## Advanced Usage
- [Advanced features and configurations]
- [Customization options]
- [Integration with other tools]
```

## 3. Create `src` folder and subfolders (all empty)

- Create folder: `src`
- Create empty folders:
  - `src/assets`
  - `src/components`
  - `src/utils`

## 4. Create `README.md` file

- Create file: `README.md`. If the README.md file already exists, rename it to `README-SCATED.md` before creating the new one.

```markdown
# GitHub Copilot Template Project

This is a template repository designed to work with GitHub Copilot using a structured task-based workflow. The repository includes automated prompts and instructions that help you create, manage, and execute development tasks systematically.

## How It Works

This template uses a task-driven development approach where all changes to the codebase are managed through structured task files. Here's how to use it:

### 1. Creating Tasks

To create a new task, start your message to GitHub Copilot with `/task-creator` followed by your task description:

```
/task-creator Create a login page with username and password fields
```

GitHub Copilot will automatically:
- Generate a timestamped task file in `docs/tasks/` (format: `T-YYYYMMDD-HHmm-description.task.md`)
- Add the task to `docs/tasks-catalog.md` with status `not-started`
- Include detailed requirements, objectives, and acceptance criteria

### 2. Executing Tasks

To execute tasks, start your message with `/task-executor`:

```
Execute the next pending task
```

GitHub Copilot will:
- Find the oldest `not-started` task in chronological order
- Change its status to `in-progress` in `docs/tasks-catalog.md`
- Create an execution plan in the task file
- Execute the task step-by-step
- Log all actions in the task file under `## Execution Log`
- Create and run tests to verify completion
- Update status to `completed` when finished

### 3. Monitoring Progress

#### Files That Get Updated

During task execution, these files are automatically updated:

- **`docs/tasks-catalog.md`**: Task status tracking and overview
- **Task files in `docs/tasks/`**: Execution plans, logs, and test results
- **`README.md`**: Project documentation updates
- **`docs/requirements/functional.requirements.md`**: Feature requirements
- **`docs/requirements/technical.requirements.md`**: Technical specifications
- **`docs/developer-guide.md`**: Development instructions
- **`docs/user-guide.md`**: User documentation
- **`docs/architecture.md`**: System architecture
- **`docs/folder-structure.md`**: Project structure documentation

#### Tracking Your Work

1. **Task Overview**: Check `docs/tasks-catalog.md` for a complete list of all tasks and their current status
2. **Individual Tasks**: Review specific task files in `docs/tasks/` for detailed execution logs and results
3. **Project Status**: Monitor the documentation files listed above to see how your project evolves

### 4. Project Structure

```
├── .github/
│   ├── copilot-instructions.md     # GitHub Copilot behavior rules
│   ├── prompts/                    # Automated prompt files
│   └── instructions/               # Additional instruction files
├── .vscode/
│   └── settings.json              # VS Code customizations
├── docs/
│   ├── requirements/              # Project requirements
│   ├── tasks/                     # Individual task files
│   ├── tasks-catalog.md          # Task tracking and status
│   ├── architecture.md           # System architecture
│   ├── developer-guide.md        # Development guidelines
│   ├── user-guide.md             # User documentation
│   └── folder-structure.md       # Project structure guide
├── src/                          # Source code (initially empty)
│   ├── assets/                   # Static files
│   ├── components/               # Reusable components
│   └── utils/                    # Utility functions
└── README.md                     # This file
```

### 5. Best Practices

- **Be Specific**: When creating tasks, provide clear and detailed descriptions
- **One Task at a Time**: The system processes tasks sequentially for better tracking
- **Review Logs**: Check execution logs in task files to understand what was implemented
- **Update Documentation**: The system automatically updates documentation, but review for accuracy
- **Monitor Status**: Regularly check `docs/tasks-catalog.md` to track overall progress

### 6. Getting Started

1. **Create Your First Task**: Use `Task: [your description]` to create your initial development task
2. **Execute It**: Ask GitHub Copilot to execute the task
3. **Review Results**: Check the generated files and documentation
4. **Continue**: Create more tasks as needed for your project

This template ensures consistent development practices, comprehensive documentation, and full traceability of all changes made to your project.

```

---

**After running this prompt, your project will be fully restored to the template structure and contents.**
