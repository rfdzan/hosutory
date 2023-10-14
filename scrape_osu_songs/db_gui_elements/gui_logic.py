from subprocess import run
from webbrowser import open
from db.sql_query import update_fave
from db.search_db import query_the_db
import PySimpleGUI as sG


class Logic:
    def __init__(self):
        self.result = []

    def clear_result(self):
        self.result.clear()

    def search(self, query_the_db, values, window):
        self.clear_result()
        data = query_the_db(values)
        for item in data:
            self.result.append(item)
        window["-TABLE-"].update(values=self.result)
        window["prog"].update(value=f"Loaded {len(self.result)} songs.")

    def add_fave(self, event, fave_key, table_index, window, values):
        if event == fave_key[0]:
            mark = "*"
        else:
            mark = ""
        id_num = self.result[table_index[0]][4]
        data = {"favorite": mark, "id": id_num}
        update_fave(data)
        self.search(
            query_the_db, values, window
        )  # return value never updates context menu.

    def to_clipboard(self, event, table_index):
        copy_prefix = {"Copy::rCopy": "", "Copy Munix::rMunix": "+p "}
        try:
            to_copy = (
                f"{copy_prefix.get(event)}"
                f"{self.result[table_index[0]][0]} {self.result[table_index[0]][1]}"
            )
            run(["clip.exe"], input=to_copy.encode("utf-8"))
        except UnboundLocalError:
            sG.popup("No track selected!")

    def preview_song(self, table_index):
        try:
            web_link = self.result[table_index[0]][5]
            open(web_link, new=2)
        except UnboundLocalError:
            sG.popup("No track selected!")

    def context_menu(self, event, table_index, window, values):
        if event in ("Copy::rCopy", "Copy Munix::rMunix"):
            self.to_clipboard(event, self.result, table_index)

        if event == "Preview::rPreview":
            self.preview_song(self.result, table_index)

        fave_key = ("Mark as Favorite::markFav", "Remove from Favorite::delFav")
        if event in fave_key:
            self.add_fave(event, fave_key, table_index, window, values)
