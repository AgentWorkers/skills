---
name: olympic-alert
description: 奥运会赛事通知：在比赛开始前10分钟发送提醒信息，支持赛事日程的添加/删除功能，并提供赛事转播链接。系统已预置2026年米兰冬季奥运会的韩国国家队相关设置。
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
该技能会在奥运会比赛开始前10分钟发送通知，同时包含韩国队的比赛信息作为默认设置。  

## 所包含的文件  
| 文件 | 说明 |  
|------|------|  
| `SKILL.md` | 本文档 |  
| `scripts/check_olympic.py` | 主要脚本（Python 3.6+，仅使用标准库） |  
| `scripts/events.json` | 比赛日程数据（2026年米兰冬奥会韩国队的默认值） |  

## 所需依赖环境  
- Python 3.6+（仅使用标准库，无需额外安装包）  

## 使用方法  
请在技能目录的相对路径下执行该脚本：  
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
（相关设置内容请参考 `HEARTBEAT.md` 文件）  

## 日程更新  
根据预赛结果调整日程：  
- 如果队伍晋级：使用 `add` 命令添加半决赛/决赛的比赛信息；  
- 如果队伍淘汰：使用 `remove` 命令删除相应的比赛记录；  
- 也可以直接编辑 `events.json` 文件。  

## 通知示例  
（通知内容示例请参考 `CODE_BLOCK_3`）  

## 适用于其他国家/赛事  
通过修改 `events.json` 文件中的 `country`、`flag`、`links`、`events` 等字段，即可将该技能应用于其他国家或赛事。  

## 问题咨询/反馈  
如需报告错误、提出功能请求或提供反馈，请发送邮件至：  
- Email: contact@garibong.dev  
- 开发者：Garibong Labs（가리봉랩스）