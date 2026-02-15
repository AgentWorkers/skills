---
name: meegle-mcp
description: 通过 MCP 协议与 Meegle 项目管理系统进行交互
homepage: https://www.meegle.com/
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw": {"requires": {"env": ["MEEGLE_USER_KEY"]}, "primaryEnv": "MEEGLE_USER_KEY", "emoji": "📊", "os": ["darwin", "linux", "win32"]}}
---

# Meegle MCP 技能

本技能通过 Model Context Protocol (MCP) 将 Meegle（一个可视化的工作流和项目管理工具）与 OpenClaw 集成。

## 什么是 Meegle？

Meegle 是由 Larksuite 提供的领先可视化项目管理工具，专为敏捷团队设计。它提供以下功能：
- 可定制的看板（Kanban）和甘特图
- 集成聊天功能的实时协作
- 工作流自动化和自定义流程
- 时间跟踪与分析仪表盘
- 为外部利益相关者提供的客户端门户访问

## 设置

### 先决条件

您需要：
1. 一个具有 API 访问权限的 Meegle 账户
2. 从您的 Meegle 工作区获取的 `MEEGLE_USER_KEY`

### 配置

#### 选项 1：环境变量（推荐）

将您的用户密钥设置为环境变量：

```bash
export MEEGLE_USER_KEY="your_user_key_here"
export MEEGLE_MCP_KEY="your_mcp_key_here"
```

将此设置添加到您的 shell 配置文件（`~/.bashrc`、`~/.zshrc` 等）中，以便在会话之间保持设置。

#### 选项 2：OpenClaw 配置

将 MCP 服务器配置添加到 OpenClaw 设置中：
1. 编辑或创建您的 OpenClaw MCP 服务器配置文件
2. 添加 Meegle MCP 服务器配置：

```json
{
  "mcpServers": {
    "meegle": {
      "command": "node",
      "args": ["{baseDir}/scripts/mcp-proxy.js"],
      "env": {
        "MEEGLE_USER_KEY": "your_user_key_here",
        "MEEGLE_MCP_URL": "https://project.larksuite.com/mcp_server/v1",
        "MEEGLE_MCP_KEY": "your_mcp_key_here"
      },
      "status": "active"
    }
  }
}
```

#### 选项 3：使用 mcporter（备用方案）

如果您已安装了 `mcporter`：

```bash
mcporter add meegle \
  --url "https://project.larksuite.com/mcp_server/v1?mcpKey=your_mcp_key_here&userKey={user_key}" \
  --env MEEGLE_USER_KEY=your_user_key_here
```

### 安装

**通过 ClawHub 安装（推荐）：**
```bash
clawhub install meegle-mcp
```

**从 GitHub 安装：**
```bash
git clone <this-repo-url> meegle-mcp
cd meegle-mcp
./scripts/setup.sh
```

然后重启 OpenClaw 并验证安装是否成功：
```bash
   openclaw skills list | grep meegle
   ```

## 可用工具

配置完成后，Meegle MCP 服务器提供了多种项目管理工具。常见操作包括：

### 项目管理
- **列出项目**：查看工作区中的所有项目
- **创建项目**：设置具有自定义工作流的新项目
- **更新项目**：修改项目详情、状态或成员

### 任务操作
- **创建任务**：添加新任务，并指定负责人、截止日期和优先级
- **列出任务**：按项目、负责人或状态筛选和搜索任务
- **更新任务**：更改任务属性，或在工作流阶段之间移动任务
- **获取任务详情**：查看任务的详细信息

### 工作流管理
- **获取工作流模板**：列出可用的工作流模板
- **应用工作流**：将工作流应用于项目
- **更新工作流阶段**：推动任务通过工作流阶段

### 团队协作
- **添加成员**：邀请团队成员加入项目
- **列出成员**：查看项目参与者和角色
- **更新权限**：管理访问权限

### 分析与报告
- **获取项目统计信息**：查看进度、完成率和指标
- **时间跟踪**：记录和查询时间使用情况
- **生成报告**：根据项目数据创建自定义报告

## 使用示例

### 创建新项目
```
Create a new Meegle project called "Q1 Website Redesign" with a Kanban workflow
```

### 管理任务
```
Show me all high-priority tasks assigned to me in Meegle
```

```
Create a task in Meegle: "Update landing page copy" assigned to @designer, due next Friday
```

### 工作流操作
```
Move the task "Homepage mockups" to the "In Review" stage in Meegle
```

### 团队协调
```
Add john@company.com as a contributor to the "Mobile App" project in Meegle
```

### 报告
```
Generate a summary of completed tasks in Meegle for the past week
```

## 限制

- **身份验证**：需要有效的 `MEEGLE_USER_KEY` 及相应的权限
- **速率限制**：受 Meegle API 速率限制的影响（请查看您的计划）
- **只读操作**：某些操作可能基于您的角色受到限制
- **工作区范围**：仅访问您被授权的工作区中的项目

## 安全注意事项

- **切勿将 `MEEGLE_USER_KEY` 提交到版本控制系统中**
- 将凭据存储在环境变量或安全的配置文件中
- 在授予 OpenClaw 访问 Meegle 的权限之前，请仔细审查权限设置
- 考虑使用专用服务账户进行自动化操作

## 故障排除

### “身份验证失败”错误
- 确认您的 `MEEGLE_USER_KEY` 是否正确
- 确保密钥未过期或被撤销
- 检查您的 Meegle 账户是否启用了 API 访问权限

### “MCP 服务器无响应”
- 确认与 `project.larksuite.com` 的网络连接是否正常
- 检查 MCP 服务器的 URL 和密钥是否正确
- 查看 OpenClaw 日志：`openclaw logs --filter=meegle`

### 工具未显示
- 安装完成后重启 OpenClaw
- 检查技能是否已加载：`openclaw skills list`
- 确认环境变量设置正确

## 资源

- [Meegle 官方网站](https://www.meegle.com/)
- [Meegle 文档](https://www.larksuite.com/hc/en-US/articles/040270863407-meegle-overview)
- [Larksuite 平台](https://www.larksuite.com/)
- [OpenClaw 技能文档](https://docs.openclaw.ai/tools/skills)
- [Model Context Protocol 规范](https://modelcontextprotocol.io/)

## 反馈

如有问题或建议，请在技能仓库中提交 issue，或通过 ClawHub 联系我们。

---

**注意**：本技能使用 Model Context Protocol 与 Meegle 的 MCP 服务器进行通信。工具的可用性和功能取决于您的 Meegle 计划和权限设置。