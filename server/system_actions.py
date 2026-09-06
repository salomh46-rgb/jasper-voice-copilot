import os
import subprocess
import shutil
import webbrowser
from typing import Dict, Any, List

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
    def open_app(app_name: str) -> Dict[str, Any]:
        app_map = {
            "calculator": "calc.exe",
            "kalkulyator": "calc.exe",
            "notepad": "notepad.exe",
            "bloknot": "notepad.exe",
            "explorer": "explorer.exe",
            "fayllar": "explorer.exe",
            "cmd": "start cmd.exe",
            "terminal": "start powershell.exe",
            "powershell": "start powershell.exe",
            "chrome": "start chrome",
            "telegram": "start telegram",
            "vscode": "code"
        }
        target = app_map.get(app_name.lower())
        if target:
            try:
                subprocess.Popen(target, shell=True)
                return {"success": True, "app": app_name, "message": f"{app_name.capitalize()} dasturi ochildi."}
            except Exception as e:
                return {"success": False, "app": app_name, "error": str(e)}
        return {"success": False, "app": app_name, "message": "Noma'lum dastur"}

    @staticmethod
    def open_website(url: str, site_name: str = "") -> Dict[str, Any]:
        try:
            if not url.startswith("http"):
                url = "https://" + url
            webbrowser.open(url)
            return {"success": True, "url": url, "site": site_name or url, "message": f"{site_name or url} sayti brauzerda ochildi."}
        except Exception as e:
            return {"success": False, "error": str(e)}
