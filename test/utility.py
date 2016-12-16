def read_file(file_path):
    """
    Read file
    """
    f = open(file_path, encoding='utf-8')
    file_content = f.read()
    f.close()
    return file_content
