---
name: neo-app-mode
description: 在收集完项目需求后，开始构建全栈应用程序。当用户选择“Neo App Mode”，或请求构建/创建一个新的应用程序时，或者希望使用 React+Vite+Tailwind 作为前端框架，并结合 Node.js/Express/MongoDB 构建后端系统（采用 MVC 架构）时，应执行此步骤。
---
# Neo 应用模式

首先收集需求，然后搭建一个可用于生产的初始框架。

## 需求收集（在搭建框架之前询问）

使用以下简洁的清单来收集需求：
1. 项目名称
2. 应用类型及核心模块（认证、仪表板、CRUD 实体）
3. 用户角色（管理员/普通用户等）
4. 所需页面和 API 端点
5. MongoDB 连接方式（本地/Atlas）
6. 认证方式（JWT/会话/OAuth）
7. 额外功能（文件上传、图表、支付、通知）

如果用户不确定，可以使用 `references/default-requirements.md` 中的默认设置。

## 生成应用框架

运行以下命令：

```bash
bash skills/neo-app-mode/scripts/scaffold_neo_app.sh \
  --name <project-name> \
  --path apps \
  --with-auth jwt
```

生成的框架结构如下：
- `frontend/` → React + Vite + Tailwind
- `backend/` → Express + MongoDB + MVC
- `frontend` 和 `backend` 目录下有 `.env.example` 配置文件
- 项目根目录下有包含运行步骤的 `README.md` 文件

## 开发规范

- 在生成代码之前，务必确认所有需求已明确。
- 后端代码应遵循清晰的 MVC 结构：`models/`、`controllers/`、`routes/`、`middlewares/`、`config/`。
- 至少添加一个包含完整 CRUD 功能的示例实体模块。
- 添加一个用于检查应用是否正常运行的健康检查路由（health check route），并设置 API 前缀为 `/api/v1`。
- 生成的代码应保持简洁、易于阅读且具备可扩展性。