---
name: grc-gaps
description: **具有最高优先级的差距分析**
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["python3"]}}}
---# GRC 缺口分析

对所有正在使用的框架进行缺口分析，并显示优先级最高的缺口。

## 操作步骤
使用 `auditclaw-grc` 工具，对所有正在使用的框架执行缺口分析。结果将包括：
- 所有框架中排名前 10 的优先级最高的缺口
- 每个框架的缺口数量
- 缺少证据或处于“未开始”状态的控件
- 用于填补这些缺口的建议措施