---
name: token-management
description: "集中式 API 令牌管理的工作流程如下：  
1. 将 API 令牌存储在 `.env` 文件中，并为每个令牌设置过期日期。  
2. 使用脚本测试令牌的权限。  
3. 在 `connections/` 目录中记录令牌的相关信息。  
4. 设置日历提醒，以便在令牌过期前自动进行更新。  
5. 该流程可防止用户重复输入凭据，确保令牌的安全性，并实时监控令牌的过期状态。"
type: public
version: 1.0.1
status: published
dependencies:
  - python3
  - requests
  - gog (for calendar reminders)
author: nonlinear
license: MIT
---

# 令牌管理

**发布地址：** https://clawhub.com/skills/token-management

**目的：** 集中管理 API 令牌——包括存储、测试、文档记录以及过期监控。

**触发操作：**
- “添加令牌 X”
- “为 Y 保存 API 密钥”
- “需要令牌 Z”

---

## 🔴 重要规则

**在请求令牌之前，务必先检查 `~/Documents/life/.env` 文件！**

---

## 工作流程

### 收到新令牌时：
1. **执行 Git 提交（如适用）**
   - 如果 `.env` 文件位于 Git 仓库中：
     ```
     cd ~/Documents/life
     git add -A
     git commit -m "在更新令牌名称之前"
     ```
   - 安全第一！

2. **查询令牌的过期日期**
   - “这个令牌什么时候过期？”
   - 格式：YYYY-MM-DD 或 “1 年” / “永不”

3. **将令牌信息存储到 `.env` 文件中**
   - **存储位置：** `~/Documents/life/.env`
   - 格式：`服务名称_令牌=值  # 过期日期：YYYY-MM-DD`
   - 例如：`WILEY_JIRA_TOKEN=abc123  # 过期日期：2027-02-12`

4. **创建日历提醒（如果令牌即将过期）**
   - **提醒时间：** 令牌到期前 7 天
   - **提醒内容：** “⚠️ [服务] API 令牌即将过期（7 天后）”
   - **提醒类型：** 全天事件
   - **执行命令：**
     ```bash
     gog calendar create primary \
       --summary "⚠️ Renew SERVICE token" \
       --from "YYYY-MM-DDT00:00:00-05:00" \
       --to "YYYY-MM-DDT23:59:59-05:00" \
       --description "Token expires YYYY-MM-DD. Renew at: [RENEWAL_URL]"
     ```

5. **测试令牌的权限**
   - 运行测试脚本以了解该令牌的功能
   - **使用模板：** 根据具体服务进行修改
   - 将测试结果记录在 `connections/` 文件中
   - **示例：**
     ```python
     # Test Jira token
     import requests, base64
     
     TOKEN = "..."
     EMAIL = "user@example.com"
     auth = base64.b64encode(f"{EMAIL}:{TOKEN}".encode()).decode()
     
     tests = [
         ("Get user", "GET", "/rest/api/3/myself"),
         ("List projects", "GET", "/rest/api/3/project"),
         ("Search issues", "GET", "/rest/api/3/search", {"jql": "assignee=currentUser()"}),
     ]
     
     for name, method, endpoint, *params in tests:
         r = requests.get(f"https://DOMAIN{endpoint}", 
                         headers={'Authorization': f'Basic {auth}'},
                         params=params[0] if params else None)
         print(f"{'✅' if r.ok else '❌'} {name}: {r.status_code}")
     ```

6. **在文档中记录令牌信息**
   - 在 `~/Documents/life/connections/` 目录下创建或更新相应的文件（例如 `figma.md`）
   - **包含内容：**
     - 令牌的权限（读/写/范围）
     - **获取时间：** YYYY-MM-DD
     - **过期日期：** YYYY-MM-DD
     - **续期链接：** 获取新令牌的 URL
     - 使用方法（代码示例）
   - 链接到 `.env` 文件中的变量名
   - **示例：**
     ```markdown
     ## Token Info
     - **Obtained:** 2026-02-12
     - **Expires:** 2027-02-12
     - **Renew at:** https://id.atlassian.com/manage-profile/security/api-tokens
     - **Scope:** read-write
     - **Variable:** `WILEY_JIRA_TOKEN` (~/Documents/life/.env)
     ```

7. **更新令牌索引**
   - 在本文档（`SKILL.md`）中维护令牌列表

### 需要 API 访问时：
1. **务必先检查 `.env` 文件：`~/Documents/life/.env`
2. **如果找不到令牌信息：** 查看 `connections/` 目录中的设置说明
3. **如果仍然找不到令牌：** 向 Nicholas 请求新的令牌

---

## 令牌索引

**存储位置：** `~/Documents/life/.env`

**示例令牌：**

| 服务 | 变量名 | 权限范围 | 过期日期 | 相关文档文件 |
|---------|----------|-------|---------|----------------|
| Figma | `FIGMA_TOKEN` | 读/写 | YYYY-MM-DD | [figma.md](~/Documents/life/connections/figma.md) |
| Jira | `JIRA_TOKEN` | 读/写 | YYYY-MM-DD | [jira.md](~/Documents/life/connections/jira.md) |
| Slack | `SLACK_TOKEN` | 机器人权限 | 永不过期 | [slack.md](~/Documents/life/connections/slack.md) |
| GitHub | `GITHUB_TOKEN` | 仓库、Gist 访问权限 | YYYY-MM-DD | [github.md](~/Documents/life/connections/github.md) |

**你的令牌列表：** 请在此部分维护自己的令牌列表（本地副本）。

---

## 命令操作

### 添加令牌
```bash
# Append to .env (skill will automate)
echo "SERVICE_TOKEN=value" >> ~/Documents/life/.env
```

### 检查令牌是否存在
```bash
grep SERVICE_TOKEN ~/Documents/life/.env
```

### 列出所有令牌
```bash
cat ~/Documents/life/.env
```

---

## `.env` 文件的存储位置

**存储位置说明：**
- ✅ 位于 `~/Documents/life/.env`，属于项目的核心配置文件
- ✅ 可在团队成员之间共享
- ✅ 在工作区被清除后仍可保留
- ✅ 与 `connections/` 目录中的配置保持一致
- ✅ 与 OpenClaw 工作区无关

**Python 使用方法：**
```python
from dotenv import load_dotenv
load_dotenv('~/Documents/life/.env')  # Or absolute path
```

**Shell 使用方法：**
```bash
source ~/Documents/life/.env
echo $YOUR_TOKEN_NAME
```

---

**创建日期：** 2026-02-12  
**更新日期：** 2026-02-13（为发布版本进行了内容整理）