import tensorflow as tf
import numpy as np
import os


class TensorFlowReadStrings:
    def __init__(self, package_name="./imp/package_no_comments.txt"):
        self.package_name = package_name
        self.package_list = []
        self.package_dict = {}
        self.package_location_dict = {}
        self.synonym_list = []
        self.input_data = []

        with file(self.package_name,'r') as f:
            categories = 0
            for line in f:
                if '\t' in line:
                    m = line.rsplit('\t', 1)
                    if m[1]:
                        key = m[0].strip()
                        value = m[1].strip()
                        self.package_list.append(key)
                        self.package_dict[key] = int(value)
                        self.package_location_dict[key] = categories
                        categories += 1
                elif ' ' in line:
                    m = line.rsplit(' ', 1)
                    if m[1]:
                        syn1 = m[0].strip()
                        syn2 = m[1].strip()
                        self.synonym_list.append((syn1,syn2))

    def read_training_data(self, training_file="./imp/learn_uniq.txt"):
        self.input_data = []
        with file(training_file, 'r') as f:
            for line in f:
                if ' ' in line:
                    m = line.rsplit(' ', 1)
                    if m[1]:
                        part_name = m[0].strip()
                        part_category = m[1].strip()
                        if part_category not in self.package_location_dict:
                            print part_category
                        self.input_data.append((part_name,part_category))


if __name__ == '__main__':
    tfrs = TensorFlowReadStrings()
    tfrs.read_training_data()
