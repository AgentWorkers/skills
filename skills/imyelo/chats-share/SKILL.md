---
name: chats-share
description: "将 AI 代理的对话内容分享为公共网页。当用户希望将对话内容外部分享、导出对话历史以用于文档编写，或将聊天会话发布到公共 URL 时，可以使用此功能。"
metadata: {"openclaw":{"emoji":"💬","homepage":"https://github.com/imyelo/openclaw-chats-share"}}
---
# chats-share  
将 AI 代理的对话内容分享为公共网页。  

## 支持的代理  
| 代理 | 详情 |  
|-------|---------|  
| OpenClaw | [参考文档：platforms/openclaw.md](references/platforms/openclaw.md) |  
| 未知代理 | [参考文档：platforms/unknown.md](references/platforms/unknown.md) — 通用的基于技能的备用方案 |  
| 新平台 | 按照 [参考文档：platforms/TEMPLATE.md](references/platforms/TEMPLATE.md) 的格式创建新文件 |  

## 核心工作流程  

### 1. 设置检查  
- 根据代理的配置信息检测代理类型，并加载项目目录及网站地址。  
- 如果项目未在本地配置，询问用户：  
  - “您是否有现有的 `chats-share` 仓库？”  
  - 如果有 → [现有仓库，新环境](references/setup.md#existing-repo-new-environment)  
  - 如果没有（默认情况） → [首次设置](references/setup.md#first-time-setup)  

### 2. 定位会话  
- 使用代理的配置信息查找会话记录。  
- 显示所有会话记录供用户选择。  

### 3. 提取并转换  
- 按照第一步中检测到的平台配置文件中的转换说明进行操作。  
- 将转换结果保存到 `{projectDir}/chats/.tmp/{timestamp}.yaml` 文件中。  

### 4. 填充元数据  
- 命令行工具（CLI）会自动填充部分结构化字段；本步骤的任务是填写面向用户的元数据：  

| 字段 | CLI 默认值 | 操作 |  
|-------|-------------|--------|  
| `date`, `sessionId`, `model`, `totalMessages`, `totalTokens`, `defaultShowProcess` | 自动填充 | 仅审核 |  
| `visibility` | `private` | 更改为 `public` |  
| `participants` | 通用角色名称（如 `user`, `assistant`） | 询问用户显示名称后更新字段名称 |  
| `title` | “会话导出”（通用标题） | 阅读生成的 YAML 文件后建议并确认标题 |  
| `description` | （未提供） | 编写简短描述后确认 |  
| `channel` | （未提供） | 询问用户后设置为平台名称（例如 `discord`）；否则省略 |  
| `cover` | （未提供） | 跳过此步骤（用户可手动添加自定义封面图片） |  
| `tags` | （未提供） | 跳过此步骤（用户可手动添加标签） |  

### 5. 去除敏感信息  
- 删除敏感内容，例如：  
  - API 密钥、令牌、密码  
  - 包含用户名的文件路径（如 `/Users/xxx` → 替换为 `~`）  
  - 电子邮件地址、电话号码  
  - 内部链接和私有 IP 地址  

### 6. 确认并保存  
- 建议文件名为：`{YYYYMMDD}-{topic}.yaml`  
- 显示文件预览，用户确认或修改文件标题/名称。  
- **在移动文件之前，创建一个专用分支**（即使用户尚未发布内容，此步骤也是必需的）：  
  ```bash
  cd {projectDir}
  git checkout -b chat/{YYYYMMDD}-{topic}
  ```  
- 将文件从 `{projectDir}/chats/.tmp/{timestamp}.yaml` 移动到 `{projectDir}/chats/{YYYYMMDD}-{topic}.yaml`。  
- 立即将文件推送到分支并提交，以确保文件独立存在于专用分支中：  
  ```bash
  git add chats/{YYYYMMDD}-{topic}.yaml
  git commit -m "docs: add {topic}"
  ```  

> **为什么要创建专用分支？** 将文件保存在默认分支中可能会导致无关的更改混入未来的 Pull Request 中。务必将每个聊天记录保存在独立的专用分支中。  

---

## 可选步骤：发布  
将步骤 6 中创建的分支推送到远程仓库，并提交 Pull Request。  
详情请参阅 [参考文档：publish.md](references/publish.md)。只有在用户明确请求的情况下才进行此操作。  

---

## 特殊情况  
- **首次设置项目** → [参考文档：setup.md](references/setup.md)  
- **大型或复杂的会话（使用未知平台）** → [参考文档：large-file.md](references/large-file.md)