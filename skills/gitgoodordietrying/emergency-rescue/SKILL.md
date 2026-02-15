---
name: emergency-rescue
description: **从开发人员引发的灾难中恢复**  
当遇到以下情况时，请使用此方案：  
- 有人将代码强制推送到主分支（main branch）；  
- Git 中的凭据被泄露；  
- 磁盘空间耗尽；  
- 错误地终止了某个进程；  
- 数据库被损坏；  
- 部署失败；  
- 用户因操作失误而无法通过 SSH 进入系统；  
- 在执行错误的 `rebase` 操作后丢失了提交记录；  
- 或者遇到任何其他需要立即、冷静且按步骤处理的紧急情况。  

**使用步骤：**  
1. 保持冷静，分析问题的根本原因。  
2. 根据具体情况，采取相应的恢复措施（例如：重新配置 Git 仓库、恢复数据库数据、重新启动相关服务、修复系统错误等）。  
3. 如果需要，记录整个恢复过程，以便将来参考。  

**注意：**  
- 请确保在恢复过程中遵循最佳实践和团队规范，以避免类似问题的再次发生。  
- 如有疑问，请及时向团队成员或技术支持人员寻求帮助。
metadata: {"clawdbot":{"emoji":"🚨","requires":{"anyBins":["git","bash"]},"os":["linux","darwin","win32"]}}
---

# 紧急救援工具包

本工具包提供了针对开发者工作中可能遇到的各种紧急情况的逐步恢复流程。所有流程都遵循相同的步骤：**诊断 → 修复 → 验证**。默认情况下，执行的命令都是非破坏性的；具有破坏性的操作会特别标明。

当出现问题时，请根据实际情况选择相应的流程并按顺序执行操作。

## 使用场景

- 有人强制推送代码到主分支（main）并覆盖了历史记录
- 凭据被提交到了公共仓库
- 使用 `git rebase` 或 `git reset --hard` 操作导致某些提交丢失
- 磁盘空间已满，导致系统无法正常运行
- 某个进程占用过多内存或无法终止
- 数据库迁移中途失败
- 需要立即回滚部署
- SSH 访问被锁定
- 生产环境中的 SSL 证书已过期
- 无法确定问题所在，但系统明显出现故障

---

## Git 相关紧急情况

### 强制推送代码到主分支（或任何共享分支）

有人执行了 `git push --force`，导致远程仓库的历史记录被覆盖。

```bash
# DIAGNOSE: Check the reflog on any machine that had the old state
git reflog show origin/main
# Look for the last known-good commit hash

# FIX (if you have the old state locally):
git push origin <good-commit-hash>:main --force-with-lease
# --force-with-lease is safer than --force: it fails if remote changed again

# FIX (if you DON'T have the old state locally):
# GitHub/GitLab retain force-pushed refs temporarily

# GitHub: check the "push" event in the audit log or use the API
gh api repos/{owner}/{repo}/events --jq '.[] | select(.type=="PushEvent") | .payload.before'

# GitLab: check the reflog on the server (admin access needed)
# Or restore from any CI runner or team member's local clone

# VERIFY:
git log --oneline -10 origin/main
# Confirm the history looks correct
```

### 使用 `git rebase` 或 `git reset --hard` 后提交丢失

执行 `git rebase` 或 `git reset --hard` 后，部分提交被删除。

```bash
# DIAGNOSE: Your commits are NOT gone. Git keeps everything for 30+ days.
git reflog
# Find the commit hash from BEFORE the rebase/reset
# Look for entries like "rebase (start)" or "reset: moving to"

# FIX: Reset back to the pre-disaster state
git reset --hard <commit-hash-before-disaster>

# FIX (alternative): Cherry-pick specific lost commits
git cherry-pick <lost-commit-hash>

# FIX (if reflog is empty — rare, usually means different repo):
git fsck --lost-found
# Look in .git/lost-found/commit/ for dangling commits
ls .git/lost-found/commit/
git show <hash>  # Inspect each one

# VERIFY:
git log --oneline -10
# Your commits should be back
```

### 提交到了错误的分支

在主分支（main）上进行了本应提交到功能分支（feature branch）的修改。

