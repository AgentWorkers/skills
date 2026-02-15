---
name: VSCode
description: 避免常见的 VSCode 错误：设置冲突、调试器配置问题以及扩展程序之间的冲突。
metadata: {"clawdbot":{"emoji":"💻","os":["linux","darwin","win32"]}}
---

## 设置优先级
- 用户设置 → 工作区设置 → 文件夹设置：后续的设置会覆盖之前的设置
- 每个项目都有独立的 `.vscode/settings.json` 文件，该文件会覆盖用户设置
- 工作区中的 `"editor.formatOnSave"` 设置会覆盖用户设置（但可能会引起混淆）
- 多根工作区需要为每个文件夹设置单独的配置；或者使用根目录下的 `.code-workspace` 文件进行统一管理
- 有些设置仅适用于用户级别，例如 `"terminal.integrated_shell"`。

## 格式化冲突
- 如果同一语言支持多种格式化工具，可以设置 `"[language]": {"editor.defaultFormatter": "id}"` 来指定默认格式化工具
- 如果同时使用了 Prettier 和 ESLint，需要禁用其中一个：在 ESLint 项目中将 `"prettier.enable": false` 设置为 `false`
- 如果保存文件时自动执行了错误的格式化工具，需要明确指定默认的格式化工具（使用 `defaultFormatter`）
- `.editorconfig` 文件会覆盖某些设置，可能会与扩展程序的设置发生冲突

## 调试器配置
- 大多数情况下需要使用 `launch.json` 文件来配置调试器，不能直接按 F5 键启动调试
- `“cwd”` 的路径是相对于工作区根目录的，而不是 `launch.json` 文件所在的路径
- 如果指定了错误的 `“program”` 路径，应使用 `${workspaceFolder}/path/to/file`
- 对于 Node.js 项目，可以使用 `"skipFiles"` 来避免进入 `node_modules` 目录
- 对于多进程应用程序，需要在 `launch.json` 中使用 `"compounds"` 数组来配置调试器

## 扩展程序
- 如果某个扩展程序导致程序崩溃，可以暂时禁用它，然后逐一重新启用
- 如果安装扩展程序后出现 “Cannot find module” 的错误，需要完全重启 VS Code
- 如果扩展程序的设置没有生效，检查是否被工作区的设置覆盖了
- 如果存在冲突的扩展程序，可能是键绑定或功能重复导致的

## 终端设置
- 如果新打开的终端使用了错误的 shell，可以通过设置 `"terminal.integrated.defaultProfile.*"` 来更改
- 如果终端缺少环境变量，这些变量通常是从调试器的配置中继承的，而不是从 `.bashrc` 文件中获取的
- 如果安装扩展程序后路径没有更新，需要重启 VS Code，而不仅仅是终端
- 如果存在终端集成问题，可以将 `"terminal.integrated.shellIntegration.enabled": false` 设置为 `false` 来禁用相关功能

## 远程开发
- 使用 SSH 进行远程开发时，`~/.ssh/config` 文件中的主机配置必须正确；如果需要使用不同的配置文件，可以设置 `"remote.SSH.configFile"`
- 对于容器环境，需要使用 `.devcontainer/devcontainer.json` 文件；Dockerfile 通常不会被自动检测到
- 在 Windows Subsystem for Linux (WSL) 环境中，扩展程序需要单独安装，且这些扩展程序会保留在 WSL 环境中
- 端口转发功能通常是自动配置的，但并非总是如此，需要查看 VS Code 的端口转发设置

## 工作区信任设置
- 在受限模式下，一些功能（如调试和某些扩展程序）可能会被禁用
- 首次打开工作区时会出现信任提示，选择 “Trust Folder” 可以启用所有功能
- 在多根工作区环境中，可以对某些文件夹进行单独信任设置

## 常见问题解决方法
- 如果 IntelliSense 不起作用，可以在输出面板中检查语言服务器的状态
- 如果在 TypeScript 项目中出现 “Cannot find module” 的错误，可以重启 TypeScript 服务器（使用快捷键 Cmd+Shift+P，然后选择 “TypeScript: Restart TS Server”）
- 如果 Git 无法检测到文件更改，检查文件是否位于子文件夹中，或者确保 `.git` 文件位于工作区根目录下或已正确配置
- 如果设置无法保存，检查 `.vscode/settings.json` 文件的写入权限是否正确