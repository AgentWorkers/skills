---
name: securityclaw-skill
description: **OpenClaw：以安全为首要原则的技能审核与隔离机制**  
该机制适用于新技能的安装、来自未知来源的技能审核、检测技能是否存在命令注入、数据泄露或供应链风险等安全威胁的情况，以及当机器人怀疑某技能具有恶意行为时。该系统支持静态检查以及可选的沙箱测试功能，能够对可疑技能进行隔离，并生成供所有者处理的操作清单（包括删除、报告、允许使用或重新扫描等选项）。
---

# SecurityClaw（技能扫描器）

## 使用扫描脚本

默认情况下，扫描器以只读模式运行：

```bash
python3 scripts/securityclaw_scan.py --skills-dir ~/.openclaw/skills --out report.json
```

将任何可疑的文件或文件夹隔离（仅进行隔离，不进行删除）：

```bash
python3 scripts/securityclaw_scan.py --skills-dir ~/.openclaw/skills --quarantine-dir ~/.openclaw/skills-quarantine --quarantine --out report.json
```

## 发现问题时的处理方式

如果报告中的任何技能的严重性（severity）被评为“高”（high）：

1) **不要执行**该技能。
2) **将**该技能所在的文件夹**隔离**。
3) **通知所有者**，并提供以下信息：
   - 技能名称
   - 主要问题所在的位置（文件/代码行）
   - 建议采取的措施
4) 等待所有者的指示：
   - **删除**：移除被隔离的技能
   - **报告**：准备公开报告或入侵事件通知（IOCs，确保不泄露任何机密信息）
   - **允许使用**：将该技能添加到允许使用的列表中并恢复其正常使用
   - **全面扫描**：对所有内容进行深度扫描

## 可选功能：沙箱环境/动态检查（高级选项）

动态检查为可选功能，需在所有者批准后才能执行。

建议在以下条件下运行未知代码：
- 代码不允许访问外部网络
- 文件系统仅支持只读操作（临时工作区除外）
- 代码无法访问 OpenClaw 的配置文件或敏感信息

详细信息请参阅 `references/sandboxing.md`。

## 相关文件

- `scripts/securityclaw_scan.py` — 主扫描脚本及隔离功能
- `references/rules.md` — 规则集（说明哪些行为会被标记为可疑以及原因）
- `references/sandboxing.md` — 安全的沙箱使用策略及应避免的操作