```bash
# DIAGNOSE: Check where you are and what you committed
git log --oneline -5
git branch

# FIX: Create the feature branch at current position, then reset main
git branch feature-branch          # Create branch pointing at current commit
git reset --hard HEAD~<N>          # Move main back N commits (⚠️ destructive)
git checkout feature-branch        # Switch to the new branch

# FIX (safer alternative using cherry-pick):
git checkout -b feature-branch     # Create and switch to new branch
git checkout main
git reset --hard origin/main       # Reset main to remote state
# Your commits are safely on feature-branch

# VERIFY:
git log --oneline main -5
git log --oneline feature-branch -5
```

### 合并操作失败（出现冲突，结果错误）

合并操作导致错误结果，需要重新开始。

```bash
# FIX (merge not yet committed — still in conflict state):
git merge --abort

# FIX (merge was committed but not pushed):
git reset --hard HEAD~1

# FIX (merge was already pushed): Create a revert commit
git revert -m 1 <merge-commit-hash>
# -m 1 means "keep the first parent" (your branch before merge)
git push

# VERIFY:
git log --oneline --graph -10
git diff HEAD~1  # Review what changed
```

### Git 仓库损坏

Git 命令执行失败，提示“对象损坏”（bad object）或“链接失效”（broken link）等错误。

```bash
# DIAGNOSE: Check repository integrity
git fsck --full

# FIX (if remote is intact — most common):
# Save any uncommitted work first
cp -r . ../repo-backup

# Re-clone and restore local work
cd ..
git clone <remote-url> repo-fresh
cp -r repo-backup/path/to/uncommitted/files repo-fresh/

# FIX (repair without re-cloning):
# Remove corrupt objects and fetch them again
git fsck --full 2>&1 | grep "corrupt\|missing" | awk '{print $NF}'
# For each corrupt object:
rm .git/objects/<first-2-chars>/<remaining-hash>
git fetch origin  # Re-download from remote

# VERIFY:
git fsck --full  # Should report no errors
git log --oneline -5
```

---

## 凭据泄露

### 重要信息被提交到了 Git 仓库（API 密钥、密码、访问令牌）

敏感信息被记录在 Git 历史记录中。时间非常紧迫——自动化监控工具会实时扫描公共 GitHub 仓库以检测泄露的凭证。

```bash
# STEP 1: REVOKE THE CREDENTIAL IMMEDIATELY
# Do this FIRST, before cleaning git history.
# The credential is already compromised the moment it was pushed publicly.

# AWS keys:
aws iam delete-access-key --access-key-id AKIAXXXXXXXXXXXXXXXX --user-name <user>
# Then create a new key pair

# GitHub tokens:
# Go to github.com → Settings → Developer settings → Tokens → Revoke

# Database passwords:
# Change the password in the database immediately
# ALTER USER myuser WITH PASSWORD 'new-secure-password';

# Generic API tokens:
# Revoke in the provider's dashboard, generate new ones

# STEP 2: Remove from current branch
git rm --cached <file-with-secret>    # If the whole file is secret
# OR edit the file to remove the secret, then:
git add <file>

# STEP 3: Add to .gitignore
echo ".env" >> .gitignore
echo "credentials.json" >> .gitignore
git add .gitignore

# STEP 4: Remove from git history (⚠️ rewrites history)
# Option A: git-filter-repo (recommended, install with pip install git-filter-repo)
git filter-repo --path <file-with-secret> --invert-paths

# Option B: BFG Repo Cleaner (faster for large repos)
# Download from https://rtyley.github.io/bfg-repo-cleaner/
java -jar bfg.jar --delete-files <filename> .
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# STEP 5: Force push the cleaned history
git push origin --force --all
git push origin --force --tags

# STEP 6: Notify all collaborators to re-clone
# Their local copies still have the secret in reflog

# VERIFY:
git log --all -p -S '<the-secret-string>' --diff-filter=A
# Should return nothing
```

### `.env` 文件被提交到了公共仓库

配置文件 `.env` 被意外提交到了公共仓库。

