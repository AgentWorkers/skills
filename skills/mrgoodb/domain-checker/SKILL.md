---
name: domain-checker
description: **检查多个顶级域名（TLD）下的域名可用性**  
适用于快速批量查询域名信息及进行头脑风暴。
metadata: {"clawdbot":{"emoji":"🌐"}}
---

# 域名检查工具

用于查询域名是否可以被注册。

## 快速查询（WHOIS）

```bash
# Single domain
whois example.com 2>/dev/null | grep -iE "no match|not found|available|no data found" && echo "✅ AVAILABLE" || echo "❌ TAKEN"

# Multiple TLDs at once
for tld in com ai io co net; do
  result=$(whois "myname.$tld" 2>/dev/null | grep -iE "no match|not found|available|no data found|^No " | head -1)
  if [ -n "$result" ]; then
    echo "✅ myname.$tld - AVAILABLE"
  else
    echo "❌ myname.$tld - taken"
  fi
done
```

## 批量查询功能

```bash
check_domains() {
  local name="$1"
  shift
  local tlds="${@:-com ai io co net org}"
  
  echo "Checking: $name"
  echo "---"
  for tld in $tlds; do
    domain="${name}.${tld}"
    # Use timeout to avoid hanging on slow WHOIS servers
    result=$(timeout 5 whois "$domain" 2>/dev/null | grep -iE "no match|not found|available|no data found|^No |status: free" | head -1)
    if [ -n "$result" ]; then
      echo "✅ $domain"
    else
      echo "❌ $domain"
    fi
  done
}

# Usage
check_domains "asklee" com ai io co bot
check_domains "myproject" com net org io
```

## 域名创意生成与可用性检查流程：

在帮助客户选择域名时：

1. 生成10-20个域名创意。
2. 使用批量查询工具检查这些域名的可用性：
```bash
for name in idea1 idea2 idea3 brandname coolbot; do
  check_domains "$name" com ai io
  echo ""
done
```

## 各顶级域名（TLD）的WHOIS查询特殊规则：

| TLD | 可用性提示 |
|-----|---------------------|
| .com, .net, .org | “未找到匹配的记录” |
| .io | “可用”或“未找到” |
| .ai | “未找到”或“数据不存在” |
| .co | “数据不存在” |
| .bot | “未找到该域名” |
| .app | “该域名不存在” |

## 快速API替代方案（当WHOIS查询速度较慢时）

```bash
# Using domainr API (no key needed for basic checks)
curl -s "https://domainr.p.rapidapi.com/v2/status?domain=example.com" \
  -H "X-RapidAPI-Key: YOUR_KEY"

# Or DNS-based check (not 100% reliable but fast)
dig +short "$domain" | grep -q . && echo "❌ Has DNS" || echo "🤔 No DNS (might be available)"
```

## 使用建议：

- 在非高峰时段进行查询，以获得更快的响应速度。
- 一些高级或预留的域名在WHOIS查询中可能显示为“可用”，但实际上无法购买。
- 在确认域名可用性之前，务必在注册商（如GoDaddy、Namecheap、Porkbun）处进行最终验证。
- .ai域名需要使用位于安圭拉的注册商进行注册，或使用专门处理此类域名的注册商。