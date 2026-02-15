---
name: csv-pipeline
description: 处理、转换、分析并报告 CSV 和 JSON 数据文件。适用于用户需要过滤数据行、合并数据集、计算聚合值、转换数据格式、去除重复数据或从表格数据生成汇总报告的场景。支持处理任何类型的 CSV、TSV 或 JSON 文件。
metadata: {"clawdbot":{"emoji":"📊","requires":{"anyBins":["python3","python","uv"]},"os":["linux","darwin","win32"]}}
---

# CSV 数据管道

使用标准的命令行工具和 Python 处理表格数据（CSV、TSV、JSON、JSON 行格式）。除了 Python 3 之外，不需要任何外部依赖。

## 使用场景

- 用户提供 CSV/TSV/JSON 文件，并要求对其进行分析、转换或生成报告
- 合并、过滤、分组或汇总表格数据
- 在不同格式之间进行转换（如 CSV 到 JSON、JSON 到 CSV 等）
- 去重、排序或清洗杂乱的数据
- 生成汇总统计信息或报告
- ETL 工作流程：从一种格式提取数据，进行转换，然后加载到另一种格式

## 使用标准工具的快速操作

### 检查数据

```bash
# Preview first rows
head -5 data.csv

# Count rows (excluding header)
tail -n +2 data.csv | wc -l

# Show column headers
head -1 data.csv

# Count unique values in a column (column 3)
tail -n +2 data.csv | cut -d',' -f3 | sort -u | wc -l
```

### 使用 `awk` 进行过滤

```bash
# Filter rows where column 3 > 100
awk -F',' 'NR==1 || $3 > 100' data.csv > filtered.csv

# Filter rows matching a pattern in column 2
awk -F',' 'NR==1 || $2 ~ /pattern/' data.csv > matched.csv

# Sum column 4
awk -F',' 'NR>1 {sum += $4} END {print sum}' data.csv
```

### 排序和去重

```bash
# Sort by column 2 (numeric)
head -1 data.csv > sorted.csv && tail -n +2 data.csv | sort -t',' -k2 -n >> sorted.csv

# Deduplicate by all columns
head -1 data.csv > deduped.csv && tail -n +2 data.csv | sort -u >> deduped.csv

# Deduplicate by specific column (keep first occurrence)
awk -F',' '!seen[$2]++' data.csv > deduped.csv
```

## 使用 Python 进行复杂的数据转换

### 读取和检查数据

```python
import csv, json, sys
from collections import Counter

def read_csv(path, delimiter=','):
    """Read CSV/TSV into list of dicts."""
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f, delimiter=delimiter))

def write_csv(rows, path, delimiter=','):
    """Write list of dicts to CSV."""
    if not rows:
        return
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys(), delimiter=delimiter)
        writer.writeheader()
        writer.writerows(rows)

# Quick stats
data = read_csv('data.csv')
print(f"Rows: {len(data)}")
print(f"Columns: {list(data[0].keys())}")
for col in data[0]:
    non_empty = sum(1 for r in data if r[col].strip())
    print(f"  {col}: {non_empty}/{len(data)} non-empty")
```

### 过滤和转换数据

```python
# Filter rows
filtered = [r for r in data if float(r['amount']) > 100]

# Add computed column
for r in data:
    r['total'] = str(float(r['price']) * int(r['quantity']))

# Rename columns
renamed = [{('new_name' if k == 'old_name' else k): v for k, v in r.items()} for r in data]

# Type conversion
for r in data:
    r['amount'] = float(r['amount'])
    r['date'] = r['date'].strip()
```

### 分组和汇总数据

```python
from collections import defaultdict

def group_by(rows, key):
    """Group rows by a column value."""
    groups = defaultdict(list)
    for r in rows:
        groups[r[key]].append(r)
    return dict(groups)

def aggregate(rows, group_col, agg_col, func='sum'):
    """Aggregate a column by groups."""
    groups = group_by(rows, group_col)
    results = []
    for name, group in sorted(groups.items()):
        values = [float(r[agg_col]) for r in group if r[agg_col].strip()]
        if func == 'sum':
            agg = sum(values)
        elif func == 'avg':
            agg = sum(values) / len(values) if values else 0
        elif func == 'count':
            agg = len(values)
        elif func == 'min':
            agg = min(values) if values else 0
        elif func == 'max':
            agg = max(values) if values else 0
        results.append({group_col: name, f'{func}_{agg_col}': str(agg), 'count': str(len(group))})
    return results

# Example: sum revenue by category
summary = aggregate(data, 'category', 'revenue', 'sum')
write_csv(summary, 'summary.csv')
```

