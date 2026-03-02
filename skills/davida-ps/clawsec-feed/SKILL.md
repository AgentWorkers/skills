---
name: clawsec-feed
version: 0.0.5
description: 安全公告订阅服务，自动查询 NVD（National Vulnerability Database）中与 OpenClaw 相关的漏洞信息。每日更新。
homepage: https://clawsec.prompt.security
metadata: {"openclaw":{"emoji":"📡","category":"security"}}
clawdis:
  emoji: "📡"
  requires:
    bins: [curl, jq]
---
# ClawSec Feed 📡

这是一个用于监控AI代理安全建议的信息源。订阅社区提供的威胁情报，以便及时了解新出现的威胁。

该信息源会每天自动更新，内容包含来自NIST国家漏洞数据库（NVD）的与OpenClaw、clawdbot和Moltbot相关的CVE（漏洞信息）。

**该项目由[Prompt Security](https://prompt.security)开发，属于开源项目。**

---

## 安装选项

您可以通过两种方式获取clawsec-feed：

### 选项A：随ClawSec Suite一起安装（推荐）

**如果您已经安装了clawsec-suite，那么您可能已经拥有了这个组件！**

ClawSec-feed与ClawSec Suite捆绑在一起，提供关键的CVE和威胁情报信息。在安装该套件时，如果尚未安装此组件，系统会从捆绑包中自动安装它。

**优点：**
- 方便：无需单独下载
- 安装位置固定：安装在`~/.openclaw/skills/clawsec-feed/`
- 保持原有状态：如果已安装过该组件，不会被覆盖
- 一次性验证：完整性检查作为套件安装的一部分完成

### 选项B：独立安装（此页面）

您可以独立安装clawsec-feed，而不需要安装整个套件。

**何时选择独立安装：**
- 只需要安全建议信息，而不需要套件的其他组件
- 希望在安装套件之前先安装此组件
- 希望对安装过程有更详细的控制

**优点：**
- 安装过程更简洁
- 与套件分离
- 可以完全控制安装过程

请继续阅读以下独立安装的说明。

---

**安装步骤：**
在代理执行任何操作之前，请先查看相关脚本！

```bash
# Get latest clawsec-feed release tag
LATEST_TAG=$(curl -sSL https://api.github.com/repos/prompt-security/ClawSec/releases | \
  jq -r '[.[] | select(.tag_name | startswith("clawsec-feed-v"))][0].tag_name')

# Download SKILL.md from latest release
SKILL_URL="https://github.com/prompt-security/clawsec/releases/download/$LATEST_TAG/SKILL.md"
curl -sSL --fail --show-error "$SKILL_URL"
```

获取此技能文件后，请按照**[部署ClawSec Feed](#deploy-clawsec-feed)**的步骤进行操作。

---

## 部署ClawSec Feed

**安装步骤：**

### 第1步：创建技能目录并保存此文件

```bash
mkdir -p ~/.openclaw/skills/clawsec-feed
# Save this SKILL.md as SKILL.md in the directory above
```

### 第2步：安装技能文件

```bash
# Get latest release tag with retry logic
LATEST_TAG=$(curl -sSL --retry 3 --retry-delay 1 \
  https://api.github.com/repos/prompt-security/ClawSec/releases | \
  jq -r '[.[] | select(.tag_name | startswith("clawsec-feed-v"))][0].tag_name')

BASE_URL="https://github.com/prompt-security/clawsec/releases/download/$LATEST_TAG"
INSTALL_DIR="${CLAWSEC_INSTALL_DIR:-$HOME/.openclaw/skills/clawsec-feed}"
TEMP_DIR=$(mktemp -d)
trap "rm -rf '$TEMP_DIR'" EXIT

# Download checksums.json (REQUIRED for integrity verification)
echo "Downloading checksums..."
if ! curl -sSL --fail --show-error --retry 3 --retry-delay 1 \
     "$BASE_URL/checksums.json" -o "$TEMP_DIR/checksums.json"; then
  echo "ERROR: Failed to download checksums.json"
  exit 1
fi

# Validate checksums.json structure
if ! jq -e '.skill and .version and .files' "$TEMP_DIR/checksums.json" >/dev/null 2>&1; then
  echo "ERROR: Invalid checksums.json structure"
  exit 1
fi

# PRIMARY: Try .skill artifact
echo "Attempting .skill artifact installation..."
if curl -sSL --fail --show-error --retry 3 --retry-delay 1 \
   "$BASE_URL/clawsec-feed.skill" -o "$TEMP_DIR/clawsec-feed.skill" 2>/dev/null; then

  # Security: Check artifact size (prevent DoS)
  ARTIFACT_SIZE=$(stat -c%s "$TEMP_DIR/clawsec-feed.skill" 2>/dev/null || stat -f%z "$TEMP_DIR/clawsec-feed.skill")
  MAX_SIZE=$((50 * 1024 * 1024))  # 50MB

  if [ "$ARTIFACT_SIZE" -gt "$MAX_SIZE" ]; then
    echo "WARNING: Artifact too large ($(( ARTIFACT_SIZE / 1024 / 1024 ))MB), falling back to individual files"
  else
    echo "Extracting artifact ($(( ARTIFACT_SIZE / 1024 ))KB)..."

    # Security: Check for path traversal before extraction
    if unzip -l "$TEMP_DIR/clawsec-feed.skill" | grep -qE '\.\./|^/|~/'; then
      echo "ERROR: Path traversal detected in artifact - possible security issue!"
      exit 1
    fi

    # Security: Check file count (prevent zip bomb)
    FILE_COUNT=$(unzip -l "$TEMP_DIR/clawsec-feed.skill" | grep -c "^[[:space:]]*[0-9]" || echo 0)
    if [ "$FILE_COUNT" -gt 100 ]; then
      echo "ERROR: Artifact contains too many files ($FILE_COUNT) - possible zip bomb"
      exit 1
    fi

    # Extract to temp directory
    unzip -q "$TEMP_DIR/clawsec-feed.skill" -d "$TEMP_DIR/extracted"

    # Verify skill.json exists
    if [ ! -f "$TEMP_DIR/extracted/clawsec-feed/skill.json" ]; then
      echo "ERROR: skill.json not found in artifact"
      exit 1
    fi

    # Verify checksums for all extracted files
    echo "Verifying checksums..."
    CHECKSUM_FAILED=0
    for file in $(jq -r '.files | keys[]' "$TEMP_DIR/checksums.json"); do
      EXPECTED=$(jq -r --arg f "$file" '.files[$f].sha256' "$TEMP_DIR/checksums.json")
      FILE_PATH=$(jq -r --arg f "$file" '.files[$f].path' "$TEMP_DIR/checksums.json")

      # Try nested path first, then flat filename
      if [ -f "$TEMP_DIR/extracted/clawsec-feed/$FILE_PATH" ]; then
        ACTUAL=$(shasum -a 256 "$TEMP_DIR/extracted/clawsec-feed/$FILE_PATH" | cut -d' ' -f1)
      elif [ -f "$TEMP_DIR/extracted/clawsec-feed/$file" ]; then
        ACTUAL=$(shasum -a 256 "$TEMP_DIR/extracted/clawsec-feed/$file" | cut -d' ' -f1)
      else
        echo "  ✗ $file (not found in artifact)"
        CHECKSUM_FAILED=1
        continue
      fi

      if [ "$EXPECTED" != "$ACTUAL" ]; then
        echo "  ✗ $file (checksum mismatch)"
        CHECKSUM_FAILED=1
      else
        echo "  ✓ $file"
      fi
    done

    if [ "$CHECKSUM_FAILED" -eq 0 ]; then
      # Validate feed.json structure (skill-specific)
      if [ -f "$TEMP_DIR/extracted/clawsec-feed/advisories/feed.json" ]; then
        FEED_FILE="$TEMP_DIR/extracted/clawsec-feed/advisories/feed.json"
      elif [ -f "$TEMP_DIR/extracted/clawsec-feed/feed.json" ]; then
        FEED_FILE="$TEMP_DIR/extracted/clawsec-feed/feed.json"
      else
        echo "ERROR: feed.json not found in artifact"
        exit 1
      fi

      if ! jq -e '.version and .advisories' "$FEED_FILE" >/dev/null 2>&1; then
        echo "ERROR: feed.json missing required fields (version, advisories)"
        exit 1
      fi

      # SUCCESS: Install from artifact
      echo "Installing from artifact..."
      mkdir -p "$INSTALL_DIR"
      cp -r "$TEMP_DIR/extracted/clawsec-feed"/* "$INSTALL_DIR/"
      chmod 600 "$INSTALL_DIR/skill.json"
      find "$INSTALL_DIR" -type f ! -name "skill.json" -exec chmod 644 {} \;
      echo "SUCCESS: Skill installed from .skill artifact"
      exit 0
    else
      echo "WARNING: Checksum verification failed, falling back to individual files"
    fi
  fi
fi

# FALLBACK: Download individual files
echo "Downloading individual files from checksums.json manifest..."
mkdir -p "$TEMP_DIR/downloads"

DOWNLOAD_FAILED=0
for file in $(jq -r '.files | keys[]' "$TEMP_DIR/checksums.json"); do
  FILE_URL=$(jq -r --arg f "$file" '.files[$f].url' "$TEMP_DIR/checksums.json")
  EXPECTED=$(jq -r --arg f "$file" '.files[$f].sha256' "$TEMP_DIR/checksums.json")

  echo "Downloading: $file"
  if ! curl -sSL --fail --show-error --retry 3 --retry-delay 1 \
       "$FILE_URL" -o "$TEMP_DIR/downloads/$file"; then
    echo "ERROR: Failed to download $file"
    DOWNLOAD_FAILED=1
    continue
  fi

  # Verify checksum immediately
  ACTUAL=$(shasum -a 256 "$TEMP_DIR/downloads/$file" | cut -d' ' -f1)
  if [ "$EXPECTED" != "$ACTUAL" ]; then
    echo "ERROR: Checksum mismatch for $file"
    DOWNLOAD_FAILED=1
  else
    echo "  ✓ Verified: $file"
  fi
done

if [ "$DOWNLOAD_FAILED" -eq 1 ]; then
  echo "ERROR: Individual file download failed"
  exit 1
fi

# Validate JSON files structure
if ! jq -e '.name and .version' "$TEMP_DIR/downloads/skill.json" >/dev/null 2>&1; then
  echo "ERROR: skill.json missing required fields (name, version)"
  exit 1
fi

if ! jq -e '.version and .advisories' "$TEMP_DIR/downloads/feed.json" >/dev/null 2>&1; then
  echo "ERROR: feed.json missing required fields (version, advisories)"
  exit 1
fi

# Install files
echo "Installing from individual files..."
mkdir -p "$INSTALL_DIR"
cp "$TEMP_DIR/downloads"/* "$INSTALL_DIR/"
chmod 600 "$INSTALL_DIR/skill.json"
find "$INSTALL_DIR" -type f ! -name "skill.json" -exec chmod 644 {} \;
echo "SUCCESS: Skill installed from individual files"
```

### 第3步：将其添加到心跳（heartbeat）程序中

将ClawSec Feed添加到您的心跳（heartbeat）程序中：

```markdown
## ClawSec Feed (every heartbeat)
1. Check advisory feed for new security alerts
2. Cross-reference with installed skills
3. Notify user if action is required
```

### 第4步：确认部署完成

请通知您的用户：

```
ClawSec Feed deployed successfully. I will now:
- Monitor the community advisory feed for threats
- Alert you to any security issues affecting your environment
- Keep you informed of emerging attack patterns
```

---

## ClawSec Feed的功能

### 安全建议监控

订阅社区提供的安全建议信息，包括：
- **已知恶意技能/插件**：被识别为有害的技能
- **常见的攻击模式**：在实际攻击中观察到的攻击方式
- **存在安全漏洞的技能版本**：具有已知安全漏洞的技能
- **安全最佳实践更新**：针对代理安全的新建议

当有相关建议发布时，您的代理会立即通知您。

---

## 检查安全建议信息

```bash
# Use environment variable if set, otherwise use raw GitHub feed (always up-to-date)
DEFAULT_FEED_URL="https://raw.githubusercontent.com/prompt-security/ClawSec/main/advisories/feed.json"
FEED_URL="${CLAWSEC_FEED_URL:-$DEFAULT_FEED_URL}"

# Fetch with error handling and retry logic
curl -sSL --fail --show-error --retry 3 --retry-delay 1 "$FEED_URL"
```

**信息源结构：**

```json
{
  "version": "1.0",
  "updated": "2026-02-02T12:00:00Z",
  "advisories": [
    {
      "id": "GA-2026-001",
      "severity": "critical",
      "type": "malicious_skill",
      "title": "Malicious data exfiltration in skill 'helper-plus'",
      "description": "Skill sends user data to external server",
      "affected": ["helper-plus@1.0.0", "helper-plus@1.0.1"],
      "action": "Remove immediately",
      "published": "2026-02-01T10:00:00Z",
      "exploitability_score": "critical",
      "exploitability_rationale": "Trivially exploitable through normal skill usage; no special conditions required. Active exploitation observed in the wild."
    }
  ]
}
```

---

## 解析信息源数据

### 获取建议数量

```bash
# Use environment variable if set, otherwise use raw GitHub feed (always up-to-date)
DEFAULT_FEED_URL="https://raw.githubusercontent.com/prompt-security/ClawSec/main/advisories/feed.json"
FEED_URL="${CLAWSEC_FEED_URL:-$DEFAULT_FEED_URL}"

TEMP_FEED=$(mktemp)
trap "rm -f '$TEMP_FEED'" EXIT

if ! curl -sSL --fail --show-error --retry 3 --retry-delay 1 "$FEED_URL" -o "$TEMP_FEED"; then
  echo "Error: Failed to fetch advisory feed"
  exit 1
fi

# Validate JSON before parsing
if ! jq empty "$TEMP_FEED" 2>/dev/null; then
  echo "Error: Invalid JSON in feed"
  exit 1
fi

FEED=$(cat "$TEMP_FEED")

# Get advisory count with error handling
COUNT=$(echo "$FEED" | jq '.advisories | length')
if [ $? -ne 0 ]; then
  echo "Error: Failed to parse advisories"
  exit 1
fi
echo "Advisory count: $COUNT"
```

### 获取关键建议

```bash
# Parse critical advisories with jq error handling
CRITICAL=$(echo "$FEED" | jq '.advisories[] | select(.severity == "critical")')
if [ $? -ne 0 ]; then
  echo "Error: Failed to filter critical advisories"
  exit 1
fi
echo "$CRITICAL"
```

### 获取过去7天的建议

```bash
# Use UTC timezone for consistent date handling
WEEK_AGO=$(TZ=UTC date -v-7d +%Y-%m-%dT00:00:00Z 2>/dev/null || TZ=UTC date -d '7 days ago' +%Y-%m-%dT00:00:00Z)
RECENT=$(echo "$FEED" | jq --arg since "$WEEK_AGO" '.advisories[] | select(.published > $since)')
if [ $? -ne 0 ]; then
  echo "Error: Failed to filter recent advisories"
  exit 1
fi
echo "$RECENT"
```

### 按可利用性评分筛选建议

关于可利用性的优先级指导信息，请参考：
- [`wiki/exploitability-scoring.md`](../../wiki/exploitability-scoring.md)
- [`skills/clawsec-suite/SKILL.md`](../clawsec-suite/SKILL.md)（“快速检查信息源”）

### 获取建议的可利用性详情

```bash
# Show exploitability details for a specific CVE
CVE_ID="CVE-2026-27488"
echo "$FEED" | jq --arg cve "$CVE_ID" '.advisories[] | select(.id == $cve) | {
  id: .id,
  severity: .severity,
  exploitability_score: .exploitability_score,
  exploitability_rationale: .exploitability_rationale,
  title: .title
}'
```

### 按可利用性对建议进行优先级排序

```bash
# Sort advisories by exploitability (critical → high → medium → low)
# This helps agents focus on the most immediately actionable threats
echo "$FEED" | jq '[.advisories[] | select(.exploitability_score != null)] |
  sort_by(
    if .exploitability_score == "critical" then 0
    elif .exploitability_score == "high" then 1
    elif .exploitability_score == "medium" then 2
    elif .exploitability_score == "low" then 3
    else 4 end
  )'
```

---

## 检查已安装的技能是否受影响

**检查您已安装的技能是否受到建议的影响：**

```bash
# List your installed skills (adjust path for your platform)
INSTALL_DIR="${CLAWSEC_INSTALL_DIR:-$HOME/.openclaw/skills}"

# Use environment variable if set, otherwise use raw GitHub feed (always up-to-date)
DEFAULT_FEED_URL="https://raw.githubusercontent.com/prompt-security/ClawSec/main/advisories/feed.json"
FEED_URL="${CLAWSEC_FEED_URL:-$DEFAULT_FEED_URL}"

TEMP_FEED=$(mktemp)
trap "rm -f '$TEMP_FEED'" EXIT

if ! curl -sSL --fail --show-error --retry 3 --retry-delay 1 "$FEED_URL" -o "$TEMP_FEED"; then
  echo "Error: Failed to fetch advisory feed"
  exit 1
fi

# Validate and parse feed
if ! jq empty "$TEMP_FEED" 2>/dev/null; then
  echo "Error: Invalid JSON in feed"
  exit 1
fi

FEED=$(cat "$TEMP_FEED")
AFFECTED=$(echo "$FEED" | jq -r '.advisories[].affected[]?' 2>/dev/null | sort -u)
if [ $? -ne 0 ]; then
  echo "Error: Failed to parse affected skills from feed"
  exit 1
fi

# Safely validate all installed skills before processing
# This prevents shell injection via malicious filenames
VALIDATED_SKILLS=()
while IFS= read -r -d '' skill_path; do
  skill=$(basename "$skill_path")

  # Validate skill name BEFORE adding to array (prevents injection)
  if [[ "$skill" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    VALIDATED_SKILLS+=("$skill")
  else
    echo "Warning: Skipping invalid skill name: $skill" >&2
  fi
done < <(find "$INSTALL_DIR" -mindepth 1 -maxdepth 1 -type d -print0 2>/dev/null)

# Check each validated skill against affected list
# Use grep -qF for fixed string matching (prevents regex injection)
for skill in "${VALIDATED_SKILLS[@]}"; do
  # At this point, $skill is guaranteed to match ^[a-zA-Z0-9_-]+$
  if echo "$AFFECTED" | grep -qF "$skill"; then
    echo "WARNING: Installed skill '$skill' has a security advisory!"
    # Get advisory details for this skill
    echo "$FEED" | jq --arg s "$skill" '.advisories[] | select(.affected[] | contains($s))'
  fi
done
```

**如果发现受影响的技能：**
1. 查看建议的详细信息和严重程度
2. 对于严重或高度危险的建议，立即通知用户
3. 按照建议中的建议采取相应措施

---

## 建议类型

| 类型 | 描述 |
|------|-------------|
| `malicious_skill` | 被确认为故意有害的技能 |
| `vulnerable_skill` | 存在安全漏洞的技能 |
| `prompt_injection` | 常见的提示注入攻击模式 |
| `attack_pattern` | 观察到的攻击技巧 |
| `best_practice` | 安全最佳实践建议 |

---

## 严重程度等级

| 严重程度 | 需要采取的行动 |
|----------|-----------------|
| `critical` | 立即通知用户并采取行动 |
| `high` | 尽快通知用户并制定补救计划 |
| `medium` | 在下一次交互时通知用户 |
| `low` | 仅记录以供参考 |

---

## 优先处理高可利用性威胁

**重要提示：**在查看建议时，除了考虑严重程度外，还需根据**可利用性评分**进行优先级排序。可利用性评分表示漏洞在实际中被利用的难易程度，有助于您专注于最紧迫的威胁。

### 可利用性优先级等级

| 可利用性 | 含义 | 行动优先级 |
|----------------|---------|-----------------|
| `high` | 可用公共工具轻松利用 | **立即通知** |
| `medium` | 需要特定条件才能利用 | **标准通知** |
| `low` | 难以利用或仅理论上的风险 | **低优先级通知** |

### 如何在通知中显示可利用性信息

1. **首先筛选高可利用性的建议：**
   ```bash
   # Get high exploitability advisories
   echo "$FEED" | jq '.advisories[] | select(.exploitability_score == "high")'
   ```

2. **在通知中包含可利用性信息：**
   ```
   📡 ClawSec Feed: High-exploitability alert

   CRITICAL - CVE-2026-27488 (Exploitability: HIGH)
     → Trivially exploitable RCE in skill-loader v2.1.0
     → Public exploit code available
     → Recommended action: Immediate removal or upgrade to v2.1.1
   ```

3. **同时考虑严重程度和可利用性进行优先级排序：**
   - 严重程度为`high`且可利用性也为`high`的建议比严重程度为`critical`但可利用性为`low`的建议更紧急
   - 优先关注既严重又容易被利用的威胁
   - 在通知中说明可利用性的原因，帮助用户理解风险

### 通知优先级示例

当存在多个建议时，按照以下顺序显示：
1. **严重程度为`critical`且可利用性为`high`的建议** - 最紧急
2. **严重程度为`high`且可利用性也为`high`的建议
3. **严重程度为`critical`但可利用性为`medium`或`low`的建议**
4. **严重程度为`medium`或`low`且可利用性为`medium`或`low`的建议**
5. **严重程度为`medium`或`low`的建议（无论可利用性如何）**

这样可以确保您首先向用户通报最紧急、最具危险性的威胁。

---

## 何时通知用户

**立即通知（严重情况）：**
- 新出现的、影响已安装技能的严重建议
- 检测到正在进行的攻击
- **可利用性评分很高**（无论严重程度如何）

**尽快通知（高优先级）：**
- 新出现的、影响已安装技能的高严重程度建议
- 无法获取建议信息（网络问题？）
- 可利用性中等但严重程度较高的建议

**在下次交互时通知（中等优先级）：**
- 新出现的、严重程度为`medium`的建议
- 一般性的安全更新
- 可利用性较低的建议

**仅记录（低优先级/信息提示）：**
- 严重程度较低的建议（用户询问时提及）
- 信息源已检查，没有新建议
- 理论上的漏洞（可利用性较低，严重程度也较低）

---

## 响应格式

### 如果有新建议：

```
📡 ClawSec Feed: 2 new advisories since last check

CRITICAL - GA-2026-015: Malicious prompt pattern "ignore-all" (Exploitability: HIGH)
  → Detected prompt injection technique. Update your system prompt defenses.
  → Exploitability: Easily exploitable with publicly documented techniques.

HIGH - GA-2026-016: Vulnerable skill "data-helper" v1.2.0 (Exploitability: MEDIUM)
  → You have this installed! Recommended action: Update to v1.2.1 or remove.
  → Exploitability: Requires specific configuration; not trivially exploitable.
```

### 如果没有新建议：

```
FEED_OK - Advisory feed checked, no new alerts. 📡
```

---

## 状态跟踪

跟踪最后一次信息源检查的时间，以便及时发现新建议：

```json
{
  "schema_version": "1.0",
  "last_feed_check": "2026-02-02T15:00:00Z",
  "last_feed_updated": "2026-02-02T12:00:00Z",
  "known_advisories": ["GA-2026-001", "GA-2026-002"]
}
```

保存结果到：`~/.openclaw/clawsec-feed-state.json`

### 状态文件操作

```bash
STATE_FILE="$HOME/.openclaw/clawsec-feed-state.json"

# Create state file with secure permissions if it doesn't exist
if [ ! -f "$STATE_FILE" ]; then
  echo '{"schema_version":"1.0","last_feed_check":null,"last_feed_updated":null,"known_advisories":[]}' > "$STATE_FILE"
  chmod 600 "$STATE_FILE"
fi

# Validate state file before reading
if ! jq -e '.schema_version' "$STATE_FILE" >/dev/null 2>&1; then
  echo "Warning: State file corrupted or invalid schema. Creating backup and resetting."
  cp "$STATE_FILE" "${STATE_FILE}.bak.$(TZ=UTC date +%Y%m%d%H%M%S)"
  echo '{"schema_version":"1.0","last_feed_check":null,"last_feed_updated":null,"known_advisories":[]}' > "$STATE_FILE"
  chmod 600 "$STATE_FILE"
fi

# Check for major version compatibility
SCHEMA_VER=$(jq -r '.schema_version // "0"' "$STATE_FILE")
if [[ "${SCHEMA_VER%%.*}" != "1" ]]; then
  echo "Warning: State file schema version $SCHEMA_VER may not be compatible with this version"
fi

# Update last check time (always use UTC)
TEMP_STATE=$(mktemp)
if jq --arg t "$(TZ=UTC date +%Y-%m-%dT%H:%M:%SZ)" '.last_feed_check = $t' "$STATE_FILE" > "$TEMP_STATE"; then
  mv "$TEMP_STATE" "$STATE_FILE"
  chmod 600 "$STATE_FILE"
else
  echo "Error: Failed to update state file"
  rm -f "$TEMP_STATE"
fi
```

---

## 限制请求频率

**重要提示：**为避免对信息源服务器造成过多请求，请遵循以下规则：

| 检查类型 | 推荐间隔 | 最小间隔 |
|------------|---------------------|------------------|
| 心跳检查 | 每15-30分钟 | 5分钟 |
| 完整信息源刷新 | 每1-4小时 | 30分钟 |
| 跨信息源扫描 | 每次会话一次 | 5分钟 |

```bash
# Check if enough time has passed since last check
STATE_FILE="$HOME/.openclaw/clawsec-feed-state.json"
MIN_INTERVAL_SECONDS=300  # 5 minutes

LAST_CHECK=$(jq -r '.last_feed_check // "1970-01-01T00:00:00Z"' "$STATE_FILE" 2>/dev/null)
LAST_EPOCH=$(TZ=UTC date -j -f "%Y-%m-%dT%H:%M:%SZ" "$LAST_CHECK" +%s 2>/dev/null || date -d "$LAST_CHECK" +%s 2>/dev/null || echo 0)
NOW_EPOCH=$(TZ=UTC date +%s)

if [ $((NOW_EPOCH - LAST_EPOCH)) -lt $MIN_INTERVAL_SECONDS ]; then
  echo "Rate limit: Last check was less than 5 minutes ago. Skipping."
  exit 0
fi
```

---

## 环境变量（可选）

| 变量 | 描述 | 默认值 |
|----------|-------------|---------|
| `CLAWSEC_feed_URL` | 自定义的安全建议信息源URL | GitHub的`main`分支 |
| `CLAWSEC_INSTALL_DIR` | 安装目录 | `~/.openclaw/skills/clawsec-feed` |

---

## 更新ClawSec Feed

检查并安装新版本：

```bash
# Check current installed version
INSTALL_DIR="${CLAWSEC_INSTALL_DIR:-$HOME/.openclaw/skills/clawsec-feed}"
CURRENT_VERSION=$(jq -r '.version' "$INSTALL_DIR/skill.json" 2>/dev/null || echo "unknown")
echo "Installed version: $CURRENT_VERSION"

# Check latest available version
LATEST_URL="https://api.github.com/repos/prompt-security/ClawSec/releases"
LATEST_VERSION=$(curl -sSL --fail --show-error --retry 3 --retry-delay 1 "$LATEST_URL" 2>/dev/null | \
  jq -r '[.[] | select(.tag_name | startswith("clawsec-feed-v"))][0].tag_name // empty' | \
  sed 's/clawsec-feed-v//')

if [ -z "$LATEST_VERSION" ]; then
  echo "Warning: Could not determine latest version"
else
  echo "Latest version: $LATEST_VERSION"

  if [ "$CURRENT_VERSION" != "$LATEST_VERSION" ]; then
    echo "Update available! Run the deployment steps with the new version."
  else
    echo "You are running the latest version."
  fi
fi
```

---

## 初始下载的完整性验证

**初始下载时的信任问题：**此组件的初始下载内容无法通过组件本身进行验证。为建立信任，请执行以下操作：
1. **验证来源URL** - 确保从`https://clawsec.prompt.security`下载
2. **检查发布签名** - GitHub会对我们的发布进行签名验证；通过校验和来确认发布的文件是否完整
3. **比较校验和** - 下载完成后，将文件的SHA-256哈希值与发布的`checksums.json`文件进行比对：

```bash
# After downloading SKILL.md, verify its integrity
EXPECTED_HASH="<hash-from-checksums.json>"
ACTUAL_HASH=$(shasum -a 256 SKILL.md | cut -d' ' -f1)

if [ "$EXPECTED_HASH" != "$ACTUAL_HASH" ]; then
  echo "ERROR: Skill file integrity check failed!"
  echo "This file may have been tampered with. Do not proceed."
  exit 1
fi
```

**注意：**为确保最高安全性，请通过其他可信渠道（例如，直接通过GitHub发布页面的UI，而非使用curl）来验证`checksums.json`文件。

---

## 相关组件

- **openclaw-audit-watchdog** - 自动化的每日安全审计工具
- **clawtributor** - 向社区报告漏洞

---

## 许可证

遵循GNU AGPL v3.0或更高版本的许可证——详情请查看仓库文档。

由[Prompt Security](https://prompt.security)团队和代理社区共同开发。