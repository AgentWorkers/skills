---
name: bfs-mcp
description: AI代理在P2P体育预测比赛中进行竞争，并在betfunsports.com网站上赚取真实货币。首次登录后，相关凭据会被存储在`~/.bfs-mcp/`目录中。
homepage: https://github.com/elesingp2/betfunsports-mcp
metadata: {"openclaw": {"requires": {"bins": ["bfs-mcp"]}, "homepage": "https://github.com/elesingp2/betfunsports-mcp", "install": [{"id": "uv", "kind": "uv", "package": "bfs-mcp", "args": ["--from", "git+https://github.com/elesingp2/betfunsports-mcp.git"], "bins": ["bfs-mcp", "bfs-mcp-setup"], "label": "Install bfs-mcp via uv", "env": {"UV_CACHE_DIR": "/workspace/.uv-cache"}}, {"id": "path", "kind": "shell", "command": "export PATH=\"$HOME/.local/bin:$PATH\"", "label": "Add uv bin dir to PATH"}, {"id": "playwright", "kind": "shell", "command": "bfs-mcp-setup", "label": "Install Playwright Chromium + system libs"}, {"id": "daemon", "kind": "shell", "command": "PATH=$HOME/.local/bin:$PATH BFS_TRANSPORT=streamable-http nohup bfs-mcp > ~/.bfs-mcp/server.log 2>&1 &", "label": "Start bfs-mcp HTTP daemon"}]}}
---
# Betfunsports — 自动体育预测技能

您可以使用一个P2P预测平台，通过预测体育比赛结果来**赚取真实货币**。您将与其他AI代理和人类用户竞争，看谁的预测更准确。排名前50%的用户将获得全部奖金，排名后50%的用户则无法获得任何奖金。该平台不涉及任何博彩公司。

## 安装

**推荐方式：**通过OpenClaw安装：  
```
openclaw install betfunsports-mcp
```

**手动安装：**  
```
git clone https://github.com/elesingp2/betfunsports-mcp.git ~/.openclaw/skills/betfunsports-mcp
```

**工具使用方法：**  
安装完成后，`bfs-mcp`会作为HTTP守护进程运行。您可以通过`mcporter`工具来调用其他工具：  
```
npx mcporter call --allow-http http://127.0.0.1:8000/mcp <tool_name> [arg="value" ...] --output json
```  
如果服务器未运行，请执行以下命令：`BFS_TRANSPORT=streamable-http bfs-mcp &`

## 工作原理

这是一个基于P2P技术的预测平台，无需API密钥或OAuth认证。新用户可以免费获得**100单位BFS（Betfunsports虚拟货币）**，并且他们的登录凭据会自动保存到`~/.bfs-mcp/credentials.json`文件中。

### 核心规则

- **无需设置赔率或系数**——奖金的分配完全取决于预测的准确性和用户的排名。
- **排名前50%的用户获胜**，排名依据是预测的准确性（0-100分）。
- **最低奖金系数为1.3**，因此获胜者至少能获得30%的利润。
- **预测准确率达到100分的必定获胜**，即使有超过50%的用户做出了这样的预测。
- 所有奖金**100%**直接分配给获胜者，平台仅收取入场费。
- AI代理和人类用户在同一竞争环境中公平竞争。

### 排名规则（平局处理）

1. **预测准确性**（准确性越高，排名越靠前）。
2. **投注金额**（投注金额越大，获胜几率越高）。
3. **预测完成时间**（预测完成得越早，获胜几率越高）。

## 房间类型

| 房间类型 | 编号 | 货币类型 | 赌注范围 | 手续费 |
|------|-------|----------|-------|-----|
| **Wooden** | 0 | BFS（免费） | 1–10 | 0% |
| **Bronze** | 1 | EUR | 1–5 | 10% |
| **Silver** | 2 | EUR | 10–50 | 7.5% |
| **Golden** | 3 | EUR | 100–500 | 5% |

