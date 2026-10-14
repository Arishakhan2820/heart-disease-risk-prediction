"""Shared styles and navigation for the Streamlit pages."""
from __future__ import annotations

import streamlit as st


def apply_theme() -> None:
    st.markdown(
        """<style>
:root {
    --canvas: #faf8f7;
    --surface: #fff;
    --surface-tint: #f6ecef;
    --maroon: #781d39;
    --maroon-deep: #481326;
    --ink: #302329;
    --muted: #756870;
    --line: #eadfe2;
    --shadow: 0 14px 32px rgba(58,17,32,.09), 0 2px 7px rgba(58,17,32,.05);
}
* { letter-spacing: 0; }
html { scroll-behavior: smooth; }
body, .stApp { color: var(--ink); background: var(--canvas); font-family: "Aptos", "Trebuchet MS", "Segoe UI", sans-serif; }
header, #MainMenu, footer { visibility: hidden; }
.block-container { max-width: 1160px; padding: .75rem 1.25rem 3.5rem; }
.stApp, .stApp p, .stApp label, .stApp [data-testid="stMarkdownContainer"] { color: var(--ink); }
.nav-rule { height:1px; margin:.15rem 0 1.25rem; background:var(--line); }
.brand { display:flex; align-items:center; gap:.7rem; color:var(--maroon-deep)!important; }
.brand-icon { display:grid; place-items:center; width:42px; height:42px; border-radius:8px; color:#fff; background:var(--maroon); font-size:1.55rem; box-shadow:0 5px 12px rgba(72,19,38,.2); }
.brand-copy { display:grid; gap:.08rem; }
.brand-copy strong { font-family:Georgia,"Times New Roman",serif; font-size:1.05rem; }
.brand-copy small { color:var(--muted); font-size:.72rem; }
.stApp [data-testid="stPageLink"] a { color:var(--maroon-deep)!important; text-decoration:none!important; font-size:.87rem; font-weight:650; border-radius:6px; }
.stApp [data-testid="stPageLink"] a:hover { color:var(--maroon)!important; background:var(--surface-tint)!important; }
.stApp [data-testid="stPageLink"] p { color:inherit!important; }
.nav-desktop-marker, .nav-mobile-marker { display:none; }
.nav-start-marker { display:none; }
[data-testid="stHorizontalBlock"] > :is([data-testid="column"],[data-testid="stColumn"]):has(.nav-start-marker) [data-testid="stBaseButton-primary"] { width:auto!important; min-height:2.4rem!important; padding:.35rem .68rem!important; font-size:.82rem!important; white-space:nowrap; }
[data-testid="stHorizontalBlock"] > :is([data-testid="column"],[data-testid="stColumn"]):has(.nav-mobile-marker) { display:none; }
[data-testid="stHorizontalBlock"] > :is([data-testid="column"],[data-testid="stColumn"]):has(.nav-mobile-marker) [data-testid="stPopover"] button { min-height:2.45rem!important; padding:.35rem .6rem!important; color:var(--maroon-deep)!important; background:var(--surface)!important; border:1px solid var(--line)!important; box-shadow:none!important; font-size:.85rem!important; }
[data-testid="stHorizontalBlock"] > :is([data-testid="column"],[data-testid="stColumn"]):has(.nav-mobile-marker) [data-testid="stPopover"] button svg { display:none; }
[data-testid="stHorizontalBlock"] > :is([data-testid="column"],[data-testid="stColumn"]):has(.nav-mobile-marker) [data-testid="stPopover"] button:hover { color:var(--maroon)!important; background:var(--surface-tint)!important; }
[data-testid="stHorizontalBlock"] > :is([data-testid="column"],[data-testid="stColumn"]):has(.nav-mobile-marker) [data-testid="stPopoverBody"] { min-width:210px; padding:.45rem; background:var(--surface); }
[data-testid="stHorizontalBlock"] > :is([data-testid="column"],[data-testid="stColumn"]):has(.nav-mobile-marker) [data-testid="stPopoverBody"] [data-testid="stPageLink"] a { width:100%; padding:.45rem .6rem; }
.home-hero-marker { display:none; }
[data-testid="stHorizontalBlock"]:has(.home-hero-marker) { position:relative; display:flex; align-items:center; gap:1.5rem; min-height:330px; padding:2.5rem 3rem; overflow:hidden; color:#fff; background:linear-gradient(112deg,#481326 0%,#681a35 61%,#842c49 100%); border-radius:10px; box-shadow:0 18px 40px rgba(72,19,38,.19),0 4px 12px rgba(72,19,38,.1); animation:rise-in .55s ease-out both; }
[data-testid="stHorizontalBlock"]:has(.home-hero-marker)::before { position:absolute; inset:0; content:""; pointer-events:none; opacity:.19; background:repeating-linear-gradient(135deg,transparent 0 28px,rgba(255,255,255,.09) 29px,transparent 30px 58px); mask-image:linear-gradient(90deg,transparent 15%,#000 100%); }
[data-testid="stHorizontalBlock"]:has(.home-hero-marker) > [data-testid="column"] { position:relative; z-index:1; }
[data-testid="stHorizontalBlock"]:has(.home-hero-marker) [data-testid="stPageLink"] a { display:inline-flex; align-items:center; gap:.4rem; width:fit-content; height:36px!important; min-height:36px!important; margin:.25rem 0 .1rem; padding:.25rem .68rem!important; color:var(--maroon-deep)!important; background:#fff; box-shadow:0 5px 12px rgba(30,5,15,.16); font-size:.8rem; line-height:1.2; }
[data-testid="stHorizontalBlock"]:has(.home-hero-marker) [data-testid="stPageLink"] a p { margin:0!important; }
[data-testid="stHorizontalBlock"]:has(.home-hero-marker) [data-testid="stPageLink"] a:hover { color:var(--maroon)!important; background:#fff!important; transform:translateY(-1px); }
.hero-copy, .heart-stage { position:relative; z-index:1; }
.hero-kicker { color:#f0c9d3; font-size:.75rem; font-weight:700; }
.hero-copy h1 { max-width:590px; margin:.75rem 0 .85rem!important; color:#fff!important; font-family:Georgia,"Times New Roman",serif; font-size:2.55rem!important; font-weight:500; line-height:1.14; }
.hero-copy p { max-width:560px; color:#f7e9ed!important; font-size:1rem; line-height:1.65; }
.hero-note { margin:.45rem 0 0!important; color:#f0c9d3!important; font-size:.76rem!important; font-weight:600; }
.hero-actions { display:flex; flex-wrap:wrap; align-items:center; gap:.7rem; margin-top:.9rem; }
.hero-action { display:inline-flex; align-items:center; gap:.65rem; padding:.78rem 1rem; color:var(--maroon-deep)!important; background:#fff; border-radius:6px; text-decoration:none; font-size:.9rem; font-weight:700; box-shadow:0 7px 16px rgba(30,5,15,.16); transition:transform .18s ease,box-shadow .18s ease; }
.hero-action:hover { transform:translateY(-2px); box-shadow:0 10px 20px rgba(30,5,15,.22); }
.hero-action-secondary { color:#fff!important; background:transparent; border:1px solid rgba(255,255,255,.45); box-shadow:none; }
.hero-action-secondary:hover { background:rgba(255,255,255,.1); box-shadow:none; }
.heart-stage { display:grid; place-items:center; min-height:250px; perspective:900px; }
.heart-stage::before { position:absolute; width:230px; height:230px; content:""; border:1px solid rgba(255,255,255,.2); border-radius:50%; box-shadow:0 0 0 22px rgba(255,255,255,.035),0 0 0 48px rgba(255,255,255,.025); }
.heart-object { position:relative; display:block; font-size:9rem; line-height:1; filter:drop-shadow(0 24px 20px rgba(25,4,12,.42)); transform-style:preserve-3d; animation:heart-float 5s ease-in-out infinite; }
.heart-object span { display:block; animation:heart-beat 2.4s ease-in-out infinite; }
.heart-caption { position:absolute; bottom:0; color:#f0c9d3; font-size:.72rem; font-weight:700; }
.section-heading { margin:2rem 0 .9rem; }
.section-heading h2 { margin:0!important; color:var(--maroon-deep)!important; font-family:Georgia,"Times New Roman",serif; font-size:1.8rem!important; }
.section-heading p { margin:.35rem 0 0; color:var(--muted)!important; font-size:.95rem; line-height:1.6; }
.steps-grid, .support-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:.85rem; margin:1.1rem 0; }
.support-grid { grid-template-columns:repeat(2,minmax(0,1fr)); }
.info-card, .support-item { padding:1.1rem 1.2rem; background:var(--surface); border:1px solid var(--line); border-radius:7px; box-shadow:var(--shadow); transition:transform .2s ease,box-shadow .2s ease; }
.info-card:hover, .support-item:hover { transform:translateY(-2px); box-shadow:0 17px 34px rgba(58,17,32,.12); }
.card-index, .support-tag { display:block; margin-bottom:.55rem; color:var(--maroon); font-size:.7rem; font-weight:800; }
.info-card h3, .support-item h3 { margin:0 0 .45rem; color:var(--maroon-deep)!important; font-family:Georgia,"Times New Roman",serif; font-size:1.15rem!important; }
.info-card p, .support-item p { margin:0; color:var(--muted)!important; font-size:.88rem; line-height:1.6; }
.note-band { display:grid; grid-template-columns:auto 1fr; align-items:start; gap:.8rem; margin:1.25rem 0; padding:1rem 1.1rem; background:var(--surface-tint); border:1px solid var(--line); border-left:4px solid var(--maroon); border-radius:6px; }
.note-mark { color:var(--maroon); font-weight:800; }
.note-band p { margin:0; color:var(--ink)!important; font-size:.87rem; line-height:1.6; }
.screening-intro { margin:1rem 0 1.4rem; }
.screening-intro h1 { margin:.45rem 0; color:var(--maroon-deep); font-family:Georgia,"Times New Roman",serif; font-size:2.15rem; font-weight:500; }
.screening-intro p { max-width:760px; margin:.35rem 0; color:var(--muted); line-height:1.65; }
.section-kicker { color:var(--maroon); font-size:.74rem; font-weight:800; }
.form-shell { margin-top:.6rem; padding:1.3rem 1.4rem; background:var(--surface); border:1px solid var(--line); border-radius:8px; box-shadow:var(--shadow); }
.field-group { display:flex; align-items:center; gap:.55rem; margin:0 0 .85rem; padding-bottom:.65rem; border-bottom:1px solid var(--line); color:var(--maroon-deep); font-size:.92rem; font-weight:700; }
.field-index { color:var(--maroon); font-size:.74rem; font-weight:800; }
.stApp [data-testid="stWidgetLabel"] p, .stApp label { color:var(--ink)!important; font-size:.87rem; font-weight:600; }
.stApp input, .stApp textarea, .stApp [data-baseweb="select"] > div { color:var(--ink)!important; background:var(--surface)!important; border-color:var(--line)!important; border-radius:6px!important; }
.stApp input:focus, .stApp [data-baseweb="select"] > div:focus-within { border-color:var(--maroon)!important; box-shadow:0 0 0 2px rgba(120,29,57,.12)!important; }
.stApp [data-baseweb="popover"], .stApp [role="option"] { color:var(--ink)!important; background:var(--surface)!important; }
.stApp [data-testid="stAlert"] { color:var(--ink)!important; background:var(--surface-tint)!important; border:1px solid var(--line); border-left:4px solid var(--maroon); border-radius:7px; }
.stApp [data-testid="stAlert"] > div { background:transparent!important; }
.stApp [data-testid="stAlert"] svg { color:var(--maroon)!important; }
.stApp [data-testid="stAlert"] p { color:var(--ink)!important; }
.stButton > button, .stButton > button *, .stFormSubmitButton > button, .stFormSubmitButton > button * { color:#fff!important; }
.stButton > button, .stFormSubmitButton > button { width:100%; min-height:3rem; background:var(--maroon)!important; border:1px solid var(--maroon)!important; border-radius:6px; font-weight:700; box-shadow:0 5px 12px rgba(72,19,38,.18); transition:transform .18s ease,background-color .18s ease,box-shadow .18s ease; }
.stButton > button:hover, .stFormSubmitButton > button:hover { background:var(--maroon-deep)!important; border-color:var(--maroon-deep)!important; transform:translateY(-1px); box-shadow:0 7px 16px rgba(72,19,38,.23); }
.stButton > button:focus-visible, .stFormSubmitButton > button:focus-visible { outline:3px solid #c98b9c; outline-offset:2px; }
.stProgress > div > div > div > div { background-color:var(--maroon); }
.result-panel { margin:1.2rem 0; padding:1.3rem; background:var(--surface); border:1px solid var(--line); border-left:4px solid var(--maroon); border-radius:8px; box-shadow:var(--shadow); }
.result-panel h2 { color:var(--maroon-deep); font-family:Georgia,"Times New Roman",serif; }
.result-panel p { color:var(--muted); line-height:1.6; }
.contribution-table-wrap { max-width:100%; overflow-x:auto; border:1px solid var(--line); border-radius:6px; background:var(--surface); }
.contribution-table { width:100%; border-collapse:collapse; font-size:.82rem; }
.contribution-table th { color:var(--maroon-deep); background:var(--surface-tint); font-weight:700; text-align:left; }
.contribution-table th, .contribution-table td { padding:.55rem .7rem; border-bottom:1px solid var(--line); white-space:nowrap; }
.contribution-table tbody tr:last-child td { border-bottom:0; }
.stApp [data-testid="stTable"] table { width:100%; border-collapse:collapse; font-size:.84rem; }
.stApp [data-testid="stTable"] th { color:var(--maroon-deep); background:var(--surface-tint); }
.stApp [data-testid="stTable"] td, .stApp [data-testid="stTable"] th { padding:.5rem .65rem; text-align:left; }
@keyframes rise-in { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:translateY(0); } }
@keyframes heart-float { 0%,100% { transform:rotateY(-13deg) rotateZ(-2deg) translateY(0); } 50% { transform:rotateY(13deg) rotateZ(2deg) translateY(-8px); } }
@keyframes heart-beat { 0%,72%,100% { transform:scale(1); } 78% { transform:scale(1.055); } 84% { transform:scale(1); } 90% { transform:scale(1.035); } }
@media (prefers-reduced-motion:reduce) { *,*::before,*::after { scroll-behavior:auto!important; animation-duration:.01ms!important; transition-duration:.01ms!important; } }
@media (max-width:760px) {
    .block-container { padding:.6rem .85rem 2rem; }
    .block-container [data-testid="element-container"], .block-container [data-testid="stMarkdown"], .block-container [data-testid="stMarkdownContainer"] { width:100%!important; min-width:0!important; max-width:100%!important; }
    [data-testid="stHorizontalBlock"] > :is([data-testid="column"],[data-testid="stColumn"]):has(.nav-desktop-marker) { display:none!important; }
    [data-testid="stHorizontalBlock"]:has(.nav-mobile-marker) { position:relative; min-height:48px; }
    [data-testid="stHorizontalBlock"] > :is([data-testid="column"],[data-testid="stColumn"]):has(.nav-mobile-marker) { display:flex!important; position:absolute!important; top:0; right:0; z-index:5; flex:0 0 44px!important; width:44px!important; min-width:44px!important; max-width:44px!important; height:44px; margin:0!important; }
    [data-testid="stHorizontalBlock"] > :is([data-testid="column"],[data-testid="stColumn"]):has(.nav-mobile-marker) [data-testid="stPopover"] button { display:grid!important; place-items:center; width:42px!important; min-width:42px!important; max-width:42px!important; height:42px!important; min-height:42px!important; padding:0!important; }
    .brand-copy small { font-size:.65rem; }
    [data-testid="stHorizontalBlock"]:has(.home-hero-marker) { flex-direction:column; align-items:stretch; gap:.5rem; min-height:unset; padding:1.6rem 1.25rem 1rem; }
    .hero-copy h1 { font-size:2rem!important; }
    .hero-copy p { font-size:.92rem; }
    .heart-stage { min-height:180px; }
    .heart-stage::before { width:150px; height:150px; box-shadow:0 0 0 15px rgba(255,255,255,.035),0 0 0 32px rgba(255,255,255,.025); }
    .heart-object { font-size:6.5rem; }
    .steps-grid, .support-grid { grid-template-columns:1fr; }
    .screening-intro h1 { font-size:1.8rem; }
    .form-shell { padding:1rem .85rem; }
}
@media (max-width:390px) { .brand-copy small { font-size:.62rem; } }
</style>""",
        unsafe_allow_html=True,
    )


