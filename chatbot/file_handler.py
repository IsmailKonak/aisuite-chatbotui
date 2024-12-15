from tika import parser

def extract_text_with_tika(file_path):
    parsed = parser.from_file(file_path)
    return parsed.get("content", "")
