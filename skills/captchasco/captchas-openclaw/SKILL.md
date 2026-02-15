---
name: captchas-openclaw
description: OpenClaw集成指南：针对CAPTCHAS Agent API的使用，包括OpenResponses工具的架构说明以及插件工具的注册方法。
homepage: https://captchas.co
metadata: {"openclaw":{"emoji":"🧩","requires":{"env":["CAPTCHAS_API_KEY","CAPTCHAS_ENDPOINT"]},"primaryEnv":"CAPTCHAS_API_KEY"}}
---

# 图形验证码（CAPTCHAs）与 OpenClaw 的集成

当需要通过 OpenResponses 工具或 OpenClaw 插件将图形验证码功能与 OpenClaw 集成时，请使用此技能。

## 配置

设置环境变量：

- `CAPTCHAS_ENDPOINT` = `https://agent.captchas.co`
- `CAPTCHAS_API_KEY` = `<your-api-key>`

请求头：

- `x-api-key`：必填项（使用 `CAPTCHAS_API_KEY`）。
- `x-domain`：可选项；如果提供，则会进行验证。

注意事项：

- `site_key` 是可选项；如果省略，系统会从 API 密钥或账户默认值中自动获取。
- 请避免在请求数据中传输个人身份信息（PII）。

## OpenResponses 工具的请求格式（OpenClaw 网关）

在调用 `/v1/responses` 端点时，需使用 OpenClaw 的 `tools` 数组格式。

```json
{
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "captchas_agent_verify",
        "description": "Run CAPTCHAS Agent Verify and return a decision (allow|deny|challenge).",
        "parameters": {
          "type": "object",
          "properties": {
            "site_key": {"type": "string"},
            "action": {"type": "string"},
            "signals": {"type": "object", "additionalProperties": true},
            "capabilities": {
              "oneOf": [
                {"type": "object", "additionalProperties": true},
                {"type": "array", "items": {"type": "string"}}
              ]
            },
            "verification_mode": {"type": "string", "enum": ["backend_linked", "agent_only"]},
            "challenge_source": {"type": "string", "enum": ["bank", "ai_generated"]},
            "input_type": {"type": "string", "enum": ["choice", "image", "behavioral"]},
            "media_url": {"type": "string"},
            "media_type": {"type": "string"}
          },
          "required": [],
          "additionalProperties": false
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "captchas_agent_challenge_complete",
        "description": "Complete a challenge and mint a verification token when passed.",
        "parameters": {
          "type": "object",
          "properties": {
            "challenge_id": {"type": "string"},
            "site_key": {"type": "string"},
            "answer": {"type": "string"}
          },
          "required": ["challenge_id", "answer"],
          "additionalProperties": false
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "captchas_agent_token_verify",
        "description": "Verify an opaque CAPTCHAS token before completing a sensitive action.",
        "parameters": {
          "type": "object",
          "properties": {
            "token": {"type": "string"},
            "site_key": {"type": "string"},
            "domain": {"type": "string"}
          },
          "required": ["token"],
          "additionalProperties": false
        }
      }
    }
  ]
}
```

## OpenClaw 插件工具的注册

使用 `api.registerTool(...)` 方法注册工具，并使用与上述相同的 JSON 格式参数。

示例：

```js
api.registerTool({
  name: "captchas_agent_verify",
  description: "Run CAPTCHAS Agent Verify and return a decision (allow|deny|challenge).",
  parameters: {
    type: "object",
    properties: {
      site_key: { type: "string" },
      action: { type: "string" },
      signals: { type: "object", additionalProperties: true }
    },
    required: [],
    additionalProperties: false
  },
  async execute(_id, params) {
    return { content: [{ type: "text", text: JSON.stringify(params) }] };
  }
});
```

## 参考资料

- 使用 `/v1/agent/verify`、`/v1/agent/challenge/:id/complete` 和 `/v1/agent/token-verify` 作为官方推荐的 API 调用方法。
- 有关工作流程的详细指导，请参阅 `captchas-human-verification/SKILL.md`。