---
slug: "email-construction"
display_name: "Email Construction"
description: "用于建筑工作流程的电子邮件生成功能：包括请求信息（RFI）的回复、文件提交通知、会议通知以及变更订单提醒等。这些电子邮件使用专业的模板生成，并且能够根据具体情境自动生成相应的内容。"
---

# 用于建筑行业的电子邮件生成工具

## 概述

该工具能够生成格式规范、内容专业的建筑行业电子邮件，并支持附件的处理。提供了适用于常见建筑沟通工作流程的模板。

## 建筑行业中的使用场景

### 1. 信息请求（RFI）回复邮件

生成专业的信息请求（RFI）回复邮件。

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class RFIResponse:
    rfi_number: str
    project_name: str
    subject: str
    question: str
    response: str
    responder_name: str
    responder_title: str
    attachments: List[str] = None
    cc_list: List[str] = None

def generate_rfi_response_email(rfi: RFIResponse) -> dict:
    """Generate RFI response email."""

    subject = f"RE: RFI #{rfi.rfi_number} - {rfi.subject}"

    body = f"""Dear Project Team,

Please find below our response to RFI #{rfi.rfi_number}.

**Project:** {rfi.project_name}
**RFI Number:** {rfi.rfi_number}
**Subject:** {rfi.subject}
**Date:** {datetime.now().strftime('%B %d, %Y')}

---

**QUESTION:**
{rfi.question}

---

**RESPONSE:**
{rfi.response}

---

Please proceed accordingly. If you have any questions regarding this response, please contact us.

{"**Attachments:**" + chr(10) + chr(10).join(f"- {a}" for a in rfi.attachments) if rfi.attachments else ""}

Best regards,

{rfi.responder_name}
{rfi.responder_title}
"""

    return {
        'subject': subject,
        'body': body,
        'cc': rfi.cc_list or [],
        'attachments': rfi.attachments or []
    }
```

### 2. 提交文件传输邮件

生成用于提交文件的传输邮件。

```python
@dataclass
class SubmittalTransmittal:
    submittal_number: str
    project_name: str
    spec_section: str
    description: str
    items: List[dict]
    action_required: str
    due_date: str
    sender_name: str
    sender_company: str

def generate_submittal_email(submittal: SubmittalTransmittal) -> dict:
    """Generate submittal transmittal email."""

    subject = f"Submittal {submittal.submittal_number} - {submittal.spec_section} - {submittal.description}"

    items_list = "\n".join(
        f"   {i+1}. {item['description']} ({item.get('copies', 1)} copies)"
        for i, item in enumerate(submittal.items)
    )

    body = f"""Dear Design Team,

Please find attached Submittal {submittal.submittal_number} for your review.

**Project:** {submittal.project_name}
**Submittal No:** {submittal.submittal_number}
**Spec Section:** {submittal.spec_section}
**Description:** {submittal.description}

**Items Transmitted:**
{items_list}

**Action Required:** {submittal.action_required}
**Response Requested By:** {submittal.due_date}

Please review and return with your comments at your earliest convenience.
If you have any questions, please don't hesitate to contact us.

Best regards,

{submittal.sender_name}
{submittal.sender_company}
"""

    return {
        'subject': subject,
        'body': body,
        'priority': 'normal'
    }
```

### 3. 会议通知邮件

生成会议邀请邮件。

```python
@dataclass
class MeetingNotice:
    meeting_type: str  # 'OAC', 'Subcontractor', 'Safety', 'Coordination'
    project_name: str
    date: str
    time: str
    location: str
    virtual_link: Optional[str]
    agenda_items: List[str]
    attendees: List[str]
    organizer_name: str

