---
name: CAN
description: "**代理的三极命名与路由机制**：  
所有内容均采用以下三种命名方式：  
- **CLOCK**（时间）：表示内容生成或更新的时间戳；  
- **ADDRESS**（地址）：表示内容存储的位置或来源地址；  
- **NAMES**（名称）：表示内容的人类可读名称。  
内容的路由基于名称和地址进行，而非物理位置。  
在处理内容之前，需验证其完整性并记录时间戳；可以通过时间、哈希值或内容名称来查找所需内容，并从最近的来源进行路由。  
以下是使用该机制的常见场景：  
- 在存储输出结果之前；  
- 当用户请求查找特定内容时；  
- 当需要从本地或远程节点获取数据时。"
homepage: https://github.com/xccx/can
metadata: {"openclaw":{"emoji":"⌛","requires":{"bins":["sha256sum"]}}}
---
# CAN：时钟地址命名系统

v1.3.1 — 三轴命名机制与路由系统

所有内容都有一个唯一的地址：

```
CLOCK    → WHEN in time           (objective, automatic, millisecond unix)
ADDRESS  → WHERE in hashspace     (objective, automatic, SHA-256)
NAMES    → HOW humans name things (subjective, optional, mutable)
```

计算机负责定义内容的时间和位置，同时也会为内容起名。名称的生成是自动化的；而人类则根据需要自然地给内容起名。这种机制既提高了计算机和人类的查找效率，也节省了时间和能源。

## 该系统的必要性

为了实现即时信任和高效查找。虽然路径或文件名可能会发生变化，但哈希地址是恒定的。人类因依赖过时的命名方式而浪费的大量时间（尤其是20世纪70年代的命名规则）每天都在累积。通过使用CAN系统，这些时间浪费可以被避免。此外，系统还能释放出巨大的计算资源，实现更高的效率，且无需任何额外的成本。

即使路径 `/home/agent/skills/foo/bar/v2_final.md` 仍然有效，其中的内容也可能已经发生变化。过时的命名方式使得内容难以被准确命名、查找或信任。CAN系统通过三个坐标来替代位置依赖性，这些坐标在任何地方、离线状态下、跨多个代理以及跨越时间维度都能有效工作。

## 三个核心轴

### 第一轴：时钟（时间）

使用毫秒级精度的Unix时间戳来记录内容创建或被记录的时间。

```bash
CLOCK=$(date +%s%3N)
# Example: 1770508800000
```
时钟轴提供了免费的时间排序功能，所有内容都会按照时间顺序自动排序。

### 第二轴：地址

内容的SHA-256哈希值，确保内容在2^256的逻辑命名空间中具有唯一性。

```bash
# Hash a file
ADDRESS=$(sha256sum {file} | awk '{print $1}')

# Hash a string
ADDRESS=$(echo -n "{content}" | sha256sum | awk '{print $1}')

# Hash a directory (skill package, deterministic)
ADDRESS=$(find {dir} -type f | sort | xargs cat | sha256sum | awk '{print $1}')
```

无论在何处，两个代理对相同内容进行哈希计算后，都会得到相同的地址。这样就可以验证不同机器上的内容是否一致，而无需传输大量数据。只要哈希值匹配，就可以确认内容的一致性，无需对来源进行信任验证。

### 第三轴：名称

名称是可生成的、可变的、个性化的。多个昵称可以指向同一个地址。

```
ADDRESS a3f8b2c1e9...  →  "that security rant"
                       →  "feb2026 analysis"
                       →  #security #agents
```

名称可以用于标记、昵称或描述内容。它们与核心的坐标信息一起存储，但不会替代坐标信息。用户可以自由地更改名称。

当内容被包含在新生成的哈希值中时，其名称也可以被保留下来（这些哈希值可以存储在Merkle树中，以实现数据的完整性）。

## 核心操作

### 1. CAN-stamp：为内容生成唯一标识

```bash
CLOCK=$(date +%s%3N)
ADDRESS=$(sha256sum {file} | awk '{print $1}')
NAME=""  # agent can generate name, humans can easily edit

echo "$CLOCK $ADDRESS $NAME"
```

