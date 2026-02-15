---
slug: "n8n-daily-report"
display_name: "N8N Daily Report"
description: "使用 n8n 工作流自动化工具来自动化每日施工报告的生成。"
---

# n8n 日报自动化

## 商业案例

日报虽然至关重要，但制作过程却非常耗时。此 n8n 工作流程能够自动从多个来源收集站点数据，并生成格式化的日报。

## 工作流程概述

```
[Site Data Sources] → [n8n Webhook] → [Data Processing] → [Report Generation] → [Distribution]
```

## n8n 工作流程配置

### 1. 触发节点：调度器 + Webhook

```json
{
  "nodes": [
    {
      "name": "Daily Schedule",
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{"field": "cronExpression", "expression": "0 17 * * 1-5"}]
        }
      }
    },
    {
      "name": "Webhook Input",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "httpMethod": "POST",
        "path": "daily-report-data"
      }
    }
  ]
}
```

### 2. 数据收集节点

```json
{
  "nodes": [
    {
      "name": "Get Weather Data",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.openweathermap.org/data/2.5/weather",
        "qs": {
          "lat": "={{$json.site_lat}}",
          "lon": "={{$json.site_lon}}",
          "appid": "={{$env.WEATHER_API_KEY}}"
        }
      }
    },
    {
      "name": "Get Site Photos",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "={{$env.PROCORE_API}}/projects/{{$json.project_id}}/images",
        "authentication": "oAuth2"
      }
    },
    {
      "name": "Get Labor Data",
      "type": "n8n-nodes-base.spreadsheetFile",
      "parameters": {
        "operation": "read",
        "fileFormat": "xlsx"
      }
    }
  ]
}
```

### 3. 数据处理

```json
{
  "name": "Process Report Data",
  "type": "n8n-nodes-base.code",
  "parameters": {
    "jsCode": "const items = $input.all();\n\nconst weather = items[0].json;\nconst photos = items[1].json;\nconst labor = items[2].json;\n\nconst report = {\n  date: new Date().toISOString().split('T')[0],\n  project: $('Webhook Input').first().json.project_name,\n  weather: {\n    condition: weather.weather[0].main,\n    temp_high: Math.round(weather.main.temp_max - 273.15),\n    temp_low: Math.round(weather.main.temp_min - 273.15)\n  },\n  labor_summary: {\n    total_workers: labor.reduce((sum, l) => sum + l.workers, 0),\n    total_hours: labor.reduce((sum, l) => sum + l.hours, 0)\n  },\n  photo_count: photos.length\n};\n\nreturn [{json: report}];"
  }
}
```

### 4. 报告生成

```json
{
  "name": "Generate PDF Report",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "method": "POST",
    "url": "={{$env.PDF_SERVICE_URL}}/generate",
    "body": {
      "template": "daily_report",
      "data": "={{$json}}"
    }
  }
}
```

### 5. 报告分发

```json
{
  "nodes": [
    {
      "name": "Send Email",
      "type": "n8n-nodes-base.emailSend",
      "parameters": {
        "toEmail": "={{$json.distribution_list}}",
        "subject": "Daily Report - {{$json.project}} - {{$json.date}}",
        "attachments": "={{$node['Generate PDF Report'].json.file}}"
      }
    },
    {
      "name": "Upload to SharePoint",
      "type": "n8n-nodes-base.microsoftSharePoint",
      "parameters": {
        "operation": "upload",
        "siteId": "={{$env.SHAREPOINT_SITE}}",
        "folderId": "/Daily Reports/{{$json.date}}"
      }
    }
  ]
}
```

## Python 辅助函数

```python
import requests
from datetime import date

def trigger_daily_report(project_data: dict, webhook_url: str):
    """Trigger n8n daily report workflow."""
    payload = {
        "project_id": project_data['id'],
        "project_name": project_data['name'],
        "site_lat": project_data['latitude'],
        "site_lon": project_data['longitude'],
        "distribution_list": project_data['stakeholder_emails']
    }

    response = requests.post(webhook_url, json=payload)
    return response.status_code == 200


def format_labor_data(labor_entries: list) -> list:
    """Format labor data for n8n processing."""
    formatted = []
    for entry in labor_entries:
        formatted.append({
            'trade': entry['trade'],
            'company': entry['company'],
            'workers': entry['worker_count'],
            'hours': entry['total_hours'],
            'activities': entry.get('activities', [])
        })
    return formatted
```

## 快速入门

1. 将工作流程导入 n8n；
2. 配置环境变量：
   - `WEATHER_API_KEY`
   - `PROCORE_API`
   - `PDF_SERVICE_URL`
   - `SHAREPOINT_SITE`
3. 设置所需的调度时间；
4. 配置电子邮件分发列表。

## 资源
- **n8n 文档**：https://docs.n8n.io
- **DDC 手册**：第 4.2 章 - 工作流程自动化