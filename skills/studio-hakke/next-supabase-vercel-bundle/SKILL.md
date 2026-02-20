---
name: next-supabase-vercel-bundle
description: >
  **全栈开发周期的真正协调者：**  
  该工具能够连接到 Supabase 数据库，生成可执行的 SQL 迁移脚本，并提供详细的操作指导。同时支持与 Vercel 的集成，实现自动部署功能。
metadata: {
  "clawdbot": {
    "emoji": "🚀",
    "requires": {
      "bins": ["node", "npm", "vercel", "npx"],
      "user-invocable": false
    }
  }
}
---
# Next-Supabase-Vercel 组件包

**Next.js + Supabase + Vercel 开发的真正“指挥官”**

这个组件不仅仅是一个基础的开发框架，它是一个完整的端到端开发流程自动化工具：

- ✅ 自动连接到 Supabase 并测试连接是否正常
- ✅ 生成可执行的 SQL 迁移脚本
- ✅ 在 Supabase 控制面板中配置身份验证（生成相应的 SQL 语句）
- ✅ 在 Supabase 控制面板中配置存储系统（生成相应的 SQL 语句）
- ✅ 自动部署到 Vercel
- ✅ 为每个手动配置步骤提供详细的指导
- ✅ 提供错误处理和状态监控功能

**价值：** 从原本需要 3+ 小时的工作，现在只需 30 秒即可完成！

---

## 使用场景

- 创建配置齐全的 Next.js + Supabase 项目
- 配置数据库并执行迁移操作
- 设置身份验证和存储系统
- 自动部署到 Vercel
- 快速原型制作以展示项目想法

---

## 快速入门

```bash
# Crear proyecto con auth + database (RECOMENDADO)
snv init my-app --template auth-db

# Configurar database (auto-conecta + genera migrations)
cd my-app
snv db:setup

# Configurar authentication (genera SQL + guía)
snv auth:setup

# Configurar storage (genera SQL + guía) - opcional
snv storage:setup --buckets avatars,documents

# Iniciar desarrollo local
snv dev

# Deployar automáticamente a Vercel
snv deploy
```

---

## 可用命令

### `snv init <project-name>` - 创建并配置项目

```bash
snv init my-app
snv init my-app --template auth-db
```

**功能：**
1. 创建 Next.js 项目结构
2. 配置 Supabase 客户端
3. 生成包含占位符的 `.env.local` 和 `.env.example` 文件
4. 创建 `supabase/migrations/` 目录
5. 生成包含预配置依赖的 `package.json`
6. 创建包含下一步操作指南的首页
7. 生成 TypeScript 的 `tsconfig.json` 配置文件
8. 初始化 Git 仓库

**参数：**
- `--template <name>`：使用的模板类型
  - `minimal`：基础版（Next.js + Supabase 客户端）
  - `auth-db`：**推荐**：包含身份验证和数据库功能
  - `auth`：仅包含身份验证功能
  - `full`：包含身份验证、数据库和存储系统功能
- `--no-typescript`：禁用 TypeScript
- `--no-tailwind`：禁用 Tailwind CSS
- `--no-eslint`：禁用 ESLint

**输出：**
```
✅ Proyecto my-app creado exitosamente!

Siguientes pasos:
1. Editar .env.local con tus credenciales de Supabase
2. Ejecutar: snv db:setup (configura DB + migrations)
3. (Opcional) Ejecutar: snv auth:setup (configura Auth)
4. (Opcional) Ejecutar: snv storage:setup (configura Storage)
5. Ejecutar: snv dev (iniciar desarrollo)

Para comenzar:
  cd my-app
  snv dev
```

---

### `snv db:setup` - 配置数据库

```bash
snv db:setup
```

**功能：**
1. **检查 `.env.local` 文件**：需要 `NEXT_PUBLIC_SUPABASE_URL` 和 `SUPABASE_SERVICE_KEY`
2. **连接到 Supabase**：通过简单查询测试连接
3. **查找迁移脚本**：扫描 `supabase/migrations/` 目录中的 SQL 文件
4. **生成迁移总结**：创建 `supabase/migrations-summary.md` 文件，列出所有迁移操作
5. **生成使用指南**：提供在 Supabase 控制面板中执行迁移的步骤说明
6. **自动执行迁移**（如果配置正确）

**生成的 SQL 迁移脚本示例：**
- 身份验证迁移脚本（用于启用身份验证功能）

**迁移脚本示例：**
- 启用多种身份验证方式（邮箱、Google、GitHub）
- 创建应用程序相关表格
- 配置行级安全（Row Level Security, RLS）
- 自动创建触发器

