---
name: Port Kill - Process Killer by Port
description: **使用一个命令终止运行在任意端口上的进程**  
这款跨平台工具专为开发者设计，彻底告别了使用 `lsof`、`grep`、`awk` 和 `xargs` 的繁琐步骤。它是一款免费的命令行工具（CLI），能够轻松完成进程管理任务。
---

# Port Kill

通过一个命令终止指定端口的进程。支持 macOS、Linux 和 Windows 系统。

## 安装

```bash
npm install -g @lxgicstudios/port-kill
```

## 命令

### 终止指定端口的进程

```bash
npx @lxgicstudios/port-kill 3000
npx @lxgicstudios/port-kill 8080
```

### 强制终止（SIGKILL）

```bash
npx @lxgicstudios/port-kill 3000 -f
```

### 列出所有进程（不终止）

```bash
npx @lxgicstudios/port-kill 3000 --list
```

### 检查端口是否被使用

```bash
npx @lxgicstudios/port-kill --check 3000
```

### 查找可用端口

```bash
npx @lxgicstudios/port-kill --find 3000
```

返回从 3000 开始的可用端口列表。

## 选项

| 选项 | 描述 |
|--------|-------------|
| `-f, --force` | 强制终止进程（使用 SIGKILL 信号） |
| `-l, --list` | 仅列出所有进程 |
| `--check <port>` | 检查指定端口是否被使用 |
| `--find <port>` | 查找指定端口是否可用 |

## 常见用法

**终止卡住的开发服务器：**
```bash
npx @lxgicstudios/port-kill 3000
```

**检查 8080 端口上的进程：**
```bash
npx @lxgicstudios/port-kill 8080 --list
```

**查找下一个可用端口：**
```bash
npx @lxgicstudios/port-kill --find 3000
```

## 跨平台支持**

- macOS：使用 `lsof` 命令 |
- Linux：使用 `lsof` 或 `ss` 命令 |
- Windows：使用 `netstat` 命令 |

---

**由 [LXGIC Studios](https://lxgicstudios.com) 开发**

🔗 [GitHub](https://github.com/lxgicstudios/port-kill) · [Twitter](https://x.com/lxgicstudios)