```bash
# STEP 1: Revoke ALL credentials in that .env file. All of them. Now.

# STEP 2: Remove and ignore
git rm --cached .env
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Remove .env from tracking"

# STEP 3: Remove from history (see credential removal above)
git filter-repo --path .env --invert-paths

# STEP 4: Check what was exposed
# List every variable that was in the .env:
git show HEAD~1:.env 2>/dev/null || git log --all -p -- .env | head -50
# Rotate every single value.

# PREVENTION: Add a pre-commit hook
cat > .git/hooks/pre-commit << 'HOOK'
#!/bin/bash
if git diff --cached --name-only | grep -qE '\.env$|\.env\.local$|credentials'; then
    echo "ERROR: Attempting to commit potential secrets file"
    echo "Files: $(git diff --cached --name-only | grep -E '\.env|credentials')"
    exit 1
fi
HOOK
chmod +x .git/hooks/pre-commit
```

### 机密信息出现在持续集成/持续部署（CI/CD）日志中

机密信息被记录在 CI/CD 日志中。

```bash
# STEP 1: Revoke the credential immediately

# STEP 2: Delete the CI run/logs if possible
# GitHub Actions:
gh run delete <run-id>
# Or: Settings → Actions → delete specific run

# STEP 3: Fix the pipeline
# Never echo secrets. Mask them:
# GitHub Actions: echo "::add-mask::$MY_SECRET"
# GitLab CI: variables are masked if marked as "Masked" in settings

# STEP 4: Audit what was exposed
# Check the log output for patterns like:
# AKIAXXXXXXXXX (AWS)
# ghp_XXXXXXXXX (GitHub)
# sk-XXXXXXXXXXX (OpenAI/Stripe)
# Any connection strings with passwords
```

## 磁盘空间不足的紧急情况

### 系统或容器磁盘空间已满

系统无法正常运行：构建任务失败，日志无法记录，服务崩溃。

```bash
# DIAGNOSE: What's using space?
df -h                          # Which filesystem is full?
du -sh /* 2>/dev/null | sort -rh | head -20    # Biggest top-level dirs
du -sh /var/log/* | sort -rh | head -10        # Log bloat?

# QUICK WINS (safe to run immediately):

# 1. Docker cleanup (often the #1 cause)
docker system df               # See Docker disk usage
docker system prune -a -f      # Remove all unused images, containers, networks
docker volume prune -f          # Remove unused volumes
docker builder prune -a -f      # Remove build cache
# ⚠️ This removes ALL unused Docker data. Safe if you can re-pull/rebuild.

# 2. Package manager caches
# npm
npm cache clean --force
rm -rf ~/.npm/_cacache

# pip
pip cache purge

# apt
sudo apt-get clean
sudo apt-get autoremove -y

# brew
brew cleanup --prune=all

# 3. Log rotation (immediate)
# Truncate (not delete) large log files to free space instantly
sudo truncate -s 0 /var/log/syslog
sudo truncate -s 0 /var/log/journal/*/*.journal  # systemd journals
find /var/log -name "*.log" -size +100M -exec truncate -s 0 {} \;
# Truncate preserves the file handle so services don't break

# 4. Old build artifacts
find . -name "node_modules" -type d -prune -exec rm -rf {} + 2>/dev/null
find . -name ".next" -type d -exec rm -rf {} + 2>/dev/null
find . -name "dist" -type d -exec rm -rf {} + 2>/dev/null
find /tmp -type f -mtime +7 -delete 2>/dev/null

# 5. Find the actual culprit
find / -xdev -type f -size +100M -exec ls -lh {} \; 2>/dev/null | sort -k5 -rh | head -20
# Shows files over 100MB, sorted by size

# VERIFY:
df -h  # Check free space increased
```

### Docker 容器磁盘空间不足

Docker 容器内的磁盘空间已满，导致容器无法启动。

```bash
# DIAGNOSE:
docker system df -v

# Common culprits:
# 1. Dangling images from builds
docker image prune -f

# 2. Stopped containers accumulating
docker container prune -f

# 3. Build cache (often the biggest)
docker builder prune -a -f

# 4. Volumes from old containers
docker volume ls -qf dangling=true
docker volume prune -f

# NUCLEAR OPTION (⚠️ removes EVERYTHING):
docker system prune -a --volumes -f
# You will need to re-pull all images and recreate all volumes

# VERIFY:
docker system df
df -h
```

## 进程相关紧急情况

### 端口已被占用

某个端口已被其他进程占用。

