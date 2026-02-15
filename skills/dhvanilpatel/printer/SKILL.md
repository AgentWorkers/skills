---
name: printer
description: 在 macOS 上通过 CUPS 管理打印机（发现、添加、打印、排队、查看状态、唤醒打印机）。
metadata: {"clawdbot":{"emoji":"🖨️","os":["darwin"],"requires":{"bins":["lp","lpstat","lpadmin"]}}}
---

# 打印机（CUPS）

在 macOS 上，可以使用内置的 CUPS 命令来控制打印机，无需额外的命令行工具（CLI）。

## 发现打印机

```bash
# Network printers (Bonjour/AirPrint)
dns-sd -B _ipp._tcp . 2>/dev/null & sleep 3; kill $! 2>/dev/null

# Get printer details (host, port, resource path)
dns-sd -L "Printer Name" _ipp._tcp . 2>/dev/null & sleep 3; kill $! 2>/dev/null

# CUPS-native discovery
lpstat -e                         # available network destinations
lpinfo --include-schemes dnssd -v # dnssd backends

# IPP discovery
ippfind --timeout 5
```

## 添加打印机（无驱动程序的 IPP Everywhere）

```bash
# Recommended: driverless queue
lpadmin -p MyPrinter -E -v "ipp://printer.local:631/ipp/print" -m everywhere

# Set as default
lpadmin -d MyPrinter

# Enable SNMP supply reporting (toner levels)
sudo lpadmin -p MyPrinter -o cupsSNMPSupplies=true
```

## 打印文件

```bash
lp filename.pdf                      # to default printer
lp -d MyPrinter filename.pdf         # specific printer
lp -d MyPrinter -n 2 file.pdf        # 2 copies
lp -d MyPrinter -o sides=two-sided-long-edge file.pdf  # duplex
lp -d MyPrinter -o media=letter file.pdf
lp -d MyPrinter -o ColorModel=Gray file.pdf  # grayscale

# Print text directly
echo "Hello World" | lp -d MyPrinter
```

## 队列管理

```bash
# Check status
lpstat -p MyPrinter        # printer status
lpstat -o MyPrinter        # queued jobs
lpstat -t                  # everything
lpq -P MyPrinter           # BSD-style queue view

# Cancel jobs
cancel JOB_ID
cancel -a MyPrinter        # cancel all

# Enable/disable
cupsenable MyPrinter       # resume printing
cupsdisable MyPrinter      # pause printer
cupsaccept MyPrinter       # accept new jobs
cupsreject MyPrinter       # reject new jobs
```

## 打印机选项

```bash
# List available options for a printer
lpoptions -p MyPrinter -l

# Set default options (per-user)
lpoptions -p MyPrinter -o sides=two-sided-long-edge

# Set server-side defaults
sudo lpadmin -p MyPrinter -o sides-default=two-sided-long-edge
```

## 状态与诊断

```bash
# IPP status query (detailed)
ipptool -t ipp://PRINTER_IP/ipp/print get-printer-attributes.test

# Filter for key info
ipptool -t ipp://PRINTER_IP/ipp/print get-printer-attributes.test \
  | grep -iE 'printer-state|marker|supply|media|error'
```

## 唤醒处于睡眠状态的打印机

```bash
# IPP poke (usually wakes the printer)
ipptool -q -T 5 ipp://PRINTER_IP/ipp/print get-printer-attributes.test

# HTTP poke (wakes web UI stack)
curl -s -m 5 http://PRINTER_IP/ >/dev/null

# TCP connect test
nc -zw2 PRINTER_IP 631
```

## 防止打印机进入深度睡眠状态

```bash
# Poll every 5 minutes (runs in foreground)
ipptool -q -T 3 -i 300 ipp://PRINTER_IP/ipp/print get-printer-attributes.test
```

若需持续保持打印机处于活跃状态，可以创建一个 launchd 代理程序。

## 通过 SNMP 查看墨盒剩余量

需要先安装 `brew install net-snmp`：

```bash
snmpwalk -v2c -c public PRINTER_IP 1.3.6.1.2.1.43.11.1.1
```

注意：打印机可能已禁用了 SNMP 功能，请检查打印机的远程用户界面（Remote UI）设置。

## 远程用户界面（Web 界面）

大多数网络打印机都提供了一个 Web 界面，地址为 `http://PRINTER_IP/`，可以用于：
- 设置睡眠/定时功能（Settings > Timer Settings > Auto Sleep Time）
- 配置网络协议（启用/禁用 IPP、SNMP、原始的 9100 端口）
- 查看耗材状态

## 故障排除

```bash
# Printer stuck/disabled? Re-enable it
cupsenable MyPrinter

# Check device URI
lpstat -v MyPrinter

# Remove and re-add printer
lpadmin -x MyPrinter
lpadmin -p MyPrinter -E -v "ipp://..." -m everywhere

# CUPS error log
tail -f /var/log/cups/error_log
```

## 注意事项：
- 建议使用 `ipp://` 或 `ipps://` 作为 URI，而不是原始的 9100 或 LPD 协议。
- 参数 `-m everywhere` 会根据打印机的 IPP 功能自动进行配置。
- 不同打印机的选项名称可能有所不同，可以使用 `lpoptions -l` 命令来查看详细信息。
- 最佳的睡眠设置方式是通过打印机的远程用户界面进行配置。
- 自动睡眠功能（1 分钟）有助于保持打印服务的活跃状态，打印任务会自动唤醒打印机。
- **如果打印机完全无响应**（IPP 端口关闭或 HTTP 请求超时），则可能是打印机进入了深度睡眠状态或已关闭。请通知用户手动检查或唤醒打印机。