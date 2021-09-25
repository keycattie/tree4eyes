# tree4eyes r0
__version__ = 'r0v0.1-dev.pooling.1'

import os
import sys
import time
import base64
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import anytree as at


def opentree():
    try:
        bt_open.configure(state='disabled')

        file_path = filedialog.askopenfilename(filetypes=((('Text files'), '*.txt'), (('All files'), '*.*')))
        if not file_path:
            return

        infotxt.set('Loading tree file...')
        root.update_idletasks()
        tree.delete(*tree.get_children())

        fsize = os.path.getsize(file_path)
        tsize = 0
        pupd = time.time()
        nupd = pupd 
        with open(file_path, 'r') as file:
            global tr
            iid = 1
            file.readline()
            file.readline()
            tree.heading('#0', text=file_path, anchor='w')
            path = file.readline()
            tree.insert('', tk.END, text=path[:(len(path) - 1)], iid=0, open=True)
            tr = at.AnyNode(id=path[:(len(path) - 1)], iid=0, isdir=True)
            stack = [tr, tr]

            while True:
                isdir = False
                line = file.readline()
                tsize += len(line)
                if not line:
                    break
                if not line.startswith((' ', '+', '|', '\\')):
                    continue
                level = 0

                while line.startswith(('|   ', '    ')):
                    line = line[4:]
                    level += 1
                if line.startswith(('+---', '\---')):
                    line = line[4:]
                    level += 1
                    isdir = True
                line = line[:(len(line) - 1)] # endl removal
                if not line:
                    continue  # last dir entry is always empty
                node = at.AnyNode(id=line, parent=stack[level], iid=iid, isdir=isdir)
                stack = stack[:(level + 1)]
                stack.append(node)
                iid += 1

                nupd = time.time()
                if nupd - pupd > .25:
                    pupd = nupd
                    infotxt.set(f'Loading tree file, {(tsize / fsize * 100):.2f}%...')
                    root.update_idletasks()
        
        tree.insert(0, tk.END, text='/...', iid=-1, open=False)
        treelevel(0)
        tree.delete(-1)
    except Exception as e:
        tree.delete(*tree.get_children())
        infotxt.set('An error occurred loading the file')
        root.update_idletasks()
        messagebox.showerror('Open file failed', f'{type(e).__name__}\n{e}')
    finally: 
        bt_open.configure(state='normal')
    infotxt.set('File successfully loaded')
    root.update_idletasks()


def treelevel(piid):
    global dummycount, tr

    # search optimization
    # TODO list of parent node references for iid-s that had already been loaded  
    n = piid
    lev = 1
    while True:
        n = tree.parent(n)
        if not n:
            break
        lev += 1
    parent = at.search.find_by_attr(tr, int(piid), name='iid', maxlevel=lev)
    if parent:
        for c in parent.children:
            if c.isdir:
                tree.insert(piid, tk.END, text=c.id, image=ico_folder, iid=c.iid, open=False)
                if c.children:
                    tree.insert(c.iid, tk.END, text='/...', iid=-dummycount, open=False)
                    dummycount += 1
            else:
                tree.insert(piid, tk.END, text=c.id, image=ico_file, iid=c.iid, open=False)

    bt_open.configure(state='normal')
    pass


def treeexpand(event):
    infotxt.set('Loading file structure...')
    root.update_idletasks()
    try:
        piid = tree.selection()[0]
        if tree.item(tree.get_children(piid)[0])['text'] == '/...':
            treelevel(piid)
            tree.delete(tree.get_children(piid)[0])
    finally:
        infotxt.set('')
        root.update_idletasks()


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


file_path = ''
dummycount = 2
tr = at.AnyNode(id=-1)

root = tk.Tk()
root.title('tree4eyes')
root.geometry('400x500')

infotxt = tk.StringVar()

bar = tk.Frame(root)
bt_open = tk.Button(bar, text='Open...', command=opentree)
bt_open.pack(side=tk.LEFT, padx=5, pady=5, ipadx=2)
l_infotxt=tk.Label(bar, textvariable=infotxt, width=255)
l_infotxt.pack(side=tk.LEFT, fill='x')
bar.pack(side=tk.TOP, fill='x')

scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
tree = ttk.Treeview(root, yscrollcommand=scrollbar.set)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
scrollbar.config(command=tree.yview)

rmenu = tk.Menu(tree, tearoff=0)
rmenu.add_command(label='Copy path', command=copypath)
tree.bind('<Button-3>', rmenu_raise)
root.protocol('WM_DELETE_WINDOW', cleanup)  # needed coz shutdown hangs for large trees
tree.bind('<<TreeviewOpen>>', treeexpand)

ico_app_raw = 'R0lGODlhEAAQAHcAACH5BAkKAAAALAAAAAAQABAAgAAAAAgICAImhI+pGO1hYJKNLVipmzsCuVhd+JXkgT2VAqKhGj2sRXbjief6UQAAOw=='
ico_app = tk.PhotoImage(data=ico_app_raw)
ico_file_raw = 'R0lGODdhDAAMAHcAACH5BAkKAAAALAAAAAAMAAwAgAAAAAEBAQIXhI+pGh0LnpGJRkbtRDq2XXGY00EmUgAAOw=='
ico_file = tk.PhotoImage(data=ico_file_raw)
ico_folder_raw = 'R0lGODlhDAAMAHcAACH5BAkKAAAALAAAAAAMAAwAgAAAAAEBAQIVhI+pyxuPnjzBVCrvVZp1Z2ViQyoFADs='
ico_folder = tk.PhotoImage(data=ico_folder_raw)

root.iconphoto(False, ico_app)
infotxt.set('tree4eyes r0 ' + __version__[2:])
root.mainloop()

