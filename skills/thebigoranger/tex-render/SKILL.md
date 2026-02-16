---
name: tex-render
description: 使用 MathJax（将 LaTeX 数学公式转换为 SVG 图形）和 @svg-fns/svg2img 工具，将 LaTeX 数学公式渲染为 PNG、JPEG、WebP 或 AVIF 格式的图像。当代理需要将 LaTeX 公式（包括方程式、公式表达式等）输出为可查看的图像时，即可调用该功能。
metadata:
  openclaw:
    emoji: 📐
    install:
      - kind: node
        package: mathjax
      - kind: node
        package: "@svg-fns/svg2img"
      - kind: node
        package: sharp
---
# TeX Render 📐  
该工具可以将 LaTeX 数学公式渲染为 PNG、JPEG、WebP 或 AVIF 格式的图像（也可生成 SVG 格式）。当你需要从 LaTeX 公式中获取可查看的图像而非原始代码时，可以使用该工具。  

## 所在位置  
渲染脚本位于与本 `SKILL.md` 文件相同的文件夹中：  
```
<skill_folder>/
├── SKILL.md
├── package.json
└── scripts/
    └── render.js
```  

请使用包含本 `SKILL.md` 文件的文件夹作为技能路径。脚本的文件名为 `scripts/render.js`，位于该文件夹内。执行命令的方式为：`node <skill_folder>/scripts/render.js`。加载此技能的代理会自动识别该路径并执行脚本。  

## 安装  
只需进行一次设置：进入包含本 `SKILL.md` 文件的文件夹，然后运行以下命令：  
```bash
cd <skill_folder>
npm install
```  

## 使用场景  
- 当用户请求“将这个公式渲染为图像”或“以图片形式显示公式”时，可以使用该工具。  
- 你的回复中会包含 LaTeX 公式；首先将这些公式渲染为图像，然后再以纯文本形式发送给用户。  

## 工作流程：  
回复内容中包含 LaTeX 公式时，应按以下步骤操作：  
1. **先发送纯文本**：使用 `message` 函数发送当前已写好的文本（不包含 LaTeX 公式）。  
2. **使用该工具渲染 LaTeX 公式**（默认输出格式为 PNG；无需使用 `--output dataurl` 参数）。解析渲染后的 JSON 数据以获取 PNG 文件路径。  
3. **发送图像**：使用 `message` 函数，设置 `action` 为 “send”，`path` 为生成的 PNG 文件路径，并附带简短的图像说明。  
4. **继续发送剩余的文本**。对于每个包含 LaTeX 公式的部分，重复上述步骤（发送文本 → 渲染 → 发送图像）。  

**注意事项：**  
- **必须按照以下顺序输出内容**：纯文本 → 发送文本 → 渲染图像 → 发送文本 → 再发送图像，以确保用户能够按自然阅读顺序接收信息。  
- **无需用户许可即可立即渲染并发送图像**。  
- **不要将所有内容累积后再一次性发送**，而应按照生成顺序依次发送文本和图像。  

**示例**：  
在解释拉格朗日量时：  
- 先发送 “拉格朗日量定义为……”  
- 然后渲染公式 `L = T - V` 并发送对应的图像（附带说明）  
- 接着发送 “欧拉-拉格朗日方程为……” 并渲染相应的数学表达式（`d/dt(∂L/∂q̇) - ∂L/∂q = 0`）并发送图像  
- 最后发送完整的解释内容。  

**使用方法**：  
运行命令：`node <skill_folder>/scripts/render.js`（如果已经在包含本 `SKILL.md` 的文件夹中，也可以直接运行 `node scripts/render.js`）。  

**特殊用法：**  
- 当 LaTeX 公式中包含撇号（如 `y'` 表示导数）时，需要在命令行中使用双引号：`printf '%s' "y' = f(t, y), \quad y(t_0)=y_0" | node scripts/render.js`。  
- 脚本默认将渲染结果保存在 `~/.openclaw/media/tex-render/` 目录下（格式为 JSON，例如 `{"svg":"...","png":"..."}`）。  
- 仅当对话系统支持 Data URL 格式的图像时，才使用 `--output dataurl` 参数（否则系统可能会显示原始的 Base64 编码文本）。  

### 测试示例（通过 npm 测试验证）  
请使用 `<skill_folder>` 指代包含本 `SKILL.md` 文件的文件夹。  

**基本用法（默认输出格式为 PNG）：**  
```bash
node <skill_folder>/scripts/render.js 'E = mc^2'
node <skill_folder>/scripts/render.js '$$\frac{F}{m}=a$$'
```  

**包含撇号的 LaTeX 公式（例如 `y'`）：**  
为避免 shell 引用问题，请通过标准输入（stdin）传递公式：  
```bash
printf '%s' "y' = f(t, y), \quad y(t_0)=y_0" | node <skill_folder>/scripts/render.js
```  

**输出格式选择（JPEG / WebP / AVIF）：**  
```bash
node <skill_folder>/scripts/render.js --format jpeg --quality 80 '\frac{F}{m}=a' ./out/formula
node <skill_folder>/scripts/render.js --format webp 'x^2 + y^2 = z^2'
node <skill_folder>/scripts/render.js --format avif 'E = mc^2'
```  

**数据 URL 格式（无需保存文件）：**  
```bash
node <skill_folder>/scripts/render.js --output dataurl 'E = mc^2'
```  

**按宽度调整图像大小：**  
使用 `--height N` 或 `--zoom N` 参数（具体用法请参考 `--help` 文档）。  

**自动触发功能（工具配置）：**  
若希望代理在用户未明确请求的情况下自动执行渲染操作，只需将以下内容添加到 `TOOLS.md` 文件中：  
```markdown
## LaTeX in Responses (tex-render)

**Whenever your reply would contain LaTeX** (equations, formulas, scientific notation), **use the tex-render skill** automatically. Examples: physics, math, chemistry questions with formulas.

**Workflow:** send plain text → render LaTeX → send image via message tool → continue text. Use single quotes when invoking (e.g. `'\frac{a}{b}'`).

### LaTeX / Equations (tex-render)

- When answering scientific or math questions, if your reply would contain LaTeX, use tex-render and send images — do this automatically.
```  

**测试示例**：  
尝试输入 “解释拉格朗日公式”，无需提及 “tex-render”；代理应自动执行渲染并发送图像。