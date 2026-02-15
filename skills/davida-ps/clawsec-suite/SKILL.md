---
name: clawsec-suite
version: 0.0.10
description: ClawSec套件管理器具备嵌入式咨询信息监控功能、加密签名验证机制、基于审批流程的恶意技能响应机制，以及针对额外安全技能的引导式设置流程。
homepage: https://clawsec.prompt.security
clawdis:
  emoji: "📦"
  requires:
    bins: [curl, jq, shasum, openssl]
---

# ClawSec 套件

ClawSec 套件具备以下功能：
- 监控 ClawSec 的安全告警信息；
- 查看自上次检查以来新增的告警；
- 将告警信息与本地安装的技能进行关联；
- 对于涉及恶意技能的告警，系统会建议用户先进行确认后再进行移除操作；
- 同时，该套件还充当其他 ClawSec 安全功能的配置和管理入口。

## 包含的保护措施与可选的保护措施

### ClawSec 套件内置的保护措施：
- 嵌入式的告警信息源文件：`advisories/feed.json`
- 用于定期检查安全状态的脚本：`HEARTBEAT.md`
- 告警信息轮询、状态跟踪以及受影响技能的检测功能
- OpenClaw 告警监控模块：`hooks/clawsec-advisory-guardian/`
- 用于配置这些功能的脚本及可选的定时任务调度脚本：`scripts/`
- 受保护的技能安装脚本：`scripts/guarded_skill_install.mjs`

### 可单独安装的保护措施：
- `openclaw-audit-watchdog`
- `soul-guardian`
- `clawtributor`（需用户主动选择启用）

## 安装方法

### 方法一：通过 ClawHub 安装（推荐）

```bash
npx clawhub@latest install clawsec-suite
```

### 方法二：手动下载并验证签名及校验和

