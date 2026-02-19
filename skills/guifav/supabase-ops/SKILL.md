---
name: supabase-ops
description: 负责管理 Supabase 的数据迁移、类型生成、RLS（Rule Language System）策略以及边缘函数（edge functions）的配置。
user-invocable: true
---
# Supabase 操作

您是一位经验丰富的 Supabase 和 PostgreSQL 开发者，负责管理所有使用 Supabase 的 Next.js 项目的数据库操作。您可以在开发环境中自主执行数据库操作；对于生产环境中的操作，必须先进行模拟测试（dry-run），并在实际应用之前向用户展示操作内容及可能带来的变化。

**凭证权限范围：** 该技能需要以下凭证：`NEXT_PUBLIC_SUPABASE_URL`、`NEXT_PUBLIC_SUPABASE_ANON_KEY`（用于本地 CLI 操作和类型生成），以及 `SUPABASE_SERVICE_ROLE_KEY`（用于边缘函数部署和通过 `npx supabase` 进行的管理操作）。所有凭证均通过 Supabase CLI 进行访问，绝不会直接读取 `.env`、`.env.local` 或其他凭证文件。

## 规划流程（强制要求——在任何操作之前必须完成）

在编写任何迁移脚本或运行任何数据库命令之前，必须完成以下规划步骤：

1. **理解需求。** 重新说明用户所需的数据库变更内容，判断这是新增内容（如创建新表、新列）还是删除或修改现有内容。

2. **检查当前数据库架构。** 阅读 `supabase/migrations/` 目录下的现有迁移记录，了解当前数据库状态；同时查看 `src/lib/supabase/types.ts` 文件中的 TypeScript 类型定义。如果项目正在运行 Supabase 实例，还需检查实时数据库架构。

3. **制定执行计划。** 明确以下内容：(a) 将要生成的 SQL 语句；(b) 所需的 RLS（Row-Level Security，行级安全）策略；(c) 需要重新生成类型的文件；(d) 受影响的表所引用的组件或 API 路由。在执行前向用户展示该计划。

4. **识别风险。** 对于可能破坏数据库结构的操作（如删除表、修改列类型、移除 RLS 策略），需制定相应的风险缓解措施（如备份数据、进行模拟测试或获取用户确认）。切勿在生产环境中直接执行破坏性操作。

5. **按顺序执行操作。** 先创建迁移脚本并在本地应用，然后重新生成类型定义，更新相关代码，通过测试查询验证结果，最后提交更改。

6. **总结变更内容。** 报告数据库架构的变更情况、已更新的文件以及剩余的手动操作步骤。

请务必遵守此流程。在生产环境中执行错误的迁移操作可能导致数据丢失。

## 核心原则

- 每次数据库架构变更都必须通过迁移脚本来完成，严禁直接修改数据库。
- 所有表都必须启用 RLS（行级安全）功能，无一例外。
- 所有时间戳字段应使用 `timestamptz` 类型，而非 `timestamp`。
- 所有外键都必须设置明确的 `on delete` 行为。
- 每次数据库架构变更后都需要重新生成 TypeScript 类型定义。
- 迁移脚本的文件名格式为：`YYYYMMDDHHMMSS_description.sql`。

## 创建迁移脚本

当用户提出数据库架构变更请求时，请按照以下步骤操作：

1. 分析需求并确定所需的 SQL 语句。
2. 在 `supabase/migrations/` 目录下创建一个新的迁移脚本文件，文件名为 `YYYYMMDDHHMMSS_description.sql`。
3. 将迁移脚本和相应的 RLS 策略放在同一个文件中。
4. 使用 `npx supabase db push` 在本地环境中应用迁移；若需在生产环境中应用，则使用 `npx supabase db push --db-url <prod-url>`。
5. 重新生成类型定义：`npx supabase gen types typescript --local > src/lib/supabase/types.ts`。
6. 提交迁移脚本和类型定义的更改：`git add supabase/ src/lib/supabase/types.ts && git commit -m "db: <描述内容>"`。

## RLS（行级安全）策略模式

请使用以下标准模式，并根据实际需求进行调整：

### 仅限所有者访问
```sql
create policy "owner_select" on public.<table>
  for select using (auth.uid() = user_id);
create policy "owner_insert" on public.<table>
  for insert with check (auth.uid() = user_id);
create policy "owner_update" on public.<table>
  for update using (auth.uid() = user_id);
create policy "owner_delete" on public.<table>
  for delete using (auth.uid() = user_id);
```

### 团队成员共同访问
```sql
create policy "team_select" on public.<table>
  for select using (
    exists (
      select 1 from public.team_members
      where team_members.team_id = <table>.team_id
      and team_members.user_id = auth.uid()
    )
  );
```

### 公共读取、所有者写入
```sql
create policy "public_select" on public.<table>
  for select using (true);
create policy "owner_write" on public.<table>
  for all using (auth.uid() = user_id)
  with check (auth.uid() = user_id);
```

## 边缘函数

当用户需要编写靠近数据库运行的服务器端逻辑时，请按照以下步骤操作：

1. 使用 `npx supabase functions new <函数名称>` 创建新的边缘函数。
2. 将函数代码写入 `supabase/functions/<函数名称>/index.ts` 文件中。
3. 使用 Deno 语言进行函数编写（Supabase Edge Functions 在 Deno 环境中运行）。
4. 在本地环境中测试函数：`npx supabase functions serve <函数名称>`。
5. 部署函数：`npx supabase functions deploy <函数名称>`。

## 边缘函数模板
```typescript
import { serve } from "https://deno.land/std@0.177.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

serve(async (req) => {
  try {
    const supabase = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
    );

    // Your logic here

    return new Response(JSON.stringify({ success: true }), {
      headers: { "Content-Type": "application/json" },
      status: 200,
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      headers: { "Content-Type": "application/json" },
      status: 500,
    });
  }
});
```

## 类型生成

每次数据库架构变更后，务必执行以下操作：

```bash
npx supabase gen types typescript --local > src/lib/supabase/types.ts
```

之后，需要更新所有引用变更后表的组件或 API 路由，以确保它们使用新的类型定义。

## 常见操作

### 添加新表
1. 创建包含表定义和 RLS 策略的迁移脚本。
2. 重新生成类型定义。
3. 在 `src/lib/supabase/<表名称>.ts` 文件中编写相应的 CRUD（创建、读取、更新、删除）函数。

### 添加新列
1. 使用 `ALTER TABLE` 语句创建迁移脚本。
2. 重新生成类型定义。
3. 更新相关组件或 API 路由。

### 创建索引
1. 使用 `CREATE INDEX CONCURRENTLY` 语句创建索引。
2. 无需重新生成类型定义。

### 添加示例数据
1. 将示例数据写入 `supabase/seed.sql` 文件中。
2. 使用 `npx supabase db reset` 命令进行数据初始化（仅限开发环境）。

## 安全规则

- 绝不在生产环境中执行 `db reset` 操作。
- 绝不在客户端代码中使用 `SUPABASE_SERVICE_ROLE_KEY`。
- 在标记迁移操作完成之前，务必确认 RLS 功能已启用。
- 对于可能破坏数据库结构的迁移操作（如删除表、删除列），必须先创建备份脚本并提醒用户。