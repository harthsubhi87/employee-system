import streamlit as st
import pandas as pd
import os
import io

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="نظام إدارة الموظفين الزجاجي",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تصميم CSS بالأنماط الزجاجية المائية والمحاذاة للوسط
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 50%, #e1f5fe 100%);
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.65);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        padding: 24px;
        margin-bottom: 25px;
    }
    
    p, h1, h2, h3, h4, label, input, select, textarea {
        text-align: center !important;
    }
    .stTextInput>div>div>input {
        text-align: center !important;
        border-radius: 10px;
    }
    
    .stButton>button {
        border-radius: 12px;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
        border: none;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

DATA_FILE = "Data_Employees.xlsx"

# 3. تحميل البيانات
@st.cache_data(ttl=1)
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_excel(DATA_FILE)
        df.columns = [str(col).strip() for col in df.columns]
        return df
    else:
        cols = ['الاسم الرباعي', 'الرقم الوظيفي', 'العنوان الوظيفي', 'الشهادة', 'الجنس', 
                'الدرجة الوظيفية', 'المرحلة', 'الراتب الاسمي', 'الاختصاص العام', 'الاختصاص الدقيق', 
                'سنة التخرج', 'رقم امر التعيين', 'تاريخ التعيين', 'تاريخ المباشرة', 'رقم الهاتف', 
                'اسم الام الثلاثي', 'الحالة الزوجية', 'اسم الزوجة', 'الرقم الوطني', 'تاريخ اصداره', 
                'تاريخ التولد', 'جهة الإصدار', 'محل الولادة', 'رقم البطاقة التموينية', 'محلة - زقاق - دار', 
                'رقم وثيقة التخرج', 'تاريخ اصدار وثيقة التخرج', 'رقم صحة الصدور', 'تاريخ صحة الصدور', 
                'عنوان السكن', 'اقرب نقطة دالة', 'رقم الهوية', 'الملاحظات']
        return pd.DataFrame(columns=cols)

def save_data(df):
    df.to_excel(DATA_FILE, index=False)
    st.cache_data.clear()

df = load_data()

# الهيدر الرئيسي
st.markdown("""
<div class="glass-card">
    <h1 style="color: #0369a1; margin:0;">💎 نظام إدارة وقاعدة بيانات الموظفين - التصميم الزجاجي المائي</h1>
    <p style="color: #0284c7; font-size: 1.1rem;">واجهة تفاعلية شاملة بالربط مع Streamlit & GitHub</p>
</div>
""", unsafe_allow_html=True)

# 4. القائمة الجانبية (شريط الأوامر)
st.sidebar.markdown("<h2 style='color:#0369a1;'>⚙️ لوحة الأوامر</h2>", unsafe_allow_html=True)
action = st.sidebar.radio(
    "اختر العملية المطلوبة:",
    ["🔍 استعلام وعرض", "➕ إضافة موظف", "✏️ تعديل بيانات", "❌ حذف موظف", "📥 تحميل / استيراد Excel", "📤 تصدير البيانات"]
)

# --- 1. أمر الاستعلام والعرض ---
if action == "🔍 استعلام وعرض":
    st.markdown("<div class='glass-card'><h3>🔍 استعلام وعرض بيانات الموظفين</h3>", unsafe_allow_html=True)
    search_term = st.text_input("أدخل الاسم أو الرقم الوظيفي للبحث:")
    
    filtered_df = df.copy()
    if search_term:
        filtered_df = df[
            df.astype(str).apply(lambda row: row.str.contains(search_term, case=False).any(), axis=1)
        ]
        st.success(f"تم العثور على {len(filtered_df)} سجل")
    
    st.dataframe(filtered_df, use_container_width=True)
    
    if st.button("🖨️ طباعة التقرير الحالي"):
        st.info("يمكنك استخدام خيار الطباعة المباشر من المتصفح (Ctrl + P) لطباعة هذه الشاشة بتنسيق زجاجي نقي.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 2. أمر إضافة موظف ---
elif action == "➕ إضافة موظف":
    st.markdown("<div class='glass-card'><h3>➕ إضافة موظف جديد</h3>", unsafe_allow_html=True)
    with st.form("add_form"):
        cols_list = list(df.columns)
        new_data = {}
        
        col1, col2 = st.columns(2)
        for i, col_name in enumerate(cols_list):
            if i % 2 == 0:
                new_data[col_name] = col1.text_input(col_name)
            else:
                new_data[col_name] = col2.text_input(col_name)
                
        submit = st.form_submit_button("💾 حفظ الموظف الجديد")
        if submit:
            new_row = pd.DataFrame([new_data])
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.success("تمت إضافة الموظف بنجاح إلى قاعدة البيانات!")

    st.markdown("</div>", unsafe_allow_html=True)

# --- 3. أمر تعديل بيانات ---
elif action == "✏️ تعديل بيانات":
    st.markdown("<div class='glass-card'><h3>✏️️ تعديل بيانات موظف</h3>", unsafe_allow_html=True)
    if not df.empty:
        emp_list = df['الاسم الرباعي'].tolist() if 'الاسم الرباعي' in df.columns else df.iloc[:,0].tolist()
        selected_emp = st.selectbox("اختر الموظف المراد تعديل بياناته:", emp_list)
        
        emp_index = df[df['الاسم الرباعي'] == selected_emp].index[0]
        emp_data = df.loc[emp_index]
        
        with st.form("edit_form"):
            updated_data = {}
            col1, col2 = st.columns(2)
            for i, col_name in enumerate(df.columns):
                val = str(emp_data[col_name]) if pd.notna(emp_data[col_name]) else ""
                if i % 2 == 0:
                    updated_data[col_name] = col1.text_input(col_name, value=val)
                else:
                    updated_data[col_name] = col2.text_input(col_name, value=val)
                    
            update_btn = st.form_submit_button("🔄 تحديث البيانات")
            if update_btn:
                for k, v in updated_data.items():
                    df.loc[emp_index, k] = v
                save_data(df)
                st.success("تم تحديث البيانات بنجاح!")
    else:
        st.warning("قاعدة البيانات فارغة حالياً.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 4. أمر الحذف ---
elif action == "❌ حذف موظف":
    st.markdown("<div class='glass-card'><h3>❌ حذف موظف من النظام</h3>", unsafe_allow_html=True)
    if not df.empty:
        emp_list = df['الاسم الرباعي'].tolist() if 'الاسم الرباعي' in df.columns else df.iloc[:,0].tolist()
        selected_emp = st.selectbox("اختر الموظف المراد حذفه:", emp_list)
        
        if st.button("🚨 تأكيد الحذف النهائي"):
            df = df[df['الاسم الرباعي'] != selected_emp]
            save_data(df)
            st.success(f"تم حذف سجل الموظف ({selected_emp}) بنجاح.")
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- 5. استيراد ملف Excel ---
elif action == "📥 تحميل / استيراد Excel":
    st.markdown("<div class='glass-card'><h3>📥 استيراد قاعدة بيانات من ملف Excel خارجي</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("اختر ملف Excel (.xlsx):", type=["xlsx", "xls"])
    if uploaded_file is not None:
        new_df = pd.read_excel(uploaded_file)
        if st.button("دمج مع قاعدة البيانات الحالية"):
            df = pd.concat([df, new_df], ignore_index=True)
            save_data(df)
            st.success("تم استيراد البيانات ودمجها بنجاح!")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 6. تصدير البيانات ---
elif action == "📤 تصدير البيانات":
    st.markdown("<div class='glass-card'><h3>📤 تصدير قاعدة البيانات</h3>", unsafe_allow_html=True)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='الموظفين')
    processed_data = output.getvalue()
    
    st.download_button(
        label="📥 تحميل قاعدة البيانات كملف Excel",
        data=processed_data,
        file_name="قاعدة_بيانات_الموظفين_المصدرة.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    st.markdown("</div>", unsafe_allow_html=True)