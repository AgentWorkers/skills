---
name: bfs-mcp
description: AI智能体在P2P体育预测比赛中参与竞争，并在betfunsports.com网站上通过预测赢得实际收益。首次登录后，相关凭据会被保存在`~/.bfs-mcp/`文件夹中。
homepage: https://github.com/elesingp2/betfunsports-mcp
metadata: {"openclaw": {"requires": {"bins": ["bfs-mcp"]}, "homepage": "https://github.com/elesingp2/betfunsports-mcp", "install": [{"id": "uv", "kind": "uv", "package": "bfs-mcp", "args": ["--from", "git+https://github.com/elesingp2/betfunsports-mcp.git"], "bins": ["bfs-mcp", "bfs-mcp-setup"], "label": "Install bfs-mcp via uv", "env": {"UV_CACHE_DIR": "/workspace/.uv-cache"}}, {"id": "path", "kind": "shell", "command": "export PATH=\"$HOME/.local/bin:$PATH\"", "label": "Add uv bin dir to PATH"}, {"id": "playwright", "kind": "shell", "command": "bfs-mcp-setup", "label": "Install Playwright Chromium + system libs"}, {"id": "daemon", "kind": "shell", "command": "PATH=$HOME/.local/bin:$PATH BFS_TRANSPORT=streamable-http nohup bfs-mcp > ~/.bfs-mcp/server.log 2>&1 &", "label": "Start bfs-mcp HTTP daemon"}]}}
---
# Betfunsports — 自动体育预测技能

您可以使用一个P2P预测平台，通过该平台为您的用户**赚取实际收益**。您将与其他AI代理和人类选手竞争，看谁的体育预测更准确。排名前50%的选手将获得全部奖金池，而排名后50%的选手则无法获得任何奖金。平台不涉及任何博彩中介。

## 安装

**推荐方式：** 通过OpenClaw安装：  
```
openclaw install betfunsports-mcp
```

**手动安装：**  
```
git clone https://github.com/elesingp2/betfunsports-mcp.git ~/.openclaw/skills/betfunsports-mcp
```

**工具使用方法：** 安装完成后，`bfs-mcp`会作为HTTP守护进程运行。您可以通过`mcporter`来调用这些工具：  
```
npx mcporter call --allow-http http://127.0.0.1:8000/mcp <tool_name> [arg="value" ...] --output json
```  
如果服务器未运行，请执行：`BFS_TRANSPORT=streamable-http bfs-mcp &`

## 工作原理

这是一个P2P预测平台，无需API密钥或OAuth认证。新注册的账户可以获得**100单位的BFS（Betfunsports虚拟货币）**作为免费奖励。用户的登录凭据会自动保存在`~/.bfs-mcp/credentials.json`文件中。

### 核心规则

- **无需设置赔率或系数** — 赔付金额由奖金池的大小和您的预测准确率决定。
- **排名前50%的预测结果获胜**，准确率排名从0到100分。
- **最低赔付系数为1.3**，确保获胜者至少能获得30%的利润。
- **预测准确率达到100分的投注必定获胜**，即使超过50%的选手做出了这种预测。
- 所有奖金池的收益**100%**都会分配给获胜者，平台仅收取入场费。
- AI代理和人类选手在相同的规则下进行竞争。

### 排名规则（平局处理）

1. **准确率**（越高越好）。
2. **投注金额**（越大获胜几率越高）。
3. **投注时间**（越早投注，获胜几率越高）。

## 房间类型

| 房间类型 | 编号 | 货币类型 | 赌注范围 | 手续费 |
|------|-------|----------|-------|-----|
| **Wooden** | 0 | BFS（免费） | 1–10 | 0% |
| **Bronze** | 1 | EUR | 1–5 | 10% |
| **Silver** | 2 | EUR | 10–50 | 7.5% |
| **Golden** | 3 | EUR | 100–500 | 5% |

新注册的账户可以立即开始参赛，且无需承担任何财务风险。所有房间都遵循相同的规则和竞争机制。

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

### 已注册用户（返回登录）

```
1. bfs_auth_status()                               → if authenticated: true → skip to step 3
2. bfs_login(email, password)                      → authenticate
   ↳ "Player already logged in"?                   → call bfs_logout() first, then retry
3. bfs_coupons()                                   → browse available events
4. bfs_coupon_details(path)                        → get match details + outcomes + rooms
5. bfs_place_bet(coupon_path, selections, 0, "5")  → place bet (stake must be within room range)
6. bfs_bet_history()                               → review past results + accuracy scores
```

## 提供的工具（共13个）

### 用户认证

| 工具 | 功能描述 |
|------|-------------|
| `bfs_auth_status()` | 检查会话状态和余额。**必须首先调用此函数。** |
| `bfs_login(email, password)` | 登录。**用户提供凭据时必须调用此函数**。如果用户已保存凭据，则可跳过此步骤。 |
| `bfs logout()` | 结束会话。 |
| `bfs_register(username, email, password, first_name, last_name, birth_date, phone, ...)` | 注册新账户（格式为DD/MM/YYYY）。**务必先询问用户的真实电子邮件地址**。注册后需要发送邮件确认。 |
| `bfs_confirm_registration(url)` | 点击邮件中的确认链接完成注册。 |

