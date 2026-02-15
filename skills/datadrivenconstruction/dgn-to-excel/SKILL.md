---
name: "dgn-to-excel"
description: "将 DGN 文件（版本 7-8）转换为 Excel 数据库。从基础设施 CAD 文件中提取元素、层级和属性信息。"
---

# DGN文件转换为Excel文件

## 商业案例

### 问题描述
DGN文件在基础设施和土木工程领域非常常见，应用于以下场景：
- 交通和公路设计
- 桥梁和隧道项目
- 公用设施网络
- 铁路基础设施

从DGN文件中提取结构化数据以用于分析和报告可能会遇到挑战。

### 解决方案
将DGN文件转换为结构化的Excel数据库，支持v7和v8两种格式。

### 商业价值
- **基础设施支持**：专注于土木工程领域
- **旧格式支持**：支持v7和v8版本的DGN文件
- **数据提取**：可以提取层次信息、单元格内容、文本以及几何图形数据
- **批量处理**：能够处理多个文件
- **结构化输出**：输出格式为Excel，便于进一步分析

## 技术实现

### 命令行接口（CLI）语法
```bash
DgnExporter.exe <input_dgn>
```

### 支持的版本
| 版本 | 描述 |
|---------|-------------|
| V7 DGN | MicroStation的旧版本格式（v8之前的格式） |
| V8 DGN | MicroStation的现代格式 |
| V8i DGN | MicroStation v8i格式 |

### 输出格式
| 输出文件类型 | 描述 |
|--------|-------------|
| `.xlsx` | 包含所有元素的Excel数据库 |

### 示例
```bash
# Basic conversion
DgnExporter.exe "C:\Projects\Bridge.dgn"

# Batch processing
for /R "C:\Infrastructure" %f in (*.dgn) do DgnExporter.exe "%f"

# PowerShell batch
Get-ChildItem "C:\Projects\*.dgn" -Recurse | ForEach-Object {
    & "C:\DDC\DgnExporter.exe" $_.FullName
}
```

