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
        self.replace_list = []
        self.base_likelihood = {}
        self.total_probability = 0

    def base_percentages_generate(self, package_names_file):
        self.synonyms = {}
        with file(package_names_file, "r") as f:
            for line in f:
                if '\t' in line:
                    m = line.rsplit('\t', 1)
                    target = m[0]
                    val = int(m[1])
                    self.base_likelihood[target] = val
                    self.total_probability += val
                else:
                    m = line.split(' ', 1)
                    if m[1]:
                        syn1 = m[0].strip()
                        syn2 = m[1].strip()

                        #relationship_introduced_1 = False
                        #relationship_introduced_2 = False


                        #for entry in self.synonyms:
                            #if syn1 in self.synonyms[entry]:
                                #self.synonyms[entry].append(syn2)
                                #relationship_introduced_1 = True
                                #for sub_entry in self.synonyms[entry]:
#                                    if sub_entry in self.synonyms:
 #                                       self.synonyms[sub_entry].append(syn1)
  #                          elif syn2 in self.synonyms[entry]:
  #                              self.synonyms[entry].append(syn1)
   #                             relationship_introduced_2 = True
   #                             for sub_entry in self.synonyms[entry]:
    #                                if sub_entry in self.synonyms:
     #                                   self.synonyms[sub_entry].append(syn1)

      #                  if not relationship_introduced_1:
        #                    self.synonyms[syn1] = [syn2]
       #                 if not relationship_introduced_2:
         #                   self.synonyms[syn2] = [syn1]
                        self.replace_list.append((syn1, syn2))

        for entry in self.replace_list:
            syn1 = entry[0]
            syn2 = entry[1]
 #           print (syn1, syn2)

            key_list_1 = []
            key_list_2 = []


            if syn1 not in self.synonyms:
                self.synonyms[syn1] = [syn2]
            else:
                for key in self.synonyms[syn1]:
                    self.synonyms[key].append(syn2)
#                    print "Recursiveappend: %s, %s, %s" % (key, syn1, syn2)
                    key_list_1.append(key)
                self.synonyms[syn1].append(syn2)
            if syn2 not in self.synonyms:
                self.synonyms[syn2] = [syn1]
            else:
                for key in self.synonyms[syn2]:
                    self.synonyms[key].append(syn1)
#                    print "Recursiveappend: %s, %s, %s" % (key, syn2, syn1)
                    key_list_2.append(key)
                self.synonyms[syn2].append(syn1)

            for entry in key_list_1:
                self.synonyms[syn2].append(entry)

            for entry in key_list_2:
                self.synonyms[syn1].append(entry)





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
        substrings.extend(get_random_substring(substring_length, num=100))

    total_len = len(substrings)

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

    substrings_no_repeats = []

    output_keys = outputs.keys()
    output_keys.sort()

    for entry in substrings:
        if entry not in output_keys and entry not in substrings_no_repeats:
            substrings_no_repeats.append(entry)

    print ("%d substrings not already learned" % len(substrings_no_repeats))

    substrings_split = []

    split_val = 1000

    if (len(substrings_no_repeats)) > split_val:
        for i in range(0, len(substrings_no_repeats), split_val):
            substrings_split.append(substrings_no_repeats[i:i + split_val])
    else:
        substrings_split = [substrings_no_repeats]

    pool = Pool(processes=8)

    # with terminating(Pool(processes=8)) as pool:
    #     output_array = []
    #     for _ in range(0,len(substrings)):
    #         output_array.append(outputs)
    #     for entry in pool.map(find_substring_occurrence,substrings,output_array):
    #         outputs = dict(outputs, **entry)

    #    with terminating(Pool(processes=8)) as pool:
#    key_array = []
#    for _ in range(0, len(substrings)):
#        key_array.append(outputs.keys())
#    for entry in pool.map(find_substring_occurrence, substrings, key_array):
#        outputs = dict(outputs, **entry)

