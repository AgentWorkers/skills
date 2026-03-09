---
name: clawsec-suite
version: 0.1.4
description: ClawSec套件管理器具备内置的咨询信息监控功能、加密签名验证机制、基于审批流程的恶意技能响应机制，以及为增强安全性而设计的引导式设置流程。
homepage: https://clawsec.prompt.security
clawdis:
  emoji: "📦"
  requires:
    bins: [curl, jq, shasum, openssl]
---
# ClawSec Suite

`clawsec-suite` 具有以下功能：
- 监控 ClawSec 建议信息流；
- 跟踪自上次检查以来新增的建议；
- 将建议与本地安装的技能进行关联；
- 对于涉及恶意技能的建议，系统会先推荐移除操作，并要求用户明确批准；
- 同时，它还是其他 ClawSec 安全功能的设置/管理入口点。

## 内置与可选的安全功能

### 内置在 `clawsec-suite` 中的功能
- 嵌入式的建议信息源文件：`advisories/feed.json`
- 便携式的心跳检测脚本：`HEARTBEAT.md`
- 建议信息轮询、状态跟踪以及受影响技能的检测
- OpenClaw 建议信息监控插件包：`hooks/clawsec-advisory-guardian/`
- 用于插件配置和可选的 Cron 定时任务的脚本：`scripts/`
- 受保护的安装脚本：`scripts/guarded_skill_install.mjs`
- 动态技能目录发现脚本：`scripts/discover_skill_catalog.mjs`

### 可单独安装的功能（动态技能目录）
`clawsec-suite` 在文档中不会硬编码附加技能的名称。运行时，系统会从权威索引（`https://clawsec.prompt.security/skills/index.json`）获取当前技能目录：

```bash
SUITE_DIR="${INSTALL_ROOT:-$HOME/.openclaw/skills}/clawsec-suite"
node "$SUITE_DIR/scripts/discover_skill_catalog.mjs"
```

**回退机制：**
- 如果远程目录索引可用且有效，系统将使用该索引；
- 如果远程索引不可用或格式错误，系统会使用 `skill.json` 中的本地目录元数据。

## 安装说明

### 跨 shell 路径注意事项
- 在 `bash`/`zsh` 中，路径变量应保持可扩展性（例如：`INSTALL_ROOT="$HOME/.openclaw/skills"`）；
- 不要对包含路径变量的字符串使用单引号（避免写成 `'$HOME/.openclaw/skills'`）；
- 在 PowerShell 中，设置路径如下：`$env:INSTALL_ROOT = Join-Path $HOME ".openclaw\\skills"`；
- 如果传递的路径包含未解析的占位符（如 `\$HOME/...`），系统会立即报错并终止执行。

### 选项 A：通过 ClawHub 安装（推荐）

```bash
npx clawhub@latest install clawsec-suite
```

### 选项 B：手动下载并验证签名及校验和

