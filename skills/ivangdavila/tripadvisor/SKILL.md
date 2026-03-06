---
name: Tripadvisor
slug: tripadvisor
version: 1.0.0
homepage: https://clawic.com/skills/tripadvisor
description: 使用官方API来查找和比较TripAdvisor上的酒店、餐厅及景点信息。系统支持基于URL的导航方式，并确保数据处理的合规性（符合相关政策要求）。
changelog: Added official API workflows, UI navigation playbook, and clear compliance guardrails for Tripadvisor interactions.
metadata: {"clawdbot":{"emoji":"🧭","requires":{"bins":["curl","jq","sed"],"env":["TRIPADVISOR_API_KEY"],"config":["~/tripadvisor/"]},"primaryEnv":"TRIPADVISOR_API_KEY","os":["linux","darwin","win32"],"configPaths":["~/tripadvisor/"]}}
---
## 设置（Setup）

如果 `~/tripadvisor/` 不存在或为空，请阅读 `setup.md` 文件，用通俗的语言解释本地存储的原理，并在创建文件之前获取用户的确认。

## 使用场景（When to Use）

当用户希望直接与 Tripadvisor 交互时：可以使用官方的 API 工作流程和稳定的网页导航方式来搜索目的地、比较酒店/餐厅/景点、查看评论，或构建旅行推荐列表。

## 架构（Architecture）

所有数据存储在 `~/tripadvisor/` 目录下。具体设置请参阅 `memory-template.md` 文件。

```text
~/tripadvisor/
├── memory.md                 # Preferences and recurring constraints
├── sessions/
│   └── YYYY-MM-DD.md         # Search context and selected candidates
├── api/
│   ├── location-cache.md     # query -> location_id mappings
│   └── request-log.md        # redacted endpoint, params, status, timestamp
├── shortlists/
│   └── {city}-{topic}.md     # ranked options with reasons
└── archive/
```

## 快速参考（Quick Reference）

| 主题 | 对应文件 |
|-------|------|
| 设置流程 | `setup.md` |
| 数据存储结构 | `memory-template.md` |
| 官方 API 工作流程 | `api-workflows.md` |
| 网页导航指南 | `web-navigation.md` |
| 术语与合规性要求 | `compliance.md` |

## 核心规则（Core Rules）

### 1. 仅使用 Tripadvisor 的官方接口  
- 严格使用 Tripadvisor 的官方 API 端点以及常规的浏览器导航方式。  
- 禁止抓取隐藏数据、绕过访问控制，或进行任何被禁止的数据提取操作。

### 2. 在开始时明确选择使用模式  
- 每个任务只能选择一种模式：  
  - **API 模式**：结构化的数据查询，适合机器处理；  
  - **UI 模式**：交互式浏览及推荐列表生成；  
  - **混合模式**：使用 API 进行初步探索，通过 UI 进行最终确认。  

### 3. 在进行深度查询前先获取 `location_id`  
- 在 API 模式下，需先将用户查询映射为有效的 `location_id`，再获取详细信息或评论/照片数据。  
- 将成功的映射结果缓存到 `~/tripadvisor/api/location-cache.md` 文件中。

### 4. 尽量使用基于 URL 的导航方式  
- 在 UI 模式下，优先使用 Tripadvisor 提供的稳定 URL（如城市页面和实体详情页面），避免复杂的点击链。

### 5. 安全处理用户同意与反机器人机制  
- 如果出现 cookie 对话框或反机器人提示，请获取用户确认；记录相关拦截信息后，继续使用 API 模式或直接访问相应 URL。  
- 禁止使用任何绕过这些机制的方法。

### 6. 提供可决策的输出结果  
- 始终返回包含明确权衡信息的推荐列表：  
  - 是否符合用户需求；  
  - 价格与质量的平衡；  
  - 数据的准确性与完整性（是否存在缺失信息）。  

### 7. 保持存储结构简洁透明  
- 仅在 `~/tripadvisor/` 目录下存储可复用的旅行偏好设置和用户选择内容。  
- 在写入数据前请先进行确认；避免存储敏感的个人信息，并且绝不要在日志中保存 API 密钥。

## 常见错误（Common Traps）  
- 在未获取 `location_id` 之前就直接进行详细数据查询 → 可能导致 API 响应混乱或无法使用。  
- 依赖不稳定的 DOM 选择器 → 当 Tripadvisor 的 UI 发生变化时可能导致流程中断。  
- 混合使用 API 和 UI 数据（且未添加时间戳） → 会导致数据比较不准确或推荐结果错误。  
- 忽视 cookie 或同意提示 → 可能导致自动化操作失败或产生错误结果。  
- 仅依赖评分来做出决策 → 会忽略评论的时效性和重复出现的投诉信息。  
- 在查询中发送不必要的用户数据 → 会增加隐私风险和合规问题。

## 外部接口（External Endpoints）  

| 接口 | 发送的数据 | 目的 |  
|----------|-----------|---------|  
| `https://api.tripadvisor.com/api/partner/2.0/location/search` | 目的地查询及语言设置 | 获取 `location_id` |  
| `https://api.tripadvisor.com/api/partner/2.0/location/{id}` 及相关子路径 | `location_id`、语言及简单过滤条件 | 获取地点详情、评论、照片及周边信息 |  
| `https://www.tripadvisor.com/*` | 标准的浏览器导航请求及用户搜索词 | 查看公开页面及验证推荐列表内容 |  

**注意：** 不会向外部发送任何其他数据。

## 安全性与隐私（Security & Privacy）  

- **离开您设备的数据**：  
  - 目的地名称、可选的日期范围及简单过滤条件会被发送给 Tripadvisor 的 API 或网页。  

- **保留在本地的数据**：  
  - 用户的偏好设置、推荐列表结果及请求日志都存储在 `~/tripadvisor/` 目录中。  

**本技能的功能限制：**  
- 本技能** **不** 访问 `~/tripadvisor/` 之外的文件；  
- **不** 存储支付信息或护照数据；  
- **不** 使用任何抓取技巧、CAPTCHA 避免机制或反机器人手段。  

## 注意事项（Trust）  
- 使用本技能时，查询数据会直接发送给 Tripadvisor 服务。  
- 仅当您信任 Tripadvisor 并对其提供的搜索词和旅行信息感到放心时，才建议安装此技能。  

## 使用范围（Scope）  
- 本技能仅用于执行 Tripadvisor 的探索和比较功能；  
- 严格遵循官方 API 规范及安全的网页导航流程；  
- 生成的推荐列表会明确显示各项权衡因素。  

**本技能的禁止行为：**  
- **不** 承诺能保证预订结果；  
- **不** 将不确定的数据当作已验证的事实呈现；  
- **不** 在未经用户明确指示的情况下执行购买或账户操作。  

## 相关技能（Related Skills）  
- 如果用户同意安装，可使用以下技能：  
  - `booking`：比较住宿选项及总费用明细；  
  - `travel`：管理更全面的旅行计划流程；  
  - `apple-maps`：在 macOS 上验证路线情况及区域可访问性；  
  - `search-engine`：优化查询流程及数据来源的验证；  
  - `expenses`：在生成推荐列表后跟踪旅行支出。  

## 反馈建议（Feedback）  
- 如觉得本技能有用，请给 `clawhub` 评分（例如：`clawhub star tripadvisor`）；  
- 如需保持信息更新，请执行 `clawhub sync` 操作。