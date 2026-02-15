---
name: braindb
version: 0.5.0
description: 为AI代理提供持久性、语义化的记忆功能。这种记忆机制能够确保AI具备长期的信息检索能力，即使在数据压缩或会话重置后也能保持信息的有效性——准确率达到98%，延迟仅为20毫秒。
homepage: https://github.com/Chair4ce/braindb
license: MIT
author: Oaiken LLC
metadata:
  {
    "openclaw": {
      "emoji": "🧠",
      "requires": {
        "bins": ["docker", "node"],
        "env": [],
        "configPaths": ["~/.openclaw/openclaw.json"]
      },
      "permissions": {
        "configWrite": true,
        "workspaceRead": true,
        "networkOptional": "Migration with --swarm sends file contents to Google Gemini API. Default migration is fully local."
      },
      "install": [
        {
          "id": "release-download",
          "kind": "download",
          "url": "https://github.com/Chair4ce/braindb/releases/download/v0.5.0/braindb-v0.5.0.zip",
          "archive": "zip",
          "extract": true,
          "stripComponents": 1,
          "targetDir": "~/.openclaw/plugins/braindb",
          "label": "Download BrainDB v0.5.0",
          "postInstall": "cd ~/.openclaw/plugins/braindb && bash install.sh"
        }
      ],
      "uninstall": "cd ~/.openclaw/plugins/braindb && bash uninstall.sh"
    }
  }
---
# BrainDB

专为AI代理设计的持久化、语义化记忆系统。适用于[OpenClaw](https://github.com/openclaw/openclaw)。

---

## 功能介绍

您的AI在会话之间会忘记所有内容。BrainDB可以解决这个问题。

它为AI助手提供了一个记忆系统，能够自动捕捉对话中的重要信息，并在需要时进行检索——例如：您是谁、您正在做什么、您之前告诉过它什么。这些记忆在数据压缩、会话重置或系统重启后依然保持不变。

**工作原理：**
```
You say something → OpenClaw captures important facts → BrainDB stores them
You ask something → OpenClaw recalls relevant memories → AI has context
```

无需任何命令或手动保存操作，系统会自动运行。

---

## 安装要求

需要Docker和约4GB的RAM。

```bash
openclaw plugin install braindb
```

或者手动安装：
```bash
git clone https://github.com/Chair4ce/braindb.git ~/.openclaw/plugins/braindb
cd ~/.openclaw/plugins/braindb
bash install.sh
```

首次安装可能需要3–5分钟（用于下载嵌入模型）。之后安装过程大约需要10秒。

**安装程序的主要操作：**
1. 将您现有的记忆文件备份到`~/.openclaw/braindb-backup/`目录。
2. 构建并启动3个Docker容器（Neo4j、嵌入器、网关）。
3. 修改您的OpenClaw配置文件（`~/.openclaw/openclaw.json`）以启用该插件。
4. （可选）将您的工作区文件迁移到BrainDB中。

如果您想了解每个安装步骤的详细信息，请先查看`install.sh`脚本。

---

## 主要特性

- **768维语义搜索**：能够找到概念上相关的记忆，而不仅仅是关键词匹配的结果。
- **4种记忆类型**：情景记忆（事件）、语义记忆（事实）、程序记忆（技能）、关联记忆（链接）。
- **分层排名机制**：语义相似度优先于关键词匹配。
- **自动去重**：不会存储重复的记忆。
- **赫布强化机制**：记忆会随着使用而增强，不使用时则会逐渐消失。
- **查询扩展**：能够理解口语化表达。
- 在50项测试基准测试中的召回准确率为98%。
- **平均查询延迟**：12–20毫秒。

---

## 安全性与隐私

- **所有核心操作都在本地完成**：
  - 网关仅绑定到`localhost`，不会暴露在您的网络中。
  - Neo4j和嵌入器无法从主机访问（它们运行在隔离的Docker网络中）。
  - Neo4j的密码是自动生成的（24位随机字符）。
  - 可通过`BRAINDB_API_KEY`进行API密钥认证。
- 容器以非root用户身份运行。
- 在正常运行期间，所有嵌入、搜索和存储操作都在本地完成，不会调用任何外部API。

**安装程序的读写操作：**
- 读取您的OpenClaw配置文件（`~/.openclaw/openclaw.json`）以添加插件配置。
- 在迁移过程中读取工作区文件（可先使用`--scan`选项进行预览）。
- 生成`.env`文件以保存Neo4j的登录凭据。
- 创建Docker卷用于持久化存储。

**关于数据迁移的隐私说明：**
- **默认迁移模式（`--no-swarm`）**：所有数据仅保存在本地，不会离开您的机器。
- **使用Swarm迁移**：会将文件内容发送到Google的Gemini API进行智能信息提取。此功能为可选设置——您必须已安装Swarm并明确允许该操作。使用`--no-swarm`选项可确保数据仅在本机处理。
- 在迁移前，请务必运行`node migrate.cjs --scan`或`--dry-run`以查看具体处理内容。

---

## 迁移现有数据

如果您已经有了`MEMORY.md`文件、日常笔记或其他工作区文件，可以按照以下步骤进行迁移：

```bash
node migrate.cjs --scan /path/to/workspace   # Preview files (no data sent anywhere)
node migrate.cjs --dry-run /path/to/workspace # Extract facts locally, don't encode
node migrate.cjs --no-swarm /path/to/workspace # Import, fully local
node migrate.cjs /path/to/workspace           # Import (uses swarm if available)
```

BrainDB不会修改您的原始文件，它只会复制其中的记忆内容。

---

## 故障处理

BrainDB具有优雅的故障处理机制：
1. **网关故障**：OpenClaw仍可正常运行，只是提示信息中会缺少相关记忆内容。您的AI仍然可以使用`MEMORY.md`文件和工作区文件。
2. **Neo4j故障**：网关会返回空结果，但不会显示错误信息，只是无法检索记忆内容。
3. **嵌入器故障**：系统会切换到纯文本搜索模式（虽然准确性较低，但仍然可用）。

您的工作区文件是数据的安全保障。即使移除了BrainDB，您也可以恢复到系统默认设置，且数据不会丢失。

---

## 卸载

卸载程序会导出所有记忆数据（以JSON和可读的markdown格式），停止相关容器，移除OpenClaw中的插件配置，并保留您的工作区文件。Docker卷也会被保留，直到您手动删除它们。

---

## 性能指标**

| 指标        | 值         |
|------------|------------|
| 召回准确率    | 98%（50项测试）    |
| 平均延迟    | 12–20毫秒      |
| 冷启动查询时间  | 约60毫秒      |
| 存储容量    | 超过10,000条记忆   |
| 内存占用    | 约2.5GB       |
| 系统要求    | Docker和约4GB RAM   |

---

## 链接

- [官方文档](https://github.com/Chair4ce/braindb#readme)
- [OpenClaw项目页面](https://github.com/openclaw/openclaw)

---

该项目由[Oaiken LLC](https://oaiken.com)开发，并遵循MIT许可证发布。