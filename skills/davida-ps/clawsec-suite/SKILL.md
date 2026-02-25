---
name: clawsec-suite
version: 0.1.3
description: ClawSec套件管理器具备嵌入式建议信息监控功能、加密签名验证机制、基于审批流程的恶意技能响应机制，以及针对额外安全技能的引导式设置功能。
homepage: https://clawsec.prompt.security
clawdis:
  emoji: "📦"
  requires:
    bins: [curl, jq, shasum, openssl]
---
# ClawSec Suite

ClawSec Suite 具有以下功能：
- 监控 ClawSec 的安全建议信息；
- 查看自上次检查以来新增的安全建议；
- 将安全建议与本地安装的技能进行关联；
- 对于被标记为恶意技能的建议，系统会建议用户先进行确认后再进行删除操作；
- 同时，它还是其他 ClawSec 安全功能的配置和管理入口点。

## 内置与可选的安全功能

### ClawSec Suite 内置的功能
- 嵌入式的安全建议数据源文件：`advisories/feed.json`
- 用于心跳检测的脚本：`HEARTBEAT.md`
- 安全建议的轮询、状态跟踪以及受影响技能的检测
- OpenClaw 安全建议监控插件：`hooks/clawsec-advisory-guardian/`
- 用于配置插件的脚本以及可选的定时任务调度脚本：`scripts/`
- 受保护的技能安装脚本：`scripts/guarded_skill_install.mjs`
- 动态技能目录发现脚本：`scripts/discover_skill_catalog.mjs`

### 可单独安装的功能（动态技能目录）
本文档中并未硬编码 ClawSec Suite 所支持的附加技能名称。用户可以通过以下方式动态获取当前可用的技能目录：
在运行时从官方索引（`https://clawsec.prompt.security/skills/index.json`）获取技能目录：

```bash
SUITE_DIR="${INSTALL_ROOT:-$HOME/.openclaw/skills}/clawsec-suite"
node "$SUITE_DIR/scripts/discover_skill_catalog.mjs"
```

**备用方案：**
- 如果远程技能目录可用且格式正确，系统将使用该目录；
- 如果远程目录无法访问或格式错误，系统将使用本地的 `skill.json` 文件中的技能目录信息。

## 安装说明

### 跨 shell 路径设置
- 在 `bash`/`zsh` 环境中，确保路径变量是可扩展的（例如：`INSTALL_ROOT="$HOME/.openclaw/skills"`）；
- 不要对路径变量使用单引号（避免写成 `'$HOME/.openclaw/skills'`）；
- 在 PowerShell 中，设置路径如下：`$env:INSTALL_ROOT = Join-Path $HOME ".openclaw\\skills"`；
- 如果传递的路径包含未解析的占位符（如 `\$HOME/...`），系统会立即报错并终止执行。

### 安装方式
**推荐方式：通过 ClawHub 安装**

```bash
npx clawhub@latest install clawsec-suite
```

**手动下载方式（需验证签名和校验哈希值）**

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

## OpenClaw 自动化配置（插件 + 定时任务）
安装完成后，需要启用安全建议监控插件：

```bash
SUITE_DIR="${INSTALL_ROOT:-$HOME/.openclaw/skills}/clawsec-suite"
node "$SUITE_DIR/scripts/setup_advisory_hook.mjs"
```

**可选操作：** 创建或更新定时任务（默认每 6 小时执行一次），以触发一次全面的安全建议扫描：
```bash
SUITE_DIR="${INSTALL_ROOT:-$HOME/.openclaw/skills}/clawsec-suite"
node "$SUITE_DIR/scripts/setup_advisory_cron.mjs"
```

该定时任务会执行以下操作：
- 在 `agent:bootstrap` 和 `/new` 路径下扫描安全建议；
- 将安全建议中列出的受影响技能与已安装的技能进行比对；
- 对于标记为 “openclaw” 的安全建议（以及旧版本中未指定 `application` 字段的建议），也会进行比对；
- 当发现匹配项时，系统会提示用户进行确认；
- 在执行任何删除操作之前，系统会要求用户再次确认。

启用插件后，请重新启动 OpenClaw 服务，并运行 `/new` 命令以在下一个会话中立即执行扫描。

## 受保护的技能安装流程（双重确认）
当用户请求安装某项技能时，系统会执行以下流程：
```bash
SUITE_DIR="${INSTALL_ROOT:-$HOME/.openclaw/skills}/clawsec-suite"
node "$SUITE_DIR/scripts/guarded_skill_install.mjs" --skill helper-plus --version 1.0.1
```

**操作流程：**
- 如果未找到匹配的安全建议，安装过程将继续；
- 如果未指定 `--version` 参数，系统会采取保守的匹配策略：任何提及该技能名称的安全建议都会被视为匹配项；
- 如果找到匹配的安全建议，系统会显示相关详情并返回错误代码 `42`；
- 系统会要求用户再次确认是否真的要安装该技能。

**注意事项：**
- 首次确认：用户需要明确表示同意安装；
- 第二次确认：用户在查看安全建议详情后必须再次确认。

