---
name: CAN
version: 1.6.1
description: "**代理的命名与路由机制（v1.6.1）：基于递归作用域的信任网络（Web of Trust）**  
信任并非被明确声明，而是通过一系列安全验证过程逐渐积累的；每一个经过验证的信息都构成了信任的证据。每个代理的身份（WHO）都代表着其声誉；每个作用域（scope）都定义了信任的边界。CAN（可能是某个特定的系统或协议）可以通过名称来表达信任关系——这些名称可以基于时间、哈希值或发起请求的代理来进行分类。"
homepage: https://github.com/xccx/can
metadata: {"openclaw":{"emoji":"⌛","requires":{"bins":["sha256sum","openssl","base64","awk","date"]}}}
---
# CAN：时钟地址命名机制（Clock Address Naming）

## WOT（Web of Trust）：信任网络（Web of Trust）

### 为什么要信任？（Why trust?）

因为现有的“WHERE”（定位机制）已经失效，而且这一点大家都心知肚明。

### 在“原子级”（atoms）中命名“WHERE”的代价（The cost of naming WHERE at the atomic level）

每一行数据都代表一个由“原子级”因素定义的“WHERE”定位：物理位置、机构权限、容器层级结构等。一旦这些因素发生变化，对应的定位信息就会失效。同时，用户必须信任那些自己并未选择且无法验证的中间节点。

这并非理论上的问题——实际上，这涉及到成千上万的工程师在维护着大量的重定向表；“404 Not Found”错误正是互联网上最常见的现象。证书固定（certificate pinning）、DNSSEC安全协议、BGP路由劫持（DNSSEC hijacking）、域名抢注（domain squatting）、链接失效（link rot）、云服务锁定（cloud lock-in）等问题，都是由于在“原子级”而非“逻辑级”（logical level）上命名“WHERE”所导致的。

### 无所作为的代价（The cost of inaction）

所有这些问题都是由于错误的命名方式造成的。

### CAN中的信任机制（Trust in CAN）

在CAN系统中，信任并非预先声明的，而是通过一系列经过验证的记录（SAWs: Verified Sightings）逐渐积累起来的。你信任某个代理，并非因为别人告诉你可以信任它，而是因为：

- 该代理的行为符合既定的规则；
- 其行为有据可查（可验证）；
- 其信任程度会随时间变化；
- 信任程度并非非黑即白的二进制状态，而是一个基于证据的动态梯度。

### 范围（Scope）的概念（The concept of Scope）

所有范围都遵循相同的模式：
- 每个范围都有成员（WHO: Participants）；
- 每个范围都有一个索引（SAW: Verified Sightings）；
- 每个范围都有信任边界（who can join, who can see）；
- 每个范围都支持相同的操作（stamp, verify, find, route, saw, cant）。

不同范围之间的唯一区别在于规模和策略：
- `SELF`范围是私有的；
- `PAIR`范围包含两个成员；
- `GROUP`范围包含多个成员；
- `REGION`范围则覆盖所有成员；
- 在每一层，使用的都是相同的CAN机制。

### CAN中的WOT（Web of Trust）

### 注册（Enrollment）

代理要加入某个范围，需要得到其他代理的担保（vouch）。担保本身也是一种SAW记录：
- 被担保的代理的“WHERE”就是其身份；
- 担保的方式（HOW）是将其加入指定的范围；
- 担保的理由（WHY）是“需要建立新的信任关系”；
- 担保者（WHO）就是担保者本身。

### 信任的权重（Trust weight）

任何范围内的代理的信任权重都是可计算的、可审计的，并且会随时间变化。这种权重并非由任何权威机构分配的，而是通过证据逐步积累起来的。

### 范围的信任边界（Scope boundaries）

谁可以加入某个范围？这由该范围的策略决定：
- `OPEN`范围：任何代理都可以加入，只需记录一个SAW即可；
- `VOUCHED`范围：现有成员必须为新成员提供担保；
- `KEYED`范围：需要提供身份的加密证明；
- `BUMPED`范围：要求代理之间有物理上的共存（v2.0版本要求）。

