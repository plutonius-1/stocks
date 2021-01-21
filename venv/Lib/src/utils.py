
def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    # print (matrix)
    return (matrix[size_x - 1, size_y - 1])

def add_data_to_statement(key : str,
                          d : dict,
                          data_to_write : dict):
    if (key in d.keys()):
        temp   = d[key]
        temp.update(data_to_write)
        d[key] = temp
        return d
    else:
        for kid in d.keys():
            if (type(d[kid]) == dict):
                d[kid] = add_data_to_statement(key, d[kid], data_to_write)
                # return d
        return d


def print_nested_dict(d : dict):
    if (len(d) == 1):
        print(d)
        return

    for i in d.keys():
        if (type(d[i]) == dict):
            print_nested_dict(d[i])

