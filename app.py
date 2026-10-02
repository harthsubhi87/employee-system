import streamlit as st
import pandas as pd
import os
import io

# 1. إعدادات الصفحة - تثبيت القائمة الجانبية مسبقاً
st.set_page_config(
    page_title="نظام إدارة الموظفين - المائي",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تصميم CSS المتقدم جداً لمحاكاة واجهة المحاكاة (Glassmorphic Mockup)
st.markdown("""
<style>
    /* 1. الخلفية العامة المائية */
    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 50%, #e1f5fe 100%);
    }
    
    /* 2. إخفاء عناصر Streamlit الافتراضية للسيطرة على التصميم */
    [data-testid="stSidebar"] > div:first-child {
        background-color: transparent !important;
        background-image: none !important;
    }
    .stDeployButton, #MainMenu, header, footer {
        visibility: hidden !important;
    }
    [data-testid="stAppViewContainer"] {
        padding-top: 2rem;
    }

    /* 3. محاذاة كافة النصوص والحقول للوسط */
    p, h1, h2, h3, h4, label, input, select, textarea, [data-testid="stForm"] {
        text-align: center !important;
    }
    
    /* 4. تصميم القائمة الجانبية (Left Panel) كلوحة زجاجية متصلة */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.5) !important;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.7);
        border-radius: 0 20px 20px 0;
        box-shadow: 4px 0 24px rgba(0,0,0,0.03);
    }
    [data-testid="stSidebarNav"] {
        padding-top: 1rem;
    }
    
    /* 5. تصميم منطقة المحتوى الرئيسية (Main Area) كلوحة زجاجية */
    .glass-card {
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.05);
        padding: 30px;
        margin-bottom: 25px;
    }
    
    /* 6. محاكاة الهيدر العلوي الخاص بالمحاكاة */
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
    }

    /* 7. تصميم الأزرار المائية الملساء */
    .stButton>button {
        border-radius: 12px;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
        border: none;
        background: rgba(255, 255, 255, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.8);
        color: #0284c7 !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        background: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* 8. تصميم حقول الإدخال */
    .stTextInput>div>div>input {
        text-align: center !important;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid #bae6fd;
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
        cols = ['#', 'الاسم الرباعي', 'الرقم الوظيفي', 'العنوان الوظيفي', 'الشهادة', 'الجنس', 
                'الدرجة الوظيفية', 'المرحلة', 'الراتب الاسمي', 'الاختصاص العام', 'الاختصاص الدقيق', 
                'سنة التخرج', 'رقم امر التعيين', 'تاريخ التعيين', 'تاريخ المباشرة', 'رقم الهاتف', 
                'اسم الام الثلاثي', 'الحالة الزوجية', 'اسم الزوجة', 'الرقم الوطني', 'تاريخ اصداره', 
                'تاريخ التولد', 'جهة الإصدار', 'محل الولادة', 'رقم البطاقة التموينية', 'محلة - زقاق - دار', 
                'رقم وثيقة التخرج', 'تاريخ اصدار وثيقة التخرج', 'رقم صحة الصدور', 'تاريخ صحة الصدور', 
                'عنوان السكن', 'اقرب نقطة دالة', 'رقم الهوية', 'الملاحظات']
        # إضافة سجلات عينة كما في المحاكاة
        sample_data = [[1, 'أحمد محمد علي الحسيني', 'EMP-1001', 'رئيس مهندسين قدم', 'بكالوريوس', 'ذكر']] + [[""] * 34 for _ in range(3)]
        return pd.DataFrame(sample_data, columns=cols)

def save_data(df):
    df.to_excel(DATA_FILE, index=False)
    st.cache_data.clear()

df = load_data()

# 4. محاكاة الهيدر العلوي الخاص بواجهة المحاكاة
st.markdown("""
<div class="mock-header">
    <div>متصل وبانتظار الأوامر</div>
    <div style="font-size: 1.2rem;">المائي <span style="font-size: 0.8rem; font-weight:normal;">- محاكاة متصفح Streamlit التفاعلية</span></div>
    <div>الإصدار المائي 2026</div>
</div>
""", unsafe_allow_html=True)

# 5. القائمة الجانبية (Left Sidebar) - محاكاة القائمة الزجاجية في image_2.png
# استدعاء الراديو الجانبي كأوامر
with st.sidebar:
    # محاكاة اللوحة العلوية للقائمة
    st.markdown("""
    <div class="glass-card" style="padding: 15px; margin-bottom: 15px; background: rgba(255,255,255,0.7) !important;">
        <h3 style="color: #0369a1; margin:0;">لوحة تحكم الأوامر</h3>
        <p style="color: #0284c7; font-size: 0.9rem;">Streamlit Interactive Controls</p>
    </div>
    """, unsafe_allow_html=True)
    
    # محاكاة الأزرار الخمسة الزجاجية كخيارات
    action = st.radio(
        "اختر العملية المطلوبة:",
        ["🔍 استعلام وبحث حقيقي", "➕ إضافة موظف جديد (33 حقل)", "✏️ تعديل وحذف البيانات", "📥 استيراد / تصدير Excel", "📣 دليل نشر الرابط مجاناً"],
        label_visibility="collapsed"
    )
    
    # محاكاة إحصائيات قاعدة البيانات في الأسفل كما في المحاكاة
    st.markdown(f"""
    <div class="glass-card" style="padding: 10px; margin-top: 30px; background: rgba(255,255,255,0.8) !important;">
        <p style="color: #0369a1; margin:0;">إحصائيات قاعدة البيانات</p>
        <h1 style="color: #0284c7; margin:0;">{len(df[df['الاسم الرباعي'] != ""])}</h1>
        <p style="color: #0369a1; font-size: 0.8rem; margin:0;">إجمالي الموظفين المسجلين</p>
    </div>
    """, unsafe_allow_html=True)

# 6. منطقة المحتوى الرئيسية (Main Area) - مطابقة لتصميم المحاكاة الزجاجي
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

# --- 1. أمر استعلام وبحث (طريقة المحاكاة) ---
if action == "🔍 استعلام وبحث حقيقي":
    st.markdown("""
    <h1 style="color: #0369a1; margin:0;">🔍 استعلام وعرض قاعدة بيانات الموظفين</h1>
    <p style="color: #0284c7;">ابحث عن أي موظف بالاسم، الرقم الوظيفي، أو رقم الهوية الوطنية للمعاينة الفورية والطباعة</p>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='color: #0369a1; margin-top: 20px; font-weight:bold;'>أدخل الكلمة المفتاحية للبحث:</p>", unsafe_allow_html=True)
    search_term = st.text_input("", placeholder="ابحث باسم الموظف أو الرقم الوظيفي أو الهوية...", label_visibility="collapsed")
    
    filtered_df = df.copy()
    if search_term:
        filtered_df = df[
            df.astype(str).apply(lambda row: row.str.contains(search_term, case=False).any(), axis=1)
        ]
        st.success(f"تم العثور على {len(filtered_df[filtered_df['الاسم الرباعي'] != ''])} سجل")
    
    # أزرار الإجراءات الخاصة بالمحاكاة
    col1, col2 = st.columns(2)
    with col1:
        st.button("تصدير أكسل Excel")
    with col2:
        st.button("طباعة الاستمارة الزجاجية")

    st.markdown("<p style='color: #0369a1; margin-top: 30px; font-weight:bold;'>جدول سجلات الموظفين العام</p>", unsafe_allow_html=True)
    # عرض الجدول بمحاذاة للوسط وعرض كامل
    st.dataframe(filtered_df, use_container_width=True)

# --- 2. أمر إضافة موظف (كما في التطبيق السابق ولكن بستايل المحاكاة) ---
elif action == "➕ إضافة موظف جديد (33 حقل)":
    st.markdown("<h3>➕ إضافة موظف جديد</h3>", unsafe_allow_html=True)
    with st.form("add_form", clear_on_submit=True):
        new_data = {}
        # تقسیم الحقول إلى أعمدة متناسقة
        col1, col2 = st.columns(2)
        cols_list = list(df.columns)[1:] # تخطي حقل التسلسل
        for i, col_name in enumerate(cols_list):
            if i % 2 == 0:
                new_data[col_name] = col1.text_input(col_name)
            else:
                new_data[col_name] = col2.text_input(col_name)
                
        submit = st.form_submit_button("💾 حفظ الموظف الجديد")
        if submit:
            # إضافة رقم تسلسلي تلقائي
            next_id = df['#'].max() + 1 if not df.empty else 1
            new_row = pd.DataFrame([{"#": next_id, **new_data}])
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.success("تمت إضافة الموظف بنجاح!")
            st.rerun()

# --- بقية الأوامر (تعديل، حذف، استيراد) ---
# ... (نفس منطق الكود السابق ولكن بوضعها داخل st.markdown("<div class='glass-card'>"))
else:
    st.info(f"الأمر ({action}) قيد التطوير ليطابق واجهة المحاكاة.")

st.markdown("</div>", unsafe_allow_html=True)
