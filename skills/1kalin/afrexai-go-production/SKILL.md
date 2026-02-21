# Go生产工程指南

作为Go生产工程的专家，您需要遵循以下系统来管理每一个Go项目——从架构设计到最终的生产部署。新项目应依次执行各个阶段；对于现有的代码库，可根据需要选择性地应用这些阶段。

---

## 快速健康检查 (/16)

对于每个检查项，评分如下：
- 0（缺失）、1（部分完成）、2（完全完成）：

| 检查项 | 需要检查的内容 |
|--------|--------------|
| 项目结构 | 是否遵循标准布局，包边界是否清晰 |
| 错误处理 | 是否正确封装错误，是否有异常错误被忽略 |
| 并发安全性 | 是否没有goroutine泄漏，上下文是否正确传递 |
| 测试 | 测试覆盖率是否超过80%，是否使用表格驱动的测试，是否使用了竞态条件检测工具 |
| 可观测性 | 是否有结构化的日志记录，是否收集了指标数据 |
| 配置 | 是否遵循12因子配置原则，并在启动时进行验证 |
| CI/CD | 是否包含代码检查（linting）、测试和构建流程 |
| 文档 | 是否有GoDoc注释，是否有README文件，是否有API设计文档（ADRs） |

**评分解释：**
- 0-6 = 🔴 存在严重问题 |
- 7-10 = 🟡 需要改进 |
- 11-14 = 🟢 较为完善 |
- 15-16 = 💎 优秀 |

---

## 第1阶段：项目架构

### 项目结构（标准布局）

```
project-root/
├── cmd/
│   ├── api/              # HTTP API binary
│   │   └── main.go
│   └── worker/           # Background worker binary
│       └── main.go
├── internal/             # Private packages (enforced by Go)
│   ├── domain/           # Business types & interfaces
│   │   ├── user.go
│   │   └── order.go
│   ├── service/          # Business logic
│   │   ├── user.go
│   │   └── user_test.go
│   ├── repository/       # Data access
│   │   ├── postgres/
│   │   └── redis/
│   ├── handler/          # HTTP/gRPC handlers
│   │   ├── http/
│   │   └── grpc/
│   ├── middleware/        # HTTP middleware
│   └── config/           # Configuration
├── pkg/                  # Public packages (use sparingly)
├── api/                  # OpenAPI specs, proto files
├── migrations/           # Database migrations
├── scripts/              # Build/deploy scripts
├── Makefile
├── Dockerfile
├── go.mod
├── go.sum
└── .golangci.yml
```

**7条架构规则：**
1. `internal/`文件夹是您的得力助手——充分利用它来防止抽象层出现泄漏问题。
2. `cmd/`文件夹仅包含`main.go`文件——在此处定义依赖关系，不要放置业务逻辑。
3. 领域相关的类型应放在`internal/domain/`文件夹中——该文件夹不允许包含外部依赖。
4. 接口应由使用方定义，而非实现方（Go语言的约定）。
5. 每个包应负责一个具体的功能。如果一个功能无法用一个单词命名，就将其拆分为多个包。
6. 除非确实希望其他项目导入该包，否则不要使用`pkg/`文件夹。
7. Go语言不允许循环导入——请将依赖关系设计为有向无环图（DAG）。

### 依赖注入模式

```go
// cmd/api/main.go — wire everything here
func main() {
    cfg := config.MustLoad()
    
    // Infrastructure
    db := postgres.MustConnect(cfg.Database)
    cache := redis.MustConnect(cfg.Redis)
    logger := logging.New(cfg.Log)
    
    // Repositories
    userRepo := postgres.NewUserRepository(db)
    orderRepo := postgres.NewOrderRepository(db)
    
    // Services
    userSvc := service.NewUserService(userRepo, cache, logger)
    orderSvc := service.NewOrderService(orderRepo, userSvc, logger)
    
    // Handlers
    router := handler.NewRouter(userSvc, orderSvc, logger)
    
    // Server
    srv := &http.Server{
        Addr:         cfg.Server.Addr,
        Handler:      router,
        ReadTimeout:  cfg.Server.ReadTimeout,
        WriteTimeout: cfg.Server.WriteTimeout,
        IdleTimeout:  cfg.Server.IdleTimeout,
    }
    
    // Graceful shutdown
    go func() {
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            logger.Fatal("server failed", "error", err)
        }
    }()
    
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit
    
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()
    
    if err := srv.Shutdown(ctx); err != nil {
        logger.Fatal("forced shutdown", "error", err)
    }
}
```

### 框架与库的选择

| 类别 | 推荐库 | 替代库 | 应避免的库 |
|----------|------------|-------------|-------|
| HTTP路由器 | chi, echo | gin, fiber | 仅使用`net/http`处理API |
| 数据库 | pgx (Postgres), sqlc | GORM, ent | 直接使用`database/sql` |
| 数据库迁移 | goose, golang-migrate | atlas | 手动编写SQL迁移脚本 |
| 配置管理 | viper, envconfig | koanf | 避免分散使用`os.Getenv` |
| 日志记录 | slog (stdlib), zerolog | zap | 使用`log (stdlib)` |
| 测试 | testify, is | gomock, mockery | 自定义断言辅助工具 |
| 验证 | validator/v10 | ozzo-validation | 手动编写验证逻辑 |
| 命令行工具 | cobra | urfave/cli | 仅使用`flag (stdlib)` |
| gRPC | google.golang.org/grpc | connect-go | 根据需要选择 |
| 可观测性 | OTel SDK | prometheus客户端 | 自定义指标收集工具 |

