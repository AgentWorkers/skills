---
name: tex-render
description: 使用 MathJax（TeX→SVG）和 @svg-fns/svg2img 将 LaTeX 数学公式渲染为 PNG、JPEG、WebP 或 AVIF 格式的图像。每当代理需要将 LaTeX 公式（包括方程式、数学表达式等）输出为可查看的图像时，即可调用该功能。
metadata:
  openclaw:
    emoji: 📐
---
# TeX Render 📐  
该技能可以将LaTeX数学公式渲染为PNG、JPEG、WebP或AVIF格式的图像（也可生成SVG格式）。当你需要从LaTeX代码中获得可查看的图像时，可以使用该技能。  

**用户须知：**  
当此技能处于激活状态时，机器人会**自动**将回复中的所有LaTeX公式渲染为图像并按顺序发送，而无需用户另行授权。如果你希望收到原始的LaTeX代码或需要手动触发渲染，请禁用此技能（或从工作区中移除它）。  

## 执行位置  
渲染脚本位于与`SKILL.md`文件相同的文件夹中：  
```
<skill_folder>/
├── SKILL.md
├── package.json
└── scripts/
    ├─── render.js
    └─── validate.js
```  

请使用包含`SKILL.md`文件的文件夹作为技能路径。脚本的文件名为`scripts/render.js`，位于该文件夹内。执行命令：`node <skill_folder>/scripts/render.js`。加载此技能的机器人会自动使用该脚本进行渲染。  

## 安装  
只需进行一次设置。安装完成后，在技能文件夹中运行`npm install`：  
```bash
cd <skill_folder>
npm install
```  

- **依赖项来源：** 所有依赖项均来自公共npm仓库（无额外下载或远程文件）。  
- **依赖库：** 安装过程中可能会使用`sharp`包；请确保你的Node.js版本为14及以上，并具备相应的构建工具链（详情请参考[sharp install](https://sharp.pixelplumbing.com/install)）。  

## 使用场景  
- 当用户请求将公式“渲染为图像”或“以图片形式展示公式”时。  
- 如果你的回复中包含LaTeX公式，应先将其渲染为图像，再以纯文本形式发送给用户。  

## 工作流程：  
每当需要输出LaTeX公式时，按照以下步骤操作：  
1. **先发送纯文本**：使用`message`函数发送已写好的文本（不含LaTeX代码）。  
2. **渲染LaTeX公式**：使用该技能将其渲染为图像（默认格式为PNG；无需使用`--output dataurl`参数）。解析生成的JSON文件以获取图像路径。  
3. **发送图像**：使用`message`函数发送图像，并附上简短的说明文字。  
4. **继续输出剩余的文本**：对每个LaTeX公式重复上述步骤。  

**重要提示：**  
输出内容必须按照以下顺序进行：先发送纯文本，再发送图像；用户会按照自然阅读顺序接收所有内容。  

**示例：**  
解释拉格朗日量时：  
- 先发送“拉格朗日量定义为……”  
- 然后渲染`L = T - V`并发送图像（附带说明文字）  
- 接着发送“欧拉-拉格朗日方程为……`并渲染相应的数学表达式（`d/dt(∂L/∂q̇) - ∂L/∂q = 0`）并发送图像  
- 最后发送完整的解释文字。  

**使用方法：**  
运行命令：`node <skill_folder>/scripts/render.js`（如果已在技能文件夹内，可直接运行`node scripts/render.js`）。  

**特殊用法：**  
- 当LaTeX公式中包含撇号（如`y'`）时，需使用双引号进行传递：`printf '%s' "y' = f(t, y), \quad y(t_0)=y_0" | node scripts/render.js`。  
- 脚本默认将图像保存在`~/.openclaw/media/tex-render/`目录下（格式为PNG、JPEG或WebP）。若对话系统支持Data URL格式，可使用`--output dataurl`参数。  

### 测试示例（已通过npm测试验证）  
请使用`<skill_folder>`表示包含`SKILL.md`文件的文件夹。  

**示例：**  
- **基本输出（默认为PNG格式）**  
- **包含撇号的LaTeX公式**  
- **JPEG / WebP / AVIF格式输出**  
- **使用Data URL格式**  
- **按宽度调整图像大小**  
- **内联数学公式（缩小显示尺寸）**  
- **设置图像高度或缩放比例**（详见`--help`参数说明）  

**自动触发方式：**  
若希望机器人自动使用`tex-render`技能（无需用户主动请求），请在工作区中添加`TOOLS.md`文件：  
```markdown
## LaTeX in Responses (tex-render)

**Whenever your reply would contain LaTeX** (equations, formulas, scientific notation), **use the tex-render skill** automatically. Examples: physics, math, chemistry questions with formulas.

**Workflow:** send plain text → render LaTeX → send image via message tool → continue text. Use single quotes when invoking (e.g. `'\frac{a}{b}'`).

### LaTeX / Equations (tex-render)

- When answering scientific or math questions, if your reply would contain LaTeX, use tex-render and send images — do this automatically.
```  

**测试建议：**  
尝试输入“解释拉格朗日公式”，无需特别提及`tex-render`，机器人应自动执行渲染并发送图像。  

## 仓库信息**  
该技能的源代码托管在[https://github.com/TheBigoranger/tex-render](https://github.com/TheBigoranger/tex-render)仓库。你可以在那里提交问题或提出功能请求。