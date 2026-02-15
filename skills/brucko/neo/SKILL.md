---
name: neo
description: |
  Give your OpenClaw the power of the Matrix. Download expertise directly into your AI's mind. 119 modules. 15 categories. Instant mastery.
  
  "I know kung fu."
  
  Physicists. Negotiators. VCs. Psychologists. Surgeons. Game theorists. The library keeps growing — or build your own.
  
  Free your mind.
---

# Neo 协议

按需加载专家级思维模型以提升推理能力。

## 命令

| 命令 | 功能 |
|---------|--------|
| `neo` | 显示当前已加载的思维模型状态（✓ 已加载；○ 未加载） |
| `neo help` | 列出所有可用命令 |
| `neo <模块名>` | 加载指定的模块。如果该模块来自库，则会自动添加到用户的思维模型中 |
| `neo <模块名> off` | 卸载指定的模块（该模块仍会保留在用户的思维模型中） |
| `neo off` | 卸载所有模块 |
| `neo browse` | 按类别浏览所有模块 |
| `neo search <查询内容>` | 在库中搜索指定的模块 |
| `neo add <模块名>` | 将模块添加到用户的思维模型中（但不立即加载） |
| `neo remove <模块名>` | 从用户的思维模型中删除该模块（将其移回库中） |
| `neo create <模块描述>` | 为库创建一个新的模块 |
| `neo delete <模块名>` | 永久删除库中的模块 |

## 工作流程

### 使用 `neo` 命令（不带参数）
显示当前已加载的思维模型状态，并提供相关帮助提示：
```
🧠 Neo Protocol

LOADED:
✓ psychologist
✓ game-theorist

CREW:
○ negotiator
○ entrepreneur

RECENTS:
○ dermatologist
○ cosmetic-plastic-surgeon

neo help for commands
```

“Recent”选项会显示最近使用但未加载到思维模型中的模块。这些模块的信息会保存在 `assets/recents.json` 文件中（包含时间戳），并在不同会话间保持一致。最多保存 5 个最近使用的模块，超过 1 周未使用的模块将被自动删除。

### 使用 `neo help` 命令
列出所有可用的命令。

### 使用 `neo <模块名>` 命令
1. 在用户的思维模型或库中查找指定的模块。
2. 将模块文件加载到当前上下文中。
3. 如果模块来自库（而非用户的思维模型），则将其添加到用户的思维模型中。
4. 确认加载成功后，会显示提示：“🧠 **<模块名>** 已加载。[模块的简要描述]”。

### 使用 `neo <模块名> off` 命令
1. 标记该模块已被卸载（不再被计入活跃模块列表）。
2. 该模块仍会保留在用户的思维模型中，方便日后重新加载。
3. 确认卸载成功后，会显示提示：“🧠 <模块名> 已卸载。”

### 使用 `neo off` 命令
1. 清除所有已加载的模块。
2. 确认所有模块均已卸载后，会显示提示：“🧠 所有模块均已卸载。”

### 使用 `neo create <模块描述>` 命令
1. 分析用户提供的描述，确定模块的类型。
2. 使用 `TEMPLATE.md` 模板生成新的模块文件。
3. 将新模块文件保存到 `assets/library/<类别>/<模块名>.md` 目录中。
4. 将新模块信息添加到 `registry.json` 文件中。
5. 确认创建成功后，系统会提示用户是否需要加载该模块。

## 相关文件
- `scripts/neo.py`：用于管理模块的命令行工具。
- `references/TEMPLATE.md`：模块创建的模板文件。
- `assets/crew.json`：用户的个人思维模型配置文件（该文件会被 Git 忽略）。
- `assets/crew.default.json`：默认的思维模型配置文件（随软件一起提供）。
- `assets/registry.json`：包含所有模块的索引文件。
- `assets/library/`：按类别分类的模块文件目录。

## 首次使用说明
如果系统中不存在 `crew.json` 文件，系统会自动将 `crew.default.json` 复制到 `crew.json`，以初始化用户的个人思维模型配置。

## 模块结构
每个模块都遵循以下结构：
- **核心思维特征**：4-5 个关键的心理特质。
- **框架**：4 个步骤的系统化方法。
- **风险警示**：6 个需要警惕的信号（🚩）。
- **关键问题**：5 个重要的问题。
- **专业术语**：5 个相关领域的专业术语。
- **适用场景**：4 种触发使用该模块的情境。
- **自定义设置**：用户可自定义的配置项。

## 状态管理
系统会记录用户会话中已加载的模块。当用户执行 `neo off` 命令或会话结束时，所有模块都会被视为已卸载。用户的思维模型配置会保存在 `crew.json` 文件中。

## 更新与自定义
`registry.json` 文件中的模块包含以下字段：
- `source`：模块的来源：
  - `"upstream"`：随软件一起提供的默认模块，由 ClawHub 自动更新。
  - `"custom"`：用户自定义的模块，不会被自动更新。
- `deleted`：表示模块的状态：
  - `false`：模块仍然有效，可以正常更新。
  - `true`：模块已被用户删除，更新时不会被恢复。

### 更新规则：
- 如果模块来自默认来源（`upstream`），则正常更新。
- 如果模块是用户自定义的（`custom`），则不会被更新。
- 如果模块已被用户删除（`deleted` 为 `true`），则更新时不会被恢复。

### 更新脚本：
```bash
# Check status
python3 scripts/update.py status

# Merge upstream updates
python3 scripts/update.py merge --upstream /path/to/new/neo

# Delete a module (marks upstream as deleted, removes custom)
python3 scripts/update.py delete --module physicist

# Restore a deleted upstream module
python3 scripts/update.py restore --module physicist
```

### 使用 `neo delete <模块名>` 命令时的处理：
- 如果模块来自默认来源（`source` 为 `upstream`），则将 `deleted` 字段设置为 `true`（表示模块仍可恢复）。
- 如果模块是用户自定义的（`source` 为 `custom`），则从 `registry` 和 `library` 中彻底删除该模块。