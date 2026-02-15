# Agent Identity Kit — OpenClaw Skill

这是一个用于AI代理的便携式身份管理系统，支持创建、验证和发布`agent.json`身份文件。

## 该技能的功能

- **创建**代理身份文件（`agent.json`），通过交互式设置完成；
- **验证**身份文件是否符合Agent Card v1的规范；
- **提供**JSON规范，以便集成到编辑器或持续集成（CI）流程中。

## 快速入门

### 生成新的`agent.json`文件

```bash
./scripts/init.sh
```

系统会提示您输入代理的名称、处理方式（handle）、描述、所有者以及代理的功能。生成后，会得到一个有效的`agent.json`文件。

### 验证现有的`agent.json`文件

```bash
./scripts/validate.sh path/to/agent.json
```

系统会使用`schema/agent.schema.json`来验证文件内容。如果缺少`ajv-cli`工具，系统会自动安装该工具。

## 文件结构

```
agent-identity-kit/
├── schema/
│   └── agent.schema.json       # JSON Schema v1 for Agent Cards
├── examples/
│   ├── kai.agent.json           # Full-featured example (Kai @ Reflectt)
│   ├── minimal.agent.json       # Bare minimum valid card
│   └── team.agents.json         # Multi-agent team roster
├── skill/
│   ├── SKILL.md                 # This file
│   └── scripts/
│       ├── init.sh              # Generate a starter agent.json
│       └── validate.sh          # Validate against schema
└── README.md
```

## 规范字段

| 字段        | 是否必填 | 描述                                      |
|------------|---------|-----------------------------------------|
| `version`     | ✅       | 规范版本（例如：“1.0”）                          |
| `agent.name`    | ✅       | 代理的显示名称                              |
| `agent.handle`    | ✅       | Fediverse风格的标识符（格式为`@name@domain`）           |
| `agent.description` | ✅       | 代理的功能描述                              |
| `owner.name`    | ✅       | 所有者的名称                               |
| `capabilities`  | —        | 代理支持的功能标签列表                          |
| `protocols`    | —        | 支持的协议（MCP、A2A、HTTP）                        |
| `trust.level`    | —        | 信任状态（`new`、`active`、`established`、`verified`）       |
| `endpoints.card` | —        | 身份文件的官方URL                            |
| `links`      | —        | 代理的网站、代码仓库或社交媒体链接                        |

## 托管您的身份文件

将您的`agent.json`文件托管在一个知名的URL地址上：

```
https://yourdomain.com/.well-known/agent.json
```

如果需要管理多个代理，可以按照以下步骤操作：

```
https://yourdomain.com/.well-known/agents.json
```

## 与forAgents.dev的集成

将您的代理注册到[foragents.dev](https://foragents.dev)，以便在全球代理目录中显示。经过验证的代理会在其身份文件上显示相应的徽章。

## 规范参考

完整规范：<https://foragents.dev/spec/agent-card>
JSON规范：<https://foragents.dev/schemas/agent-card/v1.json>