**选择原则：**
- 当标准库足够好时优先使用它们（例如`slog`、`net/http`用于简单服务，`encoding/json`用于序列化）。
- 对于Postgres数据库，`pgx`比`database/sql`更优（性能更好，功能更丰富，支持连接池）。
- `sqlc`可以从SQL生成类型安全的代码——适用于查询密集型应用。
- 对于REST API，优先选择`chi`（与标准库兼容，具有丰富的中间件生态系统）。
- 如果需要同时支持gRPC和HTTP/JSON，可以选择`connect-go`。

---

## 第2阶段：错误处理

### 错误处理架构

```go
// internal/domain/errors.go — sentinel errors
package domain

import "errors"

var (
    ErrNotFound      = errors.New("not found")
    ErrConflict      = errors.New("conflict")
    ErrUnauthorized  = errors.New("unauthorized")
    ErrForbidden     = errors.New("forbidden")
    ErrValidation    = errors.New("validation error")
    ErrInternal      = errors.New("internal error")
)

// Typed error with context
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation: %s — %s", e.Field, e.Message)
}

func (e *ValidationError) Unwrap() error {
    return ErrValidation
}
```

### 错误封装规则

```go
// ✅ GOOD: Wrap with context using fmt.Errorf %w
func (r *UserRepo) GetByID(ctx context.Context, id string) (*User, error) {
    user, err := r.db.QueryRow(ctx, query, id)
    if err != nil {
        if errors.Is(err, pgx.ErrNoRows) {
            return nil, fmt.Errorf("user %s: %w", id, domain.ErrNotFound)
        }
        return nil, fmt.Errorf("get user %s: %w", id, err)
    }
    return user, nil
}

// ❌ BAD: Swallowed error
if err != nil {
    log.Println(err) // logged but not returned — caller doesn't know it failed
    return nil
}

// ❌ BAD: Bare return
if err != nil {
    return err // no context — impossible to debug in production
}

// ❌ BAD: String wrapping (breaks errors.Is/As)
return fmt.Errorf("failed: %s", err) // use %w, not %s or %v
```

**8条错误处理规则：**
1. 总是用上下文封装错误：`fmt.Errorf("执行操作X时发生错误：%w", err)`
2. 使用`%w`格式化错误信息——这有助于`errors.Is()`和`errors.As()`正确识别错误来源。
3. 在领域相关的包中定义用于业务层错误的异常类型。
4. 在边界层（如HTTP处理器）处理错误，并将其映射到相应的状态码。
5. 绝不要忽略错误：`_ = f.Close()`是一种不良的编程习惯。至少应使用`defer func() { _ = f.Close() }()`来确保资源被释放。
6. 使用`errors.Is()`进行异常判断，`errors.As()`获取详细的错误信息。
7. 不要同时记录错误和返回错误——通常只返回错误信息；日志记录应在错误处理之后进行。
8. `panic`仅用于处理程序员可控制的错误（如不可恢复的情况），切勿用于运行时错误。

### HTTP错误响应映射

```go
func mapError(err error) (int, string) {
    switch {
    case errors.Is(err, domain.ErrNotFound):
        return http.StatusNotFound, "resource not found"
    case errors.Is(err, domain.ErrConflict):
        return http.StatusConflict, "resource already exists"
    case errors.Is(err, domain.ErrUnauthorized):
        return http.StatusUnauthorized, "authentication required"
    case errors.Is(err, domain.ErrForbidden):
        return http.StatusForbidden, "insufficient permissions"
    case errors.Is(err, domain.ErrValidation):
        var ve *domain.ValidationError
        if errors.As(err, &ve) {
            return http.StatusBadRequest, ve.Error()
        }
        return http.StatusBadRequest, "invalid request"
    default:
        return http.StatusInternalServerError, "internal server error"
    }
}
```

---

## 第3阶段：并发模式

### 上下文传递（必不可少）

```go
// Every function that does I/O takes context as first parameter
func (s *OrderService) Create(ctx context.Context, req CreateOrderRequest) (*Order, error) {
    // Check cancellation before expensive operations
    select {
    case <-ctx.Done():
        return nil, ctx.Err()
    default:
    }
    
    user, err := s.userRepo.GetByID(ctx, req.UserID)
    if err != nil {
        return nil, fmt.Errorf("get user: %w", err)
    }
    
    order, err := s.orderRepo.Create(ctx, user, req)
    if err != nil {
        return nil, fmt.Errorf("create order: %w", err)
    }
    
    // Fire-and-forget with NEW context (don't use request context)
    go func() {
        bgCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
        defer cancel()
        _ = s.notifier.SendOrderConfirmation(bgCtx, order)
    }()
    
    return order, nil
}
```

### Goroutine生命周期管理

```go
// ✅ Worker pool with errgroup
func (w *Worker) ProcessBatch(ctx context.Context, items []Item) error {
    g, ctx := errgroup.WithContext(ctx)
    g.SetLimit(10) // Max 10 concurrent goroutines
    
    for _, item := range items {
        item := item // Go < 1.22 loop variable capture
        g.Go(func() error {
            return w.processItem(ctx, item)
        })
    }
    
    return g.Wait()
}

// ✅ Long-running goroutine with shutdown
type Processor struct {
    done chan struct{}
    wg   sync.WaitGroup
}

func (p *Processor) Start(ctx context.Context) {
    p.wg.Add(1)
    go func() {
        defer p.wg.Done()
        ticker := time.NewTicker(5 * time.Second)
        defer ticker.Stop()
        
        for {
            select {
            case <-ctx.Done():
                return
            case <-ticker.C:
                p.process(ctx)
            }
        }
    }()
}

func (p *Processor) Stop() {
    p.wg.Wait()
}
```

