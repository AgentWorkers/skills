---
name: konto-deploy
description: "在本地部署并运行 Konto（个人财务管理仪表板）。适用于新实例的设置、安装故障排除，或帮助用户开始使用 Konto 的场景。"
metadata:
  openclaw:
    emoji: "🦎"
    requires:
      bins: ["node", "npm", "openssl"]
    install:
      - id: clone
        kind: git
        repo: https://github.com/angelstreet/konto
        branch: main
        label: "Clone Konto repository"
      - id: deps
        kind: script
        cwd: "konto"
        run: "npm install"
        label: "Install dependencies"
      - id: env
        kind: script
        cwd: "konto"
        run: |
          if [ ! -f backend/.env ]; then
            cp .env.example backend/.env
            KEY=$(openssl rand -hex 32)
            sed -i "s/^DB_ENCRYPTION_KEY=$/DB_ENCRYPTION_KEY=$KEY/" backend/.env
            echo "Created backend/.env with generated encryption key"
          else
            echo "backend/.env already exists, skipping"
          fi
        label: "Configure environment"
---
# Konto — 本地部署

这是一个个人及专业财务管理工具，支持银行账户同步、加密货币管理、投资记录、预算规划以及税务工具等功能。

## 先决条件

- Node.js 18+ 及 npm 9+  
- `openssl`（用于生成加密密钥）

## 安装（3条命令）

```bash
git clone https://github.com/angelstreet/konto.git
cd konto
npm install
```

## 配置

```bash
# Create env from template
cp .env.example backend/.env

# Generate and set encryption key
KEY=$(openssl rand -hex 32)
sed -i "s/^DB_ENCRYPTION_KEY=$/DB_ENCRYPTION_KEY=$KEY/" backend/.env
```

### 最小配置（可立即使用）
仅需要 `DB_ENCRYPTION_KEY`，其他配置均为可选。

### 可选集成
| 功能          | 环境变量            | 注册地址                |
|----------------|------------------|----------------------|
| 银行账户同步      | `POWENS_CLIENT_ID`, `POWENS_CLIENT_SECRET`, `POWENS_DOMAIN` | [powens.com](https://powens.com)       |
| 生产环境认证      | `CLERK_SECRET_KEY`, `VITE_CLERK_PUBLISHABLE_KEY` | [clerk.com](https://clerk.com)       |
| Coinbase       | `COINBASE_CLIENT_ID`, `COINBASE_CLIENT_SECRET` | [developers.coinbase.com](https://developers.coinbase.com) |
| Google Drive     | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | [console.cloud.google.com](https://console.cloud.google.com) |

## 运行

```bash
# Start both frontend + backend
npm run dev
```

- 前端：http://localhost:3004/konto/
- 后端 API：http://localhost:5004/api/
- 登录方式：`user` / `user`（本地开发环境，无需使用 Clerk）

## 沙箱/演示模式

Konto 会为默认用户自动填充演示数据：
- 银行账户（支票账户、储蓄账户、投资账户）
- 加密货币钱包（BTC、ETH、XRP）
- 投资持仓
- 14个月的交易记录
- 房产和车辆资产信息

只需登录即可使用，无需外部 API 密钥。

## 部署到生产环境

```bash
npm run build
# Frontend: serve frontend/dist/ as static files
# Backend: node backend/dist/index.js
```

### 使用 Vercel 进行部署
```bash
cd frontend && vercel
cd backend && vercel
```

## 端口配置

| 服务          | 端口            | URL                    |
|----------------|------------------|----------------------|
| 前端（开发环境）     | 3004            | http://localhost:3004/konto/         |
| 后端 API       | 5004            | http://localhost:5004/api/         |

## 故障排除

| 问题                | 解决方案                |
|------------------|----------------------|
| `ENCRYPTION_KEY` 错误     | 运行 `openssl rand -hex 32` 并将其设置到 `backend/.env` 文件中 |
| 端口 3004 被占用       | 使用 `lsof -i :3004` 查找占用该端口的进程，然后终止该进程或修改 `VITE_DEV_PORT` |
| 端口 5004 被占用       | 修改 `backend/.env` 文件中的 `PORT` 值       |
| 在本地环境中遇到 Clerk 错误     | 将 `CLERK_SECRET_KEY` 空置（绕过 Clerk 服务） |
| 仪表盘显示为空         | 以 `user/user` 身份登录（首次启动后仪表盘会显示演示数据） |
| 银行账户同步失败       | 需要 Powens 的 API 密钥（演示模式可选） |

## 技术栈

| 层次        | 技术栈                |
|--------------|----------------------|
| 前端          | React 18 + TypeScript + Vite + Tailwind CSS + Recharts |
| 后端          | Hono + TypeScript + Node.js         |
| 数据库        | SQLite（本地）或 Turso（云存储）       |
| 认证系统        | Clerk（可选）              |

## 主要 API 端点

| 端点          | 描述                        |
|----------------|--------------------------------------|
| `GET /api/bank/accounts` | 获取银行账户信息            |
| `GET /api/investments` | 获取投资持仓信息            |
| `GET /api/transactions` | 获取交易记录                |
| `GET /api/companies` | 获取公司信息（仅限专业用户）         |
| `GET /api/patrimoine/summary` | 获取净资产概览            |
| `GET /apipreferences` | 获取用户偏好设置              |

完整 API 文档请参阅仓库中的 `docs/API.md` 文件。