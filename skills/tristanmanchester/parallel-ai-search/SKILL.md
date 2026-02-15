---
name: parallel-ai-search
description: 通过并行搜索/提取API进行网页搜索和URL内容提取。适用于获取最新研究资料、在特定域名范围内进行搜索，以及从URL中提取适合大型语言模型（LLM）使用的文本片段或Markdown格式的内容。
homepage: https://docs.parallel.ai/search/search-quickstart
metadata: {"openclaw":{"emoji":"🔎","homepage":"https://docs.parallel.ai/","requires":{"bins":["node"],"env":["PARALLEL_API_KEY"]},"primaryEnv":"PARALLEL_API_KEY"}}
---

# 并行AI搜索（OpenClaw技能）

使用此技能可通过**并行搜索**（基于LLM优化的摘录）和**并行提取**（从特定URL中提取干净的Markdown内容，包括包含大量JavaScript的页面和PDF文件）来执行网络研究。

该技能提供了小巧的**Node.js辅助文件**（.mjs格式），以便代理可以通过OpenClaw的**exec**工具以确定性方式调用这些API。

## 快速入门

### 1) 提供API密钥

建议将API密钥配置在`~/.openclaw/openclaw.json`文件中（适用于主机环境）：

```json5
{
  skills: {
    entries: {
      "parallel-ai-search": {
        enabled: true,
        apiKey: "YOUR_PARALLEL_API_KEY"
      }
    }
  }
}
```

**注意：**
- 如果代理运行在沙箱环境中，Docker沙箱不会继承主机环境变量。请通过`agents.defaults.sandbox.docker.env`文件提供密钥（或将其嵌入到镜像中）。
- 此技能的启用依赖于`PARALLEL_API_KEY`。如果该密钥缺失，OpenClaw将无法加载该技能。

### 2) 运行搜索

使用`exec`命令来执行搜索：

```bash
node {baseDir}/scripts/parallel-search.mjs \
  --objective "When was the United Nations established? Prefer UN websites." \
  --query "Founding year UN" \
  --query "Year of founding United Nations" \
  --max-results 5 \
  --mode one-shot
```

### 3) 从URL中提取内容

```bash
node {baseDir}/scripts/parallel-extract.mjs \
  --url "https://www.un.org/en/about-us/history-of-the-un" \
  --objective "When was the United Nations established?" \
  --excerpts \
  --no-full-content
```

### 4) 一个命令：搜索 → 提取顶级结果

```bash
node {baseDir}/scripts/parallel-search-extract.mjs \
  --objective "Find recent research on quantum error correction" \
  --query "quantum error correction 2024" \
  --query "QEC algorithms" \
  --max-results 6 \
  --top 3 \
  --excerpts
```

## 适用场景

当用户请求以下内容时，可触发此技能：
- “并行搜索”、“parallel.ai搜索”、“并行提取”、“搜索API”、“提取API”
- “使用Parallel工具进行网络研究”、“基于LLM优化的摘录”、“来源策略/包含的域名”、“时间范围”、“数据获取策略”
- “从URL/PDF中提取干净的Markdown内容”、“爬取包含大量JavaScript的页面”、“获取最新的网络结果”

## 默认工作流程

1. 使用**搜索**功能，指定**目标**并输入多个**搜索查询**。
2. **检查**标题、URL和发布日期；选择最佳来源。
3. **提取**实际需要的具体页面（前N个URL）。
4. **使用提取的摘录或完整内容进行回答**。

**使用建议：**
- 使用**搜索**功能来发现信息；
- 使用**提取**功能来阅读内容。

## 使用Parallel技能的最佳提示方式

### 目标
用1-3句话描述：
- 真实的需求背景（为什么需要这些信息）
- 对内容新鲜度的要求（例如：“优先选择2025年以后的内容”、“时间范围为2024年1月1日之后”、“使用最新的文档”）
- 偏好的信息来源（例如：“官方文档”、“标准组织”、“GitHub发布的内容”）