### 常见的并发问题

| 问题 | 表现 | 解决方法 |
|---------|---------|-----|
| Goroutine泄漏 | 内存持续增长 | 确保每个Goroutine都有终止路径（使用`context`或`done`通道） |
| 竞态条件 | 使用`-race`标志检测 | 使用`sync.Mutex`、通道或`sync/atomic`来避免竞争条件 |
| 通道死锁 | Goroutine挂起 | 使用带`default`或`timeout`的`select`操作 |
| 共享闭包变量 | 数据不一致 | 使用`item := item`（Go 1.22及以下版本）或通过函数参数传递变量 |
| 缺少`sync.WaitGroup` | Goroutine执行时间超过调用者存活时间 | 在`go`之前调用`wg.Add()`，在函数结束时调用`wg.Wait()` |
| Mutex复制 | 数据竞争 | 不要复制包含`sync.Mutex`的struct |

**6条并发规则：**
1. 所有测试都必须使用`-race`标志运行。
- 对于有明确执行时长的任务，使用`errgroup`和`WaitGroup`来管理Goroutine。
- 用通道进行通信，用互斥锁保护状态——根据实际需求选择合适的工具。
- 在启动Goroutine之前，必须制定明确的终止策略。
- 对于一次性使用的资源（如数据库连接），使用`context.Background()`。

---

## 第4阶段：接口设计

### 消费者定义的接口（Go语言约定）

```go
// ❌ BAD: Defining interface where implemented
// repository/user.go
type UserRepository interface { // Don't define here
    GetByID(ctx context.Context, id string) (*User, error)
    Create(ctx context.Context, user *User) error
}

// ✅ GOOD: Define interface where consumed
// service/user.go
type userRepository interface { // Private — only this package uses it
    GetByID(ctx context.Context, id string) (*domain.User, error)
    Create(ctx context.Context, user *domain.User) error
}

type UserService struct {
    repo   userRepository
    logger *slog.Logger
}

func NewUserService(repo userRepository, logger *slog.Logger) *UserService {
    return &UserService{repo: repo, logger: logger}
}
```

**接口设计规则：**
1. 接口用于接收输入，返回具体类型的数据结构。
2. 接口应保持简洁——理想情况下包含1-3个方法。
3. 接口名应清晰反映其功能（例如`Reader`、`Storer`、`Notifier`，而不是`IUser`或`UserInterface`）。
- 空接口`any`表示放弃类型安全性——请谨慎使用。
- 接口默认满足所有实现者的要求——无需使用`implements`关键字。

---

## 第5阶段：测试

### 表格驱动的测试（Go推荐的方式）

```go
func TestUserService_Create(t *testing.T) {
    tests := []struct {
        name    string
        input   CreateUserRequest
        setup   func(*mockUserRepo)
        want    *domain.User
        wantErr error
    }{
        {
            name:  "success",
            input: CreateUserRequest{Name: "Alice", Email: "alice@example.com"},
            setup: func(m *mockUserRepo) {
                m.On("Create", mock.Anything, mock.AnythingOfType("*domain.User")).Return(nil)
            },
            want: &domain.User{Name: "Alice", Email: "alice@example.com"},
        },
        {
            name:  "duplicate email",
            input: CreateUserRequest{Name: "Alice", Email: "existing@example.com"},
            setup: func(m *mockUserRepo) {
                m.On("Create", mock.Anything, mock.Anything).Return(domain.ErrConflict)
            },
            wantErr: domain.ErrConflict,
        },
        {
            name:    "empty name",
            input:   CreateUserRequest{Name: "", Email: "alice@example.com"},
            wantErr: domain.ErrValidation,
        },
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            repo := new(mockUserRepo)
            if tt.setup != nil {
                tt.setup(repo)
            }
            
            svc := NewUserService(repo, slog.Default())
            got, err := svc.Create(context.Background(), tt.input)
            
            if tt.wantErr != nil {
                assert.ErrorIs(t, err, tt.wantErr)
                return
            }
            require.NoError(t, err)
            assert.Equal(t, tt.want.Name, got.Name)
            assert.Equal(t, tt.want.Email, got.Email)
        })
    }
}
```

### 测试类别与目标

| 类别 | 测试目标 | 使用工具 | 测试文件位置 |
|----------|--------|-------|----------|
| 单元测试 | 服务/领域的80%以上代码 | `test.go`文件 |
| 集成测试 | 数据库查询、外部API | `testcontainers-go` |
| 端到端测试 | 完整的请求生命周期 | `test/e2e/` |
| 随机测试 | 输入解析、序列化 | `testing.F` | `*_test.go`文件 |
| 性能测试 | 性能瓶颈部分 | `testing.B` | `*_test.go` |

### 使用`testcontainers`进行集成测试

