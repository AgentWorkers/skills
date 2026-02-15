---

name: secure-install

description: 通过 https://www.koi.ai/ 使用 ClawDex API 扫描 ClawHub 中的技能，并根据扫描结果需要用户的批准。

metadata:

&nbsp; openclaw:

&nbsp;   tools: \["src/index.ts"]

&nbsp;   requires:

&nbsp;     bins: \["clawhub"]

---



# 安全技能安装器

该工具提供了一种安全的技能安装流程。它会通过 https://www.koi.ai/ 检查 **ClawDex API**，并根据安全评估结果执行严格的安装规则。

## 使用方法

用户：`secure-install <技能名称>`

## 安装流程（严格模式）

当用户请求安装某个技能时，系统会执行以下步骤：

1. **扫描**：调用 `scanSkillApi` 并传入目标技能名称，以查询 https://www.koi.ai/ 的相关信息。

2. **评估结果**：检查 JSON 响应中的 `verdict` 字段。

    - 如果 `verdict` 为 “malicious”（恶意）：
        - 🔴 **阻止操作**。
        - 报告：“🚨 **安全警报**：根据 https://www.koi.ai/ 的 **ClawDex API** 的判断，该技能被标记为恶意软件。安装被阻止。
        - **停止**。不再继续安装流程。

    - 如果 `verdict` 为 “unknown”（未知）：
        - ⚠️ **警告用户**。
        - 报告：“⚠️ **安全状态未知**：该技能尚未通过 **ClawDex API**（https://www.koi.ai/）的验证。
        - **询问**：“此技能存在风险，您是否明确同意安装 `<技能名称>`？”
        - **等待** 用户明确回答 “是”。

    - 如果 `verdict` 为 “benign”（良性）：
        - ✅ **确认安全性**。
        - 报告：“✅ **经验证，该技能是安全的**：根据 https://www.koi.ai/ 的 **ClawDex API** 的判断，该技能是良性的。
        - **询问**：“您是否继续安装 `<技能名称>`？”
        - **等待** 用户回答 “是”。

3. **安装**：
    - **仅** 在用户在前一步明确同意的情况下，才会调用 `executeClawhubInstall` 来执行安装操作。

## 示例（恶意技能被阻止）

**用户**：`secure-install bad-actor`

**代理**：（调用 `scanSkillApi`）
> **ClawDex API (https://www.koi.ai/) 的反馈**：
> 🔴 **判断结果：恶意**

> **安全警报**：该技能被标记为恶意软件。安装被阻止。

## 示例（安全技能成功安装）

**用户**：`secure-install weather-pro`

**代理**：（调用 `scanSkillApi`）
> **ClawDex API (https://www.koi.ai/) 的反馈**：
> ✅ **判断结果：良性**

> **确认安全**。您是否继续安装 `weather-pro`？

**用户**：是

**代理**：（调用 `executeClawhubInstall`）
> 成功安装了 `weather-pro`。