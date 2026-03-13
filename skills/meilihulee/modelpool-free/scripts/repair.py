#!/usr/bin/env python3
"""
ModelPool Repair — One-click diagnostics and fix for OpenClaw model issues.
"""

import json
import os
import subprocess
import sys
import time
import urllib.request
import ssl

CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")
SSL_CTX = ssl.create_default_context()


def log(msg):
    print(f"  {msg}", flush=True)


def run(cmd, timeout=30):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip(), r.returncode
    except subprocess.TimeoutExpired:
        return "TIMEOUT", -1
    except Exception:
        return "", -1


def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        log("❌ Config file not found. Run 'openclaw daemon start' first.")
        sys.exit(1)
    except json.JSONDecodeError:
        log("❌ Config file corrupted. Will attempt fix in step 3.")
        return {"models": {"providers": {}}, "agents": {"defaults": {}}}


def save_config(config):
    # Backup before writing
    backup_path = CONFIG_PATH + ".bak"
    if os.path.isfile(CONFIG_PATH):
        import shutil
        shutil.copy2(CONFIG_PATH, backup_path)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def step1_diagnose():
    """Basic diagnostics."""
    print("\n📋 [1/7] Diagnostics...")
    issues = 0

    out, _ = run("ss -tlnp | grep 18789")
    if "18789" in out:
        log("✅ Gateway port 18789 listening")
    else:
        log("❌ Gateway port 18789 NOT listening")
        issues += 1

    out, _ = run("openclaw config validate 2>&1")
    if "valid" in out.lower() and "invalid" not in out.lower():
        log("✅ Config file valid")
    else:
        log("❌ Config file invalid")
        issues += 1

    out, _ = run("free -m | awk '/Mem:/{print $4}'")
    try:
        free_mb = int(out.strip())
        if free_mb < 200:
            log(f"⚠️  Low memory: {free_mb}MB free")
            issues += 1
        else:
            log(f"✅ Memory OK: {free_mb}MB free")
    except:
        pass

    out, _ = run("df / | tail -1 | awk '{print $5}' | tr -d '%'")
    try:
        usage = int(out.strip())
        if usage > 90:
            log(f"⚠️  Disk usage: {usage}%")
            issues += 1
        else:
            log(f"✅ Disk OK: {usage}%")
    except:
        pass

    return issues


def step2_test_apis():
    """Test all provider APIs."""
    print("\n📋 [2/7] Testing model API connectivity...")
    dead = []

    try:
        config = load_config()
    except:
        log("❌ Cannot read config")
        return dead

    providers = config.get("models", {}).get("providers", {})
    for name, info in providers.items():
        base_url = info.get("baseUrl", "")
        api_key = info.get("apiKey", "")
        models = info.get("models", [])
        if not models:
            continue
        model_id = models[0].get("id", "")
        url = base_url.rstrip("/") + "/chat/completions"

        try:
            req = urllib.request.Request(url, headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }, data=json.dumps({
                "model": model_id,
                "messages": [{"role": "user", "content": "hi"}],
                "max_tokens": 5
            }).encode())
            resp = urllib.request.urlopen(req, context=SSL_CTX, timeout=15)
            r = json.loads(resp.read())
            if r.get("choices"):
                log(f"✅ {name}/{model_id}")
            else:
                log(f"⚠️  {name}/{model_id} — empty response")
                dead.append(name)
        except Exception as e:
            log(f"❌ {name}/{model_id} — {str(e)[:50]}")
            dead.append(name)

    if dead:
        log(f"\n⚠️  {len(dead)} provider(s) unavailable")
    else:
        log(f"\n✅ All providers OK")
    return dead


def step3_fix_config():
    """Fix config with doctor."""
    print("\n📋 [3/7] Fixing config...")
    run("openclaw doctor --fix 2>&1")
    log("✅ doctor --fix executed")


