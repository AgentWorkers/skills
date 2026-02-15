---
name: phoenix-api-gen
description: 根据 OpenAPI 规范或自然语言描述，生成完整的 Phoenix JSON API。该工具能够创建相关的数据模型（Ecto 模式）、数据库迁移脚本、控制器、JSON 视图/渲染器、路由规则、ExUnit 测试用例（包含测试工厂）、身份验证插件（auth plugs）以及租户权限管理功能。适用于构建新的 Phoenix REST API、添加 CRUD 端点、快速搭建项目结构，或将 OpenAPI YAML 文件转换为 Phoenix 项目。
---

# Phoenix API生成器

## 工作流程

### 从OpenAPI YAML生成API

1. 解析OpenAPI规范，提取路径、数据结构（schemas）以及请求/响应体。
2. 将每个数据结构映射到Ecto数据结构，并生成相应的数据库迁移脚本。
3. 将每个路径映射到相应的控制器方法；按资源类型进行分组。
4. 根据`securitySchemes`生成认证插件（auth plugs）。
5. 生成ExUnit测试，覆盖正常处理情况和验证错误的情况。

### 从自然语言描述生成API

1. 从描述中提取资源、字段、类型和关系信息。
2. 确定资源之间的上下文关系（将相关资源分组）。
3. 生成数据结构、迁移脚本、控制器、视图（views）以及路由（router）。
4. 在编写代码之前请用户确认所有信息。

## 文件生成顺序

1. 数据库迁移脚本（文件前缀为`YYYYMMDDHHMMSS`）
2. Ecto数据结构及相应的变更集（changesets）
3. 控制器及相关功能模块（CRUD操作）
4. JSON渲染器（Phoenix 1.7及以上版本使用`*JSON`模块；旧版本使用`*View`模块）
5. 路由逻辑及处理流程（router scope + pipelines）
6. 认证插件（auth plugs）
7. 测试代码及测试工厂（tests + factories）

## Phoenix项目规范

有关项目结构、命名规范和上下文模式的详细信息，请参阅[references/phoenix-conventions.md]。

**关键规则：**
- 每个有明确边界的功能模块对应一个独立的上下文（例如：`Accounts`、`Billing`、`Notifications`）。
- 控制器不应直接调用数据库存储层（Repo）。
- 数据结构应归属于相应的上下文（例如：`MyApp.Accounts.User`）。
- 控制器应通过上下文处理请求，并返回`{:ok, resource}`或`{:error, changeset}`。
- 使用`FallbackController`和`action_fallback/1`来处理错误情况。

## Ecto模式

有关数据结构、变更集（changesets）和迁移脚本（migrations）的详细信息，请参阅[references/ecto-patterns.md]。

**关键规则：**
- 始终使用`timestamps(type: :utc_datetime_usec)`作为时间戳字段。
- 对于二进制ID，使用`@primary_key{:id, :binary_id, autogenerate: true}`和`@foreign_key_type :binary_id`进行定义。
- 当创建或更新字段不同时，分别生成`create_changeset/2`和`update_changeset/2`迁移脚本。
- 在变更集中验证必填字段、格式和约束条件；不要在控制器中验证这些内容。

## 多租户支持

在每个租户相关的表中添加`tenant_id :binary_id`字段。示例代码如下：

```elixir
# In context
def list_resources(tenant_id) do
  Resource
  |> where(tenant_id: ^tenant_id)
  |> Repo.all()
end

# In plug — extract tenant from conn and assign
defmodule MyAppWeb.Plugs.SetTenant do
  import Plug.Conn
  def init(opts), do: opts
  def call(conn, _opts) do
    tenant_id = get_req_header(conn, "x-tenant-id") |> List.first()
    assign(conn, :tenant_id, tenant_id)
  end
end
```

**注意事项：**  
始终为`[:tenant_id, <resource_id 或查找字段>]`创建复合索引。

## 认证插件（Auth Plugs）