### 搜索查询
添加3-8个关键词查询，包括：
- 具体术语、版本号、错误信息
- 相关的替代词
- 如果适用，指定时间范围（例如：“2025年”、“2026年”、“2026年1月”）

### 模式
- 使用`mode=one-shot`进行一次性查询（默认设置）。
- 使用`mode=agentic`进行多步骤研究（生成更简洁、更节省令牌的摘录）。

### 来源策略
当需要严格控制搜索结果时，可以设置`source_policy`参数：
- `include_domains`：允许访问的域名列表（最多10个）
- `exclude_domains`：禁止访问的域名列表（最多10个）
- `after_date`：按照RFC3339格式指定的日期（格式为YYYY-MM-DD），用于过滤内容的新鲜度

## 脚本

所有脚本默认会将JSON格式的响应输出到标准输出（stdout）。

### `scripts/parallel-search.mjs`
调用`POST https://api.parallel.ai/v1beta/search`接口。

**常用参数：**
- `--objective "..."`：指定搜索目标
- `--query "..."`：输入搜索查询
- `--mode one-shot` | `--mode agentic`：指定搜索模式
- `--max-results N`：指定返回的结果数量（1-20个）
- `--include-domain example.com`：指定允许访问的域名
- `--exclude-domain example.com`：指定禁止访问的域名
- `--after-date YYYY-MM-DD`：指定时间范围
- `--excerpt-max-chars N`：指定每个结果的摘录字符数上限
- `--excerpt-max-total-chars N`：指定所有结果的总字符数上限
- `--fetch-max-age-seconds N`：设置数据获取的最长时间（0表示禁用）
- `--request path/to/request.json`：指定请求的JSON文件路径（高级用法）
- `--request-json '{"objective":"..."}'`：指定请求的JSON格式（高级用法）

### `scripts/parallel-extract.mjs`
调用`POST https://api.parallel.ai/v1beta/extract`接口。

**常用参数：**
- `--url "https://..."`：指定要提取内容的URL（最多10个）
- `--objective "..."`：指定搜索目标
- `--query "..."`：输入搜索查询
- `--excerpts` | `--no-excerpts`：是否提取摘录
- `--full-content` | `--no-full-content`：是否提取完整内容
- `--excerpt-max-chars N` | `--excerpt-max-total-chars N`：指定摘录的字符数上限
- `--full-max-chars N`：指定完整内容的字符数上限
- `--fetch-max-age-seconds N`：设置数据获取的最长时间（默认为600秒）
- `--fetch-timeout-seconds N`：设置请求超时时间
- `--disable-cache-fallback`：禁用缓存回退机制
- `--request path/to/request.json`：指定请求的JSON文件路径（高级用法）

### `scripts/parallel-search-extract.mjs`
这是一个便捷的脚本组合：
1) 执行搜索；
2) 从搜索结果中提取前N个URL的内容（通过一次`parallel-extract`调用完成）。

**常用参数：**
- 所有`parallel-search.mjs`的参数
- `--top N`：指定要提取的顶级URL数量（1-10个）
- 提取选项：`--excerpts` | `--full-content`（决定是否提取摘录或完整内容）

## 输出处理规范

在将API输出转换为用户可读的答案时，请遵循以下规则：
- 尽量使用**官方或主要来源**的数据。
- **仅**引用或改写相关的提取内容。
- 包含**URL和发布日期**（如果有的话），以确保信息的透明度。
- 如果不同来源的结果存在差异，请同时展示两种结果，并说明每个来源的来源。

## 错误处理

脚本的退出状态码如下：
- `0`：表示成功
- `1`：表示出现意外错误（网络问题、JSON解析错误等）
- `2`：表示参数无效
- `3`：表示API错误（非2xx状态码）——在这种情况下，错误信息会被输出到标准错误输出（stderr）。

## 参考资料

仅在需要时加载以下文件：
- `references/parallel-api.md`：API接口的详细说明和结构参考
- `references/openclaw-config.md`：OpenClaw的配置设置及沙箱环境相关说明
- `references/prompting.md`：提示语句模板和研究方法指南