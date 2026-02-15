---
slug: "cwicr-historical-cost"
display_name: "CWICR Historical Cost"
description: "使用 CWICR 跟踪和分析历史成本数据。对比实际成本与估算成本，建立项目成本数据库，并改进未来的成本估算。"
---

# CWICR历史成本跟踪器

## 商业案例

### 问题描述
要提高估算的准确性，需要：
- 实际成本的反馈
- 历史数据的对比
- 趋势分析
- 经验总结

### 解决方案
将实际成本与CWICR的估算值进行对比，建立历史成本数据库，并利用这些数据来提高未来的估算精度。

### 商业价值
- **准确性提升**：通过实际数据来优化估算
- **基准对比**：项目间的成本比较
- **趋势分析**：成本变动模式的研究
- **组织知识积累**：构建成本数据库

## 技术实现

```python
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
import json


class ProjectStatus(Enum):
    """Project status."""
    ESTIMATED = "estimated"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class CostRecord:
    """Historical cost record."""
    project_id: str
    project_name: str
    work_item_code: str
    quantity: float
    estimated_cost: float
    actual_cost: float
    variance: float
    variance_percent: float
    completion_date: date
    notes: str = ""


@dataclass
class ProjectCostSummary:
    """Project cost summary."""
    project_id: str
    project_name: str
    project_type: str
    location: str
    status: ProjectStatus
    estimated_total: float
    actual_total: float
    variance: float
    variance_percent: float
    start_date: date
    completion_date: Optional[date]
    item_count: int


class CWICRHistoricalCost:
    """Track historical costs using CWICR data."""

    def __init__(self, cwicr_data: pd.DataFrame = None):
        self.cwicr = cwicr_data
        self._projects: Dict[str, ProjectCostSummary] = {}
        self._records: List[CostRecord] = []

        if cwicr_data is not None:
            self._index_cwicr()

    def _index_cwicr(self):
        """Index CWICR data."""
        if 'work_item_code' in self.cwicr.columns:
            self._cwicr_index = self.cwicr.set_index('work_item_code')
        else:
            self._cwicr_index = None

    def add_project(self,
                    project_id: str,
                    project_name: str,
                    project_type: str,
                    location: str,
                    estimated_total: float,
                    start_date: date) -> str:
        """Add new project to historical database."""

        summary = ProjectCostSummary(
            project_id=project_id,
            project_name=project_name,
            project_type=project_type,
            location=location,
            status=ProjectStatus.ESTIMATED,
            estimated_total=estimated_total,
            actual_total=0,
            variance=0,
            variance_percent=0,
            start_date=start_date,
            completion_date=None,
            item_count=0
        )

        self._projects[project_id] = summary
        return project_id

    def record_actual_cost(self,
                           project_id: str,
                           work_item_code: str,
                           quantity: float,
                           actual_cost: float,
                           completion_date: date = None,
                           notes: str = "") -> CostRecord:
        """Record actual cost for work item."""

        # Get estimated cost from CWICR
        estimated_unit_cost = 0
        if self._cwicr_index is not None and work_item_code in self._cwicr_index.index:
            item = self._cwicr_index.loc[work_item_code]
            labor = float(item.get('labor_cost', 0) or 0)
            material = float(item.get('material_cost', 0) or 0)
            equipment = float(item.get('equipment_cost', 0) or 0)
            estimated_unit_cost = labor + material + equipment

        estimated_cost = estimated_unit_cost * quantity
        variance = actual_cost - estimated_cost
        variance_pct = (variance / estimated_cost * 100) if estimated_cost > 0 else 0

        record = CostRecord(
            project_id=project_id,
            project_name=self._projects.get(project_id, {}).project_name if project_id in self._projects else "",
            work_item_code=work_item_code,
            quantity=quantity,
            estimated_cost=round(estimated_cost, 2),
            actual_cost=round(actual_cost, 2),
            variance=round(variance, 2),
            variance_percent=round(variance_pct, 1),
            completion_date=completion_date or date.today(),
            notes=notes
        )

        self._records.append(record)

        # Update project summary
        if project_id in self._projects:
            proj = self._projects[project_id]
            proj.actual_total += actual_cost
            proj.variance = proj.actual_total - proj.estimated_total
            proj.variance_percent = (proj.variance / proj.estimated_total * 100) if proj.estimated_total > 0 else 0
            proj.item_count += 1
            proj.status = ProjectStatus.IN_PROGRESS

        return record

    def complete_project(self, project_id: str, completion_date: date = None):
        """Mark project as completed."""
        if project_id in self._projects:
            self._projects[project_id].status = ProjectStatus.COMPLETED
            self._projects[project_id].completion_date = completion_date or date.today()

    def get_work_item_history(self, work_item_code: str) -> Dict[str, Any]:
        """Get historical data for specific work item."""

        records = [r for r in self._records if r.work_item_code == work_item_code]

        if not records:
            return {'work_item_code': work_item_code, 'records': 0}

        variances = [r.variance_percent for r in records]
        actual_costs = [r.actual_cost / r.quantity if r.quantity > 0 else 0 for r in records]

        return {
            'work_item_code': work_item_code,
            'records': len(records),
            'average_variance_pct': round(np.mean(variances), 1),
            'variance_std': round(np.std(variances), 1),
            'average_actual_unit_cost': round(np.mean(actual_costs), 2),
            'min_actual_unit_cost': round(min(actual_costs), 2),
            'max_actual_unit_cost': round(max(actual_costs), 2),
            'projects': list(set(r.project_id for r in records)),
            'trend': 'increasing' if len(records) > 2 and actual_costs[-1] > actual_costs[0] else 'stable'
        }

    def get_accuracy_metrics(self) -> Dict[str, Any]:
        """Calculate overall estimating accuracy metrics."""

        if not self._records:
            return {}

        variances = [r.variance_percent for r in self._records]

        # Accuracy by category
        by_category = {}
        for record in self._records:
            category = record.work_item_code.split('-')[0] if '-' in record.work_item_code else 'Other'
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(record.variance_percent)

        category_accuracy = {
            cat: {
                'average_variance': round(np.mean(vals), 1),
                'count': len(vals)
            }
            for cat, vals in by_category.items()
        }

        return {
            'total_records': len(self._records),
            'average_variance_pct': round(np.mean(variances), 1),
            'variance_std': round(np.std(variances), 1),
            'within_5pct': sum(1 for v in variances if abs(v) <= 5) / len(variances) * 100,
            'within_10pct': sum(1 for v in variances if abs(v) <= 10) / len(variances) * 100,
            'overestimated_pct': sum(1 for v in variances if v < 0) / len(variances) * 100,
            'underestimated_pct': sum(1 for v in variances if v > 0) / len(variances) * 100,
            'by_category': category_accuracy
        }

    def suggest_adjustment_factors(self) -> Dict[str, float]:
        """Suggest adjustment factors based on historical variance."""

        factors = {}

        for record in self._records:
            category = record.work_item_code.split('-')[0] if '-' in record.work_item_code else 'Other'
            if category not in factors:
                factors[category] = []

            if record.estimated_cost > 0:
                actual_factor = record.actual_cost / record.estimated_cost
                factors[category].append(actual_factor)

        return {
            cat: round(np.mean(vals), 3)
            for cat, vals in factors.items()
            if len(vals) >= 3  # Require minimum data points
        }

    def compare_projects(self,
                          project_ids: List[str] = None) -> pd.DataFrame:
        """Compare multiple projects."""

        if project_ids:
            projects = [self._projects[pid] for pid in project_ids if pid in self._projects]
        else:
            projects = list(self._projects.values())

        if not projects:
            return pd.DataFrame()

        return pd.DataFrame([
            {
                'Project ID': p.project_id,
                'Project Name': p.project_name,
                'Type': p.project_type,
                'Location': p.location,
                'Status': p.status.value,
                'Estimated': p.estimated_total,
                'Actual': p.actual_total,
                'Variance': p.variance,
                'Variance %': p.variance_percent,
                'Items': p.item_count
            }
            for p in projects
        ])

    def get_benchmarks_by_type(self, project_type: str) -> Dict[str, Any]:
        """Get cost benchmarks for project type."""

        projects = [p for p in self._projects.values() if p.project_type == project_type]

        if not projects:
            return {}

        actuals = [p.actual_total for p in projects if p.status == ProjectStatus.COMPLETED]

        return {
            'project_type': project_type,
            'completed_projects': len(actuals),
            'average_cost': round(np.mean(actuals), 2) if actuals else 0,
            'min_cost': round(min(actuals), 2) if actuals else 0,
            'max_cost': round(max(actuals), 2) if actuals else 0,
            'average_variance': round(np.mean([p.variance_percent for p in projects]), 1)
        }

    def export_historical_data(self, output_path: str) -> str:
        """Export historical data to Excel."""

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Projects
            if self._projects:
                projects_df = self.compare_projects()
                projects_df.to_excel(writer, sheet_name='Projects', index=False)

            # Records
            if self._records:
                records_df = pd.DataFrame([
                    {
                        'Project': r.project_id,
                        'Work Item': r.work_item_code,
                        'Quantity': r.quantity,
                        'Estimated': r.estimated_cost,
                        'Actual': r.actual_cost,
                        'Variance': r.variance,
                        'Variance %': r.variance_percent,
                        'Date': r.completion_date,
                        'Notes': r.notes
                    }
                    for r in self._records
                ])
                records_df.to_excel(writer, sheet_name='Records', index=False)

            # Accuracy metrics
            metrics = self.get_accuracy_metrics()
            if metrics:
                metrics_df = pd.DataFrame([{
                    'Total Records': metrics.get('total_records', 0),
                    'Avg Variance %': metrics.get('average_variance_pct', 0),
                    'Within 5%': f"{metrics.get('within_5pct', 0):.1f}%",
                    'Within 10%': f"{metrics.get('within_10pct', 0):.1f}%"
                }])
                metrics_df.to_excel(writer, sheet_name='Accuracy', index=False)

        return output_path

    def save_database(self, filepath: str):
        """Save historical database to JSON."""
        data = {
            'projects': {
                pid: {
                    'project_id': p.project_id,
                    'project_name': p.project_name,
                    'project_type': p.project_type,
                    'location': p.location,
                    'status': p.status.value,
                    'estimated_total': p.estimated_total,
                    'actual_total': p.actual_total,
                    'start_date': p.start_date.isoformat(),
                    'completion_date': p.completion_date.isoformat() if p.completion_date else None
                }
                for pid, p in self._projects.items()
            },
            'records': [
                {
                    'project_id': r.project_id,
                    'work_item_code': r.work_item_code,
                    'quantity': r.quantity,
                    'estimated_cost': r.estimated_cost,
                    'actual_cost': r.actual_cost,
                    'completion_date': r.completion_date.isoformat(),
                    'notes': r.notes
                }
                for r in self._records
            ]
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
```