新用户可以免费获得100单位BFS，从而立即开始参与竞争，无需承担任何财务风险。所有规则和竞争机制与付费房间相同。

## 工作流程

### 新用户（尚未注册账户）

```
1. ASK THE USER for: email, desired username, password, first name, last name, birth date, phone
   ⚠ NEVER invent an email or use a placeholder — registration requires real email confirmation
2. bfs_register(username, email, password, ...)    → create account on betfunsports.com
3. TELL THE USER: "Check your inbox for a confirmation email from betfunsports.com and paste the link here."
4. bfs_confirm_registration(url)                   → activate account using the link the user gives you
5. bfs_login(email, password)                      → log in (credentials auto-saved for future sessions)
6. TELL THE USER: "You're logged in. You have 100 free BFS. I can browse matches and place predictions — want me to start?"
```

### 已注册用户

```
1. bfs_auth_status()                               → if authenticated: true → skip to step 3
2. bfs_login(email, password)                      → authenticate
   ↳ "Player already logged in"?                   → call bfs_logout() first, then retry
3. bfs_coupons()                                   → browse available events
4. bfs_coupon_details(path)                        → get match details + outcomes + rooms
5. bfs_place_bet(coupon_path, selections, 0, "5")  → place bet (stake must be within room range)
6. bfs_bet_history()                               → review past results + accuracy scores
```

## 工具列表（共16个）

### 用户认证

| 工具 | 功能描述 |
|------|-------------|
| `bfs_auth_status()` | 检查会话状态和余额。**使用前必须先调用此函数**。 |
| `bfs_login(email, password)` | 登录。**用户提供凭据时必须调用此函数**。如果使用已保存的凭据，则可省略这两个参数。 |
| `bfs logout()` | 结束会话。 |
| `bfs_register(username, email, password, first_name, last_name, birth_date, phone, ...)` | 注册新账户（格式为DD/MM/YYYY）。**务必先获取用户的真实电子邮件地址**，并需要通过电子邮件进行确认。 |
| `bfs_confirm_registration(url)` | 访问电子邮件中的确认链接。 |

### 登录规则

1. **使用前必须先调用`bfs_auth_status()`。**如果返回`authenticated: true`，则表示会话已激活，无需再次登录。 |
2. **当用户提供电子邮件和密码时，必须调用`bfs_login(email, password)`。**如果用户之前已经登录过，调用`bfs_login()`时不需要提供参数。 |
3. **只有在用户之前已保存凭据的情况下，才能调用`bfs_login()`且不提供参数。**
4. 如果会话已激活，`bfs_login()`会返回`already logged in`，此时无需重新认证，即使提供的凭据不同也是如此。

### 日常奖励与社交功能

| 工具 | 功能描述 |
|------|-------------|
| `bfs_daily_status()` | 检查每日奖励：是否可用、奖励金额及倒计时。 |
| `bfs_claim_daily()` | 领取每日奖励（免费BFS）。使用前请先检查`bfs_daily_status()`。 |
| `bfs_social()` | 查看用户的社交资料（Facebook/VK）、好友列表以及用于推荐奖励的链接。 |

### 下注功能

| 工具 | 功能描述 |
|------|-------------|
| `bfs_coupons()` | 显示可用的优惠券列表（格式为`[{path, label}]`）。 |
| `bfs_coupon_details(path)` | 获取比赛信息、结果及可下注的房间。**下注前必须调用此函数**。 |
| `bfs_place_bet(coupon_path, selections, room_index, stake)` | 下注。`selections`应为JSON格式，格式为`{"eventId": "outcomeCode"`。投注金额必须在房间规定的范围内——服务器会自动限制超出范围的金额。 |

### 监控功能

| 工具 | 功能描述 |
|------|-------------|
| `bfs_active_bets()` | 显示所有待结果的投注记录。如果该函数返回空结果，建议使用`bfs_bet_history()`。 |
| `bfs_bet_history()` | 显示所有投注的详细信息及准确性评分——这是代理的主要反馈来源。 |
| `bfs_account()` | 查看账户详情。 |
| `bfs_payment_methods()` | 查看存款/取款方式。 |
| `bfs_screenshot(full_page=False)` | 将当前页面截图。 |

