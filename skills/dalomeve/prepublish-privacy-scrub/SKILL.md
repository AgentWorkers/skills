---
name: prepublish-privacy-scrub
description: 在发布技能之前，先扫描并删除敏感数据。检测并移除 API 密钥、令牌、机密信息以及个人隐私数据。
---
# 发布前隐私数据清洗

在发布内容之前，先扫描文件中是否存在敏感数据。

## 问题

如果未进行适当的清理，发布过程中可能会泄露以下信息：
- API 密钥和令牌
- 网关凭证
- 用户个人路径和电子邮件地址
- 内部服务地址

## 工作流程

### 1. 敏感数据模式检测

```powershell
function Test-PrivacyScan {
    param([string]$path)
    
    $sensitivePatterns = @(
        'apiKey\s*[=:]\s*["\']?[A-Za-z0-9]',
        'token\s*[=:]\s*["\']?[A-Za-z0-9]{10,}',
        'secret\s*[=:]\s*["\']?[A-Za-z0-9]',
        'password\s*[=:]\s*["\']?.+',
        'Bearer\s+[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+',
        'sk-[A-Za-z0-9]{32,}',
        'OPENCLAW_\w+\s*[=:]\s*\S+',
        'https://\S+\.ngrok\S+',
        '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    )
    
    $files = Get-ChildItem $path -Recurse -File | 
        Where-Object { $_.Extension -in @('.md', '.ps1', '.json', '.txt') }
    
    $findings = @()
    
    foreach ($file in $files) {
        $content = Get-Content $file.FullName -Raw
        foreach ($pattern in $sensitivePatterns) {
            $matches = [regex]::Matches($content, $pattern, 'IgnoreCase')
            foreach ($m in $matches) {
                $findings += @{
                    File = $file.FullName
                    Pattern = $pattern
                    Match = $m.Value.Substring(0, [Math]::Min(20, $m.Value.Length)) + "..."
                }
            }
        }
    }
    
    return $findings
}
```

### 2. 数据清洗

```powershell
function Invoke-PrivacyScrub {
    param([string]$path)
    
    $replacements = @{
        'apiKey\s*[=:]\s*["\']?[^"''\s]+' = 'apiKey: "REDACTED"'
        'token\s*[=:]\s*["\']?[^"''\s]+' = 'token: "REDACTED"'
        'secret\s*[=:]\s*["\']?[^"''\s]+' = 'secret: "REDACTED"'
    }
    
    $files = Get-ChildItem $path -Recurse -File
    
    foreach ($file in $files) {
        $content = Get-Content $file.FullName -Raw
        $modified = $false
        
        foreach ($kv in $replacements.GetEnumerator()) {
            if ($content -match $kv.Key) {
                $content = $content -replace $kv.Key, $kv.Value
                $modified = $true
            }
        }
        
        if ($modified) {
            $content | Out-File $file.FullName -Encoding UTF8
            Write-Host "Scrubbed: $($file.Name)"
        }
    }
}
```

### 3. 发布前检查清单

```markdown
## Privacy Scan Results

- [ ] No apiKey values in files
- [ ] No token values in files
- [ ] No secret/password in files
- [ ] No personal emails
- [ ] No absolute user paths (C:\Users\name\)
- [ ] No internal service URLs

**Scan Command**:
```powershell
Test-PrivacyScan -path "./skill-folder"
```
```

## 可执行任务完成标准

| 标准 | 验证方式 |
|----------|-------------|
| 扫描任务已执行 | Test-PrivacyScan 返回结果 |
| 未发现关键问题 | API 密钥/令牌/敏感信息未匹配（即匹配项数量为 0） |
| 数据清洗已完成 | 文件中的敏感信息已被替换为占位符 |
| 检查清单全部完成 | 所有项目均已通过验证 |

## 隐私与安全要求

- 扫描结果不会被外部记录
- 替换后的敏感信息使用通用占位符
- 清洗操作前会备份原始文件

## 自动触发条件

适用于以下场景：
- 在任何技能内容发布之前
- 在将技能代码推送到 Git 仓库之前
- 在从工作目录复制技能文件之后

---

**先进行数据清洗，再安全发布。**