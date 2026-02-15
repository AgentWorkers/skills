---
slug: "cwicr-takeoff-helper"
display_name: "CWICR Takeoff Helper"
description: "使用 CWICR 数据协助进行数量统计。根据尺寸计算所需数量，应用损耗系数，并提出相关的工作建议。"
---

# CWICR 计量辅助工具

## 商业案例

### 问题描述
进行数量计量时需要：
- 根据尺寸数据进行精确的计算
- 正确的单位转换
- 应用相应的损耗系数
- 确保覆盖所有相关项目

### 解决方案
通过基于 CWICR 的计算、自动损耗系数计算、单位转换以及相关项目的推荐来辅助计量过程。

### 商业价值
- **准确性**：经过验证的计算结果
- **完整性**：提供相关的建议项目
- **速度**：快速完成数量计算
- **一致性**：采用标准化的计算方法

## 技术实现
```python
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math


class TakeoffType(Enum):
    """Types of takeoff calculations."""
    LINEAR = "linear"        # Length
    AREA = "area"            # Square measure
    VOLUME = "volume"        # Cubic measure
    COUNT = "count"          # Each/number
    WEIGHT = "weight"        # By weight


class UnitSystem(Enum):
    """Unit systems."""
    METRIC = "metric"
    IMPERIAL = "imperial"


@dataclass
class TakeoffItem:
    """Single takeoff item."""
    work_item_code: str
    description: str
    takeoff_type: TakeoffType
    gross_quantity: float
    waste_factor: float
    net_quantity: float
    unit: str
    dimensions: Dict[str, float]
    calculation: str


@dataclass
class TakeoffResult:
    """Complete takeoff result."""
    items: List[TakeoffItem]
    total_items: int
    related_suggestions: List[str]


# Unit conversion factors
CONVERSIONS = {
    # Length
    ('m', 'ft'): 3.28084,
    ('ft', 'm'): 0.3048,
    ('m', 'in'): 39.3701,
    ('in', 'm'): 0.0254,

    # Area
    ('m2', 'sf'): 10.7639,
    ('sf', 'm2'): 0.0929,

    # Volume
    ('m3', 'cf'): 35.3147,
    ('cf', 'm3'): 0.0283,
    ('m3', 'cy'): 1.30795,
    ('cy', 'm3'): 0.7646,

    # Weight
    ('kg', 'lb'): 2.20462,
    ('lb', 'kg'): 0.453592,
    ('ton', 'kg'): 1000,
    ('kg', 'ton'): 0.001
}

# Standard waste factors
WASTE_FACTORS = {
    'concrete': 0.05,
    'rebar': 0.08,
    'formwork': 0.10,
    'brick': 0.10,
    'block': 0.08,
    'drywall': 0.12,
    'tile': 0.15,
    'lumber': 0.12,
    'roofing': 0.10,
    'paint': 0.10,
    'pipe': 0.05,
    'wire': 0.05,
    'duct': 0.08,
    'default': 0.05
}

# Related work items by category
RELATED_ITEMS = {
    'concrete': ['formwork', 'rebar', 'curing', 'finishing'],
    'masonry': ['mortar', 'reinforcement', 'ties', 'lintels'],
    'drywall': ['framing', 'insulation', 'taping', 'painting'],
    'roofing': ['underlayment', 'flashing', 'ventilation', 'insulation'],
    'flooring': ['underlayment', 'adhesive', 'trim', 'transitions']
}


class CWICRTakeoffHelper:
    """Assist with quantity takeoff using CWICR data."""

    def __init__(self, cwicr_data: pd.DataFrame = None):
        self.cwicr = cwicr_data
        if cwicr_data is not None:
            self._index_cwicr()

    def _index_cwicr(self):
        """Index CWICR data."""
        if 'work_item_code' in self.cwicr.columns:
            self._cwicr_index = self.cwicr.set_index('work_item_code')
        else:
            self._cwicr_index = None

    def convert_unit(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert between units."""
        if from_unit == to_unit:
            return value

        key = (from_unit.lower(), to_unit.lower())
        if key in CONVERSIONS:
            return value * CONVERSIONS[key]

        # Try reverse
        reverse_key = (to_unit.lower(), from_unit.lower())
        if reverse_key in CONVERSIONS:
            return value / CONVERSIONS[reverse_key]

        return value

    def get_waste_factor(self, work_item_code: str) -> float:
        """Get waste factor for work item."""
        code_lower = work_item_code.lower()

        for material, factor in WASTE_FACTORS.items():
            if material in code_lower:
                return factor

        return WASTE_FACTORS['default']

    def calculate_area(self,
                       length: float,
                       width: float,
                       deductions: List[Tuple[float, float]] = None) -> Dict[str, float]:
        """Calculate area with deductions."""

        gross_area = length * width

        deduction_area = 0
        if deductions:
            for d_length, d_width in deductions:
                deduction_area += d_length * d_width

        net_area = gross_area - deduction_area

        return {
            'gross_area': round(gross_area, 2),
            'deductions': round(deduction_area, 2),
            'net_area': round(net_area, 2),
            'calculation': f"{length} x {width} = {gross_area}, minus {deduction_area} deductions"
        }

    def calculate_volume(self,
                          length: float,
                          width: float,
                          depth: float) -> Dict[str, float]:
        """Calculate volume."""

        volume = length * width * depth

        return {
            'volume': round(volume, 3),
            'calculation': f"{length} x {width} x {depth} = {volume}"
        }

    def calculate_perimeter(self,
                            length: float,
                            width: float) -> Dict[str, float]:
        """Calculate perimeter."""

        perimeter = 2 * (length + width)

        return {
            'perimeter': round(perimeter, 2),
            'calculation': f"2 x ({length} + {width}) = {perimeter}"
        }

    def calculate_concrete(self,
                            length: float,
                            width: float,
                            thickness: float,
                            work_item_code: str = "CONC-001") -> TakeoffItem:
        """Calculate concrete quantity with related items."""

        volume = length * width * thickness
        waste = self.get_waste_factor(work_item_code)
        net_qty = volume * (1 + waste)

        return TakeoffItem(
            work_item_code=work_item_code,
            description="Concrete",
            takeoff_type=TakeoffType.VOLUME,
            gross_quantity=round(volume, 3),
            waste_factor=waste,
            net_quantity=round(net_qty, 3),
            unit="m3",
            dimensions={'length': length, 'width': width, 'thickness': thickness},
            calculation=f"{length}m x {width}m x {thickness}m = {volume:.3f} m3 + {waste:.0%} waste"
        )

    def calculate_wall_area(self,
                             perimeter: float,
                             height: float,
                             openings: List[Tuple[float, float]] = None,
                             work_item_code: str = "WALL-001") -> TakeoffItem:
        """Calculate wall area with openings deducted."""

        gross_area = perimeter * height

        opening_area = 0
        if openings:
            for w, h in openings:
                opening_area += w * h

        net_area = gross_area - opening_area
        waste = self.get_waste_factor(work_item_code)
        order_qty = net_area * (1 + waste)

        return TakeoffItem(
            work_item_code=work_item_code,
            description="Wall finish",
            takeoff_type=TakeoffType.AREA,
            gross_quantity=round(gross_area, 2),
            waste_factor=waste,
            net_quantity=round(order_qty, 2),
            unit="m2",
            dimensions={'perimeter': perimeter, 'height': height, 'openings': len(openings or [])},
            calculation=f"{perimeter}m x {height}m = {gross_area:.2f} m2 - {opening_area:.2f} openings + {waste:.0%} waste"
        )

    def calculate_flooring(self,
                            length: float,
                            width: float,
                            work_item_code: str = "FLOOR-001") -> TakeoffItem:
        """Calculate flooring quantity."""

        area = length * width
        waste = self.get_waste_factor(work_item_code)
        order_qty = area * (1 + waste)

        return TakeoffItem(
            work_item_code=work_item_code,
            description="Flooring",
            takeoff_type=TakeoffType.AREA,
            gross_quantity=round(area, 2),
            waste_factor=waste,
            net_quantity=round(order_qty, 2),
            unit="m2",
            dimensions={'length': length, 'width': width},
            calculation=f"{length}m x {width}m = {area:.2f} m2 + {waste:.0%} waste"
        )

    def calculate_rebar(self,
                         concrete_volume: float,
                         kg_per_m3: float = 100,
                         work_item_code: str = "REBAR-001") -> TakeoffItem:
        """Calculate rebar from concrete volume."""

        weight = concrete_volume * kg_per_m3
        waste = self.get_waste_factor(work_item_code)
        order_qty = weight * (1 + waste)

        return TakeoffItem(
            work_item_code=work_item_code,
            description="Reinforcement",
            takeoff_type=TakeoffType.WEIGHT,
            gross_quantity=round(weight, 1),
            waste_factor=waste,
            net_quantity=round(order_qty, 1),
            unit="kg",
            dimensions={'concrete_m3': concrete_volume, 'kg_per_m3': kg_per_m3},
            calculation=f"{concrete_volume} m3 x {kg_per_m3} kg/m3 = {weight:.1f} kg + {waste:.0%} waste"
        )

    def suggest_related_items(self, work_item_code: str) -> List[str]:
        """Suggest related work items."""

        code_lower = work_item_code.lower()

        for category, related in RELATED_ITEMS.items():
            if category in code_lower:
                return related

        return []

    def room_takeoff(self,
                      length: float,
                      width: float,
                      height: float,
                      openings: List[Tuple[float, float]] = None) -> TakeoffResult:
        """Complete room takeoff."""

        items = []

        # Floor
        floor = self.calculate_flooring(length, width, "FLOOR-001")
        items.append(floor)

        # Ceiling (same as floor)
        ceiling = TakeoffItem(
            work_item_code="CEIL-001",
            description="Ceiling",
            takeoff_type=TakeoffType.AREA,
            gross_quantity=floor.gross_quantity,
            waste_factor=floor.waste_factor,
            net_quantity=floor.net_quantity,
            unit="m2",
            dimensions=floor.dimensions,
            calculation=f"Same as floor: {floor.gross_quantity} m2"
        )
        items.append(ceiling)

        # Walls
        perimeter = 2 * (length + width)
        walls = self.calculate_wall_area(perimeter, height, openings, "WALL-001")
        items.append(walls)

        # Related suggestions
        suggestions = ['paint', 'baseboard', 'trim', 'electrical outlets']

        return TakeoffResult(
            items=items,
            total_items=len(items),
            related_suggestions=suggestions
        )

    def export_takeoff(self,
                        items: List[TakeoffItem],
                        output_path: str) -> str:
        """Export takeoff to Excel."""

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df = pd.DataFrame([
                {
                    'Work Item Code': item.work_item_code,
                    'Description': item.description,
                    'Type': item.takeoff_type.value,
                    'Gross Qty': item.gross_quantity,
                    'Waste %': f"{item.waste_factor:.0%}",
                    'Net Qty': item.net_quantity,
                    'Unit': item.unit,
                    'Calculation': item.calculation
                }
                for item in items
            ])
            df.to_excel(writer, sheet_name='Takeoff', index=False)

        return output_path
```

