---
name: bunpro-sync
description: 将 Bunpro 的日语语法学习进度从 API 同步到本地存储，以便进行分析和获取洞察。当用户需要备份学习进度、跟踪语法掌握情况、分析复习模式或监控日语能力等级（JLPT）的进步时，可以使用此功能。该功能支持社区文档中记录的 Bunpro 前端 API。
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - BUNPRO_FRONTEND_API_TOKEN
      bins:
        - python3
    primaryEnv: BUNPRO_FRONTEND_API_TOKEN
    emoji: 📚
    homepage: https://www.bunpro.jp
---
# Bunpro 同步

将您在 Bunpro 上的语法学习进度同步到本地，以便进行分析和获取反馈。

**⚠️ 重要提示：** 此功能使用的是社区文档中记录的 API。从设置中获取的官方 Bunpro API 密钥无法使用——您需要从浏览器中获取前端 API 令牌（Frontend API Token）。

## 概述

此功能会从 Bunpro 获取您的语法学习进度，并将其存储在本地 SQLite 数据库中。您可以跟踪 SRS（Systematic Review and Study）的学习阶段、查看学习预测、了解 JLPT（日本语言能力测试）的进度，以及识别需要重点复习的语法知识点（即那些反复出错的内容）。

## API 令牌：两种不同的令牌

Bunpro 提供了 **两种不同的 API 令牌**，它们各自具有不同的用途：

### ❌ **请勿使用：** “官方” API 密钥（来自设置）

- 获取位置：`bunpro.jp/settings/account`
- 格式：`d406663ff421af27c87caaa62eefdb7a`（32 个十六进制字符）
- **此令牌无法用于** 本功能所使用的前端 API 端点**
- 使用此令牌会收到 401 Unauthorized 的错误响应

### ✅ **请使用：** 前端 API 令牌（来自浏览器）

- 获取位置：浏览器开发者工具 → 控制台（Console）或应用程序存储（Application Storage）
- 格式：`eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...`（一个较长的 JWT 令牌，包含 200 多个字符）
- **此令牌是本功能所必需的**
- 令牌会定期过期（您需要定期刷新）

### 如何获取前端 API 令牌

