---
name: flowfi-openclaw
description: 通过使用Bearer令牌认证，可以从OpenClaw代理与FlowFi API进行交互；执行创建/读取/更新工作流（workflows）的操作，以及部署和管理工作流的生命周期相关动作。当代理需要调用FlowFi后端来处理工作流或自动化任务时，应使用此方法。
---

# FlowFi – OpenClaw 技能

当 OpenClaw 代理需要调用 FlowFi 后端时，请使用此技能：创建工作流、列出/更新/部署工作流或管理相关评论。

## 使用场景

- 用户或 FlowFi 节点触发 OpenClaw 代理，该代理需要与 FlowFi 进行交互（如创建、更新或部署工作流，或管理评论）。
- 代理需要使用 FlowFi 的 REST API，并进行承载令牌（Bearer token）身份验证。

## 使用说明

1. **身份验证**  
   使用 FlowFi 提供的承载令牌（从 FlowFi 的配置文件或环境变量中获取），并将其以 `Bearer <token>` 的格式添加到 `Authorization` 头部中。

2. **基础 URL**  
   使用 FlowFi 后端的基础 URL（例如，从 FlowFi 的配置文件或 `FLOWFI_API_URL` 中获取），然后根据需要添加路径（如 `/api/workflows`、`/api/workflows/:id/deploy`）。

3. **工作流操作**  
   - 创建工作流：使用 `POST /api/workflows` 方法，并传递工作流的相关数据。
   - 读取工作流信息：使用 `GET /api/workflows` 或 `GET /api/workflows/:id` 方法。
   - 更新工作流：使用 `PATCH` 或 `PUT` 方法对工作流资源进行更新（具体操作方式请参考相关文档）。

4. **部署与工作流生命周期管理**  
   使用 `reference.md` 中描述的端点来执行部署、运行或其他与工作流生命周期相关的操作。

5. **错误处理**  
   如果收到非 2xx 状态码的响应，请读取响应内容，并向用户或 FlowFi 节点显示简短的错误信息（例如，记录在 `error` 文件或日志中）。

## 参考文档

有关端点详情、请求/响应格式及示例，请参阅本文件夹中的 **reference.md** 文件。有关 FlowFi OpenClaw 节点的输入/输出参数及配置信息，请参阅 **nodes.md** 文件。