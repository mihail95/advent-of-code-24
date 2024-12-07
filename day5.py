import argparse

def read(filename:str) -> tuple[dict, dict, list[list[int]]]:
    with open(filename, mode='r') as f:
        instructions_list = []
        pages = []
        curr_list = instructions_list
        for line in f:
            if line == "\n":
                curr_list = pages
                continue
            curr_list.append(line.strip())

        pages = [[int(item) for item in line.split(',')] for line in pages]
        instructions_dict = {}
        for instruction in instructions_list:
            instr_split = instruction.split('|')
            instructions_dict.setdefault(int(instr_split[0]), []).append(int(instr_split[1]))
        
    reverse_instructions = {}
    for key,value in instructions_dict.items():
        for n in value:
            reverse_instructions.setdefault(n, []).append(key)

    return (instructions_dict, reverse_instructions, pages)


def get_pages_lists_checksum(instructions:dict, reverse_instructions:dict, page_lists:list[list[int]]) -> tuple[int, list]:
    correct_lists = []
    incorrect_lists = []
    for page_list in page_lists:
        check_list = [False for _ in range(len(page_list))]
        for idx, page in enumerate(page_list):
            if idx == len(page_list)-1:
                elements_before = page_list[:idx]
                if all([x in reverse_instructions[page] for x in elements_before]):
                    check_list[idx] = True
            else:
                if page in instructions:
                    elements_after = page_list[idx+1:]
                    if all([x in instructions[page] for x in elements_after]):
                        check_list[idx] = True
                else:
                    elements_before = page_list[:idx]
                    if all([x in reverse_instructions[page] for x in elements_before]):
                        check_list[idx] = True

        if all(check_list): correct_lists.append(page_list)
        else: incorrect_lists.append(page_list)

    middle_elements = []
    for curr_list in correct_lists:
        mid_idx = int((len(curr_list))/2)
        middle_elements.append(curr_list[mid_idx])

    return sum(middle_elements), incorrect_lists


def sort_incorrect_lists(instructions:dict, reverse_instructions:dict, page_lists:list[list[int]]) -> int:
    sorted_lists = []
    for page_list in page_lists:
        ordered_page = []
        for element in page_list:
            inserted = False
            for idx, ordered_element in enumerate(ordered_page):
                if ordered_element in instructions.get(element, []):
                    ordered_page.insert(idx, element)
                    inserted = True
                    break
            if not inserted:
                ordered_page.append(element)
        sorted_lists.append(ordered_page)


    middle_elements = []
    for curr_list in sorted_lists:
        mid_idx = int((len(curr_list))/2)
        middle_elements.append(curr_list[mid_idx])

    return sum(middle_elements)


if __name__  == '__main__':
    file_name = 'input5.txt'
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="turns testing mode on", action="store_true")
    args = parser.parse_args()
    if args.test:
        input_name = f'test_inputs/{file_name}'
    else:
        input_name = f'inputs/{file_name}'

    instructions, reverse_instructions, pages = read(input_name)

    checksum, incorrect_lists = get_pages_lists_checksum(instructions, reverse_instructions, pages)
    print("Part 1 Checksum:", checksum)

    checksum2 = sort_incorrect_lists(instructions, reverse_instructions, incorrect_lists)
    print("Part 2 Checksum:", checksum2)
