---
name: audit-website
description: 使用 squirrelscan CLI 对网站进行审计，涵盖 SEO、性能、安全、技术、内容等 15 个方面的问题，共计 230 多条审计规则。该工具会生成经过 LLM（Large Language Model）优化的报告，其中包含网站的健康状况评分、失效链接信息、元标签分析结果以及可操作的改进建议。通过这些报告，您可以发现并评估网站或 Web 应用程序存在的问题及其整体健康状况。
license: See LICENSE file in repository root
compatibility: Requires squirrel CLI installed and accessible in PATH
metadata:
  author: squirrelscan
  version: "1.22"
allowed-tools: Bash(squirrel:*) Read Edit Grep Glob
---

# 网站审计技能

使用`squirrelscan`命令行工具（CLI）对网站进行SEO、技术、内容、性能和安全性方面的审计。

`squirrelscan`提供了一个名为`squirrel`的CLI工具，支持macOS、Windows和Linux系统。该工具通过模拟浏览器和搜索引擎爬虫来执行全面的网站审计，并根据230多项规则分析网站的结构和内容。

审计完成后，它会列出存在的问题以及相应的修复建议。

## 链接

- `squirrelscan`的官方网站：[https://squirrelscan.com](https://squirrelscan.com)
- 文档（包括规则参考）：[docs.squirrelscan.com](https://docs.squirrelscan.com)

你可以使用以下模板查找任何规则的详细信息：

```bash
https://docs.squirrelscan.com/rules/{rule_category}/{rule_id}
```

**示例：**  
```bash
https://docs.squirrelscan.com/rules/links/external-links
```

## 该技能的功能

该技能使AI代理能够根据21个类别中的230多项规则对网站进行审计，具体包括：

- **SEO问题**：元标签、标题、描述、规范URL、Open Graph标签
- **技术问题**：失效链接、重定向链、页面速度、移动设备兼容性
- **性能**：页面加载时间、资源使用情况、缓存
- **内容质量**：标题结构、图片alt文本、内容分析
- **安全性**：泄露的敏感信息、HTTPS使用情况、安全头部信息、混合内容
- **可访问性**：alt文本、颜色对比度、键盘导航
- **可用性**：表单验证、错误处理、用户流程
- **链接**：检查内部和外部链接的有效性
- **E-E-A-T**（专家性、经验、权威性、可信度）
- **用户体验**：用户流程、错误处理、表单验证
- **移动设备**：检查移动设备兼容性、响应式设计、触控友好性
- **可爬取性**：检查可爬取性、robots.txt文件、sitemap.xml文件等
- **Schema**：Schema.org标记、结构化数据、丰富片段
- **法律合规性**：遵守法律要求、隐私政策、服务条款
- **社交媒体**：Open Graph标签、Twitter卡片、schema验证等
- **URL结构**：URL长度、连字符使用、关键词
- **关键词**：关键词填充
- **内容**：内容结构、标题
- **图片**：alt文本、颜色对比度、图片大小、图片格式
- **本地SEO**：NAP一致性、地理元数据
- **视频**：VideoObject标记、可访问性

审计过程会爬取网站，根据审计规则分析每个页面，并生成一份详细的报告，内容包括：
- **整体健康评分（0-100分）**
- **类别细分（核心SEO、技术SEO、内容、安全）**
- **受影响URL的具体问题**
- **失效链接检测**
- **可操作的修复建议**
- 规则分为错误、警告和通知三个级别，并且每个规则都有一个1到10的等级

## 适用场景

当你需要执行以下操作时，可以使用该技能：
- 分析网站的健康状况
- 调试技术SEO问题
- 修复上述所有问题
- 检查失效链接
- 验证元标签和结构化数据
- 生成网站审计报告
- 比较修改前后的网站健康状况
- 提高网站性能、可访问性、SEO效果和安全性等

建议定期重新审计，以确保网站始终保持良好的状态。

## 先决条件

使用该技能需要安装`squirrel` CLI，并确保它已添加到系统的`PATH`环境变量中。

**安装方式：** [squirrelscan.com/download](https://squirrelscan.com/download)

**验证安装：**  
```bash
squirrel --version
```

## 设置

运行`squirrel init`命令在当前目录下创建一个`squirrel.toml`配置文件。如果文件不存在，则创建一个并指定项目名称：

```bash
squirrel init -n my-project
# overwrite existing config
squirrel init -n my-project --force
```

## 使用方法

### 简介

你可以执行三个主要的操作，这些操作的结果都会被缓存到本地项目数据库中：
- `crawl`：用于执行爬取或刷新爬取任务，或继续已进行的爬取
- `analyze`：用于分析爬取结果
- `report`：用于生成所需格式的报告（如LLM、文本、控制台、HTML等）

`audit`命令是这三个操作的封装，会按顺序执行它们：

```bash
squirrel audit https://example.com --format llm
```

**推荐使用`llm`格式**：这种格式专为审计设计，输出既全面又简洁。

**首次扫描**应该是**表面扫描**，即快速且浅层的扫描，用于收集关于网站的基本信息（如结构、内容和技术栈）。这种扫描不会对网站性能产生影响。

**第二次扫描**应该是**深度扫描**，会对网站进行彻底且详细的分析，以获取更多信息（如安全性、性能和可访问性）。这种扫描可能需要更多时间，并可能对网站性能产生影响。

如果用户没有提供具体的网站地址，可以询问他们希望审计哪个URL。

**建议审计实时网站**——只有实时网站才能真实反映网站的实际情况和性能问题。

如果你需要审计本地网站和实时网站，应提示用户选择目标网站，并建议他们选择实时网站。

你可以将审计结果中的修复建议应用到实时网站上。

在规划审计任务时，可以考虑让多个代理同时执行，以加快修复速度。在实施修复后，需要验证代码是否仍然能够通过项目中的所有检查。

### 基本工作流程

审计过程分为两个步骤：
1. **执行审计**（将结果保存到数据库，并在控制台显示输出）
2. **导出报告**（选择所需的格式）

```bash
# Step 1: Run audit (default: console output)
squirrel audit https://example.com

# Step 2: Export as LLM format
squirrel report <audit-id> --format llm
```

### 回归差异检测

当需要检测审计结果之间的变化时，可以使用`diff`模式：

```bash
# Compare current report against a baseline audit ID
squirrel report --diff <audit-id> --format llm

# Compare latest domain report against a baseline domain
squirrel report --regression-since example.com --format llm
```

`diff`模式支持`console`、`text`、`json`、`llm`和`markdown`格式。`html`和`xml`格式不支持。

### 运行审计

执行审计时：
1. **展示审计结果**：向用户展示审计结果和评分
2. **提出修复建议**：列出可修复的问题，并在用户确认后进行修复
3. **并行处理已批准的修复**：使用代理来批量修改内容（如alt文本、标题、描述）
4. **迭代处理**：修复一批问题 → 重新审计 → 展示结果 → 提出下一批问题
5. **暂停以供审核**：对于失效链接、结构变化或存在疑问的问题，需要用户进行审核
6. **展示修改前后的对比**：每次修复后展示评分对比结果

- **迭代流程**：修复一批问题后，重新审计，直到达到目标评分（通常为85分以上），或者只剩下需要人工判断的问题（例如：“这个链接是否应该删除？”）
- **平等对待所有修复**：代码修改和内容修改同样重要。
- **并行处理内容修复**：对于涉及多个文件的修复，可以创建多个代理来同时处理：
  - 例如：7个文件需要添加alt文本 → 创建1-2个代理来处理
  - 例如：30个文件有标题问题 → 创建代理来批量处理
- **完成标准**：
  - 所有错误都已修复
  - 所有警告都已修复（或记录为需要人工审核）
  - 重新审计确认改进效果
  - 向用户展示修改前后的对比结果

修复完成后，询问用户是否需要查看修改内容。

### 评分标准

| 起始评分 | 目标评分 | 需要完成的工作 |
|----------------|--------------|---------------|
| < 50（F级） | 75+（C级） | 需要重大修复 |
| 50-70（D级） | 85+（B级） | 需要中等程度的修复 |
| 70-85（C级） | 90+（A级） | 需要细微调整 |
| > 85（B+级） | 95+ | 需要进一步优化 |

只有当评分达到95分（A级）且覆盖范围设置为`FULL`时，才能认为网站已经完成并修复完毕。

### 问题分类

| 问题类别 | 修复方法 | 是否可以并行处理 |
|----------|--------------|----------------|
| 元标签/标题 | 修改页面组件或元数据 | 不支持并行处理 |
| 结构化数据 | 在页面模板中添加JSON-LD | 不支持并行处理 |
| 缺失的H1标题 | 修改页面组件和内容文件 | 支持并行处理 |
| 图片alt文本 | 修改内容文件 | 支持并行处理 |
| 标题层级 | 修改内容文件 | 支持并行处理 |
| 简短描述 | 修改内容前置内容 | 支持并行处理 |
| HTTP→HTTPS链接 | 在内容中查找并替换链接 | 支持并行处理 |
| 失效链接 | 需要用户手动审核 | 不支持并行处理 |

**对于可以并行处理的修复**：为每个需要修复的文件创建相应的代理。

### 内容文件修复

许多问题需要修改内容文件，这些修复与代码修复同样重要：
- **图片alt文本**：为图片添加描述性alt文本
- **标题层级**：修复缺失的标题层级
- **元描述**：扩展内容前置内容中的描述
- **HTTP链接**：将不安全的链接更新为HTTPS链接

### 使用代理并行处理修复

用户批准一批修复建议后，可以使用代理来并行执行修复：
- **先征得用户同意**：在创建代理之前，务必确认要修复的具体内容
- 每个代理负责处理3-5个相同类型的文件
- 只处理独立的文件（避免处理共享组件或配置文件）
- 在一条消息中创建多个代理以并行执行修复任务

### 高级选项

- 审计更多页面：  
```bash
squirrel audit https://example.com --max-pages 200
```

- 强制重新爬取（忽略缓存）：  
```bash
squirrel audit https://example.com --refresh
```

- 恢复中断的爬取：  
```bash
squirrel audit https://example.com --resume
```

- 详细输出（用于调试）：  
```bash
squirrel audit https://example.com --verbose
```

## 常用选项

### 审计命令选项

| 选项 | 别名 | 描述 | 默认值 |
|--------|-------|-------------|---------|
| `--format <fmt>` | `-f <fmt>` | 输出格式：控制台、文本、JSON、HTML、Markdown、LLM | 控制台 |
| `--coverage <mode>` | `-C <mode>` | 覆盖范围模式：快速、表面、全面 | 表面 |
| `--max-pages <n>` | `-m <n>` | 最大爬取页数（最多5000页） | 根据覆盖范围而定 |
| `--output <path>` | `-o <path>` | 输出文件路径 | - |
| `--refresh` | `-r` | 忽略缓存，重新获取所有页面 | 不推荐 |
| `--resume` | - | 恢复中断的爬取 | 不推荐 |
| `--verbose` | `-v` | 详细输出 | 不推荐 |
| `--debug` | - | 开启调试日志 | 不推荐 |
| `--trace` | - | 启用性能跟踪 | 不推荐 |
| `--project-name <name>` | `-n <name>` | 覆盖项目名称 | 可从配置文件中设置 |

### 覆盖范围模式

根据审计需求选择合适的覆盖范围模式：
| 模式 | 默认页数 | 行为 | 使用场景 |
|------|---------------|----------|----------|
| `quick` | 25 | 仅爬取种子页面和sitemaps，不检测链接 | 用于持续集成（CI）检查和快速健康检查 |
| `surface` | 100 | 每个URL模式只爬取一个样本 | 通用审计（默认） |
| `full` | 500 | 爬取所有页面 | 深度分析 |

**表面模式**非常高效**——它会检测如`/blog/{slug}`或`/products/{id}`这样的URL模式，并仅爬取每个模式的一个样本。这种模式适用于页面结构相似的网站（如博客或电子商务网站）。

**每种模式的适用场景：**
- `quick`：适用于持续集成管道、日常健康检查、监控
- `surface`：适用于大多数常规审计，能高效覆盖独特模板
- `full`：适用于项目发布前进行全面分析

### 报告命令选项

| 选项 | 别名 | 描述 |
|--------|-------|-------------|
| `--list` | `-l` | 列出最近的审计结果 |
| `--severity <level>` | - | 按严重程度过滤：错误、警告、全部 |
| `--category <cats>` | - | 按类别过滤（用逗号分隔） |
| `--format <fmt>` | `-f <fmt>` | 输出格式：控制台、文本、JSON、HTML、Markdown、XML、LLM |
| `--output <path>` | `-o <path>` | 输出文件路径 |
| `--input <path>` | `-i <path>` | 从JSON文件加载数据（备用方式） |

### 配置相关命令

| 命令 | 描述 |
|---------|-------------|
| `config show` | 显示当前配置 |
| `config set <key> <value>` | 设置配置值 |
| `config path` | 显示配置文件路径 |
| `config validate` | 验证配置文件 |

### 其他命令

| 命令 | 描述 |
|---------|-------------|
| `squirrel feedback` | 向`squirrelscan`团队发送反馈 |
| `squirrel skills install` | 安装Claude Code技能 |
| `squirrel skills update` | 更新Claude Code技能 |

### 自管理命令

`squirrel self`下的自我管理命令：
| 命令 | 描述 |
|---------|-------------|
| `self install` | 初始化本地安装 |
| `self update` | 检查并应用更新 |
| `self completion` | 生成Shell命令补全提示 |
| `self doctor` | 运行健康检查 |
| `self version` | 显示版本信息 |
| `self settings` | 管理CLI设置 |
| `self uninstall` | 从系统中卸载`squirrel` |

## 输出格式

### 控制台输出（默认）

`audit`命令默认以人类可读的控制台输出格式显示结果，包含颜色编码和进度指示。

### LLM格式

若想获得优化后的LLM格式输出，可以使用`report`命令并指定`--format llm`：

```bash
squirrel report <audit-id> --format llm
```

LLM格式是一种紧凑的XML/文本混合格式，旨在提高效率（比详细输出格式节省40%的字符空间）：
- **总结**：整体健康评分和关键指标
- **问题分类**：按审计规则类别分组（核心SEO、技术、内容、安全）
- **失效链接**：列出失效的外部和内部链接
- **修复建议**：按优先级排列的修复事项

详细格式规范请参考[OUTPUT-FORMAT.md](references/OUTPUT-FORMAT.md)。

## 示例

### 示例1：使用LLM格式的快速网站审计

```bash
# User asks: "Check squirrelscan.com for SEO issues"
squirrel audit https://squirrelscan.com --format llm
```

### 示例2：大型网站的深度审计

```bash
# User asks: "Do a thorough audit of my blog with up to 500 pages"
squirrel audit https://myblog.com --max-pages 500 --format llm
```

### 示例3：修改后的重新审计

```bash
# User asks: "Re-audit the site and ignore cached results"
squirrel audit https://example.com --refresh --format llm
```

### 示例4：两步审计流程（复用之前的审计结果）

```bash
# First run an audit
squirrel audit https://example.com
# Note the audit ID from output (e.g., "a1b2c3d4")

# Later, export in different format
squirrel report a1b2c3d4 --format llm
```

## 输出

审计完成后，向用户展示所有所做的修改。

## 故障排除

### 错误：`squirrel command not found`

如果出现此错误，说明`squirrel`未安装或未添加到`PATH`环境变量中。
**解决方法：**
1. 安装`squirrel`：[squirrelscan.com/download](https://squirrelscan.com/download)
2. 确保`~/.local/bin`在`PATH`中。
3. 运行`squirrel --version`验证安装是否成功。

### 权限问题

如果`squirrel`不可执行，可能是权限问题。重新安装`squirrel`（从[https://squirrelscan.com/download]下载）即可解决。

### 爬取超时或性能缓慢

对于非常大的网站，审计过程可能需要几分钟。可以使用`--verbose`选项查看进度：

```bash
squirrel audit https://example.com --format llm --verbose
```

### 无效URL

确保URL包含协议（`http://`或`https://`）：

```bash
# ✗ Wrong
squirrel audit example.com

# ✓ Correct
squirrel audit https://example.com
```

## 工作原理

1. **爬取**：从指定URL开始爬取所有页面。
2. **分析**：对每个页面应用审计规则。
3. **检查外部链接**：验证外部链接的有效性。
4. **生成报告**：生成优化后的报告。

审计结果会保存在本地数据库中，可以使用`squirrel report`命令查看。

## 额外资源

- **输出格式参考**：[OUTPUT-FORMAT.md](references/OUTPUT-FORMAT.md)
- **squirrelscan官方文档**：[https://docs.squirrelscan.com]
- **CLI帮助文档**：`squirrel audit --help`