## 快速入门

```python
from datetime import date

# Load CWICR data
cwicr = pd.read_parquet("ddc_cwicr_en.parquet")

# Initialize tracker
tracker = CWICRHistoricalCost(cwicr)

# Add project
tracker.add_project(
    project_id="PROJ-001",
    project_name="Office Building A",
    project_type="commercial",
    location="New York",
    estimated_total=5000000,
    start_date=date(2024, 1, 1)
)

# Record actual costs
tracker.record_actual_cost(
    project_id="PROJ-001",
    work_item_code="CONC-001",
    quantity=200,
    actual_cost=32000,
    notes="Slightly over due to overtime"
)
```

## 常见使用场景

### 1. 准确性分析
```python
metrics = tracker.get_accuracy_metrics()
print(f"Within 10%: {metrics['within_10pct']:.1f}%")
```

### 2. 调整因子
```python
factors = tracker.suggest_adjustment_factors()
for cat, factor in factors.items():
    print(f"{cat}: {factor:.2f}x")
```

### 3. 工作项历史记录
```python
history = tracker.get_work_item_history("CONC-001")
print(f"Average variance: {history['average_variance_pct']}%")
```

## 资源
- **GitHub**: [OpenConstructionEstimate-DDC-CWICR](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR)
- **DDC手册**: 第3.2章 - 历史成本分析