import os
import sys
import base64
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


def opentree():
    try:
        bt_open.configure(state="disabled")
        file_path = filedialog.askopenfilename(filetypes=((('Text files'), '*.txt'), (('All files'), '*.*')))
        if not file_path:
            return
        lines = 0
        for line in open(file_path):
            lines += 1
        
        tree.delete(*tree.get_children())
        with open(file_path, 'r') as file:
            iid = 1
            stack = [0, 0]
            file.readline()
            file.readline()
            tree.heading('#0', text=file_path, anchor='w')
            path = file.readline()
            tree.insert('', tk.END, text=path[:(len(path) - 1)], iid=0, open=True)

            while True:
                _proglast = progb['value']
                _prog = int(100 * iid / lines)
                if _prog - _proglast > 1:
                    progb['value'] = _prog
                    root.update_idletasks()

                isdir = False
                line = file.readline()
                if not line:
                    break
                if not line.startswith((' ', '+', '|', '\\')):
                    continue
                level = 0
                for s in ['|   ', '    ']:
                    level += line.count(s)
                for s in ['+---', '\---']:
                    c = line.count(s)
                    level += c
                    if c > 0:
                        isdir = True
                stack = stack[:(level + 1)]
                if level != 0:
                    line = line[(4 * level):]
                line = line[:(len(line) - 1)] # endl removal
                if not line:
                    continue  # last dir entry is always empty
                # if isdir:
                #     line = '[' + line + ']'
                if isdir:
                    tree.insert(stack[level], tk.END, text=line, image=ico_folder, iid=iid, open=False)
                else:
                    tree.insert(stack[level], tk.END, text=line, image=ico_file, iid=iid, open=False)
                stack.append(iid)
                iid += 1
    except Exception as e:
        tree.delete(*tree.get_children())
        messagebox.showerror("Open file failed", f'{type(e).__name__}\n{e}')
    finally: 
        progb['value'] = 0
        bt_open.configure(state="normal")


def rmenu_raise(event):
    try:
        rmenu.tk_popup(event.x_root, event.y_root)
    finally:
        rmenu.grab_release()


def copypath():
    item_iid = tree.selection()[0]
    parent_iid = tree.parent(item_iid)
    s = tree.item(item_iid)['text']
    while parent_iid:
        s = tree.item(parent_iid)['text'] + '\\' + s
        parent_iid = tree.parent(parent_iid)
    root.clipboard_clear()
    root.clipboard_append(s)
    return


def cleanup():
    tree.delete(*tree.get_children())
    root.destroy()
    return


###


root = tk.Tk()
root.title('tree4eyes')
root.geometry('400x500')

bar = tk.Frame(root)
bt_open = tk.Button(bar, text="Open...", command=opentree)
bt_open.pack(side=tk.LEFT, padx=5, pady=5, ipadx=2)
progb = ttk.Progressbar(bar, orient='horizontal', mode='determinate', length=280)
progb.pack(side=tk.LEFT, fill='x')
bar.pack(side=tk.TOP, fill='x')

scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
tree = ttk.Treeview(root, yscrollcommand=scrollbar.set)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
scrollbar.config(command=tree.yview)

rmenu = tk.Menu(tree, tearoff=0)
rmenu.add_command(label="Copy path", command=copypath)
tree.bind("<Button-3>", rmenu_raise)
root.protocol("WM_DELETE_WINDOW", cleanup)  # needed coz shutdown hans for large trees

ico_app_raw = 'R0lGODlhEAAQAHcAACH5BAkKAAAALAAAAAAQABAAgAAAAAgICAImhI+pGO1hYJKNLVipmzsCuVhd+JXkgT2VAqKhGj2sRXbjief6UQAAOw=='
ico_app = tk.PhotoImage(data=ico_app_raw)
ico_file_raw = 'R0lGODdhDAAMAHcAACH5BAkKAAAALAAAAAAMAAwAgAAAAAEBAQIXhI+pGh0LnpGJRkbtRDq2XXGY00EmUgAAOw=='
ico_file = tk.PhotoImage(data=ico_file_raw)
ico_folder_raw = 'R0lGODlhDAAMAHcAACH5BAkKAAAALAAAAAAMAAwAgAAAAAEBAQIVhI+pyxuPnjzBVCrvVZp1Z2ViQyoFADs='
ico_folder = tk.PhotoImage(data=ico_folder_raw)

root.iconphoto(False, ico_app)
root.mainloop()

