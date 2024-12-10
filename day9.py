import argparse
import operator

def read(filename:str) -> list[int]:
    data = []
    with open(filename, mode='r') as f:
        for line in f:
            for num in line:
                data.append(int(num))
    return data

def print_expanded_memory(expanded_disk_ctr:int, files_indeces:dict) -> None:
    for idx in range(expanded_disk_ctr):
        print(files_indeces.get(idx, '.'), end='', sep='')
    print()

def print_expanded_memory_by_sizes(expanded_disk_ctr:int, file_sizes:dict, empty_sizes:dict) -> None:
    print(expanded_disk_ctr)
    print(file_sizes)
    print(empty_sizes)
    for idx in range(expanded_disk_ctr):
        if idx in file_sizes:
            print(str(file_sizes[idx][1])*file_sizes[idx][0], end='', sep='')
        elif idx in empty_sizes:
            print('.'*empty_sizes[idx][0], end='', sep='')
    print()

def get_defragment_checksum(disk_contents:list) -> int:
    files_indeces = {}
    empty_indeces = set()
    expanded_disk_ctr = 0
    file_ctr = 0
    for idx, value in enumerate(disk_contents):
        if idx % 2 == 0: # If file
            file_ctr += 1
            for ctr in range(value):
                files_indeces[expanded_disk_ctr] = idx%2+idx//2
                expanded_disk_ctr += 1
        else: # If empty space
            for ctr in range(value):
                empty_indeces.add(expanded_disk_ctr)
                expanded_disk_ctr += 1

    defragged_memory = {}

    for exp_idx in range(expanded_disk_ctr):
        if files_indeces.get(exp_idx, None) is not None: # Don't move existing files
            defragged_memory[exp_idx] = files_indeces.get(exp_idx)
            files_indeces.pop(exp_idx)
        elif exp_idx in empty_indeces and len(files_indeces) > 0: # Fill empty spaces with the max available file
            last_file = max(files_indeces.items()) # tuple(orig_idx: file_id)
            files_indeces.pop(last_file[0])
            defragged_memory[exp_idx] = last_file[1]

    return sum([key*value for key, value in defragged_memory.items()])

def get_whole_file_defragment_checksum(disk_contents:list) -> int:
    files_size_indeces = {}
    empty_size_indeces = {}
    expanded_disk_ctr = 0
    file_ctr = 0
    for idx, value in enumerate(disk_contents):
        if idx % 2 == 0: # If file
            file_ctr += 1
            files_size_indeces[expanded_disk_ctr] = (value, idx%2+idx//2) # expanded_index: size, file_id 
        else: # If empty space
            empty_size_indeces[expanded_disk_ctr] = (value, idx%2+idx//2)
        expanded_disk_ctr += value

    #print_expanded_memory_by_sizes(expanded_disk_ctr, files_size_indeces, empty_size_indeces)
    defragged_memory = {}
    for exp_idx in range(expanded_disk_ctr):
        if files_size_indeces.get(exp_idx, None) is not None: # Don't move existing files
            for subidx in range(files_size_indeces[exp_idx][0]):
                defragged_memory[exp_idx+subidx] = files_size_indeces[exp_idx][1]
            files_size_indeces.pop(exp_idx)
        elif exp_idx in empty_size_indeces and len(files_size_indeces) > 0: # Fill empty spaces with the max available file
            space_size = empty_size_indeces[exp_idx][0]
            files_of_size = dict(filter(lambda x: x[1][0] <= space_size, files_size_indeces.items()))
            if len(files_of_size) > 0:
                last_file = max(files_of_size.items()) 
                for subidx in range(last_file[1][0]):
                    defragged_memory[exp_idx+subidx] = last_file[1][1]
                files_size_indeces.pop(last_file[0])
                if last_file[1][0] < space_size:
                    empty_size_indeces[exp_idx+last_file[1][0]] = (space_size-last_file[1][0], 999)

    return sum([key*value for key, value in defragged_memory.items()])


if __name__  == '__main__':
    file_name = 'input9.txt'
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="turns testing mode on", action="store_true")
    args = parser.parse_args()
    if args.test:
        input_name = f'test_inputs/{file_name}'
    else:
        input_name = f'inputs/{file_name}'

    disk_contents = read(input_name)

    checksum = get_defragment_checksum(disk_contents)
    print("Part 1: Checksum:", checksum)

    checksum = get_whole_file_defragment_checksum(disk_contents) # Amusingly, this is waaaaaaay faster than Part 1
    print("Part 2: Checksum:", checksum)