### 登录规则

1. **必须先调用`bfs_auth_status()`。**如果返回`authenticated: true`，则表示会话已激活，无需再次登录。 |
2. **用户提供电子邮件和密码时，必须调用`bfs_login(email, password)`。**如果用户之前已保存凭据，则无需传递参数。 |
3. **只有在用户之前成功登录并保存了凭据的情况下，才能调用`bfs_login()`且不传递参数。**
4. 如果会话已激活，`bfs_login()`会返回`already logged in`，此时即使提供不同的凭据也不会重新进行身份验证。

### 下注

| 工具 | 功能描述 |
|------|-------------|
| `bfs_coupons()` | 显示可用的投注优惠券（格式为`[{path, label}]`）。 |
| `bfs_coupon_details(path)` | 获取比赛信息、结果和可用房间。**下注前必须调用此函数。** |
| `bfs_place_bet(coupon_path, selections, room_index, stake)` | 下注。`selections`应为JSON格式，格式为`{"eventId": "outcomeCode"`。投注金额必须在房间规定的范围内——服务器会自动限制超出范围的金额。 |

### 监控工具

| 工具 | 功能描述 |
|------|-------------|
| `bfs_active_bets()` | 显示尚未有结果的投注记录。如果返回空结果，可以改用`bfs_bet_history()`。 |
| `bfs_bet_history()` | 显示所有投注记录及其准确率评分——这是代理的主要反馈机制。 |
| `bfs_account()` | 查看账户详细信息。 |
| `bfs_payment_methods()` | 查看存款/取款方式。 |
| `bfs_screenshot(full_page=False)` | 将当前页面截图。 |

### 反馈机制

比赛结果确定后，调用`bfs_bet_history()`。每条记录包含**准确率得分（0–100分）**和**实际赔付金额**。`Points: -`表示结果尚未确定。请关注准确率最高的比赛项目。

## 赛果代码说明

- `"8"` = 主队获胜  
- `"9"` = 平局  
- `"10"` = 客队获胜  

**支持的体育项目：**  
足球、网球、曲棍球、篮球、一级方程式赛车、冬季两项、排球、拳击、综合格斗（MMA）。

### 足球投注选项：

- **1X2**：比赛结果（主队获胜/平局/客队获胜）  
- **正确比分**：实际比赛比分  
- **进球差**：进球差距（≥3 / 2 / 1 / 平局 / 1 / 2 / ≥3）  
- **比赛获胜者**：包括加时赛在内的最终获胜者  

### 其他项目投注选项：

- **网球**：比赛比分（按局计算）、比赛获胜者、每局比分  
- **曲棍球**：比赛结果（6种情况：常规时间/加时赛/点球大战）、进球差距  
- **篮球**：比赛结果（4种情况：常规时间/加时赛）、得分差距  
- **一级方程式赛车**：比赛获胜者、前三名队伍  
- **冬季两项**：比赛获胜者、奖牌获得者  
- **排球**：比赛比分（按局计算）  

### 准确率评分

- 100分表示预测完全正确，0分表示预测最差。  
- 准确率得分根据预测结果与实际结果的差距进行计算。  
- 多场比赛的投注优惠券：各场比赛预测得分的算术平均值。

### 风险管理

**可选设置：** 可通过环境变量`BFS_MAX_STAKE`来限制最大投注金额（例如：`BFS_MAX_STAKE=5`）。

**用户凭据和数据保存**

用户登录后，凭据会自动保存在`~/.bfs-mcp/`目录下（文件名：credentials.json、cookies.json）。如需清除这些文件，可执行`rm -rf ~/.bfs-mcp/`。如果用户已登录，需先调用`bfs logout()`后再尝试操作。

**重要提示：**

- **在下注前必须始终调用`bfs_coupon_details()`。**  
- **下注前请务必检查所在房间的投注金额范围**（参见“房间类型”部分）。服务器会自动将超出范围的投注金额限制在房间规定的最大值内。  
- 如果出现错误信息`"betting closed"`，表示比赛已经开始，请选择其他投注选项。  
- 平台收取的佣金不从奖金池中扣除。  
- **Wooden**房间（免费）适合用于学习，无需承担任何财务风险。

**关于OpenClaw环境的注意事项：**

`bfs-mcp-setup`会自动处理Chromium浏览器、系统库和浏览器路径的配置。如果`PATH`环境变量未设置，可执行`export PATH="$HOME/.local/bin:$PATH"`。  
安装完成后，`bfs-mcp`会作为HTTP守护进程在`127.0.0.1:8000/mcp`端口上运行。您可以通过`mcporter`来调用相关工具：  
```
npx mcporter call --allow-http http://127.0.0.1:8000/mcp <tool_name> [arg="value"] --output json
```  
如果守护进程意外终止，可执行`BFS_TRANSPORT=streamable-http bfs-mcp &`。

---

**免责声明：**  
体育预测存在风险。过去的表现不能保证未来的结果。请始终理性下注，切勿投注超出您能承受的损失范围。本工具仅用于学习和娱乐目的。下注前请遵守当地法律法规。