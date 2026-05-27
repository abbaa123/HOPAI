import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. إعدادات الهوية البصرية لـ Hope AI
# ==========================================
st.set_page_config(
    page_title="Hope AI - ذكاء الأمل",
    page_icon="✨",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #f0f4f8; }
    h1, h2, h3 { color: #004aad !important; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { background-color: #004aad; color: white !important; border-radius: 20px; border: none; padding: 0.6rem 2rem; font-weight: bold; }
    .stButton>button:hover { background-color: #003580; box-shadow: 0px 4px 15px rgba(0, 74, 173, 0.3); }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 2px solid #e1e8ed; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. القائمة الجانبية (شعار المنصة)
# ==========================================
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 50px;'>✨</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Hope AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>نزرع الأمل بالمعرفة</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### عن المبادرة 🇮🇶")
    st.write("منصة Hope AI مفتوحة ومجانية بالكامل لخدمة جميع الطلاب والخريجين وأبناء الشعب العراقي لتطوير المهارات وبناء القدرات.")
    st.caption("إشراف وتطوير وطني 100%")

# ==========================================
# 3. الواجهة الرئيسية للدردشة
# ==========================================
st.title("مرحباً بك في Hope AI ✨")
st.markdown("#### بوابتك الذكية لمستقبل أفضل.. كيف يمكنني مساعدتك اليوم؟")
st.write("---")

# ضبط المفتاح والتهيئة
api_key = "AIzaSyAiQswVwv3CUy8jqB-dTPCGGTP7t8KihLg"
genai.configure(api_key=api_key)

# شخصية Hope AI التوجيهية (باستخدام أحدث الأساليب)
hope_instruction = """
أنت الآن ذكاء اصطناعي عراقي متطور اسمك "Hope AI" (ذكاء الأمل).
رسالتك: تقديم المساعدة، نشر التفاؤل، وتبسيط العلم والعمل لكل العراقيين.
تحدث بالعربية الفصحى البسيطة وتفاعل ببراعة مع اللهجة العراقية بعبارات دافئة (مثل: عيوني، تدلل، عاشت إيدك).
قدم الإجابات على شكل نقاط ومنظمة جداً وبأحدث المعلومات المتاحة لعام 2026.
"""

try:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("اسأل Hope AI عن أي شيء.."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant", avatar="✨"):
            message_placeholder = st.empty()
            
            # استخدام أحدث نموذج متوفر ومستقر للدردشة السريعة: gemini-2.5-flash
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                system_instruction=hope_instruction
            )
            
            response = model.generate_content(prompt)
            full_response = response.text
            message_placeholder.markdown(full_response)
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})

except Exception as e:
    st.error("حدث خطأ في الاتصال بالنسخة المحدثة للسريرفر الذكي. يرجى إعادة المحاولة.")