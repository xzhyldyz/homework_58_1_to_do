import flet as ft 
from db import main_db
from datetime import datetime as dt

def main(page: ft.Page):
    page.title = 'ToDo list'
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=10)

    filter_type = 'all'

    def load_task():
        task_list.controls.clear()
        for task_id, task_text, completed in main_db.get_tasks(filter_type):
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task_text, completed=completed))
        page.update()


    def create_task_row(task_id, task_text, completed):
        task_field = ft.TextField(value=task_text, read_only=True, expand=True)

        checkbox = ft.Checkbox(value=bool(completed), on_change=lambda e: toggle_task(task_id, e.control.value))

        def enable_edit(_):
            task_field.read_only = False
            task_field.update()

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, tooltip="Редактировать", on_click=enable_edit, icon_color=ft.Colors.ORANGE_700)

        def save_task(_):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            task_field.read_only = True
            task_field.update()
            page.update()

        save_button = ft.IconButton(icon=ft.Icons.SAVE_ALT_ROUNDED, on_click=save_task)

        def delete_task(_):
            main_db.delete_task(task_id)
            load_task()
        
        delete_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=delete_task, icon_color=ft.Colors.RED)

        return ft.Row([checkbox, task_field, edit_button, save_button, delete_button])

    def add_task(_):
        if task_input.value:
            task = f"{dt.now().strftime('%H:%M:%S')}-{task_input.value}"
            task_id = main_db.add_task(task)
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task, completed=None))

            task_input.value = ''
            page.update()

    def toggle_task(task_id, is_completed):
        main_db.update_task(task_id=task_id, completed=int(is_completed))
        load_task()

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_task()

    filter_buttons = ft.Row([
        ft.ElevatedButton("Все", on_click=lambda e: set_filter('all')),
        ft.ElevatedButton('В работе', on_click=lambda e: set_filter('uncompleted')),
        ft.ElevatedButton("Готово", on_click=lambda e: set_filter('completed'))
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    task_input = ft.TextField(label='Введите новую задачу', expand=True)
    add_button = ft.IconButton(icon=ft.Icons.ADD, tooltip='Добавить задачу', on_click=add_task)

    page.add(ft.Row([task_input, add_button]),filter_buttons, task_list)

    load_task()


if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)