```bash
# DIAGNOSE: What's using the port?
# Linux:
lsof -i :8080
ss -tlnp | grep 8080
# macOS:
lsof -i :8080
# Windows:
netstat -ano | findstr :8080

# FIX: Kill the process
kill $(lsof -t -i :8080)           # Graceful
kill -9 $(lsof -t -i :8080)       # Force (if graceful didn't work)

# FIX (Windows):
# Find PID from netstat output, then:
taskkill /PID <pid> /F

# FIX (if it's a leftover Docker container):
docker ps | grep 8080
docker stop <container-id>

# VERIFY:
lsof -i :8080  # Should return nothing
```

### 进程无法终止

某个进程无法正常终止。

```bash
# DIAGNOSE:
ps aux | grep <process-name>
# Note the PID

# ESCALATION LADDER:
kill <pid>                # SIGTERM (graceful shutdown)
sleep 5
kill -9 <pid>             # SIGKILL (cannot be caught, immediate death)

# If SIGKILL doesn't work, it's a zombie or kernel-stuck process:
# Check if zombie:
ps aux | grep <pid>
# State "Z" = zombie. The parent must reap it:
kill -SIGCHLD $(ps -o ppid= -p <pid>)
# Or kill the parent process

# If truly stuck in kernel (state "D"):
# Only a reboot will fix it. The process is stuck in an I/O syscall.

# MASS CLEANUP: Kill all processes matching a name
pkill -f <pattern>          # Graceful
pkill -9 -f <pattern>      # Force
```

### 内存不足（操作系统触发 OOM）

系统因内存不足而自动关闭进程。

```bash
# DIAGNOSE: Was your process OOM-killed?
dmesg | grep -i "oom\|killed process" | tail -20
journalctl -k | grep -i "oom\|killed" | tail -20

# Check what's using memory right now:
ps aux --sort=-%mem | head -20        # Top memory consumers
free -h                                 # System memory overview

# FIX: Free memory immediately
# 1. Kill the biggest consumer (if safe to do so)
kill $(ps aux --sort=-%mem | awk 'NR==2{print $2}')

# 2. Drop filesystem caches (safe, no data loss)
sync && echo 3 | sudo tee /proc/sys/vm/drop_caches

# 3. Disable swap thrashing (if swap is full)
sudo swapoff -a && sudo swapon -a

# PREVENT: Set memory limits
# Docker:
docker run --memory=512m --memory-swap=1g myapp

# Systemd service:
# Add to [Service] section:
# MemoryMax=512M
# MemoryHigh=400M

# Node.js:
node --max-old-space-size=512 app.js

# VERIFY:
free -h
ps aux --sort=-%mem | head -5
```

## 数据库相关紧急情况

### 迁移操作失败（部分数据未正确应用）

数据库迁移操作失败，导致数据不一致。

```bash
# DIAGNOSE: What state is the database in?
# Check which migrations have run:

# Rails:
rails db:migrate:status

# Django:
python manage.py showmigrations

# Knex/Node:
npx knex migrate:status

# Prisma:
npx prisma migrate status

# Raw SQL — check migration table:
# PostgreSQL/MySQL:
SELECT * FROM schema_migrations ORDER BY version DESC LIMIT 10;
# Or: SELECT * FROM _migrations ORDER BY id DESC LIMIT 10;

# FIX: Roll back the failed migration
# Most frameworks track migration state. Roll back to last good state:

# Rails:
rails db:rollback STEP=1

# Django:
python manage.py migrate <app_name> <previous_migration_number>

# Knex:
npx knex migrate:rollback

# FIX (manual): If the framework is confused about state:
# 1. Check what the migration actually did
# 2. Manually undo partial changes
# 3. Delete the migration record from the migrations table
# 4. Fix the migration code
# 5. Re-run

# VERIFY:
# Run the migration again and confirm it applies cleanly
# Check the affected tables/columns exist correctly
```

### 误删除了表或整个数据库

不小心删除了数据库中的表或整个数据库。

```bash
# PostgreSQL:
# If you have WAL archiving / point-in-time recovery configured:
pg_restore -d mydb /backups/latest.dump -t dropped_table

# If no backup exists, check if the transaction is still open:
# (Only works if you haven't committed yet)
# Just run ROLLBACK; in your SQL session.

# MySQL:
# If binary logging is enabled:
mysqlbinlog /var/log/mysql/mysql-bin.000001 \
  --start-datetime="2026-02-03 10:00:00" \
  --stop-datetime="2026-02-03 10:30:00" > recovery.sql
# Review recovery.sql, then apply

# SQLite:
# If the file still exists, it's fine — SQLite DROP TABLE is within the file
# Restore from backup:
cp /backups/db.sqlite3 ./db.sqlite3

# PREVENTION: Always run destructive SQL in a transaction
BEGIN;
DROP TABLE users;  -- oops
ROLLBACK;          -- saved
```

