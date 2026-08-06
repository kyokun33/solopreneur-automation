import pypdf
reader = pypdf.PdfReader(r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\scratch\appendix_final_test.pdf")
print("=== PAGE 7 TEXT ===")
print(reader.pages[6].extract_text())