def generate_meeting_notice(meeting: MeetingNotice) -> dict:
    """Generate meeting notice email."""

    subject = f"{meeting.meeting_type} Meeting - {meeting.project_name} - {meeting.date}"

    agenda = "\n".join(f"   {i+1}. {item}" for i, item in enumerate(meeting.agenda_items))

    location_info = meeting.location
    if meeting.virtual_link:
        location_info += f"\n   Virtual Option: {meeting.virtual_link}"

    body = f"""Dear Team,

You are invited to the {meeting.meeting_type} Meeting for {meeting.project_name}.

**Meeting Details:**
- **Date:** {meeting.date}
- **Time:** {meeting.time}
- **Location:** {location_info}

**Agenda:**
{agenda}

**Attendees:**
{', '.join(meeting.attendees)}

Please confirm your attendance by replying to this email.
If you cannot attend, please send a delegate and notify the organizer.

Regards,

{meeting.organizer_name}
Project Manager
"""

    return {
        'subject': subject,
        'body': body,
        'to': meeting.attendees,
        'calendar_invite': {
            'start': f"{meeting.date} {meeting.time}",
            'duration': 60,
            'location': meeting.location
        }
    }
```

### 4. 变更订单通知邮件

生成变更订单通知邮件。

```python
@dataclass
class ChangeOrderNotification:
    co_number: str
    project_name: str
    description: str
    amount: float
    schedule_impact: str
    reason: str
    status: str  # 'Pending', 'Approved', 'Rejected'
    sender_name: str
    sender_title: str

def generate_change_order_email(co: ChangeOrderNotification) -> dict:
    """Generate change order notification email."""

    subject = f"Change Order #{co.co_number} - {co.status} - {co.project_name}"

    amount_str = f"${co.amount:,.2f}"
    if co.amount < 0:
        amount_str = f"(${abs(co.amount):,.2f}) Credit"

    body = f"""Dear Project Team,

This email is to notify you of Change Order #{co.co_number} for {co.project_name}.

**Change Order Details:**
- **CO Number:** {co.co_number}
- **Status:** {co.status}
- **Description:** {co.description}

**Financial Impact:**
- **Amount:** {amount_str}

**Schedule Impact:**
- {co.schedule_impact}

**Reason for Change:**
{co.reason}

{"Please review the attached documentation and provide your approval." if co.status == 'Pending' else ""}
{"This change order has been approved. Please proceed accordingly." if co.status == 'Approved' else ""}

If you have any questions, please contact the project team.

Best regards,

{co.sender_name}
{co.sender_title}
"""

    return {
        'subject': subject,
        'body': body,
        'priority': 'high' if co.status == 'Pending' else 'normal',
        'flag': co.status == 'Pending'
    }
```

### 5. 日报邮件

生成每日报告分发邮件。

```python
@dataclass
class DailyReportEmail:
    project_name: str
    report_date: str
    report_number: int
    weather: str
    workforce_total: int
    work_summary: List[str]
    issues: List[str]
    sender_name: str

def generate_daily_report_email(report: DailyReportEmail) -> dict:
    """Generate daily report distribution email."""

    subject = f"Daily Report #{report.report_number} - {report.project_name} - {report.report_date}"

    work_items = "\n".join(f"• {item}" for item in report.work_summary)
    issues_text = "\n".join(f"• {issue}" for issue in report.issues) if report.issues else "None"

    body = f"""Daily Construction Report

**Project:** {report.project_name}
**Date:** {report.report_date}
**Report #:** {report.report_number}

---

**Weather:** {report.weather}
**Total Workforce:** {report.workforce_total} workers on-site

---

**Work Completed:**
{work_items}

---

**Issues/Delays:**
{issues_text}

---

Full report attached. Please contact the site office with any questions.

{report.sender_name}
Site Superintendent
"""

    return {
        'subject': subject,
        'body': body,
        'attachments': [f'Daily_Report_{report.report_number}.pdf']
    }
```

### 6. 延期通知邮件

生成正式的延期通知邮件。

```python
@dataclass
class DelayNotice:
    project_name: str
    contract_number: str
    delay_type: str  # 'Excusable', 'Non-Excusable', 'Compensable'
    cause: str
    affected_activities: List[str]
    original_completion: str
    revised_completion: str
    days_impacted: int
    mitigation_plan: str
    sender_name: str
    sender_title: str

