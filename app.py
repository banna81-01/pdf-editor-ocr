
import streamlit as st
from PyPDF2 import PdfReader
from io import BytesIO
from reportlab.pdfgen import canvas

st.set_page_config(page_title="PDF Editor", layout="wide")
st.title("📝 Simple PDF Text Extractor & Editor (Demo Only)")

uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_pdf:
    reader = PdfReader(uploaded_pdf)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    st.subheader("🧾 Editable Extracted Text (Text Layer Only)")
    edited_text = st.text_area("Edit below:", text, height=400)

    if st.button("📄 Generate Edited PDF"):
        buffer = BytesIO()
        c = canvas.Canvas(buffer)
        text_object = c.beginText(40, 800)
        text_object.setFont("Helvetica", 12)

        for line in edited_text.splitlines():
            if text_object.getY() <= 50:
                c.drawText(text_object)
                c.showPage()
                text_object = c.beginText(40, 800)
                text_object.setFont("Helvetica", 12)
            text_object.textLine(line)

        c.drawText(text_object)
        c.save()
        buffer.seek(0)

        st.success("✅ Edited PDF Ready")
        st.download_button("⬇️ Download Edited PDF", buffer, file_name="edited_output.pdf", mime="application/pdf")
