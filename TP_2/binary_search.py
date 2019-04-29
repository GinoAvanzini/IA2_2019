def binary_search(arr, key):
    index = int(len(arr) / 2)
    pivot = arr[index]
    if (key == pivot):
        ans = index
    elif (key < pivot):
        ans = binary_search(arr[0:index], key)
    elif (key > pivot):
        ans = binary_search(arr[index+1:len(arr)], key) + index + 1
    
    return ans
