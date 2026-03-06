---
name: aeo-audit
description: 执行AEO审计（反走私审计），修复网站问题，验证数据模式（schema），生成llms.txt文件，并对各个网站进行比较。
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
argument-hint: <url> [--compare <url2>]
---
# AEO

官方网站：[ainyc.ai](https://ainyc.ai)

本工具用于审计并优化人工智能系统对网站的理解、内容提取及引用能力。

## 主要功能

- 全面进行AEO审计并生成评分报告  
- 修复网站中存在的AEO相关问题（如信号弱或缺失）  
- 验证JSON-LD格式及数据结构  
- 生成`llms.txt`和`llms-full.txt`文件  
- 提供网站改进前后的对比数据  

## 常见请求  

- `Audit https://example.com`（审计网站）  
- `Fix AEO issues for https://example.com in this repo`（修复该仓库中的AEO问题）  
- `Validate schema for https://example.com`（验证网站的JSON-LD格式）  
- `Generate llms.txt for this project`（为该项目生成`llms.txt`文件）  
- `Compare https://site-a.com --compare https://site-b.com`（比较两个网站）  

## 功能模式选择  

- **Audit**：用于评估网站质量、诊断问题或进行基准测试。  
- **Fix**：用户需要修改代码时使用。  
- **Schema**：用于验证JSON-LD格式、检查缺失的属性或确保实体数据的一致性。  
- **llms.txt**：用户需要生成AI可读取的Markdown格式文件时使用。  
- **Monitor**：用于跟踪项目进度或比较不同网站的表现。  

## Audit（审计）  

适用于“审计这个网站”或“为什么我的网站没有被正确引用？”等需求。  
1. 运行相应命令：  
   ```bash
   npx @ainyc/aeo-audit@latest $ARGUMENTS --format json
   ```  
2. 返回结果：  
   - 总体评分  
- 问题分析  
- 主要优点  
- 需要修复的问题  
- 其他相关信息（如数据获取时间、辅助文件的可用性等）  

## Fix（修复）  

用户希望在审计后修改代码时使用该模式。  
1. 运行相应命令：  
   ```bash
   npx @ainyc/aeo-audit@latest $ARGUMENTS --format json
   ```  
2. 查找状态为“partial”或“fail”的问题  
3. 在当前代码库中针对性地修复这些问题  
4. 优先处理以下方面：  
   - 结构化数据与数据结构的完整性  
   - `llms.txt`和`llms-full.txt`文件的生成  
   - 网站爬虫的访问权限设置（`robots.txt`文件）  
   - 与搜索引擎相关的元数据（E-E-A-T信号）  
   - 常见问题解答（FAQ）的标记  
   - 内容的更新频率  

**注意事项：**  
- 除非用户明确要求，否则不要删除现有的数据结构或内容。  
- 保持代码的风格和格式不变。  
- 如果修复方案存在风险或含义不明确，请在修改前向用户说明可能的影响。  

## Schema（验证数据结构）  

适用于需要专门检查JSON-LD格式或数据结构质量的情况。  
1. 运行相应命令：  
   ```bash
   npx @ainyc/aeo-audit@latest $ARGUMENTS --format json --factors structured-data,schema-completeness,entity-consistency
   ```  
2. 报告结果：  
   - 检测到的数据结构类型  
- 各类型属性的完整情况  
- 缺失的推荐属性  
- 实体数据的一致性问题  
- 如有必要，提供修正后的JSON-LD示例  

**检查清单：**  
- `LocalBusiness`：名称、地址、电话、营业时间、价格范围、图片、网址、地理位置、服务区域  
- `FAQPage`：至少包含3个问答对的页面  
- `HowTo`：页面名称及至少3个操作步骤  
- `Organization`：名称、标志、联系方式、成立日期、网址、描述  

## llms.txt（生成AI可读取的Markdown文件）  

用户需要生成或优化`llms.txt`或`llms-full.txt`文件时使用该模式。  
- 如果提供了网址：  
  1. 运行相应命令：  
    ```bash
   npx @ainyc/aeo-audit@latest $ARGUMENTS --format json --factors ai-readable-content
   ```  
  2. 检查是否存在AI可读取的Markdown文件  
  3. 从网站中提取关键内容  
  4. 生成优化后的`llms.txt`和`llms-full.txt`文件  
- 如果未提供网址：  
  1. 检查当前项目的数据  
  2. 提取企业的名称、服务信息、常见问题解答、联系方式及元数据  
  3. 从本地数据源生成所需的文件  

**生成文件后的操作：**  
- 在适当的情况下，添加以下链接：  
  `<link rel="alternate" type="text/markdown" href="/llms.txt">`  
- 建议将生成的文件添加到网站的站点地图中。  

## Monitor（进度跟踪/对比）  

用户需要跟踪项目进度或比较不同网站的表现时使用该模式。  
- 对单个网址进行审计：  
  1. 运行审计命令  
  2. 与之前的审计结果（存储在`.aeo-audit-history/`目录中）进行对比  
  3. 显示整体评分及各项指标的差异  
- 保存当前审计结果  

**对比功能：**  
- 使用`--compare <url2>`参数进行对比  
- 同时审计两个网站  
- 以表格形式显示各项指标的差异  
- 突出优势、劣势及需要改进的地方  

**操作规范：**  
- 如果任务需要部署到实际网站但未提供网址，请要求用户提供相关信息。  
- 仅用于诊断目的时，不要直接修改文件。  
- 对于修复请求，完成修改后请重新运行审计以验证效果。  
- 如果`npx`命令执行失败，建议安装`npm install -g @ainyc/aeo-audit`。  
- 如果网址无法访问或内容不是HTML格式，请详细报告错误原因。  
- 建议提供基于事实的、具体的改进建议，而非泛化的SEO建议。