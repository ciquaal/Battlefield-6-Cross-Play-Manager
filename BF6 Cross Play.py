#!/usr/bin/env python3
import argparse, os, shutil, sys

CROSSPLAY_LINE = "GstGameplay.CrossPlayEnable 0"
SIGNATURE = "— Babboon."
USE_COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None

def c(code, s): return f"\033[{code}m{s}\033[0m" if USE_COLOR else s
def ok(s): return c("92", s)
def warn(s): return c("93", s)
def err(s): return c("91", s)
def dim(s): return c("2", s)
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
def ui_clear(): os.system("cls" if os.name == "nt" else "clear")
def ui(lines=None, platform=None):
    ui_clear()
    print(c("96", BANNER))
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
def paths(platform):
    up = os.environ.get("USERPROFILE")
    if not up: sys.exit(err("[ERROR] USERPROFILE not set"))
    base = os.path.join(up, "Documents", "Battlefield 6", "settings")
    if platform == "steam":
        prof = os.path.join(base, "steam", "PROFSAVE_profile")
        backup = os.path.join(base, "steam", "backup", "PROFSAVE_profile")
    else:  # ea
        prof = os.path.join(base, "PROFSAVE_profile")
        backup = os.path.join(base, "backup", "PROFSAVE_profile")
    return base, prof, backup

# ---------- File ops ----------
def read(p):  return open(p,encoding="utf-8",errors="ignore").read()
def write(p,t): open(p,"w",encoding="utf-8").write(t)
def clean(t):
    return "\n".join([l for l in t.replace("\r","").split("\n")
                      if not l.strip().startswith("GstGameplay.CrossPlayEnable")]).rstrip()+"\n"

def ensure_once(platform):
    _, prof, backup = paths(platform)
    if not os.path.isfile(prof): sys.exit(err(f"[ERROR] PROFSAVE_profile not found: {prof}"))
    cur = read(prof)
    new = clean(cur)
    if new != cur:
        write(prof, new)   # remove existing overrides in-place
    if not os.path.isfile(backup):
        os.makedirs(os.path.dirname(backup), exist_ok=True)
        shutil.copy2(prof, backup)  # backup from cleaned file
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
    if not os.path.isfile(prof): sys.exit(err(f"[ERROR] PROFSAVE_profile not found: {prof}"))
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
        if ch == "1": disable(platform)
        elif ch == "2": enable(platform)
        elif ch == "3": status(platform)
        elif ch == "s":
            ui(platform=platform)
            platform = select_platform_interactive()
            ui([info(f"Switched to {platform.upper()}.")], platform=platform)
        elif ch in ("q","quit","exit"): break
        else: ui([err("Invalid choice.")], platform=platform)

# ---------- Argparse ----------
def main():
    p = argparse.ArgumentParser(description="BF6 Cross-Play CLI for Steam and EA launchers.")
    p.add_argument("--platform", choices=["steam","ea"], help="Select launcher without prompt.")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("disable")
    sub.add_parser("enable")
    sub.add_parser("status")
    sub.add_parser("menu")
    a = p.parse_args()

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

if __name__ == "__main__":
    main()