```go
func TestUserRepository_Integration(t *testing.T) {
    if testing.Short() {
        t.Skip("skipping integration test")
    }
    
    ctx := context.Background()
    
    pg, err := testcontainers.GenericContainer(ctx, testcontainers.GenericContainerRequest{
        ContainerRequest: testcontainers.ContainerRequest{
            Image:        "postgres:16-alpine",
            ExposedPorts: []string{"5432/tcp"},
            Env: map[string]string{
                "POSTGRES_PASSWORD": "test",
                "POSTGRES_DB":       "testdb",
            },
            WaitingFor: wait.ForListeningPort("5432/tcp"),
        },
        Started: true,
    })
    require.NoError(t, err)
    defer pg.Terminate(ctx)
    
    connStr, _ := pg.ConnectionString(ctx, "sslmode=disable")
    db := pgx.MustConnect(ctx, connStr)
    runMigrations(db)
    
    repo := NewUserRepository(db)
    
    t.Run("create and get", func(t *testing.T) {
        user := &domain.User{Name: "Test", Email: "test@example.com"}
        err := repo.Create(ctx, user)
        require.NoError(t, err)
        
        got, err := repo.GetByID(ctx, user.ID)
        require.NoError(t, err)
        assert.Equal(t, user.Name, got.Name)
    })
}
```

**7条测试规则：**
- 所有测试都必须使用`-race`标志：`go test -race ./...`
- 对于包含多个测试用例的测试，使用表格驱动的测试方法。
- 使用`testcontainers-go`进行集成测试（真实数据库、真实Redis环境）。
- 在安全的情况下使用`t.Parallel()`并行执行测试——Go默认按顺序执行测试。
- 使用`testing.Short()`快速运行耗时较长的测试：`go test -short ./...`
- 对关键代码进行随机测试：`func FuzzParseInput(f *testing.F)` |
- 对性能瓶颈部分进行性能测试：`func BenchmarkSerialize(b *testing.B)` |

---

## 第6阶段：配置与启动

### 12因子配置原则

```go
// internal/config/config.go
package config

import (
    "fmt"
    "time"
    "github.com/kelseyhightower/envconfig"
)

type Config struct {
    Server   ServerConfig
    Database DatabaseConfig
    Redis    RedisConfig
    Log      LogConfig
}

type ServerConfig struct {
    Addr         string        `envconfig:"SERVER_ADDR" default:":8080"`
    ReadTimeout  time.Duration `envconfig:"SERVER_READ_TIMEOUT" default:"5s"`
    WriteTimeout time.Duration `envconfig:"SERVER_WRITE_TIMEOUT" default:"10s"`
    IdleTimeout  time.Duration `envconfig:"SERVER_IDLE_TIMEOUT" default:"120s"`
}

type DatabaseConfig struct {
    URL             string        `envconfig:"DATABASE_URL" required:"true"`
    MaxConns        int           `envconfig:"DATABASE_MAX_CONNS" default:"25"`
    MinConns        int           `envconfig:"DATABASE_MIN_CONNS" default:"5"`
    MaxConnLifetime time.Duration `envconfig:"DATABASE_MAX_CONN_LIFETIME" default:"1h"`
}

type RedisConfig struct {
    URL          string        `envconfig:"REDIS_URL" default:"localhost:6379"`
    MaxRetries   int           `envconfig:"REDIS_MAX_RETRIES" default:"3"`
    DialTimeout  time.Duration `envconfig:"REDIS_DIAL_TIMEOUT" default:"5s"`
    ReadTimeout  time.Duration `envconfig:"REDIS_READ_TIMEOUT" default:"3s"`
    WriteTimeout time.Duration `envconfig:"REDIS_WRITE_TIMEOUT" default:"3s"`
}

type LogConfig struct {
    Level  string `envconfig:"LOG_LEVEL" default:"info"`
    Format string `envconfig:"LOG_FORMAT" default:"json"` // json | text
}

func MustLoad() *Config {
    var cfg Config
    if err := envconfig.Process("", &cfg); err != nil {
        panic(fmt.Sprintf("config: %v", err))
    }
    return &cfg
}
```

**配置规则：**
- 在启动时验证所有配置项——立即发现错误，不要等到凌晨3点才发现问题。
- 使用`envconfig`或`viper`进行配置管理——避免分散使用`os.Getenv()`。
- 为非敏感配置提供合理的默认值。
- 对于敏感信息（如密码），使用`required:"true"`进行校验。
- 绝不要在日志中记录敏感信息——使用`String()`方法对敏感数据进行脱敏。

---

## 第7阶段：结构化日志记录

### slog（Go 1.21及更高版本的标准库）

```go
// internal/logging/logger.go
package logging

import (
    "log/slog"
    "os"
)

func New(cfg LogConfig) *slog.Logger {
    var handler slog.Handler
    
    opts := &slog.HandlerOptions{
        Level: parseLevel(cfg.Level),
    }
    
    switch cfg.Format {
    case "text":
        handler = slog.NewTextHandler(os.Stdout, opts)
    default:
        handler = slog.NewJSONHandler(os.Stdout, opts)
    }
    
    return slog.New(handler)
}

// Usage in services
func (s *OrderService) Create(ctx context.Context, req CreateOrderRequest) (*Order, error) {
    s.logger.InfoContext(ctx, "creating order",
        "user_id", req.UserID,
        "items", len(req.Items),
    )
    
    order, err := s.repo.Create(ctx, req)
    if err != nil {
        s.logger.ErrorContext(ctx, "order creation failed",
            "user_id", req.UserID,
            "error", err,
        )
        return nil, fmt.Errorf("create order: %w", err)
    }
    
    s.logger.InfoContext(ctx, "order created",
        "order_id", order.ID,
        "total", order.Total,
    )
    return order, nil
}
```

### 请求ID中间件

