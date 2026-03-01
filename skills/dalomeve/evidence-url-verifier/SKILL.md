---
name: evidence-url-verifier
description: 验证证据URL的真实性及可访问性。确保这些链接指向实际内容，而非占位符。
---
# 证据URL验证器

用于验证证据URL的真实性及可访问性。

## 问题

证据链接通常会遇到以下问题：
- 指向不存在的资源
- 是占位符（例如 example.com）
- 过期或被删除
- 与所声称的内容不符

## 工作流程

### 1. URL验证

```powershell
function Test-EvidenceUrl {
    param([string]$url)
    
    try {
        $response = Invoke-WebRequest -Uri $url -Method Head -TimeoutSec 10
        return @{
            Valid = $true
            Status = $response.StatusCode
            ContentType = $response.ContentType
        }
    } catch {
        return @{
            Valid = $false
            Error = $_.Exception.Message
        }
    }
}

# Usage
$result = Test-EvidenceUrl "https://example.com/artifact"
if ($result.Valid) {
    Write-Host "URL valid: $($result.Status)"
} else {
    Write-Error "URL invalid: $($result.Error)"
}
```

### 2. 内容验证

```powershell
# Check URL matches claimed content type
$response = Invoke-WebRequest -Uri $url
if ($response.ContentType -notlike "text/*" -and $expectedType -eq "text") {
    Write-Warning "Content type mismatch"
}

# Check for placeholder text
$content = $response.Content
if ($content -match "lorem ipsum|placeholder|example") {
    Write-Warning "Content appears to be placeholder"
}
```

### 3. 证据文件的存在性验证

```powershell
# For local paths
if (Test-Path $artifactPath) {
    $size = (Get-Item $artifactPath).Length
    if ($size -eq 0) {
        Write-Warning "Artifact file is empty"
    }
} else {
    Write-Error "Artifact not found: $artifactPath"
}
```

## 可执行任务的完成标准

| 标准 | 验证方式 |
|----------|-------------|
| URL能够解析 | 返回HTTP 200状态码 |
| 内容与预期一致 | 文件类型符合要求 |
| 无占位符 | 文件内容具有实际意义 |
| 本地路径存在 | Test-Path函数返回true |

## 隐私/安全措施

- 不记录完整的URL内容
- 在响应中屏蔽敏感数据
- 遵守请求速率限制（每秒最多1次请求）

## 自动触发场景

在以下情况下使用该工具：
- 任务要求提供证据文件时
- 当URL被用作证明时
- 在标记任务完成之前
- 对过去的任务完成情况进行审计时

---

**验证证据。信任，但需确认。**