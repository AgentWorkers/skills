---
name: aeo
description: 执行AEO审计（反走私审计），修复网站问题，验证数据模式（schema），生成llms.txt文件，并对各个网站进行比较。
allowed-tools:
  - Bash(npx @ainyc/aeo-audit@latest *)
  - Bash(npx @ainyc/aeo-audit *)
  - Bash(aeo-audit *)
  - Bash(pnpm run build)
  - Bash(node bin/aeo-audit.js *)
  - Read
  - Edit(*.html)
  - Edit(*.json)
  - Edit(*.md)
  - Edit(*.txt)
  - Edit(*.xml)
  - Write(llms.txt)
  - Write(llms-full.txt)
  - Glob
  - Grep
---
# AEO

官方网站：[ainyc.ai](https://ainyc.ai)

这是一个用于审计、修复代码、验证JSON-LD格式、生成`llms.txt`文件以及监控网站状态的工具。

## 命令选择

- 使用 `npx @ainyc/aeo-audit@latest ...` 对已部署的网站进行审计（这些网站使用了发布的软件包）。
- 如果在本地仓库中工作并需要验证未发布的更改，请先运行 `pnpm run build`，然后使用 `node bin/aeo-audit.js ...`。

## 参数安全

**切勿直接将用户输入插入到shell命令中。**始终遵循以下规则：
1. 确保URL以 `https://` 或 `http://` 开头，并且不包含任何shell元字符。
2. 每个参数都必须用引号括起来（例如：`npx @ainyc/aeo-audit@latest "https://example.com" --format json`）。
3. 将所有参数作为独立的字符串传递，切勿从用户输入的原始文本中构建命令字符串。
4. 拒绝包含以下字符的参数：`;`, `|`, `&`, `$`, `` ` ``, `(`, `)`, `{`, `}`, `<`, `>`, 或换行符。

## 模式

- `audit`：对网站进行评分和诊断。
- `fix`：在审计后应用代码更改。
- `schema`：验证JSON-LD格式和实体的一致性。
- `llms`：生成或更新`llms.txt`和`llms-full.txt`文件。
- `monitor`：比较网站随时间的变化情况或与竞争对手的差异。

如果未指定模式，默认使用`audit`模式。

## 示例用法

- `audit https://example.com`  
- `fix https://example.com`  
- `schema https://example.com`  
- `llms https://example.com`  
- `monitor https://site-a.com --compare https://site-b.com`  

## 模式选择

- 如果第一个参数是`audit`、`fix`、`schema`、`llms`或`monitor`之一，则使用相应的模式。
- 如果未明确指定模式，系统会根据请求的意图自动选择默认模式`audit`。

## 审计（Audit）

适用于“审计这个网站”或“为什么我的网站没有被引用？”等需求。

1. 运行命令：
   ```bash
   npx @ainyc/aeo-audit@latest "<url>" [flags] --format json
   ```  
   （本地仓库的替代命令：```bash
   node bin/aeo-audit.js "<url>" [flags] --format json
   ```）
2. 返回结果：
   - 总体评分和得分  
   - 详细分析  
   - 主要优势  
   - 需要修复的问题  
   - 其他相关信息（如请求时间、辅助文件的可用性等）

## 修复（Fix）

当用户希望在审计后应用代码更改时使用此模式。

1. 运行命令：
   ```bash
   npx @ainyc/aeo-audit@latest "<url>" [flags] --format json
   ```  
   （本地仓库的替代命令：```bash
   node bin/aeo-audit.js "<url>" [flags] --format json
   ```）
2. 查找状态为`partial`或`fail`的错误项。
3. 在当前代码库中应用相应的修复措施。
4. 优先处理以下方面：
   - 数据的结构和完整性  
   `llms.txt`及`llms-full.txt`文件的内容  
   `robots.txt`文件的配置  
   与搜索引擎的兼容性（E-E-A-T信号）  
   常见问题解答（FAQ）的标记  
   内容的更新频率  

**注意事项：**
- 除非用户明确要求，否则不要删除现有的结构或内容。
- 保持原有的代码风格和格式。
- 如果修复操作存在风险或含义不明确，请在编辑前向用户说明可能的后果。

## 验证JSON-LD格式（Schema）

当用户需要检查JSON-LD格式的质量时使用此模式。

1. 运行命令：
   ```bash
   npx @ainyc/aeo-audit@latest "<url>" [flags] --format json --factors structured-data,schema-completeness,entity-consistency
   ```  
   （本地仓库的替代命令：```bash
   node bin/aeo-audit.js "<url>" [flags] --format json --factors structured-data,schema-completeness,entity-consistency
   ```）
2. 报告以下信息：
   - 找到的JSON-LD类型  
   各类型的属性完整性  
   缺失的推荐属性  
   实体一致性问题  
- 如有必要，提供修正后的JSON-LD示例。

**检查清单：**
- `LocalBusiness`：名称、地址、电话、营业时间、价格范围、图片、网址、地理位置、服务区域  
- `FAQPage`：至少包含3个问答对的页面  
- `HowTo`：页面名称及至少3个操作步骤  
- `Organization`：名称、标志、联系方式、成立日期、网址、描述  

## 生成`llms.txt`文件（LLMS）

当用户需要生成或更新`llms.txt`或`llms-full.txt`文件时使用此模式。

- 如果提供了URL：
  1. 运行命令：
    ```bash
   npx @ainyc/aeo-audit@latest "<url>" [flags] --format json --factors ai-readable-content
   ```  
    （本地仓库的替代命令：```bash
   node bin/aeo-audit.js "<url>" [flags] --format json --factors ai-readable-content
   ```）
  2. 检查网站中是否存在AI可识别的内容。
  3. 从网站中提取关键信息，并生成改进后的`llms.txt`和`llms-full.txt`文件。
- 如果未提供URL：
  1. 检查当前项目的内容。
  2. 提取企业的名称、服务信息、常见问题解答、联系方式及元数据。
  3. 从本地数据源生成这两个文件。
- 生成完成后，根据需要添加 `<link rel="alternate" type="text/markdown" href="/llms.txt">` 链接。
- 建议将这两个文件添加到网站的站点地图中。

## 监控（Monitor）

当用户需要跟踪网站的变化或与竞争对手进行对比时使用此模式。

- 提供一个URL，然后运行审计命令。
- 如果之前有审计记录（存储在`.aeo-audit-history/`目录中），则与之前的结果进行对比。
- 显示整体得分及各指标的变化情况。
- 保存当前的审计结果。

**比较模式（Comparison Mode）：**
- 使用 `--compare <url2>` 参数来比较两个网站。
- 对两个网站进行审计。
- 显示各项指标的差异。
- 突出优势、劣势及需要改进的地方。

**其他注意事项：**
- 如果任务需要审计已部署的网站但未提供URL，请要求用户提供URL。
- 如果仅需要进行诊断，请勿直接修改文件。
- 如果是修复请求，请在修改后重新运行审计命令以验证效果。
- 如果`npx`命令执行失败，建议先运行 `pnpm run build && node bin/aeo-audit.js` 以在本地进行审计。
- 如果提供的URL无法访问或不是HTML格式，需详细报告错误原因。
- 建议提供基于事实的、具体的改进建议，而非泛泛而空的SEO建议。