#    with file(frequency_filename, "w") as f:
#        for key in outputs:
#            f.write(key + " " + str(outputs[key]) + "\n")

    #print substrings_split[0]

    start_substring_pool_time = time.time()

    print ("Starting frequency analysis")

    for target_list in substrings_split:




        ck_list = split_list(target_list, 8)

        new_frequency_dict = {}

        key_array = []
        for _ in range(0, len(ck_list)):
            key_array.append(outputs.keys())
        for entry in pool.map(find_substring_occurrence_nocheck, ck_list):
            new_frequency_dict = dict(new_frequency_dict, **entry)

        with file(frequency_filename, "a") as f:
            for key in new_frequency_dict:
                f.write(key + " " + str(new_frequency_dict[key]) + "\n")


    learn_finish_time = time.time()

    print ("%d substrings learned at %d in %d" % (len(new_frequency_dict), learn_finish_time, (learn_finish_time- start_substring_pool_time)))
    print ("Time elapsed - %d" % (learn_finish_time - strt_time))

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

    sorted_key_list = counts.keys()

    sorted_key_list.sort()

    total = 0

    sweet_spot = 0.6
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

    new_substring_targets = []
    for entry in check_substring_targets:
        if entry not in substring_frequency_dict:
            new_substring_targets.append(entry)


    new_substring_targets_split = []

    split_val = 1000

    if(len(new_substring_targets)) > split_val:
        for i in range (0,len(new_substring_targets), split_val):
            new_substring_targets_split.append(new_substring_targets[i:i+split_val])
    else:
        new_substring_targets_split = [new_substring_targets]



    for target_list in new_substring_targets_split:


        ck_list = split_list(target_list, 8)

        new_frequency_dict = {}

        key_array = []
        for _ in range(0, len(ck_list)):
            key_array.append(substring_frequency_dict.keys())
        for entry in pool.map(get_substring_dict, ck_list, key_array):
            new_frequency_dict = dict(new_frequency_dict, **entry)

        with file(substring_frequency_savename, "a") as f:
            for key in new_frequency_dict:
                f.write(key + " " + str(new_frequency_dict[key]) + "\n")



    #substring_frequency_dict = dict(substring_frequency_dict, **new_frequency_dict)

    substring_dict_time = time.time()
    #    print substring_frequency_dict

    print ("Learned %d substrings in - %d" % (len(new_frequency_dict), (substring_dict_time - learn_finish_time)))

    finish_time = time.time()
#    print ("Wrote %d substrings to disk in - %d" % (len(substring_frequency_dict), (finish_time - substring_dict_time)))

    print ("Total time - %d" % (finish_time - strt_time))


def compress_substring_files(synonyms=None, substring_length=5, replace_list=[]):
    # <9T06
    frequency_filename = "./runs/substring_len_" + str(substring_length) + "_frequency.txt"
    substring_dictionary_savename = "./runs/substring_len_" + str(substring_length) + "_dictionary.txt"

    substring_dictionary_lines = 0

    substring_dict = {}

    if os.path.isfile(substring_dictionary_savename):
        with file(substring_dictionary_savename, "r") as f:
            for line in f:
                if line:
                    substring_dictionary_lines += 1
                    a = line[:substring_length]
                    b = line[substring_length + 1:]
                    substring_dict[a] = ast.literal_eval(b)

    print("%d lines in %s - %d unique keys" %(substring_dictionary_lines,substring_dictionary_savename,len(substring_dict)))

    substring_frequency_lines = 0
    substring_frequency = {}

    if os.path.isfile(frequency_filename):
        with file(frequency_filename, "r") as f:
            for line in f:
                if line:
                    substring_frequency_lines += 1
                m = line.rsplit(' ', 1)
                if m[1]:
                    substring_frequency[m[0]] = int(m[1])

    print("%d lines in %s - %d unique keys" %(substring_frequency_lines,frequency_filename,len(substring_frequency)))

    synonym_replacer = {}

    synonyms_dirty = False

    for entry in replace_list:
        for key in substring_dict:
            if entry[0] in substring_dict[key]:
                value1 = substring_dict[key][entry[0]]
                value2 = 0
                if entry[1] in substring_dict[key]:
                    value2 = substring_dict[key][entry[0]]
                value2 += value1
                substring_dict[key][entry[1]] = value2
                substring_dict[key].pop(entry[0])
                synonyms_dirty = True




    if (substring_dictionary_lines != len(substring_dict)) or synonyms_dirty:
        print ("Writing dictionary to disk without repeats - DO NOT SHUT DOWN PROCESS")
        with file(substring_dictionary_savename, "w") as f:
            key_val = substring_dict.keys()
            key_val.sort()
            for key in key_val:
                f.write(key + " " + str(substring_dict[key]) + "\n")




    if substring_frequency_lines != len(substring_frequency):
        print ("Writing frequencies to disk without repeats - DO NOT SHUT DOWN PROCESS")
        with file(frequency_filename, "w") as f:
            key_val = substring_frequency.keys()
            key_val.sort()
            for key in key_val:
                f.write(key + " " + str(substring_frequency[key]) + "\n")

    print ("It is now safe to shut down the process")



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

  #      print category_possibilities
        output_list.append((string,category_possibilities))

    return output_list

