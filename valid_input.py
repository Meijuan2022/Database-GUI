# This file will determine if the information input is valid
# Name must be characters and postnumber and fee must be numbers
#_______________________________________#

def validate(values_list):
    isvalid = True
    values_invalid = []
    if len(values_list[0]) == 0 or not values_list[0].isalpha():
        values_invalid.append('Firstname')
        isvalid = False

    if len(values_list[1]) == 0 or not values_list[1].isalpha():
        values_invalid.append('Eftername')
        isvalid = False

    if not values_list[3].isdigit():
        values_invalid.append('Postnumber')
        isvalid = False

    if not values_list[5].isdigit():
        values_invalid.append('Annual fee')
        isvalid = False

    result = [isvalid,values_invalid]
    return result