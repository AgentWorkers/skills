---
name: clawsec-feed
version: 0.0.4
description: 安全公告订阅服务，自动扫描 NVD（National Vulnerability Database）中与 OpenClaw 相关的漏洞信息。每日更新。
homepage: https://clawsec.prompt.security
metadata: {"openclaw":{"emoji":"📡","category":"security"}}
clawdis:
  emoji: "📡"
  requires:
    bins: [curl, jq]
---

# ClawSec Feed 📡  
用于监控AI代理的安全咨询信息。订阅社区提供的威胁情报，及时了解新出现的威胁。  

该信息源每天会自动更新，内容包含来自NIST国家漏洞数据库（NVD）的与OpenClaw、clawdbot和Moltbot相关的CVE（安全漏洞）。  

**该项目由[Prompt Security](https://prompt.security)开发，采用开源技术。**  

---

## 安装选项  
您可以通过两种方式获取clawsec-feed：  

### 选项A：随ClawSec Suite一起安装（推荐）  
**如果您已经安装了ClawSec Suite，那么您可能已经拥有该组件！**  
ClawSec-feed与ClawSec Suite捆绑在一起，提供重要的CVE和安全威胁情报信息。在安装套件时，如果尚未安装该组件，系统会从捆绑包中自动安装它。  
**优点：**  
- 无需单独下载；  
- 安装路径固定（`~/.openclaw/skills/clawsec-feed/`）；  
- 如果已安装过该组件，不会被覆盖；  
- 安装过程会进行完整性验证。  

### 选项B：独立安装（请参阅此页面）  
如果您只需要咨询信息源，而不需要整个套件，可以选择独立安装。  
**适用场景：**  
- 仅需要咨询信息源；  
- 希望在安装套件之前先安装该组件；  
- 希望对安装过程有更多控制权。  
**优点：**  
- 安装过程更简洁；  
- 与套件分离，安装更加灵活。  

**请继续阅读以下独立安装说明。**  

---

**安装步骤：**  
在运行代理之前，请先查看相关脚本！  

---  
**获取该技能文件后，请按照**[此处提供的分步指南](#deploy-clawsec-feed)**进行部署。  

---

## 部署ClawSec Feed  
**安装步骤：**  
1. 创建技能目录并保存该文件。  
2. 安装技能文件。  
3. 将ClawSec Feed添加到代理的心跳（heartbeat）机制中。  
4. 确认部署成功，并通知用户。  

---

## ClawSec Feed的功能  
**咨询信息监控**：  
- 监控以下内容的社区咨询信息：  
  - **已知恶意技能/插件**：被确认为有害的技能；  
  - **常见的攻击模式**：在实际攻击中观察到的攻击方式；  
  - **存在安全漏洞的技能版本**；  
  - **安全最佳实践更新**：针对代理安全的新建议。  
当有相关咨询信息发布时，代理会立即通知您。  

---

## 检查咨询信息  
**信息源结构：**  
（具体结构信息请参考原文中的**```json
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
      "published": "2026-02-01T10:00:00Z"
    }
  ]
}
```**部分。）  

---

## 解析咨询信息  
- 获取咨询信息的数量；  
- 获取关键咨询信息；  
- 获取过去7天的咨询信息。  

---

## 检查已安装的技能是否受影响  
**检查您已安装的技能是否受到咨询信息的影响：**  
（具体操作步骤请参考原文中的**```bash
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
```**部分。）  
**如果发现受影响的技能：**  
1. 查看咨询信息的详细内容和严重程度；  
2. 对于严重或高度危险的咨询信息，立即通知用户；  
3. 按照咨询信息中的建议采取相应措施。  

---

## 咨询信息类型  
| 类型 | 描述 |  
|------|-------------|  
| `malicious_skill` | 被确认为故意有害的技能；  
| `vulnerable_skill` | 存在安全漏洞的技能；  
| `prompt_injection` | 常见的提示注入攻击方式；  
| `attack_pattern` | 观察到的攻击技巧；  
| `best_practice` | 安全最佳实践建议。  

---

## 严重程度分级  
| 严重程度 | 需要采取的行动 |  
|----------|-----------------|  
| `critical` | 立即通知用户并采取行动；  
| `high` | 尽快通知用户并制定补救措施；  
| `medium` | 下次交互时通知用户；  
| `low` | 仅记录以供参考。  

---

## 何时通知用户  
**立即通知（严重情况）：**  
- 新出现的严重咨询信息影响到已安装的技能；  
- 检测到正在进行的攻击。  

**尽快通知（高度危险情况）：**  
- 新出现的严重等级的咨询信息影响到已安装的技能；  
- 无法获取咨询信息（可能是网络问题）。  

**下次交互时通知（中等情况）：**  
- 新出现的中等严重程度的咨询信息；  
- 一般性的安全更新。  

**仅记录（低/信息性情况）：**  
- 低严重程度的咨询信息（用户询问时提供）；  
- 检查了信息源，没有新咨询信息。  

---

## 响应格式  
**如果有新咨询信息：**  
（具体响应格式请参考原文中的**```
📡 ClawSec Feed: 2 new advisories since last check

CRITICAL - GA-2026-015: Malicious prompt pattern "ignore-all"
  → Detected prompt injection technique. Update your system prompt defenses.

HIGH - GA-2026-016: Vulnerable skill "data-helper" v1.2.0
  → You have this installed! Recommended action: Update to v1.2.1 or remove.
```**部分。）  
**如果没有新信息：**  
（具体处理方式请参考原文中的**```
FEED_OK - Advisory feed checked, no new alerts. 📡
```**部分。）  

---

## 状态跟踪  
**跟踪最后一次信息源检查时间，以便及时发现新咨询信息：**  
（具体操作步骤请参考原文中的**```json
{
  "schema_version": "1.0",
  "last_feed_check": "2026-02-02T15:00:00Z",
  "last_feed_updated": "2026-02-02T12:00:00Z",
  "known_advisories": ["GA-2026-001", "GA-2026-002"]
}
```**部分。）  
**保存状态信息到：`~/.openclaw/clawsec-feed-state.json`。**  

### 状态文件操作  
（具体操作步骤请参考原文中的**```bash
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
```**部分。）  

---

## 限制请求频率  
**重要提示：**为避免对信息源服务器造成过多请求，请遵循以下规则：  
| 检查类型 | 推荐间隔 | 最小间隔 |  
|------------|---------------------|------------------|  
| 心跳检查 | 每15-30分钟 | 5分钟；  
| 完整信息源刷新 | 每1-4小时 | 30分钟；  
| 跨技能关联扫描 | 每次会话一次 | 5分钟。**  

---

## 环境变量（可选）  
| 变量 | 描述 | 默认值 |  
|----------|-------------|---------|  
| `CLAWSEC_FEED_URL` | 自定义咨询信息源URL | GitHub的`main`分支地址 |  
| `CLAWSEC_INSTALL_DIR` | 安装目录 | `~/.openclaw/skills/clawsec-feed` |  

---

## 更新ClawSec Feed  
**检查并安装新版本：**  
（具体操作步骤请参考原文中的**```bash
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
```**部分。）  

---

## 初始下载的完整性验证  
**初始下载的完整性验证：**  
由于初始下载的文件无法通过自身进行验证，因此需要采取以下步骤来建立信任：  
1. **验证来源URL**：确保从`https://clawsec.prompt.security`下载；  
2. **检查发布签名**：GitHub会对我们的发布版本进行签名验证；  
3. **对比哈希值**：下载后，将文件的SHA-256哈希值与发布的`checksums.json`文件进行比对。  
（具体操作步骤请参考原文中的**```bash
# After downloading SKILL.md, verify its integrity
EXPECTED_HASH="<hash-from-checksums.json>"
ACTUAL_HASH=$(shasum -a 256 SKILL.md | cut -d' ' -f1)

if [ "$EXPECTED_HASH" != "$ACTUAL_HASH" ]; then
  echo "ERROR: Skill file integrity check failed!"
  echo "This file may have been tampered with. Do not proceed."
  exit 1
fi
```**部分。）  
**注意：**为确保最大安全性，建议通过其他可信渠道（例如直接从GitHub发布页面的UI界面）验证`checksums.json`文件。  

---

**相关技能**  
- **openclaw-audit-watchdog**：自动执行的每日安全审计工具；  
- **clawtributor**：用于向社区报告漏洞的工具。  

---

## 许可证  
MIT许可证——详情请参阅代码仓库。  
该组件由[Prompt Security](https://prompt.security)团队及代理社区共同开发。