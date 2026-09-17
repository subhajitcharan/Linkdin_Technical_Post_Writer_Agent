import json
def notebook_file(raw_text):
    notebook_data = json.loads(raw_text)
    code_blocks = []
    for cell in notebook_data.get("cells", []):
        if cell.get("cell_type") == "code":
            code_blocks.extend(cell.get("source", []))
            code_blocks.append("\n\n")
    content = "".join(code_blocks)
    return content