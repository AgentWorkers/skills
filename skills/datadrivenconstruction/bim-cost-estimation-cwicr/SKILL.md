---
name: "bim-cost-estimation-cwicr"
description: "使用 DDC CWICR 数据库，从 BIM 模型中自动进行成本估算；该数据库包含 55,719 个工作项。通过 AI 分类和向量搜索技术来实现精确的定价。"
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw":{"emoji":"🏗️","os":["darwin","linux","win32"],"homepage":"https://datadrivenconstruction.io","requires":{"bins":["python3"],"env":["OPENAI_API_KEY","QDRANT_URL"]},"primaryEnv":"OPENAI_API_KEY"}}
---

# 使用 DDC CWICR 进行 BIM 成本估算

通过 AI 分类和 DDC CWICR 建筑成本数据库，从 BIM 模型中生成准确的成本估算。

## 商业案例

**问题**：
- 传统成本估算方法：
  - 手动操作，耗时较长（详细估算可能需要数周时间）
  - 主观性强，不同估算人员之间的结果存在差异
  - 需要专业技能
  - 难以根据设计变更进行更新

**解决方案**：
- 自动化的 BIM 到成本转换流程：
  - 直接从模型中提取工程量数据
  - 使用 AI 将元素分类为具体的工作项
  - 通过向量搜索在 DDC CWICR 中查找相应的价格
  - 完成估算仅需几小时，而非数周时间

**投资回报率 (ROI)**：
- 估算时间缩短 80%，方法更加统一和一致

## 系统架构

```
┌──────────────────────────────────────────────────────────────────────────┐
│                  BIM TO COST ESTIMATION PIPELINE                          │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│   ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────────────┐   │
│   │ BIM     │     │ DDC     │     │ AI      │     │ DDC CWICR       │   │
│   │ Model   │────►│Converter│────►│ LLM     │────►│ Vector Search   │   │
│   │.rvt/.ifc│     │         │     │         │     │ (Qdrant)        │   │
│   └─────────┘     └─────────┘     └─────────┘     └─────────────────┘   │
│                        │              │                    │             │
│                        ▼              ▼                    ▼             │
│                   ┌─────────┐    ┌─────────┐         ┌──────────┐       │
│                   │ .xlsx   │    │ Work    │         │ Matched  │       │
│                   │ QTO     │    │ Items   │         │ Rates    │       │
│                   └─────────┘    └─────────┘         └──────────┘       │
│                        │              │                    │             │
│                        └──────────────┼────────────────────┘             │
│                                       ▼                                  │
│                              ┌─────────────────┐                        │
│                              │ COST ESTIMATE   │                        │
│                              │                 │                        │
│                              │ • By element    │                        │
│                              │ • By trade      │                        │
│                              │ • By phase      │                        │
│                              │ • Resources     │                        │
│                              └─────────────────┘                        │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

## DDC CWICR 数据库

```yaml
Database Overview:
  work_items: 55,719
  resources: 27,672
  languages: 9 (AR, DE, EN, ES, FR, HI, PT, RU, ZH)
  fields_per_item: 85
  embedding_model: text-embedding-3-large (3072d)
  vector_db: Qdrant

Collections:
  - ddc_cwicr_ar  # Arabic (Dubai prices)
  - ddc_cwicr_de  # German (Berlin prices)
  - ddc_cwicr_en  # English (Toronto prices)
  - ddc_cwicr_es  # Spanish (Barcelona prices)
  - ddc_cwicr_fr  # French (Paris prices)
  - ddc_cwicr_hi  # Hindi (Mumbai prices)
  - ddc_cwicr_pt  # Portuguese (São Paulo prices)
  - ddc_cwicr_ru  # Russian (St. Petersburg prices)
  - ddc_cwicr_zh  # Chinese (Shanghai prices)
