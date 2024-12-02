import fitz  
import ollama

def extract_text_from_pdf(pdf_path):
 
    document = fitz.open(pdf_path)
    text = ""


    for page_num in range(document.page_count):
        page = document[page_num]
        text += page.get_text("text")  

    document.close()
    return text

pdf_path = "C:\\Users\\Lenovo\\Downloads\\ai(1-3) (1).docx"
extracted_text = extract_text_from_pdf(pdf_path)

desiredmodel='llama3.2:3b'

ask="Provide summary and key highlights from the following text with also explain the key concepts from the text as well as notes : "+ extracted_text
response=ollama.chat(model=desiredmodel,messages=[{
    'role':'user',
    'content':ask,
},
])

final=response['message']['content']
print(final)

