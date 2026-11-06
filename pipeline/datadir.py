"""The player's library: games, firmware, licences, builds and saves (the folder the code calls the dump).

ATIV_DUMP=<dir> when set (a test library, a second disk); else <root>/dump when it exists (a checkout, or an install
from before the library had a folder of its own: nothing moves); else the platform's per-user data folder, beside the
launcher's settings, so an update can replace the install without touching anything the player made:
  macOS    ~/Library/Application Support/ProjectNativ/Nativ/library
  Linux    $XDG_DATA_HOME/ProjectNativ/Nativ/library   (~/.local/share when unset)
  Windows  %LOCALAPPDATA%/ProjectNativ/Nativ/library    (local rather than roaming: a game is gigabytes)
A folder chosen in the launcher's Settings (hub.ini's library) wins over all of that, and ATIV_PORTABLE_LIBRARY (which an
AppImage's AppRun sets: the folder beside the .AppImage) is only a default, so Settings wins over it too. The launcher makes
the same choice (launcher/hub.cpp library_dir) and passes it to the stages as ATIV_DUMP.
"""
import os
import sys


def _saved_library() -> str:
    """the library the player chose in the launcher's Settings: hub.ini's library=<dir>, beside the launcher's settings"""
    try: f = open(os.path.join(prefs_dir(), "hub.ini"), encoding="utf-8", errors="replace")
    except OSError: return ""
    with f:
        for line in f:
            k, _, v = line.partition("=")
            if k.strip() == "library" and v.strip(): return os.path.expanduser(v.strip())
    return ""


def library_dir(root: str) -> str:
    d = os.environ.get("ATIV_DUMP")
    if d: return d
    d = _saved_library()   # (the launcher's Settings: where the player keeps it)
    if d: return d
    d = os.environ.get("ATIV_PORTABLE_LIBRARY")   # (an AppImage's folder beside it: a default, not a choice)
    if d: return d
    if os.path.isdir(os.path.join(root, "dump")): return os.path.join(root, "dump")
    home = os.path.expanduser("~")
    if sys.platform == "win32": base = os.environ.get("LOCALAPPDATA") or os.path.join(home, "AppData", "Local")
    elif sys.platform == "darwin": base = os.path.join(home, "Library", "Application Support")
    else: base = os.environ.get("XDG_DATA_HOME") or os.path.join(home, ".local", "share")
    return os.path.join(base, "ProjectNativ", "Nativ", "library")


def prefs_dir() -> str:
    """the launcher's own folder (SDL_GetPrefPath("ProjectNativ", "Nativ"), or ATIV_PREFS): its settings, the settings every
    game reads (settings.ini) and its log (launcher.log). Windows keeps it in the roaming folder, as SDL does"""
    d = os.environ.get("ATIV_PREFS")
    if d: return d
    home = os.path.expanduser("~")
    if sys.platform == "win32": base = os.environ.get("APPDATA") or os.path.join(home, "AppData", "Roaming")
    elif sys.platform == "darwin": base = os.path.join(home, "Library", "Application Support")
    else: base = os.environ.get("XDG_DATA_HOME") or os.path.join(home, ".local", "share")
    return os.path.join(base, "ProjectNativ", "Nativ")