```

## 流程阶段

| 阶段 | 名称 | 描述 |
|-------|------|-------------|
| 0 | 收集 BIM 数据 | 从 Revit/IFC 文件中提取元素信息 |
| 1 | 项目识别 | AI 确定项目类型 |
| 2 | 阶段划分 | AI 创建施工阶段 |
| 3 | 元素分配 | AI 将元素类型映射到相应的施工阶段 |
| 4 | 工作项分解 | AI 将元素类型细分为具体的工作项 |
| 5 | 向量搜索 | 在 DDC CWICR 中查找匹配的价格 |
| 6 | 单位转换 | 将 BIM 单位转换为成本计算所需的单位 |
| 7 | 成本计算 | 工程量 × 单价 |
| 7.5 | 验证 | 由技术总监 (CTO) 审查估算的完整性 |
| 8 | 数据汇总 | 按阶段和类别汇总成本 |
| 9 | 报告生成 | 生成 HTML 和 Excel 格式的报告 |

## Python 实现

```python
import pandas as pd
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from openai import OpenAI
from typing import List, Dict, Optional
from dataclasses import dataclass
import json

@dataclass
class WorkItem:
    """Matched work item from CWICR"""
    cwicr_code: str
    description: str
    unit: str
    unit_price: float
    labor_cost: float
    material_cost: float
    equipment_cost: float
    productivity: float  # units per hour
    currency: str
    confidence: float

@dataclass
class CostLineItem:
    """Single line item in estimate"""
    bim_type: str
    work_item: WorkItem
    quantity: float
    quantity_unit: str
    total_cost: float
    labor_cost: float
    material_cost: float
    equipment_cost: float
    phase: str
    trade: str


class BIMCostEstimator:
    """BIM to cost estimation using DDC CWICR"""

    def __init__(
        self,
        qdrant_url: str,
        qdrant_api_key: str = None,
        openai_api_key: str = None,
        language: str = "EN"
    ):
        self.qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        self.openai = OpenAI(api_key=openai_api_key)
        self.language = language
        self.collection = f"ddc_cwicr_{language.lower()}"

    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text"""
        response = self.openai.embeddings.create(
            model="text-embedding-3-large",
            input=text,
            dimensions=3072
        )
        return response.data[0].embedding

    def search_cwicr(
        self,
        query: str,
        limit: int = 5,
        category_filter: str = None
    ) -> List[WorkItem]:
        """Search CWICR database for matching work items"""

        # Get embedding
        query_vector = self.get_embedding(query)

        # Build filter if category specified
        query_filter = None
        if category_filter:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="category",
                        match=MatchValue(value=category_filter)
                    )
                ]
            )

        # Search
        results = self.qdrant.search(
            collection_name=self.collection,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=limit
        )

        # Parse results
        work_items = []
        for r in results:
            payload = r.payload
            work_items.append(WorkItem(
                cwicr_code=payload.get('code', ''),
                description=payload.get('description', ''),
                unit=payload.get('unit', ''),
                unit_price=float(payload.get('unit_price', 0)),
                labor_cost=float(payload.get('labor_cost', 0)),
                material_cost=float(payload.get('material_cost', 0)),
                equipment_cost=float(payload.get('equipment_cost', 0)),
                productivity=float(payload.get('productivity', 1)),
                currency=payload.get('currency', 'USD'),
                confidence=r.score
            ))

        return work_items

    def decompose_bim_type(
        self,
        bim_type: str,
        category: str
    ) -> List[str]:
        """Use LLM to decompose BIM type into work items"""

        prompt = f"""
Decompose this BIM element type into construction work items:

BIM Type: {bim_type}
Category: {category}

List the individual work activities needed to construct this element.
For example, "Brick Wall 240mm" decomposes into:
- Masonry: Brick laying
- Mortar: Cement mortar for joints
- Plaster: Internal plaster finish
- Paint: Wall painting

