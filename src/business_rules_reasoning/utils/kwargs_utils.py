def merge_kwargs(kwargs1: dict, kwargs2: dict) -> dict:
    """
    Merges two dictionaries of keyword arguments, with `kwargs2` taking precedence.

    Args:
        kwargs1 (dict): The first dictionary of keyword arguments.
        kwargs2 (dict): The second dictionary of keyword arguments.

    Returns:
        dict: A merged dictionary of keyword arguments.
    """
    merged_kwargs = kwargs2.copy()
    merged_kwargs.update(kwargs1)
    return merged_kwargs
