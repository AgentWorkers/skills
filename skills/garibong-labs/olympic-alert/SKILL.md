---
name: olympic-alert
description: 奥运会赛事通知：在比赛开始前15分钟发送提醒信息，支持赛事日程的添加/删除功能，并提供赛事转播链接。系统已预设2026年米兰冬季奥运会的韩国国家队相关设置。
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    triggers:
      - 올림픽
      - Olympic
      - 동계올림픽
      - 경기 알림
      - 밀라노
---

# Olympic Alert Skill  
（奥运赛事提醒功能）  

该技能会在比赛开始前15分钟发送提醒通知，包含韩国队比赛的默认设置。  

## 所包含的文件  
| 文件 | 说明 |  
|------|------|  
| `SKILL.md` | 本文档 |  
| `scripts/check_olympic.py` | 主脚本（Python 3.6+，仅使用标准库） |  
| `scripts/events.json` | 比赛日程数据（2026年米兰冬季奥运会韩国队的默认设置） |  

## 所需依赖环境  
- Python 3.6+（仅使用标准库，无需额外安装包）  

## 使用方法  
请以技能目录为基准，通过相对路径来执行脚本：  
```bash
SKILL_DIR="<workspace>/skills/olympic-alert"

# 알림 체크 (HEARTBEAT에서 호출)
python3 "$SKILL_DIR/scripts/check_olympic.py"

# 다가오는 경기 목록
python3 "$SKILL_DIR/scripts/check_olympic.py" list

# 경기 추가
python3 "$SKILL_DIR/scripts/check_olympic.py" add "2026-02-15 14:00" "🏒 쇼트트랙 준결승" "최민정"

# 경기 삭제 (이름 패턴 매칭)
python3 "$SKILL_DIR/scripts/check_olympic.py" remove "준결승"
```  

## 设置  
### events.json  
在 `scripts/events.json` 文件中管理比赛日程：  
```json
{
  "country": "Korea",
  "flag": "🇰🇷",
  "links": {
    "네이버 스포츠": "https://m.sports.naver.com/milanocortina2026",
    "치지직": "https://chzzk.naver.com/search?query=올림픽"
  },
  "events": [
    {"time": "2026-02-10 18:00", "name": "🏒 쇼트트랙", "athletes": "최민정"}
  ]
}
```  

### 状态文件  
`~/.config/olympic-alert/state.json` — 用于记录通知发送情况（防止重复通知）  

## HEARTBEAT.md 设置  
（此处可添加与技能运行相关的其他配置信息，例如心跳检测、日志记录等）  
```markdown
## 올림픽 경기 알림 (every heartbeat)
On each heartbeat:
1. Run `python3 <skill_dir>/scripts/check_olympic.py`
2. If output is not "알림 없음" → 사용자에게 알림 전송
```  

## 日程更新  
根据预赛结果调整日程：  
- 如果队伍晋级：使用 `add` 命令添加半决赛/决赛的安排；  
- 如果队伍淘汰：使用 `remove` 命令删除相关比赛记录；  
- 也可以直接编辑 `events.json` 文件。  

## 通知示例  
（此处可展示实际发送的通知内容示例）  
```
🇰🇷 10분 후
🏒 쇼트트랙 여자1500m 결승
👤 최민정 3연속 금 도전

📺 네이버 스포츠 | 치지직
```  

## 适用于其他国家/赛事  
通过修改 `events.json` 文件中的 `country`、`flag`、`links`、`events` 等字段，即可将该技能应用于其他国家或赛事。  

## 问题咨询/反馈  
如需报告错误、提出功能请求或提供反馈，请发送邮件至：  
- Email: contact@garibong.dev  
- 开发者：Garibong Labs（가리봉랩스）