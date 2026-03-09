---
name: codesmith
description: CodeSmith——用于配置高级工程代理的工具。它支持全栈开发自动化、持续集成/持续交付（CI/CD）流程、GitHub工作流以及来自实际生产编码工作的最佳实践与经验。特别适用于那些负责发布代码的OpenClaw代理。
metadata:
  {
    "claw_mentor":
      {
        "mentor": "codesmith",
        "specialty": "Full-stack dev automation — CI/CD, code review, GitHub workflows, ACP dispatch",
        "minimum_skill_version": "2.1.0",
        "package_files":
          [
            "CLAW_MENTOR.md",
            "AGENTS.md",
            "working-patterns.md",
            "skills.md",
            "cron-patterns.json",
            "privacy-notes.md",
            "setup-guide.md"
          ]
      }
  }
---
# CodeSmith — 指导者包（Mentor Package）

**专长：** 全栈开发自动化——持续集成/持续交付（CI/CD）、代码审查、GitHub工作流程、ACP调度  
**版本：** 1.0.0  
**适用对象：** 执行实际编码任务的OpenClaw代理（负责实现功能、管理代码仓库以及向子代理分配任务）

---

## 该包包含的内容

此指导者包由`claw-mentor-mentee`技能使用，用于教导订阅者的代理如何高效地进行编码工作。  

| 文件 | 主要内容 |
|------|----------------|
| `AGENTS.md` | 带注释的配置文件——包含17个注释块，解释每个非显而易见配置决策的背后的原因 |
| `working-patterns.md` | 日常编码规范、ACP调度模式、信任关系建立流程、5个真实的失败案例 |
| `skills.md` | 分为三个级别的技能体系；明确列出未安装的技能及其原因 |
| `cron-patterns.json` | 5个 cron 作业及其使用指南（建议逐一启用） |
| `privacy-notes.md` | 明确的读写权限及网络访问规则 |
| `setup-guide.md` | 逐步引导用户了解如何设置系统，包含信任关系建立的时间线 |
| `CLAW_MENTOR.md` | 包含完整包的清单以及风险评估和兼容性说明 |

---

## 适用人群

适合将OpenClaw作为编码辅助工具的开发者，希望该工具能提升代理的自主性、判断力，并减少意外情况的发生。  
**前提条件：**  
- 拥有已配置`gh` CLI的GitHub账户  
- 使用Vercel或类似的服务进行代码托管  
- 已启用ACP（Automatic Code Placement）功能以支持子代理的任务调度  
- 对代理的自主操作有一定了解（在建立信任关系后）  

**不适用场景：**  
- 需要人工审核每一处代码变更的场景；  
- 仅涉及非技术性工作流程的场景。  

---

## 应用方式

该包会由`claw-mentor-mentee`技能（版本2.1.0及以上）在预定的更新周期内自动应用。  
**建议操作：**  
在启用任何cron作业之前，请先进行手动审核——具体步骤请参考`setup-guide.md`中的逐步指南。  

---

## 关于CodeSmith  

CodeSmith是基于实际生产环境中的经验开发的：  
- 实现API接口；  
- 调试部署流程；  
- 管理GitHub工作流程；  
- 派遣代理执行编码任务；  
- 从生产环境中的故障中吸取经验教训。  
- `working-patterns.md`中的失败案例均为真实案例；  
- `cron-patterns.json`中的调度时间表为实际运行过的设置；  
- 信任关系的建立过程也与实际操作一致。  
这些特点使得CodeSmith具有极高的实用价值。