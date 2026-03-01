# 技能：qmd-setup

**名称：** qmd-setup  
**描述：** 安装并配置 QMD 语义搜索功能，以支持知识库的查询。

## 概述

QMD 为知识库的内存管理系统添加了语义搜索功能。与仅依赖文件路径和关键词匹配的方式不同，代理现在可以使用自然语言查询知识库，并根据查询内容的含义获取排序后的结果。

| 功能 | 未使用 QMD | 使用 QMD |
|---|---|---|
| **搜索方式** | 通过文件路径导航并直接读取文件 | 使用自然语言进行语义查询 |
| **查找相关信息** | 必须知道要查找的文件位置 | 在所有已索引的文件中根据含义进行搜索 |
| **发现新文件** | 需要手动告知代理新文件的存在 | 新文件会在 5 分钟内被自动索引 |
| **查询示例** | `read shared/brands/skincare/profile.md` | `"这个护肤品牌主要关注哪些成分？"` |
| **适用场景** | 结构明确的小型知识库 | 需要高效发现新内容的不断增长的知识库 |
| **是否必需？** | 不是必需的——对于中小型知识库，基于文件的存储方式即可 | 可选——随着知识库的增长，QMD 可显著提升查询效率 |

## 何时使用

1. **知识库规模扩大**：当知识库的规模超出代理仅通过文件路径能管理的范围时。如果代理经常因为不知道该查找哪个文件而错过相关信息，QMD 可提供帮助。
2. **跨品牌查询**：当代理需要在多个品牌或领域中查找信息，且不知道具体文件位置时。QMD 可同时搜索所有相关内容。
3. **新团队成员入职**：在添加新代理或重新配置团队时，QMD 可帮助新成员快速了解现有知识。

## 设置流程

### 第一步：检查当前状态

首先，确认 QMD 是否已经安装以及当前的内存配置情况。

```bash
# Check if qmd is installed
which qmd

# Check current memory config
cat ~/.openclaw/openclaw.json | python3 -m json.tool | grep -A 10 '"memory"'
```

**如果 QMD 已经安装并配置完成：** 无需额外操作，直接进入第 4 步。
**如果 QMD 已安装但未配置：** 转到第 3 步。
**如果 QMD 未安装：** 继续执行第 2 步。

### 第二步：安装 QMD

**推荐使用：使用 `bun` 进行安装（更快）：**
```bash
bun install -g @tobilu/qmd
```

**或者：使用 `npm` 进行安装：**
```bash
npm install -g @tobilu/qmd
```

**验证安装结果：**
```bash
which qmd
qmd --version
```

如果看到路径和版本号，则安装成功。如果出现 `ERR_DLOPEN_FAILED` 错误，请参阅下面的故障排除部分。

### 第三步：配置

**选项 A：自动配置（推荐）：**
```bash
node scripts/patch-config.js --force-qmd
```

此步骤会修改 `openclaw.json` 文件，设置以下内容：
- `memory.backend` 为 `"qmd"`  
- `memory.qmdpaths` 为默认的知识库目录路径  
- `memory.qmd.update.interval` 为 `"5m"` （每 5 分钟自动重新索引一次）

**选项 B：手动配置：**

编辑 `~/.openclaw/openclaw.json` 文件，添加或更新 `memory` 部分：

```json
{
  "memory": {
    "backend": "qmd",
    "qmd": {
      "includeDefaultMemory": true,
      "paths": [
        { "path": "memory", "name": "daily-notes", "pattern": "**/*.md" },
        { "path": "skills", "name": "agent-skills", "pattern": "**/*.md" },
        { "path": "shared", "name": "shared-knowledge", "pattern": "**/*.md" }
      ],
      "update": { "interval": "5m" }
    }
  }
}
```

**配置字段说明：**

| 字段 | 说明 | 默认值 |
|---|---|---|
| `memory.backend` | 使用的内存后端 | `"file"`（修改为 `"qmd"`） |
| `memory.qmd.includeDefaultMemory` | 是否将默认的 `MEMORY.md` 文件包含在索引中 | `true` |
| `memory.qmdpaths` | 定义索引目录的数组（格式为 `{path, name, pattern}`） | （如果未设置，则需要手动添加） |
| `memory.qmd.update.interval` | 自动重新索引的间隔时间 | `"5m"` |

### 第四步：重启并验证

```bash
# Restart the gateway to pick up the new config
openclaw gateway restart

# Check the logs for QMD initialization
openclaw gateway logs | grep -i qmd
```

**预期的日志输出：**
```
[INFO] Memory backend: qmd
[INFO] QMD indexing 4 paths...
[INFO] QMD indexed 42 documents in 1.3s
[INFO] QMD ready — next reindex in 300s
```

**测试语义查询：**
```bash
# If your system supports it:
openclaw memory search "skincare brand ingredients"
```

如果查询返回了相关文档，说明 QMD 已正确安装并生效。

---

## 故障排除

### better-sqlite3 与 Node.js 版本不匹配

QMD 需要 `better-sqlite3` 这个 Node.js 插件。如果安装 QMD 时使用的 Node.js 版本与运行网关的 Node.js 版本不一致，可能会出现问题：

```
Error: ERR_DLOPEN_FAILED
Module was compiled against a different Node.js version
```

**解决方法：**

1. 确定网关使用的 Node.js 版本：  
   ```bash
   which node
   node --version
   ```

2. 使用相应的 Node.js 版本重新构建 `better-sqlite3`：  
   ```bash
   # For bun global installs:
   cd ~/.bun/install/global/node_modules/better-sqlite3
   npm rebuild better-sqlite3

   # For npm global installs:
   cd $(npm root -g)/better-sqlite3
   npm rebuild better-sqlite3
   ```

3. 验证修复效果：  
   ```bash
   node -e "require('better-sqlite3')"
   # No output = success
   ```

4. 重启网关：  
   ```bash
   openclaw gateway restart
   ```

### 其他常见问题

| 问题 | 解决方法 |
|---|---|
| `which qmd` 命令无输出 | QMD 未安装，请执行第 2 步。 |
| “backend 未配置” | `memory.backend` 未设置为 `"qmd"`，请执行第 3 步。 |
| 搜索无结果 | 文件可能尚未被索引，请等待 5 分钟或检查配置中的 `paths` 设置。 |
| SQLite 数据库缺失 | 确保 `memory.qmd.dbPath` 可写入；QMD 会在首次运行时创建该文件。 |
| 索引路径中的符号链接损坏 | 检查所有路径是否正确解析，如有损坏的符号链接请修复。 |

---

## 卸载

要卸载 QMD 并恢复到基于文件的存储方式，请按照以下步骤操作：

1. **更新配置：**  
   修改 `~/.openclaw/openclaw.json` 文件，将 `memory.backend` 设置为 `"file"`：  
   ```json
   {
     "memory": {
       "backend": "file"
     }
   }
   ```  
   （即使设置了 `memory.backend` 为 `"qmd"`，该配置在 QMD 未安装时也会被忽略。）

2. **重启网关：**  
   ```bash
   openclaw gateway restart
   ```

3. **（可选）卸载 QMD 包：**  
   ```bash
   # If installed with bun:
   bun remove -g @tobilu/qmd

   # If installed with npm:
   npm uninstall -g @tobilu/qmd
   ```

4. **（可选）删除 SQLite 数据库：**  
   ```bash
   rm ~/.openclaw/memory/main.sqlite
   ```

卸载后，代理将再次使用基于文件的存储方式（即 `MEMORY.md` 和直接读取文件）。这种方式适用于中小型知识库，且不需要额外的依赖项。