def load_script(path: str) -> str:
    with open(path, 'r', encoding='utf8') as file:
        return file.read()
