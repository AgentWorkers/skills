---
name: sapi-tts
description: Windows SAPI5文本转语音功能，支持使用神经网络生成的合成声音。作为对依赖GPU的TTS技术的轻量级替代方案，该工具完全不使用GPU资源，能够即时生成语音效果。系统会自动检测最适合您所使用语言的合成声音。兼容Windows 10/11操作系统。
---

# SAPI5 TTS（Windows）

这是一个基于Windows内置SAPI5技术的轻量级文本转语音工具，无需使用GPU，支持即时语音生成。

## 安装

将以下脚本保存为`tts.ps1`文件，并将其放在您的`skills`文件夹中：

```powershell
<#
.SYNOPSIS
    Windows SAPI5 TTS - Lightweight text-to-speech
.DESCRIPTION
    Uses Windows built-in speech synthesis (SAPI5).
    Works with Neural voices (Win11) or legacy voices (Win10).
    Zero GPU usage, instant generation.
#>

param(
    [Parameter(Mandatory=$false, Position=0)]
    [string]$Text = "",
    
    [Parameter(Mandatory=$false)]
    [Alias("Voice", "v")]
    [string]$VoiceName = "",
    
    [Parameter(Mandatory=$false)]
    [Alias("Lang", "l")]
    [string]$Language = "fr",
    
    [Parameter(Mandatory=$false)]
    [Alias("o")]
    [string]$Output = "",
    
    [Parameter(Mandatory=$false)]
    [Alias("r")]
    [int]$Rate = 0,
    
    [Parameter(Mandatory=$false)]
    [Alias("p")]
    [switch]$Play,
    
    [Parameter(Mandatory=$false)]
    [switch]$ListVoices
)

Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer

$installedVoices = $synth.GetInstalledVoices() | Where-Object { $_.Enabled } | ForEach-Object { $_.VoiceInfo }

if ($ListVoices) {
    Write-Host "`nInstalled SAPI5 voices:`n" -ForegroundColor Cyan
    foreach ($v in $installedVoices) {
        $type = if ($v.Name -match "Online|Neural") { "[Neural]" } else { "[Legacy]" }
        Write-Host "  $($v.Name)" -ForegroundColor White -NoNewline
        Write-Host " $type" -ForegroundColor DarkGray -NoNewline
        Write-Host " - $($v.Culture) $($v.Gender)" -ForegroundColor Gray
    }
    Write-Host ""
    $synth.Dispose()
    exit 0
}

if (-not $Text) {
    Write-Error "Text required. Use: .\tts.ps1 'Your text here'"
    Write-Host "Use -ListVoices to see available voices"
    $synth.Dispose()
    exit 1
}

function Select-BestVoice {
    param($voices, $preferredName, $lang)
    
    if ($preferredName) {
        $match = $voices | Where-Object { $_.Name -like "*$preferredName*" } | Select-Object -First 1
        if ($match) { return $match }
        Write-Warning "Voice '$preferredName' not found, auto-selecting..."
    }
    
    $cultureMap = @{
        "fr" = "fr-FR"; "french" = "fr-FR"
        "en" = "en-US"; "english" = "en-US"
        "de" = "de-DE"; "german" = "de-DE"
        "es" = "es-ES"; "spanish" = "es-ES"
        "it" = "it-IT"; "italian" = "it-IT"
    }
    $targetCulture = $cultureMap[$lang.ToLower()]
    if (-not $targetCulture) { $targetCulture = $lang }
    
    $neuralMatch = $voices | Where-Object { 
        $_.Name -match "Online|Neural" -and $_.Culture.Name -eq $targetCulture 
    } | Select-Object -First 1
    if ($neuralMatch) { return $neuralMatch }
    
    $langMatch = $voices | Where-Object { $_.Culture.Name -eq $targetCulture } | Select-Object -First 1
    if ($langMatch) { return $langMatch }
    
    $anyNeural = $voices | Where-Object { $_.Name -match "Online|Neural" } | Select-Object -First 1
    if ($anyNeural) { return $anyNeural }
    
    return $voices | Select-Object -First 1
}

$selectedVoice = Select-BestVoice -voices $installedVoices -preferredName $VoiceName -lang $Language

if (-not $selectedVoice) {
    Write-Error "No SAPI5 voices found! Install voices in Windows Settings > Time & Language > Speech"
    $synth.Dispose()
    exit 1
}

if (-not $Output) {
    $ttsDir = "$env:USERPROFILE\.openclaw\workspace\tts"
    if (-not (Test-Path $ttsDir)) { New-Item -ItemType Directory -Path $ttsDir -Force | Out-Null }
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $Output = "$ttsDir\sapi_$timestamp.wav"
}

try {
    $synth.SelectVoice($selectedVoice.Name)
    $synth.Rate = $Rate
    $synth.SetOutputToWaveFile($Output)
    $synth.Speak($Text)
    $synth.SetOutputToNull()
    
    Write-Host "Voice: $($selectedVoice.Name) [$($selectedVoice.Culture)]" -ForegroundColor Cyan
    Write-Host "MEDIA:$Output"
    
    # Auto-play if requested (uses .NET MediaPlayer, no external player)
    if ($Play) {
        Add-Type -AssemblyName PresentationCore
        $player = New-Object System.Windows.Media.MediaPlayer
        $player.Open([Uri]$Output)
        $player.Play()
        Start-Sleep -Milliseconds 500
        while ($player.Position -lt $player.NaturalDuration.TimeSpan) {
            Start-Sleep -Milliseconds 100
        }
        $player.Close()
    }
    
} catch {
    Write-Error "TTS failed: $($_.Exception.Message)"
    exit 1
} finally {
    $synth.Dispose()
}
```

