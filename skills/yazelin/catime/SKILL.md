---
name: catime
description: "**功能说明：**  
- **获取并发送AI生成的每小时一张猫咪图片：**  
  每小时，通过Google Gemini生成一张独特的猫咪图片。  
- **使用场景：**  
  - 当用户请求查看猫咪图片时；  
  - 当用户希望浏览猫咪图片库时；  
  - 当用户希望接收最新的AI生成的猫咪图片时。"
metadata:
  openclaw:
    requires:
      bins: [uv]
    install:
      - id: catime-pip
        kind: pip
        package: catime
        bins: [catime]
        label: "Install catime (pip install catime)"
---

# catime — 每小时自动生成的猫咪图片 🐱

> **简要说明：** 获取最新（或任意）一张由 AI 生成的猫咪图片，并附带图片说明和生成背景故事，发送给用户。

每小时，[catime](https://github.com/yazelin/catime) 会使用 Google Gemini 生成一张独特的猫咪图片。该功能允许 AI 代理根据编号、日期或生成时间来检索猫咪图片，并通过消息工具直接将图片发送给用户。

---

## 安装

```bash
pip install catime
```

安装完成后，即可使用 `catime` 命令行工具（CLI）。请验证安装是否成功：

```bash
catime --help
```

---

## AI 代理快速入门

### 第一步 — 使用 `catime` 获取猫咪图片

运行 CLI 命令以获取图片的元数据。最常用的命令如下：

```bash
catime latest
```

**输出示例：**

```
Cat # 241  2026-02-11 04:57 UTC  model: gemini-3-pro-image-preview
  URL: https://github.com/yazelin/catime/releases/download/cats/cat_2026-02-11_0457_UTC.webp
  Idea: 一隻以精緻黑絲線繡成的貓咪，正專注地在微縮的金色與黑色奢華香氛實驗室中，嗅聞試香紙上的氣味，整個場景以刺繡的微縮立體模型形式呈現。
  Prompt: An embroidered illustration of an elegant black cat, crafted from exquisite black silk threads with visible needlework, satin stitch, and French knots. The cat is presented as a handcrafted textile art miniature diorama...
  Story: 在一個宛如織品藝術品的微縮香室裡，環形燈的光線均勻地灑落，凸顯出所有織品與布料的精緻質感。這隻優雅的黑貓，其絲線繡成的毛髮閃爍著低調的光澤，牠全神貫注地分辨著香氣，周圍是數個鑲有金色瓶蓋的繡花香水瓶。牠正試圖從層疊的香氣中，捕捉那一縷最為珍貴的靈感。
```

### 第二步 — 解析输出结果并将图片发送给用户

从以 `  URL:` 开头的那一行中提取图片的 URL。然后使用消息工具（或其他相应工具）将图片连同图片说明一起发送给用户。

**消息工具的示例数据格式（YAML）：**

```yaml
action: send_message
media:
  type: image
  url: "https://github.com/yazelin/catime/releases/download/cats/cat_2026-02-11_0457_UTC.webp"
caption: "🐱 Cat #241 — AI-generated cat of the hour!"
text: |
  Here's your cat! Cat #241, created at 2026-02-11 04:57 UTC.
  Story: 在一個宛如織品藝術品的微縮香室裡，環形燈的光線均勻地灑落...
metadata:
  source: catime
  cat_number: 241
  model: gemini-3-pro-image-preview
  generated_at: "2026-02-11 04:57 UTC"
```

**消息工具的示例数据格式（JSON）：**

```json
{
  "action": "send_message",
  "media": {
    "type": "image",
    "url": "https://github.com/yazelin/catime/releases/download/cats/cat_2026-02-11_0457_UTC.webp"
  },
  "caption": "🐱 Cat #241 — AI-generated cat of the hour!",
  "text": "Here's your cat! Cat #241, created at 2026-02-11 04:57 UTC.\nStory: 在一個宛如織品藝術品的微縮香室裡…",
  "metadata": {
    "source": "catime",
    "cat_number": 241,
    "model": "gemini-3-pro-image-preview",
    "generated_at": "2026-02-11 04:57 UTC"
  }
}
```

---

## 命令参考

### `catime latest`

获取最新生成的猫咪图片。

**输入：**
```bash
catime latest
```

**输出：**
```
Cat # 241  2026-02-11 04:57 UTC  model: gemini-3-pro-image-preview
  URL: https://github.com/yazelin/catime/releases/download/cats/cat_2026-02-11_0457_UTC.webp
  Idea: 一隻以精緻黑絲線繡成的貓咪…
  Prompt: An embroidered illustration of an elegant black cat…
  Story: 在一個宛如織品藝術品的微縮香室裡…
```

**解析说明：**
- **第一行**：标题信息：`Cat # <编号> <日期> <时间> UTC  model: <模型名称>`
- **第二行**（`  URL:`）：图片的 URL。这是最重要的信息。
- **第三行**（`  Idea:`）：图片的简要概念（中文描述）。
- **第四行**（`  Prompt:`）：用于生成图片的完整英文提示语。
- **第五行**（`  Story:`）：猫咪的生成背景故事（中文描述）。

### `catime today`

获取当天生成的猫咪图片（UTC 时间）。返回多条猫咪信息。

**输入：**
```bash
catime today
```

**输出示例：**
```
Found 2 cat(s) for 'today':

Cat # 240  2026-02-11 02:49 UTC  model: gemini-3-pro-image-preview
  URL: https://github.com/yazelin/catime/releases/download/cats/cat_2026-02-11_0249_UTC.webp
  Idea: 一張以35mm底片攝影風格捕捉的畫面…
  Prompt: A candid 35mm film photograph…
  Story: 午後的自然漫射光，透過老舊窗戶溫柔地灑落在候車室地面…

Cat # 241  2026-02-11 04:57 UTC  model: gemini-3-pro-image-preview
  URL: https://github.com/yazelin/catime/releases/download/cats/cat_2026-02-11_0457_UTC.webp
  Idea: 一隻以精緻黑絲線繡成的貓咪…
  Prompt: An embroidered illustration of an elegant black cat…
  Story: 在一個宛如織品藝術品的微縮香室裡…
```

**解析说明：** 第一行显示“找到了 N 张今天的猫咪图片：”。后续的每条猫咪信息格式与 `catime latest` 相同。若需获取最新的图片，请选择最后一条记录。

### `catime <编号>`

根据编号获取特定的猫咪图片。

**输入：**
```bash
catime 42
```

**输出：**
```
Cat #  42  2026-01-31 23:24 UTC  model: gemini-3-pro-image-preview
  URL: https://github.com/yazelin/catime/releases/download/cats/cat_2026-01-31_2324_UTC.webp
```

**解析说明：** 格式相同。对于编号查询，可能仅显示标题和 URL，不包含图片概念、提示语和生成背景故事。

### `catime --list`

列出所有猫咪的详细信息（编号 + 图片 URL，格式简洁）。

**输入：**
```bash
catime --list
```

**输出示例（前 10 条）：**
```
Cat #   1  2026-01-30 05:46 UTC  model: gemini-2.5-flash-image
  URL: https://github.com/yazelin/ccat/releases/download/cats/cat_2026-01-30_0546_UTC.png
Cat #   2  2026-01-30 05:56 UTC  model: gemini-3-pro-image-preview
  URL: https://github.com/yazelin/catime/releases/download/cats/cat_2026-01-30_0556_UTC.webp
Cat #   3  2026-01-30 06:23 UTC  model: gemini-3-pro-image-preview
  URL: https://github.com/yazelin/catime/releases/download/cats/cat_2026-01-30_0623_UTC.webp
Cat #   4  2026-01-30 06:33 UTC  model: gemini-3-pro-image-preview
  URL: https://github.com/yazelin/catime/releases/download/cats/cat_2026-01-30_0633_UTC.webp
Cat #   5  2026-01-30 06:53 UTC  model: gemini-2.5-flash-image (fallback from gemini-3-pro-image-preview, reason: timeout after 180.0s)
  URL: https://github.com/yazelin/catime/releases/download/cats/cat_2026-01-30_0653_UTC.webp
```

**解析说明：** 每条猫咪信息占用两行：奇数行是标题，偶数行是图片 URL。使用 `--list | tail -2` 可查看最新的猫咪信息；使用 `--list | wc -l` 可统计猫咪数量。

### `catime <日期>`

根据指定的日期（YYYY-MM-DD 格式）获取猫咪图片。

**输入：**
```bash
catime 2026-01-30
```

### `catime view`

在默认浏览器中打开图片库。对于 AI 代理来说，此命令不太实用——建议使用 `catime latest` 或指定编号。

---

## 代理工作流程：将猫咪图片发送给用户

请严格按照以下步骤操作：

### 1. 确定要获取的猫咪图片

| 用户请求 | 需要执行的命令 |
|---|---|
| “展示一张猫咪图片” | `catime latest` |
| “展示今天的猫咪图片” | `catime today` |
| “展示编号为 42 的猫咪图片” | `catime 42` |
| “展示 2026-01-30 当天的猫咪图片” | `catime 2026-01-30` |
| “随机展示一张猫咪图片” | `catime $(shuf -i 1-241 -n 1)` |

### 2. 运行命令并捕获输出结果

```bash
output=$(catime latest 2>&1)
```

### 3. 从输出结果中提取图片 URL

查找以 `  URL: ` 开头的那一行，并提取其中的 URL。

**解析规则（伪代码）：**
```
for each line in output:
    if line.strip().startswith("URL:"):
        image_url = line.strip().removeprefix("URL:").strip()
        break
```

**解析规则（bash 命令）：**
```bash
image_url=$(echo "$output" | grep '  URL: ' | head -1 | sed 's/.*URL: //')
```

### 4. 解析可选的元数据

```
cat_number  → from header line: regex `Cat #\s*(\d+)`
datetime    → from header line: regex `(\d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC)`
model       → from header line: regex `model: (.+)$`
story       → from line starting with `  Story: ` (everything after "Story: ")
prompt      → from line starting with `  Prompt: ` (everything after "Prompt: ")
```

### 5. 将图片发送给用户

使用消息工具，将提取到的 URL 和元数据一起发送给用户：

```yaml
action: send_message
media:
  type: image
  url: "<extracted image_url>"
caption: "🐱 Cat #<cat_number> — AI-generated cat of the hour!"
text: |
  Here's your cat! Cat #<cat_number>, created at <datetime>.
  Story: <story text>
metadata:
  source: catime
  cat_number: <cat_number>
  model: <model>
  generated_at: "<datetime>"
```

### 6. 异常处理机制

- **如果 URL 不存在**：告知用户图片信息无法获取，并建议尝试使用 `catime latest` 或其他编号。
- **如果未安装 `catime`：** 先运行 `pip install catime`，然后再尝试。
- **如果网络出现问题**：CLI 会从 GitHub 下载 `catlist.json` 文件。如果网络无法连接，告知用户需要网络访问权限。
- **如果用户需要多张图片**：使用 `catime today` 并解析所有结果（每条结果之间用空行分隔），然后选择其中一张发送给用户。

---

## 输出格式说明

所有 `catime` 命令的输出结果都遵循以下格式：

```
Cat # <NUMBER>  <YYYY-MM-DD> <HH:MM> UTC  model: <MODEL_NAME>
  URL: <IMAGE_URL>
  Idea: <SHORT_CONCEPT_TEXT>
  Prompt: <FULL_GENERATION_PROMPT>
  Story: <NARRATIVE_TEXT>
```

**字段说明：**

| 字段 | 行前缀 | 是否必填 | 说明 |
|---|---|---|---|
| 编号 | `Cat # `（标题） | ✅ 是 | 猫咪的顺序编号（1, 2, 3, …） |
| 日期/时间 | 标题 | ✅ 是 | 图片的生成时间（UTC 格式） |
| 模型名称 | `model: `（标题） | ✅ 是 | 使用的 AI 模型（例如 `gemini-3-pro-image-preview`） |
| URL | `  URL: ` | ✅ 是 | 图片的直接链接（格式为.webp 或.png） |
| 图片概念 | `  Idea: ` | 有时会有 | 图片的简要概念描述（中文） |
| 生成提示语 | `  Prompt: ` | 有时会有 | 用于生成图片的完整英文提示语 |
| 生成背景故事 | `  Story: ` | 有时会有 | 图片的生成背景故事（中文描述） |

**解析注意事项：**
- `URL` 字段**始终存在**，是发送图片的关键信息。
- `Idea`、`Prompt` 和 `Story` 仅在详细显示模式下（如 `catime latest`、`catime today` 或指定编号时）出现，可能在 `--list` 模式中缺失。
- 所有图片链接均指向 GitHub 的公开资源，无需身份验证即可访问。
- 图片格式为 `.webp`（常见格式）或 `.png`（旧版本图片）。

---

## 对 AI 代理的建议：

1. **当用户仅要求“展示一张猫咪图片”时，** 建议默认使用 `catime latest`。
- **图片的 URL 在以 `  URL: ` 开头的那一行中**——发送图片时只需提供该 URL 即可。
- **图片说明为中文**——可以为英语用户进行翻译，或保留原文以增加双语效果。
- **图片存储在 GitHub 的公开资源中**——加载速度快，无需身份验证。
- **每小时会有新图片生成**——如用户需要最新图片，始终使用 `catime latest`。
- **如需随机选择图片**，可随机选取一个编号（1 到最新编号之间）。
- **使用 `--list` 可高效浏览**——每条猫咪信息仅显示两行（标题和 URL）。
- **不要使用 `catime view`——该命令会在浏览器中打开图片库，不适用于代理或命令行环境**。
- **如有图片说明，请包含在其中**——这能为图片增添趣味性和个性化。
- **如果用户对图片的生成过程感兴趣，** 可参考 `Prompt` 字段。

---

## 关于 catime

- 🎨 每小时使用 Google Gemini 生成一张猫咪图片
- 📚 提供 103 种以上的图片风格供选择
- 🐱 每张图片都有独特的背景故事和个性特征
- 图片库链接：[yazelin.github.io/catime](https://yazelin.github.io/catime/)
- PyPI 包安装地址：`pip install catime`
- GitHub 仓库：[github.com/yazelin/catime](https://github.com/yazelin/catime)

---

*注：如有需要，可以编写辅助脚本来实现自动发送猫咪图片的功能，但上述 CLI 命令已足以满足所有操作需求。*