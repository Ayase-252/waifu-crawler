def read_file(file_path):
    """
    Read file
    """
    f = open(file_path, encoding='utf-8')
    file_content = f.read()
    f.close()
    return file_content


def read_as_binary(file_path):
    """
    Reads text file then converts it to binary code.
    """
    with open(file_path, mode='r', encoding='utf-8') as f:
        content = f.read()
    return content.encode('utf-8')
