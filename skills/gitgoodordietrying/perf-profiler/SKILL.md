---
name: perf-profiler
description: 分析和优化应用程序性能。适用于诊断代码运行缓慢的问题、测量CPU/内存使用情况、生成性能分析图表（火焰图）、对函数进行基准测试、对API进行负载测试、查找内存泄漏问题，以及优化数据库查询。
metadata: {"clawdbot":{"emoji":"⚡","requires":{"anyBins":["node","python3","go","curl","ab"]},"os":["linux","darwin","win32"]}}
---

# 性能分析工具

用于测量、分析并优化应用程序的性能。涵盖CPU性能分析、内存分析、火焰图生成、基准测试、负载测试以及针对不同语言的优化技巧。

## 使用场景

- 诊断应用程序或函数运行缓慢的原因
- 测量CPU和内存使用情况
- 生成火焰图以可视化代码中耗时最多的部分
- 对函数或API端点进行基准测试
- 在部署前对API进行负载测试
- 查找并修复内存泄漏问题
- 优化数据库查询性能
- 比较修改前后的性能差异

## 快速性能测试

### 命令行性能测试

```bash
# Time any command
time my-command --flag

# More precise: multiple runs with stats
for i in $(seq 1 10); do
  /usr/bin/time -f "%e" my-command 2>&1
done | awk '{sum+=$1; sumsq+=$1*$1; count++} END {
  avg=sum/count;
  stddev=sqrt(sumsq/count - avg*avg);
  printf "runs=%d avg=%.3fs stddev=%.3fs\n", count, avg, stddev
}'

# Hyperfine (better benchmarking tool)
# Install: https://github.com/sharkdp/hyperfine
hyperfine 'command-a' 'command-b'
hyperfine --warmup 3 --runs 20 'my-command'
hyperfine --export-json results.json 'old-version' 'new-version'
```

### 内联性能测试（适用于多种语言）

```javascript
// Node.js
console.time('operation');
await doExpensiveThing();
console.timeEnd('operation'); // "operation: 142.3ms"

// High-resolution
const start = performance.now();
await doExpensiveThing();
const elapsed = performance.now() - start;
console.log(`Elapsed: ${elapsed.toFixed(2)}ms`);
```

```python
# Python
import time

start = time.perf_counter()
do_expensive_thing()
elapsed = time.perf_counter() - start
print(f"Elapsed: {elapsed:.4f}s")

# Context manager
from contextlib import contextmanager

@contextmanager
def timer(label=""):
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    print(f"{label}: {elapsed:.4f}s")

with timer("data processing"):
    process_data()
```

```go
// Go
start := time.Now()
doExpensiveThing()
fmt.Printf("Elapsed: %v\n", time.Since(start))
```

## Node.js 性能分析

### 使用V8 Inspector进行CPU性能分析

```bash
# Generate CPU profile (writes .cpuprofile file)
node --cpu-prof app.js
# Open the .cpuprofile in Chrome DevTools > Performance tab

# Profile for a specific duration
node --cpu-prof --cpu-prof-interval=100 app.js

# Inspect running process
node --inspect app.js
# Open chrome://inspect in Chrome, click "inspect"
# Go to Performance tab, click Record
```

### 内存快照分析

```bash
# Generate heap snapshot
node --heap-prof app.js

# Take snapshots programmatically
node -e "
const v8 = require('v8');
const fs = require('fs');

// Take snapshot
const snapshotStream = v8.writeHeapSnapshot();
console.log('Heap snapshot written to:', snapshotStream);
"

# Compare heap snapshots to find leaks:
# 1. Take snapshot A (baseline)
# 2. Run operations that might leak
# 3. Take snapshot B
# 4. In Chrome DevTools > Memory, load both and use "Comparison" view
```

### 内存使用监控

```javascript
// Print memory usage periodically
setInterval(() => {
  const usage = process.memoryUsage();
  console.log({
    rss: `${(usage.rss / 1024 / 1024).toFixed(1)}MB`,
    heapUsed: `${(usage.heapUsed / 1024 / 1024).toFixed(1)}MB`,
    heapTotal: `${(usage.heapTotal / 1024 / 1024).toFixed(1)}MB`,
    external: `${(usage.external / 1024 / 1024).toFixed(1)}MB`,
  });
}, 5000);

// Detect memory growth
let lastHeap = 0;
setInterval(() => {
  const heap = process.memoryUsage().heapUsed;
  const delta = heap - lastHeap;
  if (delta > 1024 * 1024) { // > 1MB growth
    console.warn(`Heap grew by ${(delta / 1024 / 1024).toFixed(1)}MB`);
  }
  lastHeap = heap;
}, 10000);
```

