---
name: realtime-react-hooks
model: standard
description: React 钩子用于实现实时数据功能，支持与 SSE（Server-Sent Events）、WebSocket 和 SWR（Server-Wide React）的集成。涵盖了连接管理、重新连接逻辑以及乐观更新（optimistic updates）等关键方面。适用于开发具有实时功能的 React 应用程序。可以通过 SSE 钩子、WebSocket 钩子以及 `useEventSource` 来触发实时数据更新，实现数据的实时同步与展示。
---

# 实时 React Hooks

在 React 应用程序中，使用 SSE（Server-Side Rendering）、WebSocket 和 SWR（Server-Wide React）来实现实时数据更新的常用模式。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install realtime-react-hooks
```


---

## 适用场景

- 需要实时数据更新的 React 应用程序
- 显示实时指标的仪表板
- 聊天界面、通知功能
- 任何无需刷新即可更新的用户界面

---

## 模式 1：SSE Hook

```typescript
import { useEffect, useRef, useState, useCallback } from 'react';

interface UseSSEOptions<T> {
  url: string;
  onMessage?: (data: T) => void;
  onError?: (error: Event) => void;
  enabled?: boolean;
}

export function useSSE<T>({
  url,
  onMessage,
  onError,
  enabled = true,
}: UseSSEOptions<T>) {
  const [data, setData] = useState<T | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    if (!enabled) return;

    const eventSource = new EventSource(url);
    eventSourceRef.current = eventSource;

    eventSource.onopen = () => {
      setIsConnected(true);
    };

    eventSource.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data) as T;
        setData(parsed);
        onMessage?.(parsed);
      } catch (e) {
        console.error('SSE parse error:', e);
      }
    };

    eventSource.onerror = (error) => {
      setIsConnected(false);
      onError?.(error);
    };

    return () => {
      eventSource.close();
      eventSourceRef.current = null;
    };
  }, [url, enabled]);

  const close = useCallback(() => {
    eventSourceRef.current?.close();
    setIsConnected(false);
  }, []);

  return { data, isConnected, close };
}
```

---

## 模式 2：带自动重连功能的 WebSocket Hook

```typescript
interface UseWebSocketOptions {
  url: string;
  onMessage?: (data: unknown) => void;
  reconnect?: boolean;
  maxRetries?: number;
}

export function useWebSocket({
  url,
  onMessage,
  reconnect = true,
  maxRetries = 5,
}: UseWebSocketOptions) {
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const retriesRef = useRef(0);

  const connect = useCallback(() => {
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => {
      setIsConnected(true);
      retriesRef.current = 0;
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage?.(data);
      } catch {
        onMessage?.(event.data);
      }
    };

    ws.onclose = () => {
      setIsConnected(false);
      if (reconnect && retriesRef.current < maxRetries) {
        retriesRef.current++;
        const delay = Math.min(1000 * 2 ** retriesRef.current, 30000);
        setTimeout(connect, delay);
      }
    };

    ws.onerror = () => {
      ws.close();
    };
  }, [url, onMessage, reconnect, maxRetries]);

  useEffect(() => {
    connect();
    return () => wsRef.current?.close();
  }, [connect]);

  const send = useCallback((data: unknown) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data));
    }
  }, []);

  return { isConnected, send };
}
```

---

## 模式 3：使用 SWR 实现实时更新

```typescript
import useSWR from 'swr';
import { useEffect } from 'react';

export function useRealtimeData<T>(
  key: string,
  fetcher: () => Promise<T>
) {
  const { data, mutate, ...rest } = useSWR(key, fetcher);

  // Subscribe to real-time updates
  useEffect(() => {
    const eventSource = new EventSource(`/api/events/${key}`);

    eventSource.onmessage = (event) => {
      const update = JSON.parse(event.data);
      
      // Optimistically update cache
      mutate((current) => {
        if (!current) return update;
        return { ...current, ...update };
      }, false); // false = don't revalidate
    };

    return () => eventSource.close();
  }, [key, mutate]);

  return { data, mutate, ...rest };
}
```

---

## 模式 4：订阅式更新 Hook

```typescript
interface UseSubscriptionOptions {
  channels: string[];
  onEvent: (channel: string, data: unknown) => void;
}

export function useSubscription({ channels, onEvent }: UseSubscriptionOptions) {
  const { send, isConnected } = useWebSocket({
    url: '/api/ws',
    onMessage: (msg: any) => {
      if (msg.type === 'event') {
        onEvent(msg.channel, msg.data);
      }
    },
  });

  useEffect(() => {
    if (!isConnected) return;

    // Subscribe to channels
    channels.forEach((channel) => {
      send({ type: 'subscribe', channel });
    });

    return () => {
      channels.forEach((channel) => {
        send({ type: 'unsubscribe', channel });
      });
    };
  }, [channels, isConnected, send]);

  return { isConnected };
}
```

---

## 模式 5：连接状态指示器

```tsx
export function ConnectionStatus({ isConnected }: { isConnected: boolean }) {
  return (
    <div className="flex items-center gap-2">
      <span
        className={cn(
          'size-2 rounded-full',
          isConnected ? 'bg-success animate-pulse' : 'bg-destructive'
        )}
      />
      <span className="text-xs text-muted-foreground">
        {isConnected ? 'Live' : 'Disconnected'}
      </span>
    </div>
  );
}
```

---

## 相关技能

- **元技能：** [ai/skills/meta/realtime-dashboard/](../../meta/realtime-dashboard/) — 完整的实时仪表板指南
- [resilient-connections](../resilient-connections/) — 重试逻辑
- [design-systems/animated-financial-display](../../design-systems/animated-financial-display/) — 数字动画效果

---

## 绝对不要做的事情

- **务必清理资源** — 在组件卸载时关闭连接
- **不要无限重连** — 使用指数级退避策略设置最大重试次数
- **不要不加异常处理就解析数据** — 服务器可能发送格式错误的数据
- **不要直接修改数据后重新验证** — 使用 `mutate(data, false)` 进行乐观更新
- **不要忽略连接状态** — 当用户断开连接时必须通知用户

---

## 快速参考

```typescript
// SSE
const { data, isConnected } = useSSE({ url: '/api/events' });

// WebSocket
const { isConnected, send } = useWebSocket({
  url: 'wss://api.example.com/ws',
  onMessage: (data) => console.log(data),
});

// SWR + Real-time
const { data } = useRealtimeData('metrics', fetchMetrics);

// Subscriptions
useSubscription({
  channels: ['user:123', 'global'],
  onEvent: (channel, data) => updateState(channel, data),
});
```