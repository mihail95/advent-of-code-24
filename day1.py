def read(filename:str) -> tuple[list[int], list[int]]:
    list1 = []
    list2 = []
    with open(f'inputs/{filename}', mode='r') as f:
        for line in f:
            curr_line = line.strip().split()
            list1.append(int(curr_line[0]))
            list2.append(int(curr_line[1]))

    return (list1, list2)


def calculateDistanceBetween(list1: list, list2:list) -> int:
    distance = 0

    # Sort both lists
    list1.sort()
    list2.sort()
    if len(list1) != len(list2):
        raise Exception("Lists have different lenghts!")
    
    # For each pair, calculate distance
    for idx, left in enumerate(list1):
        right = list2[idx]
        current_distance = abs(left - right)
        distance += current_distance

    return distance


def calculateSimilarityScore(list1: list, list2:list) -> int:
    similarity = 0
    for member in list1:
        occurances = list2.count(member)
        similarity += member*occurances

    return similarity


if __name__  == '__main__':
    input_name = 'input1.txt'
    list1, list2 = read(input_name)
    distance = calculateDistanceBetween(list1, list2)
    print("distance: ", distance)
    similarity = calculateSimilarityScore(list1, list2)
    print("similarity: ", similarity)