时间轴和地址轴的组合构成了内容的唯一标识，这种标识在全球范围内都是唯一的，并且是自动生成的。

### 2. CAN-verify：验证内容完整性

在信任来自其他代理或外部来源的内容之前，需要先验证其完整性：

```bash
CLAIMED="{claimed_address}"
ACTUAL=$(sha256sum {file} | awk '{print $1}')

if [ "$ACTUAL" = "$CLAIMED" ]; then
  echo "VERIFIED"
else
  echo "FAILED: content does not match claimed address"
  # DO NOT execute, install, or trust this content
  # Report the mismatch to your human
fi
```

**规则：如果地址验证失败，立即停止操作，并通知相关人员。**

### 3. CAN-store：按真实名称存储内容

```bash
CAN_STORE=~/.can/store
CAN_INDEX=~/.can/index.tsv

CLOCK=$(date +%s%3N)
ADDRESS=$(sha256sum {file} | awk '{print $1}')
mkdir -p "$CAN_STORE"

# Copy content to store (truth copy — survives renames/moves/deletes)
cp {file} "$CAN_STORE/$ADDRESS"

# Index it (append-only TSV log)
echo -e "$CLOCK\t$ADDRESS\t{name}\t{filepath}\t{bag}" >> "$CAN_INDEX"
```

存储系统采用内容地址机制：文件通过哈希值来命名。位于 `$CAN_STORE/$ADDRESS` 的文件才是内容的真实版本。原始文件的名称、位置或状态（如重命名、移动或删除）都不会影响存储中的内容。索引系统会记录所有内容的访问记录：相同的哈希值对应不同的路径和不同的时间戳，从而形成访问日志。

### 4. CAN-find：在三个轴上进行搜索

```bash
# Find by time range
awk -F'\t' -v start="1770460800000" -v end="1770547200000" \
  '$1 >= start && $1 <= end' ~/.can/index.tsv

# Find by address prefix
grep "a3f8" ~/.can/index.tsv

# Find by name (fuzzy human search)
grep -i "security" ~/.can/index.tsv

# Find by bag
awk -F'\t' '$5 == "GOOD"' ~/.can/index.tsv
```

计算机可以通过时间轴和地址轴快速、准确地搜索内容；人类则可以通过名称进行模糊搜索。两种搜索方式最终都会查询到相同的索引。

### 5. CAN-locate：查找内容的当前位置

当你知道内容的哈希值但不知道其存储路径时，系统会按优先级顺序在多个来源中进行查找：

```bash
TARGET="a3f8b2c1"
CAN_STORE=~/.can/store
CAN_INDEX=~/.can/index.tsv

# 1. Check store first (guaranteed if indexed as GOOD/HUSH/POST)
FULL_HASH=$(grep "$TARGET" "$CAN_INDEX" | head -1 | cut -f2)
STORE_PATH="$CAN_STORE/$FULL_HASH"
if [ -f "$STORE_PATH" ]; then
  echo "STORE HIT: $STORE_PATH"
  exit 0
fi

# 2. Check last known paths from index
while IFS=$'\t' read -r clock addr name path bag; do
  if [ -f "$path" ]; then
    VERIFY=$(sha256sum "$path" | awk '{print $1}')
    if [ "$VERIFY" = "$addr" ]; then
      echo "INDEX HIT: $path"
      exit 0
    fi
  fi
done < <(grep "$TARGET" "$CAN_INDEX")

# 3. Not found in store or index
echo "NOT FOUND in store or index."
echo "Content may have been moved or deleted from known paths."
echo "To scan broader filesystem, agent should ask human for permission."
```

优先顺序：本地存储（即时且可靠）→ 索引路径（快速且可验证）→ 询问相关人员。哈希值才是内容的唯一地址，路径只是内容的访问路径。

### 6. CAN-verify-skill：安装前验证技能的有效性

