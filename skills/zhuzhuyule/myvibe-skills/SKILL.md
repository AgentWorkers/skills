---
name: myvibe-publish
description: 将静态 HTML 文件、ZIP 压缩包或目录发布到 MyVibe。当用户需要将网页内容发布到 MyVibe 时，可以使用此功能。
---

# MyVibe Publish

将网页内容（HTML文件、ZIP压缩包或目录）发布到MyVibe平台。

## 前提条件

- 必须安装Node.js 18或更高版本。
- 本工具的所有脚本执行操作都需要网络访问权限。运行Bash命令时，请务必使用`sandbox_permissions.require_escalated`选项以确保网络权限已启用。
- 部署和截图生成可能需要几分钟时间。请为发布命令设置10分钟（600000毫秒）的超时时间。

## 使用方法

```bash
/myvibe:myvibe-publish --file ./dist.zip      # Publish ZIP
/myvibe:myvibe-publish --file ./index.html    # Publish HTML
/myvibe:myvibe-publish --dir ./dist           # Publish directory
/myvibe:myvibe-publish --url https://example.com/app  # Import from URL
/myvibe:myvibe-publish --dir ./dist --new     # Force new Vibe
/myvibe:myvibe-publish --dir ./dist --did z2qaXXX    # Update specific Vibe
```

## 参数选项

| 参数 | 别名 | 说明 |
|--------|-------|-------------|
| `--file <路径>` | `-f` | HTML文件或ZIP压缩包的路径 |
| `--dir <路径>` | `-d` | 需要压缩并发布的目录 |
| `--url <URL>` | `-u` | 需要导入并发布的URL |
| `--hub <URL>` | `-h` | MyVibe平台的URL（默认：https://www.myvibe.so/） |
| `--title <标题>` | `-t` | 项目标题 |
| `--desc <描述>` | | 项目描述 |
| `--visibility <可见性>` | `-v` | 可见性：公共或私有（默认：公共） |
| `--did <DID>` | | 用于版本更新的Vibe DID（会覆盖自动检测的结果） |
| `--new` | | 强制创建新的Vibe，忽略之前的发布记录 |

## 工作流程概述

1. **检测项目类型** → 如果不需要构建，则在后台开始截图操作。
2. **构建**（如需要） → 然后在后台开始截图操作。
3. **元数据分析** → 提取项目标题、描述和标签信息。
4. **确认发布** → 显示元数据并获取用户确认。
5. **执行发布** → 脚本自动读取截图结果。
6. **返回结果** → 显示发布的URL。

**首次调用工具时，这些步骤会并行执行：**
- `Read`：读取源文件或目录中的主要文件。
- `Bash`：`git remote get-url origin 2>/dev/null || echo "这不是一个Git仓库"`
- `Bash`：`node {skill_path}/scripts/utils/fetch-tags.mjs --hub {hub}`

---

## 第1步：检测项目类型

| 检查条件 | 项目类型 | 下一步操作 |
|-------|-------------|-----------|
| 使用`--file`且文件为HTML/ZIP格式 | **单文件项目** | → 开始截图操作，然后进入第3步 |
| 目录中包含`dist/`、`build/`或`out/`文件夹且其中包含`index.html`文件 | **预构建项目** | → 进入第2步（确认是否需要重新构建） |
| 目录中包含`package.json`文件且其中包含构建脚本，但没有构建输出 | **可构建项目** | → 进入第2步（先进行构建） |
| 目录中包含多个`package.json`文件或工作区配置 | **多仓库项目** | → 进入第2步（选择要发布的应用程序） |
| 目录根目录下包含`index.html`文件，但没有`package.json`文件 | **静态项目** | → 开始截图操作，然后进入第3步 |

**对于不需要构建的项目（`run_in_background`设置为`true`）：**

- 对于目录类型的源文件（使用`--dir`参数）：
```bash
node {skill_path}/scripts/utils/generate-screenshot.mjs --dir {publish_target} --hub {hub}
```

- 对于单个HTML文件类型的源文件（使用`--file`参数）：
```bash
node {skill_path}/scripts/utils/generate-screenshot.mjs --file {publish_target} --hub {hub}
```

**重要提示：**  
- 当源文件是单个HTML文件时，请使用`--file`参数；当源文件是一个目录时，请使用`--dir`参数。这两个参数必须与发布配置中的`source.type`匹配，以确保生成的截图文件具有相同的哈希值。

**在后台启动截图任务后**，请使用`TaskOutput`（`block`参数设置为`false`）来检查任务输出。如果输出中包含“agent-browser未安装”或“Chromium未安装”这样的信息，请执行以下操作：
1. 安装`agent-browser`：`npm install -g agent-browser && agent-browser install`
2. 重新运行截图命令（使用相同的命令，`run_in_background`参数设置为`true`）
3. 再次使用`TaskOutput`（`block`参数设置为`false`）来确认`agent-browser`已成功安装。

这样可以在您继续进行元数据分析的同时，确保截图操作能够在后台顺利完成。

---

## 第2步：构建（如需要）

从`lock`文件中检测包管理器类型，并从`package.json`中的脚本中获取构建命令。

使用`AskUserQuestion`函数获取用户确认：
- 对于**预构建项目**：询问“是否需要重新构建或使用现有的构建结果？”
- 对于**可构建项目**：询问“在发布之前是否需要先进行构建？”
- 对于**多仓库项目**：询问“要发布哪个应用程序？”

