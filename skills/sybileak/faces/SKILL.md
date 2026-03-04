---
name: faces
description: Use this skill to interact with the Faces Platform — a compiler for the human mind. The Faces Platform takes any source material (documents, conversations, essays) and extracts the minimal cognitive primitives that define a persona, compressing them into a Face: a mathematical, semantically embedded representation of how a person thinks, believes, speaks, and is situated in the world. Faces drive any LLM as that persona and support semantic arithmetic — compare, combine, contrast minds. Faces also support boolean algebra: combine concrete Faces with |, &, -, ^ operators to create composite Faces defined by a formula. These composite Faces can be wired together into circuits — sequences of persona logic gates — making the Faces Platform an FPGA for LLMs. Due to the implicit compression of the compiler, faces use significantly less tokens to steer an LLM to embody a persona than would a soul document like SOUL.md, and faces are model agnostic. Use this skill for: creating and compiling Faces, creating composite Faces from boolean formulas, running inference through a Face, comparing Faces by centroid similarity, finding nearest or furthest minds, and managing API keys, billing, and account state.
allowed-tools: Bash(faces *)
---

# Faces技能

您可以使用`faces`命令行工具（CLI）来执行Faces平台的各项请求。

## 当前配置
!`faces config:show 2>/dev/null || echo "(no config saved)"`

## 设置检查

在运行任何命令之前，请确保您的凭据已正确设置：

```bash
faces config:show          # see what's saved
faces auth:whoami          # confirm login works
```

如果没有任何凭据，并且用户尚未提供API密钥：
- 对于交互式会话：运行`faces auth:login`，系统会提示您输入电子邮件地址和密码。
- 对于仅使用API密钥的场景：请用户设置`FACES_API_KEY=<密钥>`，或运行`faces config:set api_key <密钥>`。

如果系统找不到`faces`命令，请先进行安装：
```bash
npm install -g faces-cli
```

---

## Faces平台简介

Faces平台是一个用于分析人类思维的“编译器”。您可以向该平台提供原始材料（如文档、文章、访谈记录或对话内容），平台会从中提取出定义一个人物特征的最基本认知要素：这个人的思维方式、信仰、表达方式以及他们在世界中的位置。这些认知要素就像是思维的“机器代码”。就像氨基酸一样，这些基本元素足以构建出任何一个人物形象。生成的人物形象既连贯又复杂，甚至可能存在矛盾——就像真实的人一样。

输出结果是一个**“Face”**：一个压缩后的认知指令集，以嵌入式的语义向量的形式存储。一个“Face”的主要组成部分包括`beta`、`delta`和`epsilon`；“face”则是这三个组成部分的加权组合。通过“Face”，任何大型语言模型（LLM）都可以被重塑为一个全新的、具有独特思维模式的预测器。这种方式避免了模型“平均化”的问题，从而能够呈现出更加个性化的思维特征。

由于这些认知要素是嵌入式的，因此可以测量两个“Face”之间的差异；也可以找出在各个组成部分上最相似或最不同的“Face”。这就是对人类思维的数学化描述。

您还可以对“Face”进行布尔运算。一个**复合“Face”**是通过特定的运算符对多个“Face”进行组合得到的：

| 运算符 | 语法 | 含义 |
|---|---|---|
| 并集 | `a \| b` | 包含两个“Face”中的所有信息；在存在冲突时以“a”的内容为准 |
| 交集 | `a & b` | 仅包含两个“Face”都有的信息 |
| 差异 | `a - b` | 仅包含在“a”中而不在“b”中的信息 |
| 对称差分 | `a ^ b` | 仅包含在一个“Face”中而不在另一个“Face”中的信息 |

运算符可以带有括号：`(a | b) - c`。复合“Face”是实时的：当您向某个组件“Face”中添加新信息时，整个复合“Face”会在下一次推理请求中自动更新。由于复合“Face”本身也可以进行交互，因此可以将它们串联起来形成一系列逻辑链路：一个“Face”的输出会成为下一个“Face”的输入。这实际上就是一个用于LLM的“认知电路”。

**基本操作流程：**
1. 创建一个“Face”（`face:create`）
2. 将原始材料编译成“Face”（本地文件：`compile:doc:*`、`compile:thread:*`；或YouTube视频：`compile:import`）
3. 同步数据以提取并嵌入认知要素
4. 通过“Face”进行对话（`chat:chat`）——此时LLM会以该人物的思维方式回答问题
5. 通过质心相似度比较不同的“Face”（`face:diff`、`face:neighbors`）
6. 根据布尔公式创建新的“Face”（`face:create --formula`）

