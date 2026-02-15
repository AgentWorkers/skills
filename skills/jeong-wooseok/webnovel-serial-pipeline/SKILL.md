---
name: webnovel-serial-pipeline
version: 0.1.4
description: 构建并发布一部由Quartz平台支持的韩文网络小说系列（流程包括：草稿→封面设计→图片格式转换（webp格式）→章节文档编写→代码检查（lint）→最终发布）。使用工具：Nano Banana Pro和ffmpeg。
---

# WebNovel Serial Pipeline (Quartz)

## ⚠️ 安全提示

由于以下原因，此技能可能会触发防病毒软件的误报：
- **Shell脚本（.sh）**：仅用于ffmpeg图像转换和依赖项检查
- **子进程调用**：仅用于调用Python代码检查工具
- **prepublish_check.py**：用于检测恶意模式的扫描工具（反而会被防病毒软件标记为恶意文件）
  - 该脚本包含`curl`、`wget`等命令，用于检测（而非执行）恶意代码
  - 这是一个安全功能，并非恶意软件

所有代码均为开源，可审计。不存在任何恶意行为。

---

本文档记录了我们在Quartz平台上托管韩文网络小说系列作品时所使用的端到端工作流程（例如《Drama/야간조》）。

## 快速入门（复制/粘贴）
在终端中执行以下命令：
```bash
# 1) Install
clawhub install webnovel-serial-pipeline

# 2) Go to the skill folder
cd skills/webnovel-serial-pipeline

# 3) Set your Quartz root (env var)
export WEBNOVEL_QUARTZ_ROOT="/absolute/path/to/8.quartz"

# 4) Verify deps
bash scripts/check_deps.sh

# 5) After you say “검수 완료”, publish + sync index
bash scripts/publish_review_ok.sh --series "야간조" --episode 2 --slug "불-꺼지면-가지-마세요" --draft-file "/path/to/draft.md"
```

## 目标

- 每集内容都易于阅读（避免使用“作者评论”风格的文字）
- 每集至少包含一张图片
- 图片适合网页展示：将图片大小压缩至1K字节（格式为WebP，质量设置为70~80%，最大尺寸1200像素）
- 发布过程安全：先将草稿文件存档，经过审核后再上传至Quartz平台

## 设计与需求（编写前的准备工作）

本部分介绍了我们在创建工作流程之前进行的**提案与需求分析**过程。

### 初始问题（一次性提问，可选）
请将以下问题以一条消息的形式提出，用户选择并回答后，相关风格将固定下来。

- **类型（可选）**：剧情剧 / 办公室惊悚剧 / 黑色幽默剧 / 现实题材浪漫剧
- **参考作品（可选）**：如果用户选择了自己熟悉的剧集类型，那么故事的风格、剧情走向和情感线索将直接确定。
  - 例如：《我的叔叔》、《美生》、《D.P.》、《我的解放日记》、《The Glory》（仅限类型）、《Signal》、《秘密森林》、《坏家伙们》、《怪物》、《我的名字》
  - 推荐方式：选择1部主要参考作品和1部辅助参考作品
- **适宜年龄（可选）**：12岁适合 / 15岁适合 / 适合全年龄观众
- **集长度（可选）**：3~5分钟 / 5~10分钟（符合网络小说的阅读节奏）
- **背景设定（可选）**：旧城区 / 强南办公区 / 住宅区 / 公共机构
- **角色数量（必填）**：2~6个角色（包括角色名称和简短的性格描述）

### 避免低俗内容（默认规则）
- 故事冲突基于现实生活（工作、金钱、道德、人际关系），禁止使用超能力或夸张情节
- 禁止使用网络流行语和低俗表达
- 避免过多的解释性文字，通过角色行为和选择来展现故事
- 必须包含1~2次角色内心想法（即“潜台词”）
- 角色设计应避免非黑即白的二元对立，而是通过缺陷、欲望和恐惧等复杂因素来塑造角色
- 喜剧元素应通过情境和讽刺手法来表现，而非直接嘲笑人物
- 禁止使用过度夸张的效果、字体或情绪表达（包括文字风格）
- 结局应留下“后续影响”而非简单的幸福或不幸结局

### 成熟度评估标准（自动检查）
- 不使用低俗或网络流行语
- 说明性文字占比不超过20%（大部分内容应为角色行为和选择）
- 至少有两个角色因不同目标而产生冲突
- 每个事件都应留下至少一个明确的后果（涉及金钱、人际关系或信任等方面）

### 十集剧集的设计模板
- EP01：引入剧情线索（明确设定事件起点）
- EP02：引发第一个事件
- EP03~04：揭示故事结构和关联线索（从偶然事件中发现规律）
- EP05：展示现实中的阻碍因素（例如“为什么不敢举报”）
- EP06~07：迫使角色做出选择（涉及金钱、人际关系或道德抉择）
- EP08：揭示角色身份和故事背景（内部人士的秘密或责任推卸）
- EP09：做出无法挽回的选择
- EP10：以“后续影响”作为结局（避免过度夸张的情节）

### 关系发展规则（适度的情感表达）
- 禁止通过琐碎对话来建立关系，应通过**两次小恩小惠**来推动关系发展
  - A对B：一次简单的关心行为（行动胜过言语）
- B对A：一次默默的帮助（禁止将角色塑造成英雄）
- 称呼方式要符合现实：
  - 在知道对方姓名之前：使用职业或功能相关的称呼
  - 知道姓名后：避免使用“叔叔”等称呼，应使用正式的姓名

