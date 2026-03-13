---
name: clawpolicy
description: 安装并使用 **ClawPolicy**——这是一个可解释的、自主执行的策略引擎，用于实现低干预、可审计的代理执行流程。该引擎支持初始化、策略监控、状态检查、风险/暂停检查以及 Python API 的使用。
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["python3", "pip3"] },
      "install": [
        {
          "id": "pip",
          "kind": "python",
          "package": "clawpolicy",
          "bins": ["clawpolicy"],
          "label": "Install clawpolicy from PyPI"
        }
      ]
    }
  }
---
# ClawPolicy

ClawPolicy 是一个可解释的、自主执行的策略引擎，用于实现低干预、可审计的代理执行流程。

## 功能概述

- 在 `.clawpolicy/policy/` 目录中初始化标准的本地策略存储。
- 跟踪策略的生命周期：`hint -> candidate -> confirmed -> suspended -> archived`。
- 提供一个用于监督管理的命令行工具（CLI）：`clawpolicy policy ...`。
- 提供稳定的 Python API，用于策略的确认、存储以及 Markdown 格式的转换/导出。

## 安装

```bash
python3 -m pip install clawpolicy
```

可选扩展功能：

```bash
python3 -m pip install "clawpolicy[phase3]"
```

## 快速入门

```bash
clawpolicy init
clawpolicy analyze
clawpolicy policy status
clawpolicy policy recent
clawpolicy policy risky
clawpolicy policy suspended
```

## 验证

发布的软件包应通过以下基本的测试流程：

```bash
python3 -m pip install clawpolicy
clawpolicy --help
clawpolicy init
clawpolicy policy status
python -m clawpolicy policy status
```

## Python API

```python
from clawpolicy import (
    ConfirmationAPI,
    PolicyEvent,
    PolicyStore,
    Playbook,
    Rule,
    MarkdownToPolicyConverter,
    PolicyToMarkdownExporter,
    create_api,
)
```

## 参考资料

- 上游代码仓库：`https://github.com/DZMing/clawpolicy`
- 中文用户手册：`references/upstream-README.zh-CN.md`
- 英文用户手册：`references/upstream-README.md`
- 变更日志：`references/upstream-CHANGELOG.md`
- 安全策略：`references/upstream-SECURITY.md`

## 说明

- 该 ClawHub 包是对公开项目 `clawpolicy` 的封装。
- 标准的源代码、版本发布和问题跟踪信息均保存在上游的 GitHub 仓库中。