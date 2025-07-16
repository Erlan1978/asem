from asem import interpret

with open("bagdarlama.as", encoding="utf-8") as f:
    code = f.read()

interpret(code)
