import re
from typing import Dict, Any
from server.system_actions import SystemActionExecutor

class JasperVoiceCommandEngine:
    def __init__(self):
        self.executor = SystemActionExecutor()

    def parse_and_execute(self, voice_text: str) -> Dict[str, Any]:
        t = voice_text.lower().strip()

        # 1. Kalkulyator
        if any(w in t for w in ["kalkulyator", "hisoblagich", "calculator", "калькулятор", "hisobla"]):
            res = self.executor.open_app("kalkulyator")
            return {
                "intent": "OPEN_APP",
                "action": "calc",
                "speech_response": "Kalkulyator dasturini ochdim, xo'jayin!",
                "details": res
            }

        # 2. Bloknot / Notepad
        if any(w in t for w in ["bloknot", "notepad", "yozuv daftari", "блокнот", "matn"]):
            res = self.executor.open_app("notepad")
            return {
                "intent": "OPEN_APP",
                "action": "notepad",
                "speech_response": "Bloknot matn muharriri ochildi!",
                "details": res
            }

        # 3. Fayllar / Explorer / Papka
        if any(w in t for w in ["fayllar", "provodnik", "papka", "explorer", "проводник", "kompyuterim"]):
            res = self.executor.open_app("explorer")
            return {
                "intent": "OPEN_APP",
                "action": "explorer",
                "speech_response": "Fayllar menejeri ochildi.",
                "details": res
            }

        # 4. Chrome / Brauzer
        if any(w in t for w in ["chrome", "xrom", "brauzer", "browser", "хром", "internet"]):
            res = self.executor.open_app("chrome")
            return {
                "intent": "OPEN_APP",
                "action": "chrome",
                "speech_response": "Internet brauzeri ochildi!",
                "details": res
            }

        # 5. Telegram
        if any(w in t for w in ["telegram", "telega", "tg", "телеграм"]):
            res = self.executor.open_app("telegram")
            return {
                "intent": "OPEN_APP",
                "action": "telegram",
                "speech_response": "Telegram ochildi, xizmatingizdaman!",
                "details": res
            }

        # 6. VS Code / Kod muharriri
        if any(w in t for w in ["vscode", "vs code", "kod", "dasturlash", "kodni och"]):
            res = self.executor.open_app("vscode")
            return {
                "intent": "OPEN_APP",
                "action": "vscode",
                "speech_response": "Visual Studio Code dasturlash muhiti ochildi!",
                "details": res
            }

        # 7. Terminal / CMD
        if any(w in t for w in ["terminal", "powershell", "cmd", "konsol", "buyruqlar satri"]):
            res = self.executor.open_app("terminal")
            return {
                "intent": "OPEN_APP",
                "action": "terminal",
                "speech_response": "Terminal konsoli ishga tushirildi.",
                "details": res
            }

        # 8. GitHub
        if any(w in t for w in ["github", "git xab", "git hub", "git", "гитхаб"]):
            res = self.executor.open_website("https://github.com/salomh46-rgb", "GitHub Profilingiz")
            return {
                "intent": "OPEN_WEBSITE",
                "action": "github",
                "speech_response": "GitHub profilingiz ochildi!",
                "details": res
            }

        # 9. YouTube
        if any(w in t for w in ["youtube", "yutub", "yu tub", "видео", "ютуб"]):
            res = self.executor.open_website("https://youtube.com", "YouTube")
            return {
                "intent": "OPEN_WEBSITE",
                "action": "youtube",
                "speech_response": "YouTube platformasi ochilmoqda!",
                "details": res
            }

        # 10. ChatGPT / Sun'iy Intellekt
        if any(w in t for w in ["chatgpt", "chat gpt", "ai", "sun'iy intellekt", "chatbot"]):
            res = self.executor.open_website("https://chatgpt.com", "ChatGPT")
            return {
                "intent": "OPEN_WEBSITE",
                "action": "chatgpt",
                "speech_response": "ChatGPT sahifasi ochildi!",
                "details": res
            }

        # 11. Shaxsiy Portfolio
        if any(w in t for w in ["portfolio", "portfolyo", "saytim", "shaxsiy sayt", "портфолио"]):
            res = self.executor.open_website("https://javohirbek-portfolio.vercel.app", "Shaxsiy Portfolio")
            return {
                "intent": "OPEN_WEBSITE",
                "action": "portfolio",
                "speech_response": "Shaxsiy portfolio saytingiz ochildi!",
                "details": res
            }

        # 12. Disk / Xotira holati (Disk status)
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

        # 13. Loyihalar ro'yxati (Projects)
        if any(w in t for w in ["loyiha", "proyekt", "loyihalar", "nimalar bor", "proyektlar", "proyektlarim", "проекты"]):
            projs = self.executor.list_projects()
            count = len(projs)
            sample = ", ".join(projs[:4])
            return {
                "intent": "PROJECTS_LIST",
                "action": "list_projects",
                "speech_response": f"D diskdagi ALLProjects papkasida jami {count} ta loyihangiz xavfsiz saqlanmoqda.",
                "details": {"total": count, "projects": projs}
            }

        # 14. Internetdan qidirish (Web Search)
        search_match = re.search(r"(?:qidir|izla|topib ber|haqida ma'lumot|search)\s+(.+)", t)
        if search_match:
            query = search_match.group(1).strip()
            res = self.executor.search_web(query)
            return {
                "intent": "SEARCH_WEB",
                "action": "search",
                "speech_response": f"Google orqali «{query}» qidirilmoqda.",
                "details": res
            }

        # 15. Salomlashish / Hol-ahvol
        if any(w in t for w in ["salom", "qalesan", "qalaysan", "ishlar", "nima gap", "привет", "здравствуй", "assalom"]):
            return {
                "intent": "GREETING",
                "action": "greeting",
                "speech_response": "Assalomu alaykum, xo'jayin! Men buyruqlaringizni bajarishga 100% tayyorman. Nima xizmat?",
                "details": {}
            }

        # 16. Tashakkur / Rahmat
        if any(w in t for w in ["rahmat", "raxmat", "tashakkur", "barakalla", "spasibo", "malades"]):
            return {
                "intent": "THANKS",
                "action": "thanks",
                "speech_response": "Arzimaydi xo'jayin! Har doim xizmatingizdaman.",
                "details": {}
            }

        # 17. Umumiy intellektual javob (General inquiry fallback)
        return {
            "intent": "GENERAL_ASSISTANT",
            "action": "answer",
            "speech_response": f"«{voice_text}» buyrug'ingiz qabul qilindi. Bajarishga tayyorman!",
            "details": {"raw_query": voice_text}
        }
