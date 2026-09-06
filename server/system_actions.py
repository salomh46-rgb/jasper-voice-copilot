import os
import sys
import shutil
import subprocess
import webbrowser
import urllib.parse
from typing import Dict, Any, List, Optional

class SystemActionExecutor:
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

    @staticmethod
    def _find_telegram_path() -> Optional[str]:
        candidates = [
            os.path.expandvars(r"%APPDATA%\Telegram Desktop\Telegram.exe"),
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Telegram Desktop\Telegram.exe"),
            os.path.expandvars(r"%PROGRAMFILES%\Telegram Desktop\Telegram.exe"),
            os.path.expandvars(r"%PROGRAMFILES(X86)%\Telegram Desktop\Telegram.exe"),
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
        return None

    @staticmethod
    def _find_chrome_path() -> Optional[str]:
        candidates = [
            os.path.expandvars(r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%PROGRAMFILES(X86)%\Microsoft\Edge\Application\msedge.exe"),
            os.path.expandvars(r"%PROGRAMFILES%\Microsoft\Edge\Application\msedge.exe"),
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
        return None

    @staticmethod
    def _find_vscode_path() -> Optional[str]:
        candidates = [
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"),
            os.path.expandvars(r"%PROGRAMFILES%\Microsoft VS Code\Code.exe"),
            os.path.expandvars(r"%PROGRAMFILES(X86)%\Microsoft VS Code\Code.exe"),
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
        if shutil.which("code"):
            return "code"
        return None

    @staticmethod
    def open_app(app_name: str) -> Dict[str, Any]:
        app_key = app_name.lower().strip()
        
        # 1. Calculator
        if app_key in ["calculator", "kalkulyator", "hisoblagich", "calc"]:
            try:
                subprocess.Popen(["calc.exe"])
                return {"success": True, "app": "Kalkulyator", "message": "Kalkulyator dasturi ochildi."}
            except Exception as e:
                return {"success": False, "app": "Kalkulyator", "error": str(e)}

        # 2. Notepad / Bloknot
        if app_key in ["notepad", "bloknot", "matn"]:
            try:
                subprocess.Popen(["notepad.exe"])
                return {"success": True, "app": "Bloknot", "message": "Bloknot matn muharriri ochildi."}
            except Exception as e:
                return {"success": False, "app": "Bloknot", "error": str(e)}

        # 3. Explorer / Fayllar
        if app_key in ["explorer", "fayllar", "papka", "kompyuter", "provodnik"]:
            try:
                subprocess.Popen(["explorer.exe"])
                return {"success": True, "app": "Explorer", "message": "Fayllar menejeri ochildi."}
            except Exception as e:
                return {"success": False, "app": "Explorer", "error": str(e)}

        # 4. Terminal / PowerShell / Cmd
        if app_key in ["terminal", "powershell", "cmd", "konsol"]:
            try:
                subprocess.Popen(["powershell.exe"])
                return {"success": True, "app": "PowerShell Terminal", "message": "PowerShell terminali ochildi."}
            except Exception as e:
                return {"success": False, "app": "Terminal", "error": str(e)}

        # 5. Chrome / Brauzer
        if app_key in ["chrome", "brauzer", "browser", "internet", "edge"]:
            chrome_path = SystemActionExecutor._find_chrome_path()
            if chrome_path:
                try:
                    subprocess.Popen([chrome_path])
                    return {"success": True, "app": "Brauzer", "message": "Internet brauzeri ochildi."}
                except Exception:
                    pass
            webbrowser.open("https://google.com")
            return {"success": True, "app": "Brauzer", "message": "Internet brauzeri ochildi."}

        # 6. Telegram
        if app_key in ["telegram", "telega", "tg"]:
            tg_path = SystemActionExecutor._find_telegram_path()
            if tg_path:
                try:
                    subprocess.Popen([tg_path])
                    return {"success": True, "app": "Telegram Desktop", "message": "Telegram Desktop ilovasi ochildi."}
                except Exception:
                    pass
            # Fallback to Telegram Web cleanly
            webbrowser.open("https://web.telegram.org")
            return {
                "success": True,
                "app": "Telegram Web",
                "message": "Telegram ochildi."
            }

        # 7. VS Code
        if app_key in ["vscode", "vs code", "kod", "dasturlash"]:
            code_path = SystemActionExecutor._find_vscode_path()
            if code_path:
                try:
                    subprocess.Popen([code_path])
                    return {"success": True, "app": "VS Code", "message": "Visual Studio Code ochildi."}
                except Exception:
                    pass
            webbrowser.open("https://github.com/salomh46-rgb")
            return {"success": True, "app": "GitHub", "message": "GitHub loyihalaringiz ochildi."}

        # 8. Paint
        if app_key in ["paint", "rasm", "mspaint"]:
            try:
                subprocess.Popen(["mspaint.exe"])
                return {"success": True, "app": "Paint", "message": "Paint rasm dasturi ochildi."}
            except Exception as e:
                return {"success": False, "app": "Paint", "error": str(e)}

        # 9. Task Manager / Vazifalar menejeri
        if app_key in ["taskmgr", "dispetcher", "vazifalar", "task manager"]:
            try:
                subprocess.Popen(["taskmgr.exe"])
                return {"success": True, "app": "Task Manager", "message": "Vazifalar dispetcheri ochildi."}
            except Exception as e:
                return {"success": False, "app": "Task Manager", "error": str(e)}

        # Fallback: try opening as website or generic search
        return {"success": False, "app": app_name, "message": f"{app_name} dasturi tizimda topilmadi."}

    @staticmethod
    def open_website(url: str, site_name: str = "") -> Dict[str, Any]:
        try:
            if not url.startswith("http"):
                url = "https://" + url
            webbrowser.open(url)
            return {"success": True, "url": url, "site": site_name or url, "message": f"{site_name or url} sayti brauzerda ochildi."}
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