### API密钥（API Key）

```elixir
defmodule MyAppWeb.Plugs.ApiKeyAuth do
  import Plug.Conn
  def init(opts), do: opts
  def call(conn, _opts) do
    with [key] <- get_req_header(conn, "x-api-key"),
         {:ok, account} <- Accounts.authenticate_api_key(key) do
      assign(conn, :current_account, account)
    else
      _ -> conn |> send_resp(401, "Unauthorized") |> halt()
    end
  end
end
```

### 承载令牌（Bearer Token）

```elixir
defmodule MyAppWeb.Plugs.BearerAuth do
  import Plug.Conn
  def init(opts), do: opts
  def call(conn, _opts) do
    with ["Bearer " <> token] <- get_req_header(conn, "authorization"),
         {:ok, claims} <- MyApp.Token.verify(token) do
      assign(conn, :current_user, claims)
    else
      _ -> conn |> send_resp(401, "Unauthorized") |> halt()
    end
  end
end
```

## 路由结构（Router Structure）

```elixir
scope "/api/v1", MyAppWeb do
  pipe_through [:api, :authenticated]

  resources "/users", UserController, except: [:new, :edit]
  resources "/teams", TeamController, except: [:new, :edit] do
    resources "/members", MemberController, only: [:index, :create, :delete]
  end
end
```

## 测试生成

有关ExUnit测试、Mox模拟框架和测试工厂的详细信息，请参阅[references/test-patterns.md]。

**关键规则：**
- 对于不共享状态的测试，使用`async: true`。
- 使用`Ecto.Adapters.SQL.Sandbox`进行数据库隔离。
- 使用`ex_machina`或自定义的`build/1`、`insert/1`函数来创建测试用例。
- 分别测试不同的上下文和控制器。
- 对控制器进行测试时，需验证状态码、响应体格式以及错误处理情况。
- 使用`Mox`模拟外部服务，并在测试中定义其行为和预期结果。

### 控制器测试模板（Controller Test Template）

```elixir
defmodule MyAppWeb.UserControllerTest do
  use MyAppWeb.ConnCase, async: true

  import MyApp.Factory

  setup %{conn: conn} do
    user = insert(:user)
    conn = put_req_header(conn, "authorization", "Bearer #{token_for(user)}")
    {:ok, conn: conn, user: user}
  end

  describe "index" do
    test "lists users", %{conn: conn} do
      conn = get(conn, ~p"/api/v1/users")
      assert %{"data" => users} = json_response(conn, 200)
      assert is_list(users)
    end
  end

  describe "create" do
    test "returns 201 with valid params", %{conn: conn} do
      params = params_for(:user)
      conn = post(conn, ~p"/api/v1/users", user: params)
      assert %{"data" => %{"id" => _}} = json_response(conn, 201)
    end

    test "returns 422 with invalid params", %{conn: conn} do
      conn = post(conn, ~p"/api/v1/users", user: %{})
      assert json_response(conn, 422)["errors"] != %{}
    end
  end
end
```

## JSON渲染器（Phoenix 1.7及以上版本）

```elixir
defmodule MyAppWeb.UserJSON do
  def index(%{users: users}), do: %{data: for(u <- users, do: data(u))}
  def show(%{user: user}), do: %{data: data(user)}

  defp data(user) do
    %{
      id: user.id,
      email: user.email,
      inserted_at: user.inserted_at
    }
  end
end
```

## 编写代码前的检查清单

- 确保迁移脚本使用了`timestamps(type: :utc_datetime_usec)`。
- 如果项目使用UUID作为唯一标识符，请确保配置了二进制ID。
- 在需要的地方实现了租户隔离（tenant scoping）。
- 确保认证插件已正确集成到路由处理流程中。
- `FallbackController`能够处理`{:error, changeset}`和`{:error, :not_found}`错误情况。
- 测试应覆盖200、201、404、422等状态码。
- 为每个数据结构都定义了相应的测试工厂（test factories）。