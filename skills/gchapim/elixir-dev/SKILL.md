---
name: elixir-dev
description: "Elixir/Phoenix 开发辅助工具。可以运行并解释 `mix test`、`mix credo`、`mix dialyzer`、`mix format` 等命令；遵循 OTP（Elixir Template Project）规范生成模块（包括上下文、数据模型、GenServers、Supervisors、Tasks 等）。能够调试编译错误和警告；支持 Ecto 迁移、数据库查询、变更集（changesets）以及关联（associations）操作。适用于各种 Elixir 或 Phoenix 开发任务，如编写模块、修复测试代码、重构代码或理解 OTP 设计模式。"
---

# Elixir 开发

## 运行 Mix 命令

有关完整的命令参考，请参阅 [references/mix-commands.md](references/mix-commands.md)。

### 测试

```bash
# Run all tests
mix test

# Specific file or line
mix test test/my_app/accounts_test.exs:42

# By tag
mix test --only integration

# Failed only (requires --failed flag from prior run)
mix test --failed

# With coverage
mix test --cover
```

**故障解析：**
- `** (MatchError)` — 模式匹配失败；请检查返回值的格式。
- `** (Ecto.NoResultsError)` — 使用不存在的 ID 调用 `Repo.get!`；请使用 `Repo.get` 或生成测试数据。
- `** (DBConnection.OwnershipError)` — 缺少 `async: true` 选项或未设置沙箱环境。
- `no function clause matching` — 参数数量不正确或参数类型不符合预期。

### Credo

```bash
mix credo --strict
mix credo suggest --format json
mix credo explain MyApp.Module  # Explain issues for specific module
```

**常见的 Credo 代码优化建议：**
- `Credo.Check.Readability.ModuleDoc` — 为模块添加 `@moduledoc` 注解。
- `Credo.Check.Refactor.CyclomaticComplexity` — 提取辅助函数。
- `Credo.Check.Design.TagTODO` — 处理或删除 TODO 注释。

### Dialyzer

```bash
mix dialyzer
mix dialyzer --format short
```

**常见的 Dialyzer 警告：**
- `The pattern can never match` — 模式中的代码无法被匹配；或者类型不正确。
- `Function has no local return` — 函数在所有路径上都会导致崩溃；请检查内部调用。
- `The call will never return` — 调用的函数总是会抛出异常。
- 解决方法：添加 `@spec` 注解；作为最后手段，可以使用 `@dialyzer {:nowarn_function, func: arity}`。

### 格式化

```bash
mix format
mix format --check-formatted  # CI mode — exit 1 if unformatted
```

## 模块编写规范

在公共函数上始终添加 `@moduledoc`、`@doc` 和 `@spec` 注解。

### Context 模块

```elixir
defmodule MyApp.Notifications do
  @moduledoc """
  Manages notification delivery and preferences.
  """
  import Ecto.Query
  alias MyApp.Repo
  alias MyApp.Notifications.Notification

  @doc "List notifications for a user, most recent first."
  @spec list_notifications(String.t(), keyword()) :: [Notification.t()]
  def list_notifications(user_id, opts \\ []) do
    limit = Keyword.get(opts, :limit, 50)

    Notification
    |> where(user_id: ^user_id)
    |> order_by(desc: :inserted_at)
    |> limit(^limit)
    |> Repo.all()
  end
end
```

### Schema 模块

```elixir
defmodule MyApp.Notifications.Notification do
  @moduledoc """
  Schema for push/email/sms notifications.
  """
  use Ecto.Schema
  import Ecto.Changeset

  @type t :: %__MODULE__{}

  @primary_key {:id, :binary_id, autogenerate: true}
  @foreign_key_type :binary_id
  @timestamps_opts [type: :utc_datetime_usec]

  schema "notifications" do
    field :channel, Ecto.Enum, values: [:push, :email, :sms]
    field :title, :string
    field :body, :string
    field :delivered_at, :utc_datetime_usec
    field :user_id, :binary_id

    timestamps()
  end

  @required ~w(channel title body user_id)a

  @doc false
  def changeset(notification, attrs) do
    notification
    |> cast(attrs, @required ++ [:delivered_at])
    |> validate_required(@required)
    |> validate_length(:title, max: 255)
  end
end
```

## OTP 模式

有关 GenServer、Supervisor、Agent 和 Task 的模式，请参阅 [references/otp-patterns.md](references/otp-patterns.md)。

### 何时使用哪种模式

