---
name: psd-automator
description: 在 Mac 和 Windows 上使用 Photoshop 自动替换 PSD 文件中的文本：支持安全测试（dry-run）、样式锁定检查（style-lock checks）、回滚功能（rollback），以及本地 PSD 文件索引缓存（local PSD index cache）。适用于以下场景：请求中包含文件/路径信息、图层名称（layer names），以及来自聊天渠道（如 DingTalk）的替换文本；同时要求整个过程无需弹出对话框（no popup dialogs required）。
metadata: { "openclaw": { "emoji": "🖼️", "skillKey": "psd-automator" } }
---
# PSD Automator

这是一个跨平台的PSD文本自动化工具，适用于同时使用macOS和Windows的团队。

## 使用范围

- 仅支持第1阶段和第2阶段的功能。
- 理解截图内容不在本工具的覆盖范围内。
- 该工具使用一种任务协议和两种执行引擎：
  - macOS：AppleScript (`osascript`)
  - Windows：Photoshop COM（PowerShell）

## 任务协议

在运行任务之前，请先阅读 [references/task-schema.json](references/task-schema.json) 文件。

**最低要求字段：**
- `taskId`
- `input.edits[]`（包含 `layerName` 和 `newText`）
- `input.exactPath` 或 `input.fileHint`

**可选字段：**
- `workflow.sourceMode`：`inplace` 或 `copy_then_edit`
- `output.exports[]`：PNG输出格式（`mode=single` 或 `mode=layer_sets`，用于分割后的图层资产）
- `output.bundle.zipName`：分割后图层资产的压缩包名称
- `options.pathBridgeMode`：`auto` / `always` / `off`（macOS下的Unicode路径转换方式）
- `options.bundleZip`：是否将所有分割后的PNG文件打包成一个压缩包
- `options.matchImagePath`：用于选择最相似输出图层的截图路径

## 构建和刷新PSD索引

创建或刷新本地缓存：
```bash
node skills/psd-automator/scripts/build-index.js \
  --root "/Projects/Design" \
  --root "/Users/me/Desktop/assets" \
  --index "~/.openclaw/psd-index.json"
```

**增量刷新：**
```bash
node skills/psd-automator/scripts/build-index.js --incremental
```

## 运行任务

**建议先进行模拟运行：**
```bash
node skills/psd-automator/scripts/run-task.js \
  --task "skills/psd-automator/examples/task.mac.json" \
  --dry-run
```

**执行任务：**
```bash
node skills/psd-automator/scripts/run-task.js \
  --task "skills/psd-automator/examples/task.mac.json"
```

**通过OpenClaw聊天命令进行任务调度（支持`.psd`和`.psb`文件格式）：**
```text
/psd design-mac-01 帮我找到20260225工位名牌.psd或20260225工位名牌.psb，把姓名改成琳琳，座右铭改成步履不前，稳步前进，保存成png放置在桌面 --dry-run
```

## DingTalk图像传递（必填）

当在DingTalk中回复消息且任务成功执行并生成PNG输出文件时，最终回复中必须包含以下格式的标记（包含绝对路径）：
```text
[DINGTALK_IMAGE]{"path":"<absolute_png_path>"}[/DINGTALK_IMAGE]
```

**注意事项：**
- 仅使用绝对路径（例如 `/Users/name/Desktop/xxx.png`）。
- 不要使用仅包含文件名的路径。
- 如果 `pngOutputPath`（或 `pngOutputPaths` 中的第一个路径）缺失，请明确报告错误，不要发送错误的标记。
- 对于 `mode=layer_sets` 的情况，`pngOutputPaths` 中应包含所有输出的图层文件。
- 如果有最匹配的截图图像，使用 `selectedPngPath` 作为最终输出图像。
- 如果有压缩包需要发送，使用以下格式的附件：`[DINGTALK_FILE]{"path":"<absolute_zip_path>","fileName":"<name>.zip","fileType":"zip"}[/DINGTALK_FILE]`。
- 先提供易于阅读的总结信息，然后在最后新增一行添加标记。

## OpenClaw路由模式（第2阶段）

请参考 [references/openclaw-subagent-routing.md](references/openclaw-subagent-routing.md) 以了解OpenClaw子代理的路由规则：

**核心流程：**
1. 主代理解析请求。
2. 确定目标机器及平台的能力。
3. 调用相应的目标子代理执行任务。
4. 子代理在本地运行 `run-task.js` 脚本。
5. 返回标准化结果及审计日志。

## 安全基线要求：**
- 始终支持模拟运行（`dryRun`）功能。
- 文本修改后保持字体和字号格式不变。
- 禁用Photoshop的对话框。
- 写入文件前创建备份文件（`.bak`）。
- 遇到文件路径不明确的情况时停止执行任务（`E_FILE_AMBIGUOUS`）；切勿盲目猜测。
- 如果找不到目标图层，返回 `availableLayers` 和 `suggestedLayers`。
- 使用 [references/error-codes.md](references/error-codes.md) 中定义的标准错误代码进行错误处理。