构建完成后，在后台开始截图操作（与第1步相同的检查流程：使用`TaskOutput`（`block`参数设置为`false`）来确认`agent-browser`是否已安装，如果需要则重新安装），然后进入第3步。

---

## 第3步：元数据分析

### 提取项目标题
优先顺序：`<title>` → `og:title` → `package.json`中的名称 → 文档中的第一个`<h1>`标签

### 生成项目描述（50-150字，采用故事化风格）

描述内容应涵盖项目的**目的**、**功能**以及**开发过程**（可选）。
信息来源包括：对话记录、`README.md`文件、源代码、`package.json`文件以及Git日志。

**编写描述时的指导原则：**
- 采用自然、对话式的表达方式。
- 重点介绍项目的实际价值和功能，而非技术细节。
- 避免使用过于泛泛的描述，如“使用React开发的Web应用”。

### 获取项目所在的Git仓库信息
从Git远程仓库地址或`package.json`文件中的仓库字段中获取相关信息，并将SSH地址转换为HTTPS格式。

### 提取项目标签
使用`node {skill_path}/scripts/utils/fetch-tags.mjs --hub {hub}`函数来获取项目标签。

| 标签类型 | 匹配方法 |
|----------|--------------|
| **techStackTags** | 根据`package.json`中的依赖项与标签进行匹配 |
| **platformTags** | 从相关对话内容中提取（例如：Claude Code、Cursor等） |
| **modelTags** | 从对话内容中提取（例如：Claude 3.5、GPT-4等模型） |
| **categoryTags** | 根据项目类型进行推断（例如：游戏库 → 游戏；图表 → 数据可视化工具） |

---

## 第4步：确认发布

显示项目的元数据，并使用`AskUserQuestion`函数获取用户的确认：

```
Publishing to MyVibe:
──────────────────────
Title: [value]

Description:
[50-150 word story]

GitHub: [URL or "Not detected"]
Cover Image: [Will be included if ready]

Tags: Tech Stack: [...] | Platform: [...] | Category: [...] | Model: [...]
```

选项包括：“发布”或“编辑详情”。

---

## 第5步：执行发布

**检查依赖项**：如果`scripts/node_modules`目录缺失，请先运行`npm install`命令。
发布脚本会自动读取截图结果文件。然后直接执行发布操作。

配置信息可以通过标准输入（stdin）传递：

```bash
node {skill_path}/scripts/publish.mjs --config-stdin <<'EOF'
{
  "source": { "type": "dir", "path": "./dist", "did": "z2qaXXXX" },
  "hub": "https://www.myvibe.so",
  "metadata": {
    "title": "My App",
    "description": "Story description here",
    "visibility": "public",
    "githubRepo": "https://github.com/user/repo",
    "platformTags": [1, 2],
    "techStackTags": [3, 4],
    "categoryTags": [5],
    "modelTags": [6]
  }
}
EOF
```

- `did`参数是可选的，用于指定版本更新信息。
- `coverImage`图片会自动从`/tmp/myvibe-screenshot-{hash}.json`文件中读取。
- 发布完成后，截图结果文件会被清理。

---

## 第6步：返回结果

发布脚本完成后，请检查脚本的输出结果，确保包含以下信息：

### 成功消息
务必在响应中包含项目的Vibe URL：

```
Published successfully!
🔗 [URL]
```

### 升级提示（重要）
当更新现有Vibe且未启用版本历史记录功能时，脚本会显示升级提示：

```
📦 Previous version overwritten. Want to keep version history?
   Upgrade to Creator → {hub}/pricing
```

**如果脚本输出中包含此提示，**您必须在响应中向用户明确说明这一点。**这有助于免费用户了解版本历史记录的功能。

---

## 错误处理

| 错误类型 | 处理方式 |
|-------|--------|
| 依赖项缺失 | 在`scripts`目录中运行`npm install`命令 |
| 401/403认证错误 | 自动清除令牌，重新运行脚本以获取授权 |
| 构建失败 | 分析错误原因，提供修复方案或直接发布源代码 |
| 截图生成失败 | 跳过`coverImage`步骤，继续执行发布 |
| 未安装`agent-browser` | 安装`agent-browser`：`npm install -g agent-browser && agent-browser install` |
| 脚本执行失败（网络问题或沙箱环境问题） | 检查网络权限是否已启用。如果需要，请添加`sandbox_permissions.require_escalated`选项并重新尝试 |
- **私有模式仅限Creator和Studio用户使用**：如果出现“私有模式仅限Creator和Studio用户使用”的错误，请使用`AskUserQuestion`函数询问用户：
    **问题：**“私有模式需要Creator或Studio订阅。您希望如何继续？”
    **选项：**  
        - **1**：**以公共模式发布**：您的Vibe将对所有用户可见。您可以在升级后更改此设置。  
        - **2**：**查看升级选项**：打开定价页面以了解包含私有发布功能的订阅计划。  
    **根据用户选择执行相应的操作：**  
        - 如果用户选择选项1，以公共模式重新发布Vibe，并告知用户Vibe现在已设置为公共模式。  
        - 如果用户选择选项2，显示定价页面`{hub}/pricing`并停止发布流程。

## 注意事项

- 必须为项目生成有意义的标题和描述，切勿使用目录名称作为标题。
- 在发布前务必获取用户的确认。
- 默认的MyVibe平台URL为`https://www.myvibe.so/`。
- 每次发布时都会从API中重新获取项目标签信息。
- 发布记录会保存在`~/.myvibe/published.yaml`文件中，以便自动更新版本信息。
- 使用`--new`参数可以强制创建新的Vibe，而不是更新现有Vibe。