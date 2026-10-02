import streamlit as st
import pandas as pd
import os
import io

# 1. إعدادات الصفحة الشاملة والاتجاه العربي
st.set_page_config(
    page_title="نظام إدارة الموظفين - المائي",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تصميم CSS مصحح بدقة يضمن ظهور لوحة التحكم الجانبية والجدول العربي من اليمين
st.markdown("""
<style>
    /* تطبيق اتجاه اليمين إلى اليسار بشكل آمن للواجهة */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        direction: rtl !important;
        text-align: right !important;
    }

    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 50%, #e1f5fe 100%);
    }

    /* تنسيق لوحة التحكم الجانبية الزجاجية الثابتة */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.75) !important;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-left: 1px solid rgba(255, 255, 255, 0.8) !important;
        direction: rtl !important;
        text-align: center !important;
    }
    
    .stDeployButton, #MainMenu, footer {
        visibility: hidden !important;
    }
    
    [data-testid="stAppViewContainer"] {
        padding-top: 1rem;
    }

    /* محاذاة كل النصوص والمدخلات في الوسط */
    p, h1, h2, h3, h4, label, input, select, textarea {
        text-align: center !important;
    }
    
    /* محاذاة جدول البيانات من اليمين إلى اليسار */
    [data-testid="stDataFrame"], div[role="grid"] {
        direction: rtl !important;
        text-align: center !important;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.65) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.05);
        padding: 25px;
        margin-bottom: 25px;
    }
    
    .mock-header {
        background: rgba(255, 255, 255, 0.65);
        backdrop-filter: blur(10px);
        padding: 12px 24px;
        border-radius: 14px;
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
        background: rgba(255, 255, 255, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.9);
        color: #0284c7 !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        background: rgba(255, 255, 255, 1) !important;
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

# قائمة الحقول الرسمية المعتمدة
OFFICIAL_COLUMNS = [
    'الاسم الرباعي', 'الرقم الوظيفي', 'العنوان الوظيفي', 'الشهادة', 'الجنس', 
    'الدرجة الوظيفية', 'المرحلة', 'الراتب الاسمي', 'الاختصاص العام', 'الاختصاص الدقيق', 
    'سنة التخرج', 'رقم امر التعيين', 'تاريخ التعيين', 'تاريخ المباشرة', 'رقم الهاتف', 
    'اسم الام الثلاثي', 'الحالة الزوجية', 'اسم الزوجة', 'الرقم الوطني', 'تاريخ اصداره', 
    'تاريخ التولد', 'جهة الإصدار', 'محل الولادة', 'رقم البطاقة التموينية', 'محلة - زقاق - دار', 
    'رقم وثيقة التخرج', 'تاريخ اصدار وثيقة التخرج', 'رقم صحة الصدور', 'تاريخ صحة الصدور', 
    'عنوان السكن', 'اقرب نقطة دالة', 'رقم الهوية', 'الملاحظات'
]

# 3. تحميل البيانات وإصلاح مشكلة Unnamed والأسطر الفارغة
@st.cache_data(ttl=1)
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_excel(DATA_FILE)
            # معالجة رأس الجدول في حال وجود أسطر فارغة بالملف الأصلي
            if any('Unnamed' in str(c) for c in df.columns):
                for idx, row in df.iterrows():
                    row_vals = [str(v).strip() for v in row.values if pd.notna(v)]
                    if any('الاسم' in v or 'الوظيفي' in v for v in row_vals):
                        df = pd.read_excel(DATA_FILE, header=idx+1)
                        break
            
            df.columns = [str(col).strip() for col in df.columns]
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            
            if len(df.columns) > 0 and not df.empty:
                return df
        except Exception:
            pass

    # بيانات نموذجية افتراضية جاهزة
    sample_data = [['اياد سامي مهدي عبد', '101864842', 'مستشار قانوني', 'بكالوريوس', 'ذكر', 'الثالثة', '1', '101864842', 'قانون عام', 'قانون عام', '2004'] + [""] * 22]
    return pd.DataFrame(sample_data, columns=OFFICIAL_COLUMNS)

def save_data(df):
    df.to_excel(DATA_FILE, index=False)
    st.cache_data.clear()

df = load_data()
name_col = 'الاسم الرباعي' if 'الاسم الرباعي' in df.columns else df.columns[0]

# 4. الشريط الزجاجي العلوي
st.markdown("""
<div class="mock-header">
    <div>متصل وبانتظار الأوامر</div>
    <div style="font-size: 1.2rem;">المائي <span style="font-size: 0.8rem; font-weight:normal;">- محاكاة متصفح Streamlit التفاعلية</span></div>
    <div>الإصدار المائي 2026</div>
</div>
""", unsafe_allow_html=True)

# 5. لوحة تحكم الأوامر الجانبية (Sidebar) - ثابتة وواضحة جداً
with st.sidebar:
    st.markdown("""
    <div class="glass-card" style="padding: 15px; margin-bottom: 15px; background: rgba(255,255,255,0.85) !important;">
        <h3 style="color: #0369a1; margin:0;">لوحة تحكم الأوامر</h3>
        <p style="color: #0284c7; font-size: 0.85rem; margin-top: 4px;">Streamlit Interactive Controls</p>
    </div>
    """, unsafe_allow_html=True)
    
    action = st.radio(
        "اختر العملية المطلوبة:",
        ["🔍 استعلام وبحث حقيقي", "➕ إضافة موظف جديد", "✏️ تعديل بيانات", "❌ حذف موظف", "📥 استيراد / تصدير Excel"],
        label_visibility="collapsed"
    )
    
    valid_rows = df[df[name_col].notna() & (df[name_col].astype(str).str.strip() != "") & (~df[name_col].astype(str).str.contains('None', case=False))]
    emp_count = len(valid_rows)
    
    st.markdown(f"""
    <div class="glass-card" style="padding: 12px; margin-top: 25px; background: rgba(255,255,255,0.85) !important;">
        <p style="color: #0369a1; margin:0; font-size: 0.9rem;">إحصائيات قاعدة البيانات</p>
        <h1 style="color: #0284c7; margin:5px 0;">{emp_count}</h1>
        <p style="color: #0369a1; font-size: 0.8rem; margin:0;">إجمالي الموظفين المسجلين</p>
    </div>
    """, unsafe_allow_html=True)

# 6. لوحة المحتوى الرئيسية
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

if action == "🔍 استعلام وبحث حقيقي":
    st.markdown("""
    <h2 style="color: #0369a1; margin:0;">🔍 استعلام وعرض قاعدة بيانات الموظفين</h2>
    <p style="color: #0284c7; margin-bottom: 20px;">ابحث عن أي موظف بالاسم، الرقم الوظيفي، أو رقم الهوية الوطنية للمعاينة الفورية والطباعة</p>
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

    st.markdown("<h4 style='color: #0369a1; margin-top: 25px;'>جدول سجلات الموظفين العام</h4>", unsafe_allow_html=True)
    
    # تنظيف العرض وإلغاء قيم None المزعجة
    display_df = filtered_df.fillna("").replace("None", "").copy()
    
    # عرض الجدول ابتداءً من اليمين
    st.dataframe(display_df, use_container_width=True, hide_index=True)

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

elif action == "✏️️ تعديل بيانات":
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
