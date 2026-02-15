# API 文档生成器

该工具可根据 API 端点描述自动生成可用于生产的 API 文档，包括 OpenAPI 3.0 规范、Markdown 参考文档以及 SDK 快速入门指南。

## 使用方法

只需描述您的 API 端点，该工具即可生成以下内容：

1. **OpenAPI 3.0 规范** — 机器可读的规范文件，可直接导入到 Swagger 或 Postman 中使用；
2. **Markdown 参考文档** — 以人类可读的形式呈现的端点文档，包含示例代码；
3. **SDK 快速入门指南** — 为开发者提供的集成指南，可直接复制使用。

## 使用说明

当用户提供 API 端点的详细信息（包括路由、方法、参数和响应内容）时，该工具会执行以下操作：

- 生成完整的 OpenAPI 3.0 YAML 规范文件；
- 生成 Markdown 参考文档，内容包括：
  - 认证相关内容；
  - 每个端点的详细信息（方法、路径、描述、参数表、请求/响应示例）；
  - 错误代码说明；
  - 速率限制相关提示；
- 生成快速入门指南，其中包含使用 `curl` 命令的示例代码以及适用于多种编程语言（Python、JavaScript、Go）的集成示例。

### 输出格式

```yaml
# openapi.yaml — full OpenAPI 3.0 spec
```

```markdown
# API Reference — human-readable docs
```

```markdown
# Quickstart Guide — integration examples
```

### 质量标准

- 每个端点都必须提供请求和响应的示例数据；
- 使用真实的示例数据，而非简单的 “string” 或 “example”；
- 必须包含错误响应（如 400、401、403、404、500 等）；
- 需要详细记录分页、过滤和排序的实现方式；
- 需要说明任何重大变更及版本控制策略。

## 使用技巧

- 可直接粘贴端点路由文件或控制器代码，以便工具自动提取相关信息；
- 该工具支持 REST、GraphQL（基于schema 的架构）和 gRPC（基于 proto 的架构）；
- 可与持续集成/持续部署（CI/CD）流程结合使用，实现每次部署时自动生成文档。

---

由 [AfrexAI](https://afrexai-cto.github.io/context-packs/) 开发 — 专为快速交付产品的团队打造的 AI 驱动型业务工具。