# Spring Boot 生产工程

> 为 Spring Boot 以及 Java/Kotlin 应用程序提供完整的生产工程方法论——包括架构设计、安全性、可观测性、测试、部署和性能优化。

## 快速健康检查

为您的 Spring Boot 应用程序打分（1 分表示需要改进，2 分表示基本合格）：

| 项目指标 | 检查内容 | 分数 |
|--------|-------|------|
| 🏗️ 架构 | 是否采用清晰的分层架构并使用了依赖注入？ | |
| 🔒 安全性 | 是否配置了 Spring Security，并启用了适当的认证、CORS 和 CSRF？ | |
| 📊 可观测性 | 是否有结构化的日志记录、指标收集和健康检查端点？ | |
| 🧪 测试 | 是否包含了单元测试、集成测试以及覆盖率超过 70% 的切片测试？ | |
| ⚡ 性能 | 是否使用了连接池、缓存，并在适当的地方实现了异步处理？ | |
| 🚀 部署 | 是否使用了容器化技术，并通过 CI/CD 实现了无停机时间的部署？ | |
| 📝 API 设计 | 是否提供了 OpenAPI 文档、版本控制以及一致的错误响应？ | |
| 🛡️ 弹性 | 是否配置了断路器、重试机制以及优雅的关闭流程？ | |

**总分：/16**  
→ ≤8 分：亟需改进  
→ 9-12 分：有待提升  
→ 13-14 分：表现良好  
→ 15-16 分：已具备生产环境所需的能力  

---

## 第 1 阶段：项目架构

### 推荐的项目结构

```
src/main/java/com/example/app/
├── Application.java                 # @SpringBootApplication entry
├── config/                          # Configuration classes
│   ├── SecurityConfig.java
│   ├── WebConfig.java
│   ├── CacheConfig.java
│   └── AsyncConfig.java
├── domain/                          # Domain models & business logic
│   ├── model/                       # JPA entities / domain objects
│   ├── repository/                  # Spring Data repositories
│   ├── service/                     # Business logic services
│   └── event/                       # Domain events
├── api/                             # REST controllers
│   ├── controller/                  # @RestController classes
│   ├── dto/                         # Request/Response DTOs
│   ├── mapper/                      # Entity ↔ DTO mappers
│   └── exception/                   # API exception handlers
├── infrastructure/                  # External integrations
│   ├── client/                      # REST/gRPC clients
│   ├── messaging/                   # Kafka/RabbitMQ producers/consumers
│   └── storage/                     # S3/file storage
└── common/                          # Shared utilities
    ├── exception/                   # Base exceptions
    ├── validation/                  # Custom validators
    └── util/                        # Helpers
```

### 7 条架构规则

1. **控制器应保持简洁**——仅负责验证输入、调用服务并返回数据传输对象（DTO），不包含业务逻辑。
2. **服务应负责业务逻辑**——事务边界应明确界定在服务层。
3. **数据访问对象（Repository）应为接口**——Spring Data 会自动生成实现类。
4. **数据传输对象（DTO）应在接口层进行转换**——切勿在 API 响应中直接暴露 JPA 实体。
5. **仅使用构造函数注入**——避免在字段上使用 `@Autowired` 注解（以保障测试的可读性）。
6. **对于大型应用程序，应按功能进行代码打包**——当服务数量超过 20 个时，应从基于层的架构转向基于功能的架构。
7. **避免循环依赖**——如果 A 依赖于 B，而 B 又依赖于 A，应将共享逻辑提取到单独的组件中。

### Spring Boot 启动器选择

```yaml
# build.gradle.kts (recommended over Maven for Kotlin DSL + type safety)
dependencies:
  # Core
  - spring-boot-starter-web          # REST APIs (embedded Tomcat)
  - spring-boot-starter-webflux      # Reactive APIs (Netty) — choose ONE
  - spring-boot-starter-validation   # Bean Validation (Jakarta)
  
  # Data
  - spring-boot-starter-data-jpa     # JPA + Hibernate
  - spring-boot-starter-data-redis   # Redis caching
  
  # Security
  - spring-boot-starter-security     # Spring Security
  - spring-boot-starter-oauth2-resource-server  # JWT validation
  
  # Observability
  - spring-boot-starter-actuator     # Health, metrics, info
  - micrometer-registry-prometheus   # Prometheus metrics export
  
  # Resilience
  - resilience4j-spring-boot3        # Circuit breaker, retry, rate limit
  
  # Testing
  - spring-boot-starter-test         # JUnit 5 + Mockito + AssertJ
  - spring-boot-testcontainers       # Real DB/Redis in tests
```

### 框架选择：Spring Boot 与其他框架的比较

| 比较项 | Spring Boot | Quarkus | Micronaut | Ktor (Kotlin) |
|--------|------------|---------|-----------|---------------|
| 启动时间 | 2-5 秒 | 0.5-1 秒 | 1-2 秒 | 1-2 秒 |
| 内存占用 | 200-400MB | 50-150MB | 100-200MB | 80-150MB |
| 生态系统支持 | ★★★★★ | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ |
| 企业级应用适用性 | 最受欢迎的选择 | 发展中的框架 | 小众框架 |
| 是否支持原生编译 | 需要 GraalVM（较为复杂） | 支持原生编译（简单） | 支持原生编译（简单） |
| 团队招聘难度 | 易于招聘开发人员 | 较难招聘 | 较难招聘 |

