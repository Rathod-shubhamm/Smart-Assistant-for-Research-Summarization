import fitz  #  for PyMuPDF

async def extract_text_from_file(file):
    content = await file.read()
    if file.filename.endswith(".pdf"):
        with open("temp.pdf", "wb"
                  ) as f:
            f.write(content)
        doc = fitz.open("temp.pdf")
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text
    elif file.filename.endswith(".txt"):
        return content.decode("utf-8")
    else:
        return "Unsupported file format"