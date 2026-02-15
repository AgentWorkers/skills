---
name: go-concurrency
model: standard
description: Go语言的生产环境并发模式包括：goroutine（协程）、channel（通道）、同步原语（sync primitives）、context（上下文）、worker pool（工作线程池）、pipeline（流水线）以及优雅的程序关闭（graceful shutdown）。这些模式在构建并发Go应用程序或调试竞态条件（race conditions）时非常有用。
---

# Go 并发模式

Go 并发的常用模式包括 goroutine（轻量级并发执行单元）、channel（用于goroutine之间的通信）、同步原语以及上下文管理。

## 使用场景

- 构建并发的 Go 应用程序
- 实现工作池和管道（pipeline）机制
- 管理 goroutine 的生命周期和取消操作
- 调试数据竞争（race condition）问题
- 实现优雅的程序关闭（graceful shutdown）

## 并发原语

| 原语                          | 用途                                      | 使用场景                                      |
| --------------------------- | -------------------------------------- | ---------------------------------------- |
| `goroutine`       | 轻量级的并发执行单元                            | 所有需要并发处理的任务                         |
| `channel`         | goroutine 之间的通信工具                          | 用于传递数据和发送信号                         |
| `select`          | 多路复用 channel 操作                          | 等待多个 channel 的响应                         |
| `sync.Mutex`      | 实现互斥锁（mutual exclusion）                    | 保护共享资源                             |
| `sync.WaitGroup`     | 等待所有 goroutine 完成                         | 协调 goroutine 的执行顺序                         |
| `context.Context`    | 提供取消和超时功能                            | 用于控制 goroutine 的生命周期                         |
| `errgroup.Group`     | 处理可能出错的并发任务                          | 并发任务中的错误处理                         |

**Go 并发原则：**  
“不要通过共享内存来实现通信；要通过通信来共享内存。”

## 快速入门

```go
func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    results := make(chan string, 10)
    var wg sync.WaitGroup

    for i := 0; i < 3; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            select {
            case <-ctx.Done():
                return
            case results <- fmt.Sprintf("Worker %d done", id):
            }
        }(i)
    }

    go func() { wg.Wait(); close(results) }()

    for result := range results {
        fmt.Println(result)
    }
}
```

## 模式 1：工作池（Worker Pool）

```go
type Job struct {
    ID   int
    Data string
}

type Result struct {
    JobID  int
    Output string
    Err    error
}

func WorkerPool(ctx context.Context, numWorkers int, jobs <-chan Job) <-chan Result {
    results := make(chan Result)
    var wg sync.WaitGroup

    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range jobs {
                select {
                case <-ctx.Done():
                    return
                default:
                    results <- Result{
                        JobID:  job.ID,
                        Output: fmt.Sprintf("Processed: %s", job.Data),
                    }
                }
            }
        }()
    }

    go func() { wg.Wait(); close(results) }()
    return results
}

// Usage
func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    jobs := make(chan Job, 100)
    go func() {
        for i := 0; i < 50; i++ {
            jobs <- Job{ID: i, Data: fmt.Sprintf("job-%d", i)}
        }
        close(jobs)
    }()

    for result := range WorkerPool(ctx, 5, jobs) {
        fmt.Printf("Result: %+v\n", result)
    }
}
```

## 模式 2：扇出/扇入管道（Fan-Out/Fan-In Pipeline）

```go
// Stage 1: Generate values
func generate(ctx context.Context, nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for _, n := range nums {
            select {
            case <-ctx.Done(): return
            case out <- n:
            }
        }
    }()
    return out
}

// Stage 2: Transform (run multiple instances for fan-out)
func square(ctx context.Context, in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range in {
            select {
            case <-ctx.Done(): return
            case out <- n * n:
            }
        }
    }()
    return out
}

// Fan-in: Merge multiple channels into one
func merge(ctx context.Context, channels ...<-chan int) <-chan int {
    var wg sync.WaitGroup
    out := make(chan int)

    wg.Add(len(channels))
    for _, ch := range channels {
        go func(c <-chan int) {
            defer wg.Done()
            for n := range c {
                select {
                case <-ctx.Done(): return
                case out <- n:
                }
            }
        }(ch)
    }

    go func() { wg.Wait(); close(out) }()
    return out
}

// Usage: fan out to 3 squarers, fan in results
func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    in := generate(ctx, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    c1 := square(ctx, in)
    c2 := square(ctx, in)
    c3 := square(ctx, in)

    for result := range merge(ctx, c1, c2, c3) {
        fmt.Println(result)
    }
}
```

