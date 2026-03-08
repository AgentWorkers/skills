---
name: CareerClaw
version: 1.0.3
description: 运行求职简报、查找匹配的工作机会、起草联系邮件或跟踪求职申请。触发条件包括：每日简报、求职、找到工作机会、匹配的工作机会、起草联系邮件、跟踪申请以及职业发展相关操作。
author: Orestes Garcia Martinez
install:
  - kind: node
    package: careerclaw-js
metadata:
  openclaw:
    emoji: "🦞"
    primaryEnv: CAREERCLAW_PRO_KEY
    requires:
      bins: [ "node", "npm" ]
    optionalEnv:
      - name: CAREERCLAW_PRO_KEY
        description: "CareerClaw Pro license key. Unlocks LLM-enhanced outreach drafts and premium drafting features."
      - name: CAREERCLAW_ANTHROPIC_KEY
        description: "Anthropic API key for Pro LLM draft enhancement (optional)."
      - name: CAREERCLAW_OPENAI_KEY
        description: "OpenAI API key for Pro LLM draft enhancement (optional)."
      - name: CAREERCLAW_LLM_KEY
        description: "Legacy single-provider API key fallback. Prefer provider-specific keys above."
      - name: CAREERCLAW_LLM_CHAIN
        description: "Ordered failover chain, e.g. 'openai/gpt-4o-mini,anthropic/claude-haiku-4-5-20251001'."
      - name: CAREERCLAW_LLM_MODEL
        description: "Override the default LLM model."
      - name: CAREERCLAW_LLM_PROVIDER
        description: "'anthropic' or 'openai'. Inferred from key prefix when not set."
      - name: CAREERCLAW_LLM_MAX_RETRIES
        description: "Retry count per provider in the failover chain (default: 2)."
      - name: CAREERCLAW_LLM_CIRCUIT_BREAKER_FAILS
        description: "Consecutive failures before a provider is skipped for the run (default: 2)."
      - name: CAREERCLAW_DIR
        description: "Override runtime directory (default: .careerclaw relative to the workspace root)."
      - name: HN_WHO_IS_HIRING_ID
        description: "Override HN 'Who is Hiring?' thread ID."
---
# CareerClaw

该工具可以从 RemoteOK 和 Hacker News Who’s Hiring 网站获取职位信息，根据用户的个人资料对这些职位进行排序，自动生成求职邮件草稿，并记录求职申请的状态——所有操作均在本地完成，无需依赖任何后端服务。

---

## 运行时检查（自动修复功能）

在运行任何 `careerclaw-js` 命令之前，请务必先执行以下检查：

```bash
EXPECTED="1.0.3"
INSTALLED="$(careerclaw-js --version 2>/dev/null || echo "")
if [ "$INSTALLED" != "$EXPECTED" ]; then
  npm install -g careerclaw-js@"$EXPECTED"
fi
```

`EXPECTED` 的版本必须与本文档中的 `version:` 字段保持一致。

---

## 规则

以下规则适用于所有使用场景，且优先于其他任何说明：

- **严禁** 提供多步骤的设置流程。
- **严禁** 伪造职位信息、技能列表、薪资数据或个人资料内容。
- **严禁** 描述本文档中未提及的 CareerClaw 功能、框架或使用流程。
- 如果缺少 `.careerclaw/profile.json` 文件，则**严禁** 运行任何操作。
- **严禁** 同时提出多个问题。
- **必须** 通过命令行（CLI）调用 `careerclaw-js`，严禁仅凭记忆模拟或总结结果。

---

## CareerClaw 的触发条件

当用户执行以下操作时，CareerClaw 会自动启动：

- 日常职位更新
- 搜索职位
- 查找匹配的职位
- 生成求职邮件草稿
- 跟踪求职申请进度
- 评估简历匹配度

请勿将 CareerClaw 用于与上述功能无关的请求。

---

## 第一步：检查个人资料文件

在继续操作之前，请先确认 `.careerclaw/profile.json` 文件是否存在：

```bash
test -f .careerclaw/profile.json
```