## 嵌入式安全建议数据源的配置
嵌入式数据源的配置参数如下：
- 远程数据源 URL：`https://clawsec.prompt.security/advisories/feed.json`
- 远程数据源签名文件 URL：`${CLAWSEC_FEED_URL}.sig`（可自定义为 `CLAWSEC_FEED_SIG_URL`）
- 远程校验和文件 URL：`checksums.json`（可自定义为 `CLAWSEC_FEED_CHECKSUMS_URL`）
- 本地数据源文件：`~/.openclaw/skills/clawsec-suite/advisories/feed.json`
- 本地数据源签名文件：`${CLAWSEC_LOCAL_feed}.sig`（可自定义为 `CLAWSEC_LOCAL_FEED_SIG`
- 本地校验和文件：`~/.openclaw/skills/clawsec-suite/advisories/checksums.json`
- 用于数据源签名的密钥文件：`~/.openclaw/skills/clawsec-suite/advisories/feed-signing-public.pem`（可自定义为 `CLAWSEC_FEED_PUBLIC_KEY`
- 状态文件：`~/.openclaw/clawsec-suite-feed-state.json`
- 插件使用的频率限制参数：`CLAWSECHOOK_INTERVAL_seconds`（默认值为 300 秒）

**注意事项：**
- 系统默认要求验证数据源的签名；只有在上游提供签名文件之前，才能临时将 `CLAWSEC_ALLOWUnsigned_feed` 设置为 `1`。

### 快速数据源检查
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
  done < "$NEW_IDS_FILE"
else
  echo "FEED_OK - no new advisories"
fi
```

## 心跳检测功能
使用 `HEARTBEAT.md` 脚本作为定期的安全检查入口：
该脚本负责：
- 检查系统是否需要更新；
- 轮询安全建议数据源；
- 检测新的安全建议；
- 将受影响的技能与已安装的技能进行关联；
- 对于被标记为恶意或需要删除的技能，提供相应的操作指导；
- 更新系统的状态信息。

## 基于确认的操作机制
如果安全建议提示某项技能具有恶意性或建议将其删除，系统会执行以下操作：
1. 立即通知用户相关详情和严重程度；
2. 建议用户删除或禁用该技能；
- 将用户的初始安装请求视为初次请求；
- 在执行删除或禁用操作之前，系统会要求用户再次确认；
- 只有在用户再次确认后，系统才会继续执行操作。

### 安全建议的抑制/允许列表
系统支持对已经过安全团队审核的安全建议进行抑制。这对于第三方工具或不适用当前环境的建议非常有用。

### 激活抑制功能
要启用抑制功能，只需在配置文件中添加 `enabledFor` 数组，并在其中包含 `"advisory"`。无需使用任何命令行参数——配置文件中的设置即可实现抑制功能。

如果 `enabledFor` 数组缺失、为空或不包含 `"advisory"`，系统会正常报告所有安全建议。

### 配置文件的优先级
系统按照以下优先级顺序解析抑制配置：
1. 显式的 `--config <path>` 参数；
2. 环境变量 `OPENCLAW_AUDIT_CONFIG`；
3. 文件 `~/.openclaw/security-audit.json`；
4. 文件 `.clawsec/allowlist.json`。

### 配置文件格式
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
- `"enabledFor": ["advisory"]`：仅抑制安全建议；
- `"enabledFor": ["audit"]`：仅抑制审计相关的建议；
- `"enabledFor": ["audit", "advisory"]`：同时抑制安全建议和审计相关的建议；
- 如果 `enabledFor` 为空或缺失，系统不会执行任何抑制操作（这是安全默认设置）。

### 匹配规则
- **checkId**：与安全建议的 ID 完全匹配（例如：`CVE-2026-25593` 或 `CLAW-2026-0001`）；
- **skill**：与安全建议中列出的技能名称不区分大小写地进行匹配；
- 两个字段都必须匹配，建议才能被抑制。

### 抑制配置所需的字段
| 字段 | 说明 | 示例 |
|-------|-------------|---------|
| `checkId` | 需要抑制的安全建议的 ID | `CVE-2026-25593` |
| `skill` | 受影响的技能名称 | `clawsec-suite` |
| `reason` | 审计跟踪的说明（必填） | “第三方工具，已由安全团队审核” |
| `suppressedAt` | ISO 8601 格式的日期（YYYY-MM-DD） | `2026-02-15` |

### 共享配置文件
安全建议和审计相关的配置文件是共享的。使用 `enabledFor` 数组来控制哪些流程会应用抑制规则：
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

- 具有审计标识符（如 `skills.code_safety`）的条目仅由审计流程处理；
- 具有安全建议 ID（如 `CVE-2026-25593` 或 `CLAW-2026-0001`）的条目仅由安全建议流程处理；
每个流程会分别过滤自己相关的条目。

### 动态发现并安装可用技能
系统会动态发现当前可安装的技能，并允许用户选择安装所需的技能：
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

**安全注意事项：**
- 在信任任何文件或哈希值之前，务必验证 `checksums.json` 文件的签名；
- 在临时迁移期间之外，不要启用 `CLAWSEC_ALLOWUnsigned_feed`；
- 保持安全建议的轮询频率受到限制（至少每 5 分钟检查一次）；
- 对于影响已安装技能的 `critical` 和 `high` 级别安全建议，必须立即采取行动；
- 如果从独立的 `clawsec-feed` 迁移过来，请保留一个统一的状态文件以避免重复通知；
- 在首次使用之前，务必验证公钥的指纹信息。