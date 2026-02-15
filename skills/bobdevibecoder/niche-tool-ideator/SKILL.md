# niche-tool-ideator

该工具专为需求量大的转换工具和实用工具领域生成产品配置文件。

## 概述

该功能维护了一个数据库，其中收录了经过验证的微服务（micro-SaaS）工具创意，并根据搜索量和开发难度对这些创意进行排序。当系统被触发时，它会选择下一个尚未开发的工具，并生成相应的 `product_config.json` 文件。

## 使用方法

- `next tool`：生成优先队列中下一个工具的配置文件。
- `list queue`：显示所有待开发的工具列表。
- `tool status`：显示已开发与未开发的工具状态。

## 工作原理

1. 从 `tool-database.json` 文件中读取优先队列信息。
2. 读取 `products.json` 文件以了解已开发的工具。
3. 选择优先级最高的未开发工具。
4. 根据 `microsaas-factory` 模式生成完整的 `product_config.json` 文件。
5. 将配置文件保存到 `/tmp/openclaw-configs/<slug>_config.json` 目录下。
6. 将选择结果发送到 Telegram。

## 配置文件生成规则

在生成 `product_config.json` 文件时，需遵循以下规则：

### 命名规则
- **名称**：简短且易于记忆（例如：“QRForge”、“InvoiceSnap”、“ColorCraft”）。
- **slug**：使用驼峰式命名法（例如：“qr-forge”、“invoice-snap”、“color-craft”）。
- **缩写**：从名称中提取前两个字母作为缩写（例如：“QF”、“IS”、“CC”）。

### 产品介绍部分
- **徽标**：显示“免费使用 - 无需注册”。
- **标题**：使用 `<span>` 标签突出显示功能，例如：“<span>将</span><span>X</span> 立即转换为</span><span>Y</span>”。
- **副标题**：简短且具有引导性（最多100个字符）。

### 功能介绍（共4项）
- 使用以下图标表示功能：Zap、Shield、Code、Globe、FileText、Lock、Download、Palette、Hash、Key。
  - 功能1：速度/性能优势。
  - 功能2：隐私/安全性优势。
  - 功能3：API访问权限。
  - 功能4：质量/格式优势。

### 定价方案
- **免费版**：每天10次使用权限，最大存储空间1MB。
- **专业版**：每月9美元，无限次使用权限，最大存储空间50MB，并提供API访问权限。

### 转换器代码生成
生成的代码为 TypeScript 语言，包含以下导出内容：
```typescript
export function convertForward(input: string): string { ... }
export function convertBackward(input: string): string { ... }
export function detectFormat(input: string): string { ... }
```

**转换器代码编写规则**：
- 尽量不使用外部依赖项（优先使用 Node.js 内置 API）。
- 如果确实需要第三方包，请将其添加到 `npm_packages` 数组中。
- 代码必须简洁且无误，能够正常编译。
- 需要处理边缘情况（如空输入、无效输入）。
- 为代码添加适当的 TypeScript 类型声明。

### 转换方向
- 每个工具都支持两种转换方向。
- 方向名称使用蛇形命名法（例如：“json_to_yaml”、“yaml_to_json”）。
- 方向标签使用箭头表示（例如：“JSON -> YAML”、“YAML -> JSON”）。

## 工具数据库

`tool-database.json` 文件包含25个经过验证的工具创意，每个条目包含以下信息：
- `id`：唯一标识符。
- `name`：建议的产品名称。
- `category`：转换工具、生成工具、格式化工具或验证工具。
- `priority`：高、中、低。
- `searchVolume`：预估的月搜索量。
- `difficulty`：简单、容易、中等。
- `description`：工具的功能说明。
- `directions`：支持的转换方向（例如：“forward”、“backward”）。
- `sampleInput`/`sampleOutput`：示例输入数据。
- `npmPackages`：所需依赖的包（如无依赖项则留空）。

## 集成步骤
生成配置文件后：
1. 将配置文件保存到 `/tmp/openclaw-configs/<slug>_config.json`。
2. 调用 `product-launcher` 工具进行构建和部署。
- 或者先通过 Telegram 报告给相关人员以获取手动批准（如果通过 cron 任务运行）。

## Cron 任务模式

当 `niche-tool-ideator` 通过 cron 任务被触发时：
1. 从队列中选择下一个未开发的工具。
2. 生成配置文件。
3. 发送消息到 Telegram：“[工具名称]（[功能描述]）已准备好构建。回复‘go’开始构建，或回复‘skip’跳过。”
4. 如果用户在24小时内回复‘go’，则启动 `product-launcher` 工具进行构建。
5. 如果没有回复，则自动开始构建（完全自动化模式）。