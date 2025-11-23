from datetime import datetime
import random

# Try to import LangChain components
try:
    from langchain_community.llms import Ollama
    HAS_LANGCHAIN = True
except ImportError:
    HAS_LANGCHAIN = False

# Try to import translation package
try:
    from deep_translator import GoogleTranslator
    HAS_TRANSLATOR = True
except ImportError:
    HAS_TRANSLATOR = False

def get_zodiac_sign(day: int, month: int) -> str:
    """
    Simple logic to determine zodiac sign based on day and month.
    """
    if (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "Pisces"
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    else:
        return "Capricorn"

def translate_stub(text: str, target_lang: str) -> str:
    """
    Stub for NLLB / IndicTrans2.
    Uses deep_translator as a lightweight proxy for this assignment.
    """
    if target_lang.lower() == "english":
        return text

    if not HAS_TRANSLATOR:
        return text + " [Install 'deep-translator' for Hindi]"
    
    try:
        # Map 'Hindi' to 'hi'
        lang_code = "hi" if target_lang.lower() == "hindi" else "en"
        
        # NOTE: To use real NLLB (requires ~1GB+ download):
        # from transformers import pipeline
        # translator = pipeline("translation", model="facebook/nllb-200-distilled-600M")
        # return translator(text, src_lang="eng_Latn", tgt_lang="hin_Deva")[0]['translation_text']
        
        # Using deep_translator for immediate results:
        return GoogleTranslator(source='auto', target=lang_code).translate(text)
    except Exception as e:
        print(f"Translation Error: {e}")
        return text

def generate_insight(name: str, zodiac: str, language: str = "English") -> str:
    """
    Generates insight in English first (via LLM), then translates using a package.
    """
    insight_text = ""

    # 1. Generate English Content (via LLM)
    if HAS_LANGCHAIN:
        try:
            llm = Ollama(model="llama3") 
            english_prompt = (
                f"You are a mystical astrologer. "
                f"Give a short, 2-sentence daily horoscope for {name}, who is a {zodiac}. "
                f"Focus on positive energy and practical advice."
            )
            insight_text = llm.invoke(english_prompt)
        except Exception as e:
            print(f"LLM Connection Error: {e}. Falling back to dummy data.")
            pass
    
    # 2. Fallback if LLM failed or not present
    if not insight_text:
        english_templates = [
            f"Today, your {zodiac} nature will help you handle unexpected work pressure, {name}.",
            f"{name}, your innate leadership and warmth as a {zodiac} will shine today.",
            f"Embrace spontaneity today, {name}. The stars align for {zodiac}s to make bold moves.",
            f"Caution is advised in financial matters today, {name}. Trust your {zodiac} intuition."
        ]
        insight_text = random.choice(english_templates)

    # 3. Translate using the package stub
    return translate_stub(insight_text, language)