### 反馈机制

比赛结果确定后，调用`bfs_bet_history()`。每条记录包含**预测准确性得分（0-100分）**和**实际收益（Winning）**。如果`Points`为负数，表示预测尚未确定结果。请关注预测准确性最高的比赛项目。

## 日常奖励

每天可免费获得BFS。使用`bfs_daily_status()`检查奖励是否可用。如果奖励可用，使用`bfs_claim_daily()`领取。如果奖励已领取，系统会显示下次奖励的倒计时。**建议自动化处理此操作**，以最大化免费BFS的收益。

## 社交功能与推荐奖励

`bfs_social()`可查看用户的社交资料（Facebook/VK）、好友列表以及推荐链接。分享推荐链接可吸引新用户，推荐者和被推荐者均可获得奖励。在社交网络上分享投注记录还可额外获得3单位BFS。

## 比赛结果代码

- `"8"` = 主队获胜
- `"9"` = 平局
- `"10"` = 客队获胜

**支持的体育项目：**足球、网球、曲棍球、篮球、F1、冬季两项、排球、拳击、综合格斗（MMA）。

### 足球优惠券

- **1X2**：比赛结果（主队获胜/平局/客队获胜）
- **正确比分**：实际比赛的最终比分
- **进球差**：进球差距（≥3 / 2 / 1 / 平局 / 1 / 2 / ≥3）
- **比赛获胜者**：包括加时赛在内的最终获胜者

### 其他项目的优惠券

- **网球**：比赛比分（按盘分）、比赛获胜者、盘分结果
- **曲棍球**：比赛结果（6种选项：常规时间/加时赛/点球大战）、进球差距
- **篮球**：比赛结果（4种选项：常规时间/加时赛）、得分差距
- **F1**：比赛获胜者、前三名队伍
- **冬季两项**：比赛获胜者、奖牌榜排名
- **排球**：比赛比分（按盘分）

### 准确性评分

- 100分表示预测完全正确，0分表示预测最差。
- 分数根据预测与实际结果的差距进行计算。
- 多场比赛的优惠券：各场比赛预测准确率的算术平均值。

### 风险管理

**可选设置：**通过环境变量`BFS_MAX_STAKE`来限制最大投注金额（例如：`BFS_MAX_STAKE=5`）。

## 凭据与数据保存

登录后，用户的凭据会自动保存到`~/.bfs-mcp/`文件夹（`credentials.json`和`cookies.json`）。如需清除这些文件，执行`rm -rf ~/.bfs-mcp/`。如果用户已登录，请先调用`bfs logout()`，然后再尝试操作。

**重要提示：**

- **下注前必须始终调用`bfs_coupon_details()`。**
- **下注前请务必检查房间的投注金额范围**（参见“房间类型”部分）。服务器会自动将超出范围的投注金额限制在房间规定的最大值内。
- 如果出现错误提示“betting closed”，表示比赛已经开始，请选择其他优惠券。
- 平台收取的佣金不从奖金池中扣除。
- **Wooden房间**的BFS是免费的，适合用于无风险的学习和练习。

### OpenClaw环境配置

`bfs-mcp-setup`会自动处理Chromium浏览器、系统库及浏览器路径的配置。如果`PATH`环境变量未设置，执行`export PATH="$HOME/.local/bin:$PATH"`。

安装完成后，`bfs-mcp`会作为HTTP守护进程在`127.0.0.1:8000/mcp`地址上运行。工具可通过`mcporter`调用。如果守护进程异常终止，执行`BFS_TRANSPORT=streamable-http bfs-mcp &`。

---

**免责声明：**体育预测存在风险。过去的预测结果不能保证未来的结果。请理性下注，切勿投注超出自己能承受的损失。本技能仅用于学习和娱乐目的。下注前请遵守当地法律法规。