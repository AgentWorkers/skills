---
slug: "dwg-to-excel"
display_name: "DWG To Excel"
description: "使用 DwgExporter CLI 将 AutoCAD DWG 文件（版本 1983–2026）转换为 Excel 数据库。无需 Autodesk 许可证即可提取图层、块、属性和几何数据。"
---

# DWG 到 Excel 的转换

## 商业案例

### 问题描述
AutoCAD 的 DWG 文件包含了以专有格式存储的宝贵项目数据：
- 具有绘图组织结构的图层
- 带有属性数据的块引用
- 文本注释和尺寸标注
- 几何实体（直线、多段线、弧线）
- 外部引用（xref）

提取这些数据通常需要 AutoCAD 许可证或复杂的编程技术。

### 解决方案
DwgExporter.exe 可以在离线环境下将 DWG 文件转换为结构化的 Excel 数据库，且无需 Autodesk 许可证。

### 商业价值
- **零许可成本**：无需 AutoCAD 许可证
- **对旧版本的兼容性**：支持 1983 至 2026 年发布的所有 DWG 文件格式
- **数据提取功能**：可以提取图层、块、属性、文本和几何图形等信息
- **PDF 导出**：可以将 DWG 文件中的内容导出为 PDF 格式的图纸
- **批量处理**：能够同时处理数千个 DWG 文件

## 技术实现

### 命令行接口（CLI）语法
```bash
DwgExporter.exe <input_dwg> [options]
```

### 输出格式
| 输出格式 | 描述 |
|--------|-------------|
| `.xlsx` | 包含所有几何实体的 Excel 数据库 |
| `.pdf` | 从 DWG 文件布局生成的 PDF 图纸 |

### 支持的 DWG 版本
| 版本范围 | 描述 |
|---------------|-------------|
| R12 (1992) | 旧版本的 DWG 文件格式 |
| R14 (1997) | AutoCAD 14 |
| 2000-2002 | DWG 2000 格式 |
| 2004-2006 | DWG 2004 格式 |
| 2007-2009 | DWG 2007 格式 |
| 2010-2012 | DWG 2010 格式 |
| 2013-2017 | DWG 2013 格式 |
| 2018-2026 | DWG 2018 格式 |

### 示例
```bash
# Basic conversion
DwgExporter.exe "C:\Projects\FloorPlan.dwg"

# Export with PDF drawings
DwgExporter.exe "C:\Projects\FloorPlan.dwg" sheets2pdf

# Batch processing all DWG in folder
for /R "C:\Projects" %f in (*.dwg) do DwgExporter.exe "%f"

# PowerShell batch conversion
Get-ChildItem "C:\Projects\*.dwg" -Recurse | ForEach-Object {
    & "C:\DDC\DwgExporter.exe" $_.FullName
}
```