**输出：**
```sql
-- Habilitar Authentication en Supabase

-- 1. Habilitar Email Auth
alter schema auth.users enable row level security;

-- 2. Crear tabla de usuarios (ejemplo)
create table if not exists public.users (
  id uuid default gen_random_uuid() primary key,
  email text unique not null,
  created_at timestamp with time zone default timezone('utc', now()) not null,
  updated_at timestamp with time zone default timezone('utc', now()) not null
);

-- 3. Configurar RLS para usuarios
alter table public.users enable row level security;

create policy "Usuarios pueden ver su propio perfil"
on public.users for select
using (auth.uid())
with check (auth.uid() = id);

grant select;
```

---

### `snv auth:setup` - 配置身份验证

```bash
snv auth:setup
```

**功能：**
1. **检查 `.env.local` 文件**：需要身份验证凭据
2. **连接到 Supabase**：确认身份验证功能已启用
3. **生成 SQL 迁移脚本**：创建 `002_enable_auth.sql`，包含以下内容：
  - 启用邮箱身份验证
  - 创建 `users` 表
  - 配置行级安全（RLS）
4. **生成使用指南**：提供直接访问 Supabase 控制面板的链接
5. **生成身份验证相关页面**（如果不存在的话）：
  - `src/app/auth/login/page.tsx`
  - `src/app/auth/signup/page.tsx`
  - `src/lib/auth.ts`（包含辅助函数）

**生成的 SQL 迁移脚本示例：**
```sql
-- Habilitar Authentication en Supabase

-- 1. Habilitar Email Auth
alter schema auth.users enable row level security;

-- 2. Crear tabla de usuarios
create table if not exists public.users (
  id uuid default gen_random_uuid() primary key,
  email text unique not null,
  created_at timestamp with time zone default timezone('utc', now()) not null,
  updated_at timestamp with time zone default timezone('utc', now()) not null
);

-- 3. Configurar RLS para usuarios
alter table public.users enable row level security;

create policy "Usuarios pueden ver su propio perfil"
on public.users for select
using (auth.uid())
with check (auth.uid() = id);

grant select;
```

**输出：**
```
🔐 Checking authentication setup...
✅ Authentication enabled in Supabase

📋 Creating auth migration...
✅ Migration creada: 002_enable_auth.sql

📄 Creating auth pages...
  src/app/auth/login/page.tsx
  src/app/auth/signup/page.tsx
  src/lib/auth.ts

📋 Pasos para completar configuración:

ABRIR el Supabase Dashboard: https://supabase.com/dashboard/project/_/auth/providers

1. Habilita Email Auth (Authentication > Providers > Email)
2. (Opcional) Agrega Google OAuth (Authentication > Providers > Google)

Luego ejecuta la migration 002_enable_auth.sql en SQL Editor:
https://supabase.com/dashboard/project/_/sql/new

✅ Auth setup completado!

Notas importantes:
- Las páginas de login/signup ya existen en tu proyecto
- Revisa src/lib/supabase.ts para la configuración de Auth
- Los RLS policies (Row Level Security) se aplican automáticamente
```

---

### `snv storage:setup` - 配置存储系统

```bash
snv storage:setup
snv storage:setup --buckets avatars,documents
```

**功能：**
1. **检查 `.env.local` 文件**：需要身份验证凭据
2. **连接到 Supabase**：确认存储系统已启用
3. **生成 SQL 迁移脚本**：创建 `003_enable_storage.sql`，包含以下内容：
  - 创建存储桶
  - 配置行级安全策略（RLS）
4. **生成使用指南**：提供直接访问存储系统的链接

**生成的 SQL 迁移脚本示例：**
```sql
-- Habilitar Storage en Supabase

-- 1. Crear buckets de ejemplo
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values 
  ('avatars', 'avatars', true, 5242880, 'image/jpeg,image/png,image/gif'),
  ('documents', 'documents', true, 52428800, 'application/pdf,application/msword,text/plain')
on conflict (id) do nothing;

-- 2. Configurar políticas RLS
-- NOTA: Las políticas deben configurarse manualmente en el Dashboard
-- URL: https://supabase.com/dashboard/project/_/storage/policies

-- Ejemplo de política para acceso público a avatars
create policy "Acceso público a avatars"
on storage.objects for select
using (bucket_id)
with check (bucket_id in ('avatars'))
grant select;
```

---

### `snv dev` - 启动本地开发环境

```bash
snv dev
snv dev --port 3000
```