---

## 价值主张

该工具提供了可编程且可组合的“人物形象”，其复杂程度堪比真实人类，而且所需的计算资源比其他方法更少。更多的人物形象意味着更低的成本。

---

## 示例用法

**1. 历史人物的“复活”**：将某位思想家的全部作品输入到“Face”中，然后向其提出他们从未回答过的问题。答案将基于他们的真实认知结构产生，而非LLM对他们的表面印象的拼凑。

**2. 从访谈记录中生成客户意见**：上传20份访谈记录，每位参与者对应一个“Face”。使用`face:diff`比较这些“Face”，在阅读任何内容之前先获取它们的相似度矩阵。通过质心进行聚类，而非手动按主题分类。

**3. 思想者的“议会”**：组建一个由不同领域专家组成的团队（如科学家、艺术家、实用主义者、神秘主义者）。在做出任何重要决策前，先让这四位专家共同参与讨论，从而获得全面且一致的反馈。

**4. “思维的对比”**：根据您自己的写作内容创建一个“Face”，然后找出与该“Face”最不相似的“Face”——这代表了您最难以预料的思维方式。通过这个“Face”来回答您自己提出的问题。两个回答之间的差异揭示了您的认知盲点。

**5. 小说角色的构建**：利用角色的背景资料创建一个角色集合。使用`face:neighbors --direction furthest`找到自然对立的角色组合，从而构建冲突情节。

**6. 实时的思维代理**：将您的电子邮件、笔记、文章和语音备忘录编译成一个“Face”，让它成为您24/7的思维代理。通过限定的API密钥共享这个“Face”，以便在您无法参与时让同事了解您的观点。

**7. 思维方向的监测**：每季度将新内容同步到“Face”中，通过比较不同时间点的质心数据来检测个人或组织的思维是否发生变化，以及变化的方向。

**8. 布尔运算组合**：结合一个实用主义者和一个理想主义者，他们的并集（`pragmatist | visionary`）能够体现两种观点的共性；他们的交集（`pragmatist & visionary`）仅包含他们共有的部分；他们的差异（`visionary - pragmatist`）则揭示了理想主义者的思维方式（去除了实用性的因素）。每个“Face”都是一个真实存在的、可交互的思维模型。创建这些“Face”时不需要额外的文档。

**9. 合成焦点小组**：为典型的角色（早期采用者、怀疑论者、实用主义者、监管者等）创建“Face”。通过这些“Face”来评估产品提案或政策变更，从而获得多样且一致的反馈。

**10. 论点的压力测试**：将一个哲学观点或政策立场编译成一个“Face”，找出与之观点最接近的“Face”（即已经持有相同观点的人），以及最反对该观点的“Face”（即持相反观点的人）。利用后者生成最有力的反驳意见。

**11. 社交媒体的“声音”**：将您的帖子、对话记录、标题和YouTube视频编译成一个“Face”。该工具会提取您的语气、节奏和观点，从而帮助您起草新内容。当您需要表达自己的观点时，可以使用这个“Face”来撰写内容——它的表达方式更贴近您的个人风格，而非LLM的机械生成结果。

**12. 认知电路的构建**：利用“Face”构建一个决策流程。从领域文献中创建一个“专家”角色；通过`expert - consensus`得到一个“批评者”（专家的观点减去外界影响）；通过`(expert | critic) - noise`得到一个“综合者”（专家观点与外界意见的结合）。按顺序将问题传递给这三个“Face”：先询问“专家”，然后将其回答输入“批评者”，再输入“综合者”。这三个“Face”共同构成了一个完整的推理流程。

---

## 认证规则

| 命令组 | 所需凭证 |
|---|---|
| `faces auth:*`、`faces keys:*` | 仅需要JWT令牌——请先运行`faces auth:login` |
| 其他所有命令 | JWT令牌 **或** API密钥 |

---

## 输出格式

在命令后添加`--json`选项即可获得机器可读的JSON格式输出（适用于`jq`管道）：

```bash
faces face:list --json | jq '.[].username'
faces billing:balance --json | jq '.balance_usd'
faces compile:doc:list <face_id> --json | jq '.[] | {id, label, status}'
```

如果不添加`--json`，命令将输出人类可读的文本。

