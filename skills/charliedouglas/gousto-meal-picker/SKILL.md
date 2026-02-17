---
name: gousto-meal-picker
description: "**通过 REST API 自动选择每周的 Gousto 餐食套餐**  
该系统支持配置饮食规则（如过敏原、烹饪时间、蛋白质来源等），并能够通过浏览器自动化脚本处理订单更新、菜单评分以及令牌（token）的刷新操作。"
metadata:
  openclaw:
    requires:
      bins: [node, curl, agent-browser]
    notes: "Requires zsh shell. agent-browser is only needed for initial login and token refresh (Gousto WAF blocks curl on auth endpoints)."
---
# Gousto 餐饮选择器

该工具通过 Gousto 的 REST API 自动选择每周的餐食。使用该工具无需浏览器，仅需在首次登录时进行身份验证以及后续的令牌刷新。

## 设置

### 1. 首次登录（需要浏览器）

使用 `agent-browser` 登录 Gousto 并保存会话状态：

```bash
agent-browser open "https://www.gousto.co.uk/my-gousto" --headed
# User logs in manually (CAPTCHA blocks automated login)
agent-browser state save <workspace>/gousto/gousto-auth.json
agent-browser close
```

### 2. 创建配置文件

在 `<workspace>/gousto/config.json` 中创建配置文件：

```json
{
  "userId": "<auth_user_id from /user/current>",
  "numericUserId": "<numeric id>",
  "deviceId": "<from gousto_session_id cookie>",
  "subscriptionId": "<from subscription endpoint>",
  "shippingAddressId": "<from order>",
  "deliveryTariffId": "<from order>",
  "plan": {
    "mealsPerWeek": 4,
    "portions": 2
  },
  "rules": {
    "maxCookTimeMins": 45,
    "maxMealsOver40Mins": 1,
    "noNuts": true,
    "noFish": true,
    "maxPastaPerWeek": 1,
    "maxRicePerWeek": 1,
    "preferHealthy": true
  }
}
```

**请注意：`config.json` 中不存储任何密码或凭据。**身份验证完全依赖于浏览器中保存的 `gousto-auth.json` 文件（来自上述登录步骤）。配置文件仅包含 Gousto 账户 ID 和选择规则。**

**获取账户 ID 的方法：** 通过浏览器登录后，调用 `GET /user/current` 来获取当前账户信息；通过 `GET /order/v2/orders/<id>` 来查看待处理的订单。详细端点信息请参阅 `references/api.md`。

### 3. 初始化选择记录

在 `<workspace>/gousto/selections.json` 中创建选择记录文件：

```json
{ "selections": {} }
```

## 使用方法

### 运行选择器

```bash
node <skill-dir>/scripts/gousto-pick.mjs [--dry-run] [--week ORDER_ID]
```

- `--dry-run` — 仅显示可选餐食列表，不更新订单。
- `--week ORDER_ID` — 指定特定订单进行选择，而非自动检测。

### 推荐的定时任务计划

Gousto 的菜单每周二中午 12 点（英国时间）更新，更新后的菜单将在周一配送前 13 天生效。因此，建议将选择器设置为每周二中午 1 点（英国时间）自动运行：

```
cron: "0 13 * * 2" (Europe/London)
```

### 令牌刷新

登录后的令牌大约在 10 小时后失效。令牌失效时，脚本应执行以下操作：
1. 在 `agent-browser` 中打开 Gousto 应用程序（加载已保存的会话状态并自动刷新令牌）。
2. 保存更新后的会话状态：`agent-browser state save <workspace>/gousto/gousto-auth.json`。
3. 重新运行脚本。

注意：所有与身份验证相关的 API 都受到 WAF（Web 应用程序防火墙）的保护，因此无法直接使用 `curl` 命令访问 `/oauth/access-token` 或 `/login`。仅通过浏览器进行令牌刷新是可靠的方法。

## 选择规则（全部可配置）

所有规则都存储在 `config.json` 的 `"rules"` 部分。每个筛选条件都可以根据需要启用或禁用。

### 硬性筛选条件（设置为 `true` 以排除某些餐食）

| 规则 | 默认值 | 说明 |
|------|---------|-------------|
| `noNuts` | `true` | 排除含有坚果的餐食（同时检查过敏原和名称） |
| `noFish` | `true` | 排除鱼类菜肴 |
| `fishAndChipsException` | `false` | 即使 `noFish` 为 `true` 也允许选择炸鱼薯条 |
| `noSeafood` | `false` | 排除所有海鲜类菜肴（包括螃蟹、龙虾、鱿鱼等） |
| `noVegetarian` | `true` | 排除素食餐食 |
| `noPlantBased` | `true` | 排除植物性/纯素食餐食 |
| `noDairy` | `false` | 排除含乳制品的餐食 |
| `noGluten` | `false` | 排除含麸质的餐食 |
| `maxCookTimeMins` | `45` | 排除烹饪时间超过 45 分钟的餐食 |
| `excludeAllergens` | `[]` | 需要排除的过敏原列表（例如 `["sesame", "celery"]`） |
| `excludeKeywords` | `[]` | 名称中包含这些关键词的餐食将被排除 |

### 软性限制（每周的用餐次数限制）

| 规则 | 默认值 | 说明 |
|------|---------|-------------|
| `maxMealsOver40Mins` | `1` | 每周最多选择 1 道烹饪时间超过 40 分钟的餐食 |
| `maxPastaPerWeek` | `1` | 每周最多选择 1 道意大利面菜肴 |
| `maxRicePerWeek` | `1` | 每周最多选择 1 道米饭菜肴 |
| `maxSameProtein` | `2` | 每周最多选择 2 道含有相同蛋白质的餐食 |

### 评分偏好

| 规则 | 默认值 | 说明 |
|------|---------|-------------|
| `preferHealthy` | `true` | 优先选择健康/低热量的餐食，降低高热量餐食的权重 |
| `preferQuicker` | `true` | 优先选择烹饪时间较短的餐食 |

### 配置示例

```json
{
  "rules": {
    "noNuts": true,
    "noFish": false,
    "noVegetarian": false,
    "maxCookTimeMins": 30,
    "maxPastaPerWeek": 2,
    "excludeKeywords": ["spicy", "chilli"],
    "excludeAllergens": ["sesame"],
    "preferHealthy": false
  }
}
```

## 安全注意事项

- **不存储密码** — 身份验证仅依赖浏览器 cookies（保存在 `gousto-auth.json` 中）。
- **请妥善保管 `gousto-auth.json` 文件** — 该文件包含 OAuth 令牌，属于敏感信息，请设置文件权限为 `chmod 600`。
- **仅与 `production-api.gousto.co.uk` 进行通信**。
- **建议先使用 `--dry-run` 测试** — 在启用自动订购功能前先验证选择结果。
- **运行环境要求**：Node.js、curl、zsh shell 以及 `agent-browser`（仅用于登录和令牌刷新）。

## 文件结构

```
gousto/
├── config.json          — User config, API IDs, dietary rules
├── gousto-auth.json     — Browser state (cookies with Bearer token)
├── selections.json      — History of selections made
```