import PySimpleGUI as sg
from datetime import datetime

sg.theme('Black')

layout = [[sg.Text("Enter full name:"), sg.Input(key='-NAME-', do_not_clear=True, size=(20, 1))],
          [sg.Text("Enter your passport number:"), sg.Input(key='-PASSPORT_NUMBER-', do_not_clear=True, size=(10, 1))],
          # "RADIO" makes the radio buttons part of the same group, so when you click one, the other will be unchecked
          [sg.Radio("Male", "RADIO", key='-MALE-'), sg.Radio("Female", "RADIO", key='-FEMALE-')],
          [sg.Input(key='-DEPARTURE-', size=(20,1)), sg.CalendarButton("DATE OF DEPARTURE", close_when_date_chosen=True,  target='-DEPARTURE-', location=(0,0), no_titlebar=False )],
          [sg.Input(key='-ARRIVAL-', size=(20,1)), sg.CalendarButton("DATE OF ARRIVAL", close_when_date_chosen=True,  target='-ARRIVAL-', location=(0,0), no_titlebar=False )],
          [sg.Text('Choose your destination:',size=(30, 1), font='Lucida',justification='left')],
          # Formatting is weird on Mac - also need to change number of rows based on desired appearance
          [sg.Listbox(values=['Havana', 'Moscow', 'Beijing', 'Tehran', 'Damascus', 'Tripoli', 'Sanaa'], size=(40, 5), select_mode='single', key='-DESTINATION-')],
          [sg.Button('Reserve Ticket'), sg.Exit()]
]

window = sg.Window('привет Airlines', layout)

def format_input_information(values):
    information = "Flight booked!"
    name = '\nName: ' + values['-NAME-']
    information += name
    passport_number = '\nPassport Number: ' + values['-PASSPORT_NUMBER-']
    information += passport_number
    gender = '\nGender: ' 
    if values['-FEMALE-']: 
        gender += 'Female'
    else: 
        gender += 'Male'
    information += gender
    departure_time = '\nDeparture Time: ' + values['-DEPARTURE-']
    information += departure_time
    arrival_time = '\nArrival Time: ' + values['-ARRIVAL-']
    information += arrival_time
    # Listbox will return an array of 1 element because it's marked as 'single', otherwise it would return a larger array
    destination = '\nDestination: ' + values['-DESTINATION-'][0]
    information += destination
    
    return information

# This is to make sure that the arrival date is not before the departure date
def is_arrival_before_departure(departure_string, arrival_string):
    # 2021-08-01 13:09:43
    departure_object = datetime.strptime(departure_string, '%Y-%m-%d %H:%M:%S')
    arrival_object = datetime.strptime(arrival_string, '%Y-%m-%d %H:%M:%S')
    return arrival_object < departure_object



def validate(values):
    is_valid = True
    values_invalid = []

    if len(values['-NAME-']) == 0:
        values_invalid.append('Name')
        is_valid = False

    if len(values['-PASSPORT_NUMBER-']) == 0:
        values_invalid.append('Passport Number')
        is_valid = False

    if not values['-MALE-'] and not values['-FEMALE-']:
        values_invalid.append('Gender')
        is_valid = False

    if len(values['-DEPARTURE-']) == 0:
        values_invalid.append('Departure Time')
        is_valid = False

    if len(values['-ARRIVAL-']) and is_arrival_before_departure(values['-DEPARTURE-'], values['-ARRIVAL-']):
        values_invalid.append('Arrival Time')
        is_valid = False
        
    # This is how you handle a case when an error may occur
    try:
        print(values['-DESTINATION-'][0])
    except:
        values_invalid.append('Destination')
        is_valid = False 

    result = [is_valid, values_invalid]
    return result

def generate_error_message(values_invalid):
    error_message = ''
    for value_invalid in values_invalid:
        error_message += ('\nInvalid' + ':' + value_invalid)

    return error_message

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Reserve Ticket':
        validation_result = validate(values)
        if validation_result[0]:
            sg.popup(format_input_information(values))
        else:
            error_message = generate_error_message(validation_result[1])
            sg.popup(error_message)
window.close()

