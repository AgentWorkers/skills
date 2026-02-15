---
name: kafka-streams-topology
description: Kafka Streams 拓扑设计专家。深入研究 KStream、KTable 和 GlobalKTable 的区别，掌握各种拓扑模式，以及流处理操作（如过滤、映射、扁平化映射、分支操作）、数据连接（join）、窗口化策略和“恰好一次”（exactly-once）语义。专注于 Kafka Streams 拓扑设计、KStream、KTable 的使用，以及流处理相关的技术实现细节。
---

# Kafka Streams 拓扑技能

具备使用 Kafka Streams 库构建 Java/Kotlin 流处理拓扑结构的专家级知识。

## 我所掌握的内容

### 核心抽象概念

**KStream**（事件流 - 无界、仅支持追加操作）：
- 表示不可变的事件序列
- 每条记录都是一个独立事件
- 适用于：点击流、交易数据、传感器读数等场景

**KTable**（变更日志流 - 按键存储最新状态）：
- 表示可变状态（压缩后的主题）
- 更新会覆盖之前的值（按键进行）
- 适用于：用户资料、产品目录、账户余额等场景

**GlobalKTable**（全局表 - 在所有实例上均可用）：
- 整个表会被复制到每个流实例中
- 不进行分区（广播式传输）
- 适用于：参考数据（国家、产品信息）查询等场景

**关键区别**：
```java
// KStream: Every event is independent
KStream<Long, Click> clicks = builder.stream("clicks");
clicks.foreach((key, value) -> {
    System.out.println(value); // Prints every click event
});

// KTable: Latest value wins (by key)
KTable<Long, User> users = builder.table("users");
users.toStream().foreach((key, value) -> {
    System.out.println(value); // Prints only current user state
});

// GlobalKTable: Replicated to all instances (no partitioning)
GlobalKTable<Long, Product> products = builder.globalTable("products");
// Available for lookups on any instance (no repartitioning needed)
```

## 何时需要使用此技能

当您需要以下帮助时，请使用我：
- 拓扑设计（“如何设计 Kafka Streams 拓扑？”）
- KStream 与 KTable 的选择（“何时使用 KStream，何时使用 KTable？”）
- 流操作（“过滤和转换事件”）
- 连接操作（“将 KStream 与 KTable 连接起来”）
- 窗口操作（“滚动窗口、跳跃窗口、会话窗口”）
- 一次精确处理语义（“启用 Exactly-once 语义”）
- 拓扑优化（“优化流处理性能”）

## 常见模式

### 模式 1：过滤和转换

**用例**：清洗和丰富事件数据

```java
StreamsBuilder builder = new StreamsBuilder();

// Input stream
KStream<Long, ClickEvent> clicks = builder.stream("clicks");

// Filter out bot clicks
KStream<Long, ClickEvent> humanClicks = clicks
    .filter((key, value) -> !value.isBot());

// Transform: Extract page from URL
KStream<Long, String> pages = humanClicks
    .mapValues(click -> extractPage(click.getUrl()));

// Write to output topic
pages.to("pages");
```

### 模式 2：根据条件分支事件流

**用例**：将事件路由到不同的处理路径

```java
Map<String, KStream<Long, Order>> branches = orders
    .split(Named.as("order-"))
    .branch((key, order) -> order.getTotal() > 1000, Branched.as("high-value"))
    .branch((key, order) -> order.getTotal() > 100, Branched.as("medium-value"))
    .defaultBranch(Branched.as("low-value"));

// High-value orders → priority processing
branches.get("order-high-value").to("priority-orders");

// Low-value orders → standard processing
branches.get("order-low-value").to("standard-orders");
```

### 模式 3：通过表来丰富流数据（流-表连接）

**用例**：为点击事件添加用户详细信息

