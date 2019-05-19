def binary_search(arr, key):
    """Binary search of element in list

    Parameters
    ----------
    arr : list
        The list where we want to find the element
    key : dtype of list's elements
        The element to find

    Returns
    -------
    ans
        The index of the element in the list
    """
    index = int(len(arr) / 2)
    pivot = arr[index]
    if (key == pivot):
        ans = index
    elif (key < pivot):
        ans = binary_search(arr[0:index], key)
    elif (key > pivot):
        ans = binary_search(arr[index+1:len(arr)], key) + index + 1
    
    return ans
