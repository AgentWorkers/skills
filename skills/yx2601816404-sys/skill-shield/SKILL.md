---
name: skill-shield
version: 0.6.1
description: "**ClawHub 技能的安全审计工具**  
该工具用于对技能目录进行安全审计，具备 65 种检测模式、反混淆分析功能以及双评级系统（安全性 + 合规性）。版本 v0.6.1 通过跳过 `venv` 和 `node_modules` 目录来提升批量扫描的性能。适用场景包括：安装新技能时进行安全检查、审查技能的安全性，或审计权限设置。"
---
# Skill Shield v0.6.1 — 安全审计工具

该工具可扫描任何技能目录，检测其中的权限设置和潜在危险模式，并在安装前提供安全评级。

## 使用方法

在需要扫描的技能目录上运行该工具：

```bash
python3 scripts/scan.py /path/to/skill-directory
```

### SARIF 输出格式（兼容 GitHub Code Scanning）

```bash
python3 scripts/scan.py /path/to/skill-directory --sarif
```

### 输出结果

脚本会将结果输出到标准输出（stdout）中，包含两部分内容：
1. 一个 JSON 格式的报告（位于 `--- JSON START ---` 和 `--- JSON END ---` 之间）
2. 一个 Markdown 格式的报告（位于 `--- MD START ---` 和 `--- MD END ---` 之间）

### 保存报告

脚本会在输出目录中生成 `report.json` 和 `report.md` 两个文件。

## 安全评级

| 评级 | 含义 | 处理建议 |
|-------|---------|--------|
| A | 安全 | 可自由安装 |
| B | 低风险 | 存在轻微问题，总体安全 |
| C | 需要审查 | 安装前请检查被标记的模式 |
| D | 高风险 | 检测到严重危险模式 |
| F | 危险 | 未经彻底人工审查请勿安装 |

## 检测能力（涵盖 65 种模式，11 个类别）

- 文件删除：`rm -rf`、`shred`、`unlink`、`rmtree`、`rimraf`、`del /f`（7 种模式）
- 网络数据泄露：`curl POST`、`wget --post`、`requests.post`、`fetch POST`、`netcat`、反向 shell、DNS 数据泄露、数据通过管道传输给 `curl`、`socat`（9 种模式）
- 环境变量访问：`process.env`、`os.environ`、`.env` 文件、`printenv`（5 种模式）
- 秘密信息/密钥访问：`.ssh/`、`.gnupg/`、私钥、钱包文件、令牌、密码、密钥链、云服务凭证（8 种模式）
- 权限提升：`sudo`、`su`、`chmod 777`、`chown`、`setuid/setgid`、`doas`（6 种模式）
- 代码执行：`eval`、`exec()`、`Function()`、`child_process`、`subprocess`、`os.system`、`os.popen`、`compile`（8 种模式）
- 数据收集：`/etc/passwd`、`/etc/shadow`、`whoami`、`hostname`、`ifconfig`、`/proc/self`（6 种模式）
- 持久化设置：`crontab`、`systemd`、`rc.local`、shell 配置文件修改、自动启动设置（5 种模式）
- 遮蔽技术：长字符串的 Base64 编码、十六进制转义、字符串反转（5 种模式）
- 加密货币/挖矿：`xmrig/minerd`、矿池 URL、钱包地址（3 种模式）
- Shell 注入：反引号执行、数据通过管道传输给 Shell、下载后执行（3 种模式）

## 主要特性

### 权限声明审计（Skill Shield 的独特功能）
- 比较 `SKILL.md` 中声明的工具与实际代码中使用的工具；
- 识别未声明的权限（并给出风险评分 1-5 分）；
- 识别未使用的声明权限；
- 统计工具的声明覆盖率；
- 为每种工具提供风险建议。

### 反隐蔽技术分析
- 自动解码 Base64 和十六进制编码的内容，然后重新扫描解码后的结果以检测危险模式；
- 对被发现的隐蔽技术行为提高风险等级。

### 基于上下文的误报减少机制
- 注释和文档字符串：降低风险等级 2 分；
- `SKILL.md` 中的 Markdown 代码块：降低风险等级 2 分（仅包含示例代码，非实际执行代码）；
- 扫描器源代码中的模式定义行：完全忽略；
- 报告中会显示原始风险等级和调整后的风险等级（例如：“低风险（2→4）”。

