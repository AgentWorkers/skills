---
name: azion-deploy
description: 使用 Azion CLI 部署应用程序、静态网站以及边缘函数到 Azion 服务器。当用户需要将内容部署/发布到 Azion、配置链接/构建/部署流程，或解决与 Azion 身份验证/项目链接相关的问题时，可以使用该工具。
version: 0.1.1
author: AskClaw
entrypoint: scripts/azion-deploy.sh
metadata: {"openclaw":{"emoji":"🚀","short":"Deploy to Azion (CLI)","requires":{"bins":["bash","azion"]}}}
user-invocable: true
command-dispatch: tool
command-tool: azion-deploy
commands:
  - name: azion-deploy
    usage: azion-deploy <preflight|auth-check|quickstart|deploy-local> [args]
    description: Deploy helper wrapper around azion CLI with preflight/auth checks.
---# azion-deploy

使用此技能可将项目部署到 Azion 平台，并进行安全的预检（preflight checks）。

## 内置检查

如果出现以下情况，脚本会立即失败：
- `azion` 可执行文件缺失
- 认证失败（执行 `azion whoami` 命令时）
- 在使用 `--skip-build` 选项时，`.edge/manifest.json` 文件缺失

## 命令

```bash
# Validate CLI + auth
bash {baseDir}/scripts/azion-deploy.sh preflight

# Validate auth only
bash {baseDir}/scripts/azion-deploy.sh auth-check

# Stable quickstart flow
bash {baseDir}/scripts/azion-deploy.sh quickstart --name <project-name> [--token "$AZION_TOKEN"]

# Local deploy flow
bash {baseDir}/scripts/azion-deploy.sh deploy-local [--skip-build] [--auto] [--token "$AZION_TOKEN"]
```

## 注意事项

- 请确保执行顺序为 `link -> build -> deploy`（切勿并行执行）。
- 如果 `whoami` 命令失败，请运行 `azion login`（以交互式方式登录）或提供有效的 `AZION_TOKEN`。
- 有关详细参数和框架行为的信息，请参阅：
  - `references/azion-cli.md`
  - `references/azion-build-frameworks.md`