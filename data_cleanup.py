import os
import subprocess

def get_all_partnames_for_category(category, target_file="./res/train_uniq.txt"):
    input_data = []
    with file(target_file, 'r') as f:
        for line in f:
            if ' ' in line:
                m = line.rsplit(' ', 1)
                if m[1]:
                    part_name = m[0].strip()
                    part_category = m[1].strip()
                    if part_category == category:
                        input_data.append(part_name)

    with file("./meta/" + category + ".txt", 'w') as f:
        for entry in input_data:
            f.write(entry + "\n")

    return input_data


def open_private_txt(input_strings):
    with file("/home/wanderso/Downloads/digikey/data/private.txt", 'r') as f:
        stringbuf = f.read()

    string_list = stringbuf.split("\n")
    string_dict = {}
    category_list = ["DO204AL","DO204AC","DO15","DO41","DO204AH","DO204AR"]

    for line in string_list:
        line_list = line.split()
        for entry in input_strings:
            if entry in line_list:
                if "DO204AL" in line:
                    string_dict[entry] = "DO204AL"
                elif "DO204AC" in line:
                    string_dict[entry] = "DO204AC"
                else:
                    print line, line_list, entry

    return string_dict


DO204 = get_all_partnames_for_category("DO204")

print len(DO204)
print DO204[500:600]

al = 0
ac = 0

dict = open_private_txt(DO204)

print len(dict)
print dict

#for entry in DO204:
#    #subprocess.call(["grep", "-rnw", "'/home/wanderso/Downloads/digikey/data/private.txt'", "-e", DO204[0]])
#    teststr = subprocess.check_output(["/bin/grep","-rnw","/home/wanderso/Downloads/digikey/data/private.txt", "-e", entry.strip()])

#    if "DO204AL" in teststr:
#        print "AL"
#        al += 1
#    if "DO204AC" in teststr:
#        print "AC"
#        ac += 1

#print al, ac, al+ac