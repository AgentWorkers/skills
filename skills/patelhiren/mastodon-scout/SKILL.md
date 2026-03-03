---
name: mastodon-scout
description: 这是一个仅具有读取权限的 Mastodon 技能（skill）。该技能能够输出易于人类阅读的时间线摘要，或者以原始 JSON 格式的数据。
metadata: {"clawdhub":{"emoji":"🦣"},"clawdis":{"envVars":[{"name":"MASTODON_TOKEN","required":true},{"name":"MASTODON_INSTANCE","required":false,"default":"https://mastodon.social"}]}}
---
# Mastodon Scout

## 功能说明

这是一个仅限读取数据的Mastodon技能。它通过一个名为`scripts/mastodon_scout.py`的Python脚本从Mastodon API获取数据。默认情况下，它会返回易于阅读的摘要；如果使用`--json`选项，则会返回原始的JSON数据。

---

## 调用规则（必填）

```bash
python3 ./scripts/mastodon_scout.py <command> [options]
```

### 命令

| 命令 | 功能 |
|---------|----------------|
| `home` | 获取已认证用户的个人时间线 |
| `user-tweets` | 获取已认证用户自己的帖子 |
| `mentions` | 获取提及该用户的帖子 |
| `search <query>` | 搜索与`<query>`匹配的帖子 |

### 选项
```
--instance <url>   Mastodon instance base URL (default: $MASTODON_INSTANCE or https://mastodon.social)
--limit <int>      Number of items to return (default: $LIMIT or 20)
--json             Output raw JSON instead of human-readable text
```

### 环境变量
```
MASTODON_TOKEN      Required. OAuth bearer token.
MASTODON_INSTANCE   Optional. Instance base URL (default: https://mastodon.social).
```

### 使用示例
```bash
python3 ./scripts/mastodon_scout.py home
python3 ./scripts/mastodon_scout.py mentions --limit 10
python3 ./scripts/mastodon_scout.py search "golang"
python3 ./scripts/mastodon_scout.py home --json
python3 ./scripts/mastodon_scout.py home --instance https://fosstodon.org
```

---

## 输出格式

### 文本模式（默认）

脚本会将每条帖子格式化为如下形式：
```
[N] Display Name (@user@instance) · <timestamp>
<content>
↩ <replies>  🔁 <reblogs>  ⭐ <favourites>
<url>
```
脚本还可能在列表后添加简短的摘要。

### JSON模式 (`--json`)

以原始的Mastodon API JSON格式返回数据，不进行任何解释。

---

## 错误处理

脚本会将错误信息以易于阅读的形式输出到标准错误流（stderr），并退出（返回非零状态码）：

| 错误类型 | 错误信息 |
|-----------|---------|
| 未设置Token | `错误：MASTODON_TOKEN未设置` |
| 401 | `Mastodon API错误：401未经授权——请检查MASTODON_TOKEN` |
| 403 | `Mastodon API错误：403禁止访问` |
| 422 | `Mastodon API错误：422无法处理的实体` |
| 429 | `Mastodon API错误：429请求频率受限——请稍后再试` |

如果遇到错误，请不要重试。如果Token缺失或无效，请引导用户进行身份验证设置。

---

## 触发此技能的示例命令

- `mastodon-scout home`  
- `show my mastodon timeline`  
- `check mastodon mentions`  
- `search mastodon for "golang"`  
- `get my mastodon posts`  

---

## 注意事项

- 该技能仅支持读取数据，不支持发布、关注或其他操作。  
- `scripts/mastodon_scout.py`仅使用Python标准库，无需安装额外的依赖包（如pip）。  
- 在JSON模式下，脚本会原样输出数据，不会进行任何解释。  

---

## 身份验证设置（机器人可提供协助）

**严格模式下的例外情况**：如果用户需要帮助获取Token，机器人可以在执行技能前提供指导。

### 获取Token的步骤：

**步骤1：访问开发设置**

- 登录到您的Mastodon实例（例如：mastodon.social、fosstodon.org）  
- 转到：**设置 → 开发**（或偏好设置 → 开发）  
- 直接URL：`https://[实例域名]/settings/applications`  

**步骤2：创建应用程序**

- 点击“新建应用程序”  
  - **应用程序名称**：`mastodon-scout`（或任意名称）  
  - **重定向URI**：`urn:ietf:wg:oauth:2.0:oob`  
  - **权限范围**：仅选择“读取”权限（取消勾选“写入”、“关注”和“推送”选项）  

**步骤3：获取访问Token**

- 点击“提交”，然后打开创建的应用程序  
- 复制“访问Token”字段的值  

**步骤4：设置环境变量**  
```bash
export MASTODON_TOKEN="paste_token_here"
```  

**步骤5：验证Token**  
```bash
python3 ./scripts/mastodon_scout.py home --limit 5
```  

### 常见的Mastodon实例：  
- `mastodon.social` — 通用用途  
- `fosstodon.org` — 开源/技术社区  
- `mas.to` — 专注于技术的社区  
- `hachyderm.io` — 技术/信息安全社区  

### 安全注意事项：  
- Token仅用于读取数据，无法用于发布、关注或删除操作。  
- 请保密Token信息（切勿将其提交到Git仓库）。  
- Token可以在开发设置中随时被撤销。  
- 每个Mastodon实例都需要单独的Token。