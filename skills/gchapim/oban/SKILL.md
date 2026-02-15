---
name: oban-designer
description: "设计和实现用于 Elixir 的 Oban 后台作业工作者。配置队列、重试策略、唯一性约束、Cron 调度以及错误处理机制。生成 Oban 工作者的配置文件，并进行测试。在将后台作业、异步处理、定时任务或周期性 Cron 作业添加到 Elixir 项目中时，可以使用 Oban。"
---

# Oban Designer

## 安装

```elixir
# mix.exs
{:oban, "~> 2.18"}

# config/config.exs
config :my_app, Oban,
  repo: MyApp.Repo,
  queues: [default: 10, mailers: 20, webhooks: 50, events: 5],
  plugins: [
    Oban.Plugins.Pruner,
    {Oban.Plugins.Cron, crontab: [
      {"0 2 * * *", MyApp.Workers.DailyCleanup},
      {"*/5 * * * *", MyApp.Workers.MetricsCollector}
    ]}
  ]

# In application.ex children:
{Oban, Application.fetch_env!(:my_app, Oban)}
```

生成 Oban 迁移文件：

```bash
mix ecto.gen.migration add_oban_jobs_table
```

```elixir
defmodule MyApp.Repo.Migrations.AddObanJobsTable do
  use Ecto.Migration
  def up, do: Oban.Migration.up(version: 12)
  def down, do: Oban.Migration.down(version: 1)
end
```

## 工作器实现

### 基本工作器

```elixir
defmodule MyApp.Workers.SendEmail do
  use Oban.Worker,
    queue: :mailers,
    max_attempts: 5,
    priority: 1

  @impl Oban.Worker
  def perform(%Oban.Job{args: %{"to" => to, "template" => template} = args}) do
    case MyApp.Mailer.deliver(to, template, args) do
      {:ok, _} -> :ok
      {:error, :temporary} -> {:error, "temporary failure"}  # Will retry
      {:error, :permanent} -> {:cancel, "invalid address"}   # Won't retry
    end
  end
end
```

### 返回值

| 返回值 | 含义 |
|--------|--------|
| `:ok` | 任务标记为已完成 |
| `{:ok, result}` | 任务标记为已完成，并返回结果 |
| `{:error, reason}` | 任务重试（计入尝试次数） |
| `{:cancel, reason}` | 任务被取消，不再重试 |
| `{:snooze, seconds}` | 任务被重新安排，不计入尝试次数 |
| `{:discard, reason}` | 任务被丢弃（Oban 2.17+ 版本） |

## 队列配置

有关常见的工作器模式，请参阅 [references/worker-patterns.md](references/worker-patterns.md)。

### 规模调整指南

| 队列类型 | 并发数 | 适用场景 |
|-------|------------|----------|
| `default` | 10 | 通用任务 |
| `mailers` | 20 | 邮件发送（I/O 密集型任务） |
| `webhooks` | 50 | Webhook 发送（I/O 密集型、高吞吐量任务） |
| `media` | 5 | 图像/视频处理（CPU 密集型任务） |
| `events` | 5 | 分析、审计日志处理 |
| `critical` | 3 | 计费、支付相关任务 |

### 队列优先级

队列中的任务按优先级执行（0 表示最高优先级）。请谨慎使用优先级设置：

```elixir
%{user_id: user.id}
|> MyApp.Workers.SendEmail.new(priority: 0)  # Urgent
|> Oban.insert()
```

## 重试策略

### 默认重试策略

Oban 使用指数级重试策略：`attempt^4 + attempt` 秒。

### 自定义重试策略

```elixir
defmodule MyApp.Workers.WebhookDelivery do
  use Oban.Worker,
    queue: :webhooks,
    max_attempts: 10

  @impl Oban.Worker
  def backoff(%Oban.Job{attempt: attempt}) do
    # Exponential with jitter: 2^attempt + random(0..30)
    trunc(:math.pow(2, attempt)) + :rand.uniform(30)
  end

  @impl Oban.Worker
  def perform(%Oban.Job{args: args}) do
    # ...
  end
end
```

### 超时设置

```elixir
use Oban.Worker, queue: :media

@impl Oban.Worker
def timeout(%Oban.Job{args: %{"size" => "large"}}), do: :timer.minutes(10)
def timeout(_job), do: :timer.minutes(2)
```

## 防止任务重复

```elixir
defmodule MyApp.Workers.SyncAccount do
  use Oban.Worker,
    queue: :default,
    unique: [
      period: 300,               # 5 minutes
      states: [:available, :scheduled, :executing, :retryable],
      keys: [:account_id]        # Unique by this arg key
    ]
end
```

