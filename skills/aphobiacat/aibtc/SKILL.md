# AIBTC Skill

用于管理 aibtc-worker 的自动化任务。适用于用户需要运行、停止或检查 aibtc 任务的状态的情况。

## 命令

- `run {address}`：使用指定的地址启动 aibtc-worker。
- `stop`：停止 aibtc-worker。
- `status`：检查 aibtc-worker 的当前状态。

## 实现方式

`handler.js` 处理所有的 aibtc 命令。