---
name: Env Typegen - TypeScript Types from .env
description: **从 `.env` 文件生成 TypeScript 类型（具备智能推断功能）**  
类型安全的环境变量；支持可选的 Zod 模式定义；提供免费的命令行工具（CLI）。
---

# Env Typegen

该工具能够从 `.env` 文件中生成 TypeScript 类型定义，针对数字、布尔值和 URL 等数据类型提供智能的类型推断功能。

## 安装

```bash
npm install -g @lxgicstudios/env-typegen
```

## 命令

### 生成类型定义

```bash
npx @lxgicstudios/env-typegen
npx @lxgicstudios/env-typegen .env.local
npx @lxgicstudios/env-typegen -o src/types/env.d.ts
```

### 使用 Zod Schema 生成类型定义

```bash
npx @lxgicstudios/env-typegen --zod
```

## 示例

输入 `.env` 文件内容：
```env
# Database
DATABASE_URL=postgresql://localhost:5432/db
DB_POOL_SIZE=10

# Server
PORT=3000
DEBUG=true

# API
API_KEY=sk_live_abc123
```

输出结果：
```typescript
export interface Env {
  /** Database */
  DATABASE_URL: string;
  DB_POOL_SIZE: number;
  /** Server */
  PORT: number;
  DEBUG: boolean;
  /** API */
  API_KEY: string;
}

export function getEnv(): Env {
  return {
    DATABASE_URL: process.env.DATABASE_URL || '',
    DB_POOL_SIZE: Number(process.env.DB_POOL_SIZE),
    PORT: Number(process.env.PORT),
    DEBUG: ['true', '1', 'yes'].includes(process.env.DEBUG?.toLowerCase() || ''),
    API_KEY: process.env.API_KEY || '',
  };
}

declare global {
  namespace NodeJS {
    interface ProcessEnv {
      DATABASE_URL: string;
      DB_POOL_SIZE: string;
      PORT: string;
      DEBUG: string;
      API_KEY: string;
    }
  }
}
```

## 类型推断规则：

| 模式          | 类型                |
|---------------|-------------------|
| `PORT=3000`      | number             |
| `DEBUG=true`     | boolean            |
| `API_URL=https://...`   | string (URL)          |
| `EMAIL=a@b.com`     | string (email)          |
| 其他所有内容      | string               |

## 选项

| 选项            | 描述                        |
|-----------------|---------------------------|
| `-i, --input`     | 输入文件（默认：.env）            |
| `-o, --output`     | 输出文件（默认：env.d.ts）         |
| `--zod`        | 同时生成 Zod Schema             |
| `--name`        | 接口名称（默认：Env）           |

## 常见使用场景：

- 为项目生成类型定义：  
  ```bash
npx @lxgicstudios/env-typegen -o src/types/env.d.ts
```

- 结合运行时验证功能使用：  
  ```bash
npx @lxgicstudios/env-typegen --zod -o src/env.ts
```

---

**由 [LXGIC Studios](https://lxgicstudios.com) 开发**

🔗 [GitHub](https://github.com/lxgicstudios/env-typegen) · [Twitter](https://x.com/lxgicstudios)