### 数据库被锁定或出现死锁

数据库操作被阻塞，无法正常访问。

```bash
# PostgreSQL:
-- Find blocking queries
SELECT pid, usename, state, query, wait_event_type, query_start
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_start;

-- Find locks
SELECT blocked_locks.pid AS blocked_pid,
       blocking_locks.pid AS blocking_pid,
       blocked_activity.query AS blocked_query,
       blocking_activity.query AS blocking_query
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;

-- Kill blocking query
SELECT pg_terminate_backend(<blocking_pid>);

# MySQL:
SHOW PROCESSLIST;
SHOW ENGINE INNODB STATUS\G  -- Look for "LATEST DETECTED DEADLOCK"
KILL <process_id>;

# SQLite:
# SQLite uses file-level locking. Common fix:
# 1. Find and close all connections
# 2. Check for .db-journal or .db-wal files (active transactions)
# 3. If stuck: cp database.db database-fixed.db && mv database-fixed.db database.db
# This forces SQLite to release the lock by creating a fresh file handle

# VERIFY:
# Run a simple query to confirm database is responsive
SELECT 1;
```

### 连接池耗尽

数据库连接池中的连接资源被耗尽。

```bash
# DIAGNOSE:
# Error messages like: "too many connections", "connection pool exhausted",
# "FATAL: remaining connection slots are reserved for superuser"

# PostgreSQL — check connection count:
SELECT count(*), state FROM pg_stat_activity GROUP BY state;
SELECT max_conn, used, max_conn - used AS available
FROM (SELECT count(*) AS used FROM pg_stat_activity) t,
     (SELECT setting::int AS max_conn FROM pg_settings WHERE name='max_connections') m;

# FIX: Kill idle connections
-- Terminate idle connections older than 5 minutes
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
AND query_start < now() - interval '5 minutes';

# FIX: Increase max connections (requires restart)
# postgresql.conf:
# max_connections = 200  (default is 100)

# BETTER FIX: Use a connection pooler
# PgBouncer or pgcat in front of PostgreSQL
# Application-level: set pool size to match your needs
# Node.js (pg): { max: 20 }
# Python (SQLAlchemy): pool_size=20, max_overflow=10
# Go (database/sql): db.SetMaxOpenConns(20)

# VERIFY:
SELECT count(*) FROM pg_stat_activity;
# Should be well below max_connections
```

## 部署相关紧急情况

### 快速回滚部署

需要立即回滚刚刚完成的部署操作。

```bash
# Git-based deploys:
git log --oneline -5 origin/main
git revert HEAD                    # Create a revert commit
git push origin main               # Deploy the revert
# Revert is safer than reset because it preserves history

# Docker/container deploys:
# Roll back to previous image tag
docker pull myapp:previous-tag
docker stop myapp-current
docker run -d --name myapp myapp:previous-tag

# Kubernetes:
kubectl rollout undo deployment/myapp
kubectl rollout status deployment/myapp    # Watch rollback progress

# Heroku:
heroku releases
heroku rollback v<previous-version>

# AWS ECS:
aws ecs update-service --cluster mycluster --service myservice \
  --task-definition myapp:<previous-revision>

# VERIFY:
# Hit the health check endpoint
curl -s -o /dev/null -w "%{http_code}" https://myapp.example.com/health
# Should return 200
```

### 容器无法启动

Docker 容器无法正常启动。