### Node.js 基准测试

```javascript
// Simple benchmark function
function benchmark(name, fn, iterations = 10000) {
  // Warmup
  for (let i = 0; i < 100; i++) fn();

  const start = performance.now();
  for (let i = 0; i < iterations; i++) fn();
  const elapsed = performance.now() - start;

  console.log(`${name}: ${(elapsed / iterations).toFixed(4)}ms/op (${iterations} iterations in ${elapsed.toFixed(1)}ms)`);
}

benchmark('JSON.parse', () => JSON.parse('{"key":"value","num":42}'));
benchmark('regex match', () => /^\d{4}-\d{2}-\d{2}$/.test('2026-02-03'));
```

## Python 性能分析

### 使用cProfile（内置CPU性能分析工具）

```bash
# Profile a script
python3 -m cProfile -s cumulative my_script.py

# Save to file for analysis
python3 -m cProfile -o profile.prof my_script.py

# Analyze saved profile
python3 -c "
import pstats
stats = pstats.Stats('profile.prof')
stats.sort_stats('cumulative')
stats.print_stats(20)
"

# Profile a specific function
python3 -c "
import cProfile
from my_module import expensive_function

cProfile.run('expensive_function()', sort='cumulative')
"
```

### 使用line_profiler（逐行分析工具）

```bash
# Install
pip install line_profiler

# Add @profile decorator to functions of interest, then:
kernprof -l -v my_script.py
```

```python
# Programmatic usage
from line_profiler import LineProfiler

def process_data(data):
    result = []
    for item in data:           # Is this loop the bottleneck?
        transformed = transform(item)
        if validate(transformed):
            result.append(transformed)
    return result

profiler = LineProfiler()
profiler.add_function(process_data)
profiler.enable()
process_data(large_dataset)
profiler.disable()
profiler.print_stats()
```

### Python内存分析

```bash
# memory_profiler
pip install memory_profiler

# Profile memory line-by-line
python3 -m memory_profiler my_script.py
```

```python
from memory_profiler import profile

@profile
def load_data():
    data = []
    for i in range(1000000):
        data.append({'id': i, 'value': f'item_{i}'})
    return data

# Track memory over time
import tracemalloc

tracemalloc.start()

# ... run code ...

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
```

### Python基准测试

```python
import timeit

# Time a statement
result = timeit.timeit('sorted(range(1000))', number=10000)
print(f"sorted: {result:.4f}s for 10000 iterations")

# Compare two approaches
setup = "data = list(range(10000))"
t1 = timeit.timeit('list(filter(lambda x: x % 2 == 0, data))', setup=setup, number=1000)
t2 = timeit.timeit('[x for x in data if x % 2 == 0]', setup=setup, number=1000)
print(f"filter: {t1:.4f}s  |  listcomp: {t2:.4f}s  |  speedup: {t1/t2:.2f}x")

# pytest-benchmark
# pip install pytest-benchmark
# def test_sort(benchmark):
#     benchmark(sorted, list(range(1000)))
```

## Go语言性能分析

### 使用pprof（内置性能分析工具）

```go
// Add to main.go for HTTP-accessible profiling
import (
    "net/http"
    _ "net/http/pprof"
)

func main() {
    go func() {
        http.ListenAndServe("localhost:6060", nil)
    }()
    // ... rest of app
}
```

```bash
# CPU profile (30 seconds)
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30

# Memory profile
go tool pprof http://localhost:6060/debug/pprof/heap

# Goroutine profile
go tool pprof http://localhost:6060/debug/pprof/goroutine

# Inside pprof interactive mode:
# top 20          - top functions by CPU/memory
# list funcName   - source code with annotations
# web             - open flame graph in browser
# png > out.png   - save call graph as image
```

### Go语言基准测试

```go
// math_test.go
func BenchmarkAdd(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Add(42, 58)
    }
}

func BenchmarkSort1000(b *testing.B) {
    data := make([]int, 1000)
    for i := range data {
        data[i] = rand.Intn(1000)
    }
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        sort.Ints(append([]int{}, data...))
    }
}
```

