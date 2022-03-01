from keyboa import Button, Keyboa


def reminder_list_controls_keyboard(page, left=True, right=True, master_prefix='ddoslist'):
    buttons = []
    items_in_row = 0
    if left:
        items_in_row += 1
        buttons.append(Button(button_data=dict(text="⏪️", callback_data=f'{master_prefix}_arrow_left${page}')).generate())

    if right:
        items_in_row += 1
        buttons.append(Button(button_data=dict(text="⏩️", callback_data=f'{master_prefix}_arrow_right${page}')).generate())

    return Keyboa(buttons, items_in_row=items_in_row).keyboard


def list_keyboard(list_len: int, page: int, page_size: int = 8, master_prefix='ddoslist'):
    page_items = list(range(1, list_len + 1))[page*page_size:(page + 1) * page_size]
    keyboard = [
        Keyboa(page_items, items_in_row=4, front_marker=f'{master_prefix}_select$').keyboard
    ]
    if list_len > page_size:
        keyboard.append(
            reminder_list_controls_keyboard(page, page > 0, page < list_len // page_size, master_prefix=master_prefix)
        )

    keyboard.append(
        Keyboa(Button(button_data=dict(text="❌", callback_data=f'{master_prefix}_cancel')).generate(),).keyboard
    )

    return Keyboa.combine(tuple(keyboard))


def remove_ddos_keyboard(container_name, lang: str):
    choices = dict(
        uk=dict(
            delete="Стерти",
            back="Назад до списку",
        ),
        ru=dict(
            delete="Удалить",
            back="Назад к списку",
        ),
        en=dict(
            delete="Stop",
            back="Back to list",
        ),
    )[lang]
    return Keyboa.combine((
        Keyboa([
            Button(button_data=dict(text=f"❌{choices['delete']}", callback_data=f'ddos_remove${container_name}')).generate(),
            Button(button_data=dict(text=f"⏩{choices['back']}", callback_data='ddos_back_to_list')).generate(),
        ], items_in_row=2).keyboard,
    ))
