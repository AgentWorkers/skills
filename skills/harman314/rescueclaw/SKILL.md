# RescueClaw 技能

为高风险操作提供检查点/回滚的安全保障。

## 在执行高风险操作之前

在修改配置、安装技能或更新网关之前，请先创建一个检查点：

```javascript
const rescueclaw = require('./rescueclaw-checkpoint');
await rescueclaw.createCheckpoint('About to apply config changes');
```

RescueClaw 会立即进行备份。如果代理在回滚窗口内失去响应，系统会自动恢复到备份状态。

## 操作成功后

删除检查点：

```javascript
const rescueclaw = require('./rescueclaw-checkpoint');
await rescueclaw.clearCheckpoint();
```

## 命令

代理也可以直接通过 RescueClaw CLI 来执行以下操作：

- `rescueclaw backup` — 手动创建快照
- `rescueclaw status` — 检查代理状态
- `rescueclaw list` — 列出所有备份文件

## 安装

该守护进程二进制文件已针对支持的平台（linux/arm64）进行了打包。安装完成后，它会被复制到 `~/.local/bin/rescueclaw` 目录中。对于其他平台，请从 [GitHub 仓库](https://github.com/harman314/rescueclaw/releases) 下载。

数据存储在 `~/.openclaw/rescueclaw/` 目录中（用户本地存储，无需使用 sudo 权限）。

## API 参考

### `createCheckpoint(reason, rollbackWindowSec = 300)`

创建一个供 RescueClaw 监控的检查点文件。如果代理在回滚窗口内失去响应，系统会立即从该检查点备份中恢复。

**参数：**
- `reason` (字符串): 即将执行的操作的描述
- `rollbackWindowSec` (数字，可选): 监控问题的时间窗口（默认值：300 秒）

**返回值：** Promise<void>

### `clearCheckpoint()`

删除检查点文件，表示高风险操作已成功完成。

**返回值：** Promise<void>

### `getStatus()`

通过调用 CLI 来获取 RescueClaw 守护进程的状态。

**返回值：** 包含状态详细信息的 Promise<object>

## 示例：安全配置更新

```javascript
const fs = require('fs');
const rescueclaw = require('./rescueclaw-checkpoint');

async function updateConfig(newConfig) {
  // Create safety checkpoint
  await rescueclaw.createCheckpoint('Updating OpenClaw config', 180);
  
  try {
    // Perform the risky operation
    fs.writeFileSync('~/.openclaw/openclaw.json', JSON.stringify(newConfig));
    
    // Restart gateway
    await exec('systemctl restart openclaw-gateway');
    
    // If we get here, it worked!
    await rescueclaw.clearCheckpoint();
    console.log('✅ Config updated successfully');
  } catch (err) {
    console.error('❌ Config update failed:', err);
    // Don't clear checkpoint - let RescueClaw auto-restore
  }
}
```