class StringProbabilityDeep:
    def __init__(self,categories):
        self.category_possibilities = categories
        self.factor = None
        self.target = None
        self.runner_up = None



    def process_string_probability(self):
        top_num = 0.0
        second_num = 0.0
        top_num_category = None

        for entry in self.category_possibilities:
            if self.category_possibilities[entry] >= top_num:
                self.runner_up = self.target
                second_num = top_num
                top_num_category = entry
                self.target = entry
                top_num = self.category_possibilities[entry]
            elif self.category_possibilities[entry] >= second_num:
                second_num = self.category_possibilities[entry]


        if second_num:
            self.factor = top_num/second_num

        if top_num > (second_num * 2.5):
            return (top_num_category)

        else:
            return (None)

    def round_factor(self):
        if self.factor is not None:
            return round(self.factor, 1)
        return None


def test_ai_against_data(synonyms=None,substring_length=5):

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

    fnsh_testing = time.time()


    print ("Exiting test data phase after %d seconds" % (fnsh_testing-strt))

    incorrect_list = []
    null_list = []

    runner_up = 0.0
    best_guess = 0.0

    correct_avg = 0.0
    incorrect_avg = 0.0

    correct_factors = 0
    incorrect_factors = 0


    print (synonyms)

    for (target, value) in test_data:
        data = StringProbabilityDeep(value)
        new_val = data.process_string_probability()
        actual_category = test_data_dict[target]
        if new_val == actual_category:
            correct_answers += 1
            if data.factor:
                correct_avg += data.factor
                #print (data.factor)
                correct_factors += 1
        elif synonyms and actual_category in synonyms and new_val in synonyms[actual_category]:
            correct_answers += 1
            if data.factor:
                #print (data.factor)
                correct_avg += data.factor
                correct_factors += 1
        elif new_val is not None:
            incorrect_answers += 1
            incorrect_list.append((target, new_val, actual_category))
            if data.runner_up == actual_category:
                runner_up += 1
            if data.factor:
                incorrect_avg += data.factor
                incorrect_factors += 1

        else:
            null_answers += 1
            null_list.append((target, new_val, actual_category))
            if data.target == actual_category:
                best_guess += 1



    total_runs = float(len(test_data))

    fnsh = time.time()

    print ("Processed %d tests in %d seconds" % (len(test_data),fnsh-fnsh_testing))


    print ("Correct: %d. Incorrect: %d. Insufficient data: %d" % (correct_answers, incorrect_answers, null_answers))

    print ("Correct: %.2f%%. Incorrect: %.2f%%. Insufficient data: %.2f%%" % (100*correct_answers/total_runs, 100*incorrect_answers/total_runs, 100*null_answers/total_runs))

    print ("For incorrect data, runner-up accurate in: %.2f%%." % (100*runner_up/incorrect_answers))

    print ("For insufficient data, best guess accurate in: %.2f%%." % (100 * best_guess / null_answers))

    print ("Average factor for correct data: %f." % (correct_avg/correct_factors))

    print ("Average factor for incorrect data: %f." % (incorrect_avg/incorrect_factors))



    incorrect_filename = "./meta/incorrect_substring_len_" + str(substring_length) + ".txt"
    null_filename = "./meta/null_substring_len_" + str(substring_length) + ".txt"

    with file(incorrect_filename, "w") as f:
        for entry in incorrect_list:
            string = ""
            for value in entry:
                string = string + " " + str(value)
            string = string + "\n"
            f.write(string)

    with file(null_filename, "w") as f:
        for entry in null_list:
            string = ""
            for value in entry:
                string = string + " " + str(value)
            string = string + "\n"
            f.write(string)