### Python 集成
```python
import subprocess
import pandas as pd
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class DWGEntityType(Enum):
    """DWG entity types."""
    LINE = "LINE"
    POLYLINE = "POLYLINE"
    LWPOLYLINE = "LWPOLYLINE"
    CIRCLE = "CIRCLE"
    ARC = "ARC"
    ELLIPSE = "ELLIPSE"
    SPLINE = "SPLINE"
    TEXT = "TEXT"
    MTEXT = "MTEXT"
    DIMENSION = "DIMENSION"
    INSERT = "INSERT"  # Block reference
    HATCH = "HATCH"
    SOLID = "SOLID"
    POINT = "POINT"
    ATTRIB = "ATTRIB"
    ATTDEF = "ATTDEF"


@dataclass
class DWGEntity:
    """Represents a DWG entity."""
    handle: str
    entity_type: str
    layer: str
    color: int
    linetype: str
    lineweight: float

    # Geometry (depends on entity type)
    start_x: Optional[float] = None
    start_y: Optional[float] = None
    end_x: Optional[float] = None
    end_y: Optional[float] = None

    # Block reference data
    block_name: Optional[str] = None
    rotation: Optional[float] = None
    scale_x: Optional[float] = None
    scale_y: Optional[float] = None

    # Text data
    text_content: Optional[str] = None
    text_height: Optional[float] = None


@dataclass
class DWGBlock:
    """Represents a DWG block definition."""
    name: str
    base_point_x: float
    base_point_y: float
    entity_count: int
    is_dynamic: bool
    attributes: List[str]


@dataclass
class DWGLayer:
    """Represents a DWG layer."""
    name: str
    color: int
    linetype: str
    is_on: bool
    is_frozen: bool
    is_locked: bool
    lineweight: float
    entity_count: int


class DWGExporter:
    """DWG to Excel converter using DDC DwgExporter CLI."""

    def __init__(self, exporter_path: str = "DwgExporter.exe"):
        self.exporter = Path(exporter_path)
        if not self.exporter.exists():
            raise FileNotFoundError(f"DwgExporter not found: {exporter_path}")

    def convert(self, dwg_file: str,
                export_pdf: bool = False) -> Path:
        """Convert DWG file to Excel."""
        dwg_path = Path(dwg_file)
        if not dwg_path.exists():
            raise FileNotFoundError(f"DWG file not found: {dwg_file}")

        cmd = [str(self.exporter), str(dwg_path)]
        if export_pdf:
            cmd.append("sheets2pdf")

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Export failed: {result.stderr}")

        # Output file is same name with .xlsx extension
        return dwg_path.with_suffix('.xlsx')

    def batch_convert(self, folder: str,
                      include_subfolders: bool = True,
                      export_pdf: bool = False) -> List[Dict[str, Any]]:
        """Convert all DWG files in folder."""
        folder_path = Path(folder)
        pattern = "**/*.dwg" if include_subfolders else "*.dwg"

        results = []
        for dwg_file in folder_path.glob(pattern):
            try:
                output = self.convert(str(dwg_file), export_pdf)
                results.append({
                    'input': str(dwg_file),
                    'output': str(output),
                    'status': 'success'
                })
                print(f"✓ Converted: {dwg_file.name}")
            except Exception as e:
                results.append({
                    'input': str(dwg_file),
                    'output': None,
                    'status': 'failed',
                    'error': str(e)
                })
                print(f"✗ Failed: {dwg_file.name} - {e}")

        return results

    def read_entities(self, xlsx_file: str) -> pd.DataFrame:
        """Read converted Excel as DataFrame."""
        xlsx_path = Path(xlsx_file)
        if not xlsx_path.exists():
            raise FileNotFoundError(f"Excel file not found: {xlsx_file}")

        return pd.read_excel(xlsx_file, sheet_name="Elements")

    def get_layers(self, xlsx_file: str) -> pd.DataFrame:
        """Get layer summary from converted file."""
        df = self.read_entities(xlsx_file)

        if 'Layer' not in df.columns:
            raise ValueError("Layer column not found in data")

        summary = df.groupby('Layer').agg({
            'Handle': 'count'
        }).reset_index()
        summary.columns = ['Layer', 'Entity_Count']
        return summary.sort_values('Entity_Count', ascending=False)

    def get_blocks(self, xlsx_file: str) -> pd.DataFrame:
        """Get block reference summary."""
        df = self.read_entities(xlsx_file)

        # Filter to INSERT entities (block references)
        blocks = df[df['EntityType'] == 'INSERT']

        if blocks.empty:
            return pd.DataFrame(columns=['Block_Name', 'Count'])

        summary = blocks.groupby('BlockName').agg({
            'Handle': 'count'
        }).reset_index()
        summary.columns = ['Block_Name', 'Count']
        return summary.sort_values('Count', ascending=False)

    def get_text_content(self, xlsx_file: str) -> pd.DataFrame:
        """Extract all text content from DWG."""
        df = self.read_entities(xlsx_file)

        # Filter to text entities
        text_types = ['TEXT', 'MTEXT', 'ATTRIB']
        texts = df[df['EntityType'].isin(text_types)]

        if 'TextContent' in texts.columns:
            return texts[['Handle', 'EntityType', 'Layer', 'TextContent']].copy()
        return texts[['Handle', 'EntityType', 'Layer']].copy()

    def get_entity_statistics(self, xlsx_file: str) -> Dict[str, int]:
        """Get entity type statistics."""
        df = self.read_entities(xlsx_file)

        if 'EntityType' not in df.columns:
            return {}

        return df['EntityType'].value_counts().to_dict()

    def extract_block_attributes(self, xlsx_file: str,
                                  block_name: str) -> pd.DataFrame:
        """Extract attributes from specific block type."""
        df = self.read_entities(xlsx_file)

        # Find block references
        blocks = df[(df['EntityType'] == 'INSERT') &
                    (df['BlockName'] == block_name)]

        # Find associated attributes
        # Attributes typically follow their parent INSERT in handle order
        result_data = []

        for _, block in blocks.iterrows():
            block_handle = block['Handle']
            block_data = {
                'Block_Handle': block_handle,
                'X': block.get('InsertX', 0),
                'Y': block.get('InsertY', 0),
                'Rotation': block.get('Rotation', 0)
            }

            # Add any attribute columns
            for col in df.columns:
                if col.startswith('Attr_'):
                    block_data[col] = block.get(col)

            result_data.append(block_data)

        return pd.DataFrame(result_data)


class DWGAnalyzer:
    """Advanced DWG analysis tools."""

    def __init__(self, exporter: DWGExporter):
        self.exporter = exporter

    def analyze_drawing_structure(self, dwg_file: str) -> Dict[str, Any]:
        """Analyze complete drawing structure."""
        xlsx = self.exporter.convert(dwg_file)
        df = self.exporter.read_entities(str(xlsx))

        analysis = {
            'file': dwg_file,
            'total_entities': len(df),
            'layers': self.exporter.get_layers(str(xlsx)).to_dict('records'),
            'entity_types': self.exporter.get_entity_statistics(str(xlsx)),
            'blocks': self.exporter.get_blocks(str(xlsx)).to_dict('records')
        }

        # Calculate extents if coordinates available
        if 'X' in df.columns and 'Y' in df.columns:
            analysis['extents'] = {
                'min_x': df['X'].min(),
                'max_x': df['X'].max(),
                'min_y': df['Y'].min(),
                'max_y': df['Y'].max()
            }

        return analysis

    def compare_drawings(self, dwg1: str, dwg2: str) -> Dict[str, Any]:
        """Compare two DWG files."""
        xlsx1 = self.exporter.convert(dwg1)
        xlsx2 = self.exporter.convert(dwg2)

        df1 = self.exporter.read_entities(str(xlsx1))
        df2 = self.exporter.read_entities(str(xlsx2))

        layers1 = set(df1['Layer'].unique()) if 'Layer' in df1.columns else set()
        layers2 = set(df2['Layer'].unique()) if 'Layer' in df2.columns else set()

        return {
            'file1': dwg1,
            'file2': dwg2,
            'entity_count_diff': len(df2) - len(df1),
            'layers_added': list(layers2 - layers1),
            'layers_removed': list(layers1 - layers2),
            'common_layers': list(layers1 & layers2)
        }

    def find_duplicates(self, xlsx_file: str,
                        tolerance: float = 0.001) -> pd.DataFrame:
        """Find duplicate entities at same location."""
        df = self.exporter.read_entities(xlsx_file)

        if 'X' not in df.columns or 'Y' not in df.columns:
            return pd.DataFrame()

        # Round coordinates for grouping
        df['X_rounded'] = (df['X'] / tolerance).round() * tolerance
        df['Y_rounded'] = (df['Y'] / tolerance).round() * tolerance

        # Find duplicates
        duplicates = df[df.duplicated(
            subset=['EntityType', 'Layer', 'X_rounded', 'Y_rounded'],
            keep=False
        )]

        return duplicates.sort_values(['X_rounded', 'Y_rounded'])


# Convenience functions
def convert_dwg_to_excel(dwg_file: str,
                         exporter_path: str = "DwgExporter.exe") -> str:
    """Quick conversion of DWG to Excel."""
    exporter = DWGExporter(exporter_path)
    output = exporter.convert(dwg_file)
    return str(output)


def batch_convert_dwg(folder: str,
                      exporter_path: str = "DwgExporter.exe",
                      include_subfolders: bool = True) -> List[str]:
    """Batch convert all DWG files in folder."""
    exporter = DWGExporter(exporter_path)
    results = exporter.batch_convert(folder, include_subfolders)
    return [r['output'] for r in results if r['status'] == 'success']
```

