import streamlit as st
import google.generativeai as genai

st.title("فحص اتصال Hope AI 🛠️")

api_key = "AIzaSyAiQswVwv3CUy8jqB-dTPCGGTP7t8KihLg"
genai.configure(api_key=api_key)

if prompt := st.chat_input("اكتب أي شيء هنا للفحص.."):
    st.write(f"جاري إرسال النص: {prompt}")
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        st.success("🎉 الاتصال نجح! المفتاح شغال 100%")
        st.write(response.text)
    except Exception as e:
        st.error("❌ فشل الاتصال بالسيرفر!")
        st.warning(f"السبب الحقيقي للخطأ هو: {str(e)}")