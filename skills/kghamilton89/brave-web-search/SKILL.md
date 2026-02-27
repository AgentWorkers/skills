---
name: brave-web-search
description: 使用 Brave Search API 在网络上进行搜索，并返回排名靠前的搜索结果或由 AI 生成的摘要答案。适用于实时网页查询和事实性问答场景。
metadata:
  clawdbot:
    emoji: "🔍"
    requires:
      env: ["BRAVE_SEARCH_API_KEY", "BRAVE_ANSWERS_API_KEY"]
      bins: ["node"]
    primaryEnv: "BRAVE_SEARCH_API_KEY"
    category: "Search & Research"
---
# Brave Web Search

该技能通过Brave Search API在网络上进行搜索，并获取由AI生成的摘要答案。提供了两个命令：`brave-search`用于获取排序后的网页结果，`brave-answer`用于获取简洁的AI摘要。

## 使用说明

1. **触发方式**：当用户想要在网络上查找信息、查看最新新闻或获取问题的答案时，可以激活该技能。
2. **安装要求**：无需安装任何软件，该技能没有任何外部依赖，直接在原生Node.js环境中运行。
3. **命令选择**：
   - 使用`brave-search`进行常规网页搜索，此时排序后的结果（包含网址和摘要）非常有用。
   - 使用`brave-answer`回答具体问题，此时简洁的AI摘要更为合适。
4. **执行方式**：通过将命令名称和参数作为单独的参数传递来调用脚本，切勿将用户输入直接插入到shell命令字符串中。建议使用参数数组或`execFile`风格的调用方式，以避免shell解析用户提供的内容。示例（Node.js伪代码）：

   ```javascript
   execFile('node', ['index.js', 'brave-search', '--query', userQuery, '--count', '10'])
   ```

   **注意**：**切勿**将命令构建为单个字符串，例如`"node index.js brave-search --query " + userQuery`。

5. **结果更新频率**：对于时效性强的查询，可以在`brave-search`命令中通过`--freshness`参数指定更新频率（`pd`表示过去一天，`pw`表示过去一周，`pm`表示过去一个月）。
6. **备用方案**：如果`brave-answer`返回`answer: null`，则向用户展示`fallback_results`作为替代结果。
7. **结果展示**：清晰地展示搜索结果（包括网页标题和网址），或答案的摘要文本。

## 安全性与隐私保护

- **防止shell注入**：用户查询必须以独立参数的形式传递（例如通过`execFile`或argv数组），严禁将用户输入直接插入到shell命令字符串中。将用户输入与shell命令字符串拼接（例如使用模板字符串`shell: true`）可能导致shell注入攻击，这是严格禁止的。
- **数据访问范围**：该技能仅将查询字符串发送给Brave Search API和Brave Summarizer API。
- **环境配置**：该技能使用OpenClaw环境提供的`BRAVE_SEARCH_API_KEY`和`BRAVE_ANSWERS_API_KEY`进行身份验证。
- **数据访问**：该技能不会读取本地文件或`.env`文件，所有配置均由代理程序处理。