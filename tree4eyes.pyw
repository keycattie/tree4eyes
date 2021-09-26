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
from tkinter import font


def _level(s):
    l = 0
    while s.startswith(('|   ', '    '), l * 4):
        l += 1
    if s.startswith(('+---', '\---'), l * 4):
        l += 1
    return l


def _levelcheck(s, l):
    if s.startswith(('|   ', '    '), l * 4):
        return 0 # inside or file
    elif s.startswith(('+---', '\---'), l * 4):
        return 2 # folder
    return -1 # outside


def seektree(file, iid):
    items = []
    if iid in dmap:
        for d in dmap[iid]:
            file.seek(int(d), 0)
            line = file.readline()
            line = line[(4 * _level(line)):-1]
            items.append((d, line, True))

    file.seek(int(iid), 0)
    line = file.readline()
    last = line
    slv = _level(line)
    while True:
        iid += len(last.encode('utf-8')) + 1
        line = file.readline()
        if not line:
            break
        lv = _levelcheck(line, slv)
        if (lv == -1) or (lv == 2):
            break
        if ((len(line) - 1) - (4 * (slv + 1)) == 0):
            last = line
            continue
        last = line
        line = line[(4 * (slv + 1)):-1]
        items.append((iid, line, False))
    return items


def opentree():
    global file, tr, dmap
    try:
        bt_open.configure(state='disabled')

        file_path = filedialog.askopenfilename(filetypes=((('Text files'), '*.txt'), (('All files'), '*.*')))
        if not file_path:
            return

        infotxt.set('Loading tree file...')
        root.update_idletasks()
        tree.delete(*tree.get_children())
        file = open(file_path, 'r')
        iid = 1
        file.readline()
        file.readline()
        path = file.readline()
        sk = file.tell()
        tree.insert('', tk.END, text='root', values=('Dir'), iid=0, open=True, tags=('ld', ))

        dmap = dict()
        cid = sk - 1
        ids = [0]
        lv = 0
        lt = -1
        prev = ''
        for line in file.readlines():
            cid += len(prev.encode('utf-8')) + 1
            if _levelcheck(line, len(ids) - 1) == -1:
                ids = ids[:_level(line)]
            if _levelcheck(line, len(ids) - 1) == 2:
                if not ids[-1] in dmap:
                    dmap[ids[-1]] = list([])
                dmap[ids[-1]].append(cid)
                ids.append(cid)
            prev = line

        treelevel(0)

        infotxt.set('File successfully loaded')
    except Exception as e:
        # tree.delete(*tree.get_children()) # TODO do i need this???
        infotxt.set('An error occurred loading the file')
        root.update_idletasks()
        messagebox.showerror('Open file failed', f'{type(e).__name__}\n{e}')
    finally: 
        bt_open.configure(state='normal')


def treelevel(piid):
    global dummycount, tr, file
    for c in seektree(file, int(piid)):
        if c[2]:
            tree.insert(piid, tk.END, text=c[1], values=('Dir'), image=ico_folder, iid=c[0], open=False)
            tree.insert(c[0], tk.END, text='/...', iid=-dummycount, open=False)
            dummycount += 1
        else:
            tree.insert(piid, tk.END, text=c[1], values=('File'), image=ico_file, iid=c[0], open=False)
    bt_open.configure(state='normal')
    return


def treeexpand(event):
    infotxt.set('Loading file structure...')
    root.update_idletasks()
    try:
        piid = tree.selection()[0]
        if not tree.tag_has('ld', piid):
            treelevel(piid)
            tree.delete(tree.get_children(piid)[0])
            tree.item(piid, tags=('ld', ))
    finally:
        infotxt.set('')
        root.update_idletasks()


def rmenu_raise(event):
    try:
        iid = tree.identify_row(event.y)
        if iid:
            tree.selection_set(iid)
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
file = None
dmap = None
dummycount = 2

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
columns = ('Type', )
tree = ttk.Treeview(root, columns=columns, show='tree headings', \
    displaycolumns=('Type'), yscrollcommand=scrollbar.set)
tree.column('#0', stretch=tk.YES)
tree.column('Type', stretch=tk.NO, width=32)
ldfont = font.nametofont("TkDefaultFont").copy()
ldfont.config(underline=1)
tree.tag_configure('ld', font=ldfont)
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