**决策建议**：除非启动时间要求极短（例如服务器less 或命令行接口场景），否则优先选择 Spring Boot；否则可以考虑 Quarkus。

---

## 第 2 阶段：配置与配置文件

### `application.yml` 生产环境模板

```yaml
spring:
  application:
    name: ${APP_NAME:my-service}
  profiles:
    active: ${SPRING_PROFILES_ACTIVE:local}
  
  # Database
  datasource:
    url: ${DATABASE_URL:jdbc:postgresql://localhost:5432/mydb}
    username: ${DATABASE_USERNAME:postgres}
    password: ${DATABASE_PASSWORD:postgres}
    hikari:
      maximum-pool-size: ${DB_POOL_SIZE:10}
      minimum-idle: ${DB_POOL_MIN:5}
      connection-timeout: 3000
      idle-timeout: 600000
      max-lifetime: 1800000
      leak-detection-threshold: 60000
  
  jpa:
    open-in-view: false  # CRITICAL — disable OSIV anti-pattern
    hibernate:
      ddl-auto: validate  # Production: NEVER use update/create
    properties:
      hibernate:
        default_batch_fetch_size: 25
        order_inserts: true
        order_updates: true
        jdbc:
          batch_size: 50
          batch_versioned_data: true
  
  # Jackson
  jackson:
    default-property-inclusion: non_null
    serialization:
      write-dates-as-timestamps: false
    deserialization:
      fail-on-unknown-properties: false
  
  # Cache
  cache:
    type: redis
    redis:
      time-to-live: 3600000  # 1 hour default

server:
  port: ${SERVER_PORT:8080}
  shutdown: graceful  # Wait for active requests
  tomcat:
    max-threads: ${TOMCAT_MAX_THREADS:200}
    accept-count: 100
    connection-timeout: 5000

management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus,metrics
  endpoint:
    health:
      show-details: when-authorized
      probes:
        enabled: true  # Kubernetes liveness/readiness
  metrics:
    tags:
      application: ${spring.application.name}

# Graceful shutdown
spring.lifecycle.timeout-per-shutdown-phase: 30s
```

### 配置文件策略

| 配置文件名 | 用途 | 配置内容 |
|---------|---------|--------|
| `local` | 开发环境 | 使用 H2 数据库和本地 Postgres 数据源，启用调试日志记录 |
| `test` | 测试环境 | 使用测试容器，不依赖外部资源 |
| `staging` | 预生产环境 | 使用真实数据源，减少资源消耗 |
| `production` | 生产环境 | 使用真实数据源，配置完整的功能 |

### 配置规则

1. **切勿硬编码敏感信息**——始终使用环境变量或安全存储库来管理配置。
2. **禁用 `open-in-view` 功能**——防止控制器层中的代码在运行时加载敏感数据（影响性能）。
3. **在生产环境中设置 `ddl-auto: validate` 属性**——使用 Flyway 或 Liquibase 进行数据库迁移。
4. **明确配置 HikariCP 数据源连接池**——默认配置可能不适合生产环境。
5. **启用优雅的服务器关闭机制**——设置 `server.shutdown: graceful` 选项。

---

## 第 3 阶段：JPA 与数据库设计

### 实体设计

```java
@MappedSuperclass
public abstract class BaseEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @CreationTimestamp
    @Column(updatable = false)
    private Instant createdAt;
    
    @UpdateTimestamp
    private Instant updatedAt;
    
    @Version  // Optimistic locking
    private Long version;
}

@Entity
@Table(name = "users", indexes = {
    @Index(name = "idx_users_email", columnList = "email", unique = true),
    @Index(name = "idx_users_status", columnList = "status")
})
public class User extends BaseEntity {
    
    @Column(nullable = false, length = 255)
    private String email;
    
    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private UserStatus status;
    
    @OneToMany(mappedBy = "user", fetch = FetchType.LAZY)  // ALWAYS lazy
    private List<Order> orders = new ArrayList<>();
}
```

### 避免 N+1 问题的方法

```java
// ❌ N+1 problem — loads each user's orders individually
List<User> users = userRepository.findAll();
users.forEach(u -> u.getOrders().size());  // N additional queries

// ✅ JOIN FETCH — single query
@Query("SELECT u FROM User u JOIN FETCH u.orders WHERE u.status = :status")
List<User> findByStatusWithOrders(@Param("status") UserStatus status);

// ✅ EntityGraph — declarative
@EntityGraph(attributePaths = {"orders", "orders.items"})
List<User> findByStatus(UserStatus status);

// ✅ Batch fetching (configured globally)
# application.yml: hibernate.default_batch_fetch_size: 25
```

### 数据访问对象（Repository）的设计模式

