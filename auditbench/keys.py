"""Read API keys from the process env, else from the Windows user env (HKCU\\Environment).

`setx NAME value` writes HKCU\\Environment but already-running processes never see it;
reading the registry directly means no app restart is needed. Values are never logged.
"""
from __future__ import annotations

import os


def get(name: str) -> str | None:
    if os.environ.get(name):
        return os.environ[name]
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
            return winreg.QueryValueEx(k, name)[0] or None
    except (ImportError, OSError):
        return None