```go
func RequestIDMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        requestID := r.Header.Get("X-Request-ID")
        if requestID == "" {
            requestID = uuid.NewString()
        }
        
        ctx := context.WithValue(r.Context(), requestIDKey, requestID)
        w.Header().Set("X-Request-ID", requestID)
        
        // Add to logger context
        logger := slog.Default().With("request_id", requestID)
        ctx = context.WithValue(ctx, loggerKey, logger)
        
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}
```

**日志级别说明：**
| 级别 | 使用场景 | 示例 |
|-------|------|---------|
| DEBUG | 开发调试 | SQL查询、缓存操作 |
| INFO | 业务事件 | 订单创建、用户注册 |
| WARN | 可恢复的问题 | 重试成功、使用了过时的API |
| ERROR | 操作失败 | 数据库连接丢失、外部API返回500状态码 |

---

## 第8阶段：数据库模式

### pgx连接池

```go
func MustConnect(cfg DatabaseConfig) *pgxpool.Pool {
    poolCfg, err := pgxpool.ParseConfig(cfg.URL)
    if err != nil {
        panic(fmt.Sprintf("parse db config: %v", err))
    }
    
    poolCfg.MaxConns = int32(cfg.MaxConns)
    poolCfg.MinConns = int32(cfg.MinConns)
    poolCfg.MaxConnLifetime = cfg.MaxConnLifetime
    poolCfg.HealthCheckPeriod = 30 * time.Second
    
    pool, err := pgxpool.NewWithConfig(context.Background(), poolCfg)
    if err != nil {
        panic(fmt.Sprintf("connect db: %v", err))
    }
    
    if err := pool.Ping(context.Background()); err != nil {
        panic(fmt.Sprintf("ping db: %v", err))
    }
    
    return pool
}
```

### sqlc（类型安全的SQL操作）

```sql
-- queries/user.sql
-- name: GetUser :one
SELECT id, name, email, created_at FROM users WHERE id = $1;

-- name: ListUsers :many
SELECT id, name, email, created_at FROM users
WHERE ($1::text IS NULL OR name ILIKE '%' || $1 || '%')
ORDER BY created_at DESC
LIMIT $2 OFFSET $3;

-- name: CreateUser :one
INSERT INTO users (name, email) VALUES ($1, $2)
RETURNING id, name, email, created_at;
```

### 事务处理模式

```yaml
# sqlc.yaml
version: "2"
sql:
  - engine: "postgresql"
    queries: "queries/"
    schema: "migrations/"
    gen:
      go:
        package: "db"
        out: "internal/repository/db"
        sql_package: "pgx/v5"
        emit_json_tags: true
        emit_empty_slices: true
```

---

## 第9阶段：HTTP API设计

### 使用chi设置路由器

```go
func NewRouter(userSvc *service.UserService, logger *slog.Logger) http.Handler {
    r := chi.NewRouter()
    
    // Middleware stack (order matters)
    r.Use(middleware.RequestID)
    r.Use(middleware.RealIP)
    r.Use(RequestLoggerMiddleware(logger))
    r.Use(middleware.Recoverer)
    r.Use(middleware.Timeout(30 * time.Second))
    r.Use(CORSMiddleware)
    
    // Health checks (no auth)
    r.Get("/healthz", healthCheck)
    r.Get("/readyz", readinessCheck)
    
    // API v1
    r.Route("/api/v1", func(r chi.Router) {
        r.Use(AuthMiddleware)
        
        r.Route("/users", func(r chi.Router) {
            r.Get("/", listUsers(userSvc))
            r.Post("/", createUser(userSvc))
            r.Route("/{id}", func(r chi.Router) {
                r.Get("/", getUser(userSvc))
                r.Put("/", updateUser(userSvc))
                r.Delete("/", deleteUser(userSvc))
            })
        })
    })
    
    return r
}
```

### 请求/响应处理模式

```go
func createUser(svc *service.UserService) http.HandlerFunc {
    type request struct {
        Name  string `json:"name" validate:"required,min=2,max=100"`
        Email string `json:"email" validate:"required,email"`
    }
    
    type response struct {
        ID        string    `json:"id"`
        Name      string    `json:"name"`
        Email     string    `json:"email"`
        CreatedAt time.Time `json:"created_at"`
    }
    
    return func(w http.ResponseWriter, r *http.Request) {
        var req request
        if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
            respondError(w, http.StatusBadRequest, "invalid JSON")
            return
        }
        
        if err := validate.Struct(req); err != nil {
            respondError(w, http.StatusBadRequest, formatValidation(err))
            return
        }
        
        user, err := svc.Create(r.Context(), service.CreateUserRequest{
            Name:  req.Name,
            Email: req.Email,
        })
        if err != nil {
            code, msg := mapError(err)
            respondError(w, code, msg)
            return
        }
        
        respondJSON(w, http.StatusCreated, response{
            ID:        user.ID,
            Name:      user.Name,
            Email:     user.Email,
            CreatedAt: user.CreatedAt,
        })
    }
}

func respondJSON(w http.ResponseWriter, code int, data any) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(code)
    json.NewEncoder(w).Encode(data)
}

func respondError(w http.ResponseWriter, code int, message string) {
    respondJSON(w, code, map[string]string{"error": message})
}
```

### 健康检查机制

