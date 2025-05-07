import streamlit as st
import pandas as pd
import csv
import os
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="بصيرة الأنبياء", layout="wide")

# اتجاه النص من اليمين لليسار
st.markdown("""
    <style>
        html, body, [class*="css"] {
            direction: rtl;
            text-align: right;
        }
    </style>
""", unsafe_allow_html=True)

# عداد الزوار (يُخزن في ملف نصي)
def update_counter():
    if not os.path.exists("counter.txt"):
        with open("counter.txt", "w") as f:
            f.write("0")
    with open("counter.txt", "r+") as f:
        count = int(f.read())
        count += 1
        f.seek(0)
        f.write(str(count))
        f.truncate()
    return count

visitor_count = update_counter()

# دالة لحفظ التقييمات في CSV
def save_feedback_to_csv(problem, rating):
    filename = "feedback_data.csv"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["المشكلة", "التقييم", "الوقت"])
        writer.writerow([problem, rating, now])

# الشعار وعدد الزوار
col1, col2 = st.columns([8, 1])
with col1:
    st.image("logo.png", width=120)
with col2:
    st.markdown(f"<div style='font-size: 16px; color:#003366; text-align:left;'>👥 عدد الزوار: <strong>{visitor_count}</strong></div>", unsafe_allow_html=True)

# العنوان والوصف
st.markdown("""
    <div style='text-align: center; padding-top: 10px;'>
        <h1 style='color: black;'>بصيرة الأنبياء</h1>
        <p style='font-size: 18px;'>حكمة النبوة.. لحل المشكلات الحياتية بإلهام وطمأنينة</p>
    </div>
""", unsafe_allow_html=True)

# تحميل البيانات من ملف Excel
df = pd.read_excel("Basirat_Al_Anbiya.xlsx")
df.columns = df.columns.str.strip()

# اختيار الجانب الحياتي والمشكلة
aspect = st.selectbox("اختر الجانب الحياتي:", df['الجانب الحياتي'].unique())
problems = df[df['الجانب الحياتي'] == aspect]['المشكلة'].unique()
selected_problem = st.selectbox("اختر المشكلة:", problems)

# عرض البطاقة + التقييم
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

    col_like, col_dislike = st.columns([1, 1])
    with col_like:
        if st.button("👍 مفيدة"):
            save_feedback_to_csv(row['المشكلة'], "مفيدة")
            st.success("شكرًا! سعداء بأنها أفادتك 🌟")
    with col_dislike:
        if st.button("👎 لم تفدني"):
            save_feedback_to_csv(row['المشكلة'], "غير مفيدة")
            st.warning("شكرًا لملاحظتك. سنعمل على تحسين النصيحة بإذن الله.")

# صندوق الاقتراحات عبر Google Form
st.markdown("""
    <hr style='border: 1px solid #ccc; margin-top: 40px;'>
    <div style='
        background-color: #f9f9f9;
        border: 2px dashed #003366;
        border-radius: 12px;
        padding: 25px;
        margin: 30px 0;
        text-align: center;
        font-size: 18px;
        color: #003366;
    '>
        🌿 <strong>هل لديك اقتراح يُسهم في تحسين منصة بصيرة الأنبياء؟</strong><br><br>
        ✍️ يسعدنا استقبال أفكارك وملاحظاتك بكل حب واهتمام.<br><br>
        <a href="https://forms.gle/vdBTMaqKXCoaM64c6" target="_blank"
           style="color: white; background-color: #003366; padding: 12px 25px;
                  text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block;">
            📩 اضغط هنا لتقديم اقتراحك
        </a>
    </div>
""", unsafe_allow_html=True)