## 输出数据结构

### Excel 工作表
| 工作表 | 内容 |
|-------|---------|
| 实体信息 | 所有 DWG 实体及其属性 |
| 图层信息 | 图层定义 |
| 块信息 | 块的定义 |
| 绘图布局 | 绘图布局/图纸 |

### 实体属性列
| 列名 | 类型 | 描述 |
|--------|------|-------------|
| Handle | 字符串 | 实体的唯一标识符 |
| EntityType | 字符串 | 实体类型（如直线、圆等） |
| Layer | 字符串 | 所属图层名称 |
| Color | 整数 | 图层颜色索引（0-256） |
| Linetype | 字符串 | 线型名称 |
| Lineweight | 浮点数 | 线宽（单位：毫米） |
| X, Y, Z | 浮点数 | 实体的坐标 |
| BlockName | 字符串 | 对于 INSERT 类型的实体，包含块名称 |
| TextContent | 字符串 | 对于 TEXT/MTEXT 类型的实体，包含文本内容 |

## 快速入门指南
```python
# Initialize exporter
exporter = DWGExporter("C:/DDC/DwgExporter.exe")

# Convert single file
xlsx = exporter.convert("C:/Projects/Plan.dwg")
print(f"Output: {xlsx}")

# Read and analyze
df = exporter.read_entities(str(xlsx))
print(f"Total entities: {len(df)}")

# Get layer statistics
layers = exporter.get_layers(str(xlsx))
print(layers)

# Get block usage
blocks = exporter.get_blocks(str(xlsx))
print(blocks)

# Extract text annotations
texts = exporter.get_text_content(str(xlsx))
for _, row in texts.iterrows():
    print(f"{row['Layer']}: {row.get('TextContent', 'N/A')}")
```

## 常见使用场景
- **图层审核**：检查 DWG 文件中的图层结构
- **块管理**：管理 DWG 文件中的块引用
- **图纸对比**：将 DWG 文件与现有图纸进行对比
- **与 DDC 流程集成**：将转换结果整合到数据管道中

## 最佳实践
1. **检查 DWG 文件版本**：较旧的文件可能包含有限的数据
2. **验证图层结构**：在处理前清理图层信息
3. **处理外部引用**：根据需要绑定外部引用（xref）
4. **批量处理**：对于大型文件，建议分批处理以节省时间
5. **核对实体数量**：如有必要，可以将转换结果与 AutoCAD 中的实体数量进行核对

## 资源
- **GitHub 项目**：[cad2data Pipeline](https://github.com/datadrivenconstruction/cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto)
- **视频教程**：[DWG 到 Excel 的转换流程](https://www.youtube.com/watch?v=jVU7vlMNTO0)
- **相关书籍**：第 2.4 章 – CAD 数据提取技术