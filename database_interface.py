
# This file have all the function to realize the interaction between the database and the users
#_________________________________________#

import PySimpleGUI as sg
import create_databse
import copy
import valid_input

session = create_databse.session
Medlemmar = create_databse.Medlemmar
or_= create_databse.or_

record_field = ['Firstname', 'Eftername','Street Address','Post Number','Post Address','Annual Fee']
record_key =['_FN_','_EN_','_GA_','_PN_','_PA_','_F_']

# Add new member interface
def add_record():
    insert_list =[]
    #is_valued = []
    layout = [

        [[sg.T(record_field[i],font='_15'), sg.Push(), sg.I(key=record_key[i],font='_15')] for i in range(6)],
        [sg.B('OK',key='_OK_',font='_15',size=8),sg.B('Reset',key='_RE_',font='_15',size=8),sg.B('Quit',key='_CAN_',font='_15',size=8)]

    ]
    add_record_window = sg.Window('Add a new member',layout,modal=True,keep_on_top=True)
    while True:
        event, values = add_record_window.read()
        if event in (sg.WINDOW_CLOSED,'Exit','_CAN_'):
            break
        if event =='_OK_':
            is_valued = []
            insert_list = []
            for i in record_key:
                insert_list.append(values[i])
            for i in (3,5):
                if insert_list[i] =='':
                    insert_list[i] = '0'
            is_valued = valid_input.validate(insert_list)
            if is_valued[0]:
                InsertDb(insert_list)
                sg.popup('The new member has been added!',keep_on_top=True,title='Done',font='_15')
            else:
                sg.popup_error(generate_error_message(is_valued[1]),keep_on_top=True,font='_15',title='Error!')

        if event =='_RE_':
            for i in record_key:
                add_record_window[i].Update('')

    add_record_window.close()


#Delete interface
def del_record(medindex:int,medname:str):
    layout= [
             [sg.T(f'Are your sure to delete member No.{medindex}:{medname}',font='_15')],
             [sg.B('Yes',key='_YESDEL_',font='_15',size=8),sg.B('Cancel',key='_CAN_DEL_',font='_15',size=8)]

    ]
    del_record_window = sg.Window('Delete the member?',layout,modal=True,keep_on_top=True)
    #del_record_window.make_modal()
    while True:
        event,values = del_record_window.read()
        if event in (sg.WINDOW_CLOSED,'Exit','_CAN_DEL_'):
            result = False
            break
        if event=='_YESDEL_':
            DeleteDb(medindex)
            sg.popup('Deleted Successfully!',font='_15',title='Done')
            result = True
            break

    del_record_window.close()
    return  result

#Update interface
def update_record(record_list:list):
    #return_list =copy.copy(record_list)
    mn = int(record_list[0])
    layout = [
        [sg.T(f'Update Nr.{mn} information',font='_15')],
        [[sg.T(record_field[i],font='_15'),sg.Push(),sg.I(record_list[i+1],key=record_key[i],font='_15')]for i in range(6)],
         [sg.B('OK', key='_MOD_OK_',font='_15',size=8), sg.B('Cancel', key='_MOD_CAN_',font='_15',size=8)]
    ]
    update_record_window = sg.Window("Update the member's information",layout,modal=True,keep_on_top=True)
    while True:
        event,values = update_record_window.read()
        if event in (sg.WINDOW_CLOSED,'Exit','_MOD_CAN_'):
            return_list =copy.copy(record_list)
            break
        if event == '_MOD_OK_':
            is_valued = []
            update_list = []
            for i in record_key:
                update_list.append(values[i])
            for i in (3,5):
                if update_list[i] =='':
                    update_list[i] = '0'
            is_valued = valid_input.validate(update_list)
            if is_valued[0]:
                UpdateDb(mn,values['_FN_'],values['_EN_'],values['_GA_'],values['_PN_'],values['_PA_'],values['_F_'])
                sg.popup(f"Member Nr:{mn}'s information has updated.",font='_15' ,title='Done',keep_on_top=True)
                return_list = [mn,values['_FN_'],values['_EN_'],values['_GA_'],values['_PN_'],values['_PA_'],
                     values['_F_']]
                break
            else:
                sg.popup_error(generate_error_message(is_valued[1]),keep_on_top=True,font='_15',title='Error!')
    update_record_window.close()
    return return_list

# Insert into database function
def InsertDb(insert_list):
    med_add = Medlemmar(insert_list[0], insert_list[1], insert_list[2], insert_list[3],
                        insert_list[4], insert_list[5])
    session.add(med_add)
    session.commit()


# Update the information into database function
def UpdateDb(MN:int,FN, EN, GA, PN, PA, F):
    member = session.query(Medlemmar).get(MN)
    member.Firstname = FN
    member.Eftername =EN
    member.Gatuadress = GA
    member.PostNr =int(PN)
    member.PostAdress =PA
    member.Fee = int(F)
    session.commit()

# Delete function
def DeleteDb(MN):
    member = session.query(Medlemmar).get(MN)
    session.delete(member)
    session.commit()


# select function through the given conditions
def SearchDb(paid_check,searchkey):

    searchfn = str(searchkey)
    return_list = []
    if paid_check:
        result = session.query(Medlemmar).filter(
            or_(Medlemmar.MedlNr ==searchkey, Medlemmar.Firstname.like(f'%{searchfn}%')),Medlemmar.Fee>0)
    else:
        result = session.query(Medlemmar).filter(or_(Medlemmar.MedlNr ==searchkey, Medlemmar.Firstname.like(f'%{searchfn}%')))
    for row in result:
        return_list.append([row.MedlNr, row.Firstname, row.Eftername, row.Gatuadress, row.PostNr, row.PostAdress, row.Fee])

    return return_list

# Obtain all records function
def SearchAllDb(paid_check):
    return_list = []
    if paid_check:
        result = session.query(Medlemmar).filter(Medlemmar.Fee>0)
    else:
        result = session.query(Medlemmar).all()

    for row in result:
        return_list.append([row.MedlNr, row.Firstname, row.Eftername, row.Gatuadress, row.PostNr, row.PostAdress, row.Fee])
    return return_list

#Show the invalid input:
def generate_error_message(values_invalid):
    error_message='Note:Name must be characters and postnumber and fee must be numbers!'
    for invalid in values_invalid:
        error_message +='\n Invalid'+':'+invalid
    return error_message