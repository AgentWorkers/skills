---
slug: "submittal-tracker"
display_name: "Submittal Tracker"
description: "跟踪构建提交文件在整个审核流程中的状态。管理审批、修订以及合规性相关事宜。"
---

# 提交跟踪系统

## 商业背景

为了防止延误，提交过程需要被仔细跟踪。该功能负责管理从创建到审批的整个提交工作流程。

## 技术实现

```python
import pandas as pd
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class SubmittalStatus(Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    APPROVED_AS_NOTED = "approved_as_noted"
    REVISE_RESUBMIT = "revise_resubmit"
    REJECTED = "rejected"


class SubmittalType(Enum):
    PRODUCT_DATA = "product_data"
    SHOP_DRAWING = "shop_drawing"
    SAMPLE = "sample"
    MOCK_UP = "mock_up"
    CERTIFICATE = "certificate"
    TEST_REPORT = "test_report"


@dataclass
class ReviewComment:
    reviewer: str
    comment: str
    comment_date: date
    resolved: bool = False


@dataclass
class Submittal:
    submittal_id: str
    spec_section: str
    title: str
    submittal_type: SubmittalType
    status: SubmittalStatus
    contractor: str
    revision: int
    submitted_date: Optional[date]
    required_date: date
    approved_date: Optional[date] = None
    comments: List[ReviewComment] = field(default_factory=list)
    files: List[str] = field(default_factory=list)


class SubmittalTracker:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.submittals: Dict[str, Submittal] = {}
        self._counter = 0

    def create_submittal(self, spec_section: str, title: str,
                        submittal_type: SubmittalType, contractor: str,
                        required_date: date) -> Submittal:
        self._counter += 1
        sub_id = f"SUB-{self._counter:04d}"

        submittal = Submittal(
            submittal_id=sub_id,
            spec_section=spec_section,
            title=title,
            submittal_type=submittal_type,
            status=SubmittalStatus.DRAFT,
            contractor=contractor,
            revision=0,
            submitted_date=None,
            required_date=required_date
        )
        self.submittals[sub_id] = submittal
        return submittal

    def submit(self, sub_id: str, files: List[str]):
        if sub_id in self.submittals:
            self.submittals[sub_id].status = SubmittalStatus.SUBMITTED
            self.submittals[sub_id].submitted_date = date.today()
            self.submittals[sub_id].files = files

    def review(self, sub_id: str, status: SubmittalStatus, reviewer: str, comment: str = ""):
        if sub_id in self.submittals:
            sub = self.submittals[sub_id]
            sub.status = status
            if comment:
                sub.comments.append(ReviewComment(reviewer, comment, date.today()))
            if status in [SubmittalStatus.APPROVED, SubmittalStatus.APPROVED_AS_NOTED]:
                sub.approved_date = date.today()

    def resubmit(self, sub_id: str, files: List[str]):
        if sub_id in self.submittals:
            sub = self.submittals[sub_id]
            sub.revision += 1
            sub.status = SubmittalStatus.SUBMITTED
            sub.submitted_date = date.today()
            sub.files = files

    def get_pending(self) -> List[Submittal]:
        return [s for s in self.submittals.values()
                if s.status in [SubmittalStatus.SUBMITTED, SubmittalStatus.UNDER_REVIEW]]

    def get_overdue(self) -> List[Submittal]:
        today = date.today()
        return [s for s in self.submittals.values()
                if s.status not in [SubmittalStatus.APPROVED, SubmittalStatus.APPROVED_AS_NOTED]
                and s.required_date < today]

    def export_log(self, output_path: str):
        data = [{
            'ID': s.submittal_id,
            'Spec': s.spec_section,
            'Title': s.title,
            'Type': s.submittal_type.value,
            'Status': s.status.value,
            'Rev': s.revision,
            'Submitted': s.submitted_date,
            'Required': s.required_date,
            'Approved': s.approved_date
        } for s in self.submittals.values()]
        pd.DataFrame(data).to_excel(output_path, index=False)
```

## 快速入门

```python
tracker = SubmittalTracker("Office Tower")

sub = tracker.create_submittal("09 29 00", "Gypsum Board",
                               SubmittalType.PRODUCT_DATA, "ABC Drywall",
                               date.today() + timedelta(days=14))
tracker.submit(sub.submittal_id, ["spec_sheet.pdf"])
tracker.review(sub.submittal_id, SubmittalStatus.APPROVED, "Architect")
```

## 资源
- **DDC手册**：第4章 - 文档控制