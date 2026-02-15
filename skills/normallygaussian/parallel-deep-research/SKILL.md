---
name: parallel-deep-research
description: "**深度多源研究：通过 Parallel API 实现**  
当用户明确要求对某个主题进行深入研究、全面分析或调查时，可使用该功能。如需快速查找信息或获取新闻内容，请改用 **parallel-search** 功能。"
homepage: https://parallel.ai
---

# 并行深度研究  
（Parallel Deep Research）  

该技能用于对复杂主题进行深入、多源的研究，需要整合来自多个来源的信息。研究结果会以包含引用信息的综合报告形式返回。  

## 使用场景  
当用户提出以下请求时，可使用此技能：  
- “对……进行深入研究”  
- “对……进行彻底调查”  
- “提供关于……的全面报告”  
- “全面分析……”  
- 需要整合10个以上来源信息的复杂主题  
- 竞争分析、市场调研、尽职调查  
- 在速度不如深度和准确性重要的场景中  

**不适用场景：**  
- 快速查询或简单问题（使用`parallel-search`）  
- 当前新闻或近期事件（使用`parallel-search`并添加`--after-date`参数）  
- 阅读特定URL的内容（使用`parallel-extract`）  

## 快速入门  
```bash
parallel-cli research run "your research question" --processor pro-fast --json -o ./report
```  

## 命令行接口（CLI）参考  
### 基本用法  
```bash
parallel-cli research run "<question>" [options]
```  

### 常用参数  
| 参数          | 说明                          |  
|--------------|----------------------------------|  
| `-p, --processor <tier>` | 处理器层级（见下表）                |  
| `--json`       | 以JSON格式输出                    |  
| `-o, --output <path>` | 将结果保存到文件（生成.json和.md文件）           |  
| `-f, --input-file <path>` | 从文件中读取查询内容（适用于长问题）          |  
| `--timeout N`     | 最大等待时间（秒，默认：3600秒）                |  
| `--no-wait`     | 立即返回结果，后续通过`research status`查询进度    |  

### 处理器层级  
| 处理器层级       | 处理时间（秒）                          | 适用场景                          |  
|---------------|----------------------------------|  
| `lite-fast`     | 10–20秒        | 快速查询                          |  
| `base-fast`     | 15–50秒        | 简单问题                          |  
| `core-fast`     | 15–100秒        | 中等复杂度研究                      |  
| `pro-fast`     | 30–5分钟       | 探索性研究（默认配置）                   |  
| `ultra-fast`     | 1–10分钟       | 多源深度研究                      |  
| `ultra2x-fast`     | 1–20分钟       | 非常复杂的研究                      |  
| `ultra4x-fast`     | 1–40分钟       | 极为复杂的研究                      |  
| `ultra8x-fast`     | 1分钟–1小时      | 最具挑战性的研究                      |  

非快速处理层级的处理器（如`pro`、`ultra`）处理时间较长，但能使用更新的数据。  

### 示例  
- **基础研究示例**：  
```bash
parallel-cli research run "What are the latest developments in quantum computing?" \
  --processor pro-fast \
  --json -o ./quantum-report
```  
- **深度竞争分析示例**：  
```bash
parallel-cli research run "Compare Stripe, Square, and Adyen payment platforms: features, pricing, market position, and developer experience" \
  --processor ultra-fast \
  --json -o ./payments-analysis
```  
- **从文件中读取的长问题示例**：  
```bash
# Create question file
cat > /tmp/research-question.txt << 'EOF'
Investigate the current state of AI regulation globally:
1. What regulations exist in the US, EU, and China?
2. What's pending or proposed?
3. How do companies like OpenAI, Google, and Anthropic respond?
4. What industry groups are lobbying for/against regulation?
EOF

parallel-cli research run -f /tmp/research-question.txt \
  --processor ultra-fast \
  --json -o ./ai-regulation-report
```  
- **非阻塞式研究示例**：  
```bash
# Start research without waiting
parallel-cli research run "research question" --no-wait

# Check status later
parallel-cli research status <task-id>

# Poll until complete
parallel-cli research poll <task-id> --json -o ./report
```  

## 最佳提示方式  
在提出研究请求时，请撰写2–5句话，明确以下内容：  
- 具体的问题或主题  
- 研究范围（时间范围、地理位置、行业）  
- 最为重要的考量因素（价格？功能？市场份额？）  
- 希望的输出格式（对比表、时间线、优缺点分析）  

**示例提示（良好格式）：**  
```
Compare the top 5 CRM platforms for B2B SaaS companies with 50-200 employees.
Focus on: pricing per seat, integration ecosystem, reporting capabilities.
Include recent 2024-2026 changes and customer reviews from G2/Capterra.
```  
**示例提示（不良格式）：**  
```
Tell me about CRMs
```  

## 结果输出格式  
返回结构化的JSON数据，包含以下内容：  
- `task_id`：唯一的任务标识符  
- `status`：`pending`（待处理）、`running`（运行中）、`completed`（已完成）、`failed`（失败）  
- `result`：  
  - `summary`：执行摘要  
  - `findings[]`：详细的研究结果及来源  
  - `sources[]`：所有引用的URL及其标题  

## 结果展示方式  
- 首先逐字呈现执行摘要  
- 直接展示关键发现，无需改写  
- 包含所有事实的来源URL  
- 指出来源之间的矛盾信息  
- 保留所有事实、名称、数字、日期和引文  

## 数据量过大时的处理方式  
对于长时间讨论的情况，建议先保存结果，然后使用`sessions_spawn`命令启动子代理：  
```bash
parallel-cli research run "<question>" --json -o /tmp/research-<topic>
```  
之后再通过该子代理继续处理后续任务：  
```json
{
  "tool": "sessions_spawn",
  "task": "Read /tmp/research-<topic>.json and present the executive summary and key findings with sources.",
  "label": "research-summary"
}
```  

## 错误处理  
| 错误代码 | 含义                          |  
|-----------|----------------------------------|  
| 0       | 成功                          |  
| 1       | 发生意外错误（网络问题或解析错误）                |  
| 2       | 参数无效                        |  
| 3       | API错误（非2xx状态码）                    |  

## 先决条件  
1. 在[parallel.ai](https://parallel.ai)获取API密钥。  
2. 安装相应的CLI工具：  
```bash
curl -fsSL https://parallel.ai/install.sh | bash
export PARALLEL_API_KEY=your-key
```  

## 参考资料  
- [API文档](https://docs.parallel.ai)  
- [研究API参考](https://docs.parallel.ai/api-reference/research)