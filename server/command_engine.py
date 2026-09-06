import re
from typing import Dict, Any
from server.system_actions import SystemActionExecutor

class JasperVoiceCommandEngine:
    def __init__(self):
        self.executor = SystemActionExecutor()

    def parse_and_execute(self, voice_text: str) -> Dict[str, Any]:
        t = voice_text.lower().strip()

        # 1. Kalkulyator
        if any(w in t for w in ["kalkulyator", "hisoblagich", "calculator", "калькулятор"]):
            res = self.executor.open_app("kalkulyator")
            return {
                "intent": "OPEN_APP",
                "action": "calc",
                "speech_response": "Kalkulyator dasturini ochdim, xo'jayin!",
                "details": res
            }

        # 2. Bloknot / Notepad
        if any(w in t for w in ["bloknot", "notepad", "yozuv daftari", "блокнот"]):
            res = self.executor.open_app("notepad")
            return {
                "intent": "OPEN_APP",
                "action": "notepad",
                "speech_response": "Bloknot dasturi ochildi!",
                "details": res
            }

        # 3. Fayllar / Explorer / Papka
        if any(w in t for w in ["fayllar", "provodnik", "papka", "explorer", "проводник"]):
            res = self.executor.open_app("explorer")
            return {
                "intent": "OPEN_APP",
                "action": "explorer",
                "speech_response": "Fayllar menejeri ochildi.",
                "details": res
            }

        # 4. Chrome / Brauzer
        if any(w in t for w in ["chrome", "xrom", "brauzer", "browser", "хром"]):
            res = self.executor.open_app("chrome")
            return {
                "intent": "OPEN_APP",
                "action": "chrome",
                "speech_response": "Google Chrome brauzeri ochildi!",
                "details": res
            }

        # 5. Telegram
        if any(w in t for w in ["telegram", "telega", "tg", "телеграм"]):
            res = self.executor.open_app("telegram")
            return {
                "intent": "OPEN_APP",
                "action": "telegram",
                "speech_response": "Telegram ilovasini ochdim.",
                "details": res
            }

        # 6. GitHub
        if any(w in t for w in ["github", "git xab", "git hub", "git", "гитхаб"]):
            res = self.executor.open_website("https://github.com/salomh46-rgb", "GitHub Profilingiz")
            return {
                "intent": "OPEN_WEBSITE",
                "action": "github",
                "speech_response": "GitHub profilingizni brauzerda ochdim!",
                "details": res
            }

        # 7. YouTube
        if any(w in t for w in ["youtube", "yutub", "yu tub", "видео", "ютуб"]):
            res = self.executor.open_website("https://youtube.com", "YouTube")
            return {
                "intent": "OPEN_WEBSITE",
                "action": "youtube",
                "speech_response": "YouTube platformasini ochdim, xo'jayin!",
                "details": res
            }

        # 8. Portfolio
        if any(w in t for w in ["portfolio", "portfolyo", "saytim", "портфолио"]):
            res = self.executor.open_website("https://javohirbek-portfolio.vercel.app", "Shaxsiy Portfolio")
            return {
                "intent": "OPEN_WEBSITE",
                "action": "portfolio",
                "speech_response": "Shaxsiy portfolio saytingizni ochdim!",
                "details": res
            }

        # 9. Disk / Xotira holati (Disk status)
        if any(w in t for w in ["disk", "xotira", "joy", "qancha joy", "c disk", "d disk", "память", "диск"]):
            stats = self.executor.get_disk_stats()
            c_free = stats.get("C", {}).get("free_gb", 0)
            d_free = stats.get("D", {}).get("free_gb", 0)
            return {
                "intent": "SYSTEM_AUDIT",
                "action": "disk_status",
                "speech_response": f"C diskda {c_free} gigabayt, D diskda esa {d_free} gigabayt bo'sh joy mavjud, xo'jayin!",
                "details": stats
            }

        # 10. Loyihalar ro'yxati (Projects)
        if any(w in t for w in ["loyiha", "proyekt", "loyihalar", "nimalar bor", "proyektlar", "проекты"]):
            projs = self.executor.list_projects()
            count = len(projs)
            sample = ", ".join(projs[:4])
            return {
                "intent": "PROJECTS_LIST",
                "action": "list_projects",
                "speech_response": f"D diskdagi ALLProjects papkasida jami {count} ta faol loyihalar mavjud. Masalan: {sample} va boshqalar.",
                "details": {"total": count, "projects": projs}
            }

        # 11. Salomlashish / Hol-ahvol
        if any(w in t for w in ["salom", "qalesan", "qalaysan", "ishlar", "nima gap", "привет", "здравствуй"]):
            return {
                "intent": "GREETING",
                "action": "greeting",
                "speech_response": "Assalomu alaykum, xo'jayin! Men buyruqlaringizni bajarishga 100% tayyorman. Nima xizmat?",
                "details": {}
            }

        # 12. Umumiy intellektual javob (General inquiry fallback)
        return {
            "intent": "GENERAL_ASSISTANT",
            "action": "answer",
            "speech_response": f"«{voice_text}» buyrug'ingizni qabul qildim. Kompyuteringiz to'liq nazoratimda, har qanday vazifani bajarishga tayyorman!",
            "details": {"raw_query": voice_text}
        }
