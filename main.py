import flet
import uuid

from flet import (
    LinearGradient,
    alignment,
    Page,
    Container,
    TextField,
    Column,
    Checkbox,
    TextButton,
    ElevatedButton,
    IconButton,
    Row,
    OnScrollEvent,
    AlertDialog,
    Text,
    Theme,
    ScrollbarTheme,
    MaterialState,
    colors
)


class Tarea:

    def __init__(self, page):
        self.page = page
        self.lista_task = []
        self.dlg_modal_delete = ""
        self.dlg_modal_delete_task = ""
        self.ident_event = int()
        self.page.window_width = 450
        self.page.window_height = 650

        # self.page.window_min_height = 589
        # self.page.window_min_width = 440

        # self.page.window_max_height = 589
        # self.page.window_max_width = 440

        self.page.window_center()
        self.page.update()

        self.column_scroll = Column(
            width=426,
            height=425,
            scroll=flet.ScrollMode.ALWAYS,
            on_scroll_interval=0,
            on_scroll=self.scroll,
            alignment=flet.MainAxisAlignment.CENTER,
        )

        self.page.theme = Theme(
            scrollbar_theme=ScrollbarTheme(
                track_color={
                    MaterialState.HOVERED: "transparent",
                    MaterialState.DEFAULT: colors.TRANSPARENT
                },
                track_visibility=True,
                track_border_color="transparent",
                thumb_visibility=True,
                thumb_color={
                    MaterialState.HOVERED: "#46484C",
                    MaterialState.DEFAULT: "#46484C"
                }
            )
        )

        self.row = Row(
            expand=True,
            controls=[
                self.column_scroll
            ],
            alignment=flet.MainAxisAlignment.CENTER
        )

        self.input_text = TextField(label="Write Task",
                                    width=400,
                                    height=65,
                                    bgcolor="white",
                                    multiline=True,
                                    border_radius=18
                                    )

        self.column_input = Container(
            margin=15,
            content=Row(
                controls=[
                    self.input_text
                ],
                alignment=flet.MainAxisAlignment.CENTER
            ),
        )

        self.button_add = ElevatedButton("Añadir",
                                         icon="ADD_CIRCLE_OUTLINED",
                                         width=140,
                                         height=40,
                                         on_click=self.add,
                                         icon_color="#4A356A",
                                         color="#4A356A",
                                         # bgcolor="white"
                                         )
        self.button_clear = ElevatedButton("Vaciar",
                                           icon="DELETE",
                                           width=140,
                                           height=40,
                                           on_click=self.open_dlg_modal,
                                           icon_color="#4A356A",
                                           color="#4A356A",
                                           )

        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Porfavor confirme"),
            content=Text("¿Seguro que quieres borrar todas tus tareas?"),
            actions=[
                TextButton("Yes", on_click=self.close_dlg),
                TextButton("No", on_click=self.close_dialog_no),
            ],
            actions_alignment=flet.MainAxisAlignment.END,
        )

        self.lista_buttons = Container(
            Row(controls=[
                self.button_add,
                Container(
                    width=30
                ),
                self.button_clear
            ],
                alignment=flet.MainAxisAlignment.CENTER
            ),
            margin=15
        )

        self.page.update()

        self.container_secundario = Container(
            content=self.row,

        )

        self.container_principal = Container(
            # bgcolor="red",
            gradient=LinearGradient(
                begin=alignment.center_right,
                end=alignment.top_left,
                colors=["#1B1427", "#2E2142", "#412E5D"]
            ),
            expand=True,
            margin=-10,
            height=self.page.height,
            content=Column(
                controls=[
                    self.column_input,
                    self.lista_buttons,
                    self.container_secundario
                ],
            )
        )

    def open_dlg_modal(self, e):
        if len(self.column_scroll.controls) == 0:
            pass
        elif len(self.column_scroll.controls) > 0:
            self.page.dialog = self.dlg_modal
            self.dlg_modal.open = True
            self.page.update()

    def close_dlg(self, e):
        self.column_scroll.controls = []
        self.lista_task = []
        self.dlg_modal.open = False
        self.input_text.value = ""
        self.page.update()

    def close_dialog_no(self, e):
        self.dlg_modal.open = False
        self.page.update()

    def add(self, e):
        text_value = self.input_text.value.capitalize()
        if text_value:
            self.create_task(text_value)

    def scroll(self, e: OnScrollEvent):
        print(e)

    def insert_task(self):
        self.column_scroll.controls = []

        if len(self.lista_task) > 0:
            for x in self.lista_task:
                self.column_scroll.controls.insert(0, x[1])
                self.page.update()
        elif len(self.lista_task) == 0:
            self.column_scroll.controls = []
            self.page.update()

    def create_task(self, text):
        dlg_modal_delete_task = ""

        code = uuid.uuid4()

        def open_dialog():
            self.page.dialog = dlg_modal_delete_task
            dlg_modal_delete_task.open = True
            self.page.update()

        def identificator(e):
            open_dialog()
            if self.ident_event is not None:
                self.ident_event = e

        def close_dialog_no(e):
            dlg_modal_delete_task.open = False
            self.page.update()

        def delete_task(e):
            data = self.ident_event
            for n in self.lista_task:
                if n[0] == data:
                    self.lista_task.remove(n)
                    self.insert_task()
                    dlg_modal_delete_task.open = False
                    self.page.update()
                else:
                    pass

        def edit_task(e):
            if camp_text.read_only:
                camp_text.read_only = False
                icon_edit.icon = "CHECK"
                icon_edit.icon_color = "white"
                icon_edit.bgcolor = "green"
                camp_text.bgcolor = "#E2C8E3"
                camp_text.border_color = "#06F72B"
                self.page.update()
            elif not camp_text.read_only:
                camp_text.read_only = True
                icon_edit.icon = "EDIT"
                icon_edit.icon_color = "#4A356A"
                camp_text.border_color = "#3E627F"
                icon_edit.bgcolor = "white"
                camp_text.bgcolor = "white"
                self.page.update()

        checkbox = Checkbox(
            value=False,
            fill_color="white",
            check_color="#4A356A",
        )
        camp_text = TextField(value=text,
                              read_only=True,
                              bgcolor="white",
                              multiline=True,
                              border_radius=18,
                              width=285
                              )
        icon_edit = IconButton(
            icon="EDIT",
            width=40,
            height=40,
            on_click=edit_task,
            icon_color="#4A356A",
            bgcolor="white",
        )
        icon_delete = IconButton(
            icon="DELETE",
            width=40,
            height=40,
            on_click=lambda k: identificator(k.control.data),
            icon_color="#4A356A",
            bgcolor="white",
            data=code
        )

        dlg_modal_delete_task = AlertDialog(
            modal=True,
            title=Text("Porfavor confirme"),
            content=Text("¿Seguro que quiere borrar esta tarea?"),
            actions=[
                TextButton("Yes", on_click=delete_task),
                TextButton("No", on_click=close_dialog_no),
            ],
            actions_alignment=flet.MainAxisAlignment.END,
        )

        self.lista_task.append((code, Container(
            width=self.page.width,
            content=Row(
                spacing=3,
                controls=[
                    checkbox,
                    camp_text,
                    icon_edit,
                    icon_delete
                ],
                alignment=flet.MainAxisAlignment.START
            )
        )
                                )
                               )

        for i in self.lista_task:
            if i[1] in self.column_scroll.controls:
                pass
            elif i[1] not in self.column_scroll.controls:
                self.column_scroll.controls.insert(0, i[1])
                self.input_text.focus()

        self.input_text.value = ""

        self.page.update()

    def start_td(self):
        self.page.add(self.container_principal)
        self.page.update()


def main(page: Page):
    task = Tarea(page)
    task.start_td()
    page.update()


flet.app(target=main)