```bash
# DIAGNOSE: Why did it fail?
docker logs <container-id> --tail 100
docker inspect <container-id> | grep -A5 "State"

# Common causes and fixes:

# 1. "exec format error" — wrong platform (built for arm64, running on amd64)
docker build --platform linux/amd64 -t myapp .

# 2. "permission denied" — file not executable or wrong user
# In Dockerfile:
RUN chmod +x /app/entrypoint.sh
# Or: USER root before the command, then drop back

# 3. "port already allocated" — another container or process on that port
docker ps -a | grep <port>
docker stop <conflicting-container>

# 4. "no such file or directory" — entrypoint or CMD path is wrong
docker run -it --entrypoint sh myapp  # Get a shell to debug
ls -la /app/                           # Check what's actually there

# 5. Healthcheck failing → container keeps restarting
docker inspect <container-id> --format='{{json .State.Health}}'
# Temporarily disable healthcheck to get logs:
docker run --no-healthcheck myapp

# 6. Out of memory — container OOM killed
docker inspect <container-id> --format='{{.State.OOMKilled}}'
# If true: docker run --memory=1g myapp

# VERIFY:
docker ps  # Container should show "Up" status
docker logs <container-id> --tail 5  # No errors
```

### SSL 证书过期

SSL 证书已过期，导致连接失败。

```bash
# DIAGNOSE: Check certificate expiry
echo | openssl s_client -connect mysite.com:443 -servername mysite.com 2>/dev/null | \
  openssl x509 -noout -dates
# notAfter shows expiry date

# FIX (Let's Encrypt — most common):
sudo certbot renew --force-renewal
sudo systemctl reload nginx   # or: sudo systemctl reload apache2

# FIX (manual certificate):
# 1. Get new certificate from your CA
# 2. Replace files:
sudo cp new-cert.pem /etc/ssl/certs/mysite.pem
sudo cp new-key.pem /etc/ssl/private/mysite.key
# 3. Reload web server
sudo nginx -t && sudo systemctl reload nginx

# FIX (AWS ACM):
# ACM auto-renews if DNS validation is configured.
# If email validation: check the admin email for renewal link
# If stuck: request a new certificate in ACM and update the load balancer

# PREVENTION: Auto-renewal with monitoring
# Cron job to check expiry and alert:
echo '0 9 * * 1 echo | openssl s_client -connect mysite.com:443 2>/dev/null | openssl x509 -checkend 604800 -noout || echo "CERT EXPIRES WITHIN 7 DAYS" | mail -s "SSL ALERT" admin@example.com' | crontab -

# VERIFY:
curl -sI https://mysite.com | head -5
# Should return HTTP/2 200, not certificate errors
```

## 访问权限相关紧急情况

### SSH 访问被锁定

SSH 访问被阻止，无法正常登录系统。

```bash
# DIAGNOSE: Why can't you connect?
ssh -vvv user@host  # Verbose output shows where it fails

# Common causes:

# 1. Key not accepted — wrong key, permissions, or authorized_keys issue
ssh -i ~/.ssh/specific_key user@host  # Try explicit key
chmod 600 ~/.ssh/id_rsa               # Fix key permissions
chmod 700 ~/.ssh                       # Fix .ssh dir permissions

# 2. "Connection refused" — sshd not running or firewall blocking
# If you have console access (cloud provider's web console):
sudo systemctl start sshd
sudo systemctl status sshd

# 3. Firewall blocking port 22
# Cloud console:
sudo ufw allow 22/tcp       # Ubuntu
sudo firewall-cmd --add-service=ssh --permanent && sudo firewall-cmd --reload  # CentOS

# 4. Changed SSH port and forgot
# Try common alternate ports:
ssh -p 2222 user@host
ssh -p 22222 user@host
# Or check from console: grep -i port /etc/ssh/sshd_config

# 5. IP changed / DNS stale
ping hostname    # Verify IP resolution
ssh user@<direct-ip>  # Try IP instead of hostname

# 6. Locked out after too many attempts (fail2ban)
# From console:
sudo fail2ban-client set sshd unbanip <your-ip>
# Or wait for the ban to expire (usually 10 min)

# CLOUD PROVIDER ESCAPE HATCHES:
# AWS: EC2 → Instance → Connect → Session Manager (no SSH needed)
# GCP: Compute → VM instances → SSH (browser-based)
# Azure: VM → Serial console
# DigitalOcean: Droplet → Access → Console

# VERIFY:
ssh user@host echo "connection works"
```

### sudo 权限丢失

用户失去了 `sudo` 权限，无法执行管理命令。