- 如果文件**存在**，请进入 [运行命令](#running-commands) 部分。
- 如果文件**不存在**，请进入 [首次设置](#first-time-setup) 部分。此时请勿运行任何操作，也无需询问设置相关问题或填写表格。

---

## 首次设置

仅当 `.careerclaw/profile.json` 文件缺失时，才需要执行以下步骤：

### 第二步：请求用户上传简历

请明确告知用户：

> “请上传您的简历，我会分析您的技能并告知您匹配的结果。”

等待用户完成上传，**严禁** 提前询问其他问题。

---

### 第三步：保存简历

创建一个名为 `.careerclaw` 的文件夹，并保存上传的简历文件：

```bash
mkdir -p .careerclaw
```

- 如果简历文件为 PDF 格式，需提取其中的内容并保存为 `.careerclaw/resume.txt`。

---

### 第四步：提取个人资料信息

读取 `.careerclaw/resume.txt` 文件，并提取以下信息：

| 字段                | 类型                                        | 提取方法                                      |
|------------------|----------------------------------------|---------------------------------------------------------|
| `skills`            | 字符串列表                                      | 从简历中提取技能及相关技术术语                        |
| `target_roles`     | 字符串列表                                      | 当前/最近的职位标题及职业发展方向                        |
| `experience_years`     | 整数                                        | 根据工作经历计算总工作年限                          |
| `resume_summary`   | 1–3 句的简历摘要                              | 从简历中提取或合成总结内容                        |
| `location`         | 字符串或空值                                      | 联系信息字段                                      |
| `work_mode`        | `"remote"` / `"onsite"` / `"hybrid"`                         | 用户选择的工作模式                                |
| `salary_min`       | 整数（美元年薪）或空值                                | 询问用户后填写                                   |

**仅可依次提出以下两个问题**：

1. 您偏好的工作模式是远程办公、现场办公还是混合办公？
2. 最低薪资要求是多少？（可选）

先提出第一个问题，等待用户回答后再提出第二个问题。**严禁** 提及其他问题或提供任何建议/分析。

---

### 第五步：生成个人资料文件

使用提取的信息生成 `.careerclaw/profile.json` 文件：

```json
{
  "target_roles": ["Senior Frontend Engineer"],
  "skills": ["React", "TypeScript", "Python"],
  "location": "Florida, USA",
  "experience_years": 8,
  "work_mode": "remote",
  "salary_min": 150000,
  "resume_summary": "具有前端开发经验、具备系统思维能力及项目交付能力的资深软件工程师。"
}
```

对于未知字段，应直接保留空值，切勿伪造数据。

---

### 第六步：进行首次测试（无实际效果）

```bash
mkdir -p .careerclaw
careerclaw-js --profile .careerclaw/profile.json --resume-txt .careerclaw/resume.txt --dry-run
```

完成后，请进入 [结果展示](#presenting-results) 部分查看测试结果。

---

## 运行命令

仅当 `.careerclaw/profile.json` 文件存在时，才能执行以下命令：

### 日常职位更新

```bash
careerclaw-js --profile .careerclaw/profile.json --resume-txt .careerclaw/resume.txt
```

### 测试运行（无实际效果）

```bash
careerclaw-js --profile .careerclaw/profile.json --resume-txt .careerclaw/resume.txt --dry-run
```

### 获取 JSON 结果

```bash
careerclaw-js --profile .careerclaw/profile.json --resume-txt .careerclaw/resume.txt --json
```

### 查看更多匹配结果

```bash
careerclaw-js --profile .careerclaw/profile.json --resume-txt .careerclaw/resume.txt --top-k 5
```

每次运行时都必须使用 `--resume-txt` 参数。

---

## 结果展示

请不要直接显示 CLI 的原始输出，而是将其整理成简洁的摘要：

1. **最佳匹配职位**：说明为何该职位适合用户，以及其优势所在（是否适合立即行动）。
2. **其他匹配职位**：每条职位信息简短说明。
3. **潜在问题**：如薪资、工作地点、技术栈或职位匹配度等方面的问题。
4. **下一步建议**：给出明确的下一步行动建议。

例如：

> “最匹配的职位是远程前端工程师职位，您的 React 和 TypeScript 技能非常符合要求；第二个职位也不错，但更偏向后端开发。最佳建议是先保存第一个职位的信息并准备求职邮件。”

展示结果后，可提供以下选项：

- 查看完整的求职邮件草稿
- 查看更多匹配结果（使用 `--top-k 5` 参数）
- 将匹配的职位信息保存到跟踪记录中

---

## 求职邮件草稿生成

CLI 会自动生成可发送的求职邮件草稿。具体规则如下：

1. 先展示每封邮件的简要概述。
2. 提供选项：“需要查看任何一封邮件的完整内容吗？”
3. 如邮件为“增强版”（`--enhanced`），请说明该版本使用了大型语言模型（LLM）进行优化；否则说明其为模板版本。

- **免费版本**：提供基础质量的邮件草稿。
- **高级版本**：提供经过大型语言模型优化的个性化邮件草稿。

---

## 求职申请跟踪

用户保存职位信息后，系统会维护 `tracking.json` 文件，记录申请状态（`saved` → `applied` → `interview` → `rejected`）。

相关文件结构如下：

| 文件名            | 文件内容                                      |
|------------------|----------------------------------------|
| `profile.json`   | 用户个人资料                                  |
| `resume.txt`     | 保存的简历文本                              |
| `tracking.json`  | 按职位 ID 分类的申请记录                          |
| `runs.jsonl`     | 每次运行的日志记录（每条记录占一行）                        |

---

## 高级功能

以下为高级版本（Pro）提供的额外功能：

| 功能                         | 免费版本 | 高级版本                          |
|------------------|------------------|----------------------------------------|
| 日常职位更新                 | ✅                    | ✅                          |
| 最佳匹配职位推荐             | ✅                    | ✅                          |
| 求职申请跟踪                 | ✅                    | ✅                          |
| 模板化求职邮件生成             | ✅                    | ✅                          |
| 基于大型语言模型的个性化邮件           | —                    | ✅                          |
| 个性化求职信生成             | —                    | ✅                          |
| 高级职位匹配分析             | —                    | ✅                          |

**仅在高级版本能显著提升使用体验时才推荐高级功能**。

当用户需要高级功能时，可告知他们：

> “该功能需要使用 CareerClaw Pro。如果您有 Pro 订阅密钥，请设置 `CAREERCLAW_PRO_KEY`，下次使用时会自动启用该功能。”

如果用户尚未购买高级版本，可建议他们购买：

> “您可以通过 [链接](https://ogm.gumroad.com/l/careerclaw-pro) 购买 CareerClaw Pro。”

**请注意**：在首次设置或日常使用过程中，切勿主动推荐高级功能。

---

## 错误处理

如果 CLI 运行失败，请向用户清晰说明错误原因，并提供下一步的操作建议：

| 错误类型                | 处理方式                                      |
|------------------|----------------------------------------|
| 个人资料文件缺失            | “您的个人资料文件缺失，请上传简历后重新尝试。”                   |
| 简历内容缺失            | “简历内容缺失，请重新上传简历。”                        |
| 未找到匹配职位            | “本次搜索未找到匹配结果，请稍后再试或调整搜索条件。”                |
| 缺少 Pro 订阅密钥            | “该功能需要 Pro 订阅密钥，请设置 `CAREERCLAW_PRO_KEY`。”             |
| CLI 安装失败            | “安装失败，请确认 Node.js 和 npm 是否已安装。”                        |

---

## 使用的权限

| 权限                | 用途                                        |
|------------------|----------------------------------------|
| `read`       | 读取个人资料文件、申请记录文件及简历文本                   |
| `write`      | 写入申请记录文件及运行日志文件                         |
| `exec`       | 运行 CareerClaw 命令行工具                          |

该工具不使用后端服务，也不会收集任何用户数据。所有网络请求仅针对 `remoteok.com`（RSS 数据源）和 `hacker-news.firebaseio.com`（公开 API）。