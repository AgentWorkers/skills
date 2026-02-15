---
name: putio
description: 通过 kaput CLI 管理 put.io 账户（执行文件传输、文件搜索等操作）——可以上传文件、添加磁贴（magnets）或 URL 链接，并查看文件传输的状态；该工具与 chill-institute 技能配合使用效果最佳。
---

# put.io（kaput CLI）

该技能使用非官方的**kaput** CLI通过命令行来操作put.io服务。

如果您同时安装了**chill-institute**技能，您可以：
- 使用**chill.institute**来*启动*数据传输（“发送到put.io”），
- 然后使用该技能来*验证和监控*数据是否已成功传输。

## 安装

- 需要Rust和Cargo环境。
- 安装方法：
  ```bash
  cargo install kaput-cli
  ```
- 确保`kaput`已添加到您的PATH环境变量中（通常位于`~/.cargo/bin`）。

## 认证（设备代码流程）

1. 运行以下命令：
   ```bash
   kaput login
   ```
2. 系统会生成一个链接和一个短代码（例如：`https://put.io/link` + `ABC123`）。
3. 用户在浏览器中输入该短代码。
4. CLI会完成认证过程并在本地生成一个令牌。

## 常用操作（脚本）

所有脚本都会自动查找`kaput`的可执行文件（支持配置`KAPUT_BIN=/path/to/kaput`）。

- 列出所有正在进行的传输任务：
  ```bash
  bash skills/putio/scripts/list_transfers.sh
  ```

- 添加新的传输任务（支持magnet、torrent或直接URL格式的文件）：
  ```bash
  bash skills/putio/scripts/add_transfer.sh "magnet:?xt=urn:btih:..."
  ```

- 搜索文件：
  ```bash
  bash skills/putio/scripts/search_files.sh "query"
  ```

- 查看传输状态（可选：也可查看账户信息）：
  ```bash
  bash skills/putio/scripts/status.sh
  SHOW_ACCOUNT=1 bash skills/putio/scripts/status.sh
  ```

## 高级操作（通过CLI直接执行）

更多高级操作可通过直接运行CLI命令来实现：
```bash
kaput --help
kaput transfers --help
kaput files --help
```

## 安全提示

- **请勿在聊天中输入密码**。请使用`kaput login`命令进行认证。
- `kaput`会将认证凭据（即令牌文件）存储在本地，请妥善保管，避免泄露。
- 避免在共享的日志或截图中显示`kaput debug`命令的输出，因为这可能会暴露系统的配置信息。