## 快速入门
```python
# Initialize helper
helper = CWICRTakeoffHelper()

# Calculate concrete slab
concrete = helper.calculate_concrete(
    length=10,
    width=8,
    thickness=0.2
)

print(f"Gross: {concrete.gross_quantity} m3")
print(f"Order Qty: {concrete.net_quantity} m3")
print(f"Calculation: {concrete.calculation}")
```

## 常见使用场景

### 1. 房间面积计量
```python
room = helper.room_takeoff(
    length=5,
    width=4,
    height=2.8,
    openings=[(0.9, 2.1), (1.2, 1.5)]  # door, window
)

for item in room.items:
    print(f"{item.description}: {item.net_quantity} {item.unit}")
```

### 2. 单位转换
```python
meters = helper.convert_unit(100, 'ft', 'm')
print(f"100 ft = {meters:.2f} m")
```

### 3. 从混凝土中提取钢筋的数量
```python
concrete = helper.calculate_concrete(10, 8, 0.3)
rebar = helper.calculate_rebar(concrete.gross_quantity, kg_per_m3=120)
print(f"Rebar: {rebar.net_quantity} kg")
```

### 4. 相关项目统计
```python
related = helper.suggest_related_items("CONC-SLAB-001")
print(f"Related: {related}")
```

## 资源
- **GitHub**: [OpenConstructionEstimate-DDC-CWICR](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR)
- **DDC 书籍**: 第 3.1 章 - 数量计量方法