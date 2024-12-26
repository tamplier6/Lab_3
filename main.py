from tkinter import *
from tkinter import messagebox, filedialog


# Функция выхода с подтверждением
def notepad_exit():
    if text_fild.edit_modified():  # Проверка на изменения в тексте
        answer = messagebox.askyesnocancel('Сохранение', 'Сохранить изменения перед выходом?')
        if answer:  # Да - сохранить
            save_file()
        elif answer is None:  # Отмена - не выходить
            return
    root.destroy()  # Выйти из приложения


# Функция открытия файла
def open_file():
    file_path = filedialog.askopenfilename(
        title='Выбор файла',
        filetypes=(('Текстовые документы (*.txt)', '*.txt'), ('Все файлы', '*.*'))
    )
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            text_fild.delete('1.0', END)
            text_fild.insert('1.0', file.read())
        text_fild.edit_modified(False)  # Сбрасываем флаг модификации


# Функция сохранения файла
def save_file():
    file_path = filedialog.asksaveasfilename(
        filetypes=(('Текстовые документы (*.txt)', '*.txt'), ('Все файлы', '*.*'))
    )
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text_fild.get('1.0', END))
        text_fild.edit_modified(False)  # Сбрасываем флаг модификации


# Создание главного окна
root = Tk()
root.title('Текстовый редактор')
root.geometry('800x600')

# Меню приложения
main_menu = Menu(root)
file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label='Открыть', command=open_file)
file_menu.add_command(label='Сохранить', command=save_file)
file_menu.add_separator()
file_menu.add_command(label='Выход', command=notepad_exit)
main_menu.add_cascade(label='Файл', menu=file_menu)
root.config(menu=main_menu)

# Рамка для текстового поля и скролла
f_text = Frame(root)
f_text.pack(fill=BOTH, expand=1)

# Текстовое поле
text_fild = Text(f_text,
                 bg='white',
                 fg='black',
                 padx=12,
                 pady=12,
                 wrap=WORD,
                 insertbackground='black',
                 selectbackground='#8D917A',
                 spacing3=10,
                 font='Arial 14 bold'
                 )
text_fild.pack(expand=1, fill=BOTH, side=LEFT)

# Прокрутка
scroll = Scrollbar(f_text, command=text_fild.yview)
scroll.pack(side=LEFT, fill=Y)
text_fild.config(yscrollcommand=scroll.set)


# Контекстное меню (Копировать, Вставить, Вырезать)
def create_context_menu():
    context_menu = Menu(root, tearoff=0)
    context_menu.add_command(label='Копировать', command=lambda: root.focus_get().event_generate('<<Copy>>'))
    context_menu.add_command(label='Вставить', command=lambda: root.focus_get().event_generate('<<Paste>>'))
    context_menu.add_command(label='Вырезать', command=lambda: root.focus_get().event_generate('<<Cut>>'))
    text_fild.bind('<Button-3>', lambda e: context_menu.post(e.x_root, e.y_root))


create_context_menu()


# Горячие клавиши
root.bind('<Control-s>', lambda event: save_file())
root.bind('<Control-o>', lambda event: open_file())
root.bind('<Control-q>', lambda event: notepad_exit())

# Запуск основного цикла
root.mainloop()