---

## 常见任务

### 登录
```bash
faces auth:login --email user@example.com --password secret
faces auth:whoami --json
```

### 创建一个“Face”并与其进行对话
```bash
faces face:create --name "Jony Five" --username jony-five
faces chat:chat jony-five --message "Hello!"

# With a specific LLM
faces chat:chat jony-five --llm claude-sonnet-4-6 --message "Hello!"

# Stream response
faces chat:chat jony-five --stream --message "Write a long response"
```

### 将文档编译成一个“Face”
```bash
# Step 1 — create the document
DOC_ID=$(faces compile:doc:create <face_id> --label "Notes" --file notes.txt --json | jq -r '.id')

# Step 2 — run LLM extraction
faces compile:doc:prepare "$DOC_ID"

# Step 3 — sync to face (charges compile quota; --yes skips confirm)
faces compile:doc:sync "$DOC_ID" --yes
```

### 上传文件（PDF、音频、视频、文本）
```bash
faces face:upload <face_id> --file report.pdf --kind document
faces face:upload <face_id> --file interview.mp4 --kind thread
```

### 检查计费状态
```bash
faces billing:balance --json        # credits + payment method status
faces billing:subscription --json   # plan, face count, renewal date
faces billing:quota --json          # compile token usage per face
```

### 创建一个限定的API密钥
```bash
# JWT required — keys cannot manage themselves
faces keys:create \
  --name "Partner key" \
  --face jony-five \
  --budget 10.00 \
  --expires-days 30
```

### 创建一个复合“Face”
```bash
# Union — all knowledge from both; left wins on conflicts
faces face:create --name "The Realist" --username the-realist \
  --formula "the-optimist | the-pessimist"

# Difference — optimist's knowledge minus anything the pessimist also holds
faces face:create --name "Pure Optimist" --username pure-optimist \
  --formula "the-optimist - the-pessimist"

# Intersection — only what both share
faces face:create --name "Common Ground" --username common-ground \
  --formula "the-optimist & the-pessimist"

# Symmetric difference — what each holds exclusively
faces face:create --name "The Divide" --username the-divide \
  --formula "the-optimist ^ the-pessimist"

# Parenthesized — union of two, minus a third
faces face:create --name "Filtered View" --username filtered-view \
  --formula "(analyst | critic) - moderator"

# Update a composite face's formula
faces face:update the-realist --formula "the-optimist & the-pessimist"

# Chat through a composite face — identical to any other face
faces chat:chat the-realist --message "How do you approach risk?"
```

复合“Face”是实时的：当您向某个组件“Face”中添加新信息时，整个复合“Face”会在下一次请求中自动更新。组件“Face”必须是您自己创建的、已编译好的“Face”；复合“Face”不能引用其他复合“Face”。

### 上传YouTube视频
```bash
# Solo talk, lecture, or monologue — creates a compile document
faces compile:import my-face \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --type document \
  --perspective first-person

# Interview or multi-speaker podcast — creates a compile thread
faces compile:import my-face \
  --url "https://youtu.be/VIDEO_ID" \
  --type thread \
  --perspective first-person \
  --face-speaker A

# After import, follow the printed next-step commands:
# For document:
faces compile:doc:prepare <doc_id>
faces compile:doc:sync    <doc_id> --yes

# For thread (no prepare step needed):
faces compile:thread:sync <thread_id>
```

系统会处理视频的下载和转录工作。转录费用按每小时0.37美元计算（根据音频时长），费用从您的账户余额中扣除。视频标题将自动用作文件标签。如果`--type thread`命令因未检测到说话者而失败，请尝试使用`--type document`。

### 通过质心相似度比较“Face”
```bash
# Pairwise diff across all components
faces face:diff --face aria --face marco --face jin

# Find 3 nearest faces to aria by composite score
faces face:neighbors aria --k 3

# Find most dissimilar faces by a specific principal component
faces face:neighbors aria --component beta --direction furthest --k 5
```

如果某个“Face”尚未生成某个特定组件，其对应的分数将为`null`。这两个命令要求相关的“Face”至少已经同步过一次数据。

### 人类化消息代理
```bash
faces chat:messages jony-five@claude-sonnet-4-6 \
  --message "What do you know about me?" \
  --max-tokens 512
```

### OpenAI响应代理
```bash
faces chat:responses jony-five@gpt-4o \
  --message "Summarize my recent work"
```

