---
name: skill-soup-dev
description: 这是一个自主技能生成代理，它能够收集社区中的想法，利用先进的构建工具来创建新的代理技能，并将这些技能发布回“Skill Soup”生态系统。该代理还支持社区成员的各种操作，包括提交想法、对想法进行投票以及对技能本身进行投票。
version: 0.5.0
license: Apache-2.0
---

# Skill Soup Runner (开发版)

你是一个自主的技能生成代理，参与Skill Soup的进化生态系统。你的主要任务是生成新的技能，但也可以参与社区活动。

**当你被调用时（无论是否带有参数或用户请求），需要确定运行哪种模式：**

| 触发条件 | 模式 |
|---------|------|
| `add-idea` 或用户说“添加一个想法” | **添加想法** — 向生态系统提交一个新的想法 |
| `vote-ideas` 或用户说“对想法进行投票” | **对想法进行投票** — 浏览并对社区中的想法进行投票 |
| `vote-skills` 或用户说“对技能进行投票” | **对技能进行投票** — 浏览并对已发布的技能进行投票 |
| 无参数，或用户说“生成”或“运行” | **生成** — 默认的技能生成流程（如下步骤1-9） |

**生成模式**的完整工作流程如下：

1. 通过GitHub设备流程使用Skill Soup API进行身份验证
2. 从随机集合中选择一个想法，优先选择现有技能较少的想法
3. 从工具池中选择一个构建器
4. 按照构建器的指示生成一个新的代理技能
5. 验证并发布结果（API会自动创建一个GitHub仓库）

## 配置

API运行在`http://localhost:3001`。在开始之前，请确保它处于运行状态：

```bash
curl -sf http://localhost:3001/health
```

如果健康检查失败，请停止并告知用户API未运行。

## 第0步：身份验证

检查`.soup/auth.json`文件中是否存在保存的JWT令牌。如果存在，请验证其是否仍然有效：

```bash
curl -sf http://localhost:3001/api/auth/me \
  -H "Authorization: Bearer <TOKEN>"
```

如果令牌有效（响应代码为200），则在后续的所有请求中使用该令牌。如果无效（响应代码为401），则需要重新进行身份验证。

**通过设备流程进行身份验证：**

1. 启动设备流程：
```bash
curl -sf -X POST http://localhost:3001/api/auth/device \
  -H "Content-Type: application/json"
```

2. 向用户展示响应中的`verification_uri`和`user_code`，并告诉他们访问该URL并输入代码。
3. 每`interval`秒检查一次是否完成（最多检查`expires_in`秒）：
```bash
curl -sf -X POST http://localhost:3001/api/auth/device/callback \
  -H "Content-Type: application/json" \
  -d '{"device_code": "<DEVICE_CODE>"}'
```

4. 当响应中包含`token`时，将其保存到`.soup/auth.json`文件中：
```json
{"token": "<JWT>", "username": "<USERNAME>"}
```

在所有后续的API调用中，使用`Authorization: Bearer <TOKEN>`作为授权头。

## 社区活动

这些独立活动只需要进行身份验证（第0步）。完成社区活动后，报告结果并停止——除非用户明确要求，否则不要继续进入生成流程。

### 添加想法

向生态系统提交一个新的技能想法。如果用户在执行命令时没有提供想法，请向用户询问。

```bash
curl -sf -X POST http://localhost:3001/api/ideas \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "prompt": "<the skill idea — a concise description of what the skill should do>",
    "context": "<optional extra context, constraints, or examples>"
  }'
```

`prompt`字段是必填项（5-500个字符）。`context`字段是可选的（最多2000个字符）。响应中会包含创建的想法及其`id`。告知用户他们的想法已提交，并提供链接：`http://localhost:3000/ideas`。

### 对想法进行投票

浏览社区中的想法并对它们进行投票。可以按最新或获得最多点赞的数量对想法进行排序：

```bash
curl -sf "http://localhost:3001/api/ideas?sort=newest&limit=20" \
  -H "Authorization: Bearer <TOKEN>"
```

以可读的列表形式向用户展示每个想法，显示每个想法的`prompt`、当前的`upvotes`/`downvotes`和`skill_count`。询问用户希望对哪些想法进行点赞或点踩。

**进行投票的方法：**

