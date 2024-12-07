import argparse

def read(filename:str) -> list[list[str]]:
    with open(filename, mode='r') as f:
        word_search = [[char for char in line.strip()] for line in f.readlines()]
    return word_search

def find_string_occurances_in_all_directions(search_string:str, matrix:list[list[str]]) -> int:
    starting_symbol = search_string[0]
    ending_symbol = search_string[-1]
    string_len = len(search_string)
    string_ctr = 0
    
    for row_idx, row in enumerate(matrix):
        for col_idx, curr_char in enumerate(row):
            if (curr_char == starting_symbol) or (curr_char == ending_symbol):
                curr_search_string = None
                if curr_char == starting_symbol: curr_search_string = search_string
                elif curr_char == ending_symbol: curr_search_string = search_string[::-1]

                # Search next n-1 symols to the right
                if len(row) >= col_idx + string_len:
                    temp_string = ''
                    for idx in range(string_len):
                        temp_string += row[col_idx+idx]
                    if temp_string == curr_search_string:
                        string_ctr += 1

                # Search n-1 symols down
                if len(matrix) >= row_idx + string_len:
                    temp_string = ''
                    for idx in range(string_len):
                        temp_string += matrix[row_idx+idx][col_idx]
                    if temp_string == curr_search_string:
                        string_ctr += 1
                
                # Search n-1 symbols down-left
                if len(matrix) >= row_idx + string_len and col_idx >= string_len - 1:
                    temp_string = ''
                    for idx in range(string_len):
                        temp_string += matrix[row_idx+idx][col_idx-idx]
                    if temp_string == curr_search_string:
                        string_ctr += 1
                
                # Search n-1 symbols down-right
                if len(matrix) >= row_idx + string_len and len(row) >= col_idx + string_len:
                    temp_string = ''
                    for idx in range(string_len):
                        temp_string += matrix[row_idx+idx][col_idx+idx]
                    if temp_string == curr_search_string:
                        string_ctr += 1

    return string_ctr


def find_crossing_string_occurances(search_string:str, matrix:list[list[str]]) -> int:
    if len(search_string)%2 == 0: raise Exception("String has to be of odd length to form a cross")

    string_len = len(search_string)
    inverse_string = search_string[::-1]
    middle_idx = int((len(search_string))/2)
    intersection_symbol = search_string[middle_idx]
    string_ctr = 0

    for row_idx, row in enumerate(matrix):
        for col_idx, curr_char in enumerate(row):
            if curr_char == intersection_symbol:
                if ( 
                    len(row) > col_idx + middle_idx and       # check for space to the right
                    col_idx >= middle_idx and              # check for space to the left
                    len(matrix) > row_idx + middle_idx and    # check for space down
                    row_idx >= middle_idx                 # check for space up
                ):
                    forwards_string = ''
                    backwards_string = ''
                    forwards_start_col = col_idx - middle_idx
                    backwards_start_col = col_idx + middle_idx
                    start_row = row_idx - middle_idx

                    for idx in range(string_len):
                        forwards_string += matrix[start_row+idx][forwards_start_col+idx]
                        backwards_string += matrix[start_row+idx][backwards_start_col-idx]
                    
                    if ((forwards_string == search_string or forwards_string == inverse_string) 
                        and (backwards_string == inverse_string or backwards_string == search_string)):
                        string_ctr += 1

    return string_ctr


if __name__  == '__main__':
    file_name = 'input4.txt'
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="turns testing mode on", action="store_true")
    args = parser.parse_args()
    if args.test:
        input_name = f'test_inputs/{file_name}'
    else:
        input_name = f'inputs/{file_name}'

    word_search = read(input_name)

    xmas_count = find_string_occurances_in_all_directions("XMAS", word_search)
    print("Part 1 answer:", xmas_count)
    
    cross_mas_count = find_crossing_string_occurances("MAS", word_search)
    print("Part 2 answer:", cross_mas_count)