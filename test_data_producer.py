import random
import re
import os
import time
import multiprocessing
from pathos.multiprocessing import ProcessingPool as Pool


from contextlib import contextmanager

@contextmanager
def terminating(thing):
    try:
        yield thing
    finally:
        thing.terminate()


class Base_Implementation:

    def __init__(self):
        self.synonyms = {}
        self.base_likelihood = {}
        self.total_probability = 0

    def base_percentages_generate(self, package_names_file):
        self.synonyms = {}
        pattern_category = re.compile('(\w+)\t(\d+)\n')
        pattern_synonym = re.compile('(\w+) (\w+)\n')
        with file(package_names_file, "r") as f:
            for line in f:
                m = pattern_category.match(line)
                if m:
                    target = m.group(1)
                    val = int(m.group(2))
#                    print (m.group(1),int(m.group(2)))
                    self.base_likelihood[target] = val
                    self.total_probability += val
                else:
                    n = pattern_synonym.match(line)
                    if n:
                        syn1 = n.group(1)
                        syn2 = n.group(2)
                        if syn1 in self.synonyms:
                            self.synonyms[syn1].append(syn2)
                        else:
                            self.synonyms[syn1] = [syn2]
                        if syn2 in self.synonyms:
                            self.synonyms[syn2].append(syn1)
                        else:
                            self.synonyms[syn2] = [syn1]


    def naive_implementation(self,string_part,string_category):
        target = string_category
        if target not in self.base_likelihood:
            if target in self.synonyms:
                for entry in self.synonyms:
                    if entry in self.base_likelihood:
                        target = entry
                        break
        if target not in self.base_likelihood:
            print ("Not enough data.")
            return 0
        else:
            return float(self.base_likelihood[target])/float(self.total_probability)


class Learn_Engine:
    def __init__(self):
        self.substrings = {}

    @staticmethod
    def generate_list_strings():
        words = []
        pattern = re.compile('(\w+) (\w+)\n')
        with file ("./imp/learn_uniq.txt", "r") as f:
            for line in f:
                m = pattern.match(line)
                if m:
                    target = m.group(1)
                    words.append("<" + target + ">")

        with file ("./imp/learn_strings_only.txt", "w") as f:
            for entry in words:
                f.write(entry + " ")


    @staticmethod
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







    @staticmethod
    def get_random_substring(substring_len, num=200):
        substrings = []
        filename = "./imp/learn_strings_only.txt"
        random.seed()
        with file(filename, "rb") as f:
            dist = os.path.getsize(filename)
            for _ in range(0,num):
                current_len = 1
                ran_point = random.randrange(dist)
                f.seek(ran_point, 0)
                value = f.read(1)

#                print (value)
#                print (f.read(10))

                if value == " ":
                    continue
                else:
                    #print ("%s" % value)
                    left_char = value
                    right_char = value
                    left_point = ran_point
                    right_point = ran_point
                    while current_len < substring_len:
                        current_len += 1
                        direction = 0
                        move_right = (left_char  == '<')
                        move_left = (right_char == '>')
                       # print (left_char,right_char,move_left,move_right)

                        if move_left and move_right:
                            direction = 0
                       #     print ("String blanked")
                        elif move_left:
                            direction = -1
#                            print ("Must move left")
                        elif move_right:
                            direction = 1
#                            print ("Must move right")
                        else:
                            direction = random.randrange(-1,2,2) # randomnly selects -1 or 1


                        if direction == 1:
#                            print ("Move right")
                            right_point += 1
                            f.seek(right_point,0)
                            right_char = f.read(1)
#                            print ("right_char " + right_char)
                        elif direction == -1:
#                            print ("Move left")
                            left_point -= 1
                            f.seek(left_point,0)
                            left_char = f.read(1)
#                            print ("left_char " + left_char)
                        else:
                            current_len -= 1
                            break
                    f.seek(left_point,0)
                    substring = f.read(current_len)
                    substrings.append(substring)
        return substrings


#GLOBAL_SUBSTRINGS = {}

def find_substring_occurrence(substrings):
    GLOBAL_SUBSTRINGS = {}
    filename = "./imp/learn_strings_only.txt"
    with file(filename, "rb") as f:
        megabytes = f.read()
        for entry in substrings:
            if entry in GLOBAL_SUBSTRINGS:
                continue
            p = re.compile(entry)
            result = p.findall(megabytes)
            GLOBAL_SUBSTRINGS[entry] = len(result)

    return GLOBAL_SUBSTRINGS



if __name__ == '__main__':
    naive = Base_Implementation()
    learn = Learn_Engine()

    naive.base_percentages_generate("./imp/package_no_comments.txt")

    print (naive.naive_implementation("Blank","0603"))

    strt_time = time.time()
    print ("Starting process at %d" % strt_time)


    substrings = []
    for _ in range(0,16):
        substrings.append(Learn_Engine.get_random_substring(5, num=10000))

    total_len = 0
    for entry in substrings:
        total_len += len(entry)

    print ("%d substrings identified at %d" % (total_len, time.time()))

    processes = []
    outputs = {}


    with terminating(Pool(processes=8)) as pool:
        for entry in pool.map(find_substring_occurrence,substrings):
            outputs = dict(outputs, **entry)






    finish_time = time.time()
    print ("%d Substrings learned at %d" % (len(outputs), finish_time))
    print ("Total time - %d" % (finish_time - strt_time))