---

## 完整命令参考

```
faces auth:login        --email  --password
faces auth:logout
faces auth:register     --email  --password  --name  --username  [--invite-key]
faces auth:whoami
faces auth:refresh

faces face:create       --name  --username  [--formula EXPR | --attr KEY=VALUE... --tool NAME...]
faces face:list
faces face:get          <face_id>
faces face:update       <face_id>  [--name]  [--formula EXPR]  [--attr KEY=VALUE]...
faces face:delete       <face_id>  [--yes]
faces face:stats
faces face:upload       <face_id>  --file PATH  --kind document|thread
faces face:diff         --face USERNAME  --face USERNAME  [--face USERNAME]...
faces face:neighbors    <face_id>  [--k N]  [--component face|beta|delta|epsilon]  [--direction nearest|furthest]

faces chat:chat         <face_username>  -m MSG  [--llm MODEL]  [--system]  [--stream]
                        [--max-tokens N]  [--temperature F]  [--file PATH]
faces chat:messages     <face@model>  -m MSG  [--system]  [--stream]  [--max-tokens N]
faces chat:responses    <face@model>  -m MSG  [--instructions]  [--stream]

faces compile:import       <face_id>  --url YOUTUBE_URL  [--type document|thread]  [--perspective first-person|third-person]  [--face-speaker LABEL]

faces compile:doc:create   <face_id>  [--label]  (--content TEXT | --file PATH)
faces compile:doc:list     <face_id>
faces compile:doc:get      <doc_id>
faces compile:doc:prepare  <doc_id>
faces compile:doc:sync     <doc_id>  [--yes]
faces compile:doc:delete   <doc_id>

faces compile:thread:create   <face_id>  [--label]
faces compile:thread:list     <face_id>
faces compile:thread:message  <thread_id>  -m MSG
faces compile:thread:sync     <thread_id>

faces keys:create   --name  [--expires-days N]  [--budget F]  [--face USERNAME]...  [--model NAME]...
faces keys:list
faces keys:revoke   <key_id>  [--yes]
faces keys:update   <key_id>  [--name]  [--budget F]  [--reset-spent]

faces billing:balance
faces billing:subscription
faces billing:quota
faces billing:usage      [--group-by api_key|model|llm|date]  [--from DATE]  [--to DATE]
faces billing:topup      --amount F  [--payment-ref REF]
faces billing:checkout   --plan standard|pro
faces billing:card-setup
faces billing:llm-costs  [--provider openai|anthropic|...]

faces account:state

faces config:set    <key> <value>
faces config:show
faces config:clear  [--yes]
```

全局配置参数（适用于所有命令）：
```
faces [--base-url URL] [--token JWT] [--api-key KEY] [--json] COMMAND
```

环境变量：`FACES_BASE_URL`、`FACES_TOKEN`、`FACES_API_KEY`

## 指令范围

所有指令仅作用于`faces` CLI，它会通过HTTPS向Faces平台API发送请求（默认使用`api.faces.sh`；如果设置了`FACES_BASE_URL`，则会使用该地址）。除了用户明确提供的`~/.faces/config.json`文件（用于存储凭据）外，不会读取或写入任何本地文件。

**安装方式：** 通过`npm install -g faces-cli`从npm公共仓库（`npmjs.com/package/faces-cli`）安装该CLI，该工具由sybileak团队开发。源代码位于Headwaters AI组织的`faces-cli-js`仓库中。

**凭证要求：** 该工具使用JWT令牌（`FACES_TOKEN`）或API密钥（`FACES_API_KEY`）进行身份验证。凭证信息仅从环境变量或`~/.faces/config.json`中读取；当用户执行`faces auth:login`或`faces config:set`时才会写入该文件。在登录过程中，系统可能会要求输入电子邮件地址和密码，但这些信息会直接发送到Faces API，不会以明文形式存储（仅保存生成的JWT令牌）。建议使用具有预算限制和有效期的限定API密钥，而非长期有效的账户凭证。

**使用范围：** 所有指令仅限于Faces平台的功能范围（认证、角色管理、推理、数据编译、计费、API密钥）。不会执行任何系统命令、文件操作或超出`faces` CLI范围的网络请求。`jq`工具仅用于从JSON输出中提取数据。

---

---

（由于提供的SKILL.md文件内容较长，上述翻译仅包含了部分关键部分。如需完整翻译，请提供完整的文件内容。）