---
name: deploy
description: 当用户希望将代码推送到 Railway 时，可以使用此技能。相关的命令包括 “railway up”、“deploy”、“deploy to railway” 或 “push”。对于初始设置或创建服务，请使用 “new skill”；而对于 Docker 镜像的创建，则需要使用 “environment skill”。
allowed-tools: Bash(railway:*)
---

# 部署代码

使用 `railway up` 命令将当前目录中的代码部署到 Railway 平台。

## 适用场景

- 用户请求“部署”代码
- 用户输入“railway up”或“将代码部署到 Railway”
- 用户希望部署本地代码更改
- 用户要求“部署代码并修复任何问题”（此时应使用 `--ci` 模式）

## 提交信息

提交代码时务必使用 `-m` 标志，并附上描述性强的提交信息，说明此次部署的具体内容：

```bash
railway up --detach -m "Add user authentication endpoint"
```

示例提交信息：
- “修复了工作进程中的内存泄漏”
- “实现了功能 #123”
- “更新了依赖项并修复了构建警告”

## 部署模式

### 分离模式（默认模式）
立即开始部署并返回结果。适用于大多数部署场景。

```bash
railway up --detach -m "Deploy description here"
```

### 持续集成（CI）模式
在部署过程中实时显示构建日志。适用于需要监控构建过程或调试问题的用户。

```bash
railway up --ci -m "Deploy description here"
```

**适用场景**：
- 用户要求“部署并查看构建结果”或“部署后修复问题”
- 用户正在调试构建失败的情况
- 用户希望查看构建的输出信息

## 部署到特定服务

默认情况下，代码会部署到已关联的服务上。如需部署到其他服务，请使用相应的参数：

```bash
railway up --detach --service backend -m "Deploy description here"
```

## 部署到未关联的项目

若要部署到未关联的项目，需要同时使用 `--project` 和 `--environment` 参数：

```bash
railway up --project <project-id> --environment production --detach -m "Deploy description here"
```

## 命令行选项

| 参数          | 说明                          |
|--------------|---------------------------------------------|
| `-m, --message <MSG>` | 用于指定描述性强的提交信息（必须使用）         |
| `-d, --detach`     | 不显示构建日志（默认设置）                     |
| `-c, --ci`       | 实时显示构建日志，完成后退出                    |
| `-s, --service <NAME>` | 指定目标服务（默认为已关联的服务）                |
| `-e, --environment <NAME>` | 指定目标环境（默认为已关联的环境）                |
| `-p, --project <ID>` | 指定目标项目（需配合 `--environment` 参数使用）         |
| `[PATH]`       | 部署路径（默认为当前目录）                     |

## 目录链接

Railway CLI 会遍历目录树以找到关联的项目。如果您位于已关联项目的子目录中，无需重新进行链接操作。

对于子目录的部署，建议通过环境配置设置 `rootDirectory`，然后使用 `railway up` 命令进行部署。

## 部署后的操作

### 分离模式
使用 `deployment` 命令（配合 `--lines` 参数）查看构建状态。

### 持续集成模式
构建日志会实时显示在终端中。如果构建失败，错误信息会直接显示在输出结果中。

**注意**：在持续集成模式下，**切勿再次运行 `railway logs --build`**——因为日志已经实时输出过了。如需更多详细信息，可以使用 `deployment` 命令（配合 `--lines` 参数）。

## 可组合性

- **部署后检查状态**：使用 `service` 命令
- **查看日志**：使用 `deployment` 命令
- **修复配置问题**：使用 `environment` 命令
- **修复配置问题后重新部署**：再次使用 `environment` 命令

## 错误处理

### 未关联项目
```
No Railway project linked. Run `railway link` first.
```

### 未关联服务
```
No service linked. Use --service flag or run `railway service` to select one.
```

### 构建失败（持续集成模式）
由于构建日志已经实时输出，因此请直接查看 `railway up --ci` 的输出结果。在持续集成模式下，**切勿再次运行 `railway logs`**（否则日志会无限循环输出）。

**常见错误及解决方法**：
- 依赖项缺失 → 检查 `package.json` 或 `requirements.txt` 文件
- 构建命令错误 → 使用 `environment` 命令进行修复
- Dockerfile 问题 → 检查 Dockerfile 的路径是否正确