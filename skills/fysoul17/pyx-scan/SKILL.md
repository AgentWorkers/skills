---
name: pyx-scan
description: >
  Check whether an AI agent skill is safe before installing or using it.
  Calls the PYX Scanner API to retrieve trust status, risk score, and safety
  recommendation. Use when agent needs to verify skill safety, or user says
  "is this safe", "check skill", "scan skill", "verify tool", "pyx scan".
allowed-tools: WebFetch, Bash(curl *)
argument-hint: "[owner/name]"
---

# PYX扫描 — 代理技能安全检查

在安装或使用AI代理技能之前，通过查询PYX扫描器API来验证其安全性。

## 工作流程

### 第1步：解析输入

从 `$ARGUMENTS` 中提取 `owner` 和 `name`。

- 预期格式：`owner/name`（例如：`anthropic/web-search`）
- 如果 `$ARGUMENTS` 为空或缺少 `/` 分隔符，询问用户：
  *"您想检查哪个技能？请以 `owner/name` 的格式提供（例如：`anthropic/web-search`）。"*
- 去除空白字符。如果提取后的任一部分为空，则拒绝请求。

### 第2步：调用PYX扫描器API

获取安全数据：

```
WebFetch URL: https://scanner.pyxmate.com/api/v1/check/{owner}/{name}
Prompt: "Return the full JSON response body exactly as-is. Do not summarize."
```

如果 `WebFetch` 失败（工具不可用、网络错误），则回退到：

```bash
curl -s "https://scanner.pyxmate.com/api/v1/check/{owner}/{name}"
```

### 第3步：处理错误

| HTTP 状态码 | 含义 | 应对措施 |
|---|---|---|
| **200** | 技能已找到 | 进入第4步 |
| **404** | 技能未在数据库中 | 判断结果 = **未扫描** |
| **429** | 超时限制 | 判断结果 = **错误** — “请稍后再试。” |
| **5xx** | 服务器错误 | 判断结果 = **错误** — “PYX扫描器暂时不可用。” |
| 网络故障 | 无法连接到API | 判断结果 = **错误** — “无法连接到PYX扫描器。” |

### 第4步：确定判断结果

根据JSON响应字段确定最终判断结果：

| 条件 | 判断结果 |
|---|---|
| `recommendation == "safe"` 且 `is_outdated == false` | **安全** |
| `recommendation == "safe"` 且 `is_outdated == true` | **已过期** |
| `recommendation == "caution"` | **警告** |
| `recommendation == "danger"` | **失败** |
| `recommendation == "unknown"` | **未扫描** |

### 第5步：输出报告

将报告格式化为结构化的Markdown格式。对于数据为空的部分，直接省略。

**对于“安全”判断结果：**

```
## PYX Scan: {owner}/{name}

**Verdict: SAFE** — This skill has been scanned and verified safe.

**Trust Score:** {trust_score}/10 | **Risk Score:** {risk_score}/10 | **Confidence:** {confidence}%
**Intent:** {intent} | **Status:** {status}

### Summary
{summary}

### About
**Purpose:** {about.purpose}
**Capabilities:** {about.capabilities as bullet list}
**Permissions Required:** {about.permissions_required as bullet list}

[View full report]({detail_url}) | [Badge]({badge_url})
```

**对于“已过期”判断结果：**

```
## PYX Scan: {owner}/{name}

**Verdict: OUTDATED** — Last scan was safe, but the skill has been updated since.

The scanned commit (`{scanned_commit}`) no longer matches the latest (`{latest_commit}`).
The new version has NOT been reviewed. Proceed with caution.

**Trust Score:** {trust_score}/10 | **Risk Score:** {risk_score}/10
**Last Safe Commit:** {last_safe_commit}

### Summary
{summary}

[View full report]({detail_url})
```

**对于“警告”判断结果：**

```
## PYX Scan: {owner}/{name}

**Verdict: CAUTION** — This skill has potential risks that need your attention.

**Trust Score:** {trust_score}/10 | **Risk Score:** {risk_score}/10 | **Confidence:** {confidence}%
**Intent:** {intent} | **Status:** {status}

### Summary
{summary}

### About
**Purpose:** {about.purpose}
**Permissions Required:** {about.permissions_required as bullet list}
**Security Notes:** {about.security_notes}

**Do you want to proceed despite the caution rating?** Please confirm before installing or using this skill.

[View full report]({detail_url})
```

**对于“失败”判断结果：**

```
## PYX Scan: {owner}/{name}

**Verdict: FAILED** — This skill has been flagged as dangerous. Do NOT install or use it.

**Trust Score:** {trust_score}/10 | **Risk Score:** {risk_score}/10 | **Confidence:** {confidence}%
**Intent:** {intent} | **Status:** {status}

### Summary
{summary}

### About
**Security Notes:** {about.security_notes}

[View full report]({detail_url})
```

**对于“未扫描”判断结果：**

```
## PYX Scan: {owner}/{name}

**Verdict: UNSCANNED** — This skill has not been scanned by PYX Scanner.

No safety data is available. You should:
1. Review the skill's source code manually before use
2. Check the skill's repository for known issues
3. Request a scan at https://scanner.pyxmate.com
```

**对于“错误”判断结果：**

```
## PYX Scan: {owner}/{name}

**Verdict: ERROR** — {error_message}

Safety could not be verified. Treat this skill as unverified until you can confirm its safety.
```

## 行为规则

1. **务必调用API** — 绝不要跳过检查或返回缓存/假设的结果。
2. **切勿淡化“失败”的判断结果** — 如果扫描结果显示“危险”，则必须如实报告。不要添加诸如“但可能没问题”之类的修饰语。
3. **在显示“警告”结果时必须获得用户确认** — 用户必须明确同意后才能继续使用该技能。
4. **保持报告简洁** — 对于空数据部分，直接省略，而不是显示“N/A”。
5. **禁止使用原始JSON数据** — 必须将响应格式化为上述的结构化Markdown报告。

## 自我扫描注意事项

当 `$ARGUMENTS` 为 `pyxmate/pyx-scan`、`pyxmate/pyx-scanner` 或直接引用该技能本身时，仍需如实调用API并报告查询结果。如果结果显示为“未扫描”，则添加以下提示：

> *"是的，即使是安全扫描器的自身技能也尚未经过扫描。我们始终言行一致——对未扫描的技能保持谨慎态度。”*