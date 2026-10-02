import streamlit as st
import pandas as pd
import os
import io

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="نظام إدارة الموظفين - المائي",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تصميم CSS المتقدم لدعم الاتجاه من اليمين إلى اليسار (RTL) بالكامل
st.markdown("""
<style>
    /* تطبيق الاتجاه من اليمين لليسار على كامل الواجهة */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        direction: rtl !important;
        text-align: right !important;
    }

    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 50%, #e1f5fe 100%);
    }
    
    /* تثبيت لوحة التحكم الجانبية في اليمين وتعديل حوافها الزجاجية */
    [data-testid="stSidebar"] {
        right: 0 !important;
        left: auto !important;
        background: rgba(255, 255, 255, 0.5) !important;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-left: 1px solid rgba(255, 255, 255, 0.7) !important;
        border-right: none !important;
        border-radius: 20px 0 0 20px !important;
        box-shadow: -4px 0 24px rgba(0,0,0,0.03) !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background-color: transparent !important;
        background-image: none !important;
    }
    
    .stDeployButton, #MainMenu, header, footer {
        visibility: hidden !important;
    }
    
    [data-testid="stAppViewContainer"] {
        padding-top: 1.5rem;
    }

    /* محاذاة كافة النصوص والحقول والمدخلات للوسط */
    p, h1, h2, h3, h4, label, input, select, textarea {
        text-align: center !important;
    }
    
    /* الجداول تبدأ وتترتب من اليمين إلى اليسار */
    [data-testid="stDataFrame"], div[role="grid"] {
        direction: rtl !important;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.05);
        padding: 25px;
        margin-bottom: 25px;
    }
    
    .mock-header {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(10px);
        padding: 10px 20px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.8);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        color: #0369a1;
        font-weight: bold;
        direction: rtl !important;
    }

    .stButton>button {
        border-radius: 12px;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
        border: none;
        background: rgba(255, 255, 255, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.9);
        color: #0284c7 !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        background: rgba(255, 255, 255, 0.95) !important;
    }
    
    .stTextInput>div>div>input {
        text-align: center !important;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid #bae6fd;
    }
</style>
""", unsafe_allow_html=True)

DATA_FILE = "Data_Employees.xlsx"

# 3. تحميل البيانات بأمان
@st.cache_data(ttl=1)
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_excel(DATA_FILE)
            df.columns = [str(col).strip() for col in df.columns]
            if not df.empty:
                return df
        except Exception:
            pass
            
    cols = ['الاسم الرباعي', 'الرقم الوظيفي', 'العنوان الوظيفي', 'الشهادة', 'الجنس', 
            'الدرجة الوظيفية', 'المرحلة', 'الراتب الاسمي', 'الاختصاص العام', 'الاختصاص الدقيق', 
            'سنة التخرج', 'رقم امر التعيين', 'تاريخ التعيين', 'تاريخ المباشرة', 'رقم الهاتف', 
            'اسم الام الثلاثي', 'الحالة الزوجية', 'اسم الزوجة', 'الرقم الوطني', 'تاريخ اصداره', 
            'تاريخ التولد', 'جهة الإصدار', 'محل الولادة', 'رقم البطاقة التموينية', 'محلة - زقاق - دار', 
            'رقم وثيقة التخرج', 'تاريخ اصدار وثيقة التخرج', 'رقم صحة الصدور', 'تاريخ صحة الصدور', 
            'عنوان السكن', 'اقرب نقطة دالة', 'رقم الهوية', 'الملاحظات']
    sample_data = [['أحمد محمد علي الحسيني', 'EMP-1001', 'رئيس مهندسين قدم', 'بكالوريوس', 'ذكر'] + [""] * 28]
    return pd.DataFrame(sample_data, columns=cols)

def save_data(df):
    df.to_excel(DATA_FILE, index=False)
    st.cache_data.clear()

df = load_data()
name_col = 'الاسم الرباعي' if 'الاسم الرباعي' in df.columns else df.columns[0]

# 4. شريط العنوان الزجاجي العلوي
st.markdown("""
<div class="mock-header">
    <div>متصل وبانتظار الأوامر</div>
    <div style="font-size: 1.2rem;">المائي <span style="font-size: 0.8rem; font-weight:normal;">- محاكاة متصفح Streamlit التفاعلية</span></div>
    <div>الإصدار المائي 2026</div>
</div>
""", unsafe_allow_html=True)

