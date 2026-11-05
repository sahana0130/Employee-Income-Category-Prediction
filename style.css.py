/* ==================================
   INCOME AI - CUSTOM WEBSITE DESIGN
================================== */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* MAIN BACKGROUND */

.stApp {
    background: linear-gradient(
        -45deg,
        #080d1c,
        #10152b,
        #171332,
        #0c1930
    );
    background-size: 400% 400%;
    animation: backgroundMove 15s ease infinite;
    color: #f4f5ff;
    font-family: 'Inter', sans-serif;
}

@keyframes backgroundMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* REMOVE TOP HEADER BACKGROUND */

header[data-testid="stHeader"] {
    background: transparent;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #10172d,
        #171332
    );
    border-right: 1px solid rgba(255,255,255,0.08);
}

.sidebar-brand {
    text-align: center;
    padding: 20px 5px;
}

.sidebar-brand h2 {
    color: #a99aff;
    font-size: 27px;
    font-weight: 800;
}

.sidebar-brand p {
    color: #a6acc5;
    font-size: 12px;
}

/* HERO SECTION */

.hero-section {
    position: relative;
    overflow: hidden;
    padding: 65px 45px;
    border-radius: 25px;
    background: linear-gradient(
        120deg,
        rgba(80, 58, 170, 0.38),
        rgba(24, 90, 150, 0.25),
        rgba(20, 24, 52, 0.8)
    );
    border: 1px solid rgba(180, 160, 255, 0.25);
    box-shadow: 0 15px 50px rgba(0,0,0,0.3);
    animation: heroAppear 1s ease;
}

@keyframes heroAppear {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.hero-label {
    display: inline-block;
    padding: 9px 16px;
    border-radius: 30px;
    background: rgba(150,120,255,0.18);
    border: 1px solid rgba(180,160,255,0.4);
    color: #c5b6ff;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
}

.hero-section h1 {
    font-size: clamp(32px, 5vw, 58px);
    line-height: 1.15;
    font-weight: 800;
    color: white;
    margin-top: 30px;
}

.hero-section h1 span {
    background: linear-gradient(
        90deg,
        #a995ff,
        #63c8ff
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-description {
    max-width: 700px;
    color: #c2c8df;
    font-size: 16px;
    line-height: 1.9;
    margin-top: 20px;
}

.hero-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 30px;
}

.hero-tags span {
    padding: 9px 16px;
    border-radius: 20px;
    background: rgba(255,255,255,0.09);
    border: 1px solid rgba(255,255,255,0.13);
    color: #e0dcff;
    font-size: 12px;
}

/* SECTION HEADINGS */

.section-heading {
    margin-top: 30px;
    margin-bottom: 22px;
}

.section-heading h2 {
    color: #ffffff;
    font-size: 27px;
    font-weight: 800;
}

.section-heading p {
    color: #aeb7d1;
    font-size: 14px;
}

/* INFORMATION CARDS */

.info-card {
    min-height: 205px;
    padding: 25px;
    border-radius: 20px;
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.12);
    transition: all 0.35s ease;
    animation: cardAppear 0.9s ease;
}

@keyframes cardAppear {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.info-card:hover {
    transform: translateY(-9px);
    border-color: #9581ff;
    background: rgba(120,95,230,0.14);
    box-shadow: 0 12px 35px rgba(100,80,230,0.2);
}

.card-icon {
    font-size: 35px;
    margin-bottom: 15px;
}

.info-card h3 {
    color: #c5b5ff;
    font-size: 19px;
    font-weight: 700;
}

.info-card p {
    color: #b8bfd5;
    font-size: 13px;
    line-height: 1.8;
}

/* WORKFLOW CARDS */

.workflow-card {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 18px 22px;
    margin-bottom: 13px;
    border-radius: 15px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.09);
    transition: 0.3s ease;
}

.workflow-card:hover {
    transform: translateX(8px);
    border-color: #8d7aff;
    background: rgba(130,105,255,0.12);
}

.workflow-number {
    min-width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 13px;
    background: linear-gradient(135deg,#7658e8,#318bd8);
    color: white;
    font-weight: 800;
}

.workflow-card h4 {
    color: #e2dcff;
    margin: 0 0 6px 0;
}

.workflow-card p {
    color: #aeb8d0;
    font-size: 13px;
    margin: 0;
}

/* DATASET SECTION */

.dataset-box {
    padding: 30px;
    margin-top: 25px;
    border-radius: 20px;
    background: linear-gradient(
        120deg,
        rgba(100,75,200,0.18),
        rgba(40,130,200,0.12)
    );
    border: 1px solid rgba(150,130,255,0.25);
}

.dataset-box h2 {
    color: #c5b5ff;
}

.dataset-box p {
    color: #c2c9df;
    line-height: 1.8;
}

/* GENERAL TEXT */

.stMarkdown p,
.stMarkdown li {
    color: #c4cbe0;
}

.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3 {
    color: #ffffff;
}

/* BUTTONS */

.stButton button {
    background: linear-gradient(90deg,#7555df,#287fca);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 24px;
    font-weight: 700;
    transition: 0.3s ease;
}

.stButton button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 22px rgba(110,90,240,0.35);
    color: white;
}

/* LINKS */

a {
    color: #a99aff !important;
}

/* FOOTER */

.footer {
    text-align: center;
    padding: 35px 10px;
    margin-top: 40px;
    border-top: 1px solid rgba(255,255,255,0.1);
}

.footer h3 {
    color: #a995ff;
    font-size: 24px;
}

.footer p {
    color: #939db8;
    font-size: 12px;
    line-height: 1.8;
}

/* DIVIDER */

hr {
    border-color: rgba(255,255,255,0.12) !important;
}

/* RESPONSIVE DESIGN */

@media (max-width: 768px) {
    .hero-section {
        padding: 35px 22px;
    }

    .hero-section h1 {
        font-size: 34px;
    }

    .info-card {
        margin-bottom: 15px;
    }

    .workflow-card {
        gap: 12px;
        padding: 15px;
    }
}