## 模式 3：带取消功能的 errgroup

```go
import "golang.org/x/sync/errgroup"

func fetchAllURLs(ctx context.Context, urls []string) ([]string, error) {
    g, ctx := errgroup.WithContext(ctx)
    results := make([]string, len(urls))

    for i, url := range urls {
        i, url := i, url
        g.Go(func() error {
            req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
            if err != nil {
                return fmt.Errorf("creating request for %s: %w", url, err)
            }
            resp, err := http.DefaultClient.Do(req)
            if err != nil {
                return fmt.Errorf("fetching %s: %w", url, err)
            }
            defer resp.Body.Close()
            results[i] = fmt.Sprintf("%s: %d", url, resp.StatusCode)
            return nil
        })
    }

    if err := g.Wait(); err != nil {
        return nil, err // First error cancels all others via ctx
    }
    return results, nil
}

// With concurrency limit
func fetchWithLimit(ctx context.Context, urls []string) ([]string, error) {
    g, ctx := errgroup.WithContext(ctx)
    g.SetLimit(10) // Max concurrent goroutines
    results := make([]string, len(urls))

    for i, url := range urls {
        i, url := i, url
        g.Go(func() error {
            result, err := fetchURL(ctx, url)
            if err != nil { return err }
            results[i] = result
            return nil
        })
    }

    return results, g.Wait()
}
```

## 模式 4：有界并发（使用信号量，Semaphore）

```go
import "golang.org/x/sync/semaphore"

type RateLimitedWorker struct {
    sem *semaphore.Weighted
}

func NewRateLimitedWorker(maxConcurrent int64) *RateLimitedWorker {
    return &RateLimitedWorker{sem: semaphore.NewWeighted(maxConcurrent)}
}

func (w *RateLimitedWorker) Do(ctx context.Context, tasks []func() error) []error {
    var (
        wg     sync.WaitGroup
        mu     sync.Mutex
        errors []error
    )

    for _, task := range tasks {
        if err := w.sem.Acquire(ctx, 1); err != nil {
            return []error{err}
        }
        wg.Add(1)
        go func(t func() error) {
            defer wg.Done()
            defer w.sem.Release(1)
            if err := t(); err != nil {
                mu.Lock()
                errors = append(errors, err)
                mu.Unlock()
            }
        }(task)
    }

    wg.Wait()
    return errors
}

// Simpler alternative: channel-based semaphore
type Semaphore chan struct{}

func NewSemaphore(n int) Semaphore       { return make(chan struct{}, n) }
func (s Semaphore) Acquire()             { s <- struct{}{} }
func (s Semaphore) Release()             { <-s }
```

## 模式 5：优雅关闭（Graceful Shutdown）

```go
func main() {
    ctx, cancel := context.WithCancel(context.Background())

    sigCh := make(chan os.Signal, 1)
    signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)

    server := NewServer()
    server.Start(ctx)

    sig := <-sigCh
    fmt.Printf("Received signal: %v\n", sig)
    cancel() // Cancel context to stop all workers

    server.Shutdown(5 * time.Second)
}

type Server struct {
    wg sync.WaitGroup
}

func (s *Server) Start(ctx context.Context) {
    for i := 0; i < 5; i++ {
        s.wg.Add(1)
        go s.worker(ctx, i)
    }
}

func (s *Server) worker(ctx context.Context, id int) {
    defer s.wg.Done()
    ticker := time.NewTicker(time.Second)
    defer ticker.Stop()

    for {
        select {
        case <-ctx.Done():
            fmt.Printf("Worker %d cleaning up...\n", id)
            return
        case <-ticker.C:
            fmt.Printf("Worker %d working...\n", id)
        }
    }
}

func (s *Server) Shutdown(timeout time.Duration) {
    done := make(chan struct{})
    go func() { s.wg.Wait(); close(done) }()

    select {
    case <-done:
        fmt.Println("Clean shutdown completed")
    case <-time.After(timeout):
        fmt.Println("Shutdown timed out, forcing exit")
    }
}
```

