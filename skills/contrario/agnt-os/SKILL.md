---
name: AGENT-OS
version: 1.0.3
author: contrario
homepage: https://clawhub.ai/contrario
license: MIT
description: 这是用于AI代理的操作系统层：它将目标任务分配给相应的技能（即相应的功能或模块），并在执行过程中设置检查点（即关键步骤或里程碑），以确保任务的顺利进行。
metadata:
  openclaw:
    operator_note: Instruction-only skill. No file access, no code execution, no external APIs. All cognition happens in-context.
    domains_not_recommended:
      - medical-diagnosis
      - legal-advice
      - financial-advice
---
# AGENT-OS

这是用于AI代理的操作系统层。

它将您的目标引导至相应的技能，并在执行过程中设置检查点（即关键步骤的监控点），最后验证执行结果。

*AGENT-OS v1.0.3，由@contrario开发*