---
name: AI 3D Generation
slug: 3d-generation
version: 1.0.0
homepage: 
description: 使用 Neural4D API 创建、转换并下载由 AI 生成的三维模型。该技术专为商业应用流程进行了优化。
changelog: Initial release with Text-to-3D, Image-to-3D matting pipelines, and physical format conversion (STL/FBX/USDZ).
metadata: {"clawdbot":{"requires":{"bins":["curl", "jq"],"env.optional":["NEURAL4D_API_TOKEN"],"config":["~/neural4d-3d-generation/"]},"os":["linux","darwin","win32"]}}
---
## 设置

首次使用时，请确保已设置 `NEURAL4D_API_TOKEN` 环境变量。所有 API 请求都必须包含以下头部信息：`Authorization: Bearer <YOUR_TOKEN>`。

## 使用场景

当需要使用 DreamTech 的 Neural4D 引擎根据文本提示或图像生成 3D 模型时，可以使用此功能。该功能特别适用于需要精确格式转换（如 `.stl`、`.obj`、`.fbx`）以及物理尺寸的资产创建，以适应制造工作流程。

## 核心规则与费用限制

### 1. API 资源消耗监控

在执行批量操作之前，请务必跟踪 API 资源的消耗情况：
- **文本转 3D：**每次操作消耗 20 个资源点。
- **图像转 3D：**每次操作消耗 20 个资源点。
- **Qibi 风格生成：**每次操作消耗 30 个资源点。
- **格式转换：**每次操作消耗 10 个资源点。
- 您可以通过 `/api/queryPointsInfo` 查询剩余资源余额。

### 2. 异步请求处理

模型生成是异步进行的，您需要通过轮询来获取生成结果：
- 使用 `uuid` 呼叫 `/api/retrieveModel` 来查询生成进度。
- 检查 `codeStatus` 的值：
  - `0`：生成完成。
  - `1`：正在生成中（请继续轮询）。
  - `-3`：生成失败。

## 工作流程

### 流程 A：文本转 3D
1. **请求：**发送 `POST` 请求到 `https://alb.neural4d.com:3000/api/generateModelWithText`，请求体内容为：`{"prompt": "...", "modelCount": 4, "disablePbr": 0}`。
2. **获取结果：**从响应中提取 `uuids`。
3. **轮询：**使用提取到的 `uuid` 重复调用 `/api/retrieveModel`，直到 `codeStatus` 为 `0`。
4. **下载：**提取 `modelUrl` 并下载生成的 `.glb` 文件。

### 流程 B：图像转 3D（严格的三步流程）
1. **图像预处理：**通过 `multipart/form-data` 将图像（JPG/PNG 格式，文件大小 <10MB，分辨率 256x256 至 6048x8064）上传到 `/api/mattingImage`，并获取 `requestId`。
2. **获取预处理结果：**将 `requestId` 发送到 `/api/getMattedResult`，并从响应中提取所需的 `fileKey`。
3. **生成模型：**使用 `fileKey` 调用 `/api/generateModelWithImage` 开始模型生成，并接收生成的 `uuids`。
4. **轮询：**使用 `/api/retrieveModel` 检查生成进度并获取 `modelUrl`。

### 流程 C：面向制造的格式转换

对于物理原型制作，需要将生成的 `.glb` 文件转换为所需的格式：
1. **请求：**发送 `POST` 请求到 `https://alb.neural4d.com:3000/api/convertToFormat`，请求体内容包含 `uuid`、所需的模型格式（如 `stl`、`fbx`、`obj`）以及模型尺寸（单位：毫米，且尺寸必须大于 1）。
2. **检查进度：**查看 `statusType` 的值：
   - `0`：转换完成，可以使用 `modelUrl` 下载模型文件。
   - `1`：转换中（请稍后重试）。
   - `-1`：转换失败或参数错误。

## 外部接口参考

所有请求均通过基础 URL `https://alb.neural4d.com:3000/api` 进行路由。

| 功能 | 接口地址 | 认证方式 | 功能描述 |
|--------|----------|------|---------|
| 文本转 3D | `/generateModelWithText` | Bearer Token | 根据文本提示生成 3D 模型 |
| 获取模型信息 | `/retrieveModel` | Bearer Token | 查询模型生成状态并获取模型 URL |
| 图像预处理 | `/mattingImage` | Bearer Token | 对图像进行预处理 |
| 获取预处理结果 | `/getMattedResult` | 获取用于模型生成的文件键 |
| 图像转 3D | `/generateModelWithImage` | Bearer Token | 根据预处理后的文件键生成 3D 模型 |
| 格式转换 | `/convertToFormat` | Bearer Token | 将模型格式转换为 `.stl`、`.fbx` 或 `.obj`，并保留物理尺寸信息 |
| 检查作业进度 | `/queryJobProgress` | Bearer Token | 查看作业完成百分比 |