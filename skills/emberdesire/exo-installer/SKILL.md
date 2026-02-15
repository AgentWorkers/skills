# exo-installer 技能

**E.x.O. 生态系统管理器**

通过一个命令即可安装、更新和监控所有 E.x.O. 工具。

## 使用场景

- 用户需要安装 E.x.O. 工具（如 jasper-recall、hopeIDS、context-compactor）  
- 用户想了解 E.x.O. 生态系统的详细信息  
- 用户需要配置 OpenClaw 插件  
- 用户希望检查已安装工具的运行状态  

## 快速入门  

```bash
# Install all public E.x.O. packages
npx exo-installer install --all

# Or install specific tools
exo install jasper-recall
exo install hopeIDS
exo install jasper-context-compactor

# Health check
exo doctor
exo doctor --json  # For automation
```

## 命令说明  

| 命令 | 功能说明 |
|---------|-------------|
| `exo install --all` | 安装所有公开可用的包 |
| `exo install <pkg>` | 安装指定的包 |
| `exo update` | 更新所有已安装的包 |
| `exo doctor` | 检查所有组件的运行状态 |
| `exo doctor --json` | 以 JSON 格式输出组件状态信息 |
| `exo list` | 列出所有可用的包 |
| `exo internal clone` | 克隆私有仓库（需要 GitHub 访问权限） |

## 可用包  

### 公开包（通过 npm 获取）  

| 包名 | 功能说明 |
|---------|-------------|
| `jasper-recall` | 用于管理代理内存的本地 RAG（Retrieval, Aggregation, and Generation）系统 |
| `hopeIDS` | 用于检测行为异常的工具 |
| `jasper-context-compactor` | 用于管理本地模型的令牌系统 |
| `jasper-configguard` | 提供安全配置修改功能，并支持回滚操作 |

### 私有包（存储在 GitHub 上）  

| 仓库名 | 功能说明 |
|------|-------------|
| `hopeClaw` | 用于元认知推理的引擎 |
| `moraClaw` | 用于任务调度的代理工具 |
| `task-dashboard` | 项目管理系统 |
| `exo-distiller` | 用于代理软件的分发和构建流程 |

**注意：** 私有包需要通过 GitHub 组织（org）进行访问。  

```bash
exo internal clone
```

## 状态检查  

```bash
$ exo doctor
🔍 E.x.O. Health Check

jasper-recall ................. ✅ v0.4.2
  ChromaDB: ✅ connected
  Embeddings: ✅ loaded
  Documents: 847

hopeIDS ...................... ✅ v1.3.3
  Analyzer: ✅ ready
  Models: 3 loaded

jasper-context-compactor ...... ✅ v0.2.2

Overall: 3/3 healthy
```

## 集成说明  

安装完成后，这些工具会自动注册到 OpenClaw 中：  

```json
{
  "extensions": {
    "jasper-recall": { "enabled": true },
    "hopeIDS": { "enabled": true },
    "jasper-context-compactor": { "enabled": true }
  }
}
```

## 链接  

- GitHub: https://github.com/E-x-O-Entertainment-Studios-Inc/exo-installer  
- 文档: https://exohaven.com/products  
- Discord: https://discord.com/invite/clawd