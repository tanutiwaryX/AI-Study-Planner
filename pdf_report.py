from io import BytesIO
from datetime import datetime
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def create_pdf_report(topic,result,summary):
    buffer=BytesIO()
    doc=SimpleDocTemplate(buffer,pagesize=A4,rightMargin=.7*inch,leftMargin=.7*inch,topMargin=.7*inch,bottomMargin=.7*inch)
    styles=getSampleStyleSheet()
    story=[Paragraph("MindSpace AI - Study Analysis Report",styles["Title"]),Spacer(1,12),
           Paragraph(f"<b>Topic:</b> {escape(topic)}",styles["BodyText"]),
           Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%d %B %Y, %I:%M %p')}",styles["BodyText"]),
           Spacer(1,14),Paragraph("Analysis Results",styles["Heading2"]),
           Paragraph(f"<b>Sentiment:</b> {escape(result['sentiment'])}",styles["BodyText"]),
           Paragraph(f"<b>Polarity:</b> {result['polarity']:.2f}",styles["BodyText"]),
           Paragraph(f"<b>Word count:</b> {result['word_count']}",styles["BodyText"]),
           Spacer(1,14),Paragraph("Summary",styles["Heading2"]),
           Paragraph(escape(summary).replace("\\n","<br/>"),styles["BodyText"]),
           Spacer(1,14),Paragraph("Cleaned keywords",styles["Heading2"]),
           Paragraph(escape(", ".join(result.get("keywords",[])) or "None"),styles["BodyText"])]
    doc.build(story)
    return buffer.getvalue()