### 合并数据集

```python
def inner_join(left, right, on):
    """Inner join two datasets on a key column."""
    right_index = {}
    for r in right:
        key = r[on]
        if key not in right_index:
            right_index[key] = []
        right_index[key].append(r)

    results = []
    for lr in left:
        key = lr[on]
        if key in right_index:
            for rr in right_index[key]:
                merged = {**lr}
                for k, v in rr.items():
                    if k != on:
                        merged[k] = v
                results.append(merged)
    return results

def left_join(left, right, on):
    """Left join: keep all left rows, fill missing right with empty."""
    right_index = {}
    right_cols = set()
    for r in right:
        key = r[on]
        right_cols.update(r.keys())
        if key not in right_index:
            right_index[key] = []
        right_index[key].append(r)
    right_cols.discard(on)

    results = []
    for lr in left:
        key = lr[on]
        if key in right_index:
            for rr in right_index[key]:
                merged = {**lr}
                for k, v in rr.items():
                    if k != on:
                        merged[k] = v
                results.append(merged)
        else:
            merged = {**lr}
            for col in right_cols:
                merged[col] = ''
            results.append(merged)
    return results

# Example
orders = read_csv('orders.csv')
customers = read_csv('customers.csv')
joined = left_join(orders, customers, on='customer_id')
write_csv(joined, 'orders_with_customers.csv')
```

### 去重数据

```python
def deduplicate(rows, key_cols=None):
    """Remove duplicate rows. If key_cols specified, dedupe by those columns only."""
    seen = set()
    unique = []
    for r in rows:
        if key_cols:
            key = tuple(r[c] for c in key_cols)
        else:
            key = tuple(sorted(r.items()))
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return unique

# Deduplicate by email column
clean = deduplicate(data, key_cols=['email'])
```

## 格式转换

### 将 CSV 转换为 JSON

```python
import json, csv

with open('data.csv', newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

# Array of objects
with open('data.json', 'w') as f:
    json.dump(rows, f, indent=2)

# JSON Lines (one object per line, streamable)
with open('data.jsonl', 'w') as f:
    for row in rows:
        f.write(json.dumps(row) + '\n')
```

### 将 JSON 转换为 CSV

```python
import json, csv

with open('data.json') as f:
    rows = json.load(f)

with open('data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
```

### 将 JSON 行格式转换为 CSV

```python
import json, csv

rows = []
with open('data.jsonl') as f:
    for line in f:
        if line.strip():
            rows.append(json.loads(line))

with open('data.csv', 'w', newline='', encoding='utf-8') as f:
    all_keys = set()
    for r in rows:
        all_keys.update(r.keys())
    writer = csv.DictWriter(f, fieldnames=sorted(all_keys))
    writer.writeheader()
    writer.writerows(rows)
```

### 将 TSV 转换为 CSV

```bash
tr '\t' ',' < data.tsv > data.csv
```

## 数据清洗技巧

### 解决常见的 CSV 问题

```python
def clean_csv(rows):
    """Clean common CSV data quality issues."""
    cleaned = []
    for r in rows:
        clean_row = {}
        for k, v in r.items():
            # Strip whitespace from keys and values
            k = k.strip()
            v = v.strip() if isinstance(v, str) else v
            # Normalize empty values
            if v in ('', 'N/A', 'n/a', 'NA', 'null', 'NULL', 'None', '-'):
                v = ''
            # Normalize boolean values
            if v.lower() in ('true', 'yes', '1', 'y'):
                v = 'true'
            elif v.lower() in ('false', 'no', '0', 'n'):
                v = 'false'
            clean_row[k] = v
        cleaned.append(clean_row)
    return cleaned
```

### 验证数据类型

