---
name: mission-control-visual-qa
description: 通过 SSH 连接到 SAPCONET，并使用 Puppeteer 捕获屏幕截图以及进行基本的 DOM 检查，来运行 Mission Control 的视觉质量评估（visual QA）任务。
---
# mission-control-visual-qa

作者：Billy (SAPCONET)

## 目的
通过 SSH（连接到Neill 机器 `100.110.24.44`）对 SAPCONET 上的 Mission Control 页面执行视觉质量检查（包括截图和基本的 DOM 检查）。

## 该技能包含的内容
- `scripts/mission-control-visual-qa.js`：基于 Puppeteer 的远程执行脚本，用于在 SAPCONET 上运行相关操作。
- `scripts/run-mission-control-visual-qa.sh`：本地辅助脚本，负责通过 `scp` 和 `ssh` 将远程脚本复制到本地并执行。

## 安全规则
- 仅针对您被授权检查的 Mission Control 页面进行操作。
- 默认输出路径为 SAPCONET 上的 `~/.openclaw/workspace/output/visual-qa/`。
- 除 SSH/SCP 用于连接到 SAPCONET 以及加载指定 URL 的页面外，脚本不会执行任何外部网络操作。
- 该脚本为只读脚本，不会提交表单或点击任何可能破坏页面功能的控件。

## 使用方法
在本地机器上执行以下命令：

```bash
bash scripts/run-mission-control-visual-qa.sh \
  "https://mission-control.example.local/dashboard" \
  "https://mission-control.example.local/status"
```

可选的环境变量：
- `SSH_TARGET`（默认值：`neill@100.110.24.44`）
- `REMOTE_RUN_DIR`（默认值：`~/.openclaw/workspace/mission-control-visual-qa-runner`）
- `OUTPUT_DIR`（默认值：`~/.openclaw/workspace/output/visual-qa/`）

## 预期输出
在 SAPCONET 主机上，每个 URL 会生成以下结果：
- 图片格式的截图（*.png 文件）
- 基本的 DOM 检查结果（页面的标题、`h1` 标签以及正文内容）
- 最终的 JSON 总结信息会输出到标准输出（stdout）