```bash
# Run benchmarks
go test -bench=. -benchmem ./...

# Compare before/after
go test -bench=. -count=5 ./... > old.txt
# ... make changes ...
go test -bench=. -count=5 ./... > new.txt
go install golang.org/x/perf/cmd/benchstat@latest
benchstat old.txt new.txt
```

## 火焰图

### 生成火焰图

```bash
# Node.js: 0x (easiest)
npx 0x app.js
# Opens interactive flame graph in browser

# Node.js: clinic.js (comprehensive)
npx clinic flame -- node app.js
npx clinic doctor -- node app.js
npx clinic bubbleprof -- node app.js

# Python: py-spy (sampling profiler, no code changes needed)
pip install py-spy
py-spy record -o flame.svg -- python3 my_script.py

# Profile running Python process
py-spy record -o flame.svg --pid 12345

# Go: built-in
go tool pprof -http=:8080 http://localhost:6060/debug/pprof/profile?seconds=30
# Navigate to "Flame Graph" view

# Linux (any process): perf + flamegraph
perf record -g -p PID -- sleep 30
perf script | stackcollapse-perf.pl | flamegraph.pl > flame.svg
```

### 阅读火焰图

```
Key concepts:
- X-axis: NOT time. It's alphabetical sort of stack frames. Width = % of samples.
- Y-axis: Stack depth. Top = leaf function (where CPU time is spent).
- Wide bars at the top = hot functions (optimize these first).
- Narrow tall stacks = deep call chains (may indicate excessive abstraction).

What to look for:
1. Wide plateaus at the top → function that dominates CPU time
2. Multiple paths converging to one function → shared bottleneck
3. GC/runtime frames taking significant width → memory pressure
4. Unexpected functions appearing wide → performance bug
```

## 负载测试

### 基于curl的快速测试

```bash
# Single request timing
curl -o /dev/null -s -w "HTTP %{http_code} | Total: %{time_total}s | TTFB: %{time_starttransfer}s | Connect: %{time_connect}s\n" https://api.example.com/endpoint

# Multiple requests in sequence
for i in $(seq 1 20); do
  curl -o /dev/null -s -w "%{time_total}\n" https://api.example.com/endpoint
done | awk '{sum+=$1; count++; if($1>max)max=$1} END {printf "avg=%.3fs max=%.3fs n=%d\n", sum/count, max, count}'
```

### Apache Bench (ab)

```bash
# 100 requests, 10 concurrent
ab -n 100 -c 10 http://localhost:3000/api/endpoint

# With POST data
ab -n 100 -c 10 -p data.json -T application/json http://localhost:3000/api/endpoint

# Key metrics to watch:
# - Requests per second (throughput)
# - Time per request (latency)
# - Percentage of requests served within a certain time (p50, p90, p99)
```

### wrk（现代负载测试工具）

```bash
# Install: https://github.com/wg/wrk
# 10 seconds, 4 threads, 100 connections
wrk -t4 -c100 -d10s http://localhost:3000/api/endpoint

# With Lua script for custom requests
wrk -t4 -c100 -d10s -s post.lua http://localhost:3000/api/endpoint
```

### Autocannon（Node.js负载测试工具）

```bash
npx autocannon -c 100 -d 10 http://localhost:3000/api/endpoint
npx autocannon -c 100 -d 10 -m POST -b '{"key":"value"}' -H 'Content-Type=application/json' http://localhost:3000/api/endpoint
```

## 数据库查询性能优化

### 使用EXPLAIN进行分析

```bash
# PostgreSQL
psql -c "EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT * FROM orders WHERE user_id = 123;"

# MySQL
mysql -e "EXPLAIN SELECT * FROM orders WHERE user_id = 123;" mydb

# SQLite
sqlite3 mydb.sqlite "EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 123;"
```

### 检测慢速查询

```bash
# PostgreSQL: enable slow query logging
# In postgresql.conf:
# log_min_duration_statement = 100  (ms)

# MySQL: slow query log
# In my.cnf:
# slow_query_log = 1
# long_query_time = 0.1

# Find queries missing indexes (PostgreSQL)
psql -c "
SELECT schemaname, relname, seq_scan, seq_tup_read,
       idx_scan, idx_tup_fetch,
       seq_tup_read / GREATEST(seq_scan, 1) AS avg_rows_per_scan
FROM pg_stat_user_tables
WHERE seq_scan > 100 AND seq_tup_read / GREATEST(seq_scan, 1) > 1000
ORDER BY seq_tup_read DESC
LIMIT 10;
"
```

## 内存泄漏检测

### Node.js