```go
func healthCheck(w http.ResponseWriter, r *http.Request) {
    respondJSON(w, http.StatusOK, map[string]string{"status": "ok"})
}

func readinessCheck(db *pgxpool.Pool, redis *redis.Client) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        ctx, cancel := context.WithTimeout(r.Context(), 3*time.Second)
        defer cancel()
        
        checks := map[string]string{}
        healthy := true
        
        if err := db.Ping(ctx); err != nil {
            checks["database"] = "unhealthy"
            healthy = false
        } else {
            checks["database"] = "healthy"
        }
        
        if err := redis.Ping(ctx).Err(); err != nil {
            checks["redis"] = "unhealthy"
            healthy = false
        } else {
            checks["redis"] = "healthy"
        }
        
        code := http.StatusOK
        if !healthy {
            code = http.StatusServiceUnavailable
        }
        respondJSON(w, code, checks)
    }
}
```

---

## 第10阶段：可观测性（OpenTelemetry）

### OTel配置

```go
func initTracer(ctx context.Context, serviceName string) (*sdktrace.TracerProvider, error) {
    exporter, err := otlptracehttp.New(ctx)
    if err != nil {
        return nil, fmt.Errorf("create exporter: %w", err)
    }
    
    tp := sdktrace.NewTracerProvider(
        sdktrace.WithBatcher(exporter),
        sdktrace.WithResource(resource.NewWithAttributes(
            semconv.SchemaURL,
            semconv.ServiceName(serviceName),
            semconv.ServiceVersion("1.0.0"),
        )),
        sdktrace.WithSampler(sdktrace.ParentBased(sdktrace.TraceIDRatioBased(0.1))),
    )
    
    otel.SetTracerProvider(tp)
    otel.SetTextMapPropagator(propagation.NewCompositeTextMapPropagator(
        propagation.TraceContext{},
        propagation.Baggage{},
    ))
    
    return tp, nil
}
```

### 使用Prometheus收集指标数据

```go
var (
    httpRequestsTotal = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total HTTP requests",
        },
        []string{"method", "path", "status"},
    )
    
    httpRequestDuration = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request duration",
            Buckets: []float64{.005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5},
        },
        []string{"method", "path"},
    )
)

func MetricsMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        ww := middleware.NewWrapResponseWriter(w, r.ProtoMajor)
        
        next.ServeHTTP(ww, r)
        
        duration := time.Since(start).Seconds()
        path := chi.RouteContext(r.Context()).RoutePattern()
        
        httpRequestsTotal.WithLabelValues(r.Method, path, strconv.Itoa(ww.Status())).Inc()
        httpRequestDuration.WithLabelValues(r.Method, path).Observe(duration)
    })
}
```

---

## 第11阶段：生产部署

### 多阶段Dockerfile构建

```dockerfile
# Build stage
FROM golang:1.23-alpine AS builder

RUN apk add --no-cache git ca-certificates

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-w -s -X main.version=$(git describe --tags --always)" \
    -o /app/server ./cmd/api

# Runtime stage
FROM scratch

COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app/server /server
COPY --from=builder /app/migrations /migrations

USER 65534:65534

EXPOSE 8080

ENTRYPOINT ["/server"]
```

### Makefile构建脚本

```makefile
.PHONY: build test lint run migrate

BINARY := server
VERSION := $(shell git describe --tags --always --dirty)

build:
	CGO_ENABLED=0 go build -ldflags="-w -s -X main.version=$(VERSION)" -o bin/$(BINARY) ./cmd/api

test:
	go test -race -coverprofile=coverage.out ./...
	go tool cover -func=coverage.out

test-short:
	go test -race -short ./...

lint:
	golangci-lint run

run:
	go run ./cmd/api

migrate-up:
	goose -dir migrations postgres "$(DATABASE_URL)" up

migrate-down:
	goose -dir migrations postgres "$(DATABASE_URL)" down

migrate-create:
	goose -dir migrations create $(NAME) sql

generate:
	sqlc generate
	mockery

docker-build:
	docker build -t $(BINARY):$(VERSION) .

ci: lint test build
```

### golangci-lint代码检查配置

```yaml
# .golangci.yml
run:
  timeout: 5m

linters:
  enable:
    - errcheck
    - govet
    - staticcheck
    - unused
    - gosimple
    - ineffassign
    - typecheck
    - gocritic
    - gofumpt
    - revive
    - misspell
    - prealloc
    - noctx         # Finds HTTP requests without context
    - bodyclose     # Checks HTTP response body is closed
    - sqlclosecheck # Checks sql.Rows is closed
    - contextcheck  # Checks function whether use a non-inherited context
    - errname       # Checks sentinel error names follow Go convention
    - exhaustive    # Checks exhaustiveness of enum switch statements
    - gosec         # Security-oriented linting
    - nilerr        # Finds code returning nil even on error
    - unparam       # Reports unused function parameters

linters-settings:
  gocritic:
    enabled-tags:
      - diagnostic
      - style
      - performance
  revive:
    rules:
      - name: unexported-return
        disabled: true
  gosec:
    excludes:
      - G104 # Unhandled errors — covered by errcheck

issues:
  exclude-rules:
    - path: _test\.go
      linters:
        - gosec
        - errcheck
```

### GitHub Actions与持续集成/持续部署（CI/CD）

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  ci:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-go@v5
        with:
          go-version: '1.23'
      
      - name: Lint
        uses: golangci/golangci-lint-action@v6
        with:
          version: latest
      
      - name: Test
        run: go test -race -coverprofile=coverage.out ./...
        env:
          DATABASE_URL: postgres://postgres:test@localhost:5432/testdb?sslmode=disable
      
      - name: Coverage
        run: |
          COVERAGE=$(go tool cover -func=coverage.out | grep total | awk '{print $3}')
          echo "Coverage: $COVERAGE"
      
      - name: Build
        run: go build -o /dev/null ./...
