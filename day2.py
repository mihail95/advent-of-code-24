def read(filename:str) -> list[list[int]]:
    list1 = []
    with open(f'inputs/{filename}', mode='r') as f:
        for line in f:
            curr_line = line.strip().split()
            temp_list = [ int(item) for item in curr_line ]
            list1.append(temp_list)
    return list1

def checkRowSafe(row:list[int]) -> bool:
    direction = None
    prev_level = None
    is_safe = True
    for level in row:
        if prev_level == None:
            prev_level = level
            diff = row[0] - row[1]
            if diff < 0:
                direction = "increasing"
            elif diff > 0:
                direction = "decreasing"
            else: 
                is_safe = False
                break
            continue

        diff = level - prev_level
        prev_level = level

        if abs(diff) > 3:
            is_safe = False
            break            
        if diff > 0:
            if direction == "decreasing":
                is_safe = False
                break
        elif diff < 0:
            if direction == "increasing":
                is_safe = False
                break
        else: 
            is_safe = False
            break
    
    return is_safe

def countSafeRows(inputs:list[list[int]]) -> int:
    safe_count = 0
    for row in inputs:
        is_safe = checkRowSafe(row)
        safe_count += is_safe
  
    return safe_count

def countSafeRowsWithDampener(inputs:list[list[int]]) -> int:
    safe_count = 0
    for row in inputs:
        row_safe_ctr = 0
        if checkRowSafe(row) == True:
            safe_count += 1
            continue
        for idx in range(len(row)):
            temp_row = row[:]
            temp_row.pop(idx)
            row_safe_ctr += checkRowSafe(temp_row)
            print(f"Safe count for {row}, temp_row {temp_row}: {row_safe_ctr}")

        is_safe = True if row_safe_ctr > 0 else False
        safe_count += is_safe
  
    return safe_count


if __name__  == '__main__':
    input_name = 'input2.txt'
    input_list = read(input_name)
    safe_count = countSafeRows(input_list)
    print(f"safe rows: {safe_count}")
    damp_safe_count = countSafeRowsWithDampener(input_list)
    print(f"safe rows with dampener: {damp_safe_count}")