import random
import re
import os
import time
import ast
from pathos.multiprocessing import ProcessingPool as Pool


#from contextlib import contextmanager

#@contextmanager
#def terminating(thing):
#    try:
#        yield thing
#    finally:
#        thing.terminate()


class Base_Implementation:

    def __init__(self):
        self.synonyms = {}
        self.base_likelihood = {}
        self.total_probability = 0

    def base_percentages_generate(self, package_names_file):
        self.synonyms = {}
        with file(package_names_file, "r") as f:
            for line in f:
#                m = pattern_category.match(line)
                if '\t' in line:
                    m = line.rsplit('\t', 1)
                    target = m[0]
                    val = int(m[1])
                    self.base_likelihood[target] = val
                    self.total_probability += val
                else:
                    m = line.rsplit(' ', 1)
                    if m[1]:
                        syn1 = m[0]
                        syn2 = m[1]
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
        with file ("./imp/learn_uniq.txt", "r") as f:
            megabytes = f.read()
            file_lines = megabytes.split('\n')
            for line in file_lines:
                word = line.rsplit(' ', 1)[0]
                if word:
                    words.append("<" + word + ">")

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











#GLOBAL_SUBSTRINGS = {}

def find_substring_occurrence_nocheck(substrings):
    GLOBAL_SUBSTRINGS = {}
    filename = "./imp/learn_strings_only.txt"
    with file(filename, "rb") as f:
        megabytes = f.read()
        file_lines = megabytes.split('\n')
        for entry in substrings:
            if entry in GLOBAL_SUBSTRINGS:
                continue
            result = megabytes.count(entry)
            GLOBAL_SUBSTRINGS[entry] = result

    return GLOBAL_SUBSTRINGS

def find_substring_occurrence(substrings,existing_keys):
    GLOBAL_SUBSTRINGS = {}
    walkover = 0
    filename = "./imp/learn_strings_only.txt"
    with file(filename, "rb") as f:
        megabytes = f.read()
        file_lines = megabytes.split('\n')
        for entry in substrings:
            if entry in existing_keys:
                walkover += 1
                continue
            result = megabytes.count(entry)
            GLOBAL_SUBSTRINGS[entry] = result
   # print ("Walkovers: %d" % walkover)
    return GLOBAL_SUBSTRINGS


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

def get_substring_dict(substrings, existing_keys):
    filename = "./imp/learn_uniq.txt"
    substring_dict_list = {}
    walkover = 0
    with file(filename, "rb") as f:
        megabytes = f.read()
        file_lines = megabytes.split('\n')
        for entry in substrings:
            entry_corrected = entry.strip("<>")
            entry_dict = {}
            for line in file_lines:
                found = False
                if entry[0] == '<':
                    if entry_corrected in line[:len(entry_corrected)]:
                        found = True
                elif entry[-1] == '>':
                    if entry_corrected in line.rsplit(' ', 1)[0][-len(entry_corrected):]:
                        found = True
                else:
                    if entry_corrected in line:
                        found = True

                if found:
                    object_group = line.split(" ")[-1]
                    if object_group in entry_dict:
                        entry_dict[object_group] += 1
                    else:
                        entry_dict[object_group] = 1
            substring_dict_list[entry] = entry_dict

    return substring_dict_list


def split_list(list_in, num):
    ret_list = []
    if num <= 1:
        return list_in
    split_val = len(list_in) / (num)
#    print split_val
    for i in range(num+1):
        ret_list.append(list_in[(i*split_val):((i+1)*split_val)])

#    print("In split list %d, %d, %d " % (num, split_val, ((num) * split_val)))
    return ret_list

def generate_substring_input():
    naive = Base_Implementation()
    learn = Learn_Engine()

    naive.base_percentages_generate("./imp/package_no_comments.txt")

