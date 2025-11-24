from datetime import datetime
import random

# --- Imports for Optional Libraries ---
try:
    from langchain_community.llms import Ollama
    HAS_LANGCHAIN = True
except ImportError:
    HAS_LANGCHAIN = False

try:
    from deep_translator import GoogleTranslator
    HAS_TRANSLATOR = True
except ImportError:
    HAS_TRANSLATOR = False

# --- New Imports for Vedic Calc ---
try:
    import swisseph as swe
    from geopy.geocoders import Nominatim
    HAS_VEDIC_LIBS = True
except ImportError:
    HAS_VEDIC_LIBS = False

# ==========================================
# 1. Vedic Calculation Logic
# ==========================================

def get_coordinates(city_name: str):
    """Converts city name to lat/lon using Geopy."""
    if not HAS_VEDIC_LIBS:
        return 0.0, 0.0
    
    try:
        geolocator = Nominatim(user_agent="astro_app")
        location = geolocator.geocode(city_name)
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        print(f"Geocoding error: {e}")
    return 0.0, 0.0

def get_vedic_details(date_obj: datetime, time_str: str, place: str):
    """Calculates Vedic Rasi (Moon Sign) and Nakshatra."""
    default_data = {"rasi": "Unknown", "nakshatra": "Unknown"}
    if not HAS_VEDIC_LIBS: return default_data

    try:
        lat, lon = get_coordinates(place)
        try:
            if len(time_str) == 5: t = datetime.strptime(time_str, "%H:%M")
            else: t = datetime.strptime(time_str, "%H:%M:%S")
            hour = t.hour + t.minute / 60.0
        except: hour = 12.0

        jd = swe.julday(date_obj.year, date_obj.month, date_obj.day, hour)
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        result = swe.calc_ut(jd, swe.MOON, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
        
        moon_long = result[0][0] if isinstance(result[0], (tuple, list)) else result[0]

        rasi_names = ["Mesha (Aries)", "Vrishabha (Taurus)", "Mithuna (Gemini)", "Karka (Cancer)", "Simha (Leo)", "Kanya (Virgo)", "Tula (Libra)", "Vrishchika (Scorpio)", "Dhanu (Sagittarius)", "Makara (Capricorn)", "Kumbha (Aquarius)", "Meena (Pisces)"]
        nakshatra_names = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
        
        return {
            "rasi": rasi_names[int(moon_long / 30) % 12],
            "nakshatra": nakshatra_names[int(moon_long / 13.333333) % 27]
        }
    except Exception as e:
        print(f"Vedic Error: {e}")
        return default_data

# ==========================================
# 2. Core Logic
# ==========================================

def get_zodiac_sign(day: int, month: int) -> str:
    if (month == 1 and day >= 20) or (month == 2 and day <= 18): return "Aquarius"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20): return "Pisces"
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19): return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20): return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20): return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22): return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22): return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22): return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22): return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21): return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21): return "Sagittarius"
    else: return "Capricorn"

def translate_stub(text: str, target_lang: str) -> str:
    if target_lang.lower() == "english": return text
    if not HAS_TRANSLATOR: return text
    try:
        lang_code = "hi" if target_lang.lower() == "hindi" else "en"
        return GoogleTranslator(source='auto', target=lang_code).translate(text)
    except: return text

def generate_insight(name: str, zodiac: str, category: str = "General", language: str = "English", vedic_data: dict = None) -> str:
    """Standard non-streaming generation (used for fallback/translation)."""
    insight_text = ""
    vedic_info = f" Vedic Moon: {vedic_data['rasi']}." if vedic_data and vedic_data.get("rasi") != "Unknown" else ""

    if HAS_LANGCHAIN:
        try:
            llm = Ollama(model="llama3") 
            prompt = (
                f"You are a mystical astrologer. "
                f"Give a short, 2-sentence daily horoscope for {name}, a {zodiac}.{vedic_info} "
                f"Focus specifically on {category} advice."
            )
            insight_text = llm.invoke(prompt)
        except: pass
    
    if not insight_text:
        templates = [
            f"Your {zodiac} energy favors {category} today, {name}.",
            f"{name}, focus on {category} as the stars align for {zodiac}.",
        ]
        insight_text = random.choice(templates)

    return translate_stub(insight_text, language)

def generate_insight_stream(name: str, zodiac: str, category: str, language: str, vedic_data: dict = None):
    """Generator for streaming response."""
    vedic_info = f" Vedic Moon: {vedic_data['rasi']}." if vedic_data and vedic_data.get("rasi") != "Unknown" else ""
    
    # 1. Try Streaming (English Only)
    if HAS_LANGCHAIN and language.lower() == "english":
        try:
            llm = Ollama(model="llama3")
            prompt = (
                f"You are a mystical astrologer. "
                f"Give a short, 2-sentence daily horoscope for {name}, a {zodiac}.{vedic_info} "
                f"Focus specifically on {category} advice."
            )
            for chunk in llm.stream(prompt):
                yield chunk
            return
        except Exception as e:
            print(f"Stream Error: {e}")
    
    # 2. Fallback / Translation (Non-streaming)
    # If Hindi or LLM fails, generate full text and yield it as one chunk
    full_text = generate_insight(name, zodiac, category, language, vedic_data)
    return full_text
