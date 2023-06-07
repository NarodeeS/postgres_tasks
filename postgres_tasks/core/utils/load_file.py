def load_file(file) -> str:
    with file.open('r') as opened_file:
        return opened_file.read()