```

---

## 第12阶段：性能优化

### 优先级优化策略

| 优先级 | 优化技巧 | 效果提升 |
|----------|-----------|--------|
| 1 | 使用连接池（pgx连接池、HTTP客户端重用） | 提高10-50倍性能 |
| 2 | 避免不必要的内存分配（使用`sync.Pool`、预分配切片） | 提高2-5倍性能 |
| 3 | 使用`strings.Builder`进行字符串拼接 | 提高5-20倍性能 |
| 4 | 批量处理数据库操作 | 提高5-50倍性能 |
| 5 | 缓存热点代码（使用`sync.Map`、本地缓存、Redis） | 提高10-100倍性能 |
| 6 | 在优化前进行性能分析（使用`pprof`） | 提前发现问题 |

### 性能分析工具

```go
import _ "net/http/pprof"

// In main.go (debug server on separate port)
go func() {
    log.Println(http.ListenAndServe(":6060", nil))
}()

// Then: go tool pprof http://localhost:6060/debug/pprof/heap
// Or:   go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30
```

### 常见的性能优化技巧

```go
// ✅ Pre-allocate slices when length is known
users := make([]User, 0, len(ids))

// ✅ strings.Builder for concatenation
var b strings.Builder
b.Grow(estimatedLen)
for _, s := range parts {
    b.WriteString(s)
}
result := b.String()

// ✅ Reuse HTTP clients (never create per-request)
var httpClient = &http.Client{
    Timeout: 10 * time.Second,
    Transport: &http.Transport{
        MaxIdleConns:        100,
        MaxIdleConnsPerHost: 10,
        IdleConnTimeout:     90 * time.Second,
    },
}

// ✅ sync.Pool for frequently allocated objects
var bufPool = sync.Pool{
    New: func() any {
        return new(bytes.Buffer)
    },
}

func process() {
    buf := bufPool.Get().(*bytes.Buffer)
    defer func() {
        buf.Reset()
        bufPool.Put(buf)
    }()
    // use buf...
}
```

---

## 第13阶段：安全加固

### 安全检查清单

| 检查项 | 优先级 | 处理方式 |
|----------|-------|----------|
| 输入验证 | 使用`validator/v10`验证所有输入 | 非常重要 |
| SQL操作 | 使用参数化查询（`sqlc`/`pgx`），避免字符串拼接 | 非常重要 |
| 身份验证 | 使用JWT进行验证，并定期更新密钥 | 非常重要 |
| 敏感信息管理 | 仅通过环境变量存储敏感信息，避免硬编码 | 非常重要 |
| 依赖管理 | 使用`govulncheck`进行安全检查，定期使用`go mod tidy` | 非常重要 |
| 跨源请求（CORS） | 严格限制请求来源 | 非常重要 |
| 速率限制 | 对每个IP和用户设置访问限制 | 非常重要 |
| 安全头信息 | 使用安全头信息中间件 | 非常重要 |
| TLS协议 | 使用TLS 1.2及以上版本，使用强加密算法 | 非常重要 |
| 日志记录 | 绝不要记录敏感信息、个人身份信息（PII）或令牌 | 非常重要 |

### 安全头信息中间件

```go
func SecurityHeaders(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("X-Content-Type-Options", "nosniff")
        w.Header().Set("X-Frame-Options", "DENY")
        w.Header().Set("X-XSS-Protection", "0")
        w.Header().Set("Strict-Transport-Security", "max-age=63072000; includeSubDomains")
        w.Header().Set("Content-Security-Policy", "default-src 'none'")
        w.Header().Set("Referrer-Policy", "strict-origin-when-cross-origin")
        next.ServeHTTP(w, r)
    })
}
```

### 漏洞扫描

```bash
# Install
go install golang.org/x/vuln/cmd/govulncheck@latest

# Scan
govulncheck ./...

# In CI — fail build on vulnerabilities
govulncheck -show verbose ./...
```

---

## 第14阶段：高级编程技巧

### 泛型（Go 1.18及以上版本）

```go
// Generic result type
type Result[T any] struct {
    Data  T
    Error error
}

// Generic repository
type Repository[T any] interface {
    GetByID(ctx context.Context, id string) (*T, error)
    List(ctx context.Context, filter Filter) ([]T, error)
    Create(ctx context.Context, entity *T) error
    Update(ctx context.Context, entity *T) error
    Delete(ctx context.Context, id string) error
}

// Generic pagination
type Page[T any] struct {
    Items      []T    `json:"items"`
    NextCursor string `json:"next_cursor,omitempty"`
    HasMore    bool   `json:"has_more"`
}
```

### 函数式编程风格

```go
type ServerOption func(*Server)

func WithAddr(addr string) ServerOption {
    return func(s *Server) { s.addr = addr }
}

func WithTimeout(d time.Duration) ServerOption {
    return func(s *Server) { s.timeout = d }
}

func WithLogger(l *slog.Logger) ServerOption {
    return func(s *Server) { s.logger = l }
}

func NewServer(opts ...ServerOption) *Server {
    s := &Server{
        addr:    ":8080",
        timeout: 30 * time.Second,
        logger:  slog.Default(),
    }
    for _, opt := range opts {
        opt(s)
    }
    return s
}
```

### 优雅的降级机制

```go
// Circuit breaker pattern (simplified)
type CircuitBreaker struct {
    failures   atomic.Int64
    threshold  int64
    resetAfter time.Duration
    lastFail   atomic.Int64
}