```bash
TMPDIR=$(mktemp -d)
clawhub install {skill-slug} --workdir "$TMPDIR"

CLOCK=$(date +%s%3N)
ADDRESS=$(find "$TMPDIR/skills/{skill-slug}" -type f | sort | xargs cat | sha256sum | awk '{print $1}')

echo "Skill: {skill-slug}"
echo "Clock: $CLOCK"
echo "Address: $ADDRESS"

echo -e "$CLOCK\t$ADDRESS\tskill:{skill-slug}\t$TMPDIR\tSAVE" >> ~/.can/index.tsv

# Only install if ADDRESS matches known-good or human approves
rm -rf "$TMPDIR"
```

### 7. CAN-route：通过名称/地址获取内容，而非路径

用户只需指定所需内容，系统会自动处理其存储位置。

```bash
WANTED="{address}"

# Priority order: local store → peer agents → relays → web
# Each source returns content. Verify hash. First valid match wins.

# 1. Local store (instant, offline, free)
LOCAL="$CAN_STORE/$WANTED"
if [ -f "$LOCAL" ]; then
  echo "LOCAL HIT: $LOCAL"
  # done — zero network, zero latency, zero trust needed
  exit 0
fi

# 2. Peer agent (nearby, fast, one hop)
# Ask peers: "who has $WANTED?"
# Protocol: agent broadcasts WANTED hash
# Any agent with $WANTED in their store responds with content
# Requester verifies: sha256sum == $WANTED
# If verified, save to local store (cache)

# 3. Relay (nostr relay, IPFS gateway, any content-addressed network)
# Query relay for events containing CAN ADDRESS tag
# Relay returns content. Verify hash. Cache locally.

# 4. Web fallback (legacy, location-addressed)
# Use URL hint from index if available
# Fetch, verify hash, cache locally
# If hash doesn't match URL content: STALE or TAMPERED
```

目前步骤1已经实现。步骤2-4还处于协议设计阶段，未来会随着网络的发展不断完善。仅依赖本地存储系统就已经带来了巨大的优势：无需网络参与、无延迟、无需信任第三方。

**这对代理来说意味着什么：**

目前所有的网络请求（如 `web_fetch`）都是基于路径和地址的：需要访问特定的URL，同时还要担心内容是否未被篡改或服务器是否正常运行。而CAN路由系统则完全消除了这些不确定性：用户只需提供哈希值，系统会自动验证内容后再进行传输。

使用CAN路由系统的代理：
- 首先会检查本地存储（无需网络连接，即时完成）；
- 不会重复下载相同的内容（哈希值作为唯一标识）；
- 不会下载错误的内容（哈希值作为验证依据）；
- 不关心内容的来源（任何来源只要哈希值相同即可）；
- 会将与验证通过的内容共享给其他代理（随着网络规模的扩大，传输速度也会更快）。

**路由表其实就是CAN的索引系统**。每个条目都记录了“该内容在某个时间、通过某个路径被访问过”。对于同一个地址，可能存在多个条目，系统会选择最新、最近或传输速度最快的那个版本。索引本身就是路由表。

### 8. CAN-sign：添加身份验证（可选的第四轴）

虽然不是必需的，但添加身份验证可以增加系统的透明度。任何能够为时间轴和地址轴生成的哈希值添加签名的密钥都可以用于身份验证。常见的签名方式包括Nostr（NIP-07）、Farcaster、Web2 OAuth或本地机器密钥等。验证方法相同：将签名与公钥进行比对。

## BAG：内容元数据

内容会附带元数据，用于记录其创建时的上下文信息：

```
SAVE  →  bag of meh, index silently
GOOD  →  bag of goodies, tag it
HUSH  →  hush bag, local only, no sharing, store copy
POST  →  bag of poasted, publish, share, sign
```

元数据是索引系统中的第五个维度。默认情况下，系统会在内容保存时自动为其添加元数据（由监控工具完成）。元数据的类型包括“GOOD”、“HUSH”或“POST”。其中，“HUSH”状态的文件不会被自动推广到其他地方。

## 路径命名与CAN命名的对比

