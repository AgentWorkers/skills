# 存储记忆 📦

**状态：** ✅ 已启用 | **模块：** Archive | **所属部分：** Agent Brain（代理大脑）

记忆的编码、检索、整合与清除——大脑的存储系统。

## 功能概述

- **编码（Encode）**：将经历转化为可存储的记忆。
- **检索（Retrieve）**：查找相关的过往知识。
- **整合（Consolidate）**：强化重要记忆，压缩旧记忆。
- **清除（Decay）**：删除过时、价值较低的数据。

## 数据存储方式：仅本地存储

**所有数据都保存在您的设备上。**

文件：`memory/index.json`

```json
{
  "type": "episodic|factual|procedural|preference",
  "content": "...",
  "timestamp": "2026-02-17T01:30:00Z"
}
```

## 可选功能：SuperMemory 同步

SuperMemory 的云同步功能为 **仅限自愿启用**。

启用方法：
1. 确保您的 OpenClaw 已安装 SuperMemory 工具。
2. 编辑此文件，取消注释同步相关的代码行。
**默认设置：** 无数据会被传输到云端。

### 默认情况下，该功能是禁用的

```
# Default: Local only
# To enable cloud sync, edit this module and uncomment:
# supermemory_store(category:"fact", text:"...")
```

## 记忆类型及其存储位置

| 记忆类型 | 本地存储 | 云端存储 |
|-------------|-------|-------|
| 事实性记忆（Factual） | ✅ 始终存储在本地 | ⬜ 需手动启用同步 |
| 偏好记忆（Preference） | ✅ 始终存储在本地 | ⬜ 需手动启用同步 |
| 情节性记忆（Episodic） | ✅ 始终存储在本地 | ❌ 不支持云端存储 |
| 程序性记忆（Procedural） | ✅ 始终存储在本地 | ❌ 不支持云端存储 |

## 使用方法

```
"Remember that X"
"Learn: how to do X"
"I prefer X over Y"
"What do you know about X?"
```

## 集成方式

该功能作为 Agent Brain 的一部分，与以下组件协同工作：
- **Gauge**：判断何时需要检索记忆。
- **Signal**：检测记忆之间的冲突。
- **Ritual**：存储记忆的快捷方式。