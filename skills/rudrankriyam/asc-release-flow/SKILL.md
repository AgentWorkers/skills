---
name: asc-release-flow
description: 使用 `asc publish`、`builds`、`versions` 和 `submit` 命令来实现 TestFlight 和 App Store 的端到端发布工作流程。当需要上传构建版本、将其分发到 TestFlight 或提交到 App Store 时，请使用这些命令。
---

# 发布流程（TestFlight 和 App Store）

当您需要将新的构建版本上传到 TestFlight 或提交到 App Store 时，请使用此技能。

## 前提条件
- 确保已设置凭据（通过 `asc auth login` 或环境变量 `ASC_*`）。
- 每次上传都使用一个新的构建版本号。
- 建议使用 `ASC_APP_ID`，或者明确指定 `--app` 参数。

## 推荐的完整命令
- TestFlight：
  - `asc publish testflight --app <APP_ID> --ipa <PATH> --group <GROUP_ID>[,<GROUP_ID>]`
  - 可选参数：`--wait`、`--notify`、`--platform`、`--poll-interval`、`--timeout`
- App Store：
  - `asc publish appstore --app <APP_ID> --ipa <PATH> --version <VERSION>`
  - 可选参数：`--wait`、`--submit`、`--confirm`、`--platform`、`--poll-interval`、`--timeout`

## 手动操作步骤（当需要更多控制时）
1. 上传构建版本：
   - `asc builds upload --app <APP_ID> --ipa <PATH>`
2. （如需要）查找构建版本 ID：
   - `asc builds latest --app <APP_ID> [--version <VERSION>] [--platform <PLATFORM>]`
3. 在 TestFlight 中进行分发：
   - `asc builds add-groups --build <BUILD_ID> --group <GROUP_ID>[,<GROUP_ID>]`
4. 将构建版本关联到 App Store 并提交：
   - `asc versions attach-build --version-id <VERSION_ID> --build <BUILD_ID>`
   - `asc submit create --app <APP_ID> --version <VERSION> --build <BUILD_ID> --confirm`
5. 检查或取消提交：
   - `asc submit status --id <SUBMISSION_ID>` 或 `--version-id <VERSION_ID>`
   - `asc submit cancel --id <SUBMISSION_ID> --confirm`

## 注意事项
- 始终使用 `--help` 选项来查看每个命令的详细参数说明。
- 可以使用 `--output table` 或 `--output markdown` 选项来获取更易阅读的输出格式；默认输出格式为 JSON。