import random

def generate_test_data():

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

    learn_data = []

    with file("./res/train_uniq.txt", "r") as f:
        for line in f:
            if random.random() > learn_odds:
                test_data.append(line)
            else:
                learn_data.append(line)

    with file("./imp/learn_uniq.txt", "w") as f:
        for entry in learn_data:
            f.write(entry)

    with file("./imp/test_uniq.txt", "w") as f:
        for entry in test_data:
            f.write(entry)

