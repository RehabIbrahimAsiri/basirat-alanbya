import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="بصيرة الأنبياء", layout="wide")

# جعل المنصة من اليمين لليسار
st.markdown("""
    <style>
        html, body, [class*="css"] {
            direction: rtl;
            text-align: right;
        }
    </style>
""", unsafe_allow_html=True)

# إدراج الشعار في الزاوية العليا اليمنى
col1, col2 = st.columns([8, 1])
with col2:
    st.image("logo.png", width=120)

# العنوان والوصف في المنتصف
st.markdown(
    """
    <div style='text-align: center; padding-top: 10px;'>
        <h1 style='color: black;'>بصيرة الأنبياء</h1>
        <p style='font-size: 18px;'>حكمة النبوة.. لحل المشكلات الحياتية بإلهام وطمأنينة</p>
    </div>
    """,
    unsafe_allow_html=True
)

# تحميل البيانات
df = pd.read_excel("Rehab_cleaned.xlsx")
df.columns = df.columns.str.strip()

# اختيار الجانب الحياتي
aspect = st.selectbox("اختر الجانب الحياتي:", df['الجانب الحياتي'].unique())

# اختيار المشكلة
problems = df[df['الجانب الحياتي'] == aspect]['المشكلة'].unique()
selected_problem = st.selectbox("اختر المشكلة:", problems)

# عرض النصيحة
if selected_problem:
    row = df[(df['الجانب الحياتي'] == aspect) & (df['المشكلة'] == selected_problem)].iloc[0]
    st.markdown(f"""
    <div class="card" style='border: 1px solid #ccc; padding: 20px; border-radius: 10px; background-color: white;'>
        <h4 style='color:#001f3f;'>المشكلة: {row['المشكلة']}</h4>
        <p><b>النصيحة:</b> {row['النصيحة']}</p>
        <p><b>الدليل:</b> {row['الدليل']}</p>
        <p><b>مرجع الدليل:</b> {row['مرجع الدليل']}</p>
    </div>
    """, unsafe_allow_html=True)