def render_nav(active_page: str) -> None:
    brand, home, about, start, mobile_menu = st.columns(
        [3.3, .45, .45, 1.1, .7],
        gap="small",
        vertical_alignment="center",
    )
    with brand:
        st.markdown(
            '<div class="brand"><span class="brand-icon">🫀</span><span class="brand-copy"><strong>Heart Risk</strong><small>EDUCATIONAL PROJECT</small></span></div>',
            unsafe_allow_html=True,
        )
    with home:
        st.markdown('<span class="nav-desktop-marker"></span>', unsafe_allow_html=True)
        st.page_link("pages/home.py", label="Home", icon=":material/home:")
    with about:
        st.markdown('<span class="nav-desktop-marker"></span>', unsafe_allow_html=True)
        st.page_link("pages/about.py", label="About", icon=":material/info:")
    with start:
        st.markdown('<span class="nav-desktop-marker nav-start-marker"></span>', unsafe_allow_html=True)
        if st.button("Start now", key=f"nav_start_{active_page}", type="primary"):
            st.switch_page("pages/screening.py")
    with mobile_menu:
        st.markdown('<span class="nav-mobile-marker"></span>', unsafe_allow_html=True)
        with st.popover("☰", help="Open navigation menu"):
            st.page_link("pages/home.py", label="Home", icon=":material/home:")
            st.page_link("pages/about.py", label="About", icon=":material/info:")
            if st.button("Start now", key=f"mobile_nav_start_{active_page}", type="primary", use_container_width=True):
                st.switch_page("pages/screening.py")
    st.markdown('<div class="nav-rule"></div>', unsafe_allow_html=True)