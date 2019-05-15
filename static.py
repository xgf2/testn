
def read_file(full_path):
    with open(full_path, 'r') as static_file:
        content = static_file.read()
        return content
