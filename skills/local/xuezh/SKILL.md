---
name: xuezh
description: 使用“xuezh”引擎来教授普通话，包括复习、口语练习和评估环节。
metadata: {"moltbot":{"nix":{"plugin":"github:joshp123/xuezh","systems":["aarch64-darwin","x86_64-linux"]},"config":{"requiredEnv":["XUEZH_AZURE_SPEECH_KEY_FILE","XUEZH_AZURE_SPEECH_REGION"],"stateDirs":[".config/xuezh"],"example":"config = { env = { XUEZH_AZURE_SPEECH_KEY_FILE = \"/run/agenix/xuezh-azure-speech-key\"; XUEZH_AZURE_SPEECH_REGION = \"westeurope\"; }; stateDirs = [ \".config/xuezh\" ]; };"},"cliHelp":"xuezh - Chinese learning engine\n\nUsage:\n  xuezh [command]\n\nAvailable Commands:\n  snapshot  Fetch learner state snapshot\n  review    Review due items\n  audio     Process speech audio\n  items     Manage learning items\n  events    Log learning events\n\nFlags:\n  -h, --help   help for xuezh\n  --json       Output JSON\n"}}
---

# Xuezh 技能

## 合同（Contract）

请严格按照说明使用 xuezh CLI。如果某个命令不存在，请请求相应的实现方式，而不是自行猜测。

## 默认流程（Default Loop）：

1) 调用 `xuezh snapshot`。
2) 选择一个简单的计划（1-2 个任务）。
3) 执行一个简短的活动。
4) 记录活动结果。

## CLI 示例（CLI Examples）：

```bash
xuezh snapshot --profile default
xuezh review next --limit 10
xuezh audio process-voice --file ./utterance.wav
```