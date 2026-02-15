<skill>
  <name>TaskBoard</name>
  <description>
    使用 TaskBoardAI 卡板（Kanban）系统来管理任务和项目。

  **关键生命周期规则：**
  1. **创建**：当发现新任务时，将其添加到“待办”（To Do）列中。
  2. **执行**：在创建任务后（或收到执行任务的请求时），立即将其移至“进行中”（In Progress）状态。不要让待办任务长时间停留在“待办”状态。
  3. **阻塞**：如果任务无法完成（例如缺少 API 密钥、网络错误等），将其移至“阻塞”（Blocked）状态，并在备注中说明原因。
  4. **完成**：任务完成后，更新任务卡片的内容（包括最终结果/总结），然后将其移至“已完成”（Done）状态。

  **注意**：任务卡片的主要内容/结果应存储在“content”字段中（支持 Markdown 格式），而不是“description”字段。
</description>
<mcp_server>
  <command>node</command>
  <args>
    <arg>/opt/homebrew/lib/node_modules/taskboardai/server/mcp/kanbanMcpServer.js</arg>
  </args>
</mcp_server>