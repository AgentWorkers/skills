---
name: mcd-cn
description: 通过 `mcd-cn` CLI 查询麦当劳中国的 MCP 服务器，以获取活动日历、优惠券信息以及自动领取功能的相关数据。该工具既适用于人工查询优惠券，也适用于将查询结果以 JSON 格式输出供脚本使用。
homepage: https://github.com/ryanchen01/mcd-cn
metadata: {"clawdbot":{"emoji":"🍟","requires":{"bins":["mcd-cn"],"env":["MCDCN_MCP_TOKEN"]},"primaryEnv":"MCDCN_MCP_TOKEN","install":[{"id":"brew","kind":"brew","formula":"ryanchen01/tap/mcd-cn","bins":["mcd-cn"],"label":"Install mcd-cn (brew)"}]}}

---

# mcd-cn

这是 McDonald's China 的 MCP 命令行工具（CLI）。默认情况下，工具会以人类可读的格式输出结果；若需要以 JSON 格式获取数据，可使用 `--json` 参数。

## 安装

- 使用 Homebrew：`brew install ryanchen01/tap/mcd-cn`

## 配置

- 必需配置 `MCDCN_MCP_TOKEN`，该 token 可从 McDonald's China 的 MCP 控制台获取。
- 可选配置 `MCDCN_MCP_URL`，用于指定自定义服务器地址。

## 常用命令

- 查看活动日历：`mcd-cn campaign-calender`
- 查看指定日期的活动日历：`mcd-cn campaign-calender --specifiedDate 2025-12-09`
- 查看可用优惠券：`mcd-cn available-coupons`
- 自动领取优惠券：`mcd-cn auto-bind-coupons`
- 查看我的优惠券：`mcd-cn my-coupons`
- 查看当前时间：`mcd-cn now-time-info`
- 以 JSON 格式输出数据：`mcd-cn available-coupons --json`

## 注意事项

- Token 可通过 `MCDCN_MCP_TOKEN` 环境变量或 `.env` 文件进行设置。
- `--specifiedDate` 参数的日期格式为 `yyyy-MM-dd`。
- 每个 Token 每分钟的请求次数限制为 600 次。