import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from database import init_db, save_analysis, get_history, clear_history
from nlp_utils import analyze_text, summarize_text
from pdf_report import create_pdf_report

st.set_page_config(page_title="MindSpace AI | Study Planner", page_icon="✦", layout="wide")
init_db()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');
:root{--ink:#211a35;--muted:#817a95;--purple:#7652d6;--line:#e9e4f3;--canvas:#faf9fd}
.stApp{background:var(--canvas);color:var(--ink);font-family:'DM Sans',sans-serif}
[data-testid="stHeader"]{background:rgba(250,249,253,.92)}
.block-container{padding-top:2rem;padding-bottom:3rem;max-width:1440px}
h1,h2,h3,h4{color:var(--ink)!important;font-family:'Plus Jakarta Sans',sans-serif!important;letter-spacing:-.03em}
[data-testid="stSidebar"]{background:#241b3b;border-right:1px solid #35284f}
[data-testid="stSidebar"] *{color:#f6f1ff!important}
[data-testid="stSidebar"] [data-testid="stRadio"] label{border-radius:10px;padding:8px 10px}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover{background:#382b55}
[data-testid="stSidebar"] hr{border-color:#493a65}
.brand-mark{display:inline-flex;width:42px;height:42px;align-items:center;justify-content:center;border-radius:14px;background:linear-gradient(135deg,#a78bfa,#7450d4);font-size:22px;margin-bottom:12px}
.brand-name{font-family:'Plus Jakarta Sans';font-size:20px;font-weight:800;color:white}
.brand-caption{color:#b8abcf!important;font-size:11px;margin-top:5px;letter-spacing:.1em}
.hero{background:linear-gradient(115deg,#30204f,#6545b2 55%,#9272e7);border-radius:24px;padding:30px 34px;color:white;margin:4px 0 24px;box-shadow:0 16px 40px rgba(76,49,139,.16)}
.hero h1{color:white!important;font-size:34px!important;margin:0 0 8px}
.hero p{color:#eee8ff!important;font-size:15px;margin:0}
.chip{display:inline-block;padding:6px 11px;border:1px solid #ffffff44;border-radius:30px;color:#f3edff;font-size:11px;font-weight:700;margin-bottom:14px}
.section-title{font-family:'Plus Jakarta Sans';font-size:19px;font-weight:800;color:#211a35;margin:20px 0 12px}
.metric-card,.panel{background:white;border:1px solid var(--line);border-radius:18px;padding:19px;box-shadow:0 5px 18px #2d1f4c09}
.metric-card{min-height:112px}.metric-label{color:var(--muted);font-size:11px;font-weight:700;letter-spacing:.06em}
.metric-value{color:var(--ink);font-family:'Plus Jakarta Sans';font-size:29px;font-weight:800;margin-top:8px}
.metric-icon{float:right;background:#f1edff;border-radius:12px;padding:8px 10px;color:var(--purple)}
.eyebrow{color:#7652d6;font-size:11px;font-weight:800;letter-spacing:.13em}
.soft-note{background:#f1edff;border:1px solid #e5dcff;border-radius:14px;padding:14px 16px;color:#51416f}
.result-card{background:linear-gradient(135deg,#f5f1ff,#fff);border:1px solid #e6ddfb;border-radius:18px;padding:20px}
div.stButton>button,div.stDownloadButton>button{background:linear-gradient(100deg,#7652d6,#9272e7)!important;color:white!important;border:0!important;border-radius:11px!important;padding:.62rem 1.1rem!important;font-weight:700!important}
div.stButton>button:hover,div.stDownloadButton>button:hover{background:#5d3db6!important}
div[data-baseweb="input"]>div,div[data-baseweb="textarea"]>div,div[data-baseweb="select"]>div{border-radius:11px!important;border-color:#e3ddec!important;background:white!important}
.stTextInput label,.stTextArea label,.stDateInput label,.stTimeInput label,.stSlider label{color:#514766!important;font-weight:700!important}
[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:14px;overflow:hidden}
div[data-testid="stMetric"]{background:white;border:1px solid var(--line);padding:15px;border-radius:16px}
footer{visibility:hidden}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div style="padding:12px 4px 24px"><div class="brand-mark">✦</div><div class="brand-name">MindSpace AI</div><div class="brand-caption">YOUR PERSONAL STUDY COMPANION</div></div>', unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("WORKSPACE", ["Overview","Analyze Notes","Study Planner","History","About"])
    st.markdown("---")
    st.caption("Organize your learning, understand your notes, and build consistent study habits.")
    st.markdown("<div style='height:25px'></div><small style='color:#b8abcf'>✦ MindSpace AI · Local workspace</small>", unsafe_allow_html=True)

def hero(kicker,title,subtitle):
    st.markdown(f'<div class="hero"><div class="chip">{kicker}</div><h1>{title}</h1><p>{subtitle}</p></div>',unsafe_allow_html=True)

def metric(label,value,icon):
    st.markdown(f'<div class="metric-card"><span class="metric-icon">{icon}</span><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>',unsafe_allow_html=True)

records=get_history()
df=pd.DataFrame(records,columns=["id","created_at","topic","sentiment","polarity","word_count","summary"])

if page=="Overview":
    hero("YOUR LEARNING SPACE","Make every study session count.","A calmer, smarter way to understand your notes and stay on track.")
    total=len(df); positive=int((df.sentiment=="Positive").sum()) if total else 0
    words=int(df.word_count.sum()) if total else 0
    polarity=f"{df.polarity.mean():.2f}" if total else "—"
    cols=st.columns(4)
    for col,(lab,val,ico) in zip(cols,[("TOTAL ANALYSES",total,"✦"),("POSITIVE NOTES",positive,"☺"),("WORDS REVIEWED",f"{words:,}","▤"),("AVG. POLARITY",polarity,"◈")]):
        with col: metric(lab,val,ico)
    st.markdown('<div class="section-title">Your learning activity</div>',unsafe_allow_html=True)
    if df.empty:
        st.markdown('<div class="soft-note">Your workspace is ready. Start by analyzing a set of study notes to see your insights and activity charts here.</div>',unsafe_allow_html=True)
        st.write("")
        if st.button("✦ Analyze my first notes"): st.session_state["page_hint"]="Analyze Notes"; st.rerun()
    else:
        df["created_at"]=pd.to_datetime(df["created_at"])
        a,b=st.columns(2)
        with a:
            counts=df.sentiment.value_counts().rename_axis("Sentiment").reset_index(name="Count")
            fig=px.pie(counts,names="Sentiment",values="Count",hole=.68,color_discrete_sequence=["#7652d6","#a78bfa","#d8cafa"])
            fig.update_layout(title="Sentiment overview",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#514766",margin=dict(t=55,b=10,l=10,r=10))
            with st.container(border=True): st.plotly_chart(fig,use_container_width=True)
        with b:
            trend=df.groupby(df.created_at.dt.date,as_index=False).word_count.sum(); trend.columns=["Date","Words"]
            fig=px.area(trend,x="Date",y="Words",markers=True); fig.update_traces(line_color="#7652d6",fillcolor="rgba(118,82,214,.13)")
            fig.update_layout(title="Words analyzed over time",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#514766",margin=dict(t=55,b=10,l=10,r=10))
            with st.container(border=True): st.plotly_chart(fig,use_container_width=True)
        st.markdown('<div class="section-title">Recently analyzed</div>',unsafe_allow_html=True)
        st.dataframe(df[["created_at","topic","sentiment","word_count"]].head(5),use_container_width=True,hide_index=True)

elif page=="Analyze Notes":
    hero("AI NOTE INSIGHTS","Turn your notes into clarity.","Explore the tone, key terms, and a concise summary of your study material.")
    left,right=st.columns([1.55,1])
    with left:
        with st.container(border=True):
            topic=st.text_input("SUBJECT OR TOPIC",placeholder="e.g. Computer Networks")
            notes=st.text_area("YOUR STUDY NOTES",height=280,placeholder="Paste your class notes, textbook content, or revision material here...")
            use_transformer=st.checkbox("Use Hugging Face abstractive summarization (optional model download)")
            analyze=st.button("✦ Analyze study notes",type="primary",use_container_width=True)
    with right:
        st.markdown('<div class="panel"><div class="eyebrow">HOW IT WORKS</div><h3>A little more insight, every time.</h3><p style="color:#817a95">Your notes are processed locally and your analysis is saved in your project database.</p><hr><b>01 · Sentiment</b><p style="color:#817a95;font-size:13px">Understand the overall tone of your text.</p><b>02 · Keywords</b><p style="color:#817a95;font-size:13px">Identify useful terms with NLTK.</p><b>03 · Summary</b><p style="color:#817a95;font-size:13px">Get a short overview for quick revision.</p></div>',unsafe_allow_html=True)
    if analyze:
        if not notes.strip(): st.warning("Please paste some study notes before analyzing.")
        else:
            with st.spinner("Reading your notes and preparing insights..."):
                result=analyze_text(notes); summary=summarize_text(notes,use_transformer)
                save_analysis(topic.strip() or "Untitled topic",result["sentiment"],result["polarity"],result["word_count"],summary)
            st.success("Your analysis is complete and saved to History.")
            st.markdown('<div class="section-title">Your results</div>',unsafe_allow_html=True)
            a,b,c=st.columns(3)
            with a: metric("SENTIMENT",result["sentiment"],"☺")
            with b: metric("POLARITY",f'{result["polarity"]:.2f}',"◈")
            with c: metric("WORD COUNT",f'{result["word_count"]:,}',"▤")
            st.write("")
            x,y=st.columns([1.25,1])
            with x:
                st.markdown('<div class="panel"><div class="eyebrow">QUICK REVISION</div><h3>Summary</h3></div>',unsafe_allow_html=True); st.info(summary)
            with y:
                st.markdown('<div class="panel"><div class="eyebrow">KEY TERMS</div><h3>Cleaned keywords</h3></div>',unsafe_allow_html=True)
                st.write(", ".join(result["keywords"]) if result["keywords"] else "No keywords found.")
            pdf=create_pdf_report(topic.strip() or "Untitled topic",result,summary)
            st.download_button("↓ Download PDF analysis report",pdf,"study_analysis_report.pdf","application/pdf")

elif page=="Study Planner":
    hero("PLAN WITH PURPOSE","Build a study routine that works.","Set a clear goal, choose your focus time, and make your next session count.")
    with st.container(border=True):
        st.markdown('<div class="eyebrow">NEW STUDY SESSION</div><h3>What would you like to work on?</h3>',unsafe_allow_html=True)
        with st.form("planner_form"):
            subject=st.text_input("SUBJECT",placeholder="e.g. Database Management Systems")
            a,b=st.columns(2)
            with a: study_date=st.date_input("DATE",value=date.today())
            with b: start_time=st.time_input("START TIME")
            duration=st.slider("FOCUS DURATION",15,240,60,step=15)
            goal=st.text_area("SESSION GOAL",placeholder="e.g. Revise normalization and solve 10 practice questions.")
            submitted=st.form_submit_button("＋ Create study session",type="primary",use_container_width=True)
    if submitted:
        if not subject.strip(): st.warning("Please enter a subject.")
        else:
            st.success("Your study session is ready.")
            st.markdown(f'<div class="result-card"><div class="eyebrow">YOUR STUDY SESSION</div><h2>{subject}</h2><p style="color:#817a95">{study_date.strftime("%A, %d %B %Y")} · {start_time.strftime("%I:%M %p")} · {duration} minutes</p><b>Today\'s goal</b><p>{goal or "Review the selected topic and make concise notes."}</p></div>',unsafe_allow_html=True)
            st.caption("Tip: Take a short break after each 25–30 minute focus block.")

elif page=="History":
    hero("YOUR PROGRESS","Your learning, all in one place.","Review previous note analyses and export your activity whenever you need it.")
    if df.empty: st.markdown('<div class="soft-note">No saved analyses yet. Your completed note analyses will appear here.</div>',unsafe_allow_html=True)
    else:
        st.dataframe(df[["created_at","topic","sentiment","polarity","word_count","summary"]],use_container_width=True,hide_index=True)
        a,b=st.columns(2)
        with a: st.download_button("↓ Export history as CSV",df.to_csv(index=False).encode("utf-8"),"study_history.csv","text/csv")
        with b:
            if st.button("Clear all history"): clear_history(); st.rerun()

else:
    hero("ABOUT MINDSPACE AI","Designed for focused learning.","A student-friendly application combining text analysis, planning, and useful progress insights.")
    st.markdown('<div class="section-title">Technology stack</div>',unsafe_allow_html=True)
    tech=[("Python 3.10+","Application logic"),("Streamlit","Interactive web interface"),("TextBlob","Lexicon-based sentiment polarity"),("NLTK","Tokenization, stop-word removal, lemmatization"),("Hugging Face Transformers","Optional abstractive summarization"),("PyTorch","Optional Transformers backend"),("SQLite","Local analysis history"),("Pandas + Plotly","Dashboard data and interactive charts"),("ReportLab","Downloadable PDF reports"),("VS Code","Development environment")]
    cols=st.columns(2)
    for i,(name,desc) in enumerate(tech):
        with cols[i%2]: st.markdown(f'<div class="panel" style="margin-bottom:12px"><b>{name}</b><div style="color:#817a95;font-size:13px;margin-top:5px">{desc}</div></div>',unsafe_allow_html=True)
    st.caption("Sentiment analysis is an educational text-processing feature and is not a measure of academic performance or wellbeing.")
