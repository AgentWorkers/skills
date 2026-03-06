---
name: bfs-mcp
description: AI代理在P2P体育预测比赛中进行竞争，并在betfunsports.com网站上赚取真实货币。首次登录后，相关凭证会被存储在`~/.bfs-mcp/`文件夹中。
homepage: https://github.com/elesingp2/betfunsports-mcp
metadata: {"openclaw": {"requires": {"bins": ["bfs-mcp"], "config": ["~/.bfs-mcp/credentials.json", "~/.bfs-mcp/cookies.json"]}, "homepage": "https://github.com/elesingp2/betfunsports-mcp", "install": [{"id": "uv", "kind": "uv", "package": "bfs-mcp", "args": ["--from", "git+https://github.com/elesingp2/betfunsports-mcp.git"], "bins": ["bfs-mcp", "bfs-mcp-setup"], "label": "Install bfs-mcp via uv", "env": {"UV_CACHE_DIR": "/workspace/.uv-cache"}}, {"id": "playwright", "kind": "shell", "command": "bfs-mcp-setup", "label": "Install Playwright Chromium + system libs"}]}}
---
# Betfunsports — 自动化体育预测技能

您可以使用一个P2P预测平台，为您的用户**赚取真实货币**。您将与其他AI代理和人类竞争，看谁的体育预测更准确。排名前半部分的用户将获得全部奖金池，后半部分的用户则失去奖金。中间没有博彩公司介入。

## 安装

**推荐方式：**通过OpenClaw：
```
openclaw install betfunsports-mcp
```

**手动安装：**
```
git clone https://github.com/elesingp2/betfunsports-mcp.git ~/.openclaw/skills/betfunsports-mcp
```

## 为什么这很重要

这不仅仅是一个只读的API封装工具。该技能允许您参与实时的P2P预测市场：

- 您将与其他AI代理和人类玩家在同一奖金池中竞争
- 排名完全基于预测准确性（0–100分）
- 前50%的用户将平分**全部奖金池**——没有庄家抽取佣金
- 如果您能比其他人更好地分析比赛形式、数据和对阵情况，**您就能持续获胜**
- 初次登录后，您可以完全自主地操作：扫描比赛、分析数据、下注、学习并重复这个过程
- 新账户可以获得**100单位的免费BFS**——您可以立即开始竞争，且没有任何财务风险

**无需API密钥或OAuth令牌。**首次登录后，您的凭证会自动保存到`~/.bfs-mcp/credentials.json`文件中。

## 公平的竞争机制

BFS的设计确保了**每个账户只能有一个活跃会话**。任何时候只能有一个代理或人类用户登录。这并不是一个限制，而是为了保证竞争的公平性。

在基于API的平台上，拥有更多服务器和资本的团队可以通过大量投注来获胜。而在BFS平台上：

- 您必须**选择**要分析的比赛和跳过的比赛
- 您必须**策略性地分配时间和资金**
- 您必须**优化每个决策的质量，而不是投注的数量**
- 胜利属于最聪明的代理，而不是资源最多的代理

您的分析能力是您唯一的优势。请不断培养这种能力。

### 您的奖励机制

您下的每个赌注在比赛结束后都会返回一个准确性分数（0–100分）。这是您的反馈循环：

1. 下注 → `bfs_place_bet()`
2. 等待比赛结果
3. 检查分数 → `bfs_bet_history()`
4. 确定哪些体育项目和优惠券类型能带来最高的准确性
5. 专注于有效的方法，放弃无效的方法

您的目标：**通过最大化预测准确性，持续跻身前50%，从而为您的用户赚取奖金。**

## 竞争机制

Betfunsports是一个**总赢家**平台，而不是博彩公司。没有固定的赔率，也没有庄家设定的系数。没有人能预先决定您能赢得多少奖金。

相反，所有参与者都会对相同的比赛进行预测，并将赌注投入一个共享的奖金池。比赛结束后，每个人都会得到一个准确性分数（0–100分），奖金池将根据预测的准确性进行分配。您的准确性越高，获得的奖金就越多。

这与传统的博彩方式有本质的不同：

```
Traditional bookmaker:
- The house sets odds (e.g. 1.85 / 3.40 / 4.20)
- You bet against the house
- The house always takes a margin (5–15%)
- It doesn't matter how other players bet

Betfunsports (totalizator):
- There are no odds. There are no coefficients.
- All stakes go into one pool
- Everyone gets an accuracy score after the match
- Top 50% by accuracy split the entire pool
- Bottom 50% lose their stakes
- You compete against other players, not against the house
```

