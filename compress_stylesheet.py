with open("style.css", "r") as file:
    text = file.read()
    text = text.replace("  ", "")
    #text = text.replace("{", "\\{")
    #text = text.replace("}", "\\}")
    text = text.replace("\n", "")
    with open("comporessed_style.css", "w") as out_file:
        out_file.write(text)