**功能：**
1. 检查 `.env.local` 文件是否存在
2. 启动 Next.js 服务器：`npm run dev`
3. 显示本地开发地址：`http://localhost:3000`

**输出：**
```
🚀 Starting development server...
✅ Dev server iniciado en: http://localhost:3000

Presiona Ctrl+C para detener
```

---

### `snv deploy` - 部署到 Vercel

```bash
snv deploy
snv deploy --prod
```

**功能：**
1. **检查 Vercel CLI 是否已安装**：如果未安装，会提示安装指令
2. **检查项目是否已链接到 Vercel**：如果没有链接，会提示使用 `vercel link --yes` 命令进行链接
3. **构建项目**：执行 `npm run build`
4. **部署到 Vercel**：执行 `vercel deploy` 或 `vercel deploy --prod`
5. **解析部署结果**：显示部署地址
6. **检查环境变量**：检查是否有缺失的环境变量

**输出：**
```
🔍 Checking Vercel CLI...
✅ Vercel CLI listo

🔨 Building project...
✅ Build completado

🚀 Deploying to Vercel...
✅ Deploy completado!

🌐 Deployment URL:
  https://my-app.vercel.app

📝 Environment variables en Vercel:

DEBES CONFIGURARLAS MANUALMENTE EN EL DASHBOARD DE VERCEL:
https://vercel.com/dashboard

Variables requeridas:
  NEXT_PUBLIC_SUPABASE_URL
  NEXT_PUBLIC_SUPABASE_ANON_KEY
  SUPABASE_SERVICE_KEY

⚠️  NOTA: Asegúrate de configurar estas variables en Vercel para que funcione en producción
```

---

## 可用模板

| 模板类型 | 描述 | 特点 |
|----------|-------------|------------|
| `minimal` | 基础版 | Next.js + Supabase 客户端 |
| `auth-db` | **推荐** | 包含身份验证和数据库功能 |
| `auth` | 仅包含身份验证功能 | 提供登录/注册页面和辅助函数 |
| `full` | 完整版 | 包含身份验证、数据库和存储系统功能 |

---

## 环境变量

**所有项目通用：**

```bash
# .env.local
NEXT_PUBLIC_SUPABASE_URL=https://yourproject.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key_here

# Service role key (requerido para snv db:setup)
SUPABASE_SERVICE_KEY=your_service_role_key_here
```

**获取凭据地址：**
- https://supabase.com/dashboard/project/_/settings/api

---

## 组件的工作原理

1. **初始化阶段 (`snv init`)**
   - 创建基本的项目结构
   - 生成配置文件
   - 不会在 Supabase 中安装任何依赖

2. **连接阶段 (`snv db:setup`)**
   - 从 `.env.local` 文件中读取凭据
   - 使用服务角色密钥连接到 Supabase
   - 通过简单查询测试连接
   - 生成可执行的 SQL 迁移脚本

3. **配置阶段 (`snv auth:setup`, `snv storage:setup`)**
   - 生成可执行的 SQL 迁移脚本
   - 如果需要，创建登录/注册页面
   - 提供详细的操作指南
   - 提供直接访问 Supabase 控制面板的链接

4. **开发阶段 (`snv dev`)**
   - 检查配置是否正确
   - 启动 Next.js 服务器
   - 显示本地开发地址

5. **部署阶段 (`snv deploy`)**
   - 检查 Vercel CLI 是否已安装
   - 构建项目
   - 将项目部署到 Vercel
   - 解析部署结果并显示地址
   - 检查是否有缺失的环境变量

### 生成的 SQL 迁移脚本

**身份验证迁移脚本示例 (`002_enable_auth.sql`)：**
```sql
-- Habilitar Authentication en Supabase

-- 1. Habilitar Email Auth
alter schema auth.users enable row level security;

-- 2. Crear tabla de usuarios
create table if not exists public.users (
  id uuid default gen_random_uuid() primary key,
  email text unique not null,
  created_at timestamp with time zone default timezone('utc', now()) not null,
  updated_at timestamp with time zone default timezone('utc', now()) not null
);

-- 3. Configurar RLS para usuarios
alter table public.users enable row level security;

create policy "Usuarios pueden ver su propio perfil"
on public.users for select
using (auth.uid())
with check (auth.uid() = id);

grant select;
```

