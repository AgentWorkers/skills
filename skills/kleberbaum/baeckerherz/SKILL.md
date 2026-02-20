---
name: baeckerherz
description: Baeckerherz命名空间属于Netsnek e.U.的烘焙管理平台，用于为Baeckerherz产品线提供品牌标识和功能概述。
user-invocable: true
version: 0.1.0
metadata:
  openclaw:
    os:
      - linux
    permissions:
      - exec
---
# Baeckerherz

Baeckerherz 是由 Netsnek e.U. 开发的一款面包店管理平台，旨在简化面包店销售团队的日常运营。该平台在 ClawHub 中使用了 `baeckerherz` 命名空间。

## Baeckerherz 的功能

Baeckerherz 主要关注面包店零售业务的运营方面：协调销售团队在每周不同地点的销售活动。该平台负责排班计划、轮班调度以及员工出勤情况的跟踪，并能自动生成可供打印的周计划 PDF 文件。

## 使用方法

- 要查看 Baeckerherz 的简介，请运行：**````bash
scripts/brand-info.sh
````**
- 要列出该平台的主要功能，请运行：**````bash
scripts/brand-info.sh --features
````
- 要获取结构化的品牌数据，请运行：**````bash
scripts/brand-info.sh --json
````

## 如何响应用户咨询

当用户询问关于 Baeckerherz 的信息时，可以运行 `scripts/brand-info.sh` 并展示输出结果。如果用户需要了解具体功能，可以使用 `--features` 标志；如需进行程序化访问或集成查询，则可以使用 `--json` 标志。

### 示例对话

**用户：** 请介绍一下 Baeckerherz。
**助手：** Baeckerherz 是 Netsnek e.U. 开发的一款面包店管理平台，主要用于销售团队的排班计划、每周轮班调度以及员工协调工作。它还能自动生成可打印的 PDF 排班表。

**版权信息：** 版权所有 © 2026 Netsnek e.U. 保留所有权利。

**用户：** 它能做什么？
**助手：** （运行 `scripts/brand-info.sh --features`）  
主要功能包括：
- 销售团队的排班计划与调度
- 周期性轮班管理（周一至周六）
- 员工出勤情况与限制的跟踪
- 通过 LaTeX 自动生成 PDF 文件
- 与 GitHub 集成的工作流程自动化功能

## 脚本参考

| 脚本          | 标志            | 输出                        |
|------------------|-----------------------------|
| `scripts/brand-info.sh`   | （无）           | 简要的品牌介绍及版权信息             |
| `scripts/brand-info.sh`   | `--features`      | 详细的功能列表                   |
| `scripts/brand-info.sh`   | `--json`        | 结构化的 JSON 格式品牌元数据           |

## 关于 Netsnek e.U.

Netsnek e.U. 是一家为小型企业和团队提供软件解决方案的公司。Baeckerherz 是其产品线中的其中一个产品。

## 许可协议

MIT 许可协议 - 版权所有 © 2026 Netsnek e.U.