```bash
set -euo pipefail

VERSION="${SKILL_VERSION:?Set SKILL_VERSION (e.g. 0.0.8)}"
INSTALL_ROOT="${INSTALL_ROOT:-$HOME/.openclaw/skills}"
DEST="$INSTALL_ROOT/clawsec-suite"
BASE="https://github.com/prompt-security/clawsec/releases/download/clawsec-suite-v${VERSION}"

TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT

# Pinned release-signing public key (verify fingerprint out-of-band on first use)
# Fingerprint (SHA-256 of SPKI DER): 711424e4535f84093fefb024cd1ca4ec87439e53907b305b79a631d5befba9c8
RELEASE_PUBKEY_SHA256="711424e4535f84093fefb024cd1ca4ec87439e53907b305b79a631d5befba9c8"
cat > "$TEMP_DIR/release-signing-public.pem" <<'PEM'
-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEAS7nijfMcUoOBCj4yOXJX+GYGv2pFl2Yaha1P4v5Cm6A=
-----END PUBLIC KEY-----
PEM

ACTUAL_KEY_SHA256="$(openssl pkey -pubin -in "$TEMP_DIR/release-signing-public.pem" -outform DER | shasum -a 256 | awk '{print $1}')"
if [ "$ACTUAL_KEY_SHA256" != "$RELEASE_PUBKEY_SHA256" ]; then
  echo "ERROR: Release public key fingerprint mismatch" >&2
  exit 1
fi

ZIP_NAME="clawsec-suite-v${VERSION}.zip"

# 1) Download release archive + signed checksums manifest + signing public key
curl -fsSL "$BASE/$ZIP_NAME" -o "$TEMP_DIR/$ZIP_NAME"
curl -fsSL "$BASE/checksums.json" -o "$TEMP_DIR/checksums.json"
curl -fsSL "$BASE/checksums.sig" -o "$TEMP_DIR/checksums.sig"

# 2) Verify checksums manifest signature before trusting any hashes
openssl base64 -d -A -in "$TEMP_DIR/checksums.sig" -out "$TEMP_DIR/checksums.sig.bin"
if ! openssl pkeyutl -verify \
  -pubin \
  -inkey "$TEMP_DIR/release-signing-public.pem" \
  -sigfile "$TEMP_DIR/checksums.sig.bin" \
  -rawin \
  -in "$TEMP_DIR/checksums.json" >/dev/null 2>&1; then
  echo "ERROR: checksums.json signature verification failed" >&2
  exit 1
fi

EXPECTED_ZIP_SHA="$(jq -r '.archive.sha256 // empty' "$TEMP_DIR/checksums.json")"
if [ -z "$EXPECTED_ZIP_SHA" ]; then
  echo "ERROR: checksums.json missing archive.sha256" >&2
  exit 1
fi

if command -v shasum >/dev/null 2>&1; then
  ACTUAL_ZIP_SHA="$(shasum -a 256 "$TEMP_DIR/$ZIP_NAME" | awk '{print $1}')"
else
  ACTUAL_ZIP_SHA="$(sha256sum "$TEMP_DIR/$ZIP_NAME" | awk '{print $1}')"
fi

if [ "$EXPECTED_ZIP_SHA" != "$ACTUAL_ZIP_SHA" ]; then
  echo "ERROR: Archive checksum mismatch for $ZIP_NAME" >&2
  exit 1
fi

echo "Checksums manifest signature and archive hash verified."

# 3) Install verified archive
mkdir -p "$INSTALL_ROOT"
rm -rf "$DEST"
unzip -q "$TEMP_DIR/$ZIP_NAME" -d "$INSTALL_ROOT"

chmod 600 "$DEST/skill.json"
find "$DEST" -type f ! -name "skill.json" -exec chmod 644 {} \;

echo "Installed clawsec-suite v${VERSION} to: $DEST"
echo "Next step (OpenClaw): node \"\$DEST/scripts/setup_advisory_hook.mjs\""
```

## OpenClaw 自动化配置（插件 + 可选的 Cron 定时任务）
安装完成后，需要启用建议信息监控插件：

```bash
SUITE_DIR="${INSTALL_ROOT:-$HOME/.openclaw/skills}/clawsec-suite"
node "$SUITE_DIR/scripts/setup_advisory_hook.mjs"
```

**可选操作：** 创建/更新定期执行的 Cron 定时任务（默认每 6 小时执行一次），以触发一次主要会话的建议信息扫描：

```bash
SUITE_DIR="${INSTALL_ROOT:-$HOME/.openclaw/skills}/clawsec-suite"
node "$SUITE_DIR/scripts/setup_advisory_cron.mjs"
```

该任务会：
- 在 `agent:bootstrap` 和 `/new` 路径下执行扫描；
- 将建议信息中的 `affected` 字段与已安装的技能进行比对；
- 优先处理标记为 `application: "openclaw"` 的建议（同时兼容旧版本的未标记 `application` 的建议）；
- 当发现匹配项时，系统会通知用户；
- 在任何移除操作前，系统会要求用户明确批准。

启用插件后，请重启 OpenClaw 代理，并运行 `/new` 命令以强制在下一个会话中立即执行扫描。

## 受保护的技能安装流程（双重确认）
当用户请求安装技能时，系统会执行以下流程：
```bash
SUITE_DIR="${INSTALL_ROOT:-$HOME/.openclaw/skills}/clawsec-suite"
node "$SUITE_DIR/scripts/guarded_skill_install.mjs" --skill helper-plus --version 1.0.1
```

**操作流程：**
- 如果未找到匹配的建议，安装过程将继续；
- 如果未指定 `--version` 参数，系统会采用保守的匹配规则：任何提及该技能名称的建议都会被视为匹配项；
- 如果找到匹配的建议，系统会显示建议的详细信息并返回错误代码 `42`；
- 系统会要求用户再次确认安装操作。

**注意事项：**
- 第一次确认：用户请求安装；
- 第二次确认：用户在查看建议详细信息后明确批准安装。