**存储系统迁移脚本示例 (`003_enable_storage.sql`)：**
```sql
-- Habilitar Storage en Supabase

-- 1. Crear buckets de ejemplo
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values 
  ('avatars', 'avatars', true, 5242880, 'image/jpeg,image/png,image/gif'),
  ('documents', 'documents', true, 52428800, 'application/pdf,application/msword,text/plain')
on conflict (id) do nothing;

-- 2. Nota: Las políticas RLS deben configurarse manualmente
-- En Dashboard: https://supabase.com/dashboard/project/_/storage/policies
```

---

## 常见问题及解决方法

### 错误：“No such built-in module: node:sqlite”

**解决方法：** 将 Node.js 升级到 v22.22.0 或更高版本。

```bash
# Verificar versión
node --version

# Actualizar NVM
nvm install 22.22.0
nvm alias default 22.22.0

# O actualizar symlink de sistema (Linux)
sudo ln -sf ~/.nvm/versions/node/v22.22.0/bin/node /usr/local/bin/node
```

### 错误：“.env.local 文件未找到”

**解决方法：** 先执行 `snv init` 命令。

### 错误：“无法连接到 Supabase”

**解决方法：**
1. 确认 `.env.local` 文件中的凭据正确
2. 确认项目 ID 是否正确
3. 在 Supabase 控制面板中确认身份验证功能已启用

### 错误：“Vercel CLI 未安装”

**解决方法：** 安装 Vercel CLI：`npm i -g vercel`

### 错误：“项目未链接到 Vercel”

**解决方法：** 确保项目已正确链接到 Vercel。

---

## 完整工作流程示例

### 工作流程 1：新建带有身份验证和数据库的应用程序

```bash
# 1. Crear proyecto
snv init my-app --template auth-db

# 2. Configurar credenciales
cd my-app
# Editar .env.local con:
# NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
# NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
# SUPABASE_SERVICE_KEY=eyJ...

# 3. Configurar database (auto-conecta + migrations)
snv db:setup

# 4. Configurar authentication (genera SQL)
snv auth:setup

# 5. Ejecutar migrations en Supabase Dashboard
# ABRE: https://supabase.com/dashboard/project/_/sql/new
# Copia y ejecuta 002_enable_auth.sql

# 6. Iniciar desarrollo
snv dev
```

### 工作流程 2：部署到生产环境

```bash
# 1. En desarrollo
cd my-app

# 2. Build y deploy
snv deploy --prod

# 3. Configurar env vars en Vercel Dashboard
# ABRE: https://vercel.com/dashboard
# Agrega: NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY, SUPABASE_SERVICE_KEY
```

### 工作流程 3：为头像添加存储系统

```bash
# 1. En desarrollo
cd my-app

# 2. Configurar storage (genera SQL)
snv storage:setup --buckets avatars

# 3. Ejecutar migration en Supabase Dashboard
# ABRE: https://supabase.com/dashboard/project/_/sql/new
# Copia y ejecuta 003_enable_storage.sql

# 4. Configurar políticas RLS en Supabase Dashboard
# ABRE: https://supabase.com/dashboard/project/_/storage/policies
```

---

## 系统要求

- **Node.js 18+**（建议使用 20+）
- **npm 或 yarn 或 pnpm**
- **Supabase 账户**（免费账户即可使用）
- **Vercel 账户**（免费账户即可使用）
- **安装 Vercel CLI**：`npm i -g vercel`

---

## 与其他工具的比较

### 与单独的工具（nextjs, vercel, supabase）相比

- 单独的工具：只是提供参考指南，用户需要手动执行命令
- 没有自动化流程管理

**我们的组件：**
- ✅ 自动化整个开发流程
- ✅ 生成可执行的 SQL 迁移脚本
- ✅ 为手动配置提供详细指导
- ✅ 自动部署并检测潜在问题

### 与 Antfarm 工作流程的比较

- Antfarm：依赖多个专用代理和定时任务
- 使用 SQLite 和 Cron 作业进行任务调度
- 数据库中保存状态信息
- 适用于开发团队

**我们的组件：**
- **类似的设计**：通过命令生成 SQL 和操作指南
- **专注于配置流程**（而非功能开发）
- **每个用户只需执行一个命令**（无需管理多个代理）

---

## 贡献方式

这个组件是开源的。如果您希望改进它，可以：

1. 在 GitHub 上克隆项目
2. 创建一个功能分支
3. 提交 Pull Request

欢迎提出以下方面的改进：
- 提供更多模板
- 集成更多服务（如 Cloudflare、Netlify）
- 实现自动化测试
- 改进错误处理机制

---

**Next.js + Supabase + Vercel 的真正“指挥官”——从项目构思到部署，只需 30 秒即可完成。** 🚀