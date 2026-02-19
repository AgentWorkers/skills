---
name: home-assistant-control
description: 通过 REST API 控制和检查 Home Assistant 中的实体（Entities）、状态（States）、服务（Services）、场景（Scenes）、脚本（Scripts）以及自动化任务（Automations）。当用户需要开关设备、设置亮度或温度等参数、触发特定场景/脚本/自动化任务，或查看当前的家庭环境/传感器状态时，可以使用该功能。
homepage: https://github.com/Hogar23/home-assistant-control
metadata:
  {
    "openclaw": {
      "emoji": "🏠",
      "requires": {
        "bins": ["bash", "curl", "jq"],
        "env": ["HA_TOKEN", "HA_URL_PUBLIC"]
      }
    }
  }
---
# Home Assistant 控制

使用 Home Assistant REST API 和长期有效的访问令牌（long-lived access token）进行操作。

## 所需条件

### 对于技能用户（运行时）

- `bash`
- `curl`
- `jq`
- Home Assistant 的长期有效令牌（`HA_TOKEN`）
- Home Assistant 的公共基础 URL（`HA_URL_PUBLIC`）

### 对于技能维护者（打包/验证）

- `python3`
- `pyyaml`（`skill-creator` 验证器/打包脚本所需）

## 必需的环境变量

- `HA_TOKEN`（必需）
- `HA_URL_PUBLIC`（必需；默认目标 URL）
- 可选的 URL 行为：
  - 如果设置了 `HA_URL_LOCAL`（且没有覆盖 `HA_URL`），则先尝试使用本地 URL，然后回退到 `HA_URL_PUBLIC`
  - 如果设置了 `HA_URL`，则直接使用该 URL

## 保密信息处理（安全发布）

- 将密钥/URL 存储在外部文件中，不要放在技能文件夹内。
- 当需要从文件加载保密信息时，设置 `HA_ENV_FILE=/absolute/path/to/file.env`。
- 如果未设置 `HA_ENV_FILE`，脚本将仅使用 shell 中已存在的环境变量。
- `scripts/ha_call.sh` 和 `scripts/self_check.sh` 仅在提供了 `HA_ENV_FILE` 时才会加载环境文件。

## 核心工作流程

1. 将用户请求解析为目标实体/服务及所需操作。
2. 首先查看 `references/naming-context.md` 以获取手动别名映射。
3. 在更改状态之前验证实体是否存在。
4. 执行服务调用。
5. 重新检查状态并清晰地报告结果。

## 有用的端点

- 列出状态：`GET /api/states`
- 单个状态：`GET /api/states/{entity_id}`
- 调用服务：`POST /api/services/{domain}/{service}`

请求头：

- `Authorization: Bearer $HA_TOKEN`
- `Content-Type: application/json`

## 脚本

- `scripts/ha_env.sh` — 仅在明确设置了 `HA_ENV_FILE` 时加载环境文件，使用安全的 KEY=VALUE 解析方式（不使用 `source`/`eval`）。
- `scripts/ha_call.sh` — 用于调用 Home Assistant API 的通用脚本。
- `scripts/fill_entities_md.sh` — 从 `GET /api/states` 生成 `references/entities.md`：
  - 生成完整实体列表：`./scripts/fill_entities_md.sh`
  - 过滤特定领域：`./scripts/fill_entities_md.sh --domains light,switch,climate,sensor`
- `scripts/save_naming_context.sh` — 更新 `references/naming-context.md` 以适应用户自定义的命名规则。
- `scripts/ha_entity_find.sh` — 根据部分实体 ID 或友好名称搜索实体：
  - `./scripts/ha_entity_find.sh kitchen`
  - `./scripts/ha_entity_find.sh temp --domains sensor,climate --limit 30`
- `scripts/ha_safe_action.sh` — 执行服务操作，并进行安全检查及风险确认：
  - `./scripts/ha_safe_action.sh light turn_on light.kitchen '{"brightness_pct":60}'`
  - `./scripts/ha_safe_action.sh lock unlock lock.front_door --dry-run`
  - 通过添加 `--yes` 参数可以跳过高风险操作的交互式确认。
- `scripts/self_check.sh` — 在执行操作前验证前提条件及 API 连接/身份验证。
- `./scripts/self_check.sh`

## 安全性

- 在执行高影响操作（如锁定、报警、车库门控制、关闭暖气）前进行确认。
- 不要打印原始令牌值。
- 如果目标实体不明确，应询问用户进一步的信息。
- 确保 API 路径仅限于 Home Assistant 的端点（`/api/...`）。
- 仅使用 HTTP(S) 协议访问 Home Assistant（优先使用 HTTPS）。
- 在加载环境文件时避免执行代码：仅解析键值对，不要在不可信的路径上使用 `source` 功能。

## 参考文件

- `references/entities.md` — 实体清单
- `references/naming-context.md` — 用于存储实体友好名称的映射信息（例如：“living room light”）

## 发布说明

- 保持示例的通用性（使用 `example_*` 作为文件名），避免使用真实的主机名/令牌。
- 不要将包含真实令牌的 `.env` 文件提交到代码仓库。
- 保持技能的核心功能：API 工作流程、可重用的脚本以及实体参考信息。