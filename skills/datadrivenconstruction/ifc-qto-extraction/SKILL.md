---
name: "ifc-qto-extraction"
description: "从 IFC/Revit 模型中提取用于数量统计的数据。使用 DDC（Design Data Code）转换器来获取元素的数量、面积、体积以及长度，并支持数据的分组和报告功能。"
---

# IFC数量提取功能

从BIM模型（IFC、Revit）中提取结构化数量数据，用于成本估算、材料采购和进度跟踪。

## 商业案例

**问题**：
- 手动数量统计：
  - 耗时较长（中等规模项目需40-80小时）
  - 容易出错（人为计数错误）
  - 不具重复性（任何更改都需要重新统计）
  - 与设计脱节（无法实时更新）

**解决方案**：
- 通过自动化工具从BIM模型中提取数量数据：
  - 几分钟内完成所有数量的提取
  - 按类型、层级、区域进行分类
  - 随模型变化实时更新数据
  - 导出至Excel文件以供定价使用

**投资回报率（ROI）**：
- 数量统计时间减少90%
- 计数错误率接近于零

## 使用的DDC工具

```
┌──────────────────────────────────────────────────────────────────────┐
│                      QTO EXTRACTION PIPELINE                          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│   INPUT                 CONVERT                 ANALYZE               │
│   ┌─────────┐          ┌─────────┐            ┌─────────┐            │
│   │ .rvt    │          │ DDC     │            │ Python  │            │
│   │ .ifc    │─────────►│Converter│───────────►│ pandas  │            │
│   │ .dwg    │          │         │            │         │            │
│   └─────────┘          └─────────┘            └─────────┘            │
│                              │                      │                 │
│                              ▼                      ▼                 │
│                        ┌─────────┐            ┌─────────┐            │
│                        │ .xlsx   │            │ Grouped │            │
│                        │ raw data│            │ QTO     │            │
│                        └─────────┘            └─────────┘            │
│                                                    │                  │
│   OUTPUT                                           ▼                  │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  QTO Report                                                  │   │
│   │  • Element counts by type                                    │   │
│   │  • Areas (m², ft²)                                           │   │
│   │  • Volumes (m³, ft³)                                         │   │
│   │  • Lengths (m, ft)                                           │   │
│   │  • Weights (kg, tons)                                        │   │
│   │  • Grouped by level/zone/system                              │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

## 命令行界面（CLI）命令

### 将Revit数据导出至Excel（包含体积信息）

```bash
# Basic extraction
RvtExporter.exe "C:\Models\Building.rvt"

# Full extraction with bounding boxes (for volume calculations)
RvtExporter.exe "C:\Models\Building.rvt" complete bbox

# Include schedules (Revit's built-in QTO)
RvtExporter.exe "C:\Models\Building.rvt" complete bbox schedule
```

### 将IFC数据导出至Excel

```bash
# Extract IFC data
IfcExporter.exe "C:\Models\Building.ifc"

# Output: Building.xlsx with all IFC entities
```

### 将DWG数据导出至Excel（2D面积信息）

```bash
# Extract DWG blocks and areas
DwgExporter.exe "C:\Drawings\FloorPlan.dwg"
```

## Python实现方式

```python
import pandas as pd
import numpy as np
from pathlib import Path
import subprocess
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class QuantityItem:
    """Single quantity line item"""
    category: str
    type_name: str
    count: int
    area: float = 0.0
    volume: float = 0.0
    length: float = 0.0
    weight: float = 0.0
    unit_area: str = "m²"
    unit_volume: str = "m³"
    unit_length: str = "m"
    level: str = ""
    zone: str = ""