```java
// Users table (current state)
KTable<Long, User> users = builder.table("users");

// Clicks stream
KStream<Long, ClickEvent> clicks = builder.stream("clicks");

// Enrich clicks with user data (left join)
KStream<Long, EnrichedClick> enriched = clicks.leftJoin(
    users,
    (click, user) -> new EnrichedClick(
        click.getPage(),
        user != null ? user.getName() : "unknown",
        user != null ? user.getEmail() : "unknown"
    ),
    Joined.with(Serdes.Long(), clickSerde, userSerde)
);

enriched.to("enriched-clicks");
```

### 模式 4：使用窗口功能进行聚合

**用例**：计算每 5 分钟内每个用户的点击次数

```java
KTable<Windowed<Long>, Long> clickCounts = clicks
    .groupByKey()
    .windowedBy(TimeWindows.of(Duration.ofMinutes(5)))
    .count(Materialized.as("click-counts-store"));

// Convert to stream for output
clickCounts.toStream()
    .map((windowedKey, count) -> {
        Long userId = windowedKey.key();
        Instant start = windowedKey.window().startTime();
        Instant end = windowedKey.window().endTime();
        return KeyValue.pair(userId, new WindowedCount(userId, start, end, count));
    })
    .to("click-counts");
```

### 模式 5：结合状态存储进行状态处理

**用例**：检测 10 分钟内的重复事件

```java
// Define state store
StoreBuilder<KeyValueStore<Long, Long>> storeBuilder =
    Stores.keyValueStoreBuilder(
        Stores.persistentKeyValueStore("dedup-store"),
        Serdes.Long(),
        Serdes.Long()
    );

builder.addStateStore(storeBuilder);

// Deduplicate events
KStream<Long, Event> deduplicated = events.transformValues(
    () -> new ValueTransformerWithKey<Long, Event, Event>() {
        private KeyValueStore<Long, Long> store;

        @Override
        public void init(ProcessorContext context) {
            this.store = context.getStateStore("dedup-store");
        }

        @Override
        public Event transform(Long key, Event value) {
            Long lastSeen = store.get(key);
            long now = System.currentTimeMillis();

            // Duplicate detected (within 10 minutes)
            if (lastSeen != null && (now - lastSeen) < 600_000) {
                return null; // Drop duplicate
            }

            // Not duplicate, store timestamp
            store.put(key, now);
            return value;
        }
    },
    "dedup-store"
).filter((key, value) -> value != null); // Remove nulls

deduplicated.to("unique-events");
```

## 连接类型

### 1. 流-流连接（内连接）

**用例**：在时间窗口内关联相关事件

```java
// Page views and clicks within 10 minutes
KStream<Long, PageView> views = builder.stream("page-views");
KStream<Long, Click> clicks = builder.stream("clicks");

KStream<Long, ClickWithView> joined = clicks.join(
    views,
    (click, view) -> new ClickWithView(click, view),
    JoinWindows.of(Duration.ofMinutes(10)),
    StreamJoined.with(Serdes.Long(), clickSerde, viewSerde)
);
```

### 2. 流-表连接（左连接）

**用例**：用当前状态丰富事件数据

```java
// Add product details to order items
KTable<Long, Product> products = builder.table("products");
KStream<Long, OrderItem> items = builder.stream("order-items");

KStream<Long, EnrichedOrderItem> enriched = items.leftJoin(
    products,
    (item, product) -> new EnrichedOrderItem(
        item,
        product != null ? product.getName() : "Unknown",
        product != null ? product.getPrice() : 0.0
    )
);
```

### 3. 表-表连接（内连接）

**用例**：合并两个表的数据（获取最新状态）

```java
// Join users with their current shopping cart
KTable<Long, User> users = builder.table("users");
KTable<Long, Cart> carts = builder.table("shopping-carts");

KTable<Long, UserWithCart> joined = users.join(
    carts,
    (user, cart) -> new UserWithCart(user.getName(), cart.getTotal())
);
```

### 4. 流-全局表连接

**用例**：使用参考数据进行数据丰富（无需分区）

```java
// Add country details to user registrations
GlobalKTable<String, Country> countries = builder.globalTable("countries");
KStream<Long, UserRegistration> registrations = builder.stream("registrations");

KStream<Long, EnrichedRegistration> enriched = registrations.leftJoin(
    countries,
    (userId, registration) -> registration.getCountryCode(), // Key extractor
    (registration, country) -> new EnrichedRegistration(
        registration,
        country != null ? country.getName() : "Unknown"
    )
);
```