```java
public interface UserRepository extends JpaRepository<User, Long> {
    
    // Derived queries — simple cases only
    Optional<User> findByEmail(String email);
    boolean existsByEmail(String email);
    
    // Projections — return only needed fields
    @Query("SELECT new com.example.dto.UserSummary(u.id, u.email, u.status) " +
           "FROM User u WHERE u.status = :status")
    List<UserSummary> findSummariesByStatus(@Param("status") UserStatus status);
    
    // Pagination
    Page<User> findByStatus(UserStatus status, Pageable pageable);
    
    // Bulk operations — bypass Hibernate cache
    @Modifying(clearAutomatically = true)
    @Query("UPDATE User u SET u.status = :status WHERE u.lastLoginAt < :threshold")
    int deactivateInactiveUsers(@Param("status") UserStatus status,
                                @Param("threshold") Instant threshold);
}
```

### 使用 Flyway 进行数据库迁移

```sql
-- V1__create_users_table.sql
CREATE TABLE users (
    id          BIGSERIAL PRIMARY KEY,
    email       VARCHAR(255) NOT NULL,
    status      VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    version     BIGINT NOT NULL DEFAULT 0,
    CONSTRAINT uk_users_email UNIQUE (email)
);

CREATE INDEX idx_users_status ON users(status);
```

### 8 条 JPA 使用规范

1. **始终使用 `FetchType.LAZY`**——避免不必要的数据加载（减少 N+1 问题）。
2. **为乐观锁使用 `@Version` 注解**——防止数据更新丢失。
3. **优先选择投影（projection）而非完整实体**——在只读操作中返回简化后的数据结构。
4. **批量插入/更新数据**——配置 `batch_size` 和 `order_inserts` 参数。
5. **在生产环境中禁用 `ddl-auto: update` 功能**——仅使用 Flyway 或 Liquibase 进行数据库操作。
6. **为业务键使用 `@NaturalId` 注解**——例如使用电子邮件地址或 ISBN 作为唯一标识。
7. **除非必要，否则避免双向关联**——减少代码复杂性和潜在错误。
8. **在实际数据库上进行查询测试**——使用测试容器，而非 H2 伪数据库。

---

## 第 4 阶段：REST API 设计

### 控制器设计模式

```java
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
@Validated
public class UserController {
    
    private final UserService userService;
    private final UserMapper userMapper;
    
    @GetMapping
    public Page<UserResponse> listUsers(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(required = false) UserStatus status) {
        
        Pageable pageable = PageRequest.of(page, size, Sort.by("createdAt").descending());
        return userService.findUsers(status, pageable)
                .map(userMapper::toResponse);
    }
    
    @GetMapping("/{id}")
    public UserResponse getUser(@PathVariable Long id) {
        return userMapper.toResponse(userService.findById(id));
    }
    
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UserResponse createUser(@Valid @RequestBody CreateUserRequest request) {
        User user = userService.create(request);
        return userMapper.toResponse(user);
    }
    
    @PutMapping("/{id}")
    public UserResponse updateUser(@PathVariable Long id,
                                    @Valid @RequestBody UpdateUserRequest request) {
        User user = userService.update(id, request);
        return userMapper.toResponse(user);
    }
    
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteUser(@PathVariable Long id) {
        userService.delete(id);
    }
}
```

### 数据传输对象（DTO）的验证

```java
public record CreateUserRequest(
    @NotBlank @Email @Size(max = 255)
    String email,
    
    @NotBlank @Size(min = 2, max = 100)
    String name,
    
    @NotNull
    UserRole role
) {}

public record UserResponse(
    Long id,
    String email,
    String name,
    UserStatus status,
    Instant createdAt
) {}
```

### 全局错误处理机制

```java
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {
    
    @ExceptionHandler(EntityNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse handleNotFound(EntityNotFoundException ex) {
        return new ErrorResponse("NOT_FOUND", ex.getMessage());
    }
    
    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ErrorResponse handleValidation(MethodArgumentNotValidException ex) {
        Map<String, String> errors = ex.getBindingResult().getFieldErrors().stream()
            .collect(Collectors.toMap(
                FieldError::getField,
                fe -> fe.getDefaultMessage() != null ? fe.getDefaultMessage() : "invalid",
                (a, b) -> a
            ));
        return new ErrorResponse("VALIDATION_ERROR", "Invalid request", errors);
    }
    
    @ExceptionHandler(DataIntegrityViolationException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    public ErrorResponse handleConflict(DataIntegrityViolationException ex) {
        return new ErrorResponse("CONFLICT", "Resource already exists");
    }
    
    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public ErrorResponse handleUnexpected(Exception ex) {
        log.error("Unexpected error", ex);
        return new ErrorResponse("INTERNAL_ERROR", "An unexpected error occurred");
    }
}

public record ErrorResponse(
    String code,
    String message,
    @JsonInclude(JsonInclude.Include.NON_NULL)
    Map<String, String> details
) {
    public ErrorResponse(String code, String message) {
        this(code, message, null);
    }
}
```

---

## 第 5 阶段：安全性