def exhaust_substring_freq(substring_length=5):
    frequency_filename = "./runs/substring_len_" + str(substring_length) + "_frequency.txt"
    substring_dictionary_savename = "./runs/substring_len_" + str(substring_length) + "_dictionary.txt"

    substring_dict = {}

    if os.path.isfile(substring_dictionary_savename):
        with file(substring_dictionary_savename, "r") as f:
            for line in f:
                if line:
                    a = line[:substring_length]
                    b = line[substring_length + 1:]
                    substring_dict[a] = ast.literal_eval(b)

    print("Loaded substring dictionary - %d unique keys" % (len(substring_dict)))

    substring_frequency = {}

    if os.path.isfile(frequency_filename):
        with file(frequency_filename, "r") as f:
            for line in f:
                m = line.rsplit(' ', 1)
                if m[1]:
                    substring_frequency[m[0]] = int(m[1])

    print("Loaded substring frequency chart - %d unique keys" % (len(substring_frequency)))

    substring_dict_keys = substring_dict.keys()
    substring_frequency_keys = substring_frequency.keys()

    testdata = "./imp/learn_uniq.txt"

    test_data_list = []

    print ("Loading learn data...")

    int_lines = 0

    with file(testdata, "r") as f:
        for line in f:
            int_lines += 1
            m = line.rsplit(' ', 1)
            if m[1]:
                test_data_list.append(m[0])
            else:
                pass

    print ("Loaded %d lines of learn data" % int_lines)

    total_substrings = 0
    substrings_in_freq = 0
    substrings_in_dict = 0

    all_substring_dict = {}

    with file(testdata, "r") as f:
        for line in f:
            int_lines += 1
            m = line.rsplit(' ', 1)
            if m[1]:
                test_data_list.append(m[0])
            else:
                pass

    for string in test_data_list:
        string_anchored = "<" + string + ">"

        substrings_in_input = []

        for i in range(0, (len(string_anchored) - substring_length + 1), 1):
            substrings_in_input.append(string_anchored[i:i + 5])

        for entry in substrings_in_input:
            if entry in all_substring_dict:
                all_substring_dict[entry] += 1
            else:
                all_substring_dict[entry] = 1

    all_substrings = all_substring_dict.keys()

    learn_substring_dict = dict(all_substring_dict)

    print ("%d unique substrings of length %d in test data." % (len(all_substrings), substring_length))

    for entry in all_substrings:
        entry_num = all_substring_dict[entry]
        total_substrings += entry_num

    print ("%d substrings of length %d total." % (total_substrings, substring_length))

    print ("Calculating convergence...")

    for entry in substring_dict_keys:
        if entry in all_substring_dict:
            substrings_in_dict += all_substring_dict[entry]

    print ("%d substrings of length %d found in dictionary." % (substrings_in_dict, substring_length))

    for entry in substring_frequency_keys:
        if entry in all_substring_dict:
            substrings_in_freq += all_substring_dict[entry]
            learn_substring_dict.pop(entry)

    print ("%d substrings of length %d found in frequency chart." % (substrings_in_freq, substring_length))

    print ("Convergence calculated.")

    print ("Total: %d. In dict: %d. In freq: %d" % (total_substrings, substrings_in_dict, substrings_in_freq))
    print ("In dict: %.2f%%. In freq: %.2f%%." % (100 * float(substrings_in_dict) / float(total_substrings),
                                                  100 * float(substrings_in_freq) / float(total_substrings)))

    print ("Substrings to learn: %s" % len(learn_substring_dict))

    substrings_no_repeats = learn_substring_dict.keys()

    substrings_split = []

    split_val = 10000

    if (len(substrings_no_repeats)) > split_val:
        for i in range(0, len(substrings_no_repeats), split_val):
            substrings_split.append(substrings_no_repeats[i:i + split_val])
    else:
        substrings_split = [substrings_no_repeats]

    pool = Pool(processes=8)

    print ("Starting frequency analysis")

    iterations = 0

    for target_list in substrings_split:

        ck_list = split_list(target_list, 8)

        new_frequency_dict = {}

        for entry in pool.map(find_substring_occurrence_nocheck, ck_list):
            new_frequency_dict = dict(new_frequency_dict, **entry)

        with file(frequency_filename, "a") as f:
            for key in new_frequency_dict:
                f.write(key + " " + str(new_frequency_dict[key]) + "\n")

        iterations += 1