### 独特性设置

| 设置项 | 默认值 | 说明 |
|--------|---------|-------------|
| `period` | 60 | 确保任务唯一性的时间间隔（`:infinity` 表示永久有效） |
| `states` | all active | 需检查的任务状态 |
| `keys` | all args | 需比较的参数键 |
| `timestamp` | `:inserted_at` | 使用 `:scheduled_at` 以确保定时任务的唯一性 |

### 替换现有任务

```elixir
%{account_id: id}
|> MyApp.Workers.SyncAccount.new(
  replace: [:scheduled_at],    # Update scheduled_at if duplicate
  schedule_in: 60
)
|> Oban.insert()
```

## Cron 调度

使用 Cron 表达式进行任务调度：`minute hour day_of_month month day_of_week`。

## 插入任务

```elixir
# Immediate
%{user_id: user.id, template: "welcome"}
|> MyApp.Workers.SendEmail.new()
|> Oban.insert()

# Scheduled
%{report_id: id}
|> MyApp.Workers.GenerateReport.new(schedule_in: 3600)
|> Oban.insert()

# Scheduled at specific time
%{report_id: id}
|> MyApp.Workers.GenerateReport.new(scheduled_at: ~U[2024-01-01 00:00:00Z])
|> Oban.insert()

# Bulk insert
changesets = Enum.map(users, fn user ->
  MyApp.Workers.SendEmail.new(%{user_id: user.id})
end)
Oban.insert_all(changesets)

# Inside Ecto.Multi
Ecto.Multi.new()
|> Ecto.Multi.insert(:user, changeset)
|> Oban.insert(:welcome_email, fn %{user: user} ->
  MyApp.Workers.SendEmail.new(%{user_id: user.id})
end)
|> Repo.transaction()
```

## Oban Pro 特性

仅限 Oban Pro 许可证用户使用：

### 批量处理（多个任务同时执行）

```elixir
# Process items in batch, run callback when all complete
batch = MyApp.Workers.ProcessItem.new_batch(
  items |> Enum.map(&%{item_id: &1.id}),
  callback: {MyApp.Workers.BatchComplete, %{batch_name: "import"}}
)
Oban.insert_all(batch)
```

### 工作流（任务依赖关系）

```elixir
Oban.Pro.Workflow.new()
|> Oban.Pro.Workflow.add(:extract, MyApp.Workers.Extract.new(%{file: path}))
|> Oban.Pro.Workflow.add(:transform, MyApp.Workers.Transform.new(%{}), deps: [:extract])
|> Oban.Pro.Workflow.add(:load, MyApp.Workers.Load.new(%{}), deps: [:transform])
|> Oban.insert_all()
```

### 分组处理（聚合多个任务）

```elixir
defmodule MyApp.Workers.BulkIndex do
  use Oban.Pro.Workers.Chunk,
    queue: :indexing,
    size: 100,            # Process 100 at a time
    timeout: 30_000       # Or after 30s

  @impl true
  def process(jobs) do
    items = Enum.map(jobs, & &1.args)
    SearchIndex.bulk_upsert(items)
    :ok
  end
end
```

## 测试

有关详细的测试模式，请参阅 [references/testing-oban.md](references/testing-oban.md)。

### 设置

```elixir
# config/test.exs
config :my_app, Oban,
  testing: :manual  # or :inline for synchronous execution

# test_helper.exs (if using :manual)
Oban.Testing.start()
```

### 确认任务已加入队列

```elixir
use Oban.Testing, repo: MyApp.Repo

test "enqueues welcome email on signup" do
  {:ok, user} = Accounts.register(%{email: "test@example.com"})

  assert_enqueued worker: MyApp.Workers.SendEmail,
    args: %{user_id: user.id, template: "welcome"},
    queue: :mailers
end
```

### 在测试中执行任务

```elixir
test "processes email delivery" do
  {:ok, _} =
    perform_job(MyApp.Workers.SendEmail, %{
      "to" => "user@example.com",
      "template" => "welcome"
    })
end
```

## 监控

### 监控事件

```elixir
# Attach in application.ex
:telemetry.attach_many("oban-logger", [
  [:oban, :job, :start],
  [:oban, :job, :stop],
  [:oban, :job, :exception]
], &MyApp.ObanTelemetry.handle_event/4, %{})
```

### 需要跟踪的关键指标

- 任务执行时间（p50、p95、p99 分位数）
- 队列深度（每个队列中的待处理任务数量）
- 每个工作器的错误率
- 每个工作器的重试率