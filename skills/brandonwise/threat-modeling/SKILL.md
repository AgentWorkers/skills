# 威胁建模专家

擅长使用STRIDE、PASTA、攻击树和安全需求提取等方法进行威胁建模、安全架构审查和风险评估。

## 适用场景

- 在设计新系统或新功能时（确保系统从设计阶段就具备安全性）
- 审查架构中的安全漏洞
- 为安全审计做准备
- 识别攻击途径和威胁来源
- 确定安全投资的优先级
- 制定安全文档
- 对团队进行安全思维培训

## 不适用场景

- 缺乏进行安全审查的权限或范围
- 需要法律合规性认证（请咨询法律专家）
- 仅需要自动化扫描（使用漏洞扫描工具）

---

## 核心流程

### 1. 明确范围
- 确定系统边界
- 需要保护的资产
- 信任边界
- 相关的法规要求

### 2. 创建数据流图
```
[User] → [Web App] → [API Gateway] → [Backend] → [Database]
                ↓
          [External API]
```

### 3. 识别资产和入口点
- **资产**：用户数据、凭证、业务逻辑、基础设施
- **入口点**：API接口、表单、文件上传功能、管理员面板

### 4. 应用STRIDE方法
- **S**（Spoofing，欺骗）：他人能否冒充用户？
- **T**（Tampering，篡改）：数据能否被修改？
- **R**（Repudiation，否认）：操作能否被拒绝？
- **I**（Information Disclosure，信息泄露）：数据能否被泄露？
- **D**（Denial of Service，服务拒绝）：系统的可用性能否被影响？
- **E**（Elevation of Privilege，权限提升）：用户的权限能否被提升？

### 5. 构建攻击树
```
Goal: Access Admin Panel
├── Steal admin credentials
│   ├── Phishing
│   ├── Brute force
│   └── Session hijacking
├── Exploit vulnerability
│   ├── SQL injection
│   └── Auth bypass
└── Social engineering
    └── Support desk compromise
```

### 6. 评估和排序风险
使用DREAD或CVSS评分标准：
- **D**（Damage，损害潜力）
- **R**（Reproducibility，可重现性）
- **E**（Exploitability，易攻击性）
- **A**（Affected Users，受影响用户数量）
- **D**（Discoverability，可发现性）

### 7. 设计缓解措施
将威胁与相应的安全控制措施对应起来，并验证这些措施的有效性。

### 8. 记录剩余风险
明确哪些风险已被接受，哪些风险已得到缓解。

---

## STRIDE分析模板

| 组件 | 欺骗（Spoofing） | 篡改（Tampering） | 否认（Repudiation） | 信息泄露（Information Disclosure） | 服务拒绝（DoS） | 权限提升（Elevation of Privilege） |
|---------|------------|------------------|------------------|------------------|-------------------|
| Web应用 | 身份验证绕过（Auth bypass） | XSS、CSRF攻击 | 日志缺失（Missing logs） | 错误信息（Error messages） | 流量限制（Rate limit） | 访问权限异常（Broken access） |
| API接口 | 令牌盗用（Token theft） | 输入数据篡改（Input manipulation） | 无审计机制（No audit） | 数据泄露（Data exposure） | 资源耗尽（Resource exhaustion） | 权限提升（Privilege escalation） |
| 数据库 | 凭证盗用（Credential theft） | SQL注入（SQL injection） | 无审计记录（No audit trail） | 备份泄露（Backup exposure） | 连接攻击（Connection flood） | 直接访问（Direct access） |

---

## 按层次划分的威胁类别

### 应用层
- 注入攻击（SQL注入、XSS、命令注入）
- 身份验证漏洞
- 敏感数据泄露
- 访问控制漏洞
- 安全配置错误
- 使用了易受攻击的组件

### 网络层
- 中间人攻击（Man-in-the-middle）
- 窃听（Eavesdropping）
- 重放攻击（Replay attacks）
- DNS欺骗（DNS spoofing）
- DDoS攻击（DDoS）

### 基础设施层
- 未经授权的访问
- 服务配置错误
- 未打补丁的系统
- 弱密码
- 暴露的管理员接口

### 人为因素
- 钓鱼攻击（Phishing）
- 社会工程学攻击（Social engineering）
- 内部威胁（Insider threats）
- 凭证共享（Credential sharing）

---

## 数据流图元素

| 元素 | 符号 | 说明 |
|---------|--------|-------------|
| 外部实体 | 矩形 | 用户、外部系统 |
| 过程 | 圆形 | 应用逻辑 |
| 数据存储 | 平行线 | 数据库、缓存、文件 |
| 数据流 | 箭头 | 数据传输方向 |
| 信任边界 | 虚线 | 安全边界 |

---

## 风险优先级矩阵

```
              LOW IMPACT    HIGH IMPACT
HIGH LIKELIHOOD   MEDIUM        HIGH
LOW LIKELIHOOD    LOW           MEDIUM
```

### DREAD评分（每个因素1-10分）

| 因素 | 评估问题 |
|--------|----------|
| 损害潜力（Damage） | 被利用后的后果有多严重？ |
| 可重现性（Reproducibility） | 攻击是否容易重现？ |
| 易攻击性（Exploitability） | 攻击的难易程度？ |
| 受影响用户数量（Affected Users） | 有多少用户会受到影响？ |
| 可发现性（Discoverability） | 攻击是否容易被发现？ |

**风险等级 = 各因素得分之和 / 5**

---

## 缓解策略

### 输入验证
- 使用白名单进行验证
- 使用参数化查询
- 对输出数据进行编码
- 强制指定内容类型（Content-Type enforcement）

### 身份验证
- 在可能的情况下使用多因素认证（MFA）
- 实施强密码策略
- 实施账户锁定机制
- 管理会话安全（Secure session management）

### 授权控制
- 原则最小权限（Principle of least privilege）
- 基于角色的访问控制（Role-based access control）
- 检查资源所有权
- 定期进行权限审计

### 加密技术
- 在所有通信中使用TLS 1.2及以上协议
- 实施强密钥管理
- 对存储的数据进行加密
- 对传输的数据进行加密

### 监控机制
- 记录安全事件
- 发现异常行为
- 设置警报阈值
- 制定事件响应计划

---

## 最佳实践

1. **让开发人员参与威胁建模过程**
2. **关注数据流**，而不仅仅是单个组件
3. **考虑内部威胁**的可能性
4. **随着架构变更及时更新威胁模型**
5. **将威胁与安全需求关联起来**
6. **跟踪缓解措施的实施情况**
7. **定期审查模型**，而不仅仅是在设计阶段
8. **保持威胁模型的实时更新**

---

## 输出模板
```markdown
# Threat Model: [System Name]

## Scope
- Components in scope
- Out of scope

## Assets
- Critical assets list

## Trust Boundaries
- Internal vs external
- Admin vs user

## Data Flow Diagram
[DFD here]

## STRIDE Analysis
[Table here]

## Prioritized Threats
1. [High] Description - Mitigation
2. [Medium] Description - Mitigation

## Residual Risks
- Accepted risks with justification

## Review Schedule
- Next review date
```