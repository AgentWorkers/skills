---
name: parakeet-local-asr
description: 在 Ubuntu/Linux 和 macOS（支持 Intel/Apple Silicon 处理器）系统上，安装并使用本地版的 NVIDIA Parakeet ASR（自动语音识别技术），该技术支持与 OpenAI 兼容的转录 API。适用于需要私密/本地的语音转文本功能、语音转录设置、ASR 故障排查，或使用 Parakeet 配置 OpenClaw 语音处理栈（并可选择使用 Whisper 作为备用方案）的场景。
---
# Parakeet 本地自动语音识别（ASR）功能

以确定性的方式运行 Parakeet 的本地 ASR 功能。

## 标准工作流程

1. 安装/更新运行时环境：
   ```bash
   bash scripts/bootstrap.sh
   ```
2. 启动服务：
   ```bash
   bash scripts/start.sh
   ```
3. 验证服务运行状态：
   ```bash
   bash scripts/healthcheck.sh
   ```
4. （可选）使用本地音频文件进行测试：
   ```bash
   bash scripts/smoke-test.sh /path/to/audio.mp3
   ```

## 仓库位置

脚本默认使用的安装/更新路径：
- `~/parakeet-asr`

在运行脚本前，可以通过环境变量覆盖此路径：
```bash
PARAKEET_DIR=/custom/path bash scripts/bootstrap.sh
```

## OpenClaw 集成说明

在服务运行状态检查通过后，使用以下配置：
- URL: `http://localhost:9001`
- 端点：`/v1/audio/transcriptions`

如果用户更看重服务的可靠性而非语音识别的准确性，可以将 Whisper 作为备用服务提供商。

## 安全规则

- 在执行需要提升权限的操作（如使用包管理器）之前，请先征得许可。
- 不要终止与当前任务无关的进程。
- 除非另有明确要求，否则请将更改限制在 ASR 配置范围内。