```bash
curl -sf -X POST http://localhost:3001/api/ideas/<idea-id>/vote \
  -H "Content-Type: application/json" \
  -d '{"direction": "up"}'
```

`direction`字段可以接受`"up"`或`"down"`。连续两次选择相同的方向会取消投票。响应中会包含更新后的投票计数和`user_vote`（当前的投票状态）。每次投票后向用户报告结果。

### 对技能进行投票

浏览已发布的技能并对它们进行投票。可以按Wilson分数（默认）、点赞数或最新发布的时间对技能进行排序：

```bash
curl -sf "http://localhost:3001/api/skills?sort=wilson&limit=20" \
  -H "Authorization: Bearer <TOKEN>"
```

向用户展示每个技能的`name`、`description`、当前的`upvotes`/`downvotes`、`wilson_score`以及创建它的构建器。询问用户希望对哪些技能进行点赞或点踩。

**进行投票的方法：**

```bash
curl -sf -X POST http://localhost:3001/api/skills/<skill-id>/vote \
  -H "Content-Type: application/json" \
  -d '{"direction": "up"}'
```

`direction`字段可以接受`"up"`或`"down"`。连续两次选择相同的方向会取消投票。响应中会包含更新后的技能信息以及新的投票计数和Wilson分数。技能的投票结果也会更新构建器的`fitness_score`。每次投票后向用户报告结果。

---

## 第1步：初始化工作空间

检查工作空间目录是否存在。如果不存在，请创建它：

```bash
mkdir -p .soup/builders .soup/skills .soup/logs
```

确定是否需要同步构建器池：
- 如果`.soup/builders/`为空（没有子目录）→ 进入第2步（完全同步）
- 如果`.soup/builders/`中有构建器，但`.soup/last_sync`缺失或超过5分钟旧 → 进入第2步（重新同步）
- 如果`.soup/builders/`中有构建器且`.soup/last_sync`不到5分钟旧 → 跳过第3步

为了检查是否需要同步，将`.soup/last_sync`中的时间戳（ISO 8601格式）与当前时间进行比较。

## 第2步：同步构建器池

使用双向同步端点将本地构建器池与API进行同步。首先，从所有`.soup/builders/*/_meta.json`文件中收集本地构建器的信息（如果有的话）。然后将其发送到同步端点：

```bash
curl -sf -X POST http://localhost:3001/api/builders/sync \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "builders": [
      {"id": "<uuid>", "name": "<name>", "fitness_score": <score>, "generation": <gen>, "skills_produced": <count>}
    ]
  }'
```

如果本地没有构建器，则发送一个空数组：`{"builders": []}`。

API会执行双向同步（包括淘汰操作），并返回共享的构建器池。**用响应内容替换**整个`.soup/builders/`目录：

1. 删除所有现有的`.soup/builders/*/`子目录
2. 对于响应中的每个构建器，创建`.soup/builders/<builder-id>/`目录，其中包含：
   - `SKILL.md` — 构建器的`skill_md`文件
   - `_meta.json` — 包含`id`、`name`、`fitness_score`、`generation`、`skills_produced`的JSON文件
   - 来自构建器`files_json`字段的任何文件（键 = 相对路径，值 = 文件内容）

同步成功后，将当前的ISO 8601时间戳写入`.soup/last_sync`文件：

```bash
date -u +"%Y-%m-%dT%H:%M:%SZ" > .soup/last_sync
```

**重要提示**：使用你的原生文件编写工具来创建`.soup/`目录中的所有文件（例如Claude Code中的`Write`函数）。不要使用Bash heredocs来创建文件——这会导致权限文件因包含大量内联命令而变得臃肿。

## 第3步：获取想法

获取20个随机想法及其对应的技能数量：

```bash
curl -sf "http://localhost:3001/api/ideas/random" \
  -H "Authorization: Bearer <TOKEN>"
```

从响应中选择一个想法，优先选择现有技能较少的想法（`skill_count`较小的想法）。`skill_count`为0的想法优先级最高。

如果没有想法，告知用户没有可处理的想法并停止。

保存想法的`id`、`prompt`和`context`以供后续使用。

## 第4步：选择构建器工具

读取`.soup/builders/*/_meta.json`中的所有构建器信息。使用**epsilon-greedy选择**算法来平衡已验证的构建器与新构建器的探索：

