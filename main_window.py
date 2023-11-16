
# This file would show the main  interface
#__________________________________#

import copy

import PySimpleGUI as sg
from PySimpleGUI import Column,Frame,Button,Input,Table,Text

import database_interface
import os
import create_databse

sg.theme('LightBlue2')

#sg.theme_button_color(('Black','#7186C7'))

if not os.path.exists('Members.db'):
    create_databse.CreatDb()

initial_list =[]
col11 = Column([[Frame('Search information',[[Text(),Column([[Text('Name or Medlemm Nummer',font='_15')],
                                                [Input(key='_SearchI_',font='_15',size=35),
                                                 Button('Search',expand_x= True,font='_15',key='_Sear_',size =8)],
                                                #[Button('Show all',key='_SearAll_',size=6)],
                                                ])],[sg.Checkbox('Show only with annual fee paid',font='_15',
                                                                 key='_P_')]],font='_15')],],pad =(0,0),)
col12 = Column([[Button('Add member',key='_ADD_',size=20,font='_15')],[Button('Update Selected',key='_UPD_',
                                                                              size=20,font='_15')],
                [Button('Delete Selected',key='_DEL_',size=20,font='_15')],[Button('Show all members',key='_SearAll_',
                                                                                   size=20,font='_15')]],justification='center')
col2 = Column([[Frame('Members Information',[[Column([[Table(values=initial_list,font='_15',#size=(2000,2000),
                                                               headings=[' Nr. ', 'FirstName','Eftername','Street Address'
                                                               ,'Post Number','     Post Address    ','Annual fee'],
                                                              auto_size_columns=True,
                                                               select_mode='browse',
                                                              header_font='bold 15',



                                                              header_border_width=2,
                                                               # header_background_color='blue',
                                                               # header_text_color= 'white',
                                                               alternating_row_color='lightblue',
                                                               display_row_numbers= True,
                                                               enable_events= True,

                                                               justification='center',
                                                               key='_TABEL_',expand_x=True)],],)]],font='_12',)]],)
              #element_justification='c')
layout =[[col11,sg.VSep(),col12],[sg.HSep()],[col2]]
window = sg.Window('Members Manage System',layout)
result =[]
tabel_list =[]
selected_row= []
selected_row_index= None
paid_check= False
button_list =['_Sear_','_SearAll_','_ADD_','_DEL_','_UPD_']
while True:
    event,values = window.read()
    if event in (sg.WINDOW_CLOSED, 'Exit'):
        break

    if event == '_Sear_':
        paid_check = values['_P_']
        text_input = values['_SearchI_']
        if text_input =='':
            sg.popup_error('Please input firstname or member number',title='Error!',keep_on_top=True,font='_15')
        else:
            tabel_list = database_interface.SearchDb(paid_check,text_input)
            window['_TABEL_'].Update(tabel_list)

    if event == '_SearAll_':
        paid_check = values['_P_']
        tabel_list= database_interface.SearchAllDb(paid_check)
        window['_TABEL_'].Update(tabel_list)

    if event == '_ADD_':
        for i in  button_list:
            window[i].Update(disabled=True)

        database_interface.add_record()

        for i in  button_list:
            window[i].Update(disabled=False)

    if event =='_TABEL_':
        try:
            selected_row_index = values['_TABEL_'][0]
            selected_row = copy.copy(tabel_list[selected_row_index])

        except IndexError:
            continue

    if event == '_DEL_':
        for i in  button_list:
            window[i].Update(disabled=True)

        try:

            if database_interface.del_record(int(selected_row[0]),selected_row[1]):

                del tabel_list[selected_row_index]
                window['_TABEL_'].Update(tabel_list)

        except IndexError:
             sg.popup_error('Please select row to delete!',title='Error!',font='_15')
        for i in  button_list:
            window[i].Update(disabled=False)

    if event == '_UPD_':
        for i in button_list:
            window[i].Update(disabled=True)
        try:
            tabel_list[selected_row_index]=database_interface.update_record(selected_row)
            window['_TABEL_'].Update(tabel_list)
            selected_row.clear()
        except IndexError:
            sg.popup_error('Please select row to update!',title='Error!',font='_15')

        for i in  button_list:
            window[i].Update(disabled=False)

window.close()


#[Text('Members Manage System',font='bold 20',justification='c')]





