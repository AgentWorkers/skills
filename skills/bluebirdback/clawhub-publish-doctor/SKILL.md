---
name: clawhub-publish-doctor
description: 诊断并解决 ClawHub/ClawDHUB 在发布技能时遇到的问题（如身份验证失败、浏览器登录问题、依赖项缺失、安全扫描待处理错误，以及技能/配置文件URL错误等）。当尝试将技能发布到 ClawHub 时遇到问题，或者需要检查临时错误报告，或者希望采用包含重试机制的更安全的发布与验证流程时，可以使用此方法。
---
# ClawHub 发布工具

通过预检、更安全的发布命令以及发布后的验证机制来稳定 ClawHub 的发布流程，这些机制能够容忍注册表状态的临时变化。

## 快速工作流程

1. 运行预检：
   - `scripts/clawhub_preflight.sh`

2. 如果出现登录或浏览器相关问题，请参考 `references/error-map.md`。

3. 使用具有重试功能的验证机制进行发布：
   - `scripts/clawhub_publish_safe.sh <skill_path> <slug> <name> <version> [changelog]`

4. 如果 `inspect` 命令仍然失败，请先根据 `references/error-map.md` 对错误进行分类，再考虑进一步处理。

## 标准命令

### 预检
```bash
bash scripts/clawhub_preflight.sh
```

### 登录（基于令牌，适用于无头环境）
```bash
clawhub login --token <clh_token>
clawhub whoami
```

### 安全发布
```bash
bash scripts/clawhub_publish_safe.sh ./my-skill my-skill "My Skill" 1.0.0 "Initial release"
```

### 手动检查
```bash
clawhub inspect my-skill --json
```

## 规则

- 在服务器或无头环境中，建议使用令牌登录。
- 发布后出现的 `inspect` 错误可能属于暂时性问题（通常在几分钟内消失）。
- 通过 CLI (`clawhub inspect`) 和网页 URL (`/skills/<slug>` 进行双重验证。
- 使用规范的 URL 格式：
  - 技能页面：`https://clawhub.ai/skills/<slug>`
  - 所有者页面：`https://clawhub.ai/<handle>/<slug>`
  - 用户个人资料（如果可用）：`https://clawhub.ai/users/<handle>`

## 资源

- `references/error-map.md`：用于快速诊断常见错误类型。
- `scripts/clawhub_preflight.sh`：用于检查依赖项和环境配置。
- `scripts/clawhub_publish_safe.sh`：用于执行发布操作并包含重试验证功能。