#    print (naive.naive_implementation("Blank", "0603"))

    strt_time = time.time()
    print ("Starting process at %d" % strt_time)

    substring_length = 5
    substrings = []

    frequency_filename = "./runs/substring_len_" + str(substring_length) + "_frequency.txt"

    for _ in range(0, 8):
        substrings.append(get_random_substring(substring_length, num=100))

    total_len = 0
    for entry in substrings:
        total_len += len(entry)

    print ("%d substrings identified at %d" % (total_len, time.time()))

    processes = []
    outputs = {}

    if os.path.isfile(frequency_filename):
        with file(frequency_filename, "r") as f:
            for line in f:
                m = line.rsplit(' ', 1)
                if m[1]:
                    outputs[m[0]] = int(m[1])

    total_imported = len(outputs)
    print ("%d substrings loaded at %d" % (total_imported, time.time()))

    pool = Pool(processes=8)

    # with terminating(Pool(processes=8)) as pool:
    #     output_array = []
    #     for _ in range(0,len(substrings)):
    #         output_array.append(outputs)
    #     for entry in pool.map(find_substring_occurrence,substrings,output_array):
    #         outputs = dict(outputs, **entry)

    #    with terminating(Pool(processes=8)) as pool:
    key_array = []
    for _ in range(0, len(substrings)):
        key_array.append(outputs.keys())
    for entry in pool.map(find_substring_occurrence, substrings, key_array):
        outputs = dict(outputs, **entry)

    learn_finish_time = time.time()
    print ("%d substrings learned at %d" % (len(outputs) - total_imported, learn_finish_time))
    print ("Time elapsed - %d" % (learn_finish_time - strt_time))

    with file(frequency_filename, "w") as f:
        for key in outputs:
            f.write(key + " " + str(outputs[key]) + "\n")

    substring_frequency_savename = "./runs/substring_len_" + str(substring_length) + "_dictionary.txt"
    substring_frequency_dict = {}

    if os.path.isfile(substring_frequency_savename):
        with file(substring_frequency_savename, "r") as f:
            for line in f:
                if line:
                    a = line[:substring_length]
                    b = line[substring_length+1:]
                    substring_frequency_dict[a] = ast.literal_eval(b)

    #print (substring_frequency_dict.keys())

    existing_substring_load_dict = len(substring_frequency_dict)

    print ("Length of existing substring load dictionary - %d" % existing_substring_load_dict)

    counts = {}
    for key in outputs:
        if outputs[key] in counts:
            counts[outputs[key]] += 1
        else:
            counts[outputs[key]] = 1

    #print counts

    #print counts.keys().sort(key=int)

    sorted_key_list = counts.keys().sort()

    total = 0

    sweet_spot = 0.95
    target = int(float(len(outputs)) * sweet_spot)
    list_targets = []
    for key in sorted_key_list:
        total += counts[key]
        if total > target:
            list_targets.append(key)

    #print list_targets

    print ("Targeting all entries >= %d" % list_targets[0])

    check_substring_targets = []

    for key in outputs:
        if int(outputs[key]) >= list_targets[0]:
            check_substring_targets.append(key)

    print ("%d substrings targeted for deep learning" % len(check_substring_targets))

    ck_list = split_list(check_substring_targets, 8)

    #    output = []
    #    output = get_substring_dict(check_substring_targets)


    #    for entry in ck_list:
    #        print len(entry)


    key_array = []
    for _ in range(0, len(ck_list)):
        key_array.append(substring_frequency_dict.keys())
    for entry in pool.map(get_substring_dict, ck_list, key_array):
        substring_frequency_dict = dict(substring_frequency_dict, **entry)

    substring_dict_time = time.time()
    #    print substring_frequency_dict

    print ("Learned %d substrings in - %d" % (
    len(substring_frequency_dict) - existing_substring_load_dict, (substring_dict_time - learn_finish_time)))

    with file(substring_frequency_savename, "w") as f:
        for key in substring_frequency_dict:
            f.write(key + " " + str(substring_frequency_dict[key]) + "\n")

    finish_time = time.time()
    print ("Wrote %d substrings to disk in - %d" % (len(substring_frequency_dict), (finish_time - substring_dict_time)))

    print ("Total time - %d" % (finish_time - strt_time))


