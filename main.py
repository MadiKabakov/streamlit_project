import streamlit as st
from PyPDF2 import PdfReader
import json

import google.generativeai as genai

def get_pdf_text(pdf):
    text = ""
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

API_KEY = "AIzaSyDq4dLRG_V8ur6BGdRmFTb2KtNw_znbWp4"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-pro')

prompt_template = """
Входные данные:
- Должность (Position): %s
- Описание должности (Position description): %s
- Резюме кандидата (Applicant resume): %s

Проанализируйте предоставленные данные и генерируйте выводы исключительно в формате JSON. Важно, чтобы ответ содержал только информацию, организованную в следующую структуру JSON, без каких-либо дополнительных объяснений или текста за пределами JSON-формата:

{
  "Applicant_name": "Извлеченное из резюме полное имя кандидата",
  "Short_Description": "Краткое описание профессионального профиля кандидата, включая ключевые навыки и опыт работы",
  "Advice_from_AI": "Совет рекрутеру или руководителю отдела относительно пригодности кандидата на основе анализа резюме и требований к должности",
  "Applicant_score": "Оценка кандидата на шкале от 1 до 100, основанная на соответствии квалификации, опыта работы и образования требованиям указанной должности"
}

Обратите внимание, что результат анализа должен быть строго в указанном формате JSON. Никакие дополнительные данные или комментарии вне JSON-структуры не допускаются.

"""


st.set_page_config(
        page_title="Gemini PDF Chatbot",
        page_icon="🤖"
    )


st.title('Main theme')

with st.sidebar:
    pdf_doc = st.file_uploader(
        label="Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=False
    )
    if st.button("Submit & Process"):
        with st.spinner("Processing..."):
            raw_text = get_pdf_text(pdf_doc)
            st.success("Done")

txt = st.text_area(label="Вставьте сюда текст резюме")

position = "analyst"
description = "analyst jobs"



analazy_button = st.button("Analyze", type="primary")

if analazy_button and pdf_doc:
    response = model.generate_content(prompt_template % (position, description, get_pdf_text(pdf_doc)))
    json_resp = json.loads(response.text)
    st.write(json_resp['Applicant_name'])
    st.write(json_resp['Short_Description'])
    st.write(json_resp['Advice_from_AI'])
    st.write(json_resp['Applicant_score'])
else:
    st.write("Нет файла")