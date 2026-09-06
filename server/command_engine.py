import os
import re
from typing import Dict, Any, Optional
from server.system_actions import SystemActionExecutor

CYRILLIC_TO_LATIN = {
    'а':'a', 'б':'b', 'в':'v', 'г':'g', 'д':'d', 'е':'e', 'ё':'yo', 'ж':'j',
    'з':'z', 'и':'i', 'й':'y', 'к':'k', 'л':'l', 'м':'m', 'н':'n', 'о':'o',
    'п':'p', 'р':'r', 'с':'s', 'т':'t', 'у':'u', 'ф':'f', 'х':'x', 'ҳ':'h',
    'ч':'ch', 'ш':'sh', 'щ':'sh', 'ъ':'', 'ы':'i', 'ь':'', 'э':'e', 'ю':'yu',
    'я':'ya', 'ў':'o\'', 'ғ':'g\''
}

def normalize_uzbek(text: str) -> str:
    text = text.lower().strip()
    for c, l in CYRILLIC_TO_LATIN.items():
        text = text.replace(c, l)
    text = text.replace('‘', "'").replace('’', "'").replace('`', "'")
    text = re.sub(r'[^a-z0-9\s\'\+\-\*/=]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

class JasperVoiceCommandEngine:
    def __init__(self):
        self.executor = SystemActionExecutor()

    def _eval_math(self, text: str) -> Optional[str]:
        # Ko'paytirish (a * b)
        m = re.search(r'(\d+)\s*(?:ni|ta)?\s*(\d+)\s*(?:ga|bilan)?\s*(?:ko\'paytir|kopaytir|zarb|karra)', text)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            return f"{a} ni {b} ga ko'paytirganda {a * b} bo'ladi."
        
        # Bo'lish (a / b)
        m = re.search(r'(\d+)\s*(?:ni|ta)?\s*(\d+)\s*(?:ga)?\s*(?:bo\'l|bol|taqsim)', text)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            if b != 0:
                res = round(a / b, 2)
                return f"{a} ni {b} ga bo'lganda {res} chiqadi."

        # Qo'shish (a + b)
        m = re.search(r'(\d+)\s*(?:ga|bilan)?\s*(\d+)\s*(?:ni|ta)?\s*(?:qo\'sh|qosh|plus)', text)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            return f"{a} ga {b} ni qo'shganda {a + b} bo'ladi."

        # Ayirish (a - b)
        m = re.search(r'(\d+)\s*(?:dan)?\s*(\d+)\s*(?:ni|ta)?\s*(?:ayir|ol|minus)', text)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            return f"{a} dan {b} ni ayirganda {a - b} qoladi."
        
        return None

    def parse_and_execute(self, raw_text: str, custom_api_key: Optional[str] = None) -> Dict[str, Any]:
        norm = normalize_uzbek(raw_text)

        # 1. Matematik hisob-kitoblar (Math Engine)
        math_res = self._eval_math(norm)
        if math_res:
            return {
                "intent": "MATH_CALCULATION",
                "action": "math",
                "speech_response": math_res,
                "details": {"query": raw_text, "result": math_res}
            }

        # 2. Telegram (Desktop / Web)
        if any(w in norm for w in ["telegram", "telega", "tg", "tlg"]):
            res = self.executor.open_app("telegram")
            return {
                "intent": "OPEN_APP",
                "action": "telegram",
                "speech_response": "Telegram ilovasini ochdim, xo'jayin!",
                "details": res
            }

        # 3. Kalkulyator
        if any(w in norm for w in ["kalkulyator", "hisoblagich", "calculator", "calc", "hisobla"]):
            res = self.executor.open_app("kalkulyator")
            return {
                "intent": "OPEN_APP",
                "action": "calc",
                "speech_response": "Kalkulyator dasturi ochildi!",
                "details": res
            }

        # 4. Bloknot / Notepad
        if any(w in norm for w in ["bloknot", "notepad", "yozuv daftari", "matn muharriri", "daftar"]):
            res = self.executor.open_app("notepad")
            return {
                "intent": "OPEN_APP",
                "action": "notepad",
                "speech_response": "Bloknot dasturi ochildi.",
                "details": res
            }

        # 5. Explorer / Fayllar / Papkalar
        if any(w in norm for w in ["fayllar", "provodnik", "papka", "explorer", "kompyuterim", "mening kompyuterim"]):
            res = self.executor.open_app("explorer")
            return {
                "intent": "OPEN_APP",
                "action": "explorer",
                "speech_response": "Fayllar menejeri ochildi.",
                "details": res
            }

        # 6. Brauzer / Google Chrome
        if any(w in norm for w in ["chrome", "xrom", "brauzer", "browser", "internet"]):
            res = self.executor.open_app("chrome")
            return {
                "intent": "OPEN_APP",
                "action": "chrome",
                "speech_response": "Google Chrome brauzeri ochildi!",
                "details": res
            }

        # 7. VS Code / Dasturlash muhiti
        if any(w in norm for w in ["vscode", "vs code", "code", "kod", "dasturlash"]):
            res = self.executor.open_app("vscode")
            return {
                "intent": "OPEN_APP",
                "action": "vscode",
                "speech_response": "Visual Studio Code ochildi!",
                "details": res
            }

        # 8. Terminal / Konsol
        if any(w in norm for w in ["terminal", "powershell", "cmd", "konsol"]):
            res = self.executor.open_app("terminal")
            return {
                "intent": "OPEN_APP",
                "action": "terminal",
                "speech_response": "Terminal konsoli ochildi.",
                "details": res
            }

        # 9. YouTube
        if any(w in norm for w in ["youtube", "yutub", "video", "videolar"]):
            res = self.executor.open_website("https://youtube.com", "YouTube")
            return {
                "intent": "OPEN_WEBSITE",
                "action": "youtube",
                "speech_response": "YouTube ochilmoqda!",
                "details": res
            }

        # 10. GitHub
        if any(w in norm for w in ["github", "git", "git xab", "git hub"]):
            res = self.executor.open_website("https://github.com/salomh46-rgb", "GitHub Profilingiz")
            return {
                "intent": "OPEN_WEBSITE",
                "action": "github",
                "speech_response": "GitHub profilingiz ochildi!",
                "details": res
            }

        # 11. ChatGPT
        if any(w in norm for w in ["chatgpt", "chat gpt", "ai", "sun'iy intellekt", "chatbot"]):
            res = self.executor.open_website("https://chatgpt.com", "ChatGPT")
            return {
                "intent": "OPEN_WEBSITE",
                "action": "chatgpt",
                "speech_response": "ChatGPT sahifasi ochildi!",
                "details": res
            }

        # 12. Shaxsiy Portfolio
        if any(w in norm for w in ["portfolio", "portfolyo", "saytim", "shaxsiy sayt"]):
            res = self.executor.open_website("https://javohirbek-portfolio.vercel.app", "Shaxsiy Portfolio")
            return {
                "intent": "OPEN_WEBSITE",
                "action": "portfolio",
                "speech_response": "Shaxsiy portfolio saytingiz ochildi!",
                "details": res
            }

        # 13. Disk xotirasi (Audit)
        if any(w in norm for w in ["disk", "xotira", "joy", "qancha joy", "c disk", "d disk"]):
            stats = self.executor.get_disk_stats()
            c_free = stats.get("C", {}).get("free_gb", 0)
            d_free = stats.get("D", {}).get("free_gb", 0)
            return {
                "intent": "SYSTEM_AUDIT",
                "action": "disk_status",
                "speech_response": f"C diskda {c_free} gigabayt, D diskda esa {d_free} gigabayt bo'sh joy bor, xo'jayin!",
                "details": stats
            }

        # 14. Loyihalar
        if any(w in norm for w in ["loyiha", "proyekt", "loyihalar", "nimalar bor", "proyektlar"]):
            projs = self.executor.list_projects()
            count = len(projs)
            sample = ", ".join(projs[:4])
            return {
                "intent": "PROJECTS_LIST",
                "action": "list_projects",
                "speech_response": f"D diskdagi ALLProjects papkasida jami {count} ta loyihangiz xavfsiz saqlanmoqda.",
                "details": {"total": count, "projects": projs}
            }

        # 15. Internetdan qidiruv (Search)
        search_match = re.search(r"(?:qidir|izla|topib ber|haqida ma\'lumot|haqida|kim|nima)\s+(.+)", norm)
        if search_match:
            query = search_match.group(1).strip()
            res = self.executor.search_web(query)
            return {
                "intent": "SEARCH_WEB",
                "action": "search",
                "speech_response": f"Google orqali «{query}» bo'yicha qidiruv natijalarini ochdim.",
                "details": res
            }

        # 16. Salomlashish
        if any(w in norm for w in ["salom", "qalesan", "qalaysan", "ishlar", "nima gap", "assalom"]):
            return {
                "intent": "GREETING",
                "action": "greeting",
                "speech_response": "Assalomu alaykum xo'jayin! Buyruqlaringizni bajarishga to'liq tayyorman.",
                "details": {}
            }

        # 17. Minnatdorchilik
        if any(w in norm for w in ["rahmat", "raxmat", "tashakkur", "barakalla", "malades"]):
            return {
                "intent": "THANKS",
                "action": "thanks",
                "speech_response": "Arzimaydi xo'jayin! Har doim xizmatingizdaman.",
                "details": {}
            }

        # 18. Qobiliyatlar / Nima qila olasan
        if any(w in norm for w in ["nima qilasan", "nima qila olasan", "imkoniyat", "nimalarni bilasan", "yordam"]):
            return {
                "intent": "HELP_CAPABILITIES",
                "action": "capabilities",
                "speech_response": "Men kompyuteringizdagi istalgan dasturlarni ochaman, Telegram, Kalkulyator, YouTube-ga kiraman, disk xotirasini aytaman, hisob-kitob qilaman va buyruqlaringizni bajaraman!",
                "details": {}
            }

        # 19. Gemini AI Fallback (if API key available) or Conversational fallback
        api_key = custom_api_key or os.environ.get("GEMINI_API_KEY")
        if api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                sys_prompt = "Sen 'Jasper AI' nomli o'zbekcha aqlli shaxsiy kompyuter yordamchisisan. Foydalanuvchi bilan o'zbek tilida qisqa, aniq, odobli va jonli gaplash. Maksimal 2 jumla bilan javob ber."
                prompt = f"{sys_prompt}\n\nFoydalanuvchi: {raw_text}\nJasper AI:"
                gemini_res = model.generate_content(prompt)
                ai_text = gemini_res.text.strip()
                if ai_text:
                    return {
                        "intent": "GEMINI_AI_REASONING",
                        "action": "ai_response",
                        "speech_response": ai_text,
                        "details": {"raw_query": raw_text}
                    }
            except Exception as e:
                print(f"Gemini AI error: {e}")

        # 20. Umumiy Aqlli Qabul Qilish (Conversational fallback)
        return {
            "intent": "GENERAL_ASSISTANT",
            "action": "answer",
            "speech_response": f"«{raw_text}» buyrug'ingizni qabul qildim. Kompyuteringizda har qanday vazifani bajarishga tayyorman!",
            "details": {"raw_query": raw_text}
        }
