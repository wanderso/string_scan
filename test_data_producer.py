test_data = []
learn_data = []
learn_odds = 0.9

with file("./res/clean_package_names.txt", "r") as f:
    for line in f:
        if len(line.strip()) is not 0 and line.strip()[0] is not "#":
            learn_data.append(line)

with file("./imp/package_no_comments.txt", "w") as f:
    for entry in learn_data:
        f.write(entry)