### Python集成示例
```python
import subprocess
import pandas as pd
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class DGNElementType(Enum):
    """DGN element types."""
    CELL_HEADER = 2
    LINE = 3
    LINE_STRING = 4
    SHAPE = 6
    TEXT_NODE = 7
    CURVE = 11
    COMPLEX_CHAIN = 12
    COMPLEX_SHAPE = 14
    ELLIPSE = 15
    ARC = 16
    TEXT = 17
    SURFACE = 18
    SOLID = 19
    BSPLINE_CURVE = 21
    POINT_STRING = 22
    DIMENSION = 33
    SHARED_CELL = 35


@dataclass
class DGNElement:
    """Represents a DGN element."""
    element_id: int
    element_type: int
    type_name: str
    level: int
    color: int
    weight: int
    style: int

    # Geometry
    range_low_x: Optional[float] = None
    range_low_y: Optional[float] = None
    range_low_z: Optional[float] = None
    range_high_x: Optional[float] = None
    range_high_y: Optional[float] = None
    range_high_z: Optional[float] = None

    # Cell/Text specific
    cell_name: Optional[str] = None
    text_content: Optional[str] = None


@dataclass
class DGNLevel:
    """Represents a DGN level."""
    number: int
    name: str
    is_displayed: bool
    is_frozen: bool
    element_count: int


class DGNExporter:
    """DGN to Excel converter using DDC DgnExporter CLI."""

    def __init__(self, exporter_path: str = "DgnExporter.exe"):
        self.exporter = Path(exporter_path)
        if not self.exporter.exists():
            raise FileNotFoundError(f"DgnExporter not found: {exporter_path}")

    def convert(self, dgn_file: str) -> Path:
        """Convert DGN file to Excel."""
        dgn_path = Path(dgn_file)
        if not dgn_path.exists():
            raise FileNotFoundError(f"DGN file not found: {dgn_file}")

        cmd = [str(self.exporter), str(dgn_path)]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Export failed: {result.stderr}")

        return dgn_path.with_suffix('.xlsx')

    def batch_convert(self, folder: str,
                      include_subfolders: bool = True) -> List[Dict[str, Any]]:
        """Convert all DGN files in folder."""
        folder_path = Path(folder)
        pattern = "**/*.dgn" if include_subfolders else "*.dgn"

        results = []
        for dgn_file in folder_path.glob(pattern):
            try:
                output = self.convert(str(dgn_file))
                results.append({
                    'input': str(dgn_file),
                    'output': str(output),
                    'status': 'success'
                })
                print(f"✓ Converted: {dgn_file.name}")
            except Exception as e:
                results.append({
                    'input': str(dgn_file),
                    'output': None,
                    'status': 'failed',
                    'error': str(e)
                })
                print(f"✗ Failed: {dgn_file.name} - {e}")

        return results

    def read_elements(self, xlsx_file: str) -> pd.DataFrame:
        """Read converted Excel as DataFrame."""
        return pd.read_excel(xlsx_file, sheet_name="Elements")

    def get_levels(self, xlsx_file: str) -> pd.DataFrame:
        """Get level summary."""
        df = self.read_elements(xlsx_file)

        if 'Level' not in df.columns:
            raise ValueError("Level column not found")

        summary = df.groupby('Level').agg({
            'ElementId': 'count'
        }).reset_index()
        summary.columns = ['Level', 'Element_Count']
        return summary.sort_values('Level')

    def get_element_types(self, xlsx_file: str) -> pd.DataFrame:
        """Get element type statistics."""
        df = self.read_elements(xlsx_file)

        type_col = 'ElementType' if 'ElementType' in df.columns else 'Type'
        if type_col not in df.columns:
            return pd.DataFrame()

        summary = df.groupby(type_col).agg({
            'ElementId': 'count'
        }).reset_index()
        summary.columns = ['Element_Type', 'Count']
        return summary.sort_values('Count', ascending=False)

    def get_cells(self, xlsx_file: str) -> pd.DataFrame:
        """Get cell references (similar to blocks in DWG)."""
        df = self.read_elements(xlsx_file)

        # Filter to cell elements
        cells = df[df['ElementType'].isin([2, 35])]  # CELL_HEADER, SHARED_CELL

        if cells.empty or 'CellName' not in cells.columns:
            return pd.DataFrame(columns=['Cell_Name', 'Count'])

        summary = cells.groupby('CellName').agg({
            'ElementId': 'count'
        }).reset_index()
        summary.columns = ['Cell_Name', 'Count']
        return summary.sort_values('Count', ascending=False)

    def get_text_content(self, xlsx_file: str) -> pd.DataFrame:
        """Extract all text from DGN."""
        df = self.read_elements(xlsx_file)

        # Filter to text elements
        text_types = [7, 17]  # TEXT_NODE, TEXT
        texts = df[df['ElementType'].isin(text_types)]

        if 'TextContent' in texts.columns:
            return texts[['ElementId', 'Level', 'TextContent']].copy()
        return texts[['ElementId', 'Level']].copy()

    def get_statistics(self, xlsx_file: str) -> Dict[str, Any]:
        """Get comprehensive DGN statistics."""
        df = self.read_elements(xlsx_file)

        stats = {
            'total_elements': len(df),
            'levels_used': df['Level'].nunique() if 'Level' in df.columns else 0,
            'element_types': df['ElementType'].nunique() if 'ElementType' in df.columns else 0
        }

        # Calculate extents
        for coord in ['X', 'Y', 'Z']:
            low_col = f'RangeLow{coord}'
            high_col = f'RangeHigh{coord}'
            if low_col in df.columns and high_col in df.columns:
                stats[f'min_{coord.lower()}'] = df[low_col].min()
                stats[f'max_{coord.lower()}'] = df[high_col].max()

        return stats


class DGNAnalyzer:
    """Advanced DGN analysis for infrastructure projects."""

    def __init__(self, exporter: DGNExporter):
        self.exporter = exporter

    def analyze_infrastructure(self, dgn_file: str) -> Dict[str, Any]:
        """Analyze DGN for infrastructure elements."""
        xlsx = self.exporter.convert(dgn_file)
        df = self.exporter.read_elements(str(xlsx))

        analysis = {
            'file': dgn_file,
            'statistics': self.exporter.get_statistics(str(xlsx)),
            'levels': self.exporter.get_levels(str(xlsx)).to_dict('records'),
            'element_types': self.exporter.get_element_types(str(xlsx)).to_dict('records'),
            'cells': self.exporter.get_cells(str(xlsx)).to_dict('records')
        }

        # Identify infrastructure-specific elements
        if 'ElementType' in df.columns:
            # Lines and shapes (often roads, boundaries)
            lines = df[df['ElementType'].isin([3, 4, 6, 14])].shape[0]
            analysis['linear_elements'] = lines

            # Complex elements (often structures)
            complex_elements = df[df['ElementType'].isin([12, 14, 18, 19])].shape[0]
            analysis['complex_elements'] = complex_elements

            # Annotation elements
            annotations = df[df['ElementType'].isin([7, 17, 33])].shape[0]
            analysis['annotations'] = annotations

        return analysis

    def compare_revisions(self, dgn1: str, dgn2: str) -> Dict[str, Any]:
        """Compare two DGN revisions."""
        xlsx1 = self.exporter.convert(dgn1)
        xlsx2 = self.exporter.convert(dgn2)

        df1 = self.exporter.read_elements(str(xlsx1))
        df2 = self.exporter.read_elements(str(xlsx2))

        levels1 = set(df1['Level'].unique()) if 'Level' in df1.columns else set()
        levels2 = set(df2['Level'].unique()) if 'Level' in df2.columns else set()

        return {
            'revision1': dgn1,
            'revision2': dgn2,
            'element_count_diff': len(df2) - len(df1),
            'levels_added': list(levels2 - levels1),
            'levels_removed': list(levels1 - levels2),
            'common_levels': len(levels1 & levels2)
        }

    def extract_coordinates(self, xlsx_file: str) -> pd.DataFrame:
        """Extract element coordinates for GIS integration."""
        df = self.exporter.read_elements(xlsx_file)

        coord_cols = ['ElementId', 'Level', 'ElementType']
        for col in ['RangeLowX', 'RangeLowY', 'RangeLowZ',
                    'RangeHighX', 'RangeHighY', 'RangeHighZ',
                    'CenterX', 'CenterY', 'CenterZ']:
            if col in df.columns:
                coord_cols.append(col)

        return df[coord_cols].copy()


class DGNLevelManager:
    """Manage DGN level structures."""

    def __init__(self, exporter: DGNExporter):
        self.exporter = exporter

    def get_level_map(self, xlsx_file: str) -> Dict[int, str]:
        """Create level number to name mapping."""
        df = self.exporter.read_elements(xlsx_file)

        if 'Level' not in df.columns:
            return {}

        # MicroStation levels are typically numbered 1-63 (V7) or unlimited (V8)
        level_map = {}
        for level in df['Level'].unique():
            level_map[int(level)] = f"Level_{level}"

        return level_map

    def filter_by_levels(self, xlsx_file: str,
                         levels: List[int]) -> pd.DataFrame:
        """Filter elements by level numbers."""
        df = self.exporter.read_elements(xlsx_file)
        return df[df['Level'].isin(levels)]

    def get_level_usage_report(self, xlsx_file: str) -> pd.DataFrame:
        """Generate level usage report."""
        df = self.exporter.read_elements(xlsx_file)

        if 'Level' not in df.columns or 'ElementType' not in df.columns:
            return pd.DataFrame()

        # Cross-tabulate levels and element types
        report = pd.crosstab(df['Level'], df['ElementType'], margins=True)
        return report


# Convenience functions
def convert_dgn_to_excel(dgn_file: str,
                         exporter_path: str = "DgnExporter.exe") -> str:
    """Quick conversion of DGN to Excel."""
    exporter = DGNExporter(exporter_path)
    output = exporter.convert(dgn_file)
    return str(output)


def analyze_dgn(dgn_file: str,
                exporter_path: str = "DgnExporter.exe") -> Dict[str, Any]:
    """Analyze DGN file and return summary."""
    exporter = DGNExporter(exporter_path)
    analyzer = DGNAnalyzer(exporter)
    return analyzer.analyze_infrastructure(dgn_file)
```