class BIMQuantityExtractor:
    """Extract quantities from BIM models using DDC converters"""

    def __init__(self, converter_path: str):
        self.converter_path = Path(converter_path)

    def convert_model(self, model_path: str, options: List[str] = None) -> Path:
        """Convert BIM model to Excel"""

        model = Path(model_path)
        options = options or ["complete", "bbox"]

        # Determine converter
        ext = model.suffix.lower()
        converters = {
            '.rvt': 'RvtExporter.exe',
            '.rfa': 'RvtExporter.exe',
            '.ifc': 'IfcExporter.exe',
            '.dwg': 'DwgExporter.exe',
            '.dgn': 'DgnExporter.exe'
        }

        converter = self.converter_path / converters.get(ext, 'RvtExporter.exe')

        # Build command
        cmd = [str(converter), str(model)] + options

        # Execute
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Conversion failed: {result.stderr}")

        # Return path to generated Excel
        xlsx_path = model.with_suffix('.xlsx')
        return xlsx_path

    def load_bim_data(self, xlsx_path: str) -> pd.DataFrame:
        """Load converted BIM data from Excel"""

        xlsx = Path(xlsx_path)
        if not xlsx.exists():
            raise FileNotFoundError(f"Excel file not found: {xlsx}")

        # Read main data sheet
        df = pd.read_excel(xlsx, sheet_name=0)

        # Clean column names
        df.columns = df.columns.str.strip()

        return df

    def extract_quantities(
        self,
        df: pd.DataFrame,
        group_by: str = "Type Name",
        include_categories: List[str] = None
    ) -> List[QuantityItem]:
        """Extract quantities grouped by type"""

        # Filter categories if specified
        if include_categories and 'Category' in df.columns:
            df = df[df['Category'].isin(include_categories)]

        # Group and aggregate
        quantities = []

        for (category, type_name), group in df.groupby(['Category', group_by]):
            item = QuantityItem(
                category=str(category),
                type_name=str(type_name),
                count=len(group)
            )

            # Extract area
            area_cols = ['Area', 'Surface Area', 'Gross Area', 'Net Area']
            for col in area_cols:
                if col in group.columns:
                    item.area = group[col].sum()
                    break

            # Extract volume
            vol_cols = ['Volume', 'Gross Volume', 'Net Volume']
            for col in vol_cols:
                if col in group.columns:
                    item.volume = group[col].sum()
                    break

            # Extract length
            len_cols = ['Length', 'Curve Length', 'Unconnected Height']
            for col in len_cols:
                if col in group.columns:
                    item.length = group[col].sum()
                    break

            # Extract level if available
            if 'Level' in group.columns:
                levels = group['Level'].dropna().unique()
                item.level = ', '.join(str(l) for l in levels)

            quantities.append(item)

        return quantities

    def extract_by_level(
        self,
        df: pd.DataFrame,
        group_by: str = "Type Name"
    ) -> Dict[str, List[QuantityItem]]:
        """Extract quantities grouped by level"""

        result = {}

        if 'Level' not in df.columns:
            result['All Levels'] = self.extract_quantities(df, group_by)
            return result

        for level, level_df in df.groupby('Level'):
            level_name = str(level) if pd.notna(level) else 'Unassigned'
            result[level_name] = self.extract_quantities(level_df, group_by)

        return result

    def calculate_concrete_quantities(self, df: pd.DataFrame) -> dict:
        """Calculate concrete quantities for typical elements"""

        concrete_categories = [
            'Floors', 'Structural Floors',
            'Walls', 'Structural Walls',
            'Structural Foundations', 'Foundation',
            'Structural Columns', 'Columns',
            'Structural Framing', 'Beams'
        ]

        concrete_df = df[df['Category'].isin(concrete_categories)]

        return {
            'total_volume_m3': concrete_df['Volume'].sum() if 'Volume' in concrete_df.columns else 0,
            'by_category': concrete_df.groupby('Category')['Volume'].sum().to_dict() if 'Volume' in concrete_df.columns else {},
            'element_count': len(concrete_df)
        }

    def calculate_wall_quantities(self, df: pd.DataFrame) -> dict:
        """Calculate wall quantities"""

        wall_categories = ['Walls', 'Basic Wall', 'Curtain Wall']
        walls = df[df['Category'].isin(wall_categories)]

        result = {
            'total_area_m2': 0,
            'total_length_m': 0,
            'by_type': {}
        }

        if 'Area' in walls.columns:
            result['total_area_m2'] = walls['Area'].sum()

        if 'Length' in walls.columns:
            result['total_length_m'] = walls['Length'].sum()

        if 'Type Name' in walls.columns:
            for type_name, group in walls.groupby('Type Name'):
                result['by_type'][type_name] = {
                    'count': len(group),
                    'area': group['Area'].sum() if 'Area' in group.columns else 0,
                    'length': group['Length'].sum() if 'Length' in group.columns else 0
                }

        return result

    def generate_qto_report(
        self,
        quantities: List[QuantityItem],
        output_path: str,
        project_name: str = "Project"
    ) -> str:
        """Generate QTO Excel report"""

        # Convert to DataFrame
        records = []
        for q in quantities:
            records.append({
                'Category': q.category,
                'Type': q.type_name,
                'Count': q.count,
                'Area (m²)': round(q.area, 2),
                'Volume (m³)': round(q.volume, 3),
                'Length (m)': round(q.length, 2),
                'Level': q.level
            })

        df = pd.DataFrame(records)

        # Sort by category and type
        df = df.sort_values(['Category', 'Type'])

        # Write to Excel with formatting
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary sheet
            summary = df.groupby('Category').agg({
                'Count': 'sum',
                'Area (m²)': 'sum',
                'Volume (m³)': 'sum',
                'Length (m)': 'sum'
            }).round(2)
            summary.to_excel(writer, sheet_name='Summary')

            # Detail sheet
            df.to_excel(writer, sheet_name='Detail', index=False)

            # By Level sheet
            if 'Level' in df.columns and df['Level'].notna().any():
                level_summary = df.groupby(['Level', 'Category']).agg({
                    'Count': 'sum',
                    'Area (m²)': 'sum',
                    'Volume (m³)': 'sum'
                }).round(2)
                level_summary.to_excel(writer, sheet_name='By Level')

        return output_path

    def generate_html_report(
        self,
        quantities: List[QuantityItem],
        output_path: str,
        project_name: str = "Project"
    ) -> str:
        """Generate interactive HTML QTO report"""

        # Group by category
        by_category = {}
        for q in quantities:
            if q.category not in by_category:
                by_category[q.category] = []
            by_category[q.category].append(q)

        # Calculate totals
        total_count = sum(q.count for q in quantities)
        total_area = sum(q.area for q in quantities)
        total_volume = sum(q.volume for q in quantities)

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>QTO Report - {project_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; margin-bottom: 20px; }}
        .summary {{ display: flex; gap: 20px; margin-bottom: 20px; }}
        .summary-card {{ background: #ecf0f1; padding: 15px; border-radius: 5px; flex: 1; }}
        .summary-card h3 {{ margin: 0 0 10px 0; color: #7f8c8d; font-size: 14px; }}
        .summary-card .value {{ font-size: 24px; font-weight: bold; color: #2c3e50; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
        th {{ background: #34495e; color: white; padding: 10px; text-align: left; }}
        td {{ padding: 8px; border-bottom: 1px solid #ddd; }}
        tr:hover {{ background: #f5f5f5; }}
        .category-header {{ background: #3498db; color: white; font-weight: bold; }}
        .number {{ text-align: right; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Quantity Takeoff Report</h1>
        <p>Project: {project_name}</p>
    </div>

    <div class="summary">
        <div class="summary-card">
            <h3>Total Elements</h3>
            <div class="value">{total_count:,}</div>
        </div>
        <div class="summary-card">
            <h3>Total Area</h3>
            <div class="value">{total_area:,.2f} m²</div>
        </div>
        <div class="summary-card">
            <h3>Total Volume</h3>
            <div class="value">{total_volume:,.3f} m³</div>
        </div>
        <div class="summary-card">
            <h3>Categories</h3>
            <div class="value">{len(by_category)}</div>
        </div>
    </div>

    <table>
        <thead>
            <tr>
                <th>Category / Type</th>
                <th class="number">Count</th>
                <th class="number">Area (m²)</th>
                <th class="number">Volume (m³)</th>
                <th class="number">Length (m)</th>
            </tr>
        </thead>
        <tbody>
"""

        for category, items in sorted(by_category.items()):
            cat_count = sum(i.count for i in items)
            cat_area = sum(i.area for i in items)
            cat_volume = sum(i.volume for i in items)

            html += f"""
            <tr class="category-header">
                <td>{category}</td>
                <td class="number">{cat_count:,}</td>
                <td class="number">{cat_area:,.2f}</td>
                <td class="number">{cat_volume:,.3f}</td>
                <td class="number">-</td>
            </tr>
"""
            for item in sorted(items, key=lambda x: x.type_name):
                html += f"""
            <tr>
                <td>&nbsp;&nbsp;&nbsp;{item.type_name}</td>
                <td class="number">{item.count:,}</td>
                <td class="number">{item.area:,.2f}</td>
                <td class="number">{item.volume:,.3f}</td>
                <td class="number">{item.length:,.2f}</td>
            </tr>
"""

        html += """
        </tbody>
    </table>
</body>
</html>
"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        return output_path


# Usage Example
def extract_qto_from_model(
    model_path: str,
    converter_path: str,
    output_dir: str = None
) -> dict:
    """Complete QTO extraction workflow"""

    from datetime import datetime

    extractor = BIMQuantityExtractor(converter_path)

    # Convert model
    print(f"Converting: {model_path}")
    xlsx_path = extractor.convert_model(model_path, ["complete", "bbox"])

    # Load data
    print(f"Loading data from: {xlsx_path}")
    df = extractor.load_bim_data(xlsx_path)

    # Extract quantities
    quantities = extractor.extract_quantities(df)

    # Generate reports
    output_dir = output_dir or Path(model_path).parent
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    excel_path = Path(output_dir) / f"QTO_{timestamp}.xlsx"
    html_path = Path(output_dir) / f"QTO_{timestamp}.html"

    extractor.generate_qto_report(quantities, str(excel_path))
    extractor.generate_html_report(quantities, str(html_path))

    # Calculate specific quantities
    concrete = extractor.calculate_concrete_quantities(df)
    walls = extractor.calculate_wall_quantities(df)

    return {
        'excel_report': str(excel_path),
        'html_report': str(html_path),
        'summary': {
            'total_elements': len(df),
            'categories': df['Category'].nunique() if 'Category' in df.columns else 0,
            'types': df['Type Name'].nunique() if 'Type Name' in df.columns else 0
        },
        'concrete': concrete,
        'walls': walls
    }


if __name__ == "__main__":
    result = extract_qto_from_model(
        model_path=r"C:\Projects\Building.rvt",
        converter_path=r"C:\DDC\Converters",
        output_dir=r"C:\Projects\QTO"
    )

    print(f"Excel: {result['excel_report']}")
    print(f"HTML: {result['html_report']}")
    print(f"Concrete Volume: {result['concrete']['total_volume_m3']:.2f} m³")
```

## 与n8n工作流的集成

```yaml
name: BIM QTO Extraction
trigger:
  type: webhook
  path: /qto-extract

steps:
  - convert_model:
      node: Execute Command
      command: |
        "C:\DDC\RvtExporter.exe" "{{$json.model_path}}" complete bbox schedule

  - load_excel:
      node: Spreadsheet File
      operation: read
      file: "={{$json.model_path.replace('.rvt', '.xlsx')}}"

  - group_quantities:
      node: Code
      code: |
        const grouped = {};
        items.forEach(item => {
          const type = item.json['Type Name'];
          if (!grouped[type]) {
            grouped[type] = {
              count: 0,
              area: 0,
              volume: 0
            };
          }
          grouped[type].count++;
          grouped[type].area += parseFloat(item.json['Area'] || 0);
          grouped[type].volume += parseFloat(item.json['Volume'] || 0);
        });
        return Object.entries(grouped).map(([type, data]) => ({
          type,
          ...data
        }));

  - generate_report:
      node: Code
      code: |
        // Generate HTML report
        return generateHTMLReport(items);

  - save_report:
      node: Write Binary File
      path: "={{$json.output_path}}"
```

## 最佳实践

1. **模型质量**：确保BIM模型中已正确分配层级和类型。
2. **单位**：验证模型单位与预期输出单位一致。
3. **分类**：使用统一的分类名称进行数据分组。
4. **更新**：在设计更改后重新执行数量统计。
5. **验证**：将统计结果与手动检查结果进行交叉核对。

## 常用数量计算公式

```python
# Concrete formwork area (approximate)
formwork_area = concrete_volume * 6  # m² per m³ of concrete

# Rebar quantity (approximate)
rebar_weight = concrete_volume * 100  # kg per m³ (typical)

# Paint area from wall area
paint_area = wall_area * 2  # both sides

# Ceiling area from floor area
ceiling_area = floor_area * 0.95  # typical ratio
```

---

“量两次，剪一次；更好的做法是直接从模型中自动获取数据。”