---
name: instantdb
description: 实时数据库集成与InstantDB：在使用InstantDB应用程序进行管理操作（创建/更新/删除实体、关联/解除关联关系、查询数据）以及订阅实时数据变更时，可运用此技能。触发条件包括涉及InstantDB的指令、实时更新、数据库同步、实体操作，或者当OpenClaw需要向用户实时发送操作更新信息时。
---

# InstantDB集成

## 概述

InstantDB的Node.js集成使得OpenClaw能够执行管理操作，并通过WebSocket订阅实时监控数据变化。

## 设置

安装依赖项：

```bash
npm install
```

设置环境变量：

```bash
export INSTANTDB_APP_ID="your-app-id"
export INSTANTDB_ADMIN_TOKEN="your-admin-token"
```

## 核心功能

### 1. 查询数据

使用InstantDB的查询语法获取数据：

```javascript
const { InstantDBClient } = require('./scripts/instantdb.js');

const client = new InstantDBClient(appId, adminToken);
const result = await client.query({
  tasks: {
    $: {
      where: { status: 'active' }
    }
  }
});
```

命令行界面（CLI）：

```bash
./scripts/instantdb.js query '{"tasks": {}}'
```

### 2. 创建实体

向命名空间中添加新实体：

```javascript
const { entityId, result } = await client.createEntity('tasks', {
  title: 'Process data',
  status: 'pending',
  priority: 'high'
});
```

命令行界面（CLI）：

```bash
./scripts/instantdb.js create tasks '{"title": "Process data", "status": "pending"}'
```

（可选）实体ID：

```bash
./scripts/instantdb.js create tasks '{"title": "Task"}' custom-entity-id
```

### 3. 更新实体

修改现有实体的属性：

```javascript
await client.updateEntity(entityId, 'tasks', {
  status: 'completed'
});
```

命令行界面（CLI）：

```bash
./scripts/instantdb.js update <entity-id> tasks '{"status": "completed"}'
```

### 4. 删除实体

删除实体：

```javascript
await client.deleteEntity(entityId, 'tasks');
```

命令行界面（CLI）：

```bash
./scripts/instantdb.js delete <entity-id> tasks
```

### 5. 关联实体

在实体之间创建关系：

```javascript
await client.linkEntities(taskId, assigneeId, 'assignees');
```

命令行界面（CLI）：

```bash
./scripts/instantdb.js link <parent-id> <child-id> assignees
```

### 6. 取消关联实体

删除实体之间的关系：

```javascript
await client.unlinkEntities(taskId, assigneeId, 'assignees');
```

命令行界面（CLI）：

```bash
./scripts/instantdb.js unlink <parent-id> <child-id> assignees
```

### 7. 实时订阅

通过WebSocket监控数据变化：

```javascript
const subscriptionId = client.subscribe(
  { tasks: { $: { where: { status: 'active' } } } },
  (data) => {
    console.log('Data updated:', data);
  },
  (error) => {
    console.error('Subscription error:', error);
  }
);

// Later: client.unsubscribe(subscriptionId);
```

命令行界面（监听指定时长）：

```bash
./scripts/instantdb.js subscribe '{"tasks": {}}' 60  # Listen for 60 seconds
```

### 8. 事务

使用事务构建器原子地执行多个操作：

```javascript
const { tx, id } = require('@instantdb/admin');

await client.transact([
  tx.tasks[id()].update({ title: 'Task 1' }),
  tx.tasks[id()].update({ title: 'Task 2' })
]);
```

命令行界面（CLI）：

```bash
./scripts/instantdb.js transact '[{"op": "update", "id": "...", "data": {...}}]'
```

## OpenClaw使用模式

### 操作状态更新

向人类观察者发送实时进度更新：

```javascript
const { id } = require('@instantdb/admin');

// Create status entity
const actionId = id();
await client.createEntity('actions', {
  type: 'file_processing',
  status: 'started',
  progress: 0,
  timestamp: Date.now()
}, actionId);

// Update progress
await client.updateEntity(actionId, 'actions', {
  progress: 50,
  status: 'processing'
});

// Mark complete
await client.updateEntity(actionId, 'actions', {
  progress: 100,
  status: 'completed'
});
```

### 多步骤工作流跟踪

跟踪复杂操作：

```javascript
const { tx, id } = require('@instantdb/admin');

const workflowId = id();
const steps = ['Extract', 'Transform', 'Validate', 'Load', 'Verify'];

// Initialize workflow with linked steps
const txs = [
  tx.workflows[workflowId].update({
    name: 'Data Pipeline',
    status: 'running',
    currentStep: 1,
    totalSteps: steps.length
  })
];

const stepIds = steps.map((name, i) => {
  const stepId = id();
  txs.push(
    tx.steps[stepId].update({
      name,
      order: i + 1,
      status: 'pending'
    }),
    tx.workflows[workflowId].link({ steps: stepId })
  );
  return stepId;
});

await client.transact(txs);

// Update as steps complete
for (let i = 0; i < stepIds.length; i++) {
  await client.updateEntity(stepIds[i], 'steps', { 
    status: 'completed' 
  });
  await client.updateEntity(workflowId, 'workflows', { 
    currentStep: i + 2 
  });
}
```

### 人类监控模式

人类订阅以观察OpenClaw的操作：

```javascript
// Human's frontend code
import { init } from '@instantdb/react';

const db = init({ appId });

function ActionMonitor() {
  const { data } = db.useQuery({
    actions: {
      $: {
        where: { status: { in: ['started', 'processing'] } }
      }
    }
  });
  
  return data?.actions?.map(action => (
    <div key={action.id}>
      {action.type}: {action.progress}%
    </div>
  ));
}
```

### 流式进度更新

对于长时间运行的操作，提供流式更新：

```javascript
const { id } = require('@instantdb/admin');

async function processLargeDataset(items) {
  const progressId = id();
  
  await client.createEntity('progress', {
    total: items.length,
    completed: 0,
    status: 'running'
  }, progressId);

  for (let i = 0; i < items.length; i++) {
    // Process item...
    await processItem(items[i]);
    
    // Update every 10 items
    if (i % 10 === 0) {
      await client.updateEntity(progressId, 'progress', {
        completed: i + 1,
        percentage: Math.round(((i + 1) / items.length) * 100)
      });
    }
  }

  await client.updateEntity(progressId, 'progress', {
    completed: items.length,
    percentage: 100,
    status: 'completed'
  });
}
```

## 事务模式

详细的事务模式请参阅`references/transactions.md`，包括：
- 批量操作
- 关系管理
- 条件更新
- 状态机
- 级联操作

## 错误处理

所有操作返回Promise对象，失败时会拒绝（reject）：

```javascript
try {
  const result = await client.createEntity('tasks', data);
} catch (error) {
  console.error('Operation failed:', error.message);
}
```

## 查询语法

详细的查询示例请参阅`references/query_syntax.md`，包括：
- Where子句和运算符
- 关系遍历
- 排序和分页
- 多层嵌套

## 参考资料

- InstantDB文档：https://www.instantdb.com/docs
- 管理SDK：https://www.instantdb.com/docs/admin
- 查询参考：请参阅`references/query_syntax.md`
- 事务模式：请参阅`references/transactions.md`