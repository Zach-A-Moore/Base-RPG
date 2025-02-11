from RPG_3_class import Scene


def yesno (value : str) -> int :
    """ This Function takes an Input from the user as a value, checks if it's a non blank string, and if it is, it will check if the 
    first letter input is a y or n. If the input could not be read as a y or n, then the program will return a 2. Y will return a 1, and a n will return a 0"""
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
    """ This function takes a input and a maximum, if the input is both a positive integer and lesser then or equal
    to the max then this return input as an int, otherwise a 404 error will be returned"""
    if (isinstance(input, str) and input.isdigit() == True and isinstance(max, int)):
        input = int(input)
        if ((input > 0) and (input <= max)):
            return input
        else:
            return 404
    else:
        return 404

def choice_num_loop (choices : dict, input_1 : str) -> int:
    max = len(choices)
    run = 0
    while run == 0:
        choice = choice_num(input_1, max)
        if choice != 404:
            run = 1
            return choice
        else:
            temp_num = choices.values()
            temp_list = []
            for nums in temp_num:
                temp_list.append(nums)
            print(f"the input {input_1} could not be read as {temp_list}")
            input_1 = input(f"please enter one of the values entered above :")
            continue

def print_choice (choices : dict[str : int]) -> None:
    """Prints dictionaries"""
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

def main():
    print(choice_num("3", 4))
    choice_num_loop({"Exit" : 1}, "3")


if __name__ == "__main__":
    main()