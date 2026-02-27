---
name: ai-csuite
description: 该工具为SaaS团队提供了一个基于脚本的AI驱动的战略辩论平台。它能够根据辩论场景动态生成参与者的名单，设计结构化的辩论流程，汇总辩论结果，并生成包含决策建议及行动计划的CEO报告。此外，该工具还配备了专门用于确保安全性的脚本，确保内容能够通过VirusTotal的安全检测机制进行顺利分发。
license: MIT
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
metadata:
  version: 2.0.0
  mode: prompt-plus-scripts
  runtime: python3-stdlib
---
# AI C-Suite 多智能体框架

当用户需要在产品、工程、定价、市场推广、招聘、运营或竞争应对等方面做出战略决策时，可以使用此技能。

用户的讨论主题为：**$ARGUMENTS**

## 运行时契约

该技能通过 `scripts/` 目录下的本地脚本进行操作：
- `prepare_session.py`：验证公司背景和阶段信息，构建会议数据包
- `run_debate.py`：生成多轮辩论并生成 CEO 的决策结果
- `validate_output.py`：验证所需的输出内容和字段
- `security_scan.py`：检查代码中是否存在可能影响发布的可疑模式

该技能不涉及任何隐藏的网络操作、数据混淆或凭证读取。

## 必需输入

从以下文件中加载公司背景信息：
- `config/company.yaml`

如果文件缺失，请向用户询问以下信息：
- 公司名称 + 产品线
- 发展阶段：`solo | pre-seed | seed | series-a`
- 年收入（ARR）或月收入（MRR）
- 团队规模
- 约束条件列表

## 阶段配置

| 阶段 | 参与辩论的智能体 | 轮数 |
|---|---|---|
| solo | CEO、CTO、CPO、CFO、CoS | 2 |
| pre-seed | CEO、CTO、CPO、CoS、CV | 2 |
| seed | CEO、CTO、CPO、CMO、CRO、CoS、CV | 3 |
| series-a | CEO、CTO、CPO、CFO、CMO、CRO、COO、CSA、CISO、CoS、CV | 3 |

始终参与数据汇报的智能体包括：
- `CV`：负责收集客户反馈
- `CFO`：负责财务方面的约束条件

如果某个阶段的辩论名单中缺少 `CV` 或 `CFO`，他们仍会提供预讨论阶段的数据。

## 小组构成

| 小组 | 成员 | 组长 |
|---|---|---|
| 战略小组 | CEO、CFO、COO、CoS | CFO |
| 产品小组 | CTO、CPO、CSA、CISO | CPO |
| 成长小组 | CMO、CRO、CV | CRO |

小组内部的讨论直接进行；跨小组的讨论由 CoS 调解。

## 执行步骤

1. 安全性预检查：
```bash
python3 scripts/security_scan.py .
```

2. 构建会议数据包：
```bash
python3 scripts/prepare_session.py --topic "$ARGUMENTS" --company-file config/company.yaml
```

3. 进行多轮辩论：
```bash
python3 scripts/run_debate.py --topic "$ARGUMENTS" --company-file config/company.yaml --output logs/latest-decision.md
```

4. 验证输出内容的完整性：
```bash
python3 scripts/validate_output.py --file logs/latest-decision.md
```

5. 向用户展示结果，并询问用户以下选项：
- 同意当前结果
- 对结果提出质疑
- 在调整约束条件的情况下重新进行辩论

## 辩论流程

辩论必须严格按照以下顺序进行：
1. 预讨论阶段（`CV` 和 `CFO` 提供数据汇报）
2. 第一轮：各智能体独立表达观点（每轮3-5句话）
3. 可选的人工审核环节
4. 第二轮：反驳和质疑（每轮3-5句话）
5. 第三轮：观点趋同（仅限三轮辩论的阶段）
6. CoS 将各小组的观点汇总并提交给 CEO
7. CEO 根据讨论结果做出决策，并指定具体执行负责人

## 必须包含的输出内容

最终输出必须包括以下内容：
- **数据汇报（预讨论阶段）**
- **CEO 的决策摘要**
- **CEO 的最终决策**
- **决策理由**
- **决策过程中考虑的因素**
- **被否决的选项**
- **后续行动方案**
- **需要进一步审查的议题**
- **决策的信心程度**
- **决策的可逆性**

## 升级规则

必须严格遵守以下规则：
1. CEO 的决策摘要中必须包含 CISO 关于法律/合规风险的评估
2. 如果公司的收入预测（ARR/MRR）在6个月内存在风险，必须明确说明风险的严重程度
3. 如果 `CV` 的观点与团队共识相矛盾，必须在报告中予以体现
4. 如果辩论结束后出现僵局，必须向用户展示双方的观点
5. 如果有观点发生根本性转变，必须予以标记

## 质量控制措施

1. 第一轮辩论中不能出现所有智能体都达成一致的情况
2. 建议必须具体明确，不能含糊其辞
3. 所有的观点都必须与相关角色的职责或公司背景相关
4. CEO 必须说明决策中的权衡因素
5. 如果团队在早期就达成共识，CoS 必须调查是否存在群体思维现象

## 系统安全性保障

系统的安全性要求如下：
- 仅使用纯文本格式（markdown）和 Python 代码
- 不允许使用编码数据或运行时解码
- 禁止使用 `eval`、`exec` 或 shell 注入等行为
- 系统仅允许在 `config/` 和 `logs/` 目录中进行本地读写操作

## 兼容性

- 该技能可通过 `.claude/skills/` 目录与 Claude 代码集成
- 支持 `SKILL.md` 格式的 OpenSkills 工具也能使用该技能