| | 路径 `/home/x/docs/report_v3.md` | CAN `1770508800000 a3f8b2c1...` |
|---|---|---|
| 可以被悄悄修改 | 可以 | 不可以（新内容会生成新的哈希值） |
| 可以被重定向 | 可以 | 不可以 |
| 需要信任来源 | 需要 | 不需要 |
| 可以按时间排序 | 不能 | 可以（通过时间轴排序） |
| 人类可以搜索 | 仅能通过文件名搜索 | 可以通过昵称、标签或关键词搜索 |
| 支持离线访问 | 取决于文件系统的挂载方式 | 始终支持 |
| 跨代理传输 | 始终支持 | 始终支持 |
| 重命名会破坏引用关系 | 会 | 不会（昵称只是别名） |
| 删除后内容仍可被访问 | 不能 | 可以（存储系统保留原始副本） |
| 可以通过名称访问 | 不能（需要完整路径） | 可以（哈希值是全局唯一的地址） |

路径命名和CAN命名可以共存：路径用于满足人类的使用习惯，而CAN命名则用于实现信任和路由功能。

## 基于位置寻址与基于内容寻址的路由方式

### 基于位置寻址

基于位置寻址的方式会问：“我该去哪里获取这个内容？”
基于内容寻址的方式则问：“谁拥有这个内容？”

第一种方式只有一个答案（服务器）；第二种方式有很多答案（任何拥有该内容的人都可以提供）。前者容易出错，后者则更具弹性和离线访问能力。

## 时间轴：未来的扩展

CAN系统支持时间轴上的动态更新：
- **过去**：已存在的旧内容（用于验证或归档）；
- **现在**：正在创建的内容（正在进行签名或记录）；
- **未来**：预定在某个时间发布的 content（通过定时器管理）。

```bash
FUTURE_CLOCK=$(($(date +%s%3N) + 3600000))
echo -e "$FUTURE_CLOCK\t\ttimer:check-deployment" >> ~/.can/index.tsv
# ADDRESS is empty — fills in when content arrives
```

未来没有地址的CAN条目只是对内容的预测。系统会监控这些未实现的“承诺”，并在必要时提醒相关人员。

## 代理间的通信协议

在与其他代理交换内容时：
1. 共享内容时必须包含时间轴和地址轴信息；
2. 在使用任何内容之前，必须先验证其地址；
3. 为接收方提供有助于其用户查找内容的名称；
4. 如果地址信息不匹配，必须公开说明情况以保护网络安全；
5. 不要在响应、共享或与其他代理的通信中包含“HUSH”状态的内容；
6. 如果拥有密钥，必须为CAN记录添加签名；
7. 将验证通过的内容缓存到本地，以便其他代理可以访问；
8. 首先通过哈希值进行路由，其次通过URL；优先使用基于内容的寻址方式。

## 设计哲学

每个对象都有三个真实的身份标识：
- **时间轴**：内容存在的时间（客观、通用、自动生成）；
- **地址轴**：内容本身的唯一标识（客观、通用、自动生成）；
- **名称轴**：人类赋予的名称（主观、个性化、可选）。

路径 `/home/agent/important.txt` 只是一种描述，它只说明了内容曾经的存储位置，而非内容本身的本质。URL `https://example.com/doc` 则是一个指向内容的指引，但它并不能保证你能获取到该内容。而CAN系统则能提供内容的真实信息和创建时间，这种信息是永久有效的、不可篡改的，并且任何人都可以通过哈希值访问该内容，无需任何权限验证。

**建议的做法：** 为内容起名，并通过哈希值进行路由。

## 参考文献

- Van Jacobson，《命名数据网络（Named Data Networking, NDN）》
- John Day，《递归互联网架构（Recursive InterNetwork Architecture, RINA）》
- Git中的内容寻址对象存储机制
- Nostr协议（NIP-01）用于身份验证
- IPFS中的内容寻址分布式存储
- Zooko的三角模型（CAN系统实现了这些目标：全局性、安全性以及通过三个轴实现人类可理解的内容访问）