```python
def validate_rows(rows, schema):
    """
    Validate rows against a schema.
    schema: dict of column_name -> 'int'|'float'|'date'|'email'|'str'
    Returns (valid_rows, error_rows)
    """
    import re
    valid, errors = [], []
    for i, r in enumerate(rows):
        errs = []
        for col, dtype in schema.items():
            val = r.get(col, '').strip()
            if not val:
                continue
            if dtype == 'int':
                try:
                    int(val)
                except ValueError:
                    errs.append(f"{col}: '{val}' not int")
            elif dtype == 'float':
                try:
                    float(val)
                except ValueError:
                    errs.append(f"{col}: '{val}' not float")
            elif dtype == 'email':
                if not re.match(r'^[^@]+@[^@]+\.[^@]+$', val):
                    errs.append(f"{col}: '{val}' not email")
            elif dtype == 'date':
                if not re.match(r'^\d{4}-\d{2}-\d{2}', val):
                    errs.append(f"{col}: '{val}' not YYYY-MM-DD")
        if errs:
            errors.append({'row': i + 2, 'errors': errs, 'data': r})
        else:
            valid.append(r)
    return valid, errors

# Usage
valid, bad = validate_rows(data, {'amount': 'float', 'email': 'email', 'date': 'date'})
print(f"Valid: {len(valid)}, Errors: {len(bad)}")
for e in bad[:5]:
    print(f"  Row {e['row']}: {e['errors']}")
```

## 生成报告

### 以 Markdown 格式生成汇总报告

```python
def generate_report(data, title, group_col, value_col):
    """Generate a Markdown summary report."""
    lines = [f"# {title}", f"", f"**Total rows**: {len(data)}", ""]

    # Group summary
    groups = group_by(data, group_col)
    lines.append(f"## By {group_col}")
    lines.append("")
    lines.append(f"| {group_col} | Count | Sum | Avg | Min | Max |")
    lines.append("|---|---|---|---|---|---|")

    for name in sorted(groups):
        vals = [float(r[value_col]) for r in groups[name] if r[value_col].strip()]
        if vals:
            lines.append(f"| {name} | {len(vals)} | {sum(vals):.2f} | {sum(vals)/len(vals):.2f} | {min(vals):.2f} | {max(vals):.2f} |")

    lines.append("")
    lines.append(f"*Generated from {len(data)} rows*")
    return '\n'.join(lines)

report = generate_report(data, "Sales Summary", "category", "revenue")
with open('report.md', 'w') as f:
    f.write(report)
```

## 处理大文件

对于无法一次性加载到内存中的大文件：

```python
def stream_process(input_path, output_path, transform_fn, delimiter=','):
    """Process a CSV row-by-row without loading entire file."""
    with open(input_path, newline='', encoding='utf-8') as fin, \
         open(output_path, 'w', newline='', encoding='utf-8') as fout:
        reader = csv.DictReader(fin, delimiter=delimiter)
        writer = None
        for row in reader:
            result = transform_fn(row)
            if result is None:
                continue  # Skip row
            if writer is None:
                writer = csv.DictWriter(fout, fieldnames=result.keys(), delimiter=delimiter)
                writer.writeheader()
            writer.writerow(result)

# Example: filter and transform in streaming fashion
def process_row(row):
    if float(row.get('amount', 0) or 0) < 10:
        return None  # Skip small amounts
    row['amount_usd'] = str(float(row['amount']) * 1.0)  # Add computed field
    return row

stream_process('big_file.csv', 'output.csv', process_row)
```

## 提示

- 始终检查文件的编码格式：使用 `file -i data.csv` 或使用 `encoding='utf-8-sig'` 打开文件（特别是包含 BOM 字符的文件）
- 对于 Excel 导出的数据（其中数值包含逗号），CSV 模块会自动处理引号问题
- 如果需要处理包含国际字符的数据，可以使用 `json.dumps(ensure_ascii=False)`
- 对于以管道符分隔的文件，在 `csv.reader/writer` 中设置分隔符为 `|`
- 对于需要大量数据汇总的情况，可以考虑使用 Python 自带的 `sqlite3` 数据库：
  ```bash
  sqlite3 :memory: ".mode csv" ".import data.csv t" "SELECT category, SUM(amount) FROM t GROUP BY category;"
  ```