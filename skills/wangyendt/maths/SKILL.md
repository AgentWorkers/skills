---
name: pywayne-maths
description: 数学工具函数，用于因式分解、数字计数以及使用Karatsuba算法进行大整数乘法。适用于解决数论问题、计算因数、统计数字出现的次数，或执行优化的大整数乘法运算。
---
# Pywayne Maths

提供用于数论、数字分析以及优化整数运算的数学实用函数。

## 快速入门

```python
from pywayne.maths import get_all_factors, digitCount, karatsuba_multiplication

# Get all factors of a number
factors = get_all_factors(28)
print(factors)  # [1, 2, 4, 7, 14, 28]

# Count digit occurrences
count = digitCount(100, 1)
print(count)  # 21 (digit 1 appears 21 times in 1-100)

# Large integer multiplication
product = karatsuba_multiplication(1234, 5678)
print(product)  # 7006652
```

## 函数

### get_all_factors

返回一个正整数的所有因数。

**参数:**
- `n` - 需要分解因数的正整数

**返回值:**
- `n` 的所有因数列表

**使用场景:**
- 数论问题
- 寻找除数
- 简化分数
- 计算最大公约数（GCD）

**示例:**
```python
from pywayne.maths import get_all_factors

factors = get_all_factors(36)
print(factors)  # [1, 2, 3, 4, 6, 9, 12, 18, 36]

# Check if number is prime
n = 17
factors = get_all_factors(n)
if len(factors) == 2:  # Only 1 and itself
    print(f"{n} is prime")
else:
    print(f"{n} is not prime")
```

### digitCount

统计从 1 到 `n` 中数字 `k` 出现的次数。

**参数:**
- `n` - 计数范围的上限（正整数）
- `k` - 需要统计的数字（0-9）

**返回值:**
- 数字 `k` 在 [1, n] 范围内的出现次数

**特殊情况:**
- 当 `k = 0` 时，统计所有以 `0` 结尾的数（即 `n` 之后的所有数）

**使用场景:**
- 数字频率分析
- 数论问题
- 数据分析任务

**示例:**
```python
from pywayne.maths import digitCount

# Count digit 1 from 1 to 100
count = digitCount(100, 1)
print(count)  # 21

# Count each digit 0-9 in range 1-1000
for k in range(10):
    count = digitCount(1000, k)
    print(f"Digit {k}: {count} times")
```

### karatsuba_multiplication

使用 Karatsuba 分治算法来乘两个整数。

**参数:**
- `x` - 被乘数
- `y` - 乘数

**返回值:**
- `x` 和 `y` 的乘积

**算法原理:**
- Karatsuba 算法通过递归分治的方式实现大整数的乘法运算
- 时间复杂度: O(n^log₂3) ≈ O(n^1.585)
- 对于非常大的数来说，比传统的乘法算法（O(n²)）更高效

**使用场景:**
- 大整数乘法
- 算法优化
- 竞赛编程
- 密码学应用

**示例:**
```python
from pywayne.maths import karatsuba_multiplication

# Compare with standard multiplication
a, b = 123456789, 987654321
result = karatsuba_multiplication(a, b)
print(result)  # 121932631112635269

# Verify
assert result == a * b
```

## 常见应用

### 判断质数

```python
from pywayne.maths import get_all_factors

def is_prime(n):
    factors = get_all_factors(n)
    return len(factors) == 2 and factors == [1, n]

print(is_prime(17))   # True
print(is_prime(18))   # False
```

### 计算最大公约数（GCD）

```python
from pywayne.maths import get_all_factors

def gcd(a, b):
    factors_a = set(get_all_factors(a))
    factors_b = set(get_all_factors(b))
    common = factors_a & factors_b
    return max(common)

print(gcd(24, 36))  # 12
```

### 数字频率分析

```python
from pywayne.maths import digitCount

def digit_frequency(n):
    frequency = {}
    for k in range(10):
        frequency[k] = digitCount(n, k)
    return frequency

print(digit_frequency(1000))
# {0: 189, 1: 301, 2: 300, 3: 300, ...}
```

### 大数计算

```python
from pywayne.maths import karatsuba_multiplication

# Very large numbers
x = 123456789012345678901234567890
y = 9876543210987654321098765432109876

# Use Karatsuba for efficiency
product = karatsuba_multiplication(x, y)
```

## 注意事项

- `get_all_factors` 返回的是排序后的唯一因数列表
- `digitCount` 统计的是从 1 到 `n`（包括 `n`）范围内数字 `k` 的出现次数
- `karatsuba_multiplication` 适用于具有数百位以上的大整数
- 对于较小的整数，由于开销较小，使用标准的乘法运算 `*` 可能会更快