def generate_delay_notice_email(delay: DelayNotice) -> dict:
    """Generate formal delay notice email."""

    subject = f"NOTICE OF DELAY - {delay.project_name} - {delay.days_impacted} Days"

    activities = "\n".join(f"   - {a}" for a in delay.affected_activities)

    body = f"""NOTICE OF DELAY

**Project:** {delay.project_name}
**Contract No:** {delay.contract_number}
**Date:** {datetime.now().strftime('%B %d, %Y')}

---

Dear Owner/Owner's Representative,

In accordance with the contract requirements, this letter serves as formal notice of a delay to the project schedule.

**Delay Classification:** {delay.delay_type}

**Cause of Delay:**
{delay.cause}

**Affected Activities:**
{activities}

**Schedule Impact:**
- Original Completion Date: {delay.original_completion}
- Revised Completion Date: {delay.revised_completion}
- Calendar Days Impacted: {delay.days_impacted}

**Mitigation Plan:**
{delay.mitigation_plan}

We request a meeting to discuss this matter and coordinate recovery efforts. Please contact us at your earliest convenience.

This notice is provided without prejudice to any rights or remedies available under the contract.

Respectfully,

{delay.sender_name}
{delay.sender_title}
"""

    return {
        'subject': subject,
        'body': body,
        'priority': 'high',
        'read_receipt': True,
        'delivery_receipt': True
    }
```

## 邮件发送集成

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class ConstructionEmailSender:
    """Send construction emails via SMTP."""

    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send(self, to: List[str], email_data: dict, from_addr: str = None):
        """Send email with optional attachments."""
        msg = MIMEMultipart()
        msg['From'] = from_addr or self.username
        msg['To'] = ', '.join(to)
        msg['Subject'] = email_data['subject']

        if email_data.get('cc'):
            msg['Cc'] = ', '.join(email_data['cc'])

        if email_data.get('priority') == 'high':
            msg['X-Priority'] = '1'

        msg.attach(MIMEText(email_data['body'], 'plain'))

        # Add attachments
        for attachment_path in email_data.get('attachments', []):
            with open(attachment_path, 'rb') as f:
                part = MIMEApplication(f.read())
                part.add_header('Content-Disposition', 'attachment',
                               filename=attachment_path.split('/')[-1])
                msg.attach(part)

        # Send
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)

            recipients = to + email_data.get('cc', [])
            server.sendmail(msg['From'], recipients, msg.as_string())
```

## 与DDC流程的集成

```python
# Example: Auto-generate RFI response email from RFI log
import pandas as pd

# Load RFI log
rfi_log = pd.read_excel("RFI_Log.xlsx")

# Get pending RFI
pending_rfi = rfi_log[rfi_log['status'] == 'Response Ready'].iloc[0]

# Generate email
rfi = RFIResponse(
    rfi_number=pending_rfi['rfi_number'],
    project_name=pending_rfi['project'],
    subject=pending_rfi['subject'],
    question=pending_rfi['question'],
    response=pending_rfi['response'],
    responder_name='John Smith',
    responder_title='Project Architect',
    attachments=['SK-001.pdf']
)

email_data = generate_rfi_response_email(rfi)
print(f"Subject: {email_data['subject']}")
print(email_data['body'])
```

## 电子邮件模板库

以下是建筑行业常用的电子邮件模板：

| 模板          | 使用场景                |
|----------------|----------------------|
| RFI回复邮件       | 回复信息请求              |
| 提交文件传输邮件     | 发送提交文件以供审核           |
| 会议通知邮件       | 通知相关方（如业主、分包商、安全会议） |
| 变更订单邮件       | 发送变更订单通知及审批请求       |
| 日报邮件         | 分发每日报告             |
| 延期通知邮件       | 发送正式的延期通知           |
| 支付申请邮件       | 提交付款申请             |
| 工作进度通知邮件     | 通知工作进度相关事项           |
| 项目收尾邮件       | 发送项目收尾相关文件           |

## 资源推荐

- **专业电子邮件写作指南**：确保邮件简洁明了、注重行动导向。
- **建筑行业电子邮件最佳实践**：务必在邮件中包含项目名称和参考编号。
- **法律注意事项**：延期通知可能需要遵循合同中的相关条款。