```bash
# If you have physical/console access:
# 1. Boot into single-user/recovery mode
#    - Reboot, hold Shift (GRUB), select "recovery mode"
#    - Or add init=/bin/bash to kernel command line

# 2. Remount filesystem read-write
mount -o remount,rw /

# 3. Fix sudo access
usermod -aG sudo <username>    # Debian/Ubuntu
usermod -aG wheel <username>   # CentOS/RHEL
# Or edit directly:
visudo
# Add: username ALL=(ALL:ALL) ALL

# 4. Reboot normally
reboot

# If you have another sudo/root user:
su - other-admin
sudo usermod -aG sudo <locked-user>

# CLOUD: Use the provider's console or reset the instance
# AWS: Create an AMI, launch new instance, mount old root volume, fix
```

## 网络相关紧急情况

### 全局网络故障

整个网络无法正常通信。

```bash
# DIAGNOSE: Isolate the layer
# 1. Is the network interface up?
ip addr show         # or: ifconfig
ping 127.0.0.1       # Loopback works?

# 2. Can you reach the gateway?
ip route | grep default
ping <gateway-ip>

# 3. Can you reach the internet by IP?
ping 8.8.8.8          # Google DNS
ping 1.1.1.1          # Cloudflare DNS

# 4. Is DNS working?
nslookup google.com
dig google.com

# DECISION TREE:
# ping 127.0.0.1 fails      → network stack broken, restart networking
# ping gateway fails         → local network issue (cable, wifi, DHCP)
# ping 8.8.8.8 fails        → routing/firewall issue
# ping 8.8.8.8 works but    → DNS issue
#   nslookup fails

# FIX: DNS broken
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
# Or: sudo systemd-resolve --flush-caches

# FIX: Interface down
sudo ip link set eth0 up
sudo dhclient eth0        # Request new DHCP lease

# FIX: Restart networking entirely
sudo systemctl restart NetworkManager    # Desktop Linux
sudo systemctl restart networking        # Server
sudo systemctl restart systemd-networkd  # Systemd-based

# Docker: Container can't reach the internet
docker run --rm alpine ping 8.8.8.8  # Test from container
# If fails:
sudo systemctl restart docker    # Often fixes Docker networking
# Or: docker network prune
```

### DNS 更新失败

DNS 服务器无法正确更新域名解析信息。

```bash
# DIAGNOSE: Check what different DNS servers see
dig @8.8.8.8 mysite.com        # Google
dig @1.1.1.1 mysite.com        # Cloudflare
dig @ns1.yourdns.com mysite.com # Authoritative nameserver

# Check TTL (time remaining before caches expire):
dig mysite.com | grep -i ttl

# REALITY CHECK:
# DNS propagation takes time. TTL controls this.
# TTL 300 = 5 minutes. TTL 86400 = 24 hours.
# You cannot speed this up. You can only wait.

# FIX: If authoritative nameserver has wrong records
# Update the record at your DNS provider (Cloudflare, Route53, etc.)
# Then flush your local cache:
# macOS:
sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder
# Linux:
sudo systemd-resolve --flush-caches
# Windows:
ipconfig /flushdns

# WORKAROUND: While waiting for propagation
# Add to /etc/hosts for immediate local effect:
echo "93.184.216.34 mysite.com" | sudo tee -a /etc/hosts
# Remove this after propagation completes!

# VERIFY:
dig +short mysite.com  # Should show new IP/record
```

## 文件相关紧急情况

### 误删文件（未保存在 Git 仓库中）

文件被意外删除，但未保存在 Git 仓库中。

```bash
# DIAGNOSE: Are the files recoverable?

# If the process still has the file open:
lsof | grep deleted
# Then recover from /proc:
cp /proc/<pid>/fd/<fd-number> /path/to/restored-file

# If recently deleted on ext4 (Linux):
# Install extundelete or testdisk
sudo extundelete /dev/sda1 --restore-file path/to/file
# Or use testdisk interactively for a better UI

# macOS:
# Check Trash first: ~/.Trash/
# Time Machine: tmutil restore /path/to/file

# PREVENTION:
# Use trash-cli instead of rm:
# npm install -g trash-cli
# trash file.txt  (moves to trash instead of permanent delete)
# Or alias: alias rm='echo "Use trash instead"; false'
```

### 权限设置错误

文件权限被错误地应用到了整个目录或文件上。

