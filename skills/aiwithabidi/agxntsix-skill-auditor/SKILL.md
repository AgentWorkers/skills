---
name: skill-auditor
description: **第三方 OpenClaw 技能的安全审计与隔离系统**  
用于在评估、审查或安装来自 ClawHub 或外部来源的任何技能时使用。该系统会在任何技能安装之前自动触发。
---

# 技能审核器

这是一个用于审核第三方技能安装的安全机制。**任何技能在未通过审核之前都不会被安装。**

## 使用场景

- 在从 ClawHub 或外部来源安装任何技能之前
- 当需要审查/评估某个技能的安全性时
- 当收到 `clawhub install` 或类似的安装请求时

## 审核流程

### 1. 先进行隔离
切勿直接将技能复制到生产环境的技能目录中。务必先进行隔离：

```bash
bash skills/skill-auditor/scripts/quarantine.sh /path/to/skill-source
```

该步骤会将技能复制到一个临时目录中，执行全面的审核，只有当风险评分为“CLEAN”或“LOW”时才会允许安装。

### 2. 手动审核（直接使用 Python 脚本）
对于不需要隔离处理的审核操作：

```bash
python3 skills/skill-auditor/scripts/audit_skill.py /path/to/skill-dir
```

审核结果会以 JSON 格式输出到标准输出（stdout）。若需要格式化的文本输出，请添加 `--human` 参数。

### 3. 解读审核结果

| 评分 | 处理方式 |
|--------|--------|
| CLEAN | 可以安全安装 |
| LOW | 安全，但有少量需要注意的问题——请简要查看审核结果 |
| MEDIUM | **禁止安装**——需要手动审查每个问题 |
| HIGH | **立即阻止安装**——检测到恶意行为 |
| CRITICAL | **立即阻止安装**——存在明显的威胁迹象（如数据泄露、命令注入、混淆的负载等） |

### 4. 返回代码

- `0` = CLEAN 或 LOW（安全）
- `1` = MEDIUM（需要进一步审查）
- `2` = HIGH 或 CRITICAL（被阻止）

## 审核内容

- 所有文件：文件清单、文件大小、可疑文件类型
- 代码：shell 命令、网络请求、环境变量访问、文件系统逃逸机制、代码混淆、动态导入
- SKILL.md：命令注入模式、权限请求
- 依赖项：`requirements.txt` 或 `package.json` 中标记的依赖包
- 编码：base64 编码的负载、十六进制/Unicode 转义、字符串操作技巧

## 参考资料

- `references/known-patterns.md` — ClawHub 收录的真实攻击模式库
- `references/prompt-injection-patterns.md` — 用于检测命令注入的签名模式

## 重要提示

如果技能的评分达到 MEDIUM 或更高，**在采取任何行动之前，务必将所有审核结果展示给 Abidi**。切勿绕过审核机制。这是防止未经信任的代码进入系统的最后一道防线。