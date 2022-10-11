import PySimpleGUI as sg


def CreateVisualizationViewLayout():
    left_col = [[sg.T('File Location')],
                [sg.InputText(size=(25, 1), key='-FILENAME-'), sg.FileBrowse()],
                [sg.T('Figures to Draw')],

                [sg.T('Options')],
                [sg.T('Years:')],
                [sg.Checkbox('2022', key='2022'), sg.Checkbox('2021', key='2021'),
                 sg.Checkbox('2020', key='2020')],
                [sg.Checkbox('2019', key='2019'),
                 sg.Checkbox('2018', key='2018'), sg.Checkbox('2017', key='2017')],
                [sg.T('Scams Types')],
                [sg.Checkbox('Investment Scam', key='INVESTMENT'), sg.Checkbox('Job Scam', key='JOB')],
                [sg.Checkbox('Love Scam', key='LOVE'), sg.Checkbox('Impersonation Scam', key='IMPERSONATION')]]

    layout = [[sg.T('Data Visualization', font='Any 20')],
              [sg.Col(left_col), sg.Image(key='-IMAGE-')],
              [sg.B('Visualise'), sg.B('Exit')]]

    return layout
