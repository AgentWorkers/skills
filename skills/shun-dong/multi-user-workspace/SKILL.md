---
name: multi-user-workspace
description: 支持多用户工作空间管理，具备沙箱权限机制、用户个人资料功能以及用户关系网络功能。
---

# 朋友

支持配置针对每个用户的会话环境（包含沙箱隔离功能）、用户个人资料以及用户间关系的管理。

## 核心概念

- **UserId**：小写形式的唯一标识符（例如 `alice`、`bob`），用于会话键、文件名以及跨引用中。
- **Session**：每个用户对应一个会话，格式为 `agent:<agentId>:<mainKey>`，其中 `mainKey` 通常包含用户的 `userId`。
- **Sandbox**：可选的会话隔离机制（基于 Docker），配置信息存储在 `openclaw.json` 中。
- **FRIENDS/****：用户个人资料目录（每个用户对应一个文件，文件名为 `{userId}.md`）。
- **RELATIONS/****：用户间关系记录目录（文件格式为 `{userId1}-{userId2}.md`，按字母顺序排序，可记录多个用户之间的关系）。

## 示例工作区结构

```
workspace/
├── USER.md              # User registry with permissions
├── AGENTS.md            # Multi-user guidance for assistant
├── FRIENDS/
│   ├── alice.md        # alice's profile
│   └── bob.md          # bob's profile
├── RELATIONS/
│   └── alice-bob.md    # Relationship between alice and bob
├── private/            # Admin-only files (optional)
...
```

## USER.md

存储所有用户的资料。助手会读取该文件以识别用户并提取用户的 `userId` 和 `Name`。

**格式：**

```markdown
# User Registry

## Users

### alice
- UserId: alice
- Name: Alice
- Role: administrator

### bob
- UserId: bob
- Name: Bob
- Role: guest
```

**注意：** `userId` 是唯一的且为小写形式。请通过 `openclaw.json` 中的 `Role` 字段来配置用户的沙箱环境。

## FRIENDS/

用户个人资料目录。每个用户对应一个 Markdown 文件（文件名为 `{userId}.md`）。

文件内容可以自由定制。常见的包含部分包括：

```markdown
# Alice

## Info
- UserId: alice
- Name: Alice
- Role: administrator
- Emails: alice@example.com
...
## Assistant Relationship
- How the user prefers to interact with the assistant
- Preferred communication style
- Ongoing projects or interests

## Notes
Free-form information about the user.
```

## RELATIONS/

记录用户间的关系。文件格式为 `{userId1}-{userId2}.md`（按字母顺序排序，可记录多个用户之间的关系）。

文件内容可以自由定制。示例：

```markdown
# Alice & Bob

## Users
- **alice**: Alice
- **bob**: Bob

## Relationship
Friends who collaborate on projects.

## Information Sharing
- Can mention each other's public projects
- Do not share private details without asking
```

## AGENTS.md

用于向助手提供指令的配置文件。请添加此部分：

```markdown
## User Identification

When a session starts (after `/new`):

1. Get current session via `session_status`
2. Extract userId from the session key (e.g., `agent:main:alice` → `alice`)
3. Read `FRIENDS/{userId}.md` for user profile
4. Read `RELATIONS/*{userId}*.md` for all relationships involving this user
5. Greet the user by name

## Cross-User Boundaries

- Default: Information does not flow between users
- Exception: Only when explicitly defined in RELATIONS/
```

## 会话配置

每个用户都会获得一个具有可配置沙箱环境及工具权限的独立会话。具体配置信息请参考 `openclaw.json`。

### 管理员配置

管理员拥有完全访问权限，且不受沙箱限制：

```json5
{
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
    },
    list: [
      {
        id: "main",
        // Administrator: no sandbox, all tools allowed
        sandbox: { mode: "off" },
      },
    ],
  },
  bindings: [
    // Route admin sessions to main agent without sandbox
    { agentId: "main", match: { session: { regex: "alice$" } } },
  ],
}
```

### 客户端配置

客户端会获得一个隔离的工作区环境。客户端用户只能在其自己的目录内进行读写/执行操作：

```json5
{
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
    },
    list: [
      {
        id: "main",
        // Guest: sandbox enabled, isolated directory
        sandbox: {
          mode: "all",
          scope: "session",
          workspaceAccess: "none",  // Don't mount main workspace
          docker: {
            binds: [
              // Mount guest's own directory as /workspace
              "~/.openclaw/workspace/guests/bob:/workspace:rw"
            ]
          }
        },
        tools: {
          allow: ["read", "write", "edit", "exec", "process"],
          deny: ["browser", "canvas", "nodes", "cron", "gateway"],
        },
      },
    ],
  },
  bindings: [
    // Route guest sessions to sandboxed agent
    { agentId: "main", match: { session: { regex: "bob$" } } },
  ],
}
```

## 目录结构说明：

```bash
mkdir -p ~/.openclaw/workspace/guests/bob
```

**注意事项：**

- 客户端用户将 `/workspace` 目录视为自己的根目录（与主工作区隔离）。
- 客户端用户可以在自己的目录内自由读写/执行操作。
- 客户端用户无法访问 `USER.md`、`FRIENDS/`、`RELATIONS/` 目录或其他用户的数据。

### 配置选项

**沙箱设置：**

- `mode`：`"off"` | `"all"` — 禁用或启用沙箱功能。
- `scope`：`"session"` — 每个用户会话对应一个独立的 Docker 容器。
- `workspaceAccess`：`"none"` | `"ro"` | `"rw"` — 客户端用户对工作区文件的访问权限（只读/读写）。

**工具设置：**

- `allow`：允许使用的工具名称列表。
- `deny`：禁止使用的工具名称列表（会覆盖 `allow` 中的设置）。

**路由规则：**

- `bindings[].match.session.regex`：用于匹配会话键的模式（例如，`alice$` 表示以 “alice” 结尾的会话）。