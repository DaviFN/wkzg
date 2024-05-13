import PySimpleGUI as sg

from wkzg_core import apply_wkzg

sg.theme('Light Blue 2')

toolDescription = "Tool's purpose: add field 'instanceId' in C++ classes to serve debug purposes\nSuch field can be useful to give an idea of which instances are associated with a problem\nClasses with higher instance ids were instantiated after classes with lower instance ids";

layout = [
    [sg.Text(toolDescription)],
    [sg.Button('Apply to files', key = 'applytofiles')],
    [sg.Multiline(default_text = 'Add class names here (semicolon-separated)', key = 'classesNamesLineEdit', size=(None, 3))]
]

window = sg.Window("WKZG", layout)

def process_file(file: str, classesStrInput: str):
    print('processing file: ' + file)
    print('classesStrInput: ' + classesStrInput)

    classesNames = classesStrInput.split(';')

    apply_wkzg(file, classesNames);

def on_apply_to_files():
    filesAsStr = sg.popup_get_file('Select the files', multiple_files=True)
    
    files = None
    if filesAsStr:
        files = filesAsStr.split(';')

    if files:
        classesStrInput = values['classesNamesLineEdit']
        for file in files:
            process_file(file, classesStrInput)

while True:
    event, values = window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, '-EXIT-'):
        break
    if event == 'applytofiles':
        on_apply_to_files()
window.close()