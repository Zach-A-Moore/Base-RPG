
# This is the backbone for most the code. A lot of Classes and functions rely on
# this code to work. If you plan to repeatedly use a function, put it here

def yesno (value : str) -> int :
    """ This function takes a string and checks if it is a yes or no answer.
    If it is a yes answer, it returns 1. If it is a no answer, it returns 0.
    a 2 represents an error."""
    if (not isinstance(value, str)):
        return 2
    elif (value == ""):
        return 2
    elif (value.upper()[0] == "Y"):
        return 1
    elif (value.upper()[0] == "N"):
        return 0
    else:
        return 2
    
def yesno_loop (input_1 : str, line : str = "Y/N") -> int :
    """ using the yes no function, this is a separate but similar
    function that will loop until it returns a value of 1 or 0"""
    val = 1
    while val:
        if yesno(input_1) == 1:
            return 1
        if yesno(input_1) == 0:
            return 0
        if yesno(input_1) == 2:
            print(f"input {input_1} could not be read as Y/N \n")
            input_1 = input(f"{line} ")

def choice_num (input : str, max : int) -> int:
    """ This function tests an input, mainly for menu selection. It will check
    if the given number is >= a max and will return it. 404 is returned if the input
    is not a number or if it is out of range. """
    if (isinstance(input, str) and input.isdigit() == True and isinstance(max, int)):
        input = int(input)
        if ((input > 0) and (input <= max)):
            return input
        else:
            return 404
    else:
        return 404

def choice_num_loop (choices : dict, input_1 : str) -> int:
    """This function loops choice num until a matching input is found."""
    max = len(choices)
    while True:
        choice = choice_num(input_1, max)
        if choice != 404:
            return choice
        else:
            temp_num = choices.values()
            temp_list = []
            for nums in temp_num:
                temp_list.append(nums)
            print(f"the input {input_1} could not be read as {temp_list}")
            input_1 = input(f"please enter one of the values entered above :")
            continue

def menu_handler (choices : object) -> int:
    """Given a list of choices, this function will print the choices and ask for a selection.
    until a valid selection is made. It will return the selected choice."""
    print(choices)
    temp_input = input("What would you like to choose? ")
    temp_input = choice_num_loop(choices.compile_scene(), temp_input)
    return choices.choices[temp_input - 1]

def print_choice (choices : dict[str : int]) -> None:
    """Prints dictionaries in a menu format.
    1.) choice 1
    2.) choice 2
    3.) choice 3
    """

    for key, value in choices.items():
        print(f"{value}.) {key}")

def main():
    ## checks yesno and yesno loop
    assert yesno("") == 2
    assert yesno(4) == 2
    assert yesno("bob") == 2
    assert yesno(" ") == 2
    assert yesno("y") == 1
    assert yesno("n") == 0
    temp = yesno_loop("maybe", "Y/N") == 1
    assert temp == 1 or temp == 0

    ## checks choicenum and choicenum_loop
    assert choice_num(5, "5") == 404
    assert choice_num("5", 5) == 5
    assert choice_num("5", "5") == 404
    assert choice_num("10", 5) == 404
    assert choice_num("10", 100) == 10
    assert choice_num("-5", 10) == 404
    temp_dict = {"up" : 1, "right" : 2, "left" : 3, "down" : 4}
    print_choice(temp_dict)
    choice_num_loop(temp_dict, "num")




    print(" all test pass")

if __name__ == "__main__":
    main()