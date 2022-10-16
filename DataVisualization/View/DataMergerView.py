import PySimpleGUI as sg

#region NOTE: Keys

FIRST_MERGE_FILE_LOCATION_KEY = "FIRST_MERGE_FILE_LOCATION_KEY"
SECOND_FILE_LOCATION_KEY = "SECOND_MERGE_FILE_LOCATION_KEY"
MERGED_PLOT_IMAGE_KEY = "MERGED_ANALYZE_PLOT_IMG_KEY"
MERGED_PLOT_IMAGES_SELECTOR_KEY = "MERGED_PLOT_IMAGES_SELECTOR_KEY"

USER_MESSAGE_KEY = "MERGED_PLOTTER_USER_MESSAGE_KEY"

#endregion

#region NOTE: Events

START_MERGE_EVENT = "Merge"

#endregion

def CreateMergerViewLayout():
    leftColumn = [
                [sg.T('Select Second File to Merge:')],
                [sg.InputText(size=(25, 1), key=FIRST_MERGE_FILE_LOCATION_KEY), sg.FileBrowse(target=FIRST_MERGE_FILE_LOCATION_KEY, file_types=(("JSON files", "*.json"),) )],
                [sg.T('Select First File to Merge:')],
                [sg.InputText(size=(25, 1), key=SECOND_FILE_LOCATION_KEY), sg.FileBrowse(target=SECOND_FILE_LOCATION_KEY, file_types=(("JSON files", "*.json"),) )],
                
                [sg.B(START_MERGE_EVENT)]
    ]

    rightColumn = [
        [sg.Image(key=MERGED_PLOT_IMAGE_KEY)],
        [sg.Combo(values=["Very Very Long Box With Message To Spare"], key = MERGED_PLOT_IMAGES_SELECTOR_KEY, visible=False)]
    ]

    layout = [
              [sg.Col(leftColumn), sg.Col(rightColumn)],
              [sg.T("", key=USER_MESSAGE_KEY)]
    ]

    return layout
