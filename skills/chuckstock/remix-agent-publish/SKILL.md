---
name: remix-agent-publish
description: 使用 server-api v1 代理的 REST API 以及 Farcade 游戏 SDK 的要求，为 remix.gg 平台构建 Remix 游戏。
metadata:
  tags: remix, games, api, agent, publishing
---

## 适用场景

当用户希望使用 AI 代理或外部服务来自动将游戏发布到 Remix (`remix.gg`) 平台时，可以使用此技能。

## 使用方法

1. 首先阅读 [API 认证](api/authentication.md) 的相关内容。
2. 在生成 API 调用之前，先从 `https://api.remix.gg/docs/json` 获取 OpenAPI 规范。
3. 参考 [API 参考文档](api/reference.md) 以了解工作流程的规范（但不要将其视为方法或路径的最终权威来源）。
4. 对于基于 Phaser 的游戏开发，请使用 [Phaser 2D Arcade 伴侣技能](frameworks/phaser-2d-arcade/SKILL.md)。
5. 对于轻量级的 3D 游戏开发，建议使用 [Three.js Lite 伴侣技能](frameworks/threejs-lite/SKILL.md)。
6. 在生成或修改游戏代码时，请参考 [游戏 SDK 参考文档](references/game-sdk.md)。
7. 遵循 [提交规则](rules/submission-requirements.md) 以确保代码符合平台要求。
8. 为了实现以移动设备优先且兼容 SDK 的开发方式，请遵循 [游戏开发最佳实践](rules/game-creation-best-practices.md)。
9. 如需客户端集成示例，请参考 [REST 客户端代码片段](snippets/rest-client.md)。
10. 对于辅助工作流程，可以使用 [MCP 快速入门指南](mcp/quickstart.md)。

## 权威信息来源

当文档描述与实际运行时的行为存在差异时，请以服务器 API 文档和 OpenAPI 文档为准：

- `https://api.remix.gg/docs`
- `https://api.remix.gg/docs/json`
- `apps/server-api/routes/agents.ts`
- `apps/server-api/lib/api-auth.ts`
- `apps/server-api/lib/agent-api.ts`
- `apps/server-api/app/[...path]/route.ts`
- `packages/game-sdk/src/index.ts`