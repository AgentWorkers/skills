---
name: windows-remote
description: 通过 SSH 控制远程 Windows 机器。适用于在 Windows 上执行命令、检查 GPU 状态（使用 nvidia-smi）、运行脚本或管理远程 Windows 系统。相关操作包括：“在 Windows 上运行”、“在远程机器上执行”、“检查 GPU 状态”、“使用 nvidia-smi”等。
metadata:
  {
    "openclaw":
      {
        "emoji": "🖥️",
        "requires": {
          "bins": ["ssh"],
          "env": ["WINDOWS_SSH_HOST", "WINDOWS_SSH_USER"]
        },
        "env": {
          "WINDOWS_SSH_HOST": {
            "description": "Remote Windows IP or hostname",
            "required": true,
            "example": "192.168.1.100"
          },
          "WINDOWS_SSH_PORT": {
            "description": "SSH port (default: 22)",
            "required": false,
            "default": "22",
            "example": "23217"
          },
          "WINDOWS_SSH_USER": {
            "description": "SSH username",
            "required": true,
            "example": "Administrator"
          },
          "WINDOWS_SSH_KEY": {
            "description": "Path to SSH private key (default: ~/.ssh/id_ed25519)",
            "required": false,
            "default": "~/.ssh/id_ed25519"
          },
          "WINDOWS_SSH_TIMEOUT": {
            "description": "Connection timeout in seconds",
            "required": false,
            "default": "10"
          }
        }
      }
  }
---

# Windows远程控制

通过SSH在远程Windows机器上执行命令。

## 配置

在`~/.openclaw/openclaw.json`文件中的`skills.windows-remote.env`部分设置环境变量：

```json
{
  "skills": {
    "windows-remote": {
      "env": {
        "WINDOWS_SSH_HOST": "192.168.1.100",
        "WINDOWS_SSH_PORT": "22",
        "WINDOWS_SSH_USER": "Administrator"
      }
    }
  }
}
```

或者直接导出环境变量：
```bash
export WINDOWS_SSH_HOST="192.168.1.100"
export WINDOWS_SSH_PORT="22"
export WINDOWS_SSH_USER="Administrator"
```

## 快速命令

### 检查连接
```bash
scripts/win-exec.sh "echo connected"
```

### GPU状态
```bash
scripts/win-exec.sh "nvidia-smi"
```

### 运行PowerShell
```bash
scripts/win-exec.sh "powershell -Command 'Get-Process | Select-Object -First 10'"
```

### 执行脚本
```bash
scripts/win-exec.sh "python C:\\path\\to\\script.py"
```

## 脚本参考

### win-exec.sh
在远程Windows机器上执行单个命令。

```bash
scripts/win-exec.sh "<command>"
```

### win-gpu.sh
快速检查GPU状态（使用nvidia-smi工具）。

```bash
scripts/win-gpu.sh
scripts/win-gpu.sh --query  # Compact output
```

### win-upload.sh
通过SCP将文件上传到远程机器。

```bash
scripts/win-upload.sh <local-file> <remote-path>
```

### win-download.sh
从远程机器下载文件。

```bash
scripts/win-download.sh <remote-path> <local-file>
```

## 常见任务

### 检查Ollama是否正在运行
```bash
scripts/win-exec.sh "tasklist | findstr ollama"
```

### 启动服务
```bash
scripts/win-exec.sh "net start <service-name>"
```

### 使用GPU运行Python程序
```bash
scripts/win-exec.sh "python -c \"import torch; print(torch.cuda.is_available())\""
```

### 检查磁盘空间
```bash
scripts/win-exec.sh "wmic logicaldisk get size,freespace,caption"
```

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| 连接被拒绝 | 检查SSH服务：`Get-Service sshd` |
| 权限被拒绝 | 确认`~/.ssh/authorized_keys`或`administrators_authorized_keys`中包含正确的SSH密钥 |
| 超时 | 检查防火墙规则，并确认IP地址和端口号正确 |
| 命令未找到 | 使用完整路径执行命令，或检查Windows系统的PATH环境变量 |

## 安全注意事项

- 使用SSH密钥代替密码
- 保护私钥的安全（使用`chmod 600`设置权限）
- 考虑使用Tailscale来实现跨网络访问