## 窗口策略

### 滚动窗口（非重叠）

**用例**：按固定时间周期进行数据聚合

```java
// Count events every 5 minutes
KTable<Windowed<Long>, Long> counts = events
    .groupByKey()
    .windowedBy(TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(5)))
    .count();

// Windows: [0:00-0:05), [0:05-0:10), [0:10-0:15)
```

### 跳跃窗口（重叠）

**用例**：计算移动平均值或进行重叠数据聚合

```java
// Count events in 10-minute windows, advancing every 5 minutes
KTable<Windowed<Long>, Long> counts = events
    .groupByKey()
    .windowedBy(TimeWindows.ofSizeAndGrace(
        Duration.ofMinutes(10),
        Duration.ofMinutes(5)
    ).advanceBy(Duration.ofMinutes(5)))
    .count();

// Windows: [0:00-0:10), [0:05-0:15), [0:10-0:20)
```

### 会话窗口（基于事件）

**用例**：检测用户会话中的不活跃间隔

```java
// Session ends after 30 minutes of inactivity
KTable<Windowed<Long>, Long> sessionCounts = events
    .groupByKey()
    .windowedBy(SessionWindows.ofInactivityGapWithNoGrace(Duration.ofMinutes(30)))
    .count();
```

### 滑动窗口（连续）

**用例**：在滑动时间窗口内检测异常行为

```java
// Detect >100 events in any 1-minute period
KTable<Windowed<Long>, Long> slidingCounts = events
    .groupByKey()
    .windowedBy(SlidingWindows.ofTimeDifferenceWithNoGrace(Duration.ofMinutes(1)))
    .count();
```

## 最佳实践

### 1. 正确选择分区键

✅ **应该这样做**：
```java
// Repartition by user_id before aggregation
KStream<Long, Event> byUser = events
    .selectKey((key, value) -> value.getUserId());

// Now aggregation is efficient
KTable<Long, Long> userCounts = byUser
    .groupByKey()
    .count();
```

❌ **不应该这样做**：
```java
// WRONG: groupBy with different key (triggers repartitioning!)
KTable<Long, Long> userCounts = events
    .groupBy((key, value) -> KeyValue.pair(value.getUserId(), value))
    .count();
```

### 2. 选择合适的序列化/反序列化器（Serdes）

✅ **应该这样做**：
```java
// Define custom serde for complex types
Serde<User> userSerde = new JsonSerde<>(User.class);

KStream<Long, User> users = builder.stream(
    "users",
    Consumed.with(Serdes.Long(), userSerde)
);
```

❌ **不应该这样做**：
```java
// WRONG: No serde specified (uses default String serde!)
KStream<Long, User> users = builder.stream("users");
```

### 3. 启用一次精确处理语义

✅ **应该这样做**：
```java
Properties props = new Properties();
props.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG,
    StreamsConfig.EXACTLY_ONCE_V2); // EOS v2 (recommended)
props.put(StreamsConfig.COMMIT_INTERVAL_MS_CONFIG, 100); // Commit frequently
```

### 4. 使用物化存储进行查询

✅ **应该这样做**：
```java
// Named store for interactive queries
KTable<Long, Long> counts = events
    .groupByKey()
    .count(Materialized.<Long, Long, KeyValueStore<Bytes, byte[]>>as("user-counts")
        .withKeySerde(Serdes.Long())
        .withValueSerde(Serdes.Long()));

// Query store from REST API
ReadOnlyKeyValueStore<Long, Long> store =
    streams.store(StoreQueryParameters.fromNameAndType(
        "user-counts",
        QueryableStoreTypes.keyValueStore()
    ));

Long count = store.get(userId);
```

## 拓扑优化

### 1. 合并相关操作

**好的做法**（一次完成所有操作）：
```java
KStream<Long, String> result = events
    .filter((key, value) -> value.isValid())
    .mapValues(value -> value.toUpperCase())
    .filterNot((key, value) -> value.contains("test"));
```

