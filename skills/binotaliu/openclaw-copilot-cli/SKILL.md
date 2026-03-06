# copilot-cli

## 描述
通过 `exec` 命令执行 GitHub Copilot CLI，用于代码生成、文件编辑以及使用先进模型（Claude/GPT-5）执行 shell 任务。适用于需要 Copilot 提供的编码/自动化功能的场景。

## 安装
```
npm install -g @github/copilot
```
或在 macOS 上：
```
brew install copilot-cli
```

验证安装：
```
copilot --help
```

## 认证
1. 运行 `copilot`（交互式模式）。
2. 输入 `/login` 并按照提示操作（使用 GitHub 账户，需订阅 Copilot）。
完成认证后即可进行非交互式使用。

## 使用方法
### 非交互式（一次性命令）
```
copilot -p \"Your prompt here\" --allow-all --silent
```
- `--allow-all`：允许使用所有工具、路径和 URL（简写为 `--yolo`）。
- `--silent`：仅输出代理的响应。
- `--model claude-sonnet-4.6` 或 `gpt-5.2` 等：选择使用的模型。

**在 OpenClaw 环境中执行：**
```
exec:
  command: copilot -p 'Generate a Python script to...' --allow-all --silent
```

### 交互式使用
```
exec:
  command: copilot
  pty: true
```
此时可以使用 `process` 工具：
- `send-keys`：发送输入（例如 `['prompt text', 'Enter']`）
- `log`：查看输出结果

## 示例
### Shell 任务
```
copilot -p 'List all .js files and summarize' --allow-all
```

### 代码生成
```
copilot -p 'Create a simple Express server in Node.js' --allow-all --silent
```

### 文件编辑
```
copilot -p 'Add error handling to main.js' --allow-all
```

### 高级模型
```
copilot -p '...' --model gpt-5.3-codex --allow-all
```

## 测试
测试结果：成功生成了 `hello_world.sh` 文件；
Solana NFT 铸造测试也已成功启动（属于复杂任务）。

## 提示：
- 代理（agents）中的自定义指令会自动加载。
- 如需禁用自定义指令，可使用 `--no-custom-instructions`。
- 如需将会话内容导出为文件，可使用 `--share`。
- 日志文件保存路径：`~/.copilot/logs/`