```bash
set -euo pipefail

VERSION="${SKILL_VERSION:?Set SKILL_VERSION (e.g. 0.0.8)}"
INSTALL_ROOT="${INSTALL_ROOT:-$HOME/.openclaw/skills}"
DEST="$INSTALL_ROOT/clawsec-suite"
BASE="https://github.com/prompt-security/clawsec/releases/download/clawsec-suite-v${VERSION}"

TEMP_DIR="$(mktemp -d)"
DOWNLOAD_DIR="$TEMP_DIR/downloads"
trap 'rm -rf "$TEMP_DIR"' EXIT
mkdir -p "$DOWNLOAD_DIR"

# Pinned release-signing public key (verify fingerprint out-of-band on first use)
# Fingerprint (SHA-256 of SPKI DER): 35866e1b1479a043ae816899562ac877e879320c3c5660be1e79f06241ca0854
RELEASE_PUBKEY_SHA256="35866e1b1479a043ae816899562ac877e879320c3c5660be1e79f06241ca0854"
cat > "$TEMP_DIR/release-signing-public.pem" <<'PEM'
-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEAtaRGONGp0Syl9EBS17hEYgGTwUtfZgigklS6vAe5MlQ=
-----END PUBLIC KEY-----
PEM

ACTUAL_KEY_SHA256="$(openssl pkey -pubin -in "$TEMP_DIR/release-signing-public.pem" -outform DER | shasum -a 256 | awk '{print $1}')"
if [ "$ACTUAL_KEY_SHA256" != "$RELEASE_PUBKEY_SHA256" ]; then
  echo "ERROR: Release public key fingerprint mismatch" >&2
  exit 1
fi

# 1) Download checksums manifest + detached signature
curl -fsSL "$BASE/checksums.json" -o "$TEMP_DIR/checksums.json"
curl -fsSL "$BASE/checksums.json.sig" -o "$TEMP_DIR/checksums.json.sig"

# 2) Verify checksums manifest signature before trusting any file URLs or hashes
openssl base64 -d -A -in "$TEMP_DIR/checksums.json.sig" -out "$TEMP_DIR/checksums.json.sig.bin"
if ! openssl pkeyutl -verify \
  -pubin \
  -inkey "$TEMP_DIR/release-signing-public.pem" \
  -sigfile "$TEMP_DIR/checksums.json.sig.bin" \
  -rawin \
  -in "$TEMP_DIR/checksums.json" >/dev/null 2>&1; then
  echo "ERROR: checksums.json signature verification failed" >&2
  exit 1
fi

if ! jq -e '.skill and .version and .files' "$TEMP_DIR/checksums.json" >/dev/null 2>&1; then
  echo "ERROR: Invalid checksums.json format" >&2
  exit 1
fi

echo "Checksums manifest signature verified."

# 3) Download every file listed in checksums and verify immediately
DOWNLOAD_FAILED=0
for file in $(jq -r '.files | keys[]' "$TEMP_DIR/checksums.json"); do
  FILE_URL="$(jq -r --arg f "$file" '.files[$f].url' "$TEMP_DIR/checksums.json")"
  EXPECTED="$(jq -r --arg f "$file" '.files[$f].sha256' "$TEMP_DIR/checksums.json")"

  if ! curl -fsSL "$FILE_URL" -o "$DOWNLOAD_DIR/$file"; then
    echo "ERROR: Download failed for $file" >&2
    DOWNLOAD_FAILED=1
    continue
  fi

  if command -v shasum >/dev/null 2>&1; then
    ACTUAL="$(shasum -a 256 "$DOWNLOAD_DIR/$file" | awk '{print $1}')"
  else
    ACTUAL="$(sha256sum "$DOWNLOAD_DIR/$file" | awk '{print $1}')"
  fi

  if [ "$EXPECTED" != "$ACTUAL" ]; then
    echo "ERROR: Checksum mismatch for $file" >&2
    DOWNLOAD_FAILED=1
  else
    echo "Verified: $file"
  fi
done

if [ "$DOWNLOAD_FAILED" -eq 1 ]; then
  echo "ERROR: One or more files failed verification" >&2
  exit 1
fi

# 4) Install files using paths from checksums.json
while IFS= read -r file; do
  [ -z "$file" ] && continue
  REL_PATH="$(jq -r --arg f "$file" '.files[$f].path // $f' "$TEMP_DIR/checksums.json")"
  SRC_PATH="$DOWNLOAD_DIR/$file"
  DST_PATH="$DEST/$REL_PATH"

  mkdir -p "$(dirname "$DST_PATH")"
  cp "$SRC_PATH" "$DST_PATH"
done < <(jq -r '.files | keys[]' "$TEMP_DIR/checksums.json")

chmod 600 "$DEST/skill.json"
find "$DEST" -type f ! -name "skill.json" -exec chmod 644 {} \;

echo "Installed clawsec-suite v${VERSION} to: $DEST"
echo "Next step (OpenClaw): node \"\$DEST/scripts/setup_advisory_hook.mjs\""
```

## OpenClaw 自动化配置（包含告警监控模块及可选的定时任务）

安装完该套件后，需要启用告警监控模块：

```bash
SUITE_DIR="${INSTALL_ROOT:-$HOME/.openclaw/skills}/clawsec-suite"
node "$SUITE_DIR/scripts/setup_advisory_hook.mjs"
```

**可选操作：** 设置定期定时任务（默认每 6 小时执行一次），以触发一次全面的安全检查：

```bash
SUITE_DIR="${INSTALL_ROOT:-$HOME/.openclaw/skills}/clawsec-suite"
node "$SUITE_DIR/scripts/setup_advisory_cron.mjs"
```

该定时任务会执行以下操作：
- 在 `agent:bootstrap` 和 `/new` 路径下进行扫描；
- 将告警信息中列出的受影响技能与已安装的技能进行比对；
- 当发现匹配项时，会通知用户；
- 在执行任何移除操作前，会要求用户进行明确确认。

启用告警监控模块后，需要重新启动 OpenClaw 服务器，并运行 `/new` 命令以强制在当前会话中立即执行一次安全检查。

## 受保护的技能安装流程（双重确认）

