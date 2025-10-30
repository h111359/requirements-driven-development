# Overview

Kolko Ni Struva (Колко Ни Струва - How Much Does It Cost) is a data collection, processing, and visualization system for tracking and analyzing product prices across retail chains and cities in Bulgaria. The system scrapes open data from kolkostruva.bg, processes and normalizes it, and provides an interactive web-based interface for data analysis and price comparisons. The application consists of Python backend scripts for data acquisition and processing, and a client-side web application (HTML/CSS/JavaScript) for data visualization and user interaction.

# General Functionalities

- **[GF-01] Web Data Scraping and Download**: The system shall scrape and download CSV files containing product price data from kolkostruva.bg/opendata for multiple retail chains and dates.

- **[GF-02] Data Merging and Consolidation**: The system shall merge multiple downloaded CSV files from different retail chains and dates into a single consolidated data.csv file, removing duplicates and normalizing data formats.

- **[GF-03] City Code Normalization**: The system shall normalize city codes (EKATTE) to a standardized 5-digit format, handling various input formats including extended codes and padding requirements.

- **[GF-04] Nomenclature Management**: The system shall maintain and utilize JSON-based nomenclatures for categories, cities (EKATTE codes), and trade chains to provide consistent data mapping and reference lookups.

- **[GF-05] Automated Data Updates**: The system shall support automated daily data updates, downloading current and previous day data by default when run without parameters, and maintaining only the latest two days of data.

- **[GF-06] Interactive Web-Based Data Visualization**: The system shall provide an interactive web interface (HTML/CSS/JavaScript) for visualizing and analyzing price data through multiple report types including bar charts and filtered lists.

- **[GF-07] Multi-Date Data Management**: The system shall support selection and analysis of data from multiple dates through a date selector interface, dynamically loading available dates from the consolidated dataset.

- **[GF-08] Automated Deployment to Build Folder**: The system shall automatically deploy updated website files and data to a designated build folder (kolko-ni-struva/) after successful data updates, clearing previous content and copying all necessary files.

- **[GF-09] Netlify Cloud Deployment**: The system shall support automated deployment to Netlify hosting platform via REST API without requiring npm or CLI tools, using token-based authentication.

- **[GF-10] Price Calculation and Analysis**: The system shall calculate effective prices by selecting the minimum between retail price and promotional price for each product, supporting price comparison and analysis across categories and locations.

# Functional requirements

- **[FR-01] CSV Data Extraction from Source Website**: The system shall scrape kolkostruva.bg/opendata web pages to locate and extract CSV download links for specified dates and retail chain account IDs, handling dynamic URL parameters and HTML parsing.

- **[FR-02] Multi-Chain Batch Download**: The system shall iterate through all retail chains defined in the trade-chains-nomenclature.json configuration file and download CSV data for each chain for specified dates, implementing polite scraping with delays between requests.

- **[FR-03] Downloaded File Organization**: The system shall store downloaded CSV files in a dedicated data/raw/ directory with standardized naming convention "kolko_struva_YYYY-MM-DD_account_N.csv" to enable tracking and identification of data sources.

- **[FR-04] Intelligent Duplicate Prevention**: The system shall prevent duplicate records in the merged data by identifying and removing existing rows matching the same date and chain_id combination before adding new data, supporting idempotent re-runs.

- **[FR-05] CSV Delimiter Detection and Normalization**: The system shall automatically detect CSV delimiters (comma, semicolon, or other separators from Excel exports) in source files and normalize all output to comma-separated format with full field quoting (QUOTE_ALL).

- **[FR-06] EKATTE Code Standardization**: The system shall normalize Bulgarian city EKATTE codes to a standard 5-digit format by extracting the first 5 digits from extended codes (e.g., "68134-01" → "68134") and left-padding shorter codes with zeros (e.g., "702" → "00702").

- **[FR-07] Data Schema Standardization**: The system shall enforce a standardized CSV schema with fixed column order: date, chain_id, Населено място, Търговски обект, Наименование на продукта, Код на продукта, Категория, Цена на дребно, Цена в промоция, ensuring consistency across all merged data.

- **[FR-08] Date-Based Data Filtering**: The system shall support filtering data by date ranges, with default behavior of retaining only the latest two days of data to optimize storage and performance, while allowing override to keep all historical data via command-line flag.

- **[FR-09] Multi-Report Web Interface**: The system shall provide three distinct analytical reports accessible via navigation menu: (1) Price-sorted bar chart of categories filtered by city, (2) Price-sorted product list filtered by city and category, (3) Price-sorted list of cities and products filtered by category.

