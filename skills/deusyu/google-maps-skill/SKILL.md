---
name: gmaps
description: 通过脚本直接连接到 Google Maps Platform API，可以执行地理编码、逆地理编码、路线规划、地点搜索、地点详情查询、海拔查询以及时区查询等功能。这些功能适用于用户需要使用“Google Maps 查询”、“国际路线规划”或“地点搜索”的场景，同时也适用于需要通过命令行脚本调用 Google Maps API 的情况。
---
# Google Maps 技能

## 快速入门
1. 确保已设置 `GOOGLE_MAPS_API_KEY`。
2. 在该技能目录中运行 `bun scripts/gmaps.ts --help` 命令。
3. 从 `references/command-map.md` 文件中选择相应的命令。

## 工作流程
1. 验证用户意图并选择一个命令。
2. 坐标使用 **lat,lng** 的顺序（符合 Google 的规范）。
3. 将输出结果保留为原始的 Google Maps JSON 格式，不要对字段进行包装。
4. 将任何 API 业务错误视为失败。

## 命令
- 完整的命令映射：`references/command-map.md`
- 可直接运行的示例：`references/examples.md`

## 注意事项
- 该技能以脚本为主，不依赖于 MCP 服务器。
- 仅支持 `GOOGLE_MAPS_API_KEY`。