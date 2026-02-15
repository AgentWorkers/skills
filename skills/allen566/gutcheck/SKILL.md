---
name: gutcheck
description: **GutCheck**——一款专注于消化健康追踪的应用程序，提供个性化的健康洞察和基于数据的健康建议。它帮助用户了解自己对某些食物的敏感反应，并优化肠道健康状况。
metadata:
  {
    "openclaw":
      {
        "requires": { 
          "bins": ["node", "npm"], 
          "modules": ["express", "mongoose", "bcrypt", "jsonwebtoken", "cors", "dotenv"]
        },
        "install":
          [
            {
              "id": "gutcheck-app",
              "kind": "git",
              "url": "https://github.com/openclaw/gutcheck.git",
              "dest": "./gutcheck",
              "label": "Clone GutCheck repository",
            },
            {
              "id": "gutcheck-deps",
              "kind": "shell",
              "command": "cd gutcheck && npm install",
              "label": "Install GutCheck dependencies",
            },
            {
              "id": "gutcheck-client-deps",
              "kind": "shell",
              "command": "cd gutcheck/client && npm install",
              "label": "Install GutCheck client dependencies",
            }
          ],
      },
  }
---

# GutCheck 消化健康追踪器

## 概述
GutCheck 通过个性化的洞察和数据驱动的建议，帮助用户了解并改善他们的消化健康。与一般的健康应用程序不同，GutCheck 专注于消化健康领域，提供基于科学依据的见解，帮助用户识别食物敏感性和提升肠道健康。

## 主要功能
- 支持用户认证系统，提供安全的注册和登录功能
- 个性化饮食记录功能，可评估饮食对消化系统的影响
- 通过数据分析识别食物敏感性
- 提供肠道健康指标和进度跟踪功能
- 提供科学依据的饮食建议

## 安装
```bash
clawhub install gutcheck
```

## 设置
1. 安装完成后，进入 gutcheck 目录。
2. 创建一个 `.env` 文件，设置所需的环境变量：
   ```env
   MONGODB_URI=mongodb://localhost:27017/gutcheck
   JWT_SECRET=your-super-secret-jwt-key-here
   PORT=5000
   NODE_ENV=development
   ```
3. 运行应用程序：
   ```bash
   cd gutcheck
   npm run dev
   ```

## 使用方法
- 访问应用程序：http://localhost:3000
- 注册新账户或登录现有账户
- 记录您的饮食情况以及消化系统的反应
- 查看个性化的洞察和建议

## 目标用户
- 关注健康的个人，尤其是有消化问题的人
- 希望识别食物敏感性的人
- 希望改善肠道健康的人
- 需要基于数据的饮食建议的用户

## API 端点
- `POST /api/auth/register` - 注册新用户
- `POST /api/auth/login` - 登录并获取 JWT 令牌
- `GET /api/auth/me` - 获取当前用户信息（需要认证）
- `POST /api/diet/add-meal` - 添加新的饮食记录
- `GET /api/diet/my-meals` - 查看当前用户的所有饮食记录
- `PUT/DELETE /api/diet/my-meals/:id` - 更新或删除特定的饮食记录