### CWE 参考
- 每个检测模式都包含 CWE（Common Weakness Enumeration）参考编号，用于专业漏洞分类。

## v0.6.0 — 批量扫描模式

- 使用 `--batch` 参数可一次性扫描目录中的所有技能：

```bash
python3 scripts/scan.py /path/to/skills/ --batch
python3 scripts/scan.py /path/to/skills/ --batch --json-summary
python3 scripts/scan.py /path/to/skills/ --batch --json-summary -o /path/to/output
```

### 性能优化
- 自动跳过 `venv`、`node_modules`、`dist`、`.git` 目录；
- 每个技能最多扫描 200 个脚本文件以确保安全性；
- 扫描 164 个技能仅需约 8 秒。

### 输出格式
- 默认输出为包含统计信息和每个技能评级的 Markdown 表格；
- 使用 `--json-summary` 选项时，输出 JSON 格式的摘要；
- 使用 `-o` 选项时，生成 `batch-summary.json` 文件。

## v0.5.0 — SARIF 输出格式

- 新增 `--sarif` 参数，支持 SARIF 2.1.0 格式输出，兼容以下工具：
- GitHub Code Scanning（`upload-sarif` 功能）
- VS Code 的 SARIF 查看器扩展
- SARIF Web 查看器

```bash
python3 scripts/scan.py /path/to/skill --sarif > report.sarif
python3 scripts/scan.py /path/to/skill --sarif -o /path/to/output
```

### SARIF 的详细信息
- 所有 65 种检测模式的完整规则定义；
- CWE 分类参考（MITRE CWE 4.14 标准）；
- 为避免重复检测提供部分特征信息；
- 安全风险等级（2.0-10.0 分）；
- 扫描结果中包含 Skill Shield 的元数据（评级和推荐建议）。

## v0.4.0 — 误报修复

- 安全工具中的字符串字面量（如正则表达式或常量）不再被误判为危险代码；
- 扫描器现在能识别 `rm -rf` 或 `curl POST` 等命令是否出现在字符串字面量（引号、正则表达式、数组）中，并相应降低风险等级。

### 忽略下一行的功能
- 在需要忽略的行前添加 `# skill-shield: ignore-next-line` 可忽略后续的检测结果；
- 适用于已知安全的工具。

### 扫描结果示例
- 5 个安全审计工具的评级从 F 升级为 A/C/D（`agents-skill-security-audit`、`ai-skill-scanner`、`skulk-skill-scanner`、`aoi-prompt-injection-sentinel`、`aoi-sandbox-shield-lite`）；
- 已知安全的技能未出现任何问题（无回归）。

## v0.3.0 — 双重评级系统

- **安全评级**：仅基于可执行文件中发现的危险代码模式；
- **合规评级**：基于权限声明的完整性（`SKILL.md` 是否准确反映了代码中使用的工具）。

### 综合建议
- 根据两种评级给出安装建议：
  - **install**：安全等级 A/B，合规性 A/B；
  - **install_with_review**：代码安全但权限未声明（可能文档不完善，但无恶意行为）；
  - **review_required**：检测到安全问题；
  - **do_not_install**：存在严重安全风险；
  - **documentation_only**：仅包含文档信息，无可执行代码。

### 误报修复（v0.3.0）
- JavaScript 模板字面量（反引号）不再被误判为 Shell 执行命令；
- 变量名（如 `hostname`、`whoami`）不再被误判为命令；
- Shell 脚本中的常规 `$VAR` 使用方式不再导致误报；
- `os.environ.get("KEY")` 和 `process.env.KEY` 的调用方式降低了风险等级（符合行业标准）；
- 使用 `--disable-setuid-sandbox` 选项后，相关评分从高风险降为中等风险；
- 仅包含文档信息的技能被评为 N/A（而非 A 等级）。

## 退出代码

| 代码 | 评级 | 含义 |
|------|---------|---------|
| 0 | A, B | 可安全安装 |
| 1 | C, D | 建议审查 |
| 2 | F | 请勿安装 |

## 帮助信息
如有任何问题，请发送消息：`0x6c730bDcfC762e23cE53aD991B75ab9852e87806`（联系方式）
- Moltbook：https://www.moltbook.com/u/Yuqian
- Twitter：@Yuqian0202