## 模式 6：并发映射（Concurrent Map）

```go
// sync.Map: optimized for read-heavy workloads with stable keys
type Cache struct {
    m sync.Map
}

func (c *Cache) Get(key string) (any, bool) { return c.m.Load(key) }
func (c *Cache) Set(key string, value any) { c.m.Store(key, value) }
func (c *Cache) GetOrSet(key string, val any) (any, bool) {
    return c.m.LoadOrStore(key, val)
}

// ShardedMap: better for write-heavy workloads
type ShardedMap struct {
    shards    []*shard
    numShards int
}

type shard struct {
    sync.RWMutex
    data map[string]any
}

func NewShardedMap(n int) *ShardedMap {
    m := &ShardedMap{shards: make([]*shard, n), numShards: n}
    for i := range m.shards {
        m.shards[i] = &shard{data: make(map[string]any)}
    }
    return m
}

func (m *ShardedMap) getShard(key string) *shard {
    h := 0
    for _, c := range key {
        h = 31*h + int(c)
    }
    return m.shards[h%m.numShards]
}

func (m *ShardedMap) Get(key string) (any, bool) {
    s := m.getShard(key)
    s.RLock()
    defer s.RUnlock()
    v, ok := s.data[key]
    return v, ok
}

func (m *ShardedMap) Set(key string, value any) {
    s := m.getShard(key)
    s.Lock()
    defer s.Unlock()
    s.data[key] = value
}
```

**选择合适的并发数据结构：**
- `sync.Map`：适用于键数量较少、读取操作较多、键仅添加一次且很少删除的场景。
- `ShardedMap`：适用于键数量较多、写入操作频繁、需要可预测性能的场景。

## 模式选择指南

```go
// Timeout
select {
case v := <-ch:
    fmt.Println("Received:", v)
case <-time.After(time.Second):
    fmt.Println("Timeout!")
}

// Non-blocking send/receive
select {
case ch <- 42:
    fmt.Println("Sent")
default:
    fmt.Println("Channel full, skipping")
}

// Priority select: check high-priority first
for {
    select {
    case msg := <-highPriority:
        handle(msg)
    default:
        select {
        case msg := <-highPriority:
            handle(msg)
        case msg := <-lowPriority:
            handle(msg)
        }
    }
}
```

## 数据竞争检测（Race Detection）

```bash
go test -race ./...     # Tests with race detector
go build -race .        # Build with race detector
go run -race main.go    # Run with race detector
```

## 最佳实践

- 在每个 goroutine 中使用 `context.Context` 来处理取消和超时逻辑。
- 仅从发送方关闭 channel。
- 对于可能返回错误的并发操作，使用 `errgroup` 来统一处理错误。
- 当已知 channel 的使用量时，使用缓冲区来接收数据。
- 在需要协调多个 goroutine 时，优先使用 channel 而不是 mutex。
- 在进行测试时，务必启用 `-race` 标志。

**避免的做法：**
- **不要让 goroutine 无终止路径**——每个 goroutine 都必须有退出机制。
- **不要从接收方关闭 channel**——这会导致程序 panic。
- **不要使用 `time.Sleep` 来实现同步**——应使用专门的同步原语。
- **不要忽略 `ctx.Done()` 的调用**——在长时间运行的 goroutine 中，确保它被正确调用。
- **不要在没有同步机制的情况下共享内存**——应使用 channel 或 mutex 来保证数据安全。

**绝对禁止的做法：**
- **绝对不要从接收方关闭 channel**——只能由发送方关闭 channel；否则接收方会收到 panic。
- **绝对不要向已关闭的 channel 发送数据**——这会导致 panic；应让发送方控制 channel 的关闭。
- **绝对不要无限制地创建新的 goroutine**——对于有界并发场景，应使用工作池或信号量。
- **绝对不要在测试中忽略 `-race` 标志**——数据竞争会悄悄破坏程序状态。
- **绝对不要将循环变量的指针传递给 goroutine**——应捕获变量的值或使用闭包（closure）来传递数据。
- **绝对不要使用 `time.Sleep` 来实现同步**——应使用 channel、`sync.WaitGroup` 或 `context` 来完成同步操作。