```bash
# "I ran chmod -R 777 /" or "chmod -R 000 /important/dir"

# FIX: Common default permissions
# For a web project:
find /path -type d -exec chmod 755 {} \;  # Directories: rwxr-xr-x
find /path -type f -exec chmod 644 {} \;  # Files: rw-r--r--
find /path -name "*.sh" -exec chmod 755 {} \;  # Scripts: executable

# For SSH:
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
chmod 600 ~/.ssh/authorized_keys
chmod 644 ~/.ssh/config

# For a system directory (⚠️ serious — may need rescue boot):
# If /etc permissions are broken:
# Boot from live USB, mount the drive, fix permissions
# Reference: dpkg --verify (Debian) or rpm -Va (RHEL) to compare against package defaults

# VERIFY:
ls -la /path/to/fixed/directory
```

## 通用诊断工具

当无法确定问题所在时，可以运行以下诊断命令：

```bash
#!/bin/bash
# emergency-diagnostic.sh — Quick system health check

echo "=== DISK ==="
df -h | grep -E '^/|Filesystem'

echo -e "\n=== MEMORY ==="
free -h

echo -e "\n=== CPU / LOAD ==="
uptime

echo -e "\n=== TOP PROCESSES (by CPU) ==="
ps aux --sort=-%cpu | head -6

echo -e "\n=== TOP PROCESSES (by MEM) ==="
ps aux --sort=-%mem | head -6

echo -e "\n=== NETWORK ==="
ping -c 1 -W 2 8.8.8.8 > /dev/null 2>&1 && echo "Internet: OK" || echo "Internet: UNREACHABLE"
ping -c 1 -W 2 $(ip route | awk '/default/{print $3}') > /dev/null 2>&1 && echo "Gateway: OK" || echo "Gateway: UNREACHABLE"

echo -e "\n=== RECENT ERRORS ==="
journalctl -p err --since "1 hour ago" --no-pager | tail -20 2>/dev/null || \
  dmesg | tail -20

echo -e "\n=== DOCKER (if running) ==="
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "Docker not running"
docker system df 2>/dev/null || true

echo -e "\n=== LISTENING PORTS ==="
ss -tlnp 2>/dev/null | head -15 || netstat -tlnp 2>/dev/null | head -15

echo -e "\n=== FAILED SERVICES ==="
systemctl --failed 2>/dev/null || true
```

运行该命令后，请查看输出结果，然后根据输出内容跳转到相应的处理流程。

## 提示

- **在清理 Git 历史记录之前，先撤销相关凭证。** 一旦敏感信息被公开提交，自动化监控工具会在几分钟内发现。虽然清理历史记录很重要，但撤销凭证是更紧迫的任务。
- **`git reflog` 是你的“撤销按钮”。** 它会记录过去 30 天内的所有分支切换记录（HEAD 的移动历史）。如果提交了错误的提交或执行了错误的 `git rebase` 操作，`git reflog` 中会保存相应的恢复操作信息。学会如何使用它。
- **截断日志文件，而不是直接删除它们。** 使用 `truncate -s 0 file.log` 可以立即释放磁盘空间，同时保留文件的打开状态。如果进程仍在使用该日志文件，直接删除会导致空间无法立即释放。
- **始终使用 `--force-with-lease` 而不是 `--force`。** 这个选项可以防止在他人已经推送代码的情况下覆盖他们的修改。
- **每个恢复操作都应包含验证步骤。** 运行诊断命令后，务必检查输出结果，确认修复操作是否有效。切勿盲目相信结果。
- **Docker 是开发者机器上最大的磁盘空间占用者。** 在开发环境中，执行 `docker system prune -a` 命令通常很安全，可以释放大量磁盘空间。
- **在处理数据库紧急情况时，将具有破坏性的操作封装在事务中。** 使用 `BEGIN; DROP TABLE users; ROLLBACK;` 可以确保数据安全。记住这个操作的重要性。
- **当 SSH 访问被锁定时，每个云服务提供商都提供了相应的应急解决方案。** AWS 提供了 Session Manager，GCP 提供了浏览器 SSH 连接，Azure 提供了 Serial Console。在需要使用这些工具之前，请先了解它们的使用方法。
- **操作顺序至关重要：诊断 → 修复 → 验证。** 跳过诊断步骤可能会导致错误的修复；跳过验证步骤则可能导致错误的判断。务必严格按照这个顺序操作。
- **请确保这个工具包始终安装在你的开发环境中。** 在大多数情况下你可能用不到它，但一旦需要时，它会立刻派上用场。