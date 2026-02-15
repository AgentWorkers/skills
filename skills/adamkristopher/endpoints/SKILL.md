---
name: endpoints
description: "**端点文档管理 API 工具包**  
该工具包支持使用人工智能技术对文档进行扫描，并将提取的结构化数据组织到分类后的端点中。适用于用户需要执行以下操作的场景：  
- 扫描文档  
- 上传文件  
- 列出所有端点  
- 检查端点数据  
- 查看使用统计信息  
- 创建或删除端点  
- 获取文件 URL  
- 管理文档元数据  

使用该工具包前，需要从 `endpoints.work` 仪表板中获取 `ENDPOINTS_API_KEY` 这个访问密钥。"
---

# Endpoints API 工具包

## 设置

安装依赖项：

```bash
cd scripts && npm install
```

通过在项目根目录下创建一个 `.env` 文件来配置凭据：

```
ENDPOINTS_API_URL=https://endpoints.work
ENDPOINTS_API_KEY=ep_your_api_key_here
```

**前提条件**：您需要拥有一个 Endpoints 账户以及 API 密钥。您可以从 [API 密钥页面](https://endpoints.work/api-keys) 生成 API 密钥。

## 快速入门

| 用户操作 | 调用的函数 |
|-----------|-----------------|
| “列出我的端点” | `listEndpoints()` |
| “显示 /job-tracker/january 的端点详细信息” | `getEndpoint('/job-tracker/january')` |
| “扫描此文档” | `scanFile('/path/to/file.pdf', 'job tracker')` |
| “扫描此文本” | `scanText('Meeting notes...', 'meeting tracker')` |
| “为收据创建一个端点” | `createEndpoint('/receipts/2026')` |
| “删除旧的端点” | `deleteEndpoint('/category/slug')` |
| “删除该条目” | `deleteItem('abc12345')` |
| “获取文件 URL” | `getFileUrl('userid/path/file.pdf')` |
| “查看我的使用情况” | `getStats()` |

通过导入 `scripts/src/index.ts` 来执行这些函数：

```typescript
import { listEndpoints, scanText, getStats } from './scripts/src/index.js';

const categories = await listEndpoints();
const result = await scanText('Meeting with John about Q1 goals', 'meeting tracker');
const stats = await getStats();
```

或者直接使用 `.tsx` 文件运行：

```bash
npx tsx scripts/src/index.ts
```

## 工作流程模式

每个分析过程都遵循三个阶段：

### 1. 分析
调用 API 函数。每次调用都会触发 Endpoints API 并返回结构化数据。

### 2. 自动保存
所有结果会自动保存为 JSON 文件，文件保存在 `results/{category}/` 目录下。文件命名规则如下：
- 有名称的结果文件：`{sanitized_name}.json`
- 自动生成的文件：`YYYYMMDD_HHMMSS__{operation}.json`

### 3. 总结
分析完成后，读取保存的 JSON 文件，并在 `results/summaries/` 目录下生成一个 Markdown 总结文件，其中包含数据表、洞察结果以及提取的实体信息。

## 高级函数

| 函数 | 功能 | 返回内容 |
|----------|---------|----------------|
| `listEndpoints()` | 按类别列出所有端点 | 包含类别和端点的树状结构 |
| `getEndpoint(path)` | 获取端点详细信息 | 包含旧版本和新版本的完整元数据 |
| `scanText(text, prompt)` | 使用 AI 扫描文本 | 提取实体信息及端点路径 |
| `scanFile(filePath, prompt)` | 使用 AI 扫描文件（PDF、图片、文档） | 提取实体信息及端点路径 |
| `getStats()` | 获取使用统计信息 | 包括使用量、存储空间等信息 |

## 单个 API 函数

如需进行更细粒度的控制，请导入相应的函数。请参阅 [references/api-reference.md](references/api-reference.md)，其中列出了所有函数的参数、类型和示例。

### 端点函数

| 函数 | 功能 |
|----------|---------|
| `listEndpoints()` | 按类别列出所有端点 |
| `getEndpoint(path)` | 获取端点的完整详细信息（包括元数据） |
| `createEndpoint(path)` | 创建一个新的空端点 |
| `deleteEndpoint(path)` | 删除端点及其所有关联文件 |

### 扫描函数

| 函数 | 功能 |
|----------|---------|
| `scanText(text, prompt)` | 使用 AI 扫描文本内容并提取信息 |
| `scanFile(filePath, prompt)` | 使用 AI 扫描文件（PDF、图片、文档） |

### 条目函数

| 函数 | 功能 |
|----------|---------|
| `deleteItem(itemId)` | 根据 8 位 ID 删除单个条目 |

### 文件函数

| 函数 | 功能 |
|----------|---------|
| `getFileUrl(key)` | 获取文件的预签名 S3 URL |

### 计费函数

| 函数 | 功能 |
|----------|---------|
| `getStats()` | 获取使用统计信息（包括使用量、存储空间等） |

## 数据结构

### Living JSON 模式

Endpoints 使用 Living JSON 模式来记录文档历史：

```typescript
{
  endpoint: { path, category, slug },
  metadata: {
    oldMetadata: { ... },  // Historical items
    newMetadata: { ... }   // Recent items
  }
}
```

### 元数据条目

每个条目包含以下信息：
- **8 位 ID** - 唯一标识符（例如：`abc12345`）
- **summary** - 由 AI 生成的描述
- **entities** - 提取的实体（人名、公司名称、日期等）
- **filePath** - 如果文件已上传，则包含 S3 文件路径
- **fileType** | 文件的 MIME 类型
- **originalText** | 原始文本

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 401 | API 密钥无效或缺失 |
| 404 | 未找到端点或条目 |
| 409 | 端点已存在 |
| 429 | 超过使用限制 |

## 示例

### 列出和检查端点

```typescript
// Get all endpoints
const { categories } = await listEndpoints();
console.log(`Found ${categories.length} categories`);

// Inspect specific endpoint
const details = await getEndpoint('/job-tracker/january');
console.log(`Total items: ${details.totalItems}`);
```

### 扫描文档

```typescript
// Scan text content
const result = await scanText(
  'Email from John Smith at Acme Corp about the Q1 contract renewal',
  'business contacts'
);
console.log(`Created endpoint: ${result.endpoint.path}`);

// Scan a PDF file
const fileResult = await scanFile('./invoice.pdf', 'invoice tracker');
console.log(`Extracted ${fileResult.entriesAdded} items`);
```

### 查看使用情况

```typescript
const stats = await getStats();
console.log(`Parses: ${stats.parsesUsed}/${stats.parsesLimit}`);
console.log(`Storage: ${stats.storageUsed} bytes`);
```