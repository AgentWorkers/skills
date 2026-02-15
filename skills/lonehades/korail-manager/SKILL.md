```markdown
---
name: korail-manager
version: 1.1.4
description: “Korail（KTX）和SRT票务自动化工具。支持搜索、预订票务，并可接收Telegram和Slack通知。支持英语和韩语界面。”
tools:
  # ── KTX ──
  - name: korail_search
    description: 在两个车站之间搜索KTX列车。
    parameters:
      type: object
      properties:
        dep: { type: string, description: "出发站（例如：首尔, 大田）"
        arr: { type: string, description: "到达站（例如：釜山, 东大邱）"
        date: { type: string, description: "YYYYMMDD格式（默认：今天）"
        time: { type: string, description: "HHMMSS格式（默认：当前时间）"
      }
      required: [dep, arr]
    command: ["python3", "scripts/search.py"]
  - name: korail_watch
    description: 监控KTX列车的剩余座位并自动预订。预订成功后通过Telegram/Slack发送通知。
    parameters:
      type: object
      properties:
        dep: { type: string, description: "出发站"
        arr: { type: string, description: "到达站"
        date: { type: string, description: "YYYYMMDD"
        start_time: { type: number, description: "开始时间（0-23）"
        end_time: { type: number, description: "结束时间（0-23）"
        interval: { type: number, description: "检查间隔（秒，默认：300）"
      }
      required: [dep, arr, date, start_time, end_time]
    command: ["python3", "scripts/watch.py"]
  - name: korail_cancel
    description: 取消KTX预订。如果指定了`--date`参数，仅取消该日期的预订。
    parameters:
      type: object
      properties:
        date: { type: string, description: "要取消的日期（YYYYMMDD）。如果省略，则取消所有预订。"
    command: ["python3", "scripts/cancel.py"]
  # ── SRT ──
  - name: srt_search
    description: 在两个车站之间搜索SRT列车。
    parameters:
      type: object
      properties:
        dep: { type: string, description: "出发站（例如：水西, 五松, 大田）"
        arr: { type: string, description: "到达站（例如：釜山, 大田, 东大邱）"
        date: { type: string, description: "YYYYMMDD格式（默认：今天）"
        time: { type: string, description: "HHMMSS格式（默认：当前时间）"
      }
      required: [dep, arr]
    command: ["python3", "scripts/srt_search.py"]
  - name: srt_watch
    description: 监控SRT列车的剩余座位并自动预订。预订成功后通过Telegram/Slack发送通知。
    parameters:
      type: object
      properties:
        dep: { type: string, description: "出发站"
        arr: { type: string, description: "到达站"
        date: { type: string, description: "YYYYMMDD"
        start_time: { type: number, description: "开始时间（0-23）"
        end_time: { type: number, description: "结束时间（0-23）"
        interval: { type: number, description: "检查间隔（秒，默认：300）"
      }
      required: [dep, arr, date, start_time, end_time]
    command: ["python3", "scripts/srt_watch.py"]
  - name: srt_cancel
    description: 取消SRT预订。如果指定了`--date`参数，仅取消该日期的预订。
    parameters:
      type: object
      properties:
        date: { type: string, description: "要取消的日期（YYYYMMDD）。如果省略，则取消所有预订。"
    command: ["python3", "scripts/cancel_srt.py"]
  dependencies:
    python:
      - requests
      - pycryptodome
      - python-dotenv
      - six
  browserActions:
    - label: "KTX座位搜索"
    prompt: "korail_search --dep '首尔' --arr '釜山'"
    - label: "KTX剩余座位监控及预订"
    prompt: "korail_watch --dep '釜山' --arr '首尔' --date '20260210' --start-time 9 --end-time 18"
    - label: "KTX预订取消"
    prompt: "korail_cancel"
    - label: "SRT座位搜索"
    prompt: "srt_search --dep '水西' --arr '大田'"
    - label: "SRT剩余座位监控及预订"
    prompt: "srt_watch --dep '水西' --arr '大田' --date '20260210' --start-time 9 --end-time 18"
    - label: "SRT预订取消"
    prompt: "srt_cancel"
---
```