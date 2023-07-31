def sort_list(list_to_sort: list, key: str = 'score') -> list:
    """
    Sorts a list of dictionaries by the given key
    :param list_to_sort: list of dictionaries
    :param key: key to sort by (default is 'score')
    :return: sorted list
    """

    # sorts the list of dictionaries by the given key
    sorted_list = sorted(list_to_sort, key=lambda k: k[key], reverse=True)

    # set 'rank' to the index number
    for i, candidate in enumerate(sorted_list, start=1):
        candidate['rank'] = i

    return sorted_list