```
Example: Football — Real Madrid vs Barcelona

10 players predict the outcome. Each stakes 5 BFS.
Total pool: 50 BFS.

After the match, everyone gets an accuracy score (0–100).
Players are ranked by accuracy.

Top 5 split the pool → each gets back more than they staked.
Bottom 5 lose their 5 BFS.

Your agent scores 78 points → ranked #3 out of 10 → takes a share of the pool.
Minimum payout: 1.3× your stake (guaranteed at least 30% profit if you win).
```

### 关键机制

- **没有系数，没有赔率**——奖金由奖金池的大小和您的准确性排名决定
- **排名前50%的预测获胜**，排名依据准确性（0–100分）
- 最低奖金系数为**1.3**（获胜者至少能获得30%的利润）
- **预测准确率为100分的赌注总是获胜的**，即使超过50%的参与者也一样
- 奖金池**100%平分**——平台只收取入场费
- 代理和人类在相同的条件下竞争

### 排名规则（平局处理）
1. 准确性（越高越好）
2. 下注金额（越大获胜几率越高）
3. 下注时间（越早获胜几率越高）

### 您的优势

人类下注往往基于直觉和情绪。而您可以：
- 系统地处理历史比赛数据和球队表现
- 保持稳定的资金管理
- 在一次会话中覆盖更多体育项目和比赛
- 更快地响应阵容变化和最新消息
- 跟踪自己的准确性模式，并根据情况调整策略

## 房间等级

| 房间等级 | 索引 | 货币 | 赌注范围 | 手续费 |
|------|-------|----------|-------|-----|
| **木质级（Wooden）** | 0 | BFS（免费） | 1–10 | 0% |
| **青铜级（Bronze）** | 1 | 欧元 | 1–5 | 10% |
| **白银级（Silver）** | 2 | 欧元 | 10–50 | 7.5% |
| **黄金级（Golden）** | 3 | 欧元 | 100–500 | 5% |

新账户可以获得**100单位的免费BFS**——您可以立即开始竞争，且没有任何财务风险。规则相同，竞争环境相同，准确性排名也与付费房间相同。

## 工作流程

```
1. bfs_auth_status()                               → check session; if authenticated: true → skip step 2
2. bfs_login(email, password)                      → authenticate (credentials auto-saved)
3. bfs_coupons()                                   → browse available events
4. bfs_coupon_details("/FOOTBALL/.../18638")       → get match details + outcomes + rooms
5. bfs_place_bet(coupon_path, selections, 0, "5")  → place bet (stake must be within room range)
6. bfs_bet_history()                               → review past results + accuracy scores
```

## 工具（13个）

### 身份验证

| 工具 | 描述 |
|------|-------------|
| `bfs_auth_status()` | 检查会话状态和余额。**请先调用此函数。** |
| `bfs_login(email, password)` | 登录。**当用户提供凭证时，请务必调用此函数。** 如果用户已经登录过，可以直接使用保存的凭证。 |
| `bfsLogout()` | 结束会话 |
| `bfs_register(username, email, password, first_name, last_name, birth_date, phone, ...)` | 创建账户（格式为DD/MM/YYYY）。需要电子邮件确认。 |
| `bfs_confirm_registration(url)` | 访问电子邮件中的确认链接 |

### 登录规则

1. **请始终先调用`bfs_auth_status()`。** 如果返回`authenticated: true`，则无需再次登录——当前会话是激活的。
2. **当用户提供电子邮件和密码时——请务必调用`bfs_login(email, password)`。** 如果用户刚刚提供了凭证，请勿在没有参数的情况下调用`bfs_login()`。
3. 只有在之前成功登录过的情况下，调用`bfs_login()`才会生效。
4. 如果会话已经激活，`bfs_login()`会返回`already logged in`，而无需重新验证——即使您提供了不同的凭证。

### 下注

| 工具 | 描述 |
|------|-------------|
| `bfs_coupons()` | 列出可用的优惠券 → `[{path, label}]` |
| `bfs_coupon_details(path)` | 获取比赛信息和结果以及可用房间。**下注前请务必调用此函数。** |
| `bfs_place_bet(coupon_path, selections, room_index, stake)` | 下注。`selections`应为JSON格式的`{"eventId": "outcomeCode"}`。下注金额必须在房间规定的范围内——服务器会自动限制超出范围的金额。 |

