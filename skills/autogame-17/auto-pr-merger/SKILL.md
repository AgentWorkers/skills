# 自动合并 PR 的技能

该技能可自动化以下工作流程：从 GitHub 下载 PR、运行测试、尝试修复错误代码，以及在修复成功后合并 PR。

## 使用方法

```bash
node skills/auto-pr-merger/index.js --pr <PR_NUMBER_OR_URL> --test "<TEST_COMMAND>" [--retries <NUMBER>]
```

## 参数

- `--pr`：PR 的编号或 URL（例如：`123` 或 `https://github.com/owner/repo/pull/123`）。
- `--test`：用于运行测试的命令（例如：`npm test`、`pytest`）。
- `--retries`：（可选）如果测试失败，尝试修复代码的次数。默认值：3 次。

## 前提条件

- 已安装并登录了 `gh` 命令行工具（CLI）。
- 确保系统中已安装 Node.js 环境。

## 工作原理

1. 使用 `gh pr checkout` 命令下载 PR 的代码。
2. 运行指定的测试命令。
3. 如果测试失败：
    * 读取测试结果。
    * 尝试修复代码（目前这部分代码仅为占位符/模拟修复逻辑）。
    * 提交并推送修复后的代码。
    * 重新运行测试命令。
4. 如果测试通过：
    * 使用 `gh pr merge --merge --auto` 命令合并 PR。