Return a JSON array of work item descriptions.
Example: ["Brick masonry laying", "Cement mortar for brick joints", "Internal cement plaster 15mm"]
"""

        response = self.openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        try:
            result = json.loads(response.choices[0].message.content)
            return result.get('work_items', [bim_type])
        except:
            return [bim_type]

    def estimate_element(
        self,
        bim_type: str,
        category: str,
        quantity: float,
        quantity_unit: str,
        phase: str = "Construction"
    ) -> List[CostLineItem]:
        """Estimate cost for single BIM element type"""

        # Decompose into work items
        work_descriptions = self.decompose_bim_type(bim_type, category)

        line_items = []

        for work_desc in work_descriptions:
            # Search CWICR for matching rate
            matches = self.search_cwicr(work_desc, limit=1)

            if not matches:
                continue

            best_match = matches[0]

            # Convert quantity if units don't match
            adjusted_qty = self._convert_units(
                quantity, quantity_unit, best_match.unit
            )

            # Calculate costs
            total = adjusted_qty * best_match.unit_price
            labor = adjusted_qty * best_match.labor_cost
            material = adjusted_qty * best_match.material_cost
            equipment = adjusted_qty * best_match.equipment_cost

            line_items.append(CostLineItem(
                bim_type=bim_type,
                work_item=best_match,
                quantity=adjusted_qty,
                quantity_unit=best_match.unit,
                total_cost=total,
                labor_cost=labor,
                material_cost=material,
                equipment_cost=equipment,
                phase=phase,
                trade=self._get_trade(category)
            ))

        return line_items

    def estimate_from_qto(
        self,
        qto_data: pd.DataFrame,
        type_column: str = "Type Name",
        category_column: str = "Category",
        quantity_column: str = "Volume"
    ) -> List[CostLineItem]:
        """Generate estimate from QTO DataFrame"""

        all_line_items = []

        # Group by type
        grouped = qto_data.groupby([category_column, type_column]).agg({
            quantity_column: 'sum'
        }).reset_index()

        for _, row in grouped.iterrows():
            items = self.estimate_element(
                bim_type=row[type_column],
                category=row[category_column],
                quantity=row[quantity_column],
                quantity_unit="m³"  # Assume volume, adjust based on category
            )
            all_line_items.extend(items)

        return all_line_items

    def _convert_units(
        self,
        value: float,
        from_unit: str,
        to_unit: str
    ) -> float:
        """Convert between units"""

        # Simplified conversion - expand as needed
        conversions = {
            ('m³', 'm³'): 1.0,
            ('m²', 'm²'): 1.0,
            ('m', 'm'): 1.0,
            ('ft³', 'm³'): 0.0283168,
            ('ft²', 'm²'): 0.092903,
            ('ft', 'm'): 0.3048,
        }

        key = (from_unit.lower(), to_unit.lower())
        factor = conversions.get(key, 1.0)

        return value * factor

    def _get_trade(self, category: str) -> str:
        """Map BIM category to trade"""
        trade_map = {
            'Walls': 'Masonry',
            'Floors': 'Concrete',
            'Structural Columns': 'Concrete',
            'Structural Framing': 'Steel',
            'Doors': 'Carpentry',
            'Windows': 'Glazing',
            'Plumbing Fixtures': 'Plumbing',
            'Electrical Equipment': 'Electrical',
            'Mechanical Equipment': 'HVAC'
        }
        return trade_map.get(category, 'General')

    def generate_estimate_report(
        self,
        line_items: List[CostLineItem],
        project_name: str,
        output_path: str
    ) -> dict:
        """Generate comprehensive estimate report"""

        # Convert to DataFrame
        records = []
        for item in line_items:
            records.append({
                'BIM Type': item.bim_type,
                'Work Item': item.work_item.description,
                'CWICR Code': item.work_item.cwicr_code,
                'Quantity': round(item.quantity, 2),
                'Unit': item.quantity_unit,
                'Unit Price': round(item.work_item.unit_price, 2),
                'Labor': round(item.labor_cost, 2),
                'Material': round(item.material_cost, 2),
                'Equipment': round(item.equipment_cost, 2),
                'Total': round(item.total_cost, 2),
                'Phase': item.phase,
                'Trade': item.trade,
                'Currency': item.work_item.currency,
                'Confidence': round(item.work_item.confidence, 2)
            })

        df = pd.DataFrame(records)

        # Calculate totals
        total_cost = df['Total'].sum()
        total_labor = df['Labor'].sum()
        total_material = df['Material'].sum()
        total_equipment = df['Equipment'].sum()

        # Summary by trade
        by_trade = df.groupby('Trade')['Total'].sum().sort_values(ascending=False)

        # Write Excel
        excel_path = f"{output_path}/{project_name}_Estimate.xlsx"
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            # Summary sheet
            summary_data = {
                'Metric': ['Total Cost', 'Labor Cost', 'Material Cost', 'Equipment Cost'],
                'Value': [total_cost, total_labor, total_material, total_equipment]
            }
            pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)

            # By Trade
            by_trade.to_frame().to_excel(writer, sheet_name='By Trade')

            # Detail
            df.to_excel(writer, sheet_name='Detail', index=False)

        return {
            'excel_path': excel_path,
            'total_cost': total_cost,
            'total_labor': total_labor,
            'total_material': total_material,
            'total_equipment': total_equipment,
            'by_trade': by_trade.to_dict(),
            'line_items': len(df),
            'currency': line_items[0].work_item.currency if line_items else 'USD'
        }


# Usage Example
def estimate_from_bim_model(
    model_path: str,
    qdrant_url: str,
    language: str = "EN",
    output_dir: str = "."
) -> dict:
    """Complete BIM to cost estimation workflow"""

    import subprocess
    from pathlib import Path

    # Step 1: Convert BIM to Excel
    print("Converting BIM model...")
    subprocess.run([
        r"C:\DDC\RvtExporter.exe",
        model_path,
        "complete", "bbox"
    ])

    xlsx_path = Path(model_path).with_suffix('.xlsx')

    # Step 2: Load QTO data
    print("Loading quantity data...")
    df = pd.read_excel(xlsx_path)

    # Step 3: Initialize estimator
    estimator = BIMCostEstimator(
        qdrant_url=qdrant_url,
        language=language
    )

    # Step 4: Generate estimate
    print("Generating cost estimate...")
    line_items = estimator.estimate_from_qto(df)

    # Step 5: Generate report
    project_name = Path(model_path).stem
    result = estimator.generate_estimate_report(
        line_items=line_items,
        project_name=project_name,
        output_path=output_dir
    )

    print(f"\nEstimate Complete!")
    print(f"Total Cost: {result['currency']} {result['total_cost']:,.2f}")
    print(f"Excel Report: {result['excel_path']}")

    return result


if __name__ == "__main__":
    result = estimate_from_bim_model(
        model_path=r"C:\Projects\Building.rvt",
        qdrant_url="https://your-qdrant-instance.io",
        language="DE",
        output_dir=r"C:\Projects\Estimates"
    )
```

## n8n 工作流程

详见：`n8n_4_CAD_(BIM)_Cost_Estimation_Pipeline_4D_5D_with_DDC_CWICR.json`

```yaml
stages:
  - convert: RvtExporter → XLSX
  - detect_project: LLM identifies project type
  - generate_phases: LLM creates construction phases
  - decompose: LLM breaks types into work items
  - vector_search: Qdrant finds CWICR matches
  - calculate: Qty × Unit Price
  - validate: CTO review
  - report: HTML + Excel output
```

## 输出示例

```
╔══════════════════════════════════════════════════════════════╗
║                    COST ESTIMATE SUMMARY                      ║
║   Project: Office Building Berlin                             ║
║   Date: 2026-01-24                                           ║
╠══════════════════════════════════════════════════════════════╣

TOTAL PROJECT COST:                    EUR 4,523,678.00
───────────────────────────────────────────────────────────────
  Labor:                               EUR 1,847,234.00 (41%)
  Materials:                           EUR 2,312,456.00 (51%)
  Equipment:                           EUR   363,988.00 ( 8%)

BY TRADE
───────────────────────────────────────────────────────────────
  Concrete:                            EUR 1,234,567.00 (27%)
  Masonry:                             EUR   876,543.00 (19%)
  Steel Structure:                     EUR   654,321.00 (14%)
  MEP:                                 EUR   543,210.00 (12%)
  Finishes:                            EUR   432,109.00 (10%)
  Other:                               EUR   782,928.00 (18%)

CONFIDENCE ANALYSIS
───────────────────────────────────────────────────────────────
  High (>0.85):                        78%
  Medium (0.70-0.85):                  18%
  Low (<0.70):                          4%

╚══════════════════════════════════════════════════════════════╝
```

## 资源

- **DDC CWICR 仓库**：https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR
- **在线演示**：https://openconstructionestimate.com
- **Qdrant**：https://qdrant.tech

---

*“基于资源的成本核算方法将实际工程量与价格波动因素分离，从而实现透明且可审计的估算结果。”*