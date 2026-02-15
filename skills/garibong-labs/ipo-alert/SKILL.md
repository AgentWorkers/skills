---
name: ipo-alert
description: 韩国公募股申购/新上市日程通知：数据收集来自38.co.kr，提供D-1日（截止日前一天）的通知以及每周的汇总信息。
metadata:
  openclaw:
    requires:
      bins: ["python3", "curl"]
    triggers:
      - 공모주
      - IPO
      - 청약
      - 상장
      - 38.co.kr
---

# IPO Alert Skill

该技能用于监控38.co.kr网站上的新股申购信息和上市公告，并在相关事件发生时发送通知。

## 包含的文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 本文档 |
| `check_ipo.py` | 主脚本（Python 3.6+，仅使用标准库） |

## 数据来源
- 新股申购信息：https://www.38.co.kr/html/fund/index.htm?o=k
- 新股上市信息：https://www.38.co.kr/html/fund/index.htm?o=nw

## 所需依赖
- Python 3.6+（仅使用标准库，无需额外安装包）
- `curl`（用于从38.co.kr获取数据）

## 安装后的配置步骤

1. 创建状态文件目录：`mkdir -p ~/.config/ipo-alert`
2. 将该脚本添加到Cron作业中，或将其配置到HEARTBEAT.md文件中

## 脚本执行方式

请在技能目录（skill directory）中，使用相对路径来执行该脚本：

```bash
# 스킬 경로 변수 (설치 위치에 맞게)
SKILL_DIR="<workspace>/skills/ipo-alert"

# 일일 체크 (청약 D-1, 당일 알림)
python3 "$SKILL_DIR/check_ipo.py" daily

# 주간 요약 (다음주 일정)
python3 "$SKILL_DIR/check_ipo.py" weekly

# 현재 일정 확인 (테스트용)
python3 "$SKILL_DIR/check_ipo.py" list
```

## 通知规则

### 每日通知
- 新股申购开始 **前一天** (D-1)："⏰ [明天开始申购]"
- 新股申购开始 **当天** (D-day)："🚀 [今天开始申购]"
- 新股上市 **前一天**："⏰ [明天上市]"
- 新股上市 **当天**："🎉 [今天上市]"

### 每周汇总
- 每周日晚上执行
- 显示下周的申购/上市计划列表

## 状态文件
`~/.config/ipo-alert/state.json` - 用于记录已发送通知的股票信息（防止重复通知）

## HEARTBEAT.md配置示例

```markdown
## 공모주 알림 (every heartbeat)
On each heartbeat:
1. Run `python3 <skill_dir>/check_ipo.py daily`
2. If output contains alerts (not "알림 없음") → 사용자에게 알림 전송
```

## Cron作业设置（每周汇总）

每周日晚上7点执行，显示下周的申购/上市计划：
```json
{
  "schedule": { "kind": "cron", "expr": "0 19 * * 0", "tz": "Asia/Seoul" },
  "payload": { "kind": "agentTurn", "message": "공모주 주간 요약 발송해줘." }
}
```

## 通知示例

### 每日通知示例
```
⏰ [내일 청약 시작]
📋 [카나프테라퓨틱스](https://www.38.co.kr/html/fund/?o=v&no=2269)
   청약: 03/05(목)~06(금)
   공모가: 16,000~20,000
   주간사: 한국투자증권
```

### 每周汇总示例
```
📅 다음주 공모주 일정 (03/03 ~ 03/07)

【청약 일정】
📋 [카나프테라퓨틱스](https://www.38.co.kr/html/fund/?o=v&no=2269)
   청약: 03/05(목)~06(금)
   공모가: 16,000~20,000
   주간사: 한국투자증권

【신규상장】
🔔 [케이뱅크](https://www.38.co.kr/html/fund/?o=v&no=2271)
   상장일: 03/05(수)
   공모가: 8,300~9,500
```

## 许可证
MIT许可证

## 问题咨询 / 反馈

如需报告错误、提出功能请求或提供反馈，请发送邮件至：
- Email: contact@garibong.dev
- 开发者：Garibong Labs（Garibong Labs）