import streamlit as st
import google.generativeai as genai
from streamlit_gsheets import GSheetsConnection
import pandas as pd

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
    .stButton>button { background-color: #004aad; color: white !important; border-radius: 20px; border: none; padding: 0.6rem 2rem; font-weight: bold; width: 100%; }
    .stButton>button:hover { background-color: #003580; box-shadow: 0px 4px 15px rgba(0, 74, 173, 0.3); }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 2px solid #e1e8ed; }
    .auth-box { max-width: 450px; margin: 0 auto; background: white; padding: 2.5rem; border-radius: 15px; box-shadow: 0px 4px 20px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. ربط قاعدة البيانات (Google Sheets)
# ==========================================
# ⚠️ ضع هنا رابط الجدول الخاص بك الذي نسخته في الخطوة الأولى
GSHEET_URL = "https://docs.google.com/spreadsheets/d/1dO5BahsAQxNaFCF6Igu60NULyd3_gGTwAIP-bCexs2c/edit?gid=0#gid=0"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=GSHEET_URL, ttl="0d")
except:
    df = pd.DataFrame(columns=["name", "email", "password"])

# إدارة جلسة الدخول
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# ==========================================
# 3. واجهات نظام الحسابات (تسجيل ودخول)
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<div class='auth-box'>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluent/96/000000/sparkling.png", width=70)
    
    tab1, tab2 = st.tabs(["🔐 تسجيل الدخول", "📝 إنشاء حساب جديد"])
    
    # واجهة تسجيل الدخول
    with tab1:
        login_email = st.text_input("الإيميل الإلكتروني", key="login_email_input").strip().lower()
        login_pass = st.text_input("كلمة المرور", type="password", key="login_pass_input")
        
        if st.button("دخول للمنصة"):
            if login_email and login_pass:
                user_row = df[df["email"] == login_email]
                if not user_row.empty and str(user_row.iloc[0]["password"]) == str(login_pass):
                    st.session_state.logged_in = True
                    st.session_state.user_name = user_row.iloc[0]["name"]
                    st.success(f"مرحباً بك مجدداً {st.session_state.user_name} ✨")
                    st.rerun()
                else:
                    st.error("❌ الإيميل أو رمز المرور غير صحيح!")
            else:
                st.warning("يرجى ملء جميع الحقول")

    # واجهة إنشاء الحساب الجديد
    with tab2:
        new_name = st.text_input("الاسم الكامل", key="new_name_input").strip()
        new_email = st.text_input("الإيميل الحقيقي", key="new_email_input").strip().lower()
        new_pass = st.text_input("اختر كلمة مرور", type="password", key="new_pass_input")
        
        if st.button("تأكيد إنشاء الحساب"):
            if new_name and new_email and new_pass:
                if new_email in df["email"].values:
                    st.error("⚠️ هذا الإيميل مسجل مسبقاً! انتقل لتبويب تسجيل الدخول.")
                else:
                    # إضافة الحساب الجديد لملف الإكسل فوراً
                    new_user = pd.DataFrame([[new_name, new_email, new_pass]], columns=["name", "email", "password"])
                    updated_df = pd.concat([df, new_user], ignore_index=True)
                    conn.update(spreadsheet=GSHEET_URL, data=updated_df)
                    st.success("🎉 تم إنشاء حسابك بنجاح! يمكنك الآن الدخول من التبويب الأول.")
            else:
                st.warning("يرجى ملء جميع الحقول المطلوبة")
                
    st.markdown("</div>", unsafe_allow_html=True)
    # ==========================================
# 4. تشغيل المنصة الأساسية بعد نجاح الدخول
# ==========================================
else:
    # القائمة الجانبية مع زر تسجيل الخروج
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; font-size: 50px;'>✨</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center;'>مرحباً {st.session_state.user_name}</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666;'>نزرع الأمل بالمعرفة</p>", unsafe_allow_html=True)
        st.markdown("---")
        if st.sidebar.button("تسجيل الخروج"):
            st.session_state.logged_in = False
            st.session_state.user_name = ""
            st.rerun()
        st.markdown("---")
        st.markdown("### عن المبادرة 🇮🇶")
        st.write("منصة Hope AI مفتوحة لخدمة الطلاب والخريجين لتطوير المهارات.")
        st.caption("إشراف وتطوير وطني 100%")

    # الواجهة الرئيسية للدردشة لـ Hope AI
    st.title("مرحباً بك في Hope AI ✨")
    st.markdown("#### بوابتك الذكية لمستقبل أفضل.. كيف يمكنني مساعدتك اليوم؟")
    st.write("---")

    # تهيئة مفتاح الـ API للذكاء الاصطناعي
    api_key = "AIzaSyAiQswVwv3CUy8jqB-dTPCGGTP7t8KihLg"
    genai.configure(api_key=api_key)

    hope_instruction = """
    أنت الآن ذكاء اصطناعي عراقي متطور اسمك "Hope AI" (ذكاء الأمل).
    رسالتك: تقديم المساعدة، نشر التفاؤل، وتبسيط العلم والعمل لكل العراقيين.
    تحدث بالعربية الفصحى البسيطة وتفاعل ببراعة مع اللهجة العراقية بعبارات دافئة (مثل: عيوني، تدلل، عاشت إيدك).
    قدم الإجابات على شكل نقاط ومنظمة جداً وبأحدث مخرجات عام 2026.
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
                
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash",
                    system_instruction=hope_instruction
                )
                
                response = model.generate_content(prompt)
                full_response = response.text
                message_placeholder.markdown(full_response)
                
            st.session_state.messages.append({"role": "assistant", "content": full_response})

    except Exception as e:
        st.error("حدث خطأ في الاتصال بالخادم الذكي. يرجى إعادة المحاولة لاحقاً.")