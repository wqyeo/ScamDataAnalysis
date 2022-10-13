import PySimpleGUI as sg

#region NOTE: Keys

TARGET_FILE_LOCATION_KEY = "TARGET_FILE_LOCATION_KEY"
PLOT_IMAGE_KEY = "ANALYZE_PLOT_IMG_KEY"
PLOT_IMAGES_SELECTOR_KEY = "PLOT_IMAGES_SELECTOR_KEY"

USER_MESSAGE_KEY = "PLOTTER_USER_MESSAGE_KEY"

#endregion

#region NOTE: Events

START_ANALYZE_EVENT = "Analyze"

#endregion

def CreateVisualizationViewLayout():
    leftColumn = [
        [sg.T('File Location')],
                [sg.InputText(size=(25, 1), key=TARGET_FILE_LOCATION_KEY), sg.FileBrowse(target=TARGET_FILE_LOCATION_KEY, file_types=(("JSON files", "*.json"),) )],
                [sg.B(START_ANALYZE_EVENT)]
    ]

    rightColumn = [
        [sg.Image(key=PLOT_IMAGE_KEY)],
        [sg.Combo(values=["Very Very Long Box"], key = PLOT_IMAGES_SELECTOR_KEY, visible=False)]
    ]

    layout = [[sg.T('Data Visualization', font='Any 20')],
              [sg.Col(leftColumn), sg.Col(rightColumn)]
              ]

    return layout