def calculate_string_probability_for_target(input_list):
    # Chain rule - P(A,B) = P(B|A)P(A)
    #            - P(A,B,C,D) = P(D|A,B,C)P(C|A,B)P(B|A)P(A)

    # Bayes' Law - P(A|B) = P(B|A)*P(A)/P(B)
    #            - P(A|B) = P(A,B)/P(B)

    # Probability that String is-a Target: A
    # Probability that String
    # P(A) = P(A|B)*P(B) / P(B|A)

    # P(A|B,C,D...) = P(A,B,C,D...)/P(B,C,D...)

    # Fsck, doing it right is O(n^2) on n=number of saved substrings. We'll have to approximate.

    total_flag = "__TOTAL__><"



    substring_length = 5

    substring_frequency_savename = "./runs/substring_len_" + str(substring_length) + "_dictionary.txt"
    substring_frequency_dict = {}

    total_frequency_dict = {}

    if os.path.isfile(substring_frequency_savename):
        with file(substring_frequency_savename, "r") as f:
            for line in f:
                if line:
                    a = line[:substring_length]
                    b = line[substring_length + 1:]
                    substring_frequency_dict[a] = ast.literal_eval(b)

    output_list = []



    for string in input_list:
        string_anchored = "<" + string + ">"

        substrings_in_input = []

        for i in range(0, (len(string_anchored)-substring_length+1),1):
            substrings_in_input.append(string_anchored[i:i+5])

     #   print substrings_in_input

        substrings_in_dictionary = {}
        category_possibilities = {}

        for entry in substrings_in_input:
            if entry in substring_frequency_dict:
                #print substring_frequency_dict[entry]
                total_items_in_category = 0
                target_items_in_category = {}
                substrings_in_dictionary[entry] = substring_frequency_dict[entry]
                for category in substring_frequency_dict[entry]:
                    if category not in category_possibilities:
                        category_possibilities[category] = 1.0
                    target_items_in_category[category] = substring_frequency_dict[entry][category]
                    total_items_in_category += substring_frequency_dict[entry][category]
                    total_frequency_dict[entry] = total_items_in_category
                #substrings_in_dictionary.append(substring_frequency_dict[entry])
    #            category_possibilities[entry]
                #percentage = (float(target_items_in_category[target]) / float(total_items_in_category))
                #print ("For string %s, %f probability across %d appearances" % (entry, percentage, total_items_in_category))

        # How to make the approximation algorithm?
        # Should return a number between 0 and 1 to indicate probability fitness
        # Unanimity == V. good
        # Floor? Not for start

        #Super-naive version:

    #    category_probability_dict = {}

    #    for entry in category_possibilities.keys():
    #        category_probability_dict[entry] = 1.0

    #    print substrings_in_dictionary.keys()

        for entry in substrings_in_input:
            if entry in substring_frequency_dict:
                for category in category_possibilities:
                    current_prob = category_possibilities[category]
                    if category in substrings_in_dictionary[entry]:
                        new_factor = float(substrings_in_dictionary[entry][category])
                    else:
                        new_factor = 0.1
                    category_possibilities[category] = category_possibilities[category] * (new_factor / float(total_frequency_dict[entry]))


        if total_flag in category_possibilities:
            print ("Total flag here")

  #      print category_possibilities

    #    return category_possibilities

        top_num = 0.0
        second_num = 0.0
        top_num_category = None

        for entry in category_possibilities:
            if category_possibilities[entry] >= top_num:
                second_num = top_num
                top_num_category = entry
                top_num = category_possibilities[entry]
            elif category_possibilities[entry] >= second_num:
                second_num = category_possibilities[entry]

        if top_num > (second_num * 2.5):
            output_list.append((string, top_num_category))

        else:
            output_list.append((string, None))

    return output_list


def test_ai_against_data():
    testdata = "./imp/test_uniq.txt"

    test_data_dict = {}

    print ("Loading test data...")

    int_lines = 0

    with file(testdata, "r") as f:
#        pattern = re.compile('^([\w,-/\\\\+\(\):#%\$&;\'\*\s]+) ([^\n]+)\n$')
        for line in f:
            int_lines += 1
            #m = pattern.match(line)
            m = line.rsplit(' ', 1)
            if m[1]:
                test_data_dict[m[0]] = m[1].strip("\n")
            else:
#                print line
                print ("Error!")
                pass

    print (int_lines)


    #target = random.choice(test_data_dict.keys())
    #print ("Testing: %s - actual category %s: " % (target, test_data_dict[target]))

    test_cycle = 100000

    correct_answers = 0
    null_answers = 0
    incorrect_answers = 0

    test_list = []


    print ("Finding random keys")



    key_values = test_data_dict.keys()

    for _ in range(test_cycle):
        test_data = random.choice(key_values)
        test_list.append(test_data)

    test_list = key_values

    print (len(key_values))

    pool = Pool(processes=8)

    ck_list = split_list(test_list, 8)

    #    output = []
    #    output = get_substring_dict(check_substring_targets)


    #    for entry in ck_list:
    #        print len(entry)

    print ("Entering test data phase")

    strt = time.time()

    test_data = []
#    for _ in range(0, len(ck_list)):
#        key_array.append(substring_frequency_dict.keys())


    for entry in pool.map(calculate_string_probability_for_target, ck_list):
        test_data.extend(entry)



   # test_data = calculate_string_probability_for_target(test_list)

    fnsh = time.time()


    print ("Exiting test data phase")

    print (fnsh-strt)


    for (target, value) in test_data:
#        print (target,value,test_data_dict[target])
#        print value == test_data_dict[target]
        if value == test_data_dict[target]:
            correct_answers += 1
        elif value is not None:
            incorrect_answers += 1
        else:
            null_answers += 1

    print ("Correct: %d. Incorrect: %d. Insufficient data: %d" % (correct_answers, incorrect_answers, null_answers))



if __name__ == '__main__':
#    Learn_Engine.generate_list_strings()
    generate_substring_input()
#    calculate_string_probability_for_target(["GRM185D70J475ME11D"])
#    print calculate_string_probability_for_target("XC3S50AN-4TQG144I")
#    test_ai_against_data()






