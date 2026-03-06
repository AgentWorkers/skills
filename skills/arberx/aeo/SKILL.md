---
name: aeo
description: Run AEO audits, fix site issues, validate schema, generate llms.txt, and compare sites.
allowed-tools:
  - Bash(npx *)
  - Bash(aeo-audit *)
  - Bash(curl *)
  - Read
  - Edit
  - Write
  - Glob
  - Grep
context: fork
argument-hint: [audit|fix|schema|llms|monitor] <url> [--compare <url2>]
---

# AEO

官方网站：[ainyc.ai](https://ainyc.ai)

AEO 提供了一套工具，用于审计网站、修复代码问题、验证 JSON-LD 标签格式以及监控网站性能。

## 功能模式

- **audit**：对网站进行评估和诊断。
- **fix**：在审计完成后应用代码修改。
- **schema**：验证 JSON-LD 标签的正确性及实体数据的一致性。
- **llms**：生成或优化 `llms.txt` 和 `llms-full.txt` 文件。
- **monitor**：跟踪网站的变化或与竞争对手进行对比分析。

如果未指定模式，系统将默认使用 **audit** 模式。

## 使用示例

- `audit https://example.com`  
- `fix https://example.com`  
- `schema https://example.com`  
- `llms https://example.com`  
- `monitor https://site-a.com --compare https://site-b.com`  

## 模式选择

- 如果命令的第一个参数是 `audit`、`fix`、`schema` 或 `monitor`，则直接使用该模式。  
- 如果未明确指定模式，系统会根据请求的意图自动选择 `audit` 模式。  

### Audit（审计）

适用于以下场景：  
- “审计这个网站”  
- “为什么我的网站没有被搜索引擎收录？”  

**操作步骤：**  
1. 运行相关命令（代码块：```bash
   npx @ainyc/aeo-audit@latest $ARGUMENTS --format json
   ```）  
2. 返回结果：  
  - 网站的总体评分和概况  
  - 问题分析  
  - 主要优点  
  - 需要修复的错误  
  - 诸如页面加载时间、辅助文件可用性等元数据  

### Fix（修复）

适用于用户希望在审计后修改代码的情况。  

**操作步骤：**  
1. 运行相关命令（代码块：```bash
   npx @ainyc/aeo-audit@latest $ARGUMENTS --format json
   ```）  
2. 查找状态为 `partial` 或 `fail` 的问题。  
3. 在当前代码库中针对性地修复这些问题。  
4. 优先处理以下方面：  
  - 结构化数据及 JSON-LD 标签的完整性  
  `llms.txt` 和 `llms-full.txt` 文件的内容  
  网站的可爬取性（如 `robots.txt` 文件）  
  常见问题解答（FAQ）的展示方式  
  页面内容的更新频率  

**注意事项：**  
- 除非用户明确要求，否则不要删除现有的 JSON-LD 标签或内容。  
- 请保持代码风格和格式的一致性。  
- 如果修复操作存在风险或含义不明确，请在修改前向用户说明可能的影响。  

### Schema（验证 JSON-LD 标签）

适用于需要检查 JSON-LD 标签质量的情况。  

**操作步骤：**  
1. 运行相关命令（代码块：```bash
   npx @ainyc/aeo-audit@latest $ARGUMENTS --format json --factors structured-data,schema-completeness,entity-consistency
   ```）  
2. 报告以下信息：  
  - 网站中使用的 JSON-LD 标签类型  
  - 各类型标签的完整性  
  - 缺失的推荐标签  
  - 实体数据的一致性问题  
- 如有必要，提供修正后的 JSON-LD 标签示例。  

**检查项：**  
- `LocalBusiness`：名称、地址、电话、营业时间、价格范围、图片、网址、地理位置、服务区域  
- `FAQPage`：包含至少 3 个问题与答案的对  
- `HowTo`：名称及至少 3 个操作步骤  
- `Organization`：名称、标志、联系方式、成立日期、网址、描述  

### llms.txt（生成 AI 可读文件）

适用于用户需要生成或优化 `llms.txt` 或 `llms-full.txt` 文件的情况。  

**操作步骤：**  
- 如果提供了网址：  
  1. 运行相关命令（代码块：```bash
   npx @ainyc/aeo-audit@latest $ARGUMENTS --format json --factors ai-readable-content
   ```）  
  2. 检查网站中是否存在 AI 可读的文件（如 `llms.txt`）。  
  3. 从网站中提取关键信息并生成新的文件。  
- 如果未提供网址：  
  1. 分析当前网站的结构和内容。  
  2. 提取企业的名称、服务信息、常见问题解答、联系方式及元数据。  
  3. 生成 `llms.txt` 和 `llms-full.txt` 文件。  
- 生成完成后：  
  - 在适当的位置添加 `<link rel="alternate" type="text/markdown" href="/llms.txt">` 链接。  
  - 建议将生成的文件添加到网站的站点地图中。  

### Monitor（监控）

适用于用户需要跟踪网站变化或与竞争对手进行对比的情况。  

**操作步骤：**  
- 对单个网址进行审计。  
- 如果存在审计历史记录（文件路径：`.aeo-audit-history/`），则与历史数据对比。  
- 显示整体评分及各指标的变化情况。  
- 保存当前的审计结果。  

**对比模式：**  
- 使用 `--compare <url2>` 参数进行对比分析。  
- 同时审计两个网站，展示各项指标的差异。  
- 突出网站的优势、劣势及需要改进的地方。  

**其他注意事项：**  
- 如果任务需要部署到实际网站但未提供网址，系统会要求用户提供网址。  
- 仅进行诊断时，系统不会修改文件。  
- 对于修复请求，系统会在修改后重新进行审计以验证效果。  
- 如果 `npx` 命令执行失败，建议安装 `npm install -g @ainyc/aeo-audit`。  
- 如果目标网址无法访问或不是 HTML 格式，系统会报告具体错误原因。  
- 系统提供的建议应基于实际数据，避免泛泛而空的 SEO 建议。