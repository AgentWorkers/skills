---
slug: "bim-clash-detection"
display_name: "BIM Clash Detection"
description: "在BIM模型中检测并分析几何冲突。在施工前识别机电（MEP）、结构和建筑方面的矛盾或冲突。"
---

# BIM碰撞检测

## 商业案例

### 问题描述
协调问题导致了大量的返工：
- 现场发现机电（MEP）系统与结构系统之间的冲突
- 设计变更发生在后期，增加了成本
- 手动碰撞审查耗时较长
- 缺乏标准化的碰撞分类体系

### 解决方案
开发一个自动化的碰撞检测与分析系统，能够识别不同建筑系统之间的冲突，并提供优先级的解决建议。

### 商业价值
- **成本节约**：在施工前发现问题
- **时间节省**：自动化碰撞识别过程
- **协调效率提升**：系统化的冲突解决机制
- **质量改善**：减少现场问题的发生

## 技术实现

```python
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import math


class ClashType(Enum):
    """Types of clashes."""
    HARD = "hard"           # Physical intersection
    SOFT = "soft"           # Clearance violation
    WORKFLOW = "workflow"   # Sequencing conflict
    DUPLICATE = "duplicate" # Duplicated elements


class ClashStatus(Enum):
    """Clash resolution status."""
    NEW = "new"
    ACTIVE = "active"
    RESOLVED = "resolved"
    APPROVED = "approved"
    IGNORED = "ignored"


class ClashSeverity(Enum):
    """Clash severity level."""
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    INFO = "info"


class Discipline(Enum):
    """BIM disciplines."""
    ARCHITECTURAL = "architectural"
    STRUCTURAL = "structural"
    MECHANICAL = "mechanical"
    ELECTRICAL = "electrical"
    PLUMBING = "plumbing"
    FIRE_PROTECTION = "fire_protection"
    CIVIL = "civil"


@dataclass
class BoundingBox:
    """3D bounding box."""
    min_x: float
    min_y: float
    min_z: float
    max_x: float
    max_y: float
    max_z: float

    def intersects(self, other: 'BoundingBox') -> bool:
        """Check if boxes intersect."""
        return (self.min_x <= other.max_x and self.max_x >= other.min_x and
                self.min_y <= other.max_y and self.max_y >= other.min_y and
                self.min_z <= other.max_z and self.max_z >= other.min_z)

    def volume(self) -> float:
        """Calculate bounding box volume."""
        return ((self.max_x - self.min_x) *
                (self.max_y - self.min_y) *
                (self.max_z - self.min_z))

    def center(self) -> Tuple[float, float, float]:
        """Get center point."""
        return (
            (self.min_x + self.max_x) / 2,
            (self.min_y + self.max_y) / 2,
            (self.min_z + self.max_z) / 2
        )


@dataclass
class BIMElement:
    """BIM element representation."""
    element_id: str
    name: str
    discipline: Discipline
    category: str  # e.g., "Duct", "Beam", "Pipe"
    level: str
    bounding_box: BoundingBox
    properties: Dict[str, Any] = field(default_factory=dict)

    def distance_to(self, other: 'BIMElement') -> float:
        """Calculate distance between element centers."""
        c1 = self.bounding_box.center()
        c2 = other.bounding_box.center()
        return math.sqrt(
            (c2[0] - c1[0])**2 +
            (c2[1] - c1[1])**2 +
            (c2[2] - c1[2])**2
        )


@dataclass
class Clash:
    """Clash between two elements."""
    clash_id: str
    element_a: BIMElement
    element_b: BIMElement
    clash_type: ClashType
    severity: ClashSeverity
    status: ClashStatus
    distance: float  # Penetration depth (negative) or clearance gap
    location: Tuple[float, float, float]
    detected_at: datetime
    resolved_at: Optional[datetime] = None
    assigned_to: Optional[str] = None
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            'clash_id': self.clash_id,
            'element_a_id': self.element_a.element_id,
            'element_a_name': self.element_a.name,
            'element_a_discipline': self.element_a.discipline.value,
            'element_b_id': self.element_b.element_id,
            'element_b_name': self.element_b.name,
            'element_b_discipline': self.element_b.discipline.value,
            'clash_type': self.clash_type.value,
            'severity': self.severity.value,
            'status': self.status.value,
            'distance': round(self.distance, 3),
            'location_x': self.location[0],
            'location_y': self.location[1],
            'location_z': self.location[2],
            'level': self.element_a.level,
            'detected_at': self.detected_at.isoformat(),
            'assigned_to': self.assigned_to,
            'notes': self.notes
        }


@dataclass
class ClashTest:
    """Clash test configuration."""
    name: str
    discipline_a: Discipline
    discipline_b: Discipline
    clash_type: ClashType
    tolerance: float = 0.0  # Clearance tolerance in meters
    enabled: bool = True


class BIMClashDetector:
    """Detect and manage BIM clashes."""

    def __init__(self):
        self.elements: List[BIMElement] = []
        self.clashes: List[Clash] = []
        self.clash_tests: List[ClashTest] = []
        self._clash_counter = 0

    def load_elements(self, elements_df: pd.DataFrame) -> int:
        """Load BIM elements from DataFrame."""
        loaded = 0
        for _, row in elements_df.iterrows():
            element = BIMElement(
                element_id=str(row.get('element_id', '')),
                name=str(row.get('name', '')),
                discipline=Discipline(row.get('discipline', 'architectural')),
                category=str(row.get('category', '')),
                level=str(row.get('level', '')),
                bounding_box=BoundingBox(
                    min_x=float(row.get('min_x', 0)),
                    min_y=float(row.get('min_y', 0)),
                    min_z=float(row.get('min_z', 0)),
                    max_x=float(row.get('max_x', 0)),
                    max_y=float(row.get('max_y', 0)),
                    max_z=float(row.get('max_z', 0))
                )
            )
            self.elements.append(element)
            loaded += 1
        return loaded

    def add_clash_test(self, test: ClashTest):
        """Add clash test configuration."""
        self.clash_tests.append(test)

    def setup_standard_tests(self):
        """Setup standard MEP coordination tests."""
        standard_tests = [
            ClashTest("MEP vs Structure", Discipline.MECHANICAL, Discipline.STRUCTURAL, ClashType.HARD),
            ClashTest("Electrical vs Structure", Discipline.ELECTRICAL, Discipline.STRUCTURAL, ClashType.HARD),
            ClashTest("Plumbing vs Structure", Discipline.PLUMBING, Discipline.STRUCTURAL, ClashType.HARD),
            ClashTest("MEP vs MEP", Discipline.MECHANICAL, Discipline.ELECTRICAL, ClashType.HARD),
            ClashTest("Duct Clearance", Discipline.MECHANICAL, Discipline.MECHANICAL, ClashType.SOFT, tolerance=0.05),
            ClashTest("Fire Protection", Discipline.FIRE_PROTECTION, Discipline.STRUCTURAL, ClashType.HARD),
        ]
        for test in standard_tests:
            self.add_clash_test(test)

    def run_clash_detection(self) -> List[Clash]:
        """Run all clash tests."""
        new_clashes = []

        for test in self.clash_tests:
            if not test.enabled:
                continue

            # Filter elements by discipline
            elements_a = [e for e in self.elements if e.discipline == test.discipline_a]
            elements_b = [e for e in self.elements if e.discipline == test.discipline_b]

            # Check all pairs
            for elem_a in elements_a:
                for elem_b in elements_b:
                    if elem_a.element_id == elem_b.element_id:
                        continue

                    clash = self._check_clash(elem_a, elem_b, test)
                    if clash:
                        new_clashes.append(clash)

        self.clashes.extend(new_clashes)
        return new_clashes

    def _check_clash(self, elem_a: BIMElement, elem_b: BIMElement,
                     test: ClashTest) -> Optional[Clash]:
        """Check if two elements clash."""

        # Expand bounding box by tolerance for soft clashes
        box_a = elem_a.bounding_box
        box_b = elem_b.bounding_box

        if test.clash_type == ClashType.SOFT:
            # Add clearance tolerance
            expanded_a = BoundingBox(
                box_a.min_x - test.tolerance, box_a.min_y - test.tolerance, box_a.min_z - test.tolerance,
                box_a.max_x + test.tolerance, box_a.max_y + test.tolerance, box_a.max_z + test.tolerance
            )
            intersects = expanded_a.intersects(box_b)
        else:
            intersects = box_a.intersects(box_b)

        if not intersects:
            return None

        # Calculate clash point and severity
        self._clash_counter += 1
        clash_id = f"CLH-{self._clash_counter:05d}"

        # Clash location (center of intersection)
        location = (
            (max(box_a.min_x, box_b.min_x) + min(box_a.max_x, box_b.max_x)) / 2,
            (max(box_a.min_y, box_b.min_y) + min(box_a.max_y, box_b.max_y)) / 2,
            (max(box_a.min_z, box_b.min_z) + min(box_a.max_z, box_b.max_z)) / 2
        )

        # Calculate penetration depth
        distance = elem_a.distance_to(elem_b)

        # Determine severity
        if test.clash_type == ClashType.HARD:
            severity = ClashSeverity.CRITICAL if distance < 0.1 else ClashSeverity.MAJOR
        else:
            severity = ClashSeverity.MINOR if distance > test.tolerance else ClashSeverity.MAJOR

        return Clash(
            clash_id=clash_id,
            element_a=elem_a,
            element_b=elem_b,
            clash_type=test.clash_type,
            severity=severity,
            status=ClashStatus.NEW,
            distance=distance,
            location=location,
            detected_at=datetime.now()
        )

    def get_summary(self) -> Dict[str, Any]:
        """Get clash detection summary."""
        by_severity = {}
        by_discipline = {}
        by_status = {}

        for clash in self.clashes:
            # By severity
            sev = clash.severity.value
            by_severity[sev] = by_severity.get(sev, 0) + 1

            # By discipline pair
            pair = f"{clash.element_a.discipline.value} vs {clash.element_b.discipline.value}"
            by_discipline[pair] = by_discipline.get(pair, 0) + 1

            # By status
            stat = clash.status.value
            by_status[stat] = by_status.get(stat, 0) + 1

        return {
            'total_clashes': len(self.clashes),
            'by_severity': by_severity,
            'by_discipline': by_discipline,
            'by_status': by_status,
            'elements_checked': len(self.elements),
            'tests_run': len([t for t in self.clash_tests if t.enabled])
        }

    def export_to_dataframe(self) -> pd.DataFrame:
        """Export clashes to DataFrame."""
        return pd.DataFrame([c.to_dict() for c in self.clashes])

    def resolve_clash(self, clash_id: str, resolution_note: str):
        """Mark clash as resolved."""
        for clash in self.clashes:
            if clash.clash_id == clash_id:
                clash.status = ClashStatus.RESOLVED
                clash.resolved_at = datetime.now()
                clash.notes = resolution_note
                break

    def assign_clash(self, clash_id: str, assignee: str):
        """Assign clash to team member."""
        for clash in self.clashes:
            if clash.clash_id == clash_id:
                clash.assigned_to = assignee
                clash.status = ClashStatus.ACTIVE
                break
```

## 快速入门

```python
# Initialize detector
detector = BIMClashDetector()

# Setup standard MEP tests
detector.setup_standard_tests()

# Load elements from DataFrame
elements_df = pd.read_excel("bim_elements.xlsx")
detector.load_elements(elements_df)

# Run detection
clashes = detector.run_clash_detection()
print(f"Found {len(clashes)} clashes")

# Get summary
summary = detector.get_summary()
print(f"Critical: {summary['by_severity'].get('critical', 0)}")
```

## 常见使用场景

### 1. 机电系统协调
```python
# Focus on MEP vs Structure
mep_clashes = [c for c in detector.clashes
               if c.element_a.discipline in [Discipline.MECHANICAL, Discipline.ELECTRICAL]]
```

### 2. 数据导出以供审查
```python
df = detector.export_to_dataframe()
df.to_excel("clash_report.xlsx", index=False)
```

### 3. 分配给团队处理
```python
for clash in detector.clashes:
    if clash.element_a.discipline == Discipline.MECHANICAL:
        detector.assign_clash(clash.clash_id, "MEP Team")
```

## 参考资源
- **DDC手册**：第2.4章 - BIM协调
- **参考标准**：ISO 19650 BIM标准