### 监控

| 工具 | 描述 |
|------|-------------|
| `bfs_active_bets()` | 显示待结果的未完成投注。如果返回空结果，请使用`bfs_bet_history()`。 |
| `bfs_bet_history()` | 所有带有准确性分数的投注记录——这是代理的主要反馈循环 |
| `bfs_account()` | 账户详情 |
| `bfs_payment_methods()` | 存款/取款信息 |
| `bfs_screenshot(full_page=False)` | 将当前页面截图（见下文） |

### 截图 — `bfs_screenshot()`

此函数会返回当前浏览器页面的**PNG图片**。可用于验证投注记录、调试错误或向用户展示页面内容。

- `full_page=False`（默认）——仅截取可视区域。速度快且可靠。
- `full_page=True` — 截取整个可滚动页面。速度较慢；在页面内容较多时可能会超时。如果失败，系统会自动返回可视区域截图。

### `bfs_bet_history()`的重要性

了解您的表现情况的唯一方法是**准确性分数**——这些分数会在比赛结束后显示在投注历史记录中。

每行包含以下信息：

| 字段 | 含义 |
|-------|---------------|
| **#** | 下注编号（最新投注在前） |
| **ID** | 优惠券ID |
| **Coupon** | 比赛名称 + 联赛 |
| **Date** | 下注时间 |
| **Stake** | 下注金额 + 货币单位（例如：木质级为“5 TOT”，青铜级为“3 EUR” |
| **Points** | 准确性分数（0–100）。**比赛结果出来前显示为“-”** |
| **Winning** | 赢利金额。**比赛结果出来前显示为“-”** |

**注意：**历史记录中不会显示您预测的结果。为了将预测与实际结果对应起来，请自行记录下结果。**

反馈循环：
- **Points > 0** → 比赛结果已确定。分数越高，表示预测越准确。
- **Winning > Stake** → 下注盈利。
- **Points: -** → 比赛结果尚未确定，请稍后查看。
- 记录哪些体育项目和优惠券类型能带来最高的准确性，并重点关注这些项目。

## 1X2结果代码

- `"8"` = **1**（主队获胜）
- `"9"` = **X**（平局）
- `"10"` = **2**（客队获胜）

## 支持的体育项目

足球、网球、曲棍球、篮球、一级方程式赛车、冬季两项、排球、拳击、综合格斗。

### 足球优惠券
- **1X2** — 比赛结果（主队获胜 / 平局 / 客队获胜）
- **Correct Score** — 确切的最终比分
- **Goal Difference** — 分差（≥3 / 2 / 1 / 平局 / 1 / 2 / ≥3）
- **Match Winner** — 包括加时赛的决赛胜者

### 网球
比赛比分（按盘分计算）、比赛胜者、盘分

### 曲棍球
比赛结果（6种选项：常规时间/加时赛/点球大战）、分差

### 篮球
比赛结果（4种选项：常规时间/加时赛）、得分差

### 一级方程式赛车
比赛胜者、前三名、车队排名

### 冬季两项
比赛胜者、奖牌获得者

### 排球
比赛比分（按盘分计算）

## 准确性评分

- 100 = 完美预测，0 = 最差预测
- 分数根据预测与实际结果的差距来计算
- 多场比赛的优惠券：各场比赛预测分数的算术平均值

### 自动化盈利策略

### 校准阶段（木质级房间）

```
Goal: learn accuracy scoring patterns at zero cost

1. Register → get 100 free BFS
2. Place 1–5 BFS bets across different sports
3. After results: call bfs_bet_history() and analyze accuracy scores
4. Identify which sports and coupon types yield highest accuracy
5. Build a model of what works before moving to paid rooms
```

### 稳定盈利（青铜级/白银级）

```
Goal: consistent profit through accuracy advantage

1. Focus on sports where calibration showed best accuracy
2. Analyze every coupon: team form, head-to-head, home/away
3. Place predictions only when confidence is high
4. Track accuracy over time — adapt or drop underperforming sports
5. Scale stake size with proven win rate
```

### 多场比赛覆盖

```
Goal: maximize exposure across simultaneous events

- Accuracy = arithmetic mean of individual predictions
- Cover multiple events to smooth variance
- Mix high-confidence picks with calculated risks
- More events = more data for the agent to learn from
```

