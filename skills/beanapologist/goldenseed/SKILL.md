---
name: goldenseed
description: 用于可重复测试和程序化生成的确定性熵流。该熵流能够实现完美的50/50统计分布，并支持哈希验证功能。虽然不具备加密安全性，但适用于测试、世界生成（world generation）以及那些可重复性比不可预测性更重要的场景。
tags: [testing, procedural-generation, deterministic, reproducibility, golden-ratio]
version: 1.0.0
author: beanapologist
license: GPL-3.0+
---

# GoldenSeed - 用于代理程序的确定性熵生成工具

**在需要每次都获得相同结果时，提供可复现的随机性。**

## 功能概述

GoldenSeed 通过一个固定的种子值生成无限的确定性字节流。相同的种子值始终会产生相同的输出。非常适合以下场景：

- ✅ **测试可复现性**：通过重放精确的随机序列来调试那些结果不稳定的测试
- ✅ **程序化内容生成**：使用种子值创建可验证的游戏世界、艺术作品或音乐
- ✅ **科学模拟**：实现可复现的蒙特卡洛模拟和物理引擎
- ✅ **统计测试**：提供完美的 50/50 概率分布（可证明公平性）
- ✅ **哈希验证**：确认输出确实来源于指定的种子值

## 注意事项

⚠️ **不具备加密安全性** - 不适用于密码、密钥或安全令牌的生成。请使用 `os.urandom()` 或 `secrets` 模块进行加密操作。

## 快速入门

### 安装

```bash
pip install golden-seed
```

### 基本用法

```python
from gq import UniversalQKD

# Create generator with default seed
gen = UniversalQKD()

# Generate 16-byte chunks
chunk1 = next(gen)
chunk2 = next(gen)

# Same seed = same sequence (reproducibility!)
gen1 = UniversalQKD()
gen2 = UniversalQKD()
assert next(gen1) == next(gen2)  # Always identical
```

### 统计质量 - 完美的 50/50 概率分布

```python
from gq import UniversalQKD

def coin_flip_test(n=1_000_000):
    """Demonstrate perfect 50/50 distribution"""
    gen = UniversalQKD()
    heads = 0
    
    for _ in range(n):
        byte = next(gen)[0]  # Get first byte
        if byte & 1:  # Check LSB
            heads += 1
    
    ratio = heads / n
    print(f"Heads: {ratio:.6f} (expected: 0.500000)")
    return abs(ratio - 0.5) < 0.001  # Within 0.1%

assert coin_flip_test()  # ✓ Passes every time
```

### 可复现的测试

```python
from gq import UniversalQKD

class TestDataGenerator:
    def __init__(self, seed=0):
        self.gen = UniversalQKD()
        # Skip to seed position
        for _ in range(seed):
            next(self.gen)
    
    def random_user(self):
        data = next(self.gen)
        return {
            'id': int.from_bytes(data[0:4], 'big'),
            'age': 18 + (data[4] % 50),
            'premium': bool(data[5] & 1)
        }

# Same seed = same test data every time
def test_user_pipeline():
    users = TestDataGenerator(seed=42)
    user1 = users.random_user()
    
    # Run again - identical results!
    users2 = TestDataGenerator(seed=42)
    user1_again = users2.random_user()
    
    assert user1 == user1_again  # ✓ Reproducible!
```

### 程序化内容生成

```python
from gq import UniversalQKD

class WorldGenerator:
    def __init__(self, world_seed=0):
        self.gen = UniversalQKD()
        for _ in range(world_seed):
            next(self.gen)
    
    def chunk(self, x, z):
        """Generate deterministic chunk at coordinates"""
        data = next(self.gen)
        return {
            'biome': data[0] % 10,
            'elevation': int.from_bytes(data[1:3], 'big') % 256,
            'vegetation': data[3] % 100,
            'seed_hash': data.hex()[:16]  # For verification
        }

# Generate infinite world from single seed
world = WorldGenerator(world_seed=12345)
chunk = world.chunk(0, 0)
print(f"Biome: {chunk['biome']}, Elevation: {chunk['elevation']}")
print(f"Verifiable hash: {chunk['seed_hash']}")
```

### 哈希验证

```python
from gq import UniversalQKD
import hashlib

def generate_with_proof(seed=0, n_chunks=1000):
    """Generate data with hash proof"""
    gen = UniversalQKD()
    for _ in range(seed):
        next(gen)
    
    chunks = [next(gen) for _ in range(n_chunks)]
    data = b''.join(chunks)
    proof = hashlib.sha256(data).hexdigest()
    
    return data, proof

# Anyone with same seed can verify
data1, proof1 = generate_with_proof(seed=42, n_chunks=100)
data2, proof2 = generate_with_proof(seed=42, n_chunks=100)

assert data1 == data2      # ✓ Same output
assert proof1 == proof2    # ✓ Same hash
```

## 代理程序应用案例

### 调试不稳定的测试

当您的测试有时通过、有时失败时，可以使用 GoldenSeed 替换随机值，以重现相同的测试场景：

```python
# Instead of:
import random
value = random.randint(1, 100)  # Different every time

# Use:
from gq import UniversalQKD
gen = UniversalQKD()
value = next(gen)[0] % 100 + 1  # Same value for same seed
```

### 程序化艺术创作

使用可验证的种子值生成艺术作品、音乐或非同质化代币（NFT）：

```python
def generate_art(seed):
    gen = UniversalQKD()
    for _ in range(seed):
        next(gen)
    
    # Generate deterministic art parameters
    palette = [next(gen)[i % 16] for i in range(10)]
    composition = next(gen)
    
    return create_artwork(palette, composition)

# Seed 42 always produces the same artwork
art = generate_art(seed=42)
```

### 竞技游戏的公平性验证

通过共享种子值来证明游戏结果的公平性：

```python
class FairDice:
    def __init__(self, game_seed):
        self.gen = UniversalQKD()
        for _ in range(game_seed):
            next(self.gen)
    
    def roll(self):
        return (next(self.gen)[0] % 6) + 1

# Players can verify rolls by running same seed
dice = FairDice(game_seed=99999)
rolls = [dice.roll() for _ in range(100)]
# Share seed 99999 - anyone can verify identical sequence
```

## 参考资料

- **GitHub**: https://github.com/COINjecture-Network/seed
- **PyPI**: https://pypi.org/project/golden-seed/
- **示例代码**：请查看仓库中的 `examples/` 目录
- **统计测试**：请参阅 `docs/ENTROPY_ANALYSIS.md`

## 多语言支持

支持多种编程语言，确保在不同平台上生成相同的输出：
- Python（本工具的核心实现）
- JavaScript（`examples/binary_fusion_tap.js` 示例）
- C、C++、Go、Rust、Java（详见仓库文档）

## 许可证

遵循 GPL-3.0+ 许可协议，但军事应用受到限制。详细许可条款请参阅仓库中的 `LICENSE` 文件。

---

**请注意**：GoldenSeed 的主要用途是确保测试结果的可复现性和程序化内容的可验证性，而非提供加密安全功能。如需进行加密操作，请使用 `secrets` 模块。