import streamlit as st
import pandas as pd
import os
from openpyxl import load_workbook

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

# تحديث عداد الزوار
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

# دالة حفظ التقييم في ملف Excel
def save_feedback_excel(problem, result):
    file_path = "feedback_data.xlsx"
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=["المشكلة", "التقييم"])
        df.to_excel(file_path, index=False)
    wb = load_workbook(file_path)
    ws = wb.active
    ws.append([problem, result])
    wb.save(file_path)

# حساب نسبة الإعجاب
def calculate_like_ratio(problem):
    file_path = "feedback_data.xlsx"
    if not os.path.exists(file_path):
        return None
    df_feedback = pd.read_excel(file_path)
    problem_data = df_feedback[df_feedback["المشكلة"] == problem]
    if len(problem_data) == 0:
        return None
    likes = len(problem_data[problem_data["التقييم"] == "مفيدة"])
    total = len(problem_data)
    return int((likes / total) * 100)

# الشعار + عداد الزوار (العداد في اليسار)
col1, col2 = st.columns([1, 8])
with col1:
    st.markdown(f"<div style='font-size: 16px; color:#003366;'>👥 عدد الزوار: <strong>{visitor_count}</strong></div>", unsafe_allow_html=True)
with col2:
    st.image("logo.png", width=120)

# العنوان والوصف
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
df = pd.read_excel("Basirat_Al_Anbiya.xlsx")
df.columns = df.columns.str.strip()

# اختيار الجانب والمشكلة
aspect = st.selectbox("اختر الجانب الحياتي:", df['الجانب الحياتي'].unique())
problems = df[df['الجانب الحياتي'] == aspect]['المشكلة'].unique()
selected_problem = st.selectbox("اختر المشكلة:", problems)

# عرض البطاقة + التقييم + النسبة
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

    # نسبة الإعجاب
    ratio = calculate_like_ratio(row['المشكلة'])
    if ratio is not None:
        st.markdown(f"<p style='color:#003366;'>📊 نسبة الرضا عن هذه النصيحة: <strong>{ratio}%</strong></p>", unsafe_allow_html=True)

    # أزرار التقييم
    col_like, col_dislike = st.columns([1, 1])
    with col_like:
        if st.button("👍 مفيدة"):
            save_feedback_excel(row['المشكلة'], "مفيدة")
            st.success("شكرًا! سعداء بأنها أفادتك 🌟")
    with col_dislike:
        if st.button("👎 لم تفدني"):
            save_feedback_excel(row['المشكلة'], "غير مفيدة")
            st.warning("شكرًا لملاحظتك. سنعمل على تحسين النصيحة بإذن الله.")

# قسم صندوق الاقتراحات
st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)
with st.form("suggestion_form"):
    st.markdown("<h5 style='color:#003366;'>🌿 هل لديك اقتراح يُسهم في تحسين المنصة؟</h5>", unsafe_allow_html=True)
    suggestion = st.text_area("اكتب اقتراحك هنا", placeholder="مثال: أقترح إضافة نصيحة عن الشعور بالذنب...")
    send = st.form_submit_button("إرسال")
    if send and suggestion.strip():
        st.info("📬 هل ترغب في إرسال الاقتراح الآن بالبريد؟")
        suggestion_link = f"mailto:rahooob64@gmail.com?subject=اقتراح%20لمنصة%20بصيرة%20الأنبياء&body={suggestion}"
        st.markdown(f"""
            <a href='{suggestion_link}' target='_blank' style='color:#001f3f; font-weight:bold; font-size:18px;'>
            ✉️ اضغط هنا لإرسال الاقتراح بالبريد
            </a>
        """, unsafe_allow_html=True)