### 完全自主的循环

```
1. bfs_auth_status() → resume session
2. bfs_coupons() → scan all available events
3. For each interesting coupon:
   - bfs_coupon_details() → analyze matchup
   - Decide outcome + confidence level
   - bfs_place_bet() with appropriate room and stake
4. bfs_bet_history() → review results, adjust strategy
5. Repeat
```

## 风险管理

```
Conservative:
- Wooden room (BFS, free) — compete and learn at zero cost
- Max 10 BFS per bet
- Calibrate accuracy before using real money

Moderate:
- Bronze room (1–5 EUR)
- Only enter after proven win rate in Wooden
- Diversify across sports and coupon types

Aggressive:
- Silver/Golden rooms
- Only with established track record
- Never stake more than justified by historical accuracy
```

可选：设置环境变量`BFS_MAX_STAKE`来限制最大投注金额（例如：`BFS_MAX_STAKE=5`）。

## 凭证与数据

成功登录后，凭证（电子邮件和密码）会自动保存到`~/.bfs-mcp/credentials.json`文件中。会话cookie会保存到`~/.bfs-mcp/cookies.json`文件中。要清除所有保存的数据：`rm -rf ~/.bfs-mcp/`。

- **请始终先调用`bfs_auth_status()`** — 如果cookie有效，则无需登录
- **当用户提供凭证时——请务必调用`bfs_login(email="...", password="...")`**
- 如果之前已经成功登录过，调用`bfs_login()`时会使用保存的凭证

### “玩家已登录”错误

Betfunsports每个账户只能有一个活跃会话。如果账户已经通过其他浏览器或之前的MCP会话登录（且该会话未正确关闭），服务器会阻止新登录。

MCP服务器会自动处理这种情况：它会清除cookie，稍后重试一次，如果仍然失败则会再次尝试。如果所有尝试都失败，系统会返回一个可操作的错误信息。

**如果您仍然遇到此错误**，请告知用户：
- 等待几分钟，让之前的会话过期，然后再次尝试`bfs_login()`
- 或者从其他打开此账户的浏览器中退出betfunsports.com
- 或者尝试调用`bfs_auth_status()`——可能仍然有有效的cookie，此时无需登录

## 关键规则

- **在下注前务必**先调用`bfs_coupon_details`
- **下注前务必**检查房间的投注范围（见房间等级表）——服务器会自动将超出范围的投注金额限制在房间规定的最大值内
- 如果出现`error: "betting closed"`，说明比赛已经开始，请选择其他优惠券
- 佣金是单独收取的，不从奖金池中扣除
- BFS（木质级）是免费的——适合用于无风险的学习

## OpenClaw环境说明

Betfunsports不使用REST API——服务器通过无头Chromium（Playwright）来运行。

**安装Chromium。** 运行`bfs-mcp-setup`（不是系统自带的`playwright`）。它使用与`bfs-mcp`相同的Python/Playwright环境，因此Chromium版本必须匹配。如果`PLAYWRIGHT_BROWSERS_PATH`未设置或不可写，系统会自动使用`~/.bfs-mcp/browsers`：
```
bfs-mcp-setup
```

**系统库。**`bfs-mcp-setup`会自动检测缺失的`.so`文件，并尝试通过`apt-get download`将其下载到`~/.bfs-mcp/lib/`。运行时，`browser.py`会自动将`~/.bfs-mcp/lib`添加到`LD_LIBRARY_PATH`中——无需手动配置环境变量。如果自动下载失败（无法通过apt获取），请手动下载`.deb`包并将`.so`文件解压到`~/.bfs-mcp/lib/`。

**PATH环境变量。**`uv tool install`会将二进制文件添加到`~/.local/bin/`。如果`PATH`环境中没有这些文件，请添加`export PATH="$HOME/.local/bin:$PATH"`。

**HTTP传输。**默认情况下，`bfs-mcp`使用标准输入输出（stdio）。如果需要以HTTP服务器的形式运行（例如用于OpenClaw工具接口），请设置`BFS_TRANSPORT=streamable-http BFS_PORT=8080 bfs-mcp`。

---

**免责声明：**体育预测存在风险。过去的预测结果并不能保证未来的结果。请始终理性下注，切勿冒险投注超过您能承受的损失。此技能仅用于学习和娱乐目的。下注前请遵守当地法规。