## 快速入门

```powershell
# Generate audio file
.\tts.ps1 "Bonjour, comment vas-tu ?"

# Generate AND play immediately
.\tts.ps1 "Bonjour !" -Play
```

## 参数

| 参数          | 别名        | 默认值     | 说明                                      |
|---------------|------------|---------|-----------------------------------------|
| `-Text`        | （位置参数）     | 必需      | 需要转语音的文本                          |
| `-VoiceName`     | `-Voice`, `-v`     | 自动匹配   | 语音名称（部分匹配即可）                         |
| `-Language`     | `-Lang`, `-l`     | fr       | 语言：fr, en, de, es, it...                      |
| `-Output`      | `-o`        | 自动匹配   | 输出WAV文件的路径                          |
| `-Rate`        | `-r`        | 0        | 语速：-10（慢）到+10（快）                         |
| `-Play`        | `-p`        | false      | 生成后立即播放音频                          |
| `-ListVoices`    |            |           | 显示已安装的语音列表                         |

## 示例

```powershell
# French with auto-play
.\tts.ps1 "Bonjour !" -Lang fr -Play

# English, faster
.\tts.ps1 "Hello there!" -Lang en -Rate 2 -Play

# Specific voice
.\tts.ps1 "Salut !" -Voice "Denise" -Play

# List available voices
.\tts.ps1 -ListVoices
```

## （推荐）安装神经语音（Neural Voices）

神经语音（Neural Voices）的音质远优于传统的桌面语音（Desktop Voices）。

### Windows 11
神经语音已内置。操作步骤：
**设置 → 时间与语言 → 语音 → 管理语音**

### Windows 10/11（更多语音选项）
若需使用更多神经语音（例如法语的Denise语音）：
1. 安装[NaturalVoiceSAPIAdapter](https://github.com/gexgd0419/NaturalVoiceSAPIAdapter)
2. 在**设置 → 时间与语言 → 语音**中下载所需语音
3. 运行`-ListVoices`命令查看可用语音列表

## 性能
- **语音生成时间**：即时（<1秒）
- **硬件要求**：无需GPU
- **CPU占用**：极低
- **音质**：高质量（神经语音）/ 基础质量（传统语音）

## 致谢

本工具由Pocus 🎩开发，AI助手团队与Olive (@Korddie) 共同完成。