- **[FR-10] Dynamic Filter-Based Report Display**: The system shall automatically refresh and display report results immediately upon filter selection changes without requiring manual button clicks, providing real-time interactive analysis.

- **[FR-11] Nomenclature-Based Data Lookup**: The system shall load and utilize JSON nomenclature files for categories, cities (EKATTE), and trade chains to provide human-readable labels for coded data fields in visualizations and reports.

- **[FR-12] Client-Side CSV Parsing**: The system shall implement client-side CSV parsing with proper handling of quoted fields containing delimiters, ensuring accurate data extraction from the consolidated CSV file in the browser.

- **[FR-13] Effective Price Computation**: The system shall calculate effective price for each product by selecting the minimum value between "Цена на дребно" (retail price) and "Цена в промоция" (promotional price), defaulting to retail price when promotional price is absent or zero.

- **[FR-14] Command-Line Interface for Updates**: The system shall provide a command-line interface with arguments for specifying dates (--dates), data retention policy (--keep-all), deployment control (--no-deploy), and Netlify deployment (--netlify), with sensible defaults for zero-configuration execution.

- **[FR-15] Bulgarian Language Support**: The system shall display all user interface elements, labels, and content in Bulgarian language, including the landing page description, navigation menu, filter labels, and report headings.

# Non-functional requirements

- **[NFR-01] Performance - Page Load Time**: The web application should load and display data within 5 seconds under normal conditions, optimizing for large CSV file handling through efficient client-side parsing and minimal data retention strategy (latest 2 days by default).

- **[NFR-02] Scalability - Multi-Chain Support**: The system should support scraping data from 100+ retail chains as configured in the nomenclature file, with polite scraping delays (0.3s between requests) to respect server resources.

- **[NFR-03] Reliability - Error Handling and Logging**: The system should implement comprehensive logging at INFO level for all operations and gracefully handle errors during web scraping, file operations, and deployment, continuing execution where possible and reporting failures clearly.

- **[NFR-04] Usability - Zero-Configuration Operation**: The system should provide sensible defaults allowing users to run the update script without any parameters for common use cases (downloading today and yesterday's data), while supporting advanced configuration through optional command-line arguments.

- **[NFR-05] Maintainability - Configuration-Driven Architecture**: The system should externalize all configuration data (retail chains, categories, cities) in JSON files, enabling updates without code modifications and supporting data consistency across components.

- **[NFR-06] Portability - No Build Tools Required**: The web application should run entirely client-side using vanilla HTML/CSS/JavaScript without requiring npm, build processes, or server-side dependencies, ensuring easy deployment to any static hosting platform.

- **[NFR-07] Security - Token-Based Authentication**: The system should use environment variable-based authentication (NETLIFY_AUTH_TOKEN) for deployment operations, avoiding hardcoded credentials and supporting secure CI/CD integration.

# Technical requirements

- **[TR-01] Python Runtime Environment**: The system shall require Python 3.x runtime with support for virtual environments (venv) for isolated dependency management.

- **[TR-02] Python Dependencies**: The system shall depend on the following Python packages: requests (HTTP client for web scraping and API calls), beautifulsoup4 (HTML parsing for web scraping), csv (built-in, CSV file processing), json (built-in, JSON processing), argparse (built-in, command-line interface), logging (built-in, application logging), shutil (built-in, file operations), hashlib (built-in, file hashing for Netlify deployment).

- **[TR-03] Web Technologies Stack**: The web application shall be built using: HTML5 for structure and semantic markup, CSS3 for styling and responsive layout, Vanilla JavaScript (ES6+) for client-side logic, No frameworks or build tools required.

- **[TR-04] Data Format Standards**: The system shall use the following data formats: CSV (RFC 4180 compliant) with QUOTE_ALL for fact data storage, JSON for configuration and nomenclature files, UTF-8 encoding for all text files to support Bulgarian Cyrillic text.

- **[TR-05] Deployment Platform**: The system shall support deployment to Netlify static hosting platform via REST API (v1), using token-based authentication and direct file upload without CLI dependencies.

- **[TR-06] Version Control**: The system shall use Git for version control with a minimal .gitignore configuration excluding generated data files (data/raw/, data.csv), virtual environments (.venv/), and build outputs (kolko-ni-struva/ deployment folder).

- **[TR-07] External Data Source**: The system shall integrate with kolkostruva.bg/opendata as the authoritative data source, supporting date and account ID parameters for targeted data retrieval.
