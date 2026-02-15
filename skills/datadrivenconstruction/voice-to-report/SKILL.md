---
slug: "voice-to-report"
display_name: "Voice To Report"
description: "将语音录音转换为结构化的施工报告。现场工作人员进行语音录制，AI系统负责转录和格式化。该功能支持生成每日报告、安全观察记录以及进度更新报告。"
---

# 语音转报告功能

## 概述

现场工作人员更喜欢通过语音交流而非打字。该功能利用语音转文本技术以及大型语言模型（LLM）将语音记录转换为结构化的施工报告。

## 为什么选择语音？

| 打字 | 语音 |
|--------|-------|
| 在移动设备上速度较慢 | 速度快3倍 |
| 需要集中注意力 | 可实现免提操作 |
| 在寒冷或雨天使用受限 | 可在任何地方使用 |
| 语言形式较为正式 | 表达更自然 |
| 适合发送简短信息 | 适合发送详细描述 |

## 架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    VOICE TO REPORT PIPELINE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  🎤 Voice      →    📝 Transcribe    →    🤖 Structure    →    📊 Report │
│  Recording         Whisper API           GPT-4o               Formatted  │
│                                                                  │
│  "We finished      "We finished         {                    Daily Report │
│   the foundation    the foundation       "activity":         ──────────── │
│   pour today,       pour today,          "foundation",       Foundation   │
│   about 500         about 500            "quantity": 500,    pour: 500m³  │
│   cubic meters"     cubic meters"        "unit": "m³"        Complete ✓   │
│                                          }                               │
└─────────────────────────────────────────────────────────────────┘
```

## 快速入门

```python
from openai import OpenAI
import json

client = OpenAI()

def voice_to_report(audio_path: str, report_type: str = "daily") -> dict:
    """Convert voice recording to structured report"""

    # Step 1: Transcribe audio
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="en"
        )

    # Step 2: Structure with LLM
    schema = get_report_schema(report_type)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": f"""You are a construction report assistant.
                Convert the voice transcript into a structured report.
                Extract all relevant information and format as JSON.

                Report type: {report_type}
                Schema: {json.dumps(schema, indent=2)}

                Rules:
                - Extract quantities with units
                - Identify activities and locations
                - Note any issues or concerns
                - Capture weather if mentioned
                - List workers/trades if mentioned
                """
            },
            {
                "role": "user",
                "content": f"Transcript:\n{transcript.text}"
            }
        ],
        response_format={"type": "json_object"}
    )

    return {
        "transcript": transcript.text,
        "structured_report": json.loads(response.choices[0].message.content)
    }
```

## 报告模板

### 日报模板

```python
daily_report_schema = {
    "date": "YYYY-MM-DD",
    "project": "string",
    "weather": {
        "conditions": "string",
        "temperature": "number",
        "impact": "none|minor|major"
    },
    "workforce": [
        {
            "trade": "string",
            "count": "number",
            "hours": "number"
        }
    ],
    "activities": [
        {
            "description": "string",
            "location": "string",
            "quantity": "number",
            "unit": "string",
            "status": "in_progress|completed|delayed"
        }
    ],
    "equipment": [
        {
            "type": "string",
            "hours": "number"
        }
    ],
    "issues": [
        {
            "description": "string",
            "severity": "low|medium|high",
            "action_taken": "string"
        }
    ],
    "notes": "string"
}
```

### 安全观察模板

```python
safety_schema = {
    "date": "YYYY-MM-DD",
    "time": "HH:MM",
    "location": "string",
    "observer": "string",
    "observation_type": "positive|concern|incident",
    "description": "string",
    "people_involved": ["list of names/roles"],
    "immediate_action": "string",
    "follow_up_required": "boolean",
    "photos_attached": "boolean"
}
```

### 进度更新模板

```python
progress_schema = {
    "date": "YYYY-MM-DD",
    "area": "string",
    "activity": "string",
    "planned_quantity": "number",
    "actual_quantity": "number",
    "unit": "string",
    "percent_complete": "number",
    "on_schedule": "boolean",
    "variance_reason": "string or null",
    "next_steps": "string"
}
```

## n8n工作流程

```json
{
  "workflow": "Voice to Report",
  "nodes": [
    {
      "name": "Telegram Trigger",
      "type": "Telegram",
      "event": "voice_message"
    },
    {
      "name": "Download Voice",
      "type": "Telegram",
      "action": "getFile"
    },
    {
      "name": "Transcribe",
      "type": "OpenAI",
      "operation": "transcribe",
      "model": "whisper-1"
    },
    {
      "name": "Detect Report Type",
      "type": "OpenAI",
      "prompt": "Classify: daily_report, safety, progress, issue"
    },
    {
      "name": "Structure Report",
      "type": "OpenAI",
      "operation": "chat",
      "model": "gpt-4o"
    },
    {
      "name": "Save to Database",
      "type": "PostgreSQL"
    },
    {
      "name": "Confirm to User",
      "type": "Telegram",
      "action": "sendMessage"
    },
    {
      "name": "Generate PDF",
      "type": "HTTP Request",
      "url": "pdf-service/generate"
    }
  ]
}
```

## 多语言支持

```python
def transcribe_multilingual(audio_path: str) -> dict:
    """Transcribe in any language, output in English"""

    with open(audio_path, "rb") as audio_file:
        # Detect language automatically
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
            # language parameter omitted for auto-detection
        )

    # Translate to English if needed
    if not is_english(transcript.text):
        translation = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Translate to English, preserve construction terminology."},
                {"role": "user", "content": transcript.text}
            ]
        )
        english_text = translation.choices[0].message.content
    else:
        english_text = transcript.text

    return {
        "original": transcript.text,
        "english": english_text
    }
```

## 移动应用集成

```python
# Example: Flutter/React Native integration

# Send voice to API
async def upload_voice_report(audio_bytes, project_id):
    response = await api.post(
        "/voice-report",
        files={"audio": audio_bytes},
        data={
            "project_id": project_id,
            "report_type": "daily"
        }
    )
    return response.json()

# Response includes:
# - transcript
# - structured_report
# - report_id
# - pdf_url (if generated)
```

## 成本优化

```python
# Use local Whisper for high volume
import whisper

model = whisper.load_model("base")  # or "small", "medium", "large"

def transcribe_local(audio_path: str) -> str:
    """Transcribe locally to save API costs"""
    result = model.transcribe(audio_path)
    return result["text"]

# Cost comparison (per hour of audio):
# - OpenAI Whisper API: $0.36
# - Local Whisper (base): $0 (compute only)
# - Local Whisper (large): $0 (compute only, slower)
```

## 需求

```bash
pip install openai whisper python-telegram-bot
```

## 资源

- OpenAI Whisper: https://platform.openai.com/docs/guides/speech-to-text
- Local Whisper: https://github.com/openai/whisper
- n8n语音处理服务: https://docs.n8n.io/integrations/