func (cb *CircuitBreaker) Execute(fn func() error) error {
    if cb.isOpen() {
        return ErrCircuitOpen
    }
    
    err := fn()
    if err != nil {
        cb.failures.Add(1)
        cb.lastFail.Store(time.Now().UnixNano())
        return err
    }
    
    cb.failures.Store(0)
    return nil
}

func (cb *CircuitBreaker) isOpen() bool {
    if cb.failures.Load() < cb.threshold {
        return false
    }
    // Allow retry after reset period
    elapsed := time.Since(time.Unix(0, cb.lastFail.Load()))
    return elapsed < cb.resetAfter
}
```

---

## Go生产开发的10条准则

1. `internal/`文件夹是隐藏实现细节的“守门人”——积极使用它来保护代码。
2. 错误是可处理的对象——务必正确封装和处理错误，绝不要忽略它们。
3. 总是使用`-race`标志——数据竞争可能是无声的杀手。
4. 接口应由使用方定义——保持简洁、具体且明确。
5. 在所有需要I/O操作的场景中都使用上下文对象。
6. 使用`errgroup`来管理Goroutine的生命周期，确保并发操作可控且错误处理得当。
7. 对于SQL操作，优先使用`sqlc`而非ORM——它提供了类型安全性和避免运行时反射。
8. 在优化之前先进行性能分析（使用`pprof`）——数据分析比直觉更可靠。
9. 在启动时验证配置、检查连接状态，遇到问题立即退出程序。
10. 实现优雅的程序关闭机制——捕获异常信号，及时释放资源。

---

## 10个常见的Go开发错误

| 错误类型 | 影响 | 解决方法 |
|---------|--------|-----|
| Goroutine泄漏 | 导致内存耗尽 | 确保每个Goroutine都有终止路径 |
| 未检查错误 | 会导致程序无声失败 | 使用`errcheck`进行代码检查 |
| 循环中直接拼接字符串 | 会导致O(n²)级别的内存分配 | 使用`strings.Builder` |
| 复制包含`sync.Mutex`的变量 | 会导致数据竞争 | 通过指针传递变量 |
| 忽略上下文取消操作 | 会导致资源泄露 | 使用`defer cancel()`确保资源被释放 |
| 在`init()`函数中滥用资源 | 会影响代码的可测试性 | 明确初始化资源 |

---

## 生产就绪性检查清单

### 必须满足的条件（P0级）
- 清晰的测试套件（包含`-race`标志）
- 业务逻辑的测试覆盖率超过80%
- 有结构化的日志记录（使用`slog`或`zerolog`）
- 具有优雅的程序关闭机制（能够响应异常信号）
- 启动时验证配置
- 所有错误都使用上下文进行封装
- 代码通过`golangci-lint`检查
- 使用多阶段Docker构建流程
- 安全检查工具`govulncheck`运行正常

### 推荐的做法（P1级）
- 使用OpenTelemetry进行追踪
- 使用Prometheus收集指标数据
- 实现请求ID的传递机制
- 设置速率限制
- 使用安全头信息中间件
- 使用`testcontainers`进行集成测试
- 进行数据库迁移（使用`goose/migrate`）
- 配置CI/CD流程（包括代码检查、测试、构建和部署）

---

## 代码质量评分（0-100分）

| 评估维度 | 权重 | 评估内容 |
|-----------|--------|-----------------|
| 错误处理 | 15% | 错误封装、异常处理机制 |
| 并发处理 | 15% | 无竞态条件、上下文传递、Goroutine生命周期管理 |
| 测试 | 15% | 测试覆盖率、表格驱动的测试方法、集成测试 |
| 代码组织 | 15% | 包结构、`internal/`文件夹的使用、依赖关系管理 |
| 可观测性 | 10% | 有结构化的日志记录、指标收集、追踪能力 |
| 安全性 | 10% | 输入验证、安全检查、敏感信息管理 |
| 性能 | 10% | 性能分析工具、资源池的使用、预分配机制 |
| 文档编写 | 10% | GoDoc文档、README文件、API设计文档 |

**评分标准：**
- 0-40分 = 需要彻底重构 |
- 41-60分 = 存在明显问题 |
- 61-80分 = 基本符合生产要求 |
- 81-100分 = 代码质量优秀 |

---

## 常用命令

当被询问关于Go项目的问题时，可以按照以下方式自然地回答：
- “审查这段Go代码” → 运行快速健康检查，识别潜在的问题模式。
- “新建一个Go服务” → 生成包含所有开发阶段的完整项目结构。
- “修复错误处理逻辑” → 在整个项目中应用第2阶段的优化技巧。
- “添加测试代码” → 根据第5阶段的要求生成相应的测试代码。
- “使项目具备生产就绪条件” → 完成所有必要的检查流程。
- “分析代码性能” → 使用`pprof`进行分析。
- “增强项目的可观测性” | 配置OpenTelemetry和Prometheus。
- “优化性能” | 先进行性能分析，再应用相应的优化措施。
- “设置CI/CD流程” | 配置GitHub Actions和`golangci-lint`。
- “配置数据库” | 使用`pgx`连接池、`sqlc`和数据库迁移工具。
- “评估项目架构” | 根据第1阶段的规则进行审查。
- “进行安全审计” | 执行第13阶段的检查流程。