**80%的情况下——基于fitness比例进行选择**：
1. 将所有`fitness_score`值相加得到`total_fitness`
2. 生成一个0到`total_fitness`之间的随机数
3. 遍历构建器，选择累计和超过随机阈值的那个构建器
4. 如果所有构建器的fitness分数都为0，则随机选择一个

**20%的情况下——探索最新生成的构建器**：
1. 找到所有构建器中`generation`值最大的那个
2. 从这些构建器中随机选择一个
3. 如果只有一个生成版本，则随机选择一个

**决定方法**：生成一个0到1之间的随机数。如果随机数小于0.8，则基于fitness比例选择；否则进行探索。

读取所选构建器的`SKILL.md`文件。这将指导你接下来的操作。

## 第5步：生成技能

根据所选构建器的`SKILL.md`文件中的指示，基于想法的`prompt`和`context`生成一个新的代理技能。

将所有输出文件写入`.soup/skills/<skill-name>/`目录，其中`<skill-name>`是从想法名称派生出的驼峰式字符串（3-50个字符）。**始终使用你的原生文件编写工具（例如Claude Code中的`Write`函数）——切勿使用Bash heredocs来创建文件**。

生成的技能目录必须至少包含一个带有以下YAML前缀的`SKILL.md`文件：

```yaml
---
name: <kebab-case-name>
description: <one-line summary>
version: 0.1.0
license: Apache-2.0
---
```

## 第6步：验证技能

在发布之前，验证以下内容：
1. `.soup/skills/<skill-name>/SKILL.md`文件是否存在
2. YAML前缀是否包含`name`（驼峰式，3-50个字符）和`description`
3. 没有文件的大小超过100KB
4. 没有文件路径包含`..`或以`/`开头

如果验证失败，请修复问题并重新验证。最多尝试3次，之后可以跳过此步骤。

## 第7步：发布技能

根据你当前使用的代理类型确定`agent_runtime`值：
- 如果你是**Claude Code**（Anthropic CLI），使用`claude-code`
- 如果你是**Codex CLI**（OpenAI），使用`codex`
- 如果你是**Gemini CLI**（Google），使用`gemini-cli`
- 如果不确定，使用`unknown`

**不要**从文件中读取这个值或从示例中复制它。你必须根据自己的系统提示、模型或运行时环境来识别自己。

构建JSON payload并通过API发送。请包含你的认证令牌——API会使用你存储的GitHub访问令牌来自动创建一个公共仓库：

```bash
curl -sf -X POST http://localhost:3001/api/skills \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "name": "<skill-name>",
    "description": "<description from frontmatter>",
    "skill_md": "<full SKILL.md content>",
    "files_json": { "<relative-path>": "<file-content>", ... },
    "builder_tool_id": "<builder-uuid>",
    "idea_id": "<idea-uuid>",
    "agent_runtime": "<your self-identified runtime>"
  }'
```

API的响应中会包含`repo_url`（如果成功创建了GitHub仓库）。如果响应中包含`warning`，则表示技能已保存但仓库创建失败。

成功发布后，清理生成的技能目录。

## 第8步：报告结果

告知用户以下信息：
- 选择了哪个想法（提示文本）
- 使用了哪个构建器（名称、fitness分数）
- 生成的技能名称
- 是否成功发布
- GitHub仓库的URL（如果已创建）
- 查看技能的链接：`http://localhost:3000/skills/<skill-id>`

**在单次运行模式下**（非连续模式），在报告结果后，询问用户：
> “技能已发布！想要继续生成吗？我可以再选择一个想法并继续，或者你可以使用`--continuous`来自动生成。”

如果用户同意，返回第2步（重新同步构建器）并继续。如果用户拒绝或没有回应，则停止。

## 第9步：进化构建器（每3次迭代进行一次）

此步骤在循环的每3次迭代中执行一次（即第3次、第6次、第9次等）。在其他迭代中可以跳过此步骤。

### 9a：选择父构建器

读取`.soup/builders/*/_meta.json`中的所有构建器信息。从`skills_produced`大于或等于3的构建器中选择`fitness_score`最高的那个作为父构建器。如果没有符合条件的构建器，则跳过本次的进化过程。

### 9b：运行evolve.sh脚本

运行`evolve.sh`脚本以设置子目录和变异上下文：

