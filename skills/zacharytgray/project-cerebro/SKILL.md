---
name: project-cerebro
version: 1.0.2
description: "**Project Cerebro - Control Surface：基于 OpenClaw 构建的模块化多脑执行控制面板**  
Project Cerebro 的 Control Surface 是一个模块化设计的多脑执行控制面板，旨在实现对多个智能系统的协同控制与管理。该平台充分利用 OpenClaw 的强大功能，提供了灵活的接口和丰富的配置选项，帮助用户轻松构建和扩展复杂的智能系统。"
homepage: https://github.com/zacharytgray/project-cerebro
metadata: {"clawhub":{"category":"productivity","emoji":"🧠","requiresEnv":["OPENCLAW_GATEWAY_URL","OPENCLAW_TOKEN"],"exposesHttp":true,"fileUploads":true}}
---

# 项目 Cerebro – 控制界面

这是一个高度模块化的、专为代理（agents）设计的执行控制界面，用于运行多个 OpenClaw “代理”（agents）：
- **执行流**（Execution Stream）：所有任务执行情况的真实来源
- **重复性任务**（Recurring Tasks）：会在指定时间将实例添加到执行流中
- 每个代理都支持 **自动模式**（Auto Mode）和手动运行
- 通过 OpenClaw 消息系统发送与通道无关的通知

![仪表板截图](https://raw.githubusercontent.com/zacharytgray/project-cerebro/master/assets/dashboard.png)

## 项目简介

Cerebro 是一个结合了仪表板和运行时的工具，帮助您监控和管理一组专门的代理（“代理”）。

### 核心模型
- **执行流**（Execution Stream）：所有任务执行情况的真实来源。
- **一次性任务**（One-time tasks）：在您点击 **运行** 时执行，或者在代理处于 **自动模式** 时执行。
- **重复性任务**（Recurring tasks）：会在指定时间将一个实例添加到执行流中，并且无论代理是否处于自动模式都会执行。

### 代理（Agents）
- **代理**（Brain）：是一个与 OpenClaw 代理 ID 相关联的命名范围、工具和配置组合。
- **Nexus** 是默认的代理：用于通用任务编排和其他功能。

## 安装/设置（简要步骤）

请参阅 **SETUP.md** 以获取完整说明。

**必需的秘钥/环境变量**
- `OPENCLAW_GATEWAY_URL`（例如：`ws://127.0.0.1:18789`）
- `OPENCLAW_TOKEN`（OpenClaw 网关令牌）

安装步骤概要：
1. 克隆仓库并安装依赖项。
2. 根据 `.env.example` 文件创建 `.env` 文件，并设置上述 OpenClaw 相关的变量。
3. 复制模板文件：
   - `config/brains.template.json` → `config/brains.json`
   - `config/brain_targets.template.json` → `config/brain_targets.json`
4. （可选）运行示例代码：`npm run seed`

## 模块化设计（便于代理定制）

该仓库支持代理快速进行自定义：
- 通过编辑 `config/brains.json` 和 `config/brain_targets.json` 文件来添加/删除代理。
- 可选的工作模块（Job module）：通过添加/删除相应的代理和页面来启用/禁用该模块（参见 `config/brains_jobs.addon.template.json`）。
- 重复性任务的模板位于 `config/seeds/` 目录下。

## 运行时行为（安全透明性）

该项目运行一个本地 HTTP 服务（基于 Fastify 和 React UI）：
- 通过 `PORT`（默认为 3000）提供仪表板访问。
- 使用您提供的秘钥调用 **OpenClaw 网关/CLI**。
- 通过 **OpenClaw 消息系统** 将消息发送到各个代理的指定通道和目标。
- 支持通过 `POST /api/upload` 接受文件上传，并将文件存储在 `./data/<brainId>/intake/` 目录下。

## 注意事项
- 项目中不会存储任何秘钥或个人身份信息；本地配置文件和数据库会被 Git 忽略。
- 通知会通过 OpenClaw 的通道系统（如 Discord、Telegram、Signal 等）发送。
- 可选模块（如任务跟踪器/个人资料）是可选的；如果未启用相关模块，UI 中的相关页面将不会显示。