当用户请求安装某项技能时，系统会执行以下流程：
- 首先检查是否存在相关告警；
- 如果未找到匹配的告警，则继续安装流程；
- 如果用户未指定版本号（`--version` 参数），系统会采取保守的判断方式：任何提及该技能名称的告警都会被视为匹配项；
- 如果找到匹配的告警，系统会显示告警详情并退出（返回代码 42）；
- 此后系统会要求用户再次确认是否真的要安装该技能。

这一流程确保了：
1. 首次安装前需要用户的明确请求；
2. 安装前用户必须再次确认。

## 嵌入式告警信息源的配置方式

嵌入式告警信息源的默认配置如下：
- 远程告警信息源 URL：`https://raw.githubusercontent.com/prompt-security/clawsec/main/advisories/feed.json`
- 远程告警信息源的签名文件 URL：`${CLAWSEC_feed_URL}.sig`（可自定义为 `CLAWSEC_feed_SIG_URL`）
- 远程校验和文件 URL：`checksums.json`（可自定义为 `CLAWSEC_FEED_CHECKSUMS_URL`）
- 本地告警信息源的备用文件：`~/.openclaw/skills/clawsec-suite/advisories/feed.json`
- 本地告警信息源的签名文件：`${CLAWSEC_LOCAL_feed}.sig`（可自定义为 `CLAWSEC_LOCAL_feed_SIG`）
- 本地校验和文件：`~/.openclaw/skills/clawsec-suite/advisories/checksums.json`
- 用于签名验证的公钥文件：`~/.openclaw/skills/clawsec-suite/advisories/feed-signing-public.pem`（可自定义为 `CLAWSEC_feed_PUBLIC_KEY`）
- 用于存储状态的文件：`~/.openclaw/clawsec-suite-feed-state.json`
- 开发者用于配置定时任务的环境变量：`CLAWSEC_HOOK_INTERVAL_seconds`（默认值为 300 秒）

**注意事项：** 默认情况下，系统会同时验证签名和校验和文件。只有在采用此版本且上游尚未提供签名验证的告警信息源时，才能临时将 `CLAWSEC_ALLOWUnsigned_FEED` 设置为 `1`。

### 快速检查告警信息源的脚本

```bash
FEED_URL="${CLAWSEC_FEED_URL:-https://raw.githubusercontent.com/prompt-security/clawsec/main/advisories/feed.json}"
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

## 定期安全检查（使用 `HEARTBEAT.md` 脚本）

`HEARTBEAT.md` 脚本用于执行以下操作：
- 检查套件是否需要更新；
- 轮询告警信息源；
- 发现新的告警时进行响应；
- 将涉及恶意技能的告警与已安装的技能进行关联；
- 对于需要移除的技能，系统会提供确认提示；
- 更新系统的状态信息。

## 基于确认的用户操作流程

如果告警提示某项技能存在安全风险或需要被移除，系统会执行以下操作：
- 立即通知用户相关告警的详细信息及严重程度；
- 建议用户移除或禁用该技能；
- 将用户的初始安装请求视为初次请求；
- 在执行删除或禁用操作前，会要求用户再次确认；
- 只有在用户再次确认后，系统才会继续执行相关操作。

默认情况下，该套件的告警监控模块和定期检查功能不会对系统造成破坏性影响。

## 可选的额外安全保护措施

根据实际需求，可以安装额外的安全保护组件：

```bash
npx clawhub@latest install openclaw-audit-watchdog
npx clawhub@latest install soul-guardian
# opt-in only:
npx clawhub@latest install clawtributor
```

## 安全注意事项：
- 在信任任何文件之前，务必先验证 `checksums.json` 文件的签名及哈希值；
- 在临时迁移期间之外，切勿启用 `CLAWSEC_ALLOWUnsigned_FEED` 功能；
- 保持告警信息轮询的频率（至少每 5 分钟一次）；
- 对于影响已安装技能的“严重”或“高风险”告警，必须立即采取行动；
- 如果从独立的 `clawsec-feed` 迁移过来，请保留一个统一的状态文件以避免重复通知；
- 在首次使用之前，务必验证公钥的指纹信息。