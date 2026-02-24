# cancorteaw-app

这是一个用于我的 OpenClaw 服务器的本地 **Expo / React Native** 应用构建工具。

该工具是一个 **受控的运行器**，仅会执行预先允许的脚本：
`/home/patron/apps/_bin/appctl`
并且该脚本只能在以下路径下运行：
`/home/patron/apps/<project>`

## 功能介绍

该工具通过封装 `appctl` 命令，提供了一个安全、可重复的工作流程：

- 在 `/home/patron/apps/<name>` 下创建一个新的 Expo 应用框架。
- 在 `/home/patron/apps/<name>/app/<Screen>.tsx` 文件中添加一个新的屏幕组件。
- 启动一个基于 `127.0.0.1` 端口的 Web 预览（使用 `expo start --web` 命令）。
- 检查预览进程的状态。

## 命令说明

### 1) 创建新应用
**命令：**
- `new <name>`

**示例：**
- `new demoapp`

**结果：**
- 在 `/home/patron/apps/demoapp` 目录下创建一个新的应用文件夹。
- 尝试初始化 Git（如果可用）。
- 使用 `npx create-expo-app` 命令以非交互式模式生成应用代码。

---

### 2) 添加屏幕组件
**命令：**
- `add-screen <name> <screenName> <title>`

**示例：**
- `add-screen demoapp Settings "Settings"`

**结果：**
- 在 `/home/patron/apps/demoapp/app/Settings.tsx` 文件中生成新的屏幕组件代码。
- 尝试提交更改到 Git（如果可用）。

---

### 3) 启动 Web 预览
**命令：**
- `preview <name>`

**环境参数：**
- `EXPO_PORT`（可选）：自定义预览端口
  默认值：`19006`

**示例：**
- `preview demoapp`
- `EXPO_PORT=19010 preview demoapp`

**结果：**
- 启动 `npx expo start --web --port <port>` 命令。
- 将日志文件保存到：`/home/patron/apps/_logs/<name>.preview.log`
- 将进程 ID 保存到：`/home/patron/apps/_state/<name>.pid`
- 将使用的端口保存到：`/home/patron/apps/_state/<name>.port`

---

### 4) 检查状态
**命令：**
- `status <name>`

**示例：**
- `status demoapp`

**结果：**
- 如果应用正在运行，会显示 “RUNNING” 以及对应的 URL；否则显示 “STOPPED”。

## 安全性与限制

- 该工具仅允许使用 `node`、`npm`、`npx`、`git`、`bash` 和 `python3` 等命令。
- 所有项目路径都被限制在 `/home/patron/apps` 目录内。
- 预览服务绑定在 `127.0.0.1` 端口（本地回环地址）。如需外部访问，需通过 SSH 隧道进行配置。
- 在预览模式下，Expo 的遥测功能被禁用（`EXPO_NO_TELEMETRY=1`）。

## 故障排除

- 如果预览显示 “running” 但页面无法加载，请检查 `/home/patron/apps/_logs/` 目录下的日志文件。
- 如果某个端口已被占用，请更改 `EXPO_PORT` 为空闲端口，然后重新运行 `preview` 命令。
- 要停止预览服务，可以使用 `kill $(cat /home/patron/apps/_state/<name>.pid)` 命令（前提是该进程存在）。