## 嵌入式建议信息源的配置
嵌入式建议信息源的默认配置如下：
- 远程建议信息源 URL：`https://clawsec.prompt.security/advisories/feed.json`
- 远程建议信息源签名 URL：`${CLAWSEC_feed_URL}.sig`（可自定义为 `CLAWSEC_feed_SIG_URL`）
- 远程校验和文件 URL：`checksums.json`（可自定义为 `CLAWSEC_feed_CHECKSUMS_URL`）
- 本地建议信息源文件：`~/.openclaw/skills/clawsec-suite/advisories/feed.json`
- 本地建议信息源签名：`${CLAWSEC_LOCAL_feed}.sig`（可自定义为 `CLAWSEC_LOCAL_feed_SIG`
- 本地校验和文件：`~/.openclaw/skills/clawsec-suite/advisories/checksums.json`
- 用于签名验证的公钥文件：`~/.openclaw/skills/clawsec-suite/advisories/feed-signing-public.pem`（可自定义为 `CLAWSEC_FEED_PUBLIC_KEY`
- 状态文件：`~/.openclaw/clawsec-suite-feed-state.json`
- 插件运行的频率配置环境变量：`CLAWSECHOOK_INTERVAL_seconds`（默认值为 300 秒）

**注意事项：**
- 系统默认要求对建议信息源的签名进行验证；只有在上游提供签名验证文件之前，才能临时将 `CLAWSEC_ALLOW_UNSIGNED_FEED` 设置为 `1`。

### 快速建议信息源检查

```bash
FEED_URL="${CLAWSEC_FEED_URL:-https://clawsec.prompt.security/advisories/feed.json}"
STATE_FILE="${CLAWSEC_SUITE_STATE_FILE:-$HOME/.openclaw/clawsec-suite-feed-state.json}"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

if ! curl -fsSLo "$TMP/feed.json" "$FEED_URL"; then
  echo "ERROR: Failed to fetch advisory feed"
  exit 1
fi

if ! jq -e '.version and (.advisories | type == "array")' "$TMP/feed.json" >/dev/null; then
  echo "ERROR: Invalid advisory feed format"
  exit 1
fi

mkdir -p "$(dirname "$STATE_FILE")"
if [ ! -f "$STATE_FILE" ]; then
  echo '{"schema_version":"1.0","known_advisories":[],"last_feed_check":null,"last_feed_updated":null}' > "$STATE_FILE"
  chmod 600 "$STATE_FILE"
fi

NEW_IDS_FILE="$TMP/new_ids.txt"
jq -r --argfile state "$STATE_FILE" '($state.known_advisories // []) as $known | [.advisories[]?.id | select(. != null and ($known | index(.) | not))] | .[]?' "$TMP/feed.json" > "$NEW_IDS_FILE"

if [ -s "$NEW_IDS_FILE" ]; then
  echo "New advisories detected:"
  while IFS= read -r id; do
    [ -z "$id" ] && continue
    jq -r --arg id "$id" '.advisories[] | select(.id == $id) | "- [\(.severity | ascii_upcase)] \(.id): \(.title)"' "$TMP/feed.json"
    jq -r --arg id "$id" '.advisories[] | select(.id == $id) | "  Exploitability: \(.exploitability_score // "unknown" | ascii_upcase)"' "$TMP/feed.json"
  done < "$NEW_IDS_FILE"
else
  echo "FEED_OK - no new advisories"
fi
```

## 漏洞利用性评估
建议信息中包含 `exploitability_score` 和 `exploitability_rationale` 字段，帮助代理优先处理实际威胁：
- **漏洞利用性评分**：`high`、`medium`、`low` 或 `unknown`
- **基于上下文的评估**：考虑攻击途径、认证要求以及 AI 代理的部署模式
- **漏洞利用情况**：检测公开漏洞及其被利用的状态

在处理建议信息时，系统会根据漏洞利用性进行优先级排序。例如，严重性为 `CRITICAL` 且漏洞利用性为 `HIGH` 的漏洞比严重性为 `CRITICAL` 但漏洞利用性为 `LOW` 的漏洞更为紧急。

有关详细方法，请参阅 [漏洞利用性评分文档](../../wiki/exploitability-scoring.md)。

## 心跳检测集成
使用 `HEARTBEAT.md` 脚本作为定期的安全检查入口点：
该脚本负责：
- 检查 `clawsec-suite` 的更新情况；
- 轮询建议信息源；
- 检测新发布的建议；
- 将受影响的技能与已安装的技能进行关联；
- 对于涉及恶意技能的建议，提供审批后的处理指导；
- 更新系统状态。

## 基于审批的处理流程
如果建议信息指出某个技能具有恶意性或建议将其移除，并且该技能已被安装：
1. 立即向用户发送包含建议详细信息的通知；
2. 建议移除或禁用该技能；
- 将原始的安装请求视为用户的初始意图；
- 在执行删除或禁用操作之前，要求用户再次确认；
- 只有在获得第二次确认后，系统才会继续执行操作。

系统默认情况下，插件和心跳检测功能不会对系统造成破坏性影响。

