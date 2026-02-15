---
name: bring-recipes
description: **使用场景：**  
当用户希望从 Bring! 购物应用中浏览食谱灵感时使用。该功能允许用户发现新的食谱、查看食谱详情（名称、作者、类型、图片），或根据标签进行筛选。**注意：** 由于 API 的限制，用户无法导入食谱所需的食材信息。
---

# Bring! 食谱浏览器 CLI

## 概述

这是一个用于浏览 Bring! 食谱灵感的命令行工具（CLI）。**仅用于浏览**——Bring! 食谱灵感 API 不提供食材列表。

## 使用场景

**在以下情况下使用此工具：**
- 用户希望发现新的 Bring! 食谱
- 浏览食谱灵感
- 查看食谱元数据（名称、作者、类型、图片、链接）
- 按标签筛选食谱（全部、个人收藏的）
- 需要将食谱数据以 JSON 格式导出用于脚本编写

**不适用的场景：**
- 用户需要将食材添加到购物清单（受 API 限制）
- 直接管理购物清单
- 需要包含食材的完整食谱详情

## 快速参考

| 命令 | 功能 |
|---------|---------|
| `bring-recipes list` | 浏览食谱灵感（默认） |
| `bring-recipes filters` | 显示可用的筛选标签 |
| `bring-recipes list --filter mine` | 显示个人收藏的食谱 |
| `bring-recipes list --json` | 以 JSON 格式输出食谱数据（用于脚本编写） |

**环境变量：**
```bash
export BRING_EMAIL="your@email.com"
export BRING_PASSWORD="yourpassword"
```

## 安装

```bash
cd skills/bring-recipes
npm install
```

## 常见操作流程

**浏览所有食谱：**
```bash
node index.js list --limit 10
```

**筛选个人收藏的食谱：**
```bash
node index.js list --filter mine
```

**获取 JSON 数据用于脚本编写：**
```bash
node index.js list --json | jq -r '.[] | .content.name'
```

**查看可用的筛选选项：**
```bash
node index.js filters
```

## 标志参数说明

| 标志 | 说明 |
|------|-------------|
| `-f, --filter <标签>` | 筛选标签：全部、个人收藏的 |
| `--limit <数量>` | 最多显示的食谱数量（默认：10） |
| `--json` | 以 JSON 格式输出 |
| `--no-color` | 禁用颜色显示 |
| `-q, --quiet` | 减少输出信息 |
| `-v, --verbose` | 显示详细调试信息 |

## API 限制

⚠️ **重要提示：** Bring! 的 `getInspirations()` API 仅返回元数据：
- ✅ 食谱名称、作者、类型
- ✅ 图片、链接、标签、点赞数
- ❌ **食材列表**（不提供）

这是 Bring! API 的限制，并非 CLI 的错误。该 CLI 仅用于浏览和发现食谱。

## 食谱类型

- **TEMPLATE**：Bring! 提供的模板（例如：“周日早午餐”）
- **RECIPE**：来自合作伙伴的解析后的食谱
- **POST**：促销内容

## 常见错误

- **误以为 API 提供食材列表**：API 不提供食材列表，请使用 CLI 发现食谱后手动添加食材。
- **误以为有季节性筛选选项**：API 不支持季节性筛选，仅提供“全部”和“个人收藏”两种筛选方式。
- **误以为所有食谱都有名称**：POST 类型的食谱可能没有名称，这是 API 的正常行为。

## 实现说明

- 该工具基于 `node-bring-api` v2.0.2+ 及其 `getInspirations()` API 开发。
- 需要 Node.js 18.0.0+ 或更高版本。
- 不支持季节性筛选（受 API 限制）。
- 仅提供浏览功能。
- 支持 JSON 格式输出，便于自动化操作。

## 实际应用场景

- **食谱发现**：浏览 Bring! 上可用的食谱。
- **灵感浏览**：查看热门食谱和模板。
- **个人收藏管理**：筛选保存的食谱。
- **数据集成**：将食谱数据以 JSON 格式导出，供外部工具使用。