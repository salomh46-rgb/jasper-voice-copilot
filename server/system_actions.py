import os
import sys
import json
import shutil
import subprocess
import webbrowser
import urllib.parse
from typing import Dict, Any, List, Optional

class SystemActionExecutor:
    _cached_apps: Dict[str, str] = {}

    @classmethod
    def _load_start_apps(cls):
        try:
            cmd = ['powershell', '-NoProfile', '-Command', '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; Get-StartApps | ConvertTo-Json']
            p = subprocess.run(cmd, capture_output=True, timeout=10)
            if p.returncode == 0 and p.stdout:
                data = json.loads(p.stdout.decode('utf-8', errors='ignore'))
                if isinstance(data, list):
                    for item in data:
                        name = item.get("Name", "").lower()
                        appid = item.get("AppID", "")
                        if name and appid:
                            cls._cached_apps[name] = appid
        except Exception as e:
            print(f"Error loading start apps: {e}")

    @classmethod
    def get_start_apps(cls) -> Dict[str, str]:
        if not cls._cached_apps:
            cls._load_start_apps()
        return cls._cached_apps

    @staticmethod
    def get_disk_stats() -> Dict[str, Any]:
        stats = {}
        for d in ['C:\\', 'D:\\']:
            if os.path.exists(d):
                total, used, free = shutil.disk_usage(d)
                stats[d[0]] = {
                    "total_gb": round(total / (1024**3), 2),
                    "used_gb": round(used / (1024**3), 2),
                    "free_gb": round(free / (1024**3), 2),
                    "percent_used": round((used / total) * 100, 1)
                }
        return stats

    @staticmethod
    def list_projects() -> List[str]:
        p_dir = r"D:\ALLProjects"
        if os.path.exists(p_dir):
            return sorted([f for f in os.listdir(p_dir) if os.path.isdir(os.path.join(p_dir, f))])
        return []

    @classmethod
    def open_app(cls, app_name: str) -> Dict[str, Any]:
        app_key = app_name.lower().strip()
        apps_map = cls.get_start_apps()

        # 1. Telegram Desktop (Store or Win32)
        if any(k in app_key for k in ["telegram", "telega", "tg", "телеграм"]):
            for name, appid in apps_map.items():
                if "telegram" in name:
                    try:
                        subprocess.Popen(["explorer.exe", f"shell:AppsFolder\{appid}"])
                        return {"success": True, "app": "Telegram Desktop", "message": "Telegram Desktop ilovasi ochildi."}
                    except Exception:
                        pass
            # Fallback to telegram URL protocol or web
            try:
                os.startfile("tg://")
                return {"success": True, "app": "Telegram Desktop", "message": "Telegram ilovasi ochildi."}
            except Exception:
                webbrowser.open("https://web.telegram.org")
                return {"success": True, "app": "Telegram Web", "message": "Telegram ochildi."}

        # 2. Google Chrome / Brauzer
        if any(k in app_key for k in ["chrome", "xrom", "brauzer", "browser", "хром"]):
            for name, appid in apps_map.items():
                if "chrome" in name:
                    try:
                        subprocess.Popen(["explorer.exe", f"shell:AppsFolder\{appid}"])
                        return {"success": True, "app": "Google Chrome", "message": "Google Chrome brauzeri ochildi."}
                    except Exception:
                        pass
            webbrowser.open("https://google.com")
            return {"success": True, "app": "Brauzer", "message": "Internet brauzeri ochildi."}

        # 3. Visual Studio Code
        if any(k in app_key for k in ["vscode", "vs code", "code", "kod", "dasturlash"]):
            for name, appid in apps_map.items():
                if "visual studio code" in name or "code" == name:
                    try:
                        subprocess.Popen(["explorer.exe", f"shell:AppsFolder\{appid}"])
                        return {"success": True, "app": "VS Code", "message": "Visual Studio Code dasturi ochildi."}
                    except Exception:
                        pass

        # 4. Calculator / Kalkulyator
        if any(k in app_key for k in ["calculator", "kalkulyator", "hisoblagich", "calc"]):
            for name, appid in apps_map.items():
                if "calculator" in name or "kalkulyator" in name:
                    try:
                        subprocess.Popen(["explorer.exe", f"shell:AppsFolder\{appid}"])
                        return {"success": True, "app": "Kalkulyator", "message": "Kalkulyator dasturi ochildi."}
                    except Exception:
                        pass
            try:
                subprocess.Popen(["calc.exe"])
                return {"success": True, "app": "Kalkulyator", "message": "Kalkulyator dasturi ochildi."}
            except Exception as e:
                return {"success": False, "error": str(e)}

        # 5. Notepad / Bloknot
        if any(k in app_key for k in ["notepad", "bloknot", "matn"]):
            for name, appid in apps_map.items():
                if "notepad" in name or "bloknot" in name:
                    try:
                        subprocess.Popen(["explorer.exe", f"shell:AppsFolder\{appid}"])
                        return {"success": True, "app": "Bloknot", "message": "Bloknot dasturi ochildi."}
                    except Exception:
                        pass
            try:
                subprocess.Popen(["notepad.exe"])
                return {"success": True, "app": "Bloknot", "message": "Bloknot dasturi ochildi."}
            except Exception as e:
                return {"success": False, "error": str(e)}

        # 6. Explorer / Fayllar
        if any(k in app_key for k in ["explorer", "fayllar", "papka", "kompyuter"]):
            try:
                subprocess.Popen(["explorer.exe"])
                return {"success": True, "app": "Explorer", "message": "Fayllar menejeri ochildi."}
            except Exception as e:
                return {"success": False, "error": str(e)}

        # 7. Terminal / PowerShell / CMD
        if any(k in app_key for k in ["terminal", "powershell", "cmd", "konsol"]):
            try:
                subprocess.Popen(["powershell.exe"])
                return {"success": True, "app": "Terminal", "message": "PowerShell terminali ochildi."}
            except Exception as e:
                return {"success": False, "error": str(e)}

        # 8. Dynamic Search in all installed Apps
        for name, appid in apps_map.items():
            if app_key in name:
                try:
                    subprocess.Popen(["explorer.exe", f"shell:AppsFolder\{appid}"])
                    return {"success": True, "app": name.title(), "message": f"{name.title()} dasturi ochildi."}
                except Exception:
                    pass

        return {"success": False, "app": app_name, "message": f"{app_name} kompyuteringizda topilmadi."}

    @staticmethod
    def open_website(url: str, site_name: str = "") -> Dict[str, Any]:
        try:
            if not url.startswith("http"):
                url = "https://" + url
            webbrowser.open(url)
            return {"success": True, "url": url, "site": site_name or url, "message": f"{site_name or url} sahifasi ochildi."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def search_web(query: str) -> Dict[str, Any]:
        try:
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.google.com/search?q={encoded_query}"
            webbrowser.open(url)
            return {"success": True, "query": query, "url": url, "message": f"Google orqali «{query}» qidirilmoqda."}
        except Exception as e:
            return {"success": False, "error": str(e)}
