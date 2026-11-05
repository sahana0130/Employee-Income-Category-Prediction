from pathlib import Path
import streamlit as st

# ==================================================
# 1. APP SETTINGS
# ==================================================
st.set_page_config(
    page_title="IncomeAI | Employee Income Predictor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
PAGES_DIR = BASE_DIR / "pages"


# ==================================================
# 2. SHARED BACKGROUND AND SIDEBAR DESIGN
# ==================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    .stApp {
        background:
            radial-gradient(ellipse at top left, #243b70 0%, transparent 42%),
            radial-gradient(ellipse at bottom right, #51275f 0%, transparent 40%),
            linear-gradient(135deg, #090e1d, #11182d 60%, #19132d);
        color: #f5f7ff;
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #10172b, #19152e);
        border-right: 1px solid rgba(255,255,255,0.12);
        min-width: 245px;
    }

    /* Do not hide Streamlit's navigation */
    [data-testid="stSidebarNav"] {
        display: block !important;
        visibility: visible !important;
    }

    [data-testid="stSidebarNav"] a {
        border-radius: 10px;
        margin: 4px 6px;
    }

    [data-testid="stSidebarNav"] a:hover {
        background: rgba(167,139,250,0.18);
    }

    .incomeai-brand {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -1px;
        color: #ffffff;
        margin-top: 12px;
    }

    .incomeai-brand span {
        color: #a78bfa;
    }

    .incomeai-caption {
        font-size: 10px;
        letter-spacing: 1.5px;
        color: #b8c4df;
        margin-top: 4px;
        margin-bottom: 20px;
    }

    .page-banner {
        padding: 34px;
        border-radius: 23px;
        border: 1px solid rgba(255,255,255,0.15);
        background: linear-gradient(
            120deg,
            rgba(38,60,111,0.90),
            rgba(73,41,90,0.90)
        );
        box-shadow: 0 15px 40px rgba(0,0,0,0.18);
        margin-bottom: 24px;
        animation: appear 0.6s ease-out;
    }

    .page-banner h1 {
        font-size: clamp(30px, 4vw, 46px);
        font-weight: 800;
        color: white;
        line-height: 1.2;
        margin: 12px 0;
    }

    .page-banner h1 span {
        background: linear-gradient(90deg, #c4b5fd, #67e8f9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .page-banner p {
        color: #d0d8ee;
        font-size: 15px;
        line-height: 1.8;
    }

    div.stButton > button {
        border-radius: 10px;
    }

    @keyframes appear {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# 3. FIND EXISTING PAGE FILES
# ==================================================
def find_page(keywords):
    if not PAGES_DIR.is_dir():
        return None

    files = sorted(PAGES_DIR.glob("*.py"))

    for keyword in keywords:
        for file in files:
            if keyword in file.stem.lower():
                return file

    return None


predict_file = find_page(["predict"])
comparison_file = find_page(["model_comparison", "comparison"])
chatbot_file = find_page(["chatbot", "incomeai"])


# ==================================================
# 4. BUILD THE PAGE NAVIGATION
# ==================================================
pages = []

if predict_file:
    pages.append(
        st.Page(
            str(predict_file),
            title="Predict Income",
            icon="🔮",
            default=True,
        )
    )

if comparison_file:
    pages.append(
        st.Page(
            str(comparison_file),
            title="Model Comparison",
            icon="📈",
        )
    )

if chatbot_file:
    pages.append(
        st.Page(
            str(chatbot_file),
            title="Ask IncomeAI",
            icon="💬",
        )
    )


# ==================================================
# 5. SHARED SIDEBAR BRANDING
# ==================================================
with st.sidebar:
    st.markdown(
        """
        <div class="incomeai-brand">
            📊 Income<span>AI</span>
        </div>
        <div class="incomeai-caption">
            EMPLOYEE INCOME PREDICTOR
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.caption("YOUR WORKSPACE")

    # Streamlit automatically displays the registered
    # page links below this branding.


# ==================================================
# 6. HANDLE MISSING FILES SAFELY
# ==================================================
if not pages:
    st.error("No page files were found.")

    st.write("Expected pages folder:")
    st.code(str(PAGES_DIR))

    st.write("Create or check these Python files:")

    st.code(
        "pages/1_Predict_Income.py\n"
        "pages/2_Model_Comparison.py\n"
        "pages/3_Ask_IncomeAI.py"
    )

    if PAGES_DIR.exists():
        st.write("Files currently found:")
        existing_files = sorted(PAGES_DIR.glob("*.py"))

        if existing_files:
            for file in existing_files:
                st.code(file.name)
        else:
            st.info("Your pages folder is empty.")
    else:
        st.error("The pages folder does not exist.")

    st.stop()


# ==================================================
# 7. START THE SELECTED PAGE
# ==================================================
navigation = st.navigation(
    pages,
    position="sidebar",
)

navigation.run()