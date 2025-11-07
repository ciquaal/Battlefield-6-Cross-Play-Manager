import argparse, os, shutil, sys, glob

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

IS_TTY = sys.stdout.isatty()
IS_UTF8 = (getattr(sys.stdout, "encoding", "") or "").lower().startswith("utf")
USE_COLOR = IS_TTY and os.environ.get("NO_COLOR") is None
SHOW_BANNER = IS_TTY and IS_UTF8 and os.environ.get("NO_BANNER") is None

CROSSPLAY_LINE = "GstGameplay.CrossPlayEnable 0"
SIGNATURE = "— Babboon."

def c(code, s): return f"\033[{code}m{s}\033[0m" if USE_COLOR else s
def ok(s): return c("92", s)
def warn(s): return c("93", s)
def err(s): return c("91", s)
def dim(s): return c("2",  s)
def info(s): return c("94", s)

BANNER = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⠟⢿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠀⠀⠀⠀⠀⣴⣶⠲⣶⢦⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⠶⠋⠁⢈⣷⠾⠟⠉
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⠀⠀⠀⠀⠐⣿⣶⣺⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⠞⠋⠀⣠⡴⠞⠉⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⡏⡍⠉⢹⡞⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡴⠞⠋⠘⣿⣶⠶⠋⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣷⣄⣴⠿⠦⠤⣤⣀⣸⡇⠳⠶⠘⣧⣀⣀⣀⣀⠀⠀⠀⠀⣀⡤⠞⣏⠀⣀⡤⠖⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣤⣶⣦⣼⡿⢦⣿⡀⢐⠐⣿⠉⢽⡿⠿⠿⠿⠿⠿⣿⠿⠿⣧⣤⠶⢿⠁⣀⡤⠞⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⠿⢿⣯⣿⣥⣤⣤⣽⠿⣶⡶⠦⠀⠙⠂⠐⢦⢀⣺⠿⣶⡞⠉⠀⣠⣾⡿⣿⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡘⣆⠋⢀⡔⠋⢠⠞⠀⣴⠛⠶⣄⠀⠀⠑⡶⠞⢫⣠⠞⢀⣱⢶⣿⠇⣠⠟⣶⡿⢷⣽⣿⡷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣈⣓⣾⣦⣀⣱⣄⣈⣧⣀⣘⣦⣀⣘⣦⣀⡼⠓⠶⠛⣣⣤⠟⠛⣻⣯⣾⣿⣿⣷⣾⣿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢠⣤⣤⣴⣶⣶⣿⣿⣿⣏⣵⣿⣷⣶⣷⣿⣿⣿⠿⠶⠶⣶⣶⣶⡶⠾⠾⠿⢿⣟⣛⠛⢻⣛⣛⣉⣉⣉⣉⡉⢹⣯⡙⠛⢿⣛⠻⣗⣒⠶⠦⢤⣄⣀⡀⠀⠀⠀⠀
⣾⣿⠶⣿⣿⠧⢾⣧⠀⡇⠀⠀⠀⠇⠀⢹⠉⠉⡟⠲⢤⡀⠀⠈⣉⣙⣒⣲⣦⣤⣉⣻⣏⣉⠉⠉⠉⠉⠉⠁⠀⠀⠙⢦⣀⡼⣷⣤⡈⠉⠓⢲⣶⣾⣿⣿⡳⢶⡄
⠚⣿⣠⣿⡇⠀⣾⡿⠒⡿⠒⢶⣆⣱⣤⣤⣤⠀⣇⠀⠈⣇⡴⠻⠛⠛⠛⠋⠉⠉⠉⢿⠿⠿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠞⠛⠛⠳⣄⡴⠋⠀⠀⠀⢀⣀⣀⣿
⠀⠛⠛⢻⡆⠀⣿⣧⠀⠁⠀⠀⠀⡇⠀⠈⠉⠉⡇⠀⠀⣿⠃⠀⣀⣤⣴⣶⣶⣶⣤⠬⣷⣤⣤⣤⣤⣤⣤⣶⣶⣶⣶⣖⣶⣶⡶⠾⢿⡿⣷⣤⣴⣶⣿⣿⣿⣿⠛
⠀⠀⠀⠈⣷⣿⣷⣬⠀⠀⠒⠒⠒⢶⠤⠬⢤⣀⣀⠀⠀⣯⣴⣿⣿⡿⢿⣿⣛⠻⣷⠀⠀⠀⠀⠀⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⣠⢿⣿⣷⣿⣿⣟⣸⣿⣿⡿⠀
⠀⠀⠀⠀⠹⣿⣿⣿⣶⣶⣤⣤⣀⣸⣄⠀⠀⠀⠘⣠⣴⣿⣿⣿⣿⣿⣟⣛⣛⣻⣯⣀⣀⣀⣀⣀⡀⠀⢀⣠⣤⣤⣤⣤⣤⣄⣞⣡⠟⢉⣿⣿⣿⣲⣿⣿⡿⠃⠀
⠀⠀⠀⠀⠀⠹⣿⣿⣾⣿⣼⣿⣏⢸⣿⡋⢹⣶⠋⢹⣿⡟⠛⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣇⣼⣿⡅⢳⣀⣿⣿⠿⠿⢿⣿⠟⠁⠀⠀
⠀⠀⠀⠀⠀⠀⠙⠻⠿⢿⣿⣿⣿⣿⣿⣷⣾⣿⣇⣾⣿⣇⣸⣿⣿⣿⣛⠃⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣽⢟⣱⣿⣿⠟⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣥⣾⣿⣿⣿⣿⠿⠿⠿⠿⠟⠛⠛⠛⠛⠋⠉⠉⠉⠙⠛⠛⠛⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠙⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                     Battlefield 6 Cross-Play Manager
Backup is automatic once on first run after cleaning the profile.
- babboon.
"""

FOOT = "\n" + "─"*76 + "\n" + dim(SIGNATURE) + "\n"

# ---------- UI ----------
def ui_clear():
    os.system("cls" if os.name == "nt" else "clear")

def ui(lines=None, platform=None):
    ui_clear()
    if SHOW_BANNER:
        print(c("96", BANNER))
    else:
        print("Battlefield 6 Cross-Play Manager")
        print("Backup is automatic once on first run after cleaning the profile.\n")
    if platform:
        print(dim(f"Launcher: {platform.upper()}"))
    if lines:
        for line in lines:
            if line: print(line)
    print()

def select_platform_interactive():
    while True:
        print(c("95"," [1] ") + "Steam  " + dim(r"(Documents\Battlefield 6\settings\steam\PROFSAVE_profile)"))
        print(c("95"," [2] ") + "EA     " + dim(r"(Documents\Battlefield 6\settings\PROFSAVE_profile)"))
        choice = input(dim("\nSelect launcher: ")).strip()
        if choice == "1": return "steam"
        if choice == "2": return "ea"
        ui([err("Invalid choice.")])

# ---------- Paths ----------
def documents_roots():
    """Return candidate 'Documents' roots, handling OneDrive redirection."""
    up = os.environ.get("USERPROFILE", "")
    if not up:
        sys.exit(err("[ERROR] USERPROFILE not set"))
    candidates = [
        os.path.join(up, "Documents"),
        os.path.join(up, "OneDrive", "Documents"),
    ]
    candidates.extend([os.path.join(up, d, "Documents")
                       for d in os.listdir(up)
                       if d.startswith("OneDrive") and os.path.isdir(os.path.join(up, d))])
    seen, uniq = set(), []
    for p in candidates:
        if p not in seen:
            seen.add(p)
            uniq.append(p)
    return uniq

def game_settings_base():
    user = os.environ.get("USERNAME")
    if not user:
        up = os.environ.get("USERPROFILE", "")
        user = os.path.basename(up) if up else ""
    if not user:
        sys.exit(err("[ERROR] Could not determine current username"))

    targets = [
        os.path.join("Documents", "Battlefield 6", "settings", "steam", "PROFSAVE_profile"),
        os.path.join("Documents", "Battlefield 6", "settings", "PROFSAVE_profile"),
    ]
    for code in range(65, 91):  # A..Z
        drive = f"{chr(code)}:\\"
        base = os.path.join(drive, "Users", user)
        if not os.path.isdir(base):
            continue
        for t in targets:
            test = os.path.join(base, t)
            if os.path.isfile(test):
                print(info(f"[INFO] Found Battlefield 6 settings on drive {drive[0]}"))
                return os.path.dirname(os.path.dirname(test))

    sys.exit(err("[ERROR] Could not locate Battlefield 6 settings on any drive"))

def paths(platform):
    base = game_settings_base()
    if platform == "steam":
        prof   = os.path.join(base, "steam", "PROFSAVE_profile")
        backup = os.path.join(base, "steam", "backup", "PROFSAVE_profile")
    else:  # ea
        prof   = os.path.join(base, "PROFSAVE_profile")
        backup = os.path.join(base, "backup", "PROFSAVE_profile")
    return base, prof, backup

# ---------- File ops ----------
def read(p):  return open(p, encoding="utf-8", errors="ignore").read()
def write(p,t):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(t)

def clean(t):
    return "\n".join(
        [l for l in t.replace("\r","").split("\n")
         if not l.strip().startswith("GstGameplay.CrossPlayEnable")]
    ).rstrip() + "\n"

def ensure_once(platform):
    _, prof, backup = paths(platform)
    if not os.path.isfile(prof):
        sys.exit(err(f"[ERROR] PROFSAVE_profile not found: {prof}"))
    cur = read(prof)
    new = clean(cur)
    if new != cur:
        write(prof, new)
    if not os.path.isfile(backup):
        os.makedirs(os.path.dirname(backup), exist_ok=True)
        shutil.copy2(prof, backup)
        return True
    return False

# ---------- Actions ----------
def disable(platform):
    _, prof, _ = paths(platform)
    backed = ensure_once(platform)
    new = CROSSPLAY_LINE + "\n" + clean(read(prof))
    write(prof, new)
    lines = [ok("[OK] Cross-play disabled. Override line placed at top.")]
    if backed:
        lines.append(ok("[OK] Backup created from cleaned profile."))
    ui(lines, platform=platform)
    print(FOOT)

def enable(platform):
    _, prof, backup = paths(platform)
    if not os.path.isfile(backup):
        backed = ensure_once(platform)
        if not os.path.isfile(backup):
            sys.exit(err("[ERROR] No backup found"))
    shutil.copy2(backup, prof)
    ui([ok("[OK] Cross-play enabled. Restored from backup.")], platform=platform)
    print(FOOT)

def status(platform):
    _, prof, _ = paths(platform)
    if not os.path.isfile(prof):
        sys.exit(err(f"[ERROR] PROFSAVE_profile not found: {prof}"))
    txt = read(prof)
    if CROSSPLAY_LINE in txt:
        ui([ok("Cross play has been disabled, BOT ON!")], platform=platform)
    else:
        ui([warn("Cross play is ENABLED")], platform=platform)
    print(FOOT)

# ---------- Menus ----------
def main_menu(platform):
    ui(platform=platform)
    while True:
        print(c("95"," [1] ")+"Disable cross-play")
        print(c("95"," [2] ")+"Enable cross-play")
        print(c("95"," [3] ")+"Status")
        print(c("95"," [S] ")+"Switch launcher")
        print(c("95"," [Q] ")+"Quit")
        ch = input(dim("\nSelect: ")).strip().lower()
        if ch == "1":
            disable(platform)
        elif ch == "2":
            enable(platform)
        elif ch == "3":
            status(platform)
        elif ch == "s":
            ui(platform=platform)
            platform = select_platform_interactive()
            ui([info(f"Switched to {platform.upper()}.")], platform=platform)
        elif ch in ("q","quit","exit"):
            break
        else:
            ui([err("Invalid choice.")], platform=platform)

# ---------- Argparse ----------
def main():
    p = argparse.ArgumentParser(description="BF6 Cross-Play CLI for Steam and EA launchers.")
    p.add_argument("--platform", choices=["steam", "ea"], help="Select launcher without prompt.")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("disable")
    sub.add_parser("enable")
    sub.add_parser("status")
    sub.add_parser("menu")
    a = p.parse_args()

    _ = game_settings_base()

    platform = a.platform or select_platform_interactive()

    if a.cmd in (None, "menu"):
        main_menu(platform)
    elif a.cmd == "disable":
        disable(platform)
    elif a.cmd == "enable":
        enable(platform)
    elif a.cmd == "status":
        status(platform)
    else:
        p.print_help()

def hold_if_no_tty():
    if not sys.stdin.isatty():
        try:
            input("\nPress Enter to close...")
        except Exception:
            pass

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        hold_if_no_tty()
        raise
    except Exception as e:
        print(err(f"\n[CRASH] {e}"))
        hold_if_no_tty()
        raise
    finally:
        hold_if_no_tty()