不同的范围有不同的信任策略：
- 家庭范围可能采用`BUMPED`策略；
- 公共中继节点可能采用`OPEN`策略；
- 公司范围可能采用`KEYED`策略。

### 信任在范围之间的传递（Trust flows through scopes）

代理A信任代理B（基于直接的SAW记录）；代理B信任代理C（同样基于直接的SAW记录）。即使代理A从未见过代理C，也可以通过信任路径来推断它们之间的信任关系。

### WOT的优势（Advantages of WOT）

- **无需信任权威或证书链**；
- **代理无需默认信任任何人**；
- **不会泄露私密范围的成员信息**；
- **信任程度可以有所不同**；
- **私密信息仍然保持私密**；
- **无需新的索引格式**；
- **使用CAN时无需代理参与特定的信任流程**。

### 共享与网络安全性（Sharing and network security）

CAN系统不会自动共享索引条目；所有数据共享都需要代理的明确操作（例如通过POST请求）。系统没有后台广播机制，也没有持续运行的监听程序。代理只有在自己愿意的情况下才会选择共享数据。

在跨范围共享索引条目时：
- 需要删除或对路径（PATH）字段进行加密处理；
- 必须遵守“HUSH”规则（规则5）：私密信息永远不会离开当前范围；
- 范围边界决定了谁可以查看哪些数据；
- 索引包含敏感信息（文件名、时间戳、代理标识符），因此默认应视为私密数据。

### 注意事项（Notes）

- 完整的规范文档请访问：https://github.com/xccx/can

### 输入安全（Input safety）

在CAN系统中，所有用于操作的变量在用于shell命令之前都必须进行安全处理（sanitization）。切勿直接将网络接收到的数据传递给echo、awk等工具。

### 验证规则（Validation rules）

本文档中的bash示例仅用于说明目的，并非可执行代码。实现CAN系统的代理应使用平台提供的安全字符串处理机制，避免直接使用未经验证的输入数据。在将数据写入索引或执行任何操作之前，必须对所有字段进行验证；如果验证失败，应拒绝数据并记录错误日志。

### 协议扩展（Protocol additions）

- **代理间通信协议**（agent-to-agent protocol）：新增规则（v1.5版本仍然适用）：
  16. 所有范围都有名称，且名称都是可哈希处理的；
  17. 注册过程需要提供“WHY=WOT”的理由；
  18. 信任权重基于SAW记录计算，而非预先声明；
  19. 信任是单向的（信任B并不意味着B也信任A）；
  20. 一个范围可以包含其他范围；
  21. 范围的策略（OPEN/VOUCHED/KEYED/BUMPED）由创建者设定，成员可以通过共识进行修改；
  22. 在跨范围共享索引条目时，需要删除或加密路径字段；
  23. 共享行为完全由代理自主决定，没有后台同步或守护进程。

### CAN的递归特性（Recursive CAN）

- v1.5版本：让代理学会构建网络的同时，也学会了如何成为网络中的一个节点；
- v1.6版本：让代理学会信任他人，同时也明确了信任在网络中的边界——范围内部存在信任关系，CAN系统本身也遵循这种信任机制。

### 制定路线图（Roadmap）

每个新版本都会基于前一个版本进行改进和发展。

### 参考文献（References）

- Paul Baran，《分布式通信》（On Distributed Communications, RAND, 1964）
- Phil Zimmermann，《Pretty Good Privacy》（PGP, 1991）
- Van Jacobson，《网络的新视角》（A New Way to Look at Networking, Google Tech Talk, 2006）
- John Day，《递归互联网架构》（Recursive InterNetwork Architecture, RINA）
- Linus Torvalds，《Git内容寻址对象存储》（Git content-addressable object store）
- Zooko的三角模型（Zooko’s Triangle，用于说明CAN的扩展性）

### 总结（TL;DR）

CAN系统通过一种基于证据的信任机制，解决了现有网络架构中的诸多问题，提供了更加安全、灵活和可扩展的网络解决方案。