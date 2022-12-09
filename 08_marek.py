import numpy as np



def visible_trees(l: list) -> int:
    """
 # read the input into a list
file = open("Day-8/input.txt", "r")
L = file.read().splitlines()

   Finds how many trees are visible = have only shorter trees prior in their col or row from some side.
    """

    # parse input
    input = []
    input_row = []
    for i in l:
        for j in i:
            input_row.append(int(j))
        input.append(input_row)
        input_row = []

    input_array = np.array(input)
    input_array_shape = input_array.shape

    # visibility from left
    visible_from_left = np.zeros(input_array_shape)
    for i in range(input_array_shape[0]):
        threshold = -1
        for j in range(input_array_shape[1]):
            if input_array[i, j] > threshold:
                visible_from_left[i, j] = 1
                threshold = input_array[i, j]

    # visibility from right
    visible_from_right = np.zeros(input_array_shape)
    for i in range(input_array_shape[0]):
        threshold = -1
        for j in range(input_array_shape[1] - 1, -1, -1):
            if input_array[i, j] > threshold:
                visible_from_right[i, j] = 1
                threshold = input_array[i, j]

    # visibility from top
    visible_from_top = np.zeros(input_array_shape)
    for j in range(input_array_shape[1]):
        threshold = -1
        for i in range(input_array_shape[0]):
            if input_array[i, j] > threshold:
                visible_from_top[i, j] = 1
                threshold = input_array[i, j]

    # visibility from bot
    visible_from_bot = np.zeros(input_array_shape)
    for j in range(input_array_shape[1]):
        threshold = -1
        for i in range(input_array_shape[0] - 1, -1, -1):
            if input_array[i, j] > threshold:
                visible_from_bot[i, j] = 1
                threshold = input_array[i, j]

    # put together
    result = (
        (visible_from_left + visible_from_right + visible_from_top + visible_from_bot)
        > 0
    ).sum()

    return result


def highest_scenic_score(l: list) -> int:
    """
    For each tree find how many trees are visible from all four direction and multiply. Return the highest score from the whole input.
    """

    # parse input
    input = []
    input_row = []
    for i in l:
        for j in i:
            input_row.append(int(j))
        input.append(input_row)
        input_row = []

    input_array = np.array(input)
    input_array_shape = input_array.shape

    # scenic score from left
    ss_from_left = np.zeros(input_array_shape)
    for i in range(input_array_shape[0]):
        for j in range(input_array_shape[1]):
            k = j
            while k > 0:
                ss_from_left[i, j] += 1
                k -= 1
                if input_array[i, k] >= input_array[i, j]:
                    k = 0

    # scenic score from right
    ss_from_right = np.zeros(input_array_shape)
    for i in range(input_array_shape[0]):
        for j in range(input_array_shape[1] - 1, -1, -1):
            k = j
            while k < input_array_shape[1] - 1:
                ss_from_right[i, j] += 1
                k += 1
                if input_array[i, k] >= input_array[i, j]:
                    k = input_array_shape[1] - 1

    # scenic score from top
    ss_from_top = np.zeros(input_array_shape)
    for j in range(input_array_shape[1]):
        for i in range(input_array_shape[0]):
            k = i
            while k > 0:
                ss_from_top[i, j] += 1
                k -= 1
                if input_array[k, j] >= input_array[i, j]:
                    k = 0

    # scenic score from bot
    ss_from_bot = np.zeros(input_array_shape)
    for j in range(input_array_shape[1]):
        for i in range(input_array_shape[0] - 1, -1, -1):
            k = i
            while k < input_array_shape[0] - 1:
                ss_from_bot[i, j] += 1
                k += 1
                if input_array[k, j] >= input_array[i, j]:
                    k = input_array_shape[0] - 1

    # # put together
    result = int(np.max(ss_from_left * ss_from_right * ss_from_top * ss_from_bot))

    return result


if __name__ == "__main__":
    # read the input into a list
    file = open("Day-8/input.txt", "r")
    L = file.read().splitlines()

    print(highest_scenic_score(L))
