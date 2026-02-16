---
name: "csv-handler"
description: "处理来自建筑软件导出的 CSV 文件。自动检测分隔符、编码，并清理格式混乱的数据。"
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🏷️", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---# 用于建筑数据的 CSV 处理工具

## 概述
CSV 是建筑行业通用的数据交换格式，广泛应用于调度数据导出和成本数据库的创建。本工具负责处理编码问题、分隔符检测以及数据清洗等工作。

## Python 实现
```python
import pandas as pd
import csv
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
import chardet


@dataclass
class CSVProfile:
    """Profile of CSV file."""
    encoding: str
    delimiter: str
    has_header: bool
    row_count: int
    column_count: int
    columns: List[str]


class ConstructionCSVHandler:
    """Handle CSV files from construction software."""

    COMMON_DELIMITERS = [',', ';', '\t', '|']
    COMMON_ENCODINGS = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']

    def __init__(self):
        self.last_profile: Optional[CSVProfile] = None

    def detect_encoding(self, file_path: str) -> str:
        """Detect file encoding."""
        with open(file_path, 'rb') as f:
            raw = f.read(10000)
        result = chardet.detect(raw)
        return result.get('encoding', 'utf-8') or 'utf-8'

    def detect_delimiter(self, file_path: str, encoding: str) -> str:
        """Detect CSV delimiter."""
        with open(file_path, 'r', encoding=encoding, errors='replace') as f:
            sample = f.read(5000)

        # Count occurrences
        counts = {d: sample.count(d) for d in self.COMMON_DELIMITERS}

        # Return most common that appears consistently
        if counts:
            return max(counts, key=counts.get)
        return ','

    def profile_csv(self, file_path: str) -> CSVProfile:
        """Profile CSV file."""
        encoding = self.detect_encoding(file_path)
        delimiter = self.detect_delimiter(file_path, encoding)

        # Read sample
        df = pd.read_csv(file_path, encoding=encoding, delimiter=delimiter,
                         nrows=10, on_bad_lines='skip')

        has_header = not df.columns[0].replace('.', '').replace('-', '').isdigit()

        # Full row count
        with open(file_path, 'r', encoding=encoding, errors='replace') as f:
            row_count = sum(1 for _ in f) - (1 if has_header else 0)

        profile = CSVProfile(
            encoding=encoding,
            delimiter=delimiter,
            has_header=has_header,
            row_count=row_count,
            column_count=len(df.columns),
            columns=list(df.columns)
        )
        self.last_profile = profile
        return profile

    def read_csv(self, file_path: str,
                 encoding: Optional[str] = None,
                 delimiter: Optional[str] = None,
                 clean: bool = True) -> pd.DataFrame:
        """Read CSV with auto-detection."""

        # Auto-detect if not provided
        if encoding is None:
            encoding = self.detect_encoding(file_path)
        if delimiter is None:
            delimiter = self.detect_delimiter(file_path, encoding)

        # Read with error handling
        df = pd.read_csv(
            file_path,
            encoding=encoding,
            delimiter=delimiter,
            on_bad_lines='skip',
            low_memory=False
        )

        if clean:
            df = self.clean_dataframe(df)

        return df

    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean construction CSV data."""
        # Clean column names
        df.columns = [self._clean_column_name(c) for c in df.columns]

        # Remove empty rows and columns
        df = df.dropna(how='all')
        df = df.dropna(axis=1, how='all')

        # Strip whitespace from strings
        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].str.strip() if df[col].dtype == 'object' else df[col]

        return df

    def _clean_column_name(self, name: str) -> str:
        """Clean column name."""
        if not isinstance(name, str):
            return str(name)

        # Remove special characters, replace spaces
        clean = name.strip().lower()
        clean = clean.replace(' ', '_').replace('-', '_')
        clean = ''.join(c for c in clean if c.isalnum() or c == '_')
        return clean

    def merge_csvs(self, file_paths: List[str],
                   on_column: Optional[str] = None) -> pd.DataFrame:
        """Merge multiple CSV files."""
        dfs = []
        for path in file_paths:
            df = self.read_csv(path)
            df['_source_file'] = Path(path).name
            dfs.append(df)

        if not dfs:
            return pd.DataFrame()

        if on_column and on_column in dfs[0].columns:
            result = dfs[0]
            for df in dfs[1:]:
                result = pd.merge(result, df, on=on_column, how='outer')
            return result

        return pd.concat(dfs, ignore_index=True)

    def split_csv(self, df: pd.DataFrame,
                  group_column: str,
                  output_dir: str) -> List[str]:
        """Split CSV by column values."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        files = []
        for value in df[group_column].unique():
            subset = df[df[group_column] == value]
            filename = f"{group_column}_{value}.csv"
            filepath = output_path / filename
            subset.to_csv(filepath, index=False)
            files.append(str(filepath))

        return files

    def convert_types(self, df: pd.DataFrame,
                      type_map: Dict[str, str] = None) -> pd.DataFrame:
        """Convert column types intelligently."""
        df = df.copy()

        if type_map:
            for col, dtype in type_map.items():
                if col in df.columns:
                    try:
                        df[col] = df[col].astype(dtype)
                    except:
                        pass
        else:
            # Auto-convert
            for col in df.columns:
                # Try numeric
                try:
                    df[col] = pd.to_numeric(df[col])
                    continue
                except:
                    pass

                # Try datetime
                try:
                    df[col] = pd.to_datetime(df[col])
                except:
                    pass

        return df

    def export_csv(self, df: pd.DataFrame,
                   file_path: str,
                   encoding: str = 'utf-8-sig',
                   delimiter: str = ',') -> str:
        """Export DataFrame to CSV."""
        df.to_csv(file_path, encoding=encoding, sep=delimiter, index=False)
        return file_path


# Specialized handlers
class ScheduleCSVHandler(ConstructionCSVHandler):
    """Handler for project schedule CSVs."""

    SCHEDULE_COLUMNS = ['task_id', 'task_name', 'start_date', 'end_date',
                        'duration', 'predecessors', 'resources']

    def parse_schedule(self, file_path: str) -> pd.DataFrame:
        """Parse schedule CSV."""
        df = self.read_csv(file_path)

        # Convert date columns
        for col in df.columns:
            if 'date' in col.lower() or 'start' in col.lower() or 'end' in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col])
                except:
                    pass

        return df


class CostCSVHandler(ConstructionCSVHandler):
    """Handler for cost/estimate CSVs."""

    def parse_costs(self, file_path: str) -> pd.DataFrame:
        """Parse cost CSV."""
        df = self.read_csv(file_path)

        # Find and convert numeric columns
        for col in df.columns:
            if any(word in col.lower() for word in ['cost', 'price', 'amount', 'total', 'qty', 'quantity']):
                df[col] = pd.to_numeric(df[col].replace(r'[\$,]', '', regex=True), errors='coerce')

        return df
```

## 快速入门
```python
handler = ConstructionCSVHandler()

# Profile CSV first
profile = handler.profile_csv("export.csv")
print(f"Encoding: {profile.encoding}, Delimiter: '{profile.delimiter}'")

# Read with auto-detection
df = handler.read_csv("export.csv")
print(f"Loaded {len(df)} rows, {len(df.columns)} columns")
```

## 常见使用场景

### 1. 合并多个导出的数据文件
```python
files = ["jan_export.csv", "feb_export.csv", "mar_export.csv"]
merged = handler.merge_csvs(files)
```

### 2. 按类别对数据进行分类
```python
handler.split_csv(df, group_column='category', output_dir='./split_files')
```

### 3. 导入调度数据
```python
schedule_handler = ScheduleCSVHandler()
schedule = schedule_handler.parse_schedule("p6_export.csv")
```

## 参考资源
- **DDC 手册**：第 2.1 章 - 结构化数据