---
name: viral-app
description: 使用 `viral.app` API，通过带有本地命令行界面（CLI）的代理工具，可以进行账户分析、跟踪视频/账户信息、项目管理、创作者中心（Creator Hub）操作以及实时数据操作。
metadata: {"homepage":"https://github.com/fmd-labs/viral-app-skills"}
---
# viral-app

当您需要通过 viral.app API 读取或管理数据时，请使用此技能。

## 使用场景

- 查询分析数据（账户信息、视频内容、关键绩效指标 KPI、数据导出结果）。
- 管理被跟踪的实体（账户、视频、排除项、数据刷新操作）。
- 管理项目及创作者中心资源。
- 获取实时平台数据（TikTok、Instagram、YouTube）。

## 快速入门

1. 确保已安装 `viral-app` CLI，并将其添加到系统路径 `PATH` 中。

```bash
viral-app --help
```

2. 设置 API 密钥：

```bash
export VIRAL_API_KEY="..."
```

您可以从 viral.app 的仪表板中的“设置 -> API 密钥”处获取该密钥。

3. 验证访问权限：

```bash
viral-app accounts-list --per-page 1
```

除非已经传递了相应的请求头信息，否则该工具会自动从 `VIRAL_API_KEY` 变量中获取 `x-api-key` 并将其添加到请求中。

## 需要首先提供的输入参数

- 任务类型：读取/报告数据或修改/管理资源。
- 组织范围内的标识符：`orgacc_*`、`orgproj_*`；在相关情况下还需提供创作者/活动/支付信息的标识符。
- 平台和实体标识符（`tiktok|instagram|youtube`、平台账户/视频 ID）。
- 时间范围（用于分析任务的参数：`--date-range[from]`、`--date-range[to]`）。
- 分页参数/筛选条件（`--per-page`、`--filters`），以控制输出结果的范围和内容。

## 命令参考

查看可用的操作：

```bash
viral-app --help
viral-app <command> --help
```

常见的读取操作：

```bash
viral-app accounts-list --per-page 10
viral-app videos-list --per-page 10
viral-app analytics-get-kpis
viral-app analytics-top-videos --per-page 10
viral-app integrations-apps-list
```

常见的修改操作：

```bash
viral-app projects-create --body '{"name":"My Project"}'
viral-app accounts-tracked-refresh --body '{"accounts":["orgacc_..."]}'
viral-app projects-add-to-account --body '{"projectId":"orgproj_...","accountId":"orgacc_..."}'
```

## 安全规则

- 在执行 `POST`、`PUT`、`PATCH` 或 `DELETE` 操作之前，请确认用户的操作意图是否正确。
- 在执行任何修改操作之前，请运行 `<command> --help` 命令以核实所需的参数和请求格式。
- 在进行大规模数据导出之前，建议先使用精确的查询条件（如分页参数、筛选条件、时间范围）。
- 默认情况下，输出结果为机器可读的 JSON 格式；只有在用户明确要求时才转换输出格式。

## 故障排除

- 错误代码 `401 UNAUTHORIZED`：表示 API 密钥缺失或无效，请检查 `VIRAL_API_KEY` 的值，或确保请求头中包含了正确的 `x-api-key`。
- 错误代码 `401` 也可能表示 API 密钥已过期或被撤销，或者请求的上下文不正确。
- 错误代码 `429` 表示请求被拒绝，建议稍后重试；请检查响应头中的 `Retry-After` 等字段。
- 如果 `data` 数组为空，请检查筛选条件、项目/账户 ID 以及时间范围设置是否正确。
- 严禁在代码提交中泄露 API 密钥；在共享代码用于测试后，请定期更换 API 密钥。

## 默认设置

- 输出格式默认为 JSON（除非通过 `RSH_OUTPUT_FORMAT=json` 参数进行更改）。
- 自动分页功能默认处于禁用状态（`RSH_NO_PAGINATE=true`），以确保脚本执行的稳定性。
- 读取数据后默认会汇总关键指标；修改数据后请明确说明可能产生的写操作影响。