def find_substring_coverage(substring_length=5):

    frequency_filename = "./runs/substring_len_" + str(substring_length) + "_frequency.txt"
    substring_dictionary_savename = "./runs/substring_len_" + str(substring_length) + "_dictionary.txt"

    substring_dict = {}

    if os.path.isfile(substring_dictionary_savename):
        with file(substring_dictionary_savename, "r") as f:
            for line in f:
                if line:
                    a = line[:substring_length]
                    b = line[substring_length + 1:]
                    substring_dict[a] = ast.literal_eval(b)

    print("Loaded substring dictionary - %d unique keys" % (len(substring_dict)))

    substring_frequency = {}

    if os.path.isfile(frequency_filename):
        with file(frequency_filename, "r") as f:
            for line in f:
                m = line.rsplit(' ', 1)
                if m[1]:
                    substring_frequency[m[0]] = int(m[1])

    print("Loaded substring frequency chart - %d unique keys" % (len(substring_frequency)))

    substring_dict_keys = substring_dict.keys()
    substring_frequency_keys = substring_frequency.keys()

    testdata = "./imp/test_uniq.txt"

    test_data_list = []

    print ("Loading test data...")

    int_lines = 0

    with file(testdata, "r") as f:
        for line in f:
            int_lines += 1
            m = line.rsplit(' ', 1)
            if m[1]:
                test_data_list.append(m[0])
            else:
                pass

    print ("Loaded %d lines of test data" % int_lines)

    print ("Counting all substrings...")


    total_substrings = 0
    substrings_in_freq = 0
    substrings_in_dict = 0

    all_substring_dict = {}

    for string in test_data_list:
        string_anchored = "<" + string + ">"

        substrings_in_input = []

        for i in range(0, (len(string_anchored) - substring_length + 1), 1):
            substrings_in_input.append(string_anchored[i:i + 5])

        for entry in substrings_in_input:
            if entry in all_substring_dict:
                all_substring_dict[entry] += 1
            else:
                all_substring_dict[entry] = 1

    all_substrings = all_substring_dict.keys()

    print ("%d unique substrings of length %d in test data." %(len(all_substrings),substring_length))

    for entry in all_substrings:
        entry_num = all_substring_dict[entry]
        total_substrings += entry_num

    print ("%d substrings of length %d total." % (total_substrings,substring_length))

    print ("Calculating convergence...")

    for entry in substring_dict_keys:
        if entry in all_substring_dict:
            substrings_in_dict += all_substring_dict[entry]

    print ("%d substrings of length %d found in dictionary." % (substrings_in_dict,substring_length))

    for entry in substring_frequency_keys:
        if entry in all_substring_dict:
            substrings_in_freq += all_substring_dict[entry]

    print ("%d substrings of length %d found in frequency chart." % (substrings_in_freq,substring_length))


    print ("Convergence calculated.")

    print ("Total: %d. In dict: %d. In freq: %d" % (total_substrings, substrings_in_dict, substrings_in_freq))
    print ("In dict: %.2f%%. In freq: %.2f%%." % (100*float(substrings_in_dict)/float(total_substrings), 100*float(substrings_in_freq)/float(total_substrings)))





if __name__ == '__main__':
    learn = Base_Implementation()
    learn.base_percentages_generate("./imp/package_no_comments.txt")
#    print learn.replace_list

    print learn.synonyms
#     generate_substring_input()
#    calculate_string_probability_for_target(["GRM185D70J475ME11D"])
#    print calculate_string_probability_for_target("XC3S50AN-4TQG144I")
    test_ai_against_data(synonyms=learn.synonyms)

    #MCUR> {'VQFN': 3}

#    compress_substring_files(synonyms=learn.synonyms,replace_list=learn.replace_list)
    #find_substring_coverage()
    #exhaust_substring_freq()



# Correct: 88299. Incorrect: 3989. Insufficient data: 2077
# Correct: 93.57%. Incorrect: 4.23%. Insufficient data: 2.20%