def step4_clean_sessions():
    """Clean stuck sessions."""
    print("\n📋 [4/7] Cleaning stuck sessions...")
    out, _ = run("openclaw sessions cleanup 2>&1")
    log(f"✅ {out.split(chr(10))[-1] if out else 'Sessions cleaned'}")


def step5_rebuild_fallback(dead_providers):
    """Rebuild fallback chain, skip dead providers."""
    print("\n📋 [5/7] Rebuilding fallback chain...")
    try:
        config = load_config()
    except:
        log("❌ Cannot read config")
        return

    model_config = config.get("agents", {}).get("defaults", {}).get("model", {})
    if isinstance(model_config, str):
        model_config = {"primary": model_config, "fallbacks": []}

    primary = model_config.get("primary", "")
    fallbacks = model_config.get("fallbacks", [])
    dead_set = set(dead_providers)

    # Check if primary is dead
    primary_provider = primary.split("/")[0] if "/" in primary else ""
    if primary_provider in dead_set:
        log(f"⚠️  Primary {primary} is dead, finding replacement...")
        new_primary = None
        new_fallbacks = []
        for fb in fallbacks:
            fb_provider = fb.split("/")[0] if "/" in fb else ""
            if fb_provider not in dead_set and new_primary is None:
                new_primary = fb
            else:
                new_fallbacks.append(fb)
        if new_primary:
            new_fallbacks.append(primary)  # Keep old primary as last resort
            model_config["primary"] = new_primary
            model_config["fallbacks"] = new_fallbacks
            log(f"✅ Switched to: {new_primary}")
        else:
            log("❌ All models dead, keeping current config")
    else:
        log(f"✅ Primary {primary} is alive")

    config["agents"]["defaults"]["model"] = model_config
    save_config(config)
    log(f"📊 Chain: {model_config['primary']} + {len(model_config.get('fallbacks', []))} fallbacks")


def step6_cleanup():
    """Clean resources."""
    print("\n📋 [6/7] Cleaning resources...")
    out, _ = run("free -m | awk '/Mem:/{print $4}'")
    try:
        if int(out.strip()) < 200:
            run("sync; echo 3 > /proc/sys/vm/drop_caches 2>/dev/null")
            log("✅ Memory cache cleared")
    except:
        pass

    run("find /tmp/openclaw -name '*.log' -mtime +3 -delete 2>/dev/null")
    log("✅ Old logs cleaned")


def step7_restart():
    """Full restart."""
    print("\n📋 [7/7] Restarting OpenClaw...")
    run("openclaw daemon stop 2>&1")
    time.sleep(3)
    run("killall -9 node 2>/dev/null")
    time.sleep(3)
    run("openclaw daemon start 2>&1")
    time.sleep(15)

    out, _ = run("ss -tlnp | grep 18789")
    if "18789" in out:
        log("✅ Gateway running")
    else:
        log("❌ Gateway still down")

    out, _ = run("openclaw config validate 2>&1")
    log(out.split("\n")[0] if out else "Config check done")


def main():
    print("")
    print("🔧 ModelPool Repair v1.0")
    print("=" * 40)

    out, _ = run("openclaw --version 2>&1")
    log(f"{'✅ ' + out if out else '❌ OpenClaw not found'}")

    issues = step1_diagnose()
    dead = step2_test_apis()
    step3_fix_config()
    step4_clean_sessions()
    step5_rebuild_fallback(dead)
    step6_cleanup()
    step7_restart()

    print("")
    print("=" * 40)
    print("🎉 Repair complete!")
    print("=" * 40)
    print("")
    print("  Executed:")
    print("    1. Diagnostics (Gateway/Config/Memory/Disk)")
    print("    2. API connectivity test")
    print("    3. Config fix (doctor --fix)")
    print("    4. Session cleanup")
    print("    5. Fallback chain rebuild")
    print("    6. Resource cleanup")
    print("    7. Full restart")
    print("")


if __name__ == "__main__":
    main()
