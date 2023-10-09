from subprocess import run
from webbrowser import open

import PySimpleGUI as sG


def search(query_the_db, values, window):
    data = query_the_db(values)
    result = []
    for item in data:
        result.append(item)
    window["-TABLE-"].update(values=result)
    window["prog"].update(value=f"Loaded {len(result)} songs.")
    return result


def context_menu(event, result, index):
    if event in ("Copy::rCopy", "Copy Munix::rMunix"):
        copy_prefix = {"Copy::rCopy": "", "Copy Munix::rMunix": "+p "}
        try:
            to_copy = (
                f"{copy_prefix.get(event)}"
                f"{result[index[0]][0]} {result[index[0]][1]}"
            )
            run(["clip.exe"], input=to_copy.encode("utf-8"))
        except UnboundLocalError:
            sG.popup("No track selected!")
    if event == "Preview::rPreview":
        try:
            web_link = result[index[0]][3]
            open(web_link, new=2)
        except UnboundLocalError:
            sG.popup("No track selected!")
