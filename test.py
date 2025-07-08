from langchain_community.document_loaders import PDFPlumberLoader

loader = PDFPlumberLoader("resume.pdf")
docs = loader.load()
print(docs)
print(docs[0])