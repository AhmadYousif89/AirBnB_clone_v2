#!/usr/bin/python3
"""A small program"""


def format_params(input):
    """function to format parameters"""
    split_input = input.split(' ')
    kwargs_dict = {}

    for item in split_input:
        if '=' in item:
            key, val = item.split('=')
            if '"' in val:
                val = val.replace('_', ' ')
                val = val[1:-1]
            kwargs_dict[key] = val

    kwargs_dict['__class__'] = split_input[0]

    return(kwargs_dict)


if __name__ == "__main__":
    # Test input
    input = "User name=\"Andy_Stone\" age=32 height=5.7"
    test = format_params(input)
    print(test[1])
