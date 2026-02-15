---
name: coda-packs
description: 通过 REST API v1 管理 Coda 包：支持列出、创建、更新和删除私有包。需要使用 CODA_API_TOKEN。删除操作需要确认。注意：构建、作品集提交、数据分析以及协作功能需要使用 Coda 的 Pack SDK CLI，这些功能无法通过 REST API 实现。
---

# Coda Packs 技能

通过 REST API v1 管理 Coda Packs。支持创建、列出、更新和删除私有 Pack。

## ⚠️ API 限制

Coda REST API v1 的 Pack 管理功能有限：

| 功能 | REST API | Pack SDK CLI |
|---------|----------|--------------|
| **列出 Pack** | ✅ 可用 | ✅ |
| **创建 Pack** | ✅ 可用 | ✅ |
| **更新 Pack** | ✅ 可用 | ✅ |
| **删除 Pack** | ✅ 可用 | ✅ |
| **构建 Pack 版本** | ❌ 不可用 | ✅ 必需 |
| **提交到图库** | ❌ 不可用 | ✅ 必需 |
| **分析数据** | ❌ 不可用 | ✅ 必需 |
| **协作者管理** | ❌ 不可用 | ✅ 必需 |

**如需进行构建、提交到图库或使用高级功能，请使用：**
```bash
npx @codahq/packs-sdk register    # Create account
npx @codahq/packs-sdk build       # Build Pack
npx @codahq/packs-sdk release     # Submit to Gallery
```

## 适用场景

当用户需要执行以下操作时，请使用此技能：
- 列出现有的 Coda Packs
- 创建新的私有 Pack
- 更新 Pack 的元数据（名称、描述）
- 删除未使用的 Pack

## 不适用场景

- **请勿** 用于文档管理（如表格、行、页面） → 使用 `coda` 技能
- **请勿** 用于构建 Pack 版本 → 使用 Pack SDK CLI
- **请勿** 用于提交到图库 → 使用 Pack SDK CLI
- **请勿** 用于查看分析数据 → 使用 Pack SDK CLI 或 Coda 网页界面

## 先决条件

1. **API Token**：设置环境变量 `CODA_API_TOKEN`
   - 在以下链接获取 Token：https://coda.io/account -> API Settings
   - 必须具有 Pack 管理权限

2. **Python 3.7+** 及 `requests` 库

## 快速入门

```bash
# Setup
export CODA_API_TOKEN="your_token_here"

# List your Packs
python scripts/coda_packs_cli.py packs list

# Create new Pack shell
python scripts/coda_packs_cli.py packs create \
  --name "My Integration" \
  --description "Does cool things"

# Update Pack
python scripts/coda_packs_cli.py packs update my-pack-id \
  --description "Updated description"

# Delete Pack (requires confirmation)
python scripts/coda_packs_cli.py packs delete my-pack-id
```

## 完整的 Pack 开发工作流程

由于 REST API 仅支持基本的 Pack 管理功能，以下是完整的开发流程：

### 第 1 步：通过 REST API 创建 Pack
```bash
python scripts/coda_packs_cli.py packs create \
  --name "Karakeep Bookmarks" \
  --description "Save and search bookmarks"
```

### 第 2-4 步：使用 Pack SDK CLI（必需）
```bash
# Install Pack SDK
npm install -g @codahq/packs-sdk

# Initialize Pack project
npx @codahq/packs-sdk init karakeep-pack

# Develop your Pack (edit pack.ts)
# See: https://coda.io/packs/build/latest/guides/quickstart/

# Build and upload
npx @codahq/packs-sdk build
npx @codahq/packs-sdk upload

# Submit to Gallery (when ready)
npx @codahq/packs-sdk release
```

## CLI 工具使用说明

### Pack 管理

```bash
# List all your Packs
python scripts/coda_packs_cli.py packs list

# Get Pack details
python scripts/coda_packs_cli.py packs get 48093
python scripts/coda_packs_cli.py packs get "Karakeep"

# Create new Pack
python scripts/coda_packs_cli.py packs create \
  --name "My Pack" \
  --description "Description" \
  --readme "# My Pack\n\nDetails here"

# Update Pack metadata
python scripts/coda_packs_cli.py packs update my-pack-id \
  --name "New Name" \
  --description "New description"

# Delete Pack (requires confirmation)
python scripts/coda_packs_cli.py packs delete my-pack-id
# Or skip confirmation: --force
```

### Pack ID 的识别方式

CLI 支持使用 **数字 Pack ID** 和 **Pack 名称**：

```bash
# These are equivalent:
python scripts/coda_packs_cli.py packs get 48093
python scripts/coda_packs_cli.py packs get "Karakeep"
```

如果 Pack 名称存在歧义，CLI 会列出所有匹配的 Pack 并退出。

## 安全防护措施

### 需要确认的操作

| 操作 | 风险 | 确认方式 |
|-----------|------|--------------|
| **删除 Pack** | 不可逆 | “确定要删除 Pack ‘X’ 吗？此操作无法撤销。” |

### 无需确认的操作

- **创建 Pack**：安全且可逆
- **列出/获取 Pack**：仅读操作
- **更新 Pack**：可逆操作

## 错误处理

常见的 API 错误：

| 错误代码 | 含义 | 解决方案 |
|------|---------|------------|
| `401` | 无效的 Token | 重新获取 CODA_API_TOKEN |
| `403` | 权限不足 | 确保拥有 Pack 管理权限 |
| `404` | 未找到 Pack | 检查 Pack ID 或名称 |
| `429` | 请求频率限制 | 等待片刻后重试（系统自动处理）

## 参考资料

- **Pack SDK 使用指南**：https://coda.io/packs/build/latest/guides/overview/
- **Pack SDK 快速入门**：https://coda.io/packs/build/latest/guides/quickstart/
- **Coda API 文档**：https://coda.io/developers apis/v1
- **Pack SDK NPM 包**：https://www.npmjs.com/package/@codahq/packs-sdk

## 示例：Karakeep Pack

创建示例 Pack：
- **名称**：Karakeep
- **ID**：48093
- **描述**：Karakeep 书签管理工具——用于保存 URL、搜索和按标签组织内容

**完成 Pack 开发的下一步操作：**
1. 使用 Pack SDK CLI：`npx @codahq/packs-sdk init karakeep-pack`
2. 实现 Karakeep 的 API 集成（参见：https://docs.karakeep.app/api/）
3. 构建并上传 Pack：`npx @codahq/packs-sdk build && npx @codahq/packs-sdk upload`