```javascript
// Track object counts over time
const v8 = require('v8');

function checkMemory() {
  const heap = v8.getHeapStatistics();
  const usage = process.memoryUsage();
  return {
    heapUsedMB: (usage.heapUsed / 1024 / 1024).toFixed(1),
    heapTotalMB: (usage.heapTotal / 1024 / 1024).toFixed(1),
    rssMB: (usage.rss / 1024 / 1024).toFixed(1),
    externalMB: (usage.external / 1024 / 1024).toFixed(1),
    arrayBuffersMB: (usage.arrayBuffers / 1024 / 1024).toFixed(1),
  };
}

// Sample every 10s, alert on growth
let baseline = process.memoryUsage().heapUsed;
setInterval(() => {
  const current = process.memoryUsage().heapUsed;
  const growthMB = (current - baseline) / 1024 / 1024;
  if (growthMB > 50) {
    console.warn(`Memory grew ${growthMB.toFixed(1)}MB since start`);
    console.warn(checkMemory());
  }
}, 10000);
```

### 常见的内存泄漏类型

```
Node.js:
- Event listeners not removed (emitter.on without emitter.off)
- Closures capturing large objects in long-lived scopes
- Global caches without eviction (Map/Set that only grows)
- Unresolved promises accumulating

Python:
- Circular references (use weakref for caches)
- Global lists/dicts that grow unbounded
- File handles not closed (use context managers)
- C extension objects not properly freed

Go:
- Goroutine leaks (goroutine started, never returns)
- Forgotten channel listeners
- Unclosed HTTP response bodies
- Global maps that grow forever
```

## 性能对比脚本

```bash
#!/bin/bash
# perf-compare.sh - Compare performance before/after a change
# Usage: perf-compare.sh <command> [runs]
CMD="${1:?Usage: perf-compare.sh <command> [runs]}"
RUNS="${2:-10}"

echo "Benchmarking: $CMD"
echo "Runs: $RUNS"
echo ""

times=()
for i in $(seq 1 "$RUNS"); do
  start=$(date +%s%N)
  eval "$CMD" > /dev/null 2>&1
  end=$(date +%s%N)
  elapsed=$(echo "scale=3; ($end - $start) / 1000000" | bc)
  times+=("$elapsed")
  printf "  Run %2d: %sms\n" "$i" "$elapsed"
done

echo ""
printf '%s\n' "${times[@]}" | awk '{
  sum += $1
  sumsq += $1 * $1
  if (NR == 1 || $1 < min) min = $1
  if (NR == 1 || $1 > max) max = $1
  count++
} END {
  avg = sum / count
  stddev = sqrt(sumsq/count - avg*avg)
  printf "Results: avg=%.1fms min=%.1fms max=%.1fms stddev=%.1fms (n=%d)\n", avg, min, max, stddev, count
}'
```

## 使用建议

- **先分析再优化。** 直接猜测性能瓶颈的位置往往是不准确的，应先进行实际测量。
- **优先优化耗时最多的代码段。** 火焰图能清晰显示哪些函数消耗了最多的时间。对于占CPU时间80%的函数，提高10%的性能比对于只占2%时间的函数提高50%的性能更有意义。
- **内存问题和CPU问题不同。** 快速运行的代码也可能存在内存泄漏；而内存使用稳定的代码也可能存在CPU瓶颈。应分别对这两方面进行性能分析。
- **在真实环境下进行基准测试。** 微基准测试（如空循环、单函数测试）可能因JIT优化、缓存机制和分支预测而产生误导。应使用真实的数据和工作负载进行测试。
- **关注99百分位的数据。** 一个API的平均响应时间为50毫秒，但99百分位的响应时间为2秒，说明存在严重的延迟问题。应关注数据分布的百分位数，而不仅仅是平均值。
- **在发布前进行负载测试。** 使用`ab`、`wrk`或`autocannon`在预期的高峰流量下测试60秒，可以发现单元测试无法发现的问题。
- **垃圾回收（GC）会导致延迟。** 在Node.js、Python、Go和Java中，垃圾回收操作可能会引起性能波动。如果火焰图显示垃圾回收时间较长，应减少内存分配压力（重用对象、使用对象池、避免不必要的数据复制）。
- **数据库查询通常是性能瓶颈。** 在优化应用程序代码之前，先对最慢的查询使用`EXPLAIN`进行分析。适当的索引优化可以将原本需要2秒的查询时间缩短至2毫秒。