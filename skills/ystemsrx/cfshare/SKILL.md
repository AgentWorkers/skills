---
name: cfshare
description: 通过 Cloudflare Quick Tunnel 将本地服务、端口、文件或目录暴露为临时的公共 HTTPS 链接。可用于共享本地服务、发送可下载文件、预览内容等。
metadata:
  {
    "openclaw":
      {
        "emoji": "☁️",
        "skillKey": "cfshare",
        "requires":
          {
            "bins": ["cloudflared"],
            "config": ["plugins.entries.cfshare.enabled"],
          },
      },
  }
---

# CFShare — Cloudflare 快速隧道服务

该服务允许您将本地服务、端口、文件或目录暴露为临时的公共链接（格式为 `https://*.trycloudflare.com`）。

---

## 标准工作流程

1. **`env_check()`** — 首先执行此命令，以确认 `cloudflared` 是否已安装并获取当前的策略默认值。
2. **创建暴露服务：**
   - 如果有正在运行的本地服务 → 使用 `expose_port(port, opts?)` 命令进行暴露。
   - 如果需要共享或预览文件或目录 → 使用 `expose_files(paths, opts?)` 命令。
3. **创建成功后**：向用户提供 `public_url` 和 `expires_at`（过期时间）。提醒用户在使用完成后调用 `exposure_stop` 命令来停止服务。
4. **检查/监控**：使用 `exposure_get(id)` 命令（可选参数 `probe_public: true`）来验证链接的端到端可达性。
5. **故障排除**：当出现问题时，使用 `exposure_logs(id)` 命令查看日志。
6. **清理**：使用 `exposure_stop(id)` 或 `exposure_stop(id="all")` 命令来停止所有暴露服务。

---

## 工具参考

### 1. `env_check`

检查 `cloudflared` 是否已安装，获取其版本信息，并返回当前的策略默认值。

---

### 2. `expose_port`

通过 Cloudflare 快速隧道服务暴露正在运行的本地服务。该工具会先测试 `127.0.0.1:<port>` 端口是否可访问，如果端口被阻止，则会返回相应的错误信息。

**可能出现的错误：**
- `"invalid port"`（端口无效）
- `"port blocked by policy: <N>"`（端口被策略禁止）
- `"local service is not reachable on 127.0.0.1:<N>"`（无法通过 `127.0.0.1:<port>` 访问本地服务）

---

### 3. `expose_files`

将文件或目录复制到临时工作区，启动一个只读的静态文件服务器，并通过隧道服务将其公开。

**文件服务方式：**

- **普通模式**：
  - 单个文件 → 直接在根路径下提供。
  - 多个文件或目录 → 通过文件浏览器界面展示。
- **ZIP 模式**：
  - 所有文件会被打包成一个 ZIP 文件包。

**展示方式：**
  - 默认选项：下载 | 预览 | 原始格式
  - 可通过查询参数自定义展示方式：
    - `download` → 强制浏览器下载文件。
    - `preview` → 在浏览器中直接显示文件内容（图片、PDF、Markdown、音频/视频、HTML、文本等）。
    - `raw` → 以原始格式提供文件内容。
    - 如果文件类型无法预览，系统会自动切换到原始格式或下载选项。

---

### 4. `exposure_list`

列出所有正在运行的暴露服务（包括活跃的服务和最近停止的服务）。

---

### 5. `exposure_get`

获取一个或多个暴露服务的详细信息。支持三种选择方式（这些方式互斥）：

---

### 6. `exposure_stop`

停止一个、多个或所有暴露服务。该命令会终止 `cloudflared` 进程，关闭源服务器和代理服务器，并删除临时工作区的文件。

---

### 7. `exposure_logs`

从 `cloudflared` 和源服务器获取合并后的日志记录。

---

### 8. `maintenance`

用于管理服务的生命周期：

- **`start_guard`** — 启动 TTL 过期处理机制（定期运行；通常会自动启动）。
- **`run_gc` ** — 清理未被任何活跃服务使用的临时工作区目录和过期进程。
- **`set_policy` ** — 将策略更改保存到磁盘并重新加载。需要提供 `opts.policy` 或 `opts.ignore_patterns` 参数。

---

### 9. `audit_query`

搜索审计事件日志。

---

### 10. `audit_export`

将筛选后的审计事件导出到本地 JSONL 文件中。

---

## 安全性与策略默认值

策略优先级（从高到低）：**策略 JSON 文件** > **插件配置** > **内置默认值**。

---

## 响应规则

在向用户展示结果时，LLM（Large Language Model）必须遵守以下规则：

1. **创建暴露服务后**，必须始终显示 `public_url` 和 `expires_at`。
2. **时间戳** 必须使用用户所在时区的可读格式（`yyyy-mm-dd HH:MM:SS`）显示。禁止使用原始的 ISO 格式。
3. 当访问模式设置为 `"none"` 时，必须警告用户链接为公开可访问状态（无需认证）。
4. 必须提供清理说明（建议用户使用 `exposure_stop` 命令来停止服务）。
5. 发生错误时，建议用户查看 `exposure_logs(id)` 以获取诊断信息。
6. 为确保安全，如果用户的操作意图不明确或可能涉及敏感信息，必须先获取用户的确认才能创建暴露服务。