# 5. القائمة الجانبية المائية في جهة اليمين
with st.sidebar:
    st.markdown("""
    <div class="glass-card" style="padding: 15px; margin-bottom: 15px; background: rgba(255,255,255,0.7) !important;">
        <h3 style="color: #0369a1; margin:0;">لوحة تحكم الأوامر</h3>
        <p style="color: #0284c7; font-size: 0.9rem;">Streamlit Interactive Controls</p>
    </div>
    """, unsafe_allow_html=True)
    
    action = st.radio(
        "اختر العملية المطلوبة:",
        ["🔍 استعلام وبحث حقيقي", "➕ إضافة موظف جديد", "✏️ تعديل بيانات", "❌ حذف موظف", "📥 استيراد / تصدير Excel"],
        label_visibility="collapsed"
    )
    
    valid_rows = df[df[name_col].notna() & (df[name_col].astype(str).str.strip() != "")]
    emp_count = len(valid_rows)
    
    st.markdown(f"""
    <div class="glass-card" style="padding: 10px; margin-top: 30px; background: rgba(255,255,255,0.8) !important;">
        <p style="color: #0369a1; margin:0;">إحصائيات قاعدة البيانات</p>
        <h1 style="color: #0284c7; margin:0;">{emp_count}</h1>
        <p style="color: #0369a1; font-size: 0.8rem; margin:0;">إجمالي الموظفين المسجلين</p>
    </div>
    """, unsafe_allow_html=True)

# 6. لوحة المحتوى الرئيسية
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

if action == "🔍 استعلام وبحث حقيقي":
    st.markdown("""
    <h2 style="color: #0369a1; margin:0;">🔍 استعلام وعرض قاعدة بيانات الموظفين</h2>
    <p style="color: #0284c7;">ابحث عن أي موظف بالاسم، الرقم الوظيفي، أو رقم الهوية الوطنية للمعاينة الفورية والطباعة</p>
    """, unsafe_allow_html=True)
    
    search_term = st.text_input("أدخل الكلمة المفتاحية للبحث:", placeholder="ابحث باسم الموظف أو الرقم الوظيفي أو الهوية...")
    
    filtered_df = df.copy()
    if search_term:
        filtered_df = df[
            df.astype(str).apply(lambda row: row.str.contains(search_term, case=False).any(), axis=1)
        ]
        st.success(f"تم العثور على {len(filtered_df)} سجل")
    
    col1, col2 = st.columns(2)
    with col1:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            filtered_df.to_excel(writer, index=False, sheet_name='الموظفين')
        st.download_button("📥 تصدير أكسل Excel", data=output.getvalue(), file_name="بيانات_الموظفين.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    with col2:
        if st.button("🖨️ طباعة الاستمارة الزجاجية"):
            st.info("استخدم أمر الطباعة المباشر من المتصفح (Ctrl + P) لطباعة الاستمارة.")

    st.markdown("<h4 style='color: #0369a1; margin-top: 20px;'>جدول سجلات الموظفين العام</h4>", unsafe_allow_html=True)
    st.dataframe(filtered_df, use_container_width=True)

elif action == "➕ إضافة موظف جديد":
    st.markdown("<h2 style='color: #0369a1;'>➕ إضافة موظف جديد</h2>", unsafe_allow_html=True)
    with st.form("add_form"):
        new_data = {}
        cols_list = list(df.columns)
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
            st.success("تمت إضافة الموظف بنجاح!")
            st.rerun()

elif action == "✏️ تعديل بيانات":
    st.markdown("<h2 style='color: #0369a1;'>✏️ تعديل بيانات موظف</h2>", unsafe_allow_html=True)
    emp_list = df[name_col].dropna().astype(str).tolist()
    if emp_list:
        selected_emp = st.selectbox("اختر الموظف المراد تعديل بياناته:", emp_list)
        emp_index = df[df[name_col].astype(str) == selected_emp].index[0]
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
                st.rerun()

elif action == "❌ حذف موظف":
    st.markdown("<h2 style='color: #0369a1;'>❌ حذف موظف من النظام</h2>", unsafe_allow_html=True)
    emp_list = df[name_col].dropna().astype(str).tolist()
    if emp_list:
        selected_emp = st.selectbox("اختر الموظف المراد حذفه:", emp_list)
        if st.button("🚨 تأكيد الحذف النهائي"):
            df = df[df[name_col].astype(str) != selected_emp]
            save_data(df)
            st.success(f"تم حذف الموظف ({selected_emp}) بنجاح!")
            st.rerun()

elif action == "📥 استيراد / تصدير Excel":
    st.markdown("<h2 style='color: #0369a1;'>📥 استيراد وتصدير قاعدة البيانات</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("اختر ملف Excel (.xlsx):", type=["xlsx", "xls"])
    if uploaded_file is not None:
        new_df = pd.read_excel(uploaded_file)
        if st.button("دمج البيانات المرفوعة مع القاعدة الحالية"):
            df = pd.concat([df, new_df], ignore_index=True)
            save_data(df)
            st.success("تم استيراد البيانات ودمجها بنجاح!")
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