## 输出结构

### Excel表格内容
| 表格名称 | 内容 |
|-------|---------|
| 元素信息 | 所有DGN元素的详细信息 |
| 层次信息 | 各层次的定义 |
| 单元格信息 | 单元格的相关数据 |

### 元素列信息
| 列名称 | 类型 | 描述 |
|--------|------|-------------|
| ElementId | int | 元素的唯一标识符 |
| ElementType | int | 元素类型代码（例如：3=线条，17=文本等） |
| Level | int | 元素所在的层次编号 |
| Color | int | 元素的颜色索引 |
| Weight | int | 线条的粗细 |
| Style | int | 线条的样式 |
| RangeLowX/Y/Z | float | 元素的边界框最小值 |
| RangeHighX/Y/Z | float | 元素的边界框最大值 |
| CellName | string | 文本元素的名称 |
| TextContent | string | 文本元素的内容 |

## 快速入门指南
```python
# Initialize exporter
exporter = DGNExporter("C:/DDC/DgnExporter.exe")

# Convert DGN to Excel
xlsx = exporter.convert("C:/Projects/Highway.dgn")
print(f"Output: {xlsx}")

# Read elements
df = exporter.read_elements(str(xlsx))
print(f"Total elements: {len(df)}")

# Get level statistics
levels = exporter.get_levels(str(xlsx))
print(levels)

# Get element types
types = exporter.get_element_types(str(xlsx))
print(types)
```

## 常见使用场景
- **基础设施分析**  
- **层次信息审核**  
- **GIS数据集成**  
- **版本对比**  

## 与DDC管道的集成
```python
# Infrastructure pipeline: DGN → Excel → Analysis
from dgn_exporter import DGNExporter, DGNAnalyzer

# 1. Convert DGN
exporter = DGNExporter("C:/DDC/DgnExporter.exe")
xlsx = exporter.convert("highway_project.dgn")

# 2. Analyze structure
stats = exporter.get_statistics(str(xlsx))
print(f"Elements: {stats['total_elements']}")
print(f"Levels: {stats['levels_used']}")

# 3. Extract for GIS
analyzer = DGNAnalyzer(exporter)
coords = analyzer.extract_coordinates(str(xlsx))
coords.to_csv("for_gis.csv", index=False)
```

## 最佳实践
1. **检查文件版本**：v7和v8版本具有不同的功能，请确保正确处理。
2. **单独处理参考文件**：对所有参考文件进行单独处理。
3. **明确层次标准**：为组织内部制定统一的层次标准。
4. **验证坐标系统**：确保坐标系统和单位的一致性。
5. **选择性导出单元格数据**：根据需要选择性地导出单元格信息。

## 资源推荐
- **GitHub仓库**：[cad2data Pipeline](https://github.com/datadrivenconstruction/cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto)
- **DDC手册**：第2.4章——CAD数据提取
- **MicroStation**：一款专注于基础设施设计的CAD软件