**方法 1：通过控制台（推荐）**
1. 访问 [bunpro.jp](https://bunpro.jp) 并登录
2. 按下 **F12** 打开开发者工具
3. 点击 **控制台**（Console）选项卡
4. 粘贴以下 JavaScript 代码并按回车键：
   ```javascript
   Object.fromEntries(
     new URLSearchParams(
       document.cookie.replace(/; /g, '&')
     )
   ).frontend_api_token
   ```
5. 复制出现的長字符串（以 `eyJ` 开头）

**方法 2：通过本地存储（Local Storage）**
1. 访问 bunpro.jp 并登录
2. 按下 F12 → 选择 **应用程序**（Application）选项卡（或 Firefox 中的 **存储**）
3. 在左侧导航栏中，展开 **本地存储**（Local Storage） → **https://bunpro.jp**
4. 查找 `token`、`authToken` 或 `frontend_api_token`
5. 复制对应的值（以 `eyJ` 开头）

**方法 3：通过网络请求（Network Requests）**
1. 访问 bunpro.jp 并登录
2. 按下 F12 → 选择 **网络**（Network）选项卡
3. 刷新页面
4. 查找任何 API 请求（例如 `/user` 或 `/queue`）
5. 点击该请求 → **请求头**（Request Headers）选项卡
6. 找到 `Authorization: Bearer eyJ...` 这一行
7. 复制 `Bearer` 后面的部分

**⚠️ 令牌过期：**
前端 API 令牌会定期过期（几天或几周后）。当您收到 401 错误时，请重复上述步骤以获取新的令牌。

## 快速入门

### 同步所有数据
```bash
# Using environment variable (recommended)
export BUNPRO_FRONTEND_API_TOKEN="eyJ0eXAiOiJKV1Qi..."
python3 scripts/sync.py

# Or pass token directly (less secure)
python3 scripts/sync.py --token "eyJ0eXAiOiJKV1Qi..."

# Store in specific directory
python3 scripts/sync.py --data-dir ~/bunpro-data
```

### 同步特定数据
```bash
# Only user info
python3 scripts/sync.py --user-only

# Only study queue
python3 scripts/sync.py --queue-only

# Only reviews
python3 scripts/sync.py --reviews-only
```

### 强制进行完整同步
```bash
python3 scripts/sync.py --full
```

## 数据库架构

### `user`  
包含您的账户信息，如等级、经验值（XP）、虚拟货币（buncoin）以及账户状态。

### `grammar_points`  
包含语法知识点的相关信息，如标题、含义、结构、JLPT 等级、单元/课程内容。

### `reviews`  
记录您对每个语法知识点的学习进度（学习阶段、下一次复习时间、复习状态等）。

### `study_queue`  
列出计划在未来复习的语法知识点。

### `due_items`  
显示当前可以复习的语法知识点（包含 `is_leech` 标志，表示需要重点复习的内容）。

### `user_stats`  
汇总统计信息（如 SRS 学习情况、学习预测、JLPT 进度、活动记录等）。

### `review_histories`  
记录您的复习历史（最近一次复习、过去 24 小时的记录）。

### `sync_meta`  
用于跟踪上次同步的时间戳。

## 常用查询语句
```sql
-- Grammar mastery by JLPT level
SELECT jlpt_level, COUNT(*) as total,
       SUM(CASE WHEN burned = 1 THEN 1 ELSE 0 END) as burned
FROM reviews r
JOIN grammar_points g ON r.grammar_point_id = g.id
GROUP BY jlpt_level;

-- Upcoming reviews
SELECT DATE(next_review) as day, COUNT(*)
FROM reviews
WHERE next_review > datetime('now')
GROUP BY day
ORDER BY day
LIMIT 7;

-- Grammar leeches
SELECT g.title, g.meaning, d.streak, r.srs_stage_string
FROM due_items d
JOIN grammar_points g ON d.reviewable_id = g.id
LEFT JOIN reviews r ON d.reviewable_id = r.reviewable_id
WHERE d.is_leech = 1
ORDER BY d.streak ASC;
```

## 查询工具
```bash
# Show SRS distribution
python3 scripts/queries.py srs

# Show upcoming review forecast
python3 scripts/queries.py forecast

# Show grammar mastery by JLPT level
python3 scripts/queries.py grammar --jlpt 5

# Show currently due reviews
python3 scripts/queries.py due

# Show grammar leeches
python3 scripts/queries.py leeches

# Show overall progress
python3 scripts/queries.py progress

# Show recent activity
python3 scripts/queries.py activity
```

## API 注意事项

- **基础 URL：** `https://api.bunpro.jp/api/frontend`
- **认证方式：** 使用来自浏览器的 JWT 令牌（而非设置中的 API 密钥）
- **请求频率限制：** 目前未知，请合理使用请求频率
- **稳定性：** 该 API 受社区文档管理，可能会随时更改
- **权限说明：** 在 Bunpro 团队的许可下进行了逆向工程（即通过分析其实现方式来使用）

## 故障排除

**401 Unauthorized 错误：**
- 令牌已过期（请从浏览器中获取新的令牌）
- 使用了错误的令牌类型（需要前端 API 令牌，而非设置中的 API 密钥）
- 令牌格式应为 JWT 格式（`eyJ0eXAi...`）

**500 Server Error 错误：**
- Bunpro API 可能暂时不可用
- 端点地址可能发生了变化
- 请查阅 [Bunpro 社区 API 文档](https://github.com/cbullard-dev/bunpro-community-api)

**数据为空：**
- 您可能处于“休假模式”（请查看 bunpro.jp 上的状态说明）
- 尚未进行任何复习操作
- 端点结构与预期不符

## 参考资料

- [Bunpro 社区 API 的 GitHub 仓库](https://github.com/cbullard-dev/bunpro-community-api)
- [Bunpro 社区论坛上的 API 相关讨论](https://community.bunpro.jp/t/bunpro-api-when/100574)
- [Postman 示例集合](https://www.postman.com/technical-meteorologist-63813544/bunpro-api/collection/a7eufz9/bunpro-frontend-api)
- `references/api-structure.md` — 完整的 API 端点文档

## 相关文件

- `scripts/sync.py` — 主要的同步工具（支持命令行界面）
- `scripts/queries.py` — 提供常用查询功能的辅助脚本
- `references/api-structure.md` — Bunpro API 的详细参考文档