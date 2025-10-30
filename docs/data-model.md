# Kolko Ni Struva Product Data Model

## Key Entities

### 1. DataFile
- **Attributes (as implemented):**
  - `raw_path`: Path to raw file in `data/raw/` (filename encodes date and chain)
  - `date`: Inferred from filename (e.g., `kolko_struva_2025-10-10_account_1.csv` → `2025-10-10`)
  - `chain_id`: Inferred from filename (e.g., `kolko_struva_2025-10-10_account_1.csv` → `1`)
  - **Fields in file:**
    - "Населено място" (Settlement code, e.g. EKATTE)
    - "Търговски обект" (Store name and address)
    - "Наименование на продукта" (Product name)
    - "Код на продукта" (Product code)
    - "Категория" (Category code)
    - "Цена на дребно" (Retail price)
    - "Цена в промоция" (Promotional price, may be empty)
  - No explicit `source`, `completeness`, or interim/processed path attributes are tracked in code or files.

### 2. SiteBuild
- **Attributes (as implemented):**
  - `included_dates`: List of dates included in the build (tracked in script logic, not as a file)
  - `output_folder`: Path to build output (e.g., `build/web/`)
  - `status`/`warnings`: Not explicitly tracked or output as a file; warnings are logged to console.

### 3. DimensionTable
- **Attributes (as implemented):**
  - `name`: category, city, or chain
  - `json_path`: Path to JSON file in `data/` and/or `build/web/`
  - **Format:** JSON dictionary mapping string IDs to names, e.g. `{ "1": "Хляб бял", ... }`
  - No explicit array of objects with `id` and `name` fields.

### 4. FactTable
- **Attributes (as implemented):**
  - `name`: prices
  - `csv_path`: `build/web/data.csv`
  - **Fields:**
    - `date` (from filename)
    - `chain_id` (from filename)
    - "Населено място"
    - "Търговски обект"
    - "Наименование на продукта"
    - "Код на продукта"
    - "Категория"
    - "Цена на дребно"
    - "Цена в промоция"
  - No explicit `product_id`, `category_id`, `city_id`, or `unit` columns in the output.

## Relationships
- Each `SiteBuild` references multiple `DataFile` objects (for the last 2 days, inferred from filenames)
- Each `SiteBuild` includes a merged fact table CSV and copies of the nomenclature JSON files as dimension tables.

## Validation Rules
- Only the last 2 days of data are included in each build (enforced by script logic)
- If data for a day is missing, script skips and logs a warning
- Output files are written to `build/web/` (fact table as `data.csv`, dimension tables as JSON dictionaries)
- No explicit completeness checks or validation files are produced.

## State Transitions
- DataFile: raw → merged (no explicit interim or processed file tracked)
- SiteBuild: not materialized as a file; status/warnings are logged only.

## Historical Analytics Support
- Processed (merged) data is retained in `build/web/data.csv` (overwritten on each build)
- Nomenclature files are retained in `data/` and copied to `build/web/`
- Date fields in the fact table support time-series queries and trend analysis

## Folder Structure Reference

## Data File Formats

### 1. Source Data File Format (Raw)
**Location:** `data/raw/`
**Format:** CSV (comma-separated values, UTF-8, quoted fields)
**Fields (Bulgarian, as in real file):**
  - "Населено място" (Settlement code, e.g. EKATTE)
  - "Търговски обект" (Store name and address)
  - "Наименование на продукта" (Product name)
  - "Код на продукта" (Product code)
  - "Категория" (Category code)
  - "Цена на дребно" (Retail price)
  - "Цена в промоция" (Promotional price, may be empty)

**Example header:**
```
"Населено място","Търговски обект","Наименование на продукта","Код на продукта","Категория","Цена на дребно","Цена в промоция"
```

**Example row:**
```
"68134","МАГАЗИН МЛАДОСТ - СОФИЯ, ЖК МЛАДОСТ 2, БУЛ. АЛЕКСАНДЪР МАЛИНОВ 75","КРАВЕ МАСЛО 125 ГР ДИМИТЪР МАДЖАРОВ","040001","11","4.98",""
```

### 2. Interim Data File Format
- **Not implemented in current code or data files.**

### 3. Final Data File Format (Processed)
**Location:** `build/web/`
**Format:**
  - **Dimension Tables:** JSON files in `data/` and copied to `build/web/` (e.g., `category-nomenclature.json`, `cities-ekatte-nomenclature.json`, `trade-chains-nomenclature.json`)
    - **Format:** Dictionary mapping string IDs to names, e.g. `{ "1": "Хляб бял", ... }`
  - **Fact Table:** CSV file as `build/web/data.csv`
    - **Fields:**
      - `date`, `chain_id`, "Населено място", "Търговски обект", "Наименование на продукта", "Код на продукта", "Категория", "Цена на дребно", "Цена в промоция"
    - No explicit `product_id`, `category_id`, `city_id`, or `unit` columns.

## Example File Layouts

### Raw CSV Example
```csv
"Населено място","Търговски обект","Наименование на продукта","Код на продукта","Категория","Цена на дребно","Цена в промоция"
"68134","МАГАЗИН МЛАДОСТ - СОФИЯ, ЖК МЛАДОСТ 2, БУЛ. АЛЕКСАНДЪР МАЛИНОВ 75","КРАВЕ МАСЛО 125 ГР ДИМИТЪР МАДЖАРОВ","040001","11","4.98",""
```

### Dimension JSON Example
```json
{
  "1": "Хляб бял",
  "2": "Хляб тъмен"
}
```

### Fact CSV Example
```csv
date,chain_id,Населено място,Търговски обект,Наименование на продукта,Код на продукта,Категория,Цена на дребно,Цена в промоция
2025-10-25,1,68134,МАГАЗИН МЛАДОСТ - СОФИЯ, ЖК МЛАДОСТ 2, БУЛ. АЛЕКСАНДЪР МАЛИНОВ 75,КРАВЕ МАСЛО 125 ГР ДИМИТЪР МАДЖАРОВ,040001,11,4.98,
```

---

This data model now covers metadata, source, interim, and final data formats for the Kolko Ni Struva product.
