'''                     HELPER FUNCTIONS                    '''

# Increments all elements in an integer array and returns the array and a bool indicating if the numbers are at max
def increment(indexes,maxindexes):
    max = True
    for i in range(len(indexes)):
        if indexes[i] == maxindexes[i]:
            indexes[i] = 0
        else:
            indexes[i] += 1
            break
    for i in indexes:
        if i != 0:
            max = False
    return indexes, max
