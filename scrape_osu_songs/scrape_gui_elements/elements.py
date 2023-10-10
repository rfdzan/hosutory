from dataclasses import dataclass

import PySimpleGUI as sG

sG.theme("SystemDefaultForReal")


@dataclass
class ScrapeGUI:
    text_id = [sG.Text("ID:")]
    user_id = [sG.InputText("", key="-ID-")]
    start_stop = [
        sG.Text("start:"),
        sG.InputText("0", size=(10, 10), key="-INDEXSTART-"),
        sG.Text("stop:"),
        sG.InputText("", size=(10, 10), key="-INDEXSTOP-"),
    ]
    json_dbstore = [
        sG.Checkbox("Store JSON to Database", default=True, key="-STOREDB-")
    ]
    start_procedure = [sG.Button("Start")]
    text_progress = [sG.Text("No downloads.", key="-PROGTXT-")]
    progress = [sG.ProgressBar(100, orientation="h", size=(30, 10), key="-PROGRESS-")]
    text_progress_db = [sG.Text("No database task.", key="-PROGTXTDB-")]
    progress_db = [sG.ProgressBar(100, orientation="h", size=(30, 10), key="-PROGDB-")]