### Spring Security 6 的配置

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
@RequiredArgsConstructor
public class SecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(csrf -> csrf.disable())  // Disable for stateless APIs
            .cors(cors -> cors.configurationSource(corsConfig()))
            .sessionManagement(session -> 
                session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/v1/auth/**").permitAll()
                .requestMatchers("/actuator/health/**").permitAll()
                .requestMatchers("/api/v1/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(jwt -> jwt.jwtAuthenticationConverter(jwtConverter()))
            )
            .exceptionHandling(ex -> ex
                .authenticationEntryPoint((req, res, e) -> {
                    res.setStatus(401);
                    res.getWriter().write("{\"code\":\"UNAUTHORIZED\",\"message\":\"Invalid or missing token\"}");
                })
            )
            .headers(headers -> headers
                .contentSecurityPolicy(csp -> csp.policyDirectives("default-src 'self'"))
                .frameOptions(HeadersConfigurer.FrameOptionsConfig::deny)
            )
            .build();
    }
    
    private CorsConfigurationSource corsConfig() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOrigins(List.of("https://app.example.com"));
        config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE"));
        config.setAllowedHeaders(List.of("Authorization", "Content-Type"));
        config.setMaxAge(3600L);
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/api/**", config);
        return source;
    }
    
    private JwtAuthenticationConverter jwtConverter() {
        JwtGrantedAuthoritiesConverter authorities = new JwtGrantedAuthoritiesConverter();
        authorities.setAuthorityPrefix("ROLE_");
        authorities.setAuthoritiesClaimName("roles");
        JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
        converter.setJwtGrantedAuthoritiesConverter(authorities);
        return converter;
    }
}
```

### 安全性检查清单（10 项）

| 编号 | 检查内容 | 优先级 |
|------|-------|---------|
| 1 | 无状态 API 应禁用 CSRF，会话状态相关的 API 应启用 CSRF | P0 |
| 2 | 配置 CORS 以限制请求来源（生产环境中禁止使用通配符） | P0 |
| 3 | 对 JWT 进行验证，并检查发行者和接收者信息 | P0 |
| 4 | 对所有请求中的数据传输对象进行输入验证 | P0 |
| 5 | 防止 SQL 注入（仅使用参数化查询） | P0 |
| 6 | 敏感信息应存储在环境变量或安全存储库中（切勿直接写在代码中） | P0 |
| 7 | 设置安全头部信息（如 CSP、X-Frame-Options、HSTS） | P1 |
| 8 | 对认证相关接口实施速率限制 | P1 |
| 9 | 定期扫描依赖项的安全漏洞（如 OWASP、Snyk） | P1 |
| 10 | 对敏感操作实施方法级别的权限控制 | P1 |

---

## 第 6 阶段：服务层与业务逻辑

### 服务设计模式

```java
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)  // Default read-only
@Slf4j
public class UserService {
    
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final ApplicationEventPublisher eventPublisher;
    
    public User findById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new EntityNotFoundException("User not found: " + id));
    }
    
    public Page<User> findUsers(UserStatus status, Pageable pageable) {
        if (status != null) {
            return userRepository.findByStatus(status, pageable);
        }
        return userRepository.findAll(pageable);
    }
    
    @Transactional  // Write transaction
    public User create(CreateUserRequest request) {
        if (userRepository.existsByEmail(request.email())) {
            throw new ConflictException("Email already registered: " + request.email());
        }
        
        User user = User.builder()
            .email(request.email())
            .name(request.name())
            .status(UserStatus.ACTIVE)
            .build();
        
        user = userRepository.save(user);
        
        eventPublisher.publishEvent(new UserCreatedEvent(user.getId(), user.getEmail()));
        log.info("User created: id={}, email={}", user.getId(), user.getEmail());
        
        return user;
    }
    
    @Transactional
    @CacheEvict(value = "users", key = "#id")
    public User update(Long id, UpdateUserRequest request) {
        User user = findById(id);
        // Update fields...
        return userRepository.save(user);
    }
}
```

### 领域事件（Domain Events）的设计

```java
public record UserCreatedEvent(Long userId, String email) {}

@Component
@RequiredArgsConstructor
@Slf4j
public class UserEventListener {
    
    private final EmailService emailService;
    
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    @Async
    public void onUserCreated(UserCreatedEvent event) {
        log.info("Sending welcome email to user: {}", event.userId());
        emailService.sendWelcome(event.email());
    }
}
```

---

## 第 7 阶段：缓存

### Redis 缓存配置

```java
@Configuration
@EnableCaching
public class CacheConfig {
    
    @Bean
    public RedisCacheManager cacheManager(RedisConnectionFactory factory) {
        RedisCacheConfiguration defaults = RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofHours(1))
            .serializeValuesWith(
                RedisSerializationContext.SerializationPair.fromSerializer(
                    new GenericJackson2JsonRedisSerializer()
                ))
            .disableCachingNullValues();
        
        Map<String, RedisCacheConfiguration> configs = Map.of(
            "users", defaults.entryTtl(Duration.ofMinutes(30)),
            "products", defaults.entryTtl(Duration.ofHours(2)),
            "config", defaults.entryTtl(Duration.ofHours(24))
        );
        
        return RedisCacheManager.builder(factory)
            .cacheDefaults(defaults)
            .withInitialCacheConfigurations(configs)
            .build();
    }
}
```

### 缓存的使用策略

```java
@Cacheable(value = "users", key = "#id")
public UserResponse getUserById(Long id) { ... }

@CachePut(value = "users", key = "#result.id")
public UserResponse updateUser(Long id, UpdateUserRequest req) { ... }

@CacheEvict(value = "users", key = "#id")
public void deleteUser(Long id) { ... }

@CacheEvict(value = "users", allEntries = true)
@Scheduled(fixedRate = 3600000)  // Hourly full invalidation
public void evictAllUsers() { ... }
```

---

## 第 8 阶段：系统弹性

### Resilience4j 的配置

```yaml
resilience4j:
  circuitbreaker:
    instances:
      payment-service:
        sliding-window-size: 10
        failure-rate-threshold: 50
        wait-duration-in-open-state: 10s
        permitted-number-of-calls-in-half-open-state: 3
        slow-call-duration-threshold: 2s
        slow-call-rate-threshold: 80
  
  retry:
    instances:
      payment-service:
        max-attempts: 3
        wait-duration: 500ms
        exponential-backoff-multiplier: 2
        retry-exceptions:
          - java.io.IOException
          - java.util.concurrent.TimeoutException
        ignore-exceptions:
          - com.example.exception.BusinessException
  
  ratelimiter:
    instances:
      api:
        limit-for-period: 100
        limit-refresh-period: 1s
        timeout-duration: 0s
```

### Resilience4j 的使用方法

```java
@CircuitBreaker(name = "payment-service", fallbackMethod = "paymentFallback")
@Retry(name = "payment-service")
public PaymentResponse processPayment(PaymentRequest request) {
    return paymentClient.charge(request);
}

private PaymentResponse paymentFallback(PaymentRequest request, Throwable t) {
    log.warn("Payment service unavailable, queuing for retry: {}", t.getMessage());
    paymentQueue.enqueue(request);
    return PaymentResponse.pending();
}
```

---

## 第 9 阶段：可观测性

### 结构化的日志记录

```java
// logback-spring.xml
// Use JSON format in production
@Slf4j
public class OrderService {
    
    public Order processOrder(CreateOrderRequest request) {
        try (var mdc = MDC.putCloseable("orderId", request.orderId());
             var userMdc = MDC.putCloseable("userId", request.userId())) {
            
            log.info("Processing order: items={}, total={}", 
                     request.items().size(), request.total());
            // All logs within this scope include orderId + userId
        }
    }
}
```

### 使用 Micrometer 收集指标数据

```java
@Component
@RequiredArgsConstructor
public class OrderMetrics {
    
    private final MeterRegistry registry;
    
    public void recordOrderProcessed(String status, Duration duration) {
        registry.counter("orders.processed", "status", status).increment();
        registry.timer("orders.processing.time", "status", status)
                .record(duration);
    }
    
    public void recordActiveOrders(int count) {
        registry.gauge("orders.active", count);
    }
}
```

### 健康检查指标的实现

```java
@Component
public class PaymentServiceHealthIndicator implements HealthIndicator {
    
    private final PaymentClient paymentClient;
    
    @Override
    public Health health() {
        try {
            paymentClient.ping();
            return Health.up().withDetail("latency", "ok").build();
        } catch (Exception e) {
            return Health.down().withException(e).build();
        }
    }
}
```

---

## 第 10 阶段：测试

### 测试策略

| 测试类型 | 测试内容 | 使用工具 | 目标覆盖范围 |
|---------|--------|-------|----------------|
| 单元测试 | 服务层、映射器、辅助类 | JUnit 5 + Mockito | 80% 的代码覆盖率 |
| 切片测试 | 控制器、数据访问对象 | @WebMvcTest、@DataJpaTest | 关键业务路径 |
| 集成测试 | 使用真实数据库的完整业务流程 | @SpringBootTest + 测试容器 | 确保所有功能正常运行且无错误 |
| 接口契约测试 | API 接口 | Spring Cloud Contract / Pact | 所有 API 端点 |

### 单元测试模式

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    
    @Mock UserRepository userRepository;
    @Mock ApplicationEventPublisher eventPublisher;
    @InjectMocks UserService userService;
    
    @Test
    void create_validRequest_savesAndPublishesEvent() {
        var request = new CreateUserRequest("test@example.com", "Test User", UserRole.USER);
        var savedUser = User.builder().id(1L).email(request.email()).build();
        
        when(userRepository.existsByEmail(request.email())).thenReturn(false);
        when(userRepository.save(any(User.class))).thenReturn(savedUser);
        
        User result = userService.create(request);
        
        assertThat(result.getId()).isEqualTo(1L);
        verify(eventPublisher).publishEvent(any(UserCreatedEvent.class));
    }
    
    @Test
    void create_duplicateEmail_throwsConflict() {
        var request = new CreateUserRequest("existing@example.com", "Test", UserRole.USER);
        when(userRepository.existsByEmail(request.email())).thenReturn(true);
        
        assertThatThrownBy(() -> userService.create(request))
            .isInstanceOf(ConflictException.class)
            .hasMessageContaining("already registered");
    }
}
```

### 控制器的切片测试

```java
@WebMvcTest(UserController.class)
@Import(SecurityConfig.class)
class UserControllerTest {
    
    @Autowired MockMvc mockMvc;
    @MockBean UserService userService;
    @MockBean UserMapper userMapper;
    
    @Test
    @WithMockUser(roles = "USER")
    void getUser_exists_returns200() throws Exception {
        var user = User.builder().id(1L).email("test@test.com").build();
        var response = new UserResponse(1L, "test@test.com", "Test", UserStatus.ACTIVE, Instant.now());
        
        when(userService.findById(1L)).thenReturn(user);
        when(userMapper.toResponse(user)).thenReturn(response);
        
        mockMvc.perform(get("/api/v1/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.email").value("test@test.com"));
    }
}
```

### 使用测试容器进行集成测试

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Testcontainers
class UserIntegrationTest {
    
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine");
    
    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }
    
    @Autowired TestRestTemplate restTemplate;
    
    @Test
    void fullUserLifecycle() {
        // Create
        var createReq = new CreateUserRequest("int@test.com", "Integration", UserRole.USER);
        var created = restTemplate.postForEntity("/api/v1/users", createReq, UserResponse.class);
        assertThat(created.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        
        // Read
        var fetched = restTemplate.getForEntity(
            "/api/v1/users/" + created.getBody().id(), UserResponse.class);
        assertThat(fetched.getBody().email()).isEqualTo("int@test.com");
    }
}
```

### 7 条集成测试规则

1. **使用构造函数注入进行测试**——避免反射相关的测试技巧。
2. **控制器测试使用 `@WebMvcTest` | 仅加载与 Web 层相关的代码。
3. **数据访问对象测试使用 `@DataJpaTest` | 自动配置 JPA 模型并支持回滚操作。
4. **集成测试使用测试容器**——使用真实的 Postgres/Redis 数据库，而非 H2 伪数据库。
5. **安全相关测试需使用 `@WithMockUser` 或 `@WithAnonymousUser` | 模拟用户行为。
6. **验证输入数据的有效性**——确保 `@Valid` 注解能正确处理无效输入。
7. **不要测试框架代码**——重点测试业务逻辑。

---

## 第 11 阶段：性能优化

### 性能优化优先级

| 优化措施 | 影响程度 | 实施难度 |
|---------|-----------|--------|--------|
| 1 | 修复导致 N+1 问题的查询（如 JOIN 或实体图相关操作） | ★★★★★ | 低难度 |
| 2 | 为频繁访问的列添加数据库索引 | ★★★★★ | 低难度 |
| 3 | 调优 HikariCP 数据源连接池 | ★★★★☆ | 低难度 |
| 4 | 对读取密集型数据使用 Redis 缓存 | ★★★★☆ | 中等难度 |
| 5 | 使用数据传输对象（DTO）代替完整实体 | ★★★★☆ | 中等难度 |
| 6 | 对非关键任务启用异步处理 | ★★★☆☆ | 中等难度 |
| 7 | 对 I/O 密集型任务使用 Java 21 及更高版本的虚拟线程 | ★★★☆☆ | 低难度 |
| 8 | 使用 GraalVM 进行原生编译以提升启动速度 | ★★★☆☆ | 高难度 |

### Java 21 及更高版本的虚拟线程

```yaml
# application.yml — enable virtual threads
spring:
  threads:
    virtual:
      enabled: true  # Tomcat uses virtual threads for requests
```

### 异步处理技术的应用

```java
@Configuration
@EnableAsync
public class AsyncConfig {
    
    @Bean
    public TaskExecutor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(20);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("async-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        return executor;
    }
}

@Async
public CompletableFuture<Report> generateReport(Long userId) {
    // Runs on thread pool, doesn't block request thread
    Report report = reportGenerator.generate(userId);
    return CompletableFuture.completedFuture(report);
}
```

---

## 第 12 阶段：部署

### 多阶段的 Dockerfile 编写

```dockerfile
# Build
FROM eclipse-temurin:21-jdk-alpine AS build
WORKDIR /app
COPY gradle/ gradle/
COPY gradlew build.gradle.kts settings.gradle.kts ./
RUN ./gradlew dependencies --no-daemon  # Cache deps
COPY src/ src/
RUN ./gradlew bootJar --no-daemon -x test

# Runtime
FROM eclipse-temurin:21-jre-alpine
RUN addgroup -S app && adduser -S app -G app
WORKDIR /app
COPY --from=build /app/build/libs/*.jar app.jar
USER app
EXPOSE 8080

# JVM tuning for containers
ENV JAVA_OPTS="-XX:+UseContainerSupport \
  -XX:MaxRAMPercentage=75.0 \
  -XX:InitialRAMPercentage=50.0 \
  -XX:+UseG1GC \
  -XX:+ExitOnOutOfMemoryError \
  -Djava.security.egd=file:/dev/./urandom"

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
```

### 使用 GitHub Actions 实现持续集成与持续部署（CI/CD）

```yaml
name: CI/CD
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        ports: ['5432:5432']
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: 21
          cache: gradle
      
      - name: Build & Test
        run: ./gradlew build
        env:
          DATABASE_URL: jdbc:postgresql://localhost:5432/testdb
          DATABASE_USERNAME: test
          DATABASE_PASSWORD: test
      
      - name: Build Docker Image
        if: github.ref == 'refs/heads/main'
        run: |
          docker build -t ${{ secrets.REGISTRY }}/app:${{ github.sha }} .
          docker push ${{ secrets.REGISTRY }}/app:${{ github.sha }}
```

### 生产环境准备检查清单

**必填项：**
- 禁用 `open-in-view` 功能
- 配置 `ddl-auto: validate` 以及 Flyway/Liquibase 迁移工具
- 启用 HikariCP 连接池的泄漏检测功能
- 启用优雅的服务器关闭机制
- 暴露健康检查端点和可用性检查接口
- 对所有请求中的输入数据进行验证
- 配置适当的安全措施（认证、CORS、安全头部信息）
- 使用结构化的 JSON 格式记录日志
- 导出 Prometheus 指标数据

**建议在 30 天内完成：**
- 为外部请求配置断路器
- 为热点数据路径启用 Redis 缓存
- 启用 Java 21 及更高版本的虚拟线程
- 设置容器资源限制
- 定期扫描依赖项的安全漏洞

---

## 第 13 阶段：Kotlin 特有的最佳实践（如果使用 Kotlin）

如果使用 Kotlin 作为开发语言：

```kotlin
// Coroutines + WebFlux
@RestController
@RequestMapping("/api/v1/users")
class UserController(private val userService: UserService) {
    
    @GetMapping("/{id}")
    suspend fun getUser(@PathVariable id: Long): UserResponse =
        userService.findById(id).toResponse()
    
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    suspend fun createUser(@Valid @RequestBody request: CreateUserRequest): UserResponse =
        userService.create(request).toResponse()
}

// Data classes as DTOs (no Lombok needed)
data class CreateUserRequest(
    @field:NotBlank @field:Email
    val email: String,
    @field:NotBlank @field:Size(min = 2, max = 100)
    val name: String,
)

// Extension functions for mapping
fun User.toResponse() = UserResponse(
    id = id,
    email = email,
    name = name,
    status = status,
    createdAt = createdAt,
)
```

**Kotlin 的优势**：支持空值安全、提供数据类（无需 Lombok）、支持异步操作（通过协程实现）、提供扩展函数以简化数据映射、以及使用密封类来管理错误类型。

---

## 第 14 阶段：高级开发技巧

### 定时任务的实现

```java
@Component
@RequiredArgsConstructor
@Slf4j
public class CleanupJob {
    
    private final UserRepository userRepository;
    
    @Scheduled(cron = "0 0 2 * * *")  // 2 AM daily
    @SchedulerLock(name = "cleanup", lockAtMostFor = "30m")  // ShedLock for distributed
    public void cleanupInactiveUsers() {
        int count = userRepository.deactivateInactiveUsers(
            UserStatus.INACTIVE,
            Instant.now().minus(90, ChronoUnit.DAYS)
        );
        log.info("Deactivated {} inactive users", count);
    }
}
```

### Kafka 的集成

```java
@Component
@RequiredArgsConstructor
public class OrderEventProducer {
    
    private final KafkaTemplate<String, OrderEvent> kafkaTemplate;
    
    public void publishOrderCreated(Order order) {
        var event = new OrderEvent("ORDER_CREATED", order.getId(), Instant.now());
        kafkaTemplate.send("orders", order.getId().toString(), event);
    }
}

@Component
@KafkaListener(topics = "orders", groupId = "notification-service")
public class OrderEventConsumer {
    
    @KafkaHandler
    public void handleOrderEvent(OrderEvent event) {
        // Process event with idempotency check
    }
}
```

### 多租户架构的实现

```java
@Component
public class TenantFilter extends OncePerRequestFilter {
    
    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                     HttpServletResponse response,
                                     FilterChain chain) throws ServletException, IOException {
        String tenantId = request.getHeader("X-Tenant-ID");
        if (tenantId != null) {
            TenantContext.setTenantId(tenantId);
        }
        try {
            chain.doFilter(request, response);
        } finally {
            TenantContext.clear();
        }
    }
}
```

---

## 常见错误与解决方法

| 错误类型 | 解决方法 |
|---------|---------|
| 1 | 默认启用 `open-in-view` 功能 | 应将其设置为 `false` | 避免在事务之外加载敏感数据 |
| 2 | 在生产环境中使用 `ddl-auto: update` | 应使用 Flyway 或 Liquibase 进行数据库迁移 | 确保迁移过程可预测且可逆 |
| 3 | 在代码中使用字段注入（`@Autowired`） | 应使用构造函数注入 | 便于测试并明确依赖关系 |
| 4 | 控制器直接返回 JPA 实体 | 应使用数据传输对象（DTO） | 避免不必要的数据加载和数据泄露 |
| 5 | 未配置 HikariCP | 应调整连接池大小、设置超时参数并启用泄漏检测 |
| 6 | 在代码中到处捕获异常 | 应使用特定的异常处理机制并进行全局异常处理 |
| 7 | 列表接口未提供分页功能 | 应始终使用分页机制（`Pageable` 参数） |
| 8 | 在响应中混合使用阻塞式操作和异步操作 | 应避免在响应中混合使用阻塞式数据库操作和异步处理 |
| 9 | 未为读取操作配置 `@Transactional(readOnly=true)` | 应配置该属性以优化读取性能 |
| 10 | 使用 H2 伪数据库进行测试 | 应使用测试容器进行真实数据库的测试 |

---

## 质量评估标准（0-100 分）

| 评估维度 | 权重 | 评估标准 |
|---------|--------|----------|
| 架构设计 | 15% | 清晰的代码层次结构、依赖注入、避免循环依赖 |
| 数据访问 | 15% | 避免 N+1 问题、使用索引、合理管理数据库迁移 |
| 安全性 | 15% | 有效的认证机制、输入验证、正确的安全配置 |
| 测试 | 15% | 全面的测试覆盖、使用测试容器、切片测试 |
| API 设计 | 10% | 一致的错误处理方式、提供分页功能、完整的 API 文档 |
| 可观测性 | 10% | 结构化的日志记录、指标收集、健康检查机制 |
| 系统弹性 | 10% | 配置断路器、重试机制、优雅的关闭流程 |
| 部署 | 10% | 使用容器化技术、实现持续集成与持续部署 |

## Spring Boot 生产环境的 10 条黄金法则

1. **首先禁用 `open-in-view` 功能**——这是每个项目的首要任务。
2. **始终使用构造函数注入**——为所有依赖项使用 `@RequiredArgsConstructor` 注解。
3. **所有数据传输对象（DTO）都应在接口层进行转换**——控制器不应直接操作 JPA 实体。
4. **默认情况下，读取操作应配置为 `@Transactional(readOnly=true)` | 只在需要写入操作时才启用事务。
5. **优先使用测试容器进行测试**——而非 H2 伪数据库。
6. **使用 Flyway 进行数据库迁移**——避免使用 `ddl-auto: update` 功能。
7. **对所有输入数据进行验证**——使用 `@Valid` 注解进行验证。
8. **规范日志记录格式**——在生产环境中使用 JSON 格式，使用 MDC 标记日志上下文。
9. **优化 HikariCP 连接池配置**——连接池大小 = （核心线程数 × 2）+ 额外线程数。
10. **启用优雅的服务器关闭机制**——设置 `server.shutdown: graceful` 选项。

---

## 常用命令

在处理 Spring Boot 项目时，您可以执行以下操作：

1. `review my Spring Boot app` —— 全面检查项目架构和配置。
2. `check my JPA entities` —— 检查数据访问对象的实现、索引配置以及映射关系。
3. `review my security config` —— 审查安全配置，确保认证、CORS 设置正确，无安全漏洞。
4. `optimize my queries` —— 检查是否存在 N+1 问题以及是否可以优化数据访问方式。
5. `set up Testcontainers` —— 配置测试环境。
6. `add caching` —— 设置 Redis 缓存并配置缓存策略。
7. `add circuit breaker` —— 配置 Resilience4j 以提升系统弹性。
8. `Dockerize my app` —— 编写多阶段的 Dockerfile 并配置持续集成与持续部署。
9. `add observability` —— 配置 Actuator、Prometheus 和结构化日志记录。
10. `review my tests` —— 检查测试覆盖率，查找缺失的切片测试。

---

## 提升您的 Spring Boot 技能

本文档涵盖了生产环境下的最佳实践。如需针对特定行业场景（如 SaaS、金融技术或医疗保健领域）的进阶内容，可参考以下额外资源：

- **[SaaS 场景包（47 美元）**：SaaS 相关的 billing、多租户管理、订阅管理等功能。
- **[金融技术场景包（47 美元）**：支付处理、合规性要求、金融数据相关的技术最佳实践。
- **[医疗保健场景包（47 美元）**：HIPAA 合规性、HL7/FHIR 标准、审计日志记录等。

## 更多免费学习资源

- `afrexai-python-production`：Python 生产环境开发指南。
- `afrexai-api-architecture`：API 设计与架构相关内容。
- `afrexai-database-engineering`：数据库优化与扩展技巧。
- `afrexai-test-automation-engineering`：自动化测试策略与工具。
- `afrexai-cicd-engineering`：持续集成与持续部署流程。

更多资源请访问：[AfrexAI 在 ClawHub 上的文档库](https://clawhub.com) | [Context Packs 商店](https://afrexai-cto.github.io/context-packs/)