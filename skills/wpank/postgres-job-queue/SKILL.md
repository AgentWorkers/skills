---
name: postgres-job-queue
model: standard
description: 基于 PostgreSQL 的作业队列系统，支持优先级调度、批量任务处理以及进度跟踪功能。适用于构建无需依赖外部组件的作业队列。该系统可用于触发 PostgreSQL 作业队列、后台任务、任务队列及优先级队列的相关操作，并支持 `SKIP LOCKED` 机制。
---

# PostgreSQL作业队列

这是一个基于PostgreSQL的作业队列解决方案，支持优先级调度、批量任务处理以及任务进度跟踪功能，适用于生产环境。

---

## 适用场景

- 需要作业队列功能，但希望避免依赖Redis/RabbitMQ；
- 任务需要根据优先级进行调度；
- 长时间运行的任务需要能够实时查看进度；
- 作业数据需要在服务重启后依然保持完整。

---

## 数据库架构设计

```sql
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_type VARCHAR(50) NOT NULL,
    priority INT NOT NULL DEFAULT 100,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    data JSONB NOT NULL DEFAULT '{}',
    
    -- Progress tracking
    progress INT DEFAULT 0,
    current_stage VARCHAR(100),
    events_count INT DEFAULT 0,
    
    -- Worker tracking
    worker_id VARCHAR(100),
    claimed_at TIMESTAMPTZ,
    
    -- Timing
    created_at TIMESTAMPTZ DEFAULT NOW(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    
    -- Retry handling
    attempts INT DEFAULT 0,
    max_attempts INT DEFAULT 3,
    last_error TEXT,
    
    CONSTRAINT valid_status CHECK (
        status IN ('pending', 'claimed', 'running', 'completed', 'failed', 'cancelled')
    )
);

-- Critical: Partial index for fast claiming
CREATE INDEX idx_jobs_claimable ON jobs (priority DESC, created_at ASC) 
    WHERE status = 'pending';
CREATE INDEX idx_jobs_worker ON jobs (worker_id) 
    WHERE status IN ('claimed', 'running');
```

---

## 使用`SKIP LOCKED`进行批量任务处理

```sql
CREATE OR REPLACE FUNCTION claim_job_batch(
    p_worker_id VARCHAR(100),
    p_job_types VARCHAR(50)[],
    p_batch_size INT DEFAULT 10
) RETURNS SETOF jobs AS $$
BEGIN
    RETURN QUERY
    WITH claimable AS (
        SELECT id
        FROM jobs
        WHERE status = 'pending'
          AND job_type = ANY(p_job_types)
          AND attempts < max_attempts
        ORDER BY priority DESC, created_at ASC
        LIMIT p_batch_size
        FOR UPDATE SKIP LOCKED  -- Critical: skip locked rows
    ),
    claimed AS (
        UPDATE jobs
        SET status = 'claimed',
            worker_id = p_worker_id,
            claimed_at = NOW(),
            attempts = attempts + 1
        WHERE id IN (SELECT id FROM claimable)
        RETURNING *
    )
    SELECT * FROM claimed;
END;
$$ LANGUAGE plpgsql;
```

---

## Go语言实现

```go
const (
    PriorityExplicit   = 150  // User-requested
    PriorityDiscovered = 100  // System-discovered
    PriorityBackfill   = 30   // Background backfills
)

type JobQueue struct {
    db       *pgx.Pool
    workerID string
}

func (q *JobQueue) Claim(ctx context.Context, types []string, batchSize int) ([]Job, error) {
    rows, err := q.db.Query(ctx,
        "SELECT * FROM claim_job_batch($1, $2, $3)",
        q.workerID, types, batchSize,
    )
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    var jobs []Job
    for rows.Next() {
        var job Job
        if err := rows.Scan(&job); err != nil {
            return nil, err
        }
        jobs = append(jobs, job)
    }
    return jobs, nil
}

func (q *JobQueue) Complete(ctx context.Context, jobID uuid.UUID) error {
    _, err := q.db.Exec(ctx, `
        UPDATE jobs 
        SET status = 'completed',
            progress = 100,
            completed_at = NOW()
        WHERE id = $1`,
        jobID,
    )
    return err
}

func (q *JobQueue) Fail(ctx context.Context, jobID uuid.UUID, errMsg string) error {
    _, err := q.db.Exec(ctx, `
        UPDATE jobs 
        SET status = CASE 
                WHEN attempts >= max_attempts THEN 'failed' 
                ELSE 'pending' 
            END,
            last_error = $2,
            worker_id = NULL,
            claimed_at = NULL
        WHERE id = $1`,
        jobID, errMsg,
    )
    return err
}
```

---

## 失效任务的恢复机制

```go
func (q *JobQueue) RecoverStaleJobs(ctx context.Context, timeout time.Duration) (int, error) {
    result, err := q.db.Exec(ctx, `
        UPDATE jobs 
        SET status = 'pending',
            worker_id = NULL,
            claimed_at = NULL
        WHERE status IN ('claimed', 'running')
          AND claimed_at < NOW() - $1::interval
          AND attempts < max_attempts`,
        timeout.String(),
    )
    if err != nil {
        return 0, err
    }
    return int(result.RowsAffected()), nil
}
```

---

## 决策树

| 场景 | 选择方案 |
|------|------|
| 需要保证任务一定能完成 | 使用PostgreSQL队列 |
| 需要低于毫秒级的延迟 | 改用Redis |
| 每秒处理任务数 < 1000个 | 使用PostgreSQL即可 |
| 每秒处理任务数 > 10000个 | 需要添加Redis层 |
| 需要严格的任务顺序 | 每种类型任务由单独的工作者处理 |

---

## 相关技能

- **相关技术：** [service-layer-architecture](../service-layer-architecture/) — 作业处理器的服务架构模式 |
- **相关技术：** [realtime/dual-stream-architecture](../../realtime/dual-stream-architecture/) — 作业任务的实时事件发布机制 |

---

## 绝对不要做的事情

- **绝对不要使用“SELECT后更新”的操作** — 这会导致竞态条件；请使用`SKIP LOCKED`机制。
- **绝对不要在没有`SKIP LOCKED`的情况下进行任务处理** — 否则会导致工作者程序死锁。
- **绝对不要存储大型数据 payload** — 只需要存储数据的引用即可。
- **绝对不要忘记创建部分索引** — 没有部分索引，任务处理效率会大大降低。