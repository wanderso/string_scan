import test_data_producer
import openpyxl

def parse_file(filename):
    wb = openpyxl.load_workbook(filename)
    sheet_ranges = wb.active
    print(sheet_ranges['D1'].value)
    cursor_row = 2
    cursor = 'D2'

    part_list = []
    while sheet_ranges[cursor].value is not None:
        part_name = sheet_ranges[cursor].value
        part_list.append(part_name)
        cursor_row += 1
        cursor = 'D' + str(cursor_row)

    data_list = test_data_producer.calculate_string_probability_for_target(part_list)

    for entry in data_list:
        if entry[0] == u'DNP':
            continue
        SP = test_data_producer.StringProbabilityDeep(entry[1])
        print(entry[0], SP.process_string_probability())

if __name__ == '__main__':
    parse_file("./bom/bom1.xlsx")
