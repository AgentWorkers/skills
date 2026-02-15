---
name: fivem
description: 修复、创建或验证 QBCore/ESX 的 FiveM 服务器资源（包括 config.lua、fxmanifest.lua、物品、房屋/家具、脚本以及 MLO 文件）。当需要调试资源错误、在 ESX 和 QB 之间进行转换、更新 fxmanifest 版本、添加新物品或从 GitHub 下载源代码脚本时，请使用此功能。此外，该工具还用于生成 SSH 密钥以实现 SFTP 访问。
---

# FiveM (QBCore/ESX)

## 概述
负责处理 FiveM 资源的端到端管理工作：验证/修复配置文件、更新 `fxmanifest`、在 QBCore 与 ESX 之间进行资源转换、添加物品、设置房屋/家具、调试错误，以及编写简单的脚本或编写 MLO（Mission Layout Notes）。相关检查清单和操作指南可参考相应的参考文档。

## 工作流程决策树
1) **定位文件**：如果文件不在工作区中，请提供文件的准确路径或上传文件。
2) **分类任务**：
   - 更新 `fxmanifest` → 参考 `references/fxmanifest_checklist.md`
   - 修复/验证 `config.lua` → 参考 `references/config_patterns.md`
   - 在 QBCore 与 ESX 之间转换资源 → 参考 `references/qb_esx_conversion.md`
   - 添加/更新物品 → 参考 `references/items.md`
   - 设置房屋/家具 → 参考 `references/housing_furniture.md`
   - 调试错误 → 参考 `references/debugging.md`
   - 在 GitHub 上搜索相关脚本 → 参考 `references/github_search.md`
   - 生成 SSH 密钥 → 参考 `references/ssh_keys.md`
3) **应用修复措施**：精确地进行编辑，保持文件结构不变，并保留原有的注释。
4) **总结变更内容** + 提供下一步的操作及测试要求。

## 核心任务

### 1) 修复/验证 `config.lua`
   - 打开文件，检查语法错误（如缺少逗号/括号、引号不匹配、键重复等）。
   - 确保表格正确关闭，且物品列表一致。
   - 如果有疑问，请提供错误日志或预期的行为描述。

### 2) 更新 `fxmanifest.lua`
   - 将文件格式转换为推荐的版本，确保 `fx_version`、`game`、依赖项以及共享脚本/客户端/服务器脚本的设置正确。
   - 确保文件的导出/导入内容与资源使用情况相匹配。

### 3) 在 QBCore 与 ESX 之间转换资源
   - 映射框架钩子、玩家对象访问方式、物品、任务、货币、库存和通知系统。
   - 明确记录 API 的差异，并记录所有变更内容。

### 4) 添加物品
   - 将物品插入目标框架（QBCore/ESX）对应的共享物品文件中，确保物品的重量、堆叠方式及图像引用信息一致。

### 5) 设置房屋/家具
   - 验证家具的类别、价格、属性名称及放置位置；确保配置信息与资源要求一致。

### 6) 调试错误
   - 提供控制台错误信息；根据错误信息定位到具体文件和行进行修复；如果发现缺少依赖项，请标记出来。

### 7) 在 GitHub 上搜索相关脚本
   - 根据资源名称、框架名称以及 “fivem” 和 “qbcore/esx” 的关键词进行搜索，提供前三个符合条件的脚本选项，并附上相关说明。

### 8) 生成 SSH 密钥（用于 SFTP）
   - 生成 ed25519 密钥对，提供公钥以供服务器使用，并指导如何安全地存储密钥。

## 参考文档
- `references/fxmanifest_checklist.md`
- `references/config_patterns.md`
- `references/qb_esx_conversion.md`
- `references/items.md`
- `references/housing_furniture.md`
- `references/debugging.md`
- `references/github_search.md`
- `references/ssh_keys.md`
- `references/ox_lib.md`
- `references/menanak47.md`
- `references/qb_target.md`
- `references/qb_core.md`