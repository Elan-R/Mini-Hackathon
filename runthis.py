import os

global INDENT
INDENT = 3

class Folder:
    def __init__(self, name, files = None):
        i = ""
        while os.path.exists(name + i):
            try:
                i = str(int(i) + 1)
            except:
                i = "1"
        name += i
        self.name = name.strip()
        self.files = files if isinstance(files, list) else []

    def add(self, obj):
        obj.parent = self
        self.files.append(obj)

    def pretty_print(self, indent):
        s = " " * (indent - INDENT) + ("|" if indent > 0 else "\n") + "-" * (INDENT if indent > 0 else 0) + self.name + "/\n"
        for file in self.files:
            s += file.pretty_print(indent + INDENT)
        return s

    def create(self, path):
        if not self.name == "ñéw_dír":
            path = path + "/" + self.name
            os.mkdir(path)
        for file in self.files:
            file.create(path)

class File:
    def __init__(self, name):
        self.name = name.strip()

    def pretty_print(self, indent):
        return " " * (indent - INDENT) + "|" + "-" * INDENT + self.name + "\n"

    def create(self, path):
        f = open(path + "/" + self.name, "w+")
        f.close()

class Parser:
    def __init__(self, string):
        self.string = string
        self.objs = self.parse()
        self.pretty_print()
        self.create()

    def parse(self):
        current_name = ""
        current_dir = Folder("ñéw_dír")
        temp_cd = current_dir
        for char in self.string:
            if char == ",":
                if current_name.strip() != "":
                    temp_cd.add(File(current_name))
                current_name = ""
            elif char == "[":
                if current_name.strip() == "":
                    current_name = "Unnamed Folder"
                f = Folder(current_name)
                temp_cd.add(f)
                temp_cd = f
                current_name = ""
            elif char == "]":
                if current_name.strip() != "":
                    temp_cd.add(File(current_name))
                temp_cd = temp_cd.parent
                current_name = ""
            else:
                current_name += char
        if current_name.strip() != "":
            current_dir.add(File(current_name))
        return current_dir

    def pretty_print(self):
        s = self.objs.pretty_print(0)
        print(s)
        return s

    def create(self):
        self.objs.create("./")

Parser(input("String: "))