## 建议信息抑制/允许列表
建议信息监控插件支持对已由安全团队审核并通过的建议信息进行抑制。这对于第三方工具或不适用当前环境的建议信息非常有用。

### 激活抑制功能
启用抑制功能需要配置文件中的 `enabledFor` 数组包含 `"advisory"`。无需使用 CLI 参数——配置文件中的设置即为抑制功能的开关。

如果 `enabledFor` 数组缺失、为空或不包含 `"advisory`，系统会正常报告所有建议信息。

### 配置文件解析规则（共 4 个层级）
建议信息监控插件根据以下优先级顺序解析抑制配置：
1. 显式的 `--config <path>` 参数；
2. 环境变量 `OPENCLAW_AUDIT_CONFIG`；
3. 文件 `~/.openclaw/security-audit.json`；
4. 文件 `.clawsec/allowlist.json`。

### 配置文件的语法说明
```json
{
  "enabledFor": ["advisory"],
  "suppressions": [
    {
      "checkId": "CVE-2026-25593",
      "skill": "clawsec-suite",
      "reason": "First-party security tooling — reviewed by security team",
      "suppressedAt": "2026-02-15"
    },
    {
      "checkId": "CLAW-2026-0001",
      "skill": "example-skill",
      "reason": "Advisory does not apply to our deployment configuration",
      "suppressedAt": "2026-02-16"
    }
  ]
}
```

### 配置参数的含义
- `"enabledFor": ["advisory"]`：仅抑制建议信息；
- `"enabledFor": ["audit"]`：仅抑制审计相关的建议信息（不影响建议信息处理流程）；
- `"enabledFor": ["audit", "advisory"]`：同时抑制建议信息和审计相关的建议信息；
- 如果 `enabledFor` 不存在或为空，则不执行任何抑制操作（安全默认设置）。

### 匹配规则
- **checkId**：与建议信息的 ID 完全匹配（例如：`CVE-2026-25593` 或 `CLAW-2026-0001`）；
- **skill**：与建议信息中提到的技能名称不区分大小写地匹配；
- 两个字段都必须匹配，建议信息才能被抑制。

### 抑制配置所需的字段
| 字段 | 说明 | 示例 |
|-------|-------------|---------|
| `checkId` | 需要抑制的建议信息 ID | `CVE-2026-25593` |
| `skill` | 受影响的技能名称 | `clawsec-suite` |
| `reason` | 审计跟踪的说明（必填） | “第三方工具，已由安全团队审核” |
| `suppressedAt` | ISO 8601 格式的日期（YYYY-MM-DD） | `2026-02-15` |

### 共享配置文件
建议信息处理流程和审计处理流程使用相同的配置文件。通过 `enabledFor` 数组来控制哪些流程会执行抑制操作：
```json
{
  "enabledFor": ["audit", "advisory"],
  "suppressions": [
    {
      "checkId": "skills.code_safety",
      "skill": "clawsec-suite",
      "reason": "First-party tooling — audit finding accepted",
      "suppressedAt": "2026-02-15"
    },
    {
      "checkId": "CVE-2026-25593",
      "skill": "clawsec-suite",
      "reason": "First-party tooling — advisory reviewed",
      "suppressedAt": "2026-02-15"
    }
  ]
}
```

- 审计相关的条目（例如：`skills.code_safety`）仅由审计处理流程处理；
- 建议信息相关的条目（例如：`CVE-2026-25593` 或 `CLAW-2026-0001`）仅由建议信息处理流程处理。每个流程会过滤自己相关的条目。

### 动态安装可用技能
系统会动态检测当前可安装的技能，并允许用户安装所需的技能：

```bash
SUITE_DIR="${INSTALL_ROOT:-$HOME/.openclaw/skills}/clawsec-suite"
node "$SUITE_DIR/scripts/discover_skill_catalog.mjs"

# then install any discovered skill by name
npx clawhub@latest install <skill-name>
```

系统还提供了机器可读的输出格式，便于自动化操作：

```bash
node "$SUITE_DIR/scripts/discover_skill_catalog.mjs" --json
```

## 安全注意事项：
- 在信任文件 URL 或哈希值之前，务必验证 `checksums.json` 的签名；
- 在临时迁移期间之外，不要启用 `CLAWSEC_ALLOW_UNSIGNED_feed`；
- 保持建议信息轮询的频率限制（至少每 5 分钟检查一次）；
- 对于影响已安装技能的 `critical` 或 `high` 级别建议，应立即采取行动；
- 如果从独立的 `clawsec-feed` 迁移过来，请保留一个标准的状态文件以避免重复通知；
- 在首次使用之前，务必验证公钥的指纹信息。