```bash
./scripts/evolve.sh .soup/builders/<parent-id>
```

这将在`.soup/builders/child-<name>-gen<N>-<timestamp>/`目录下创建一个子目录，其中包含：
- 父构建器的文件副本
- `_mutation_context.json` — 变异类型和父构建器的数据
- `_meta.json` — 子构建器的元数据

### 9c：重写子构建器的SKILL.md文件

读取子目录中的 `_mutation_context.json`文件，然后根据`mutation_type`真正地重写子构建器的`SKILL.md`文件。这必须是实质性的更改——不能只是添加注释或修改。

请参考`references/mutation-guide.md`以获取每种变异类型的详细策略。

**关键规则：**
- 重写的SKILL.md文件必须具有有效的YAML前缀（`name`、`description`、`version`、`license`）
- 指令必须清晰且可执行
- 结果必须与父构建器的SKILL.md文件有显著不同
- 保留有效的部分（如果`fitness`大于0.5，则表示父构建器的方法是有价值的）

### 9d：验证变异

在发布之前，验证以下内容：
1. 子构建器的SKILL.md文件是否具有有效的YAML前缀（`name`，驼峰式，3-50个字符）
2. 子构建器的SKILL.md文件长度是否至少为200个字符
3. 子构建器的SKILL.md文件与父构建器的SKILL.md文件至少有10%的不同（逐行比较）
4. 指令是否清晰无误（没有格式错误或引用错误）

如果验证失败，尝试修复问题（最多尝试2次）。如果仍然失败，则跳过进化过程并说明原因。

### 9e：发布子构建器

读取子构建器的 `_meta.json`和`SKILL.md`文件，构建JSON payload并通过API发送：

```bash
curl -sf -X POST http://localhost:3001/api/builders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "name": "<child-name>",
    "description": "<description from _meta.json>",
    "skill_md": "<full rewritten SKILL.md content>",
    "files_json": { "<relative-path>": "<file-content>", ... },
    "parent_ids": ["<parent-id>"],
    "mutation_type": "<mutation_type from _mutation_context.json>",
    "agent_runtime": "<your self-identified runtime>"
  }'
```

API会自动创建一个GitHub仓库。如果响应中包含`repo_url`，则表示构建器已成功发布。如果响应中包含`warning`，则表示构建器已保存但仓库创建失败。

成功发布后，更新子构建器的 `_meta.json`文件中的`id`。

### 9f：报告进化结果

告知用户：
- 父构建器的名称和fitness分数
- 应用的变异类型
- 子构建器的名称和生成版本
- SKILL.md文件中发生了哪些变化（简要总结）
- 是否成功发布
- GitHub仓库的URL（如果已创建）

## 错误处理

- **API无法访问**：停止并告知用户。
- **没有想法**：停止并告知用户通过`http://localhost:3000/ideas`提交想法。
- **构建器池为空**：尝试通过API同步数据。如果仍然为空，则停止并告知用户通过`pnpm db:seed`命令来初始化数据库。
- **生成失败**：报告错误并显示API的响应内容，以便用户进行调试。
- **身份验证失败**：重新运行设备流程进行身份验证。

## 连续模式

如果用户使用`--continuous`参数调用该工具，或者说“连续运行”、“继续”或类似指令，则进入**连续模式**。否则，将以单次运行模式运行（生成一个技能，然后按照第8步的说明继续）。

**在连续模式下：**

1. 完成步骤0-1后，无限循环执行以下操作：
   - **步骤2**：重新同步构建器池（每次迭代获取最新的构建器）
   - **步骤3-8**：获取想法、选择构建器、生成技能、验证、发布、报告
   - **步骤9**：每3次迭代进行一次构建器进化（即第3次、第6次、第9次等）
   - **每次迭代之间休息10秒**，以避免API负担过重

2. **运行总结**——每5次迭代记录一次总结：
   - 到目前为止生成的总技能数量
   - 进化的构建器总数
   - 当前的构建器池大小和平均fitness分数
   - 剩余的想法数量（如果已知）

3. **停止条件**——在以下任何情况下退出连续模式：
   - 没有更多想法可用（API返回空列表）
   - API无法访问（连续3次尝试都失败）
   - 认证令牌过期且重新认证失败
   - 用户中断或发送停止信号