---

## 分发前的准备工作（路径设置及可选API）

### 1) 设置Quartz项目的根目录
在分发过程中，我们**不使用固定的机器路径**。

所需环境变量：
- `WEBNOVEL_QUARTZ_ROOT`：你的Quartz项目根目录（存放已发布内容的文件夹）

可选设置：
- `WEBNOVEL_DRAFT_ROOT`：存放草稿文件的目录
- `NANO_BANANA_KEY`（仅在使用nano-banana-pro生成封面图片时需要）

示例：
```bash
export WEBNOVEL_QUARTZ_ROOT="/absolute/path/to/8.quartz"
export WEBNOVEL_DRAFT_ROOT="/absolute/path/to/drafts"   # optional
```

### 2) 依赖项检查
在该技能文件夹内执行以下命令：
```bash
bash scripts/check_deps.sh
```

### 3) 发布前的安全检查（使用ClawHub）
在上传文件之前，运行以下命令：
```bash
python3 scripts/prepublish_check.py
```
如果发现明显的窃取或下载痕迹，该命令会失败。

## 文件夹结构规范

- Quartz项目根目录（已发布内容）：
  - `$WEBNOVEL_QUARTZ_ROOT`（例如：`/path/to/8.quartz`
- 示例剧集文件夹结构：
  - `Drama/<series>/index.md`（包含项目介绍和制作规则）
  - `Drama/<series>/<series>-01-....md`（已发布的剧集文件）
  - `Drama/<series>/images/*.webp`（封面图片）
- 草稿文件（未发布）：
  - `$WEBNOVEL_DRAFT_ROOT/<series>_serial_drafts/`（例如：`/path/to/drafts/yaganjo_serial_drafts/`

## 推荐的工作流程

### 0) 确定剧集内容
- EP01：引入剧情线索
- EP02+：逐步推进剧情（每集新增一个事件）

### 1) 创建剧集草稿
首先在草稿文件夹中编写剧集内容。

### 2) 生成封面图片
使用Nano Banana Pro工具生成1K字节的PNG封面图片，然后将其转换为WebP格式。

### 3) 嵌入封面图片并添加标签
- 确保封面图片的标签包含六个关键信息：
  - `领域/主题/格式/目标受众/语言`
- 使用Quartz的wiki链接将封面图片嵌入剧集正文中：
  - `![[Drama/<series>/images/<cover>.webp]]`

### 4) 代码检查（风格审核）
发布前进行快速代码检查：
- 避免重复的表达（如“因为……所以……”）
- 避免使用过于笼统的描述
- 保持对话自然简洁

### 5) 发布文件
只有在用户确认同意后，才将文件上传至Quartz平台。

推荐的发布命令（将草稿文件上传至Quartz并重命名文件）：
```bash
python3 scripts/publish_episode.py \
  --draft-file /path/to/draft.md \
  --quartz-root "$WEBNOVEL_QUARTZ_ROOT" \
  --series-dir "$WEBNOVEL_QUARTZ_ROOT/Drama/<series>" \
  --series "<series>" \
  --episode 2 \
  --slug "불-꺼지면-가지-마세요"
```

### 6) 同步`index.md`文件中的剧集列表（可选，推荐）
在`Drama/<series>/index.md`文件中添加相应的标记：
```md
## 에피소드
<!-- episodes:start -->
<!-- episodes:end -->
```

然后执行以下命令：
```bash
python3 scripts/sync_index.py \
  --index-file "$WEBNOVEL_QUARTZ_ROOT/Drama/<series>/index.md" \
  --series-dir "$WEBNOVEL_QUARTZ_ROOT/Drama/<series>" \
  --series "<series>"
```

### 一次性发布流程（仅在用户确认“审核完成”后执行）
推荐的安全发布流程如下：等待用户明确表示“审核完成”，然后执行以下操作：
```bash
bash scripts/publish_review_ok.sh \
  --series "야간조" \
  --episode 2 \
  --slug "불-꺼지면-가지-마세요" \
  --draft-file "/path/to/drafts/yaganjo_serial_drafts/야간조-연재-02-불-꺼지면-가지-마세요.md"
```

该流程将执行以下操作：
- 代码检查 + 资产验证 + 将文件上传至Quartz平台
- 同步`Drama/<series>/index.md`文件中的剧集列表

## 所需脚本

### A) 创建剧集框架
```bash
python3 scripts/new_episode.py \
  --series "야간조" \
  --series-dir "$WEBNOVEL_QUARTZ_ROOT/Drama/야간조" \
  --episode 2 \
  --slug "불-꺼지면-가지-마세요" \
  --draft-dir "/path/to/drafts/yaganjo_serial_drafts"
```

### B) 将PNG图片转换为WebP格式
```bash
bash scripts/to_webp.sh \
  /path/to/cover.png \
  /path/to/cover.webp
```

### C) 对剧集内容进行代码检查
```bash
python3 scripts/lint_episode.py \
  --file /path/to/episode.md
```

## 实际使用的工作规则

- **禁止使用作者评论**：删除类似“因此故事更加真实”这样的解释性文字
- **通过行动展现故事情节**：避免使用冗长的解释性描述
- **避免重复的表述**：尤其是类似“因为……所以……”这样的连贯句式
- **角色关系发展**：通过**两次小恩小惠**来推动关系发展（A对B，B对A）
- **剧情结尾**：每集结尾都要设置一个明确的下一步行动线索