**不好的做法**（使用多个中间主题）：
```java
KStream<Long, Event> valid = events.filter((key, value) -> value.isValid());
valid.to("valid-events"); // Unnecessary write

KStream<Long, Event> fromValid = builder.stream("valid-events");
KStream<Long, String> upper = fromValid.mapValues(v -> v.toUpperCase());
```

### 2. 重用 KTable

**好的做法**（共享数据表）：
```java
KTable<Long, User> users = builder.table("users");

KStream<Long, EnrichedClick> enrichedClicks = clicks.leftJoin(users, ...);
KStream<Long, EnrichedOrder> enrichedOrders = orders.leftJoin(users, ...);
```

**不好的做法**（创建重复的数据表）：
```java
KTable<Long, User> users1 = builder.table("users");
KTable<Long, User> users2 = builder.table("users"); // Duplicate!
```

## 拓扑测试

### 拓扑测试工具

```java
@Test
public void testClickFilter() {
    // Setup topology
    StreamsBuilder builder = new StreamsBuilder();
    KStream<Long, Click> clicks = builder.stream("clicks");
    clicks.filter((key, value) -> !value.isBot())
          .to("human-clicks");

    Topology topology = builder.build();

    // Create test driver
    TopologyTestDriver testDriver = new TopologyTestDriver(topology);

    // Input topic
    TestInputTopic<Long, Click> inputTopic = testDriver.createInputTopic(
        "clicks",
        Serdes.Long().serializer(),
        clickSerde.serializer()
    );

    // Output topic
    TestOutputTopic<Long, Click> outputTopic = testDriver.createOutputTopic(
        "human-clicks",
        Serdes.Long().deserializer(),
        clickSerde.deserializer()
    );

    // Send test data
    inputTopic.pipeInput(1L, new Click(1L, "page1", false)); // Human
    inputTopic.pipeInput(2L, new Click(2L, "page2", true));  // Bot

    // Assert output
    List<Click> output = outputTopic.readValuesToList();
    assertEquals(1, output.size()); // Only human click
    assertFalse(output.get(0).isBot());

    testDriver.close();
}
```

## 常见问题及解决方法

### 问题 1：StreamsException - 分区不匹配

**错误**：连接的流/表的分区数量不一致
**根本原因**：分区数量不同
**解决方法**：重新分区以匹配数据：

```java
// Ensure same partition count
KStream<Long, Event> repartitioned = events
    .through("events-repartitioned",
        Produced.with(Serdes.Long(), eventSerde)
            .withStreamPartitioner((topic, key, value, numPartitions) ->
                (int) (key % 12) // Match target partition count
            )
    );
```

### 问题 2：内存不足（状态存储占用过多）

**错误**：Java 堆内存不足
**根本原因**：状态存储空间过大，未使用窗口功能
**解决方法**：添加基于时间的清理机制：

```java
// Use windowing to limit state size
KTable<Windowed<Long>, Long> counts = events
    .groupByKey()
    .windowedBy(TimeWindows.ofSizeAndGrace(
        Duration.ofHours(24),     // Window size
        Duration.ofHours(1)       // Grace period
    ))
    .count();
```

### 问题 3：延迟高，处理速度慢

**根本原因**：阻塞操作或转换效率低下
**解决方法**：采用异步处理方式：

```java
// BAD: Blocking HTTP call
events.mapValues(value -> {
    return httpClient.get(value.getUrl()); // BLOCKS!
});

// GOOD: Async processing with state store
events.transformValues(() -> new AsyncEnricher());
```

## 参考资料

- Kafka Streams 文档：https://kafka.apache.org/documentation/streams/
- Kafka Streams 教程：https://kafka.apache.org/documentation/streams/tutorial
- 测试指南：https://kafka.apache.org/documentation/streams/developer-guide/testing.html

---

**当您需要关于拓扑设计、连接操作、窗口处理或一次精确处理语义方面的帮助时，请随时调用我！**