| 模式 | 使用场景 |
|---------|----------|
| GenServer | 具有同步/异步调用状态的管理进程（例如缓存、速率限制器、连接池） |
| Agent | 无需复杂逻辑的简单状态封装 |
| Task | 一次性异步任务，执行后即可忽略 |
| Task.Supervisor | 监控并执行一次性任务 |
| Supervisor | 管理子进程的生命周期 |
| Registry | 通过名称/键查找进程 |
| DynamicSupervisor | 在运行时启动子进程 |

### GenServer 模板

```elixir
defmodule MyApp.RateLimiter do
  @moduledoc "Token bucket rate limiter."
  use GenServer

  # Client API
  def start_link(opts) do
    name = Keyword.get(opts, :name, __MODULE__)
    GenServer.start_link(__MODULE__, opts, name: name)
  end

  @spec check_rate(String.t()) :: :ok | {:error, :rate_limited}
  def check_rate(key), do: GenServer.call(__MODULE__, {:check, key})

  # Server callbacks
  @impl true
  def init(opts) do
    {:ok, %{limit: Keyword.get(opts, :limit, 100), window_ms: 60_000, buckets: %{}}}
  end

  @impl true
  def handle_call({:check, key}, _from, state) do
    now = System.monotonic_time(:millisecond)
    {count, state} = increment(state, key, now)
    if count <= state.limit, do: {:reply, :ok, state}, else: {:reply, {:error, :rate_limited}, state}
  end

  defp increment(state, key, now) do
    # Implementation
  end
end
```

## 常见的编译错误

| 错误 | 原因 | 解决方法 |
|-------|-------|-----|
| `module X is not available` | 缺少依赖项或拼写错误 | 检查 `mix.exs` 文件中的依赖项列表，并验证模块名称 |
| `undefined function X/N` | 模块未被导入或别名未正确设置 | 添加 `import` 语句、别名或完整的模块路径 |
| `(CompileError) redefining module` | 模块名称重复 | 为其中一个模块重新命名 |
| `protocol not implemented` | 缺少协议实现 | 为相关结构体添加 `defimpl` 方法 |
| `cannot use ^x outside of match` | `^x` 的使用位置不正确 | 将其移至模式匹配的上下文中 |

## Ecto 查询模式

### 动态过滤器

```elixir
def list(filters) do
  Enum.reduce(filters, base_query(), fn
    {:status, val}, q -> where(q, [r], r.status == ^val)
    {:since, dt}, q -> where(q, [r], r.inserted_at >= ^dt)
    {:search, term}, q -> where(q, [r], ilike(r.name, ^"%#{term}%"))
    _, q -> q
  end)
  |> Repo.all()
end
```

### 预加载

```elixir
# Query-time preload (single query with join)
from(p in Post, join: a in assoc(p, :author), preload: [author: a])

# Separate query preload
Post |> Repo.all() |> Repo.preload(:author)

# Nested
Repo.preload(posts, [comments: :author])
```

### 聚合操作

```elixir
from(o in Order,
  where: o.tenant_id == ^tenant_id,
  group_by: o.status,
  select: {o.status, count(o.id), sum(o.amount)}
)
|> Repo.all()
```

## Phoenix LiveView 基础知识

### 绑定组件 + 处理事件

```elixir
defmodule MyAppWeb.DashboardLive do
  use MyAppWeb, :live_view

  @impl true
  def mount(_params, _session, socket) do
    {:ok, assign(socket, items: [], loading: true)}
  end

  @impl true
  def handle_event("delete", %{"id" => id}, socket) do
    MyApp.Items.delete_item!(id)
    {:noreply, assign(socket, items: MyApp.Items.list_items())}
  end

  @impl true
  def render(assigns) do
    ~H"""
    <div :for={item <- @items}>
      <span><%= item.name %></span>
      <button phx-click="delete" phx-value-id={item.id}>Delete</button>
    </div>
    """
  end
end
```

### 使用 PubSub 实现实时通信

```elixir
# Subscribe in mount
def mount(_, _, socket) do
  if connected?(socket), do: Phoenix.PubSub.subscribe(MyApp.PubSub, "items")
  {:ok, assign(socket, items: list_items())}
end

# Broadcast from context
def create_item(attrs) do
  with {:ok, item} <- %Item{} |> Item.changeset(attrs) |> Repo.insert() do
    Phoenix.PubSub.broadcast(MyApp.PubSub, "items", {:item_created, item})
    {:ok, item}
  end
end

# Handle in LiveView
def handle_info({:item_created, item}, socket) do
  {:noreply, update(socket, :items, &[item | &1])}
end
```