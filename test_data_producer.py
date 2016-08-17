with file("./res/clean_package_names.txt", "r") as f:
    read_line = f.readline()
    while read_line is not "":
        print read_line.strip("\n")
        read_line = f.readline()