import streamlit as st
from google import genai
from google.genai import types

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

# شخصية Hope AI
hope_instruction = """
أنت الآن ذكاء اصطناعي عراقي متطور اسمك "Hope AI" (ذكاء الأمل).
رسالتك: تقديم المساعدة، نشر التفاؤل، وتبسيط العلم والعمل لكل العراقيين.
تحدث بالعربية الفصحى البسيطة وتفاعل ببراعة مع اللهجة العراقية بعبارات دافئة (مثل: عيوني، تدلل، عاشت إيدك).
قدم الإجابات على شكل نقاط ومنظمة جداً.
"""

# دمج المفتاح الخاص بك مباشرة داخل الكود ليعمل فوراً بدون الاعتماد على السيرفر
api_key = "AIzaSyDDjq5CmlGrYfDuzZsNmCuH9daqcddgiSo"
try:
    client = genai.Client(api_key=AIzaSyDDjq5CmlGrYfDuzZsNmCuH9daqcddgiSo)
    
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
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=hope_instruction,
                    temperature=0.7,
                )
            )
            
            full_response = response.text
            message_placeholder.markdown(full_response)
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})

except Exception as e:
    st.error("حدث خطأ أثناء الاتصال بالخادم الذكي. يرجى المحاولة لاحقاً.")