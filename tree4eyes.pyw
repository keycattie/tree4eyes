# tree4eyes r0
__version__ = 'r0v0.1-dev.pooling.1'

import logging as log
import os
import time
import base64
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font


class WinASCIITree:
    def __init__(self, path, info: tk.StringVar = None, progress: tk.StringVar = None):
        log.info(f'New tree for \"{path}\"')
        self.path = path
        self.info = info
        self.progress = progress
        if self.info:
            self.info.set('Opening Windows ASCII Tree file')
        else:
            log.warning('No info updates')
        if self.progress:
            self.progress.set('')
        else:
            log.warning('No progress updates')
        self.file = open(self.path, 'r')
        if not self.file: 
            log.error('File opening failed')
            if self.progress:
                self.progress.set("Failed!")
            raise EOFError(f'Empty or inexistent file, path: \"{self.path}\"')
        self.dmap = self.build()
        self.root = 0


    def build(self):
        _fsize = os.path.getsize(self.path)
        _stime = time.time() 
        log.info(f'Building folder map for \"{self.path}\" size {(_fsize / 1024):.2f}kB')

        _updi = 0.1
        if self.info:
            self.info.set('Building folder database')
        if self.progress:
            self.progress.set('0.00')
        _updt = time.time()

        self.file.seek(0, 0)
        self.file.readline() # header skipping
        self.file.readline()
        self.file.readline()

        cid = self.file.tell() - 1
        self.start = cid
        ids = [cid]
        prev = ''
        dmap = dict()
        for line in self.file.readlines():
            cid += len(prev.encode('utf-8')) + 1
            if self._levelcheck(line, len(ids) - 1) == -1:
                ids = ids[:self._level(line)]
            if self._levelcheck(line, len(ids) - 1) == 2:
                if not ids[-1] in dmap:
                    dmap[ids[-1]] = list([])
                dmap[ids[-1]].append(cid)
                ids.append(cid)
            prev = line

            if self.progress:
                if time.time() - _updt > _updi:
                    self.progress.set(f"{(cid / _fsize * 100):.2f}")
                    _updt += _updi

        if self.progress:
            self.progress.set('Done')

        _stime = time.time() - _stime
        log.info(f'Folder map length {len(dmap)} for \"{self.path}\" starting at \
{self.start} done in {(_stime * 1000):.2f}ms, {(_fsize / _stime / 1024):.2f}kB/s')

        return dmap


    def seek(self, iid):
        _stime = time.time() 
        log.info(f'Seeking iid {iid} in \"{self.path}\"')

        _updi = 0.1
        _siid = iid
        _lastd = iid
        _lastf = 0

        items = []
        if iid in self.dmap:
            if self.info:
                self.info.set('Loading folders')
            if self.progress:
                self.progress.set('0.00')
            _updt = time.time()
            _lastd = self.dmap[iid][-1]
            _lastf = self.dmap[iid][0]

            for d in self.dmap[iid]:
                self.file.seek(int(d), 0)
                line = self.file.readline()
                lv = self._level(line)
                line = line[(4 * lv):-1]
                if self._levelcheck(self.file.readline(), lv) == -1:
                    items.append((d, line, True, False))
                else:
                    items.append((d, line, True, True))

                if time.time() - _updt > _updi:
                    if self.progress:
                        self.progress.set(f"{((d - iid) / (_lastd - iid) * 100):.2f}")
                    _updt += _updi
        _stime = time.time() - _stime 
        log.info(f'Seeked {len(items)} folders in {(_stime * 1000):.2f}ms')
        _stime = time.time() 

        _updf = _lastd != _siid
        _updt = time.time()
        if self.info:
            self.info.set('Loading files')
        if self.progress:
            if _updf:
                self.progress.set('0.00')
            else: 
                self.progress.set('Unknown') # TODO file progress when no folders

        self.file.seek(int(iid), 0)
        line = self.file.readline()
        last = line
        slv = self._level(line)
        while True:
            iid += len(last.encode('utf-8')) + 1
            line = self.file.readline()
            if not line:
                break
            lv = self._levelcheck(line, slv)
            if (lv == -1) or (lv == 2):
                break
            if ((len(line) - 1) - (4 * (slv + 1)) == 0):
                last = line
                continue
            last = line
            line = line[(4 * (slv + 1)):-1]
            items.append((iid, line, False, False))

            if self.progress:
                if time.time() - _updt > _updi:
                    if _updf:
                        self.progress.set(f"{((iid - _siid) / (_lastf - _siid) * 100):.2f}")
                    _updt += _updi
           
        if self.progress:     
            self.progress.set('Done')
        _stime = time.time() - _stime 
        log.info(f'Seeked {len(items)} files in {(_stime * 1000):.2f}ms')

        return items


    def _level(self, s):
        l = 0
        while s.startswith(('|   ', '    '), l * 4):
            l += 1
        if s.startswith(('+---', '\---'), l * 4):
            l += 1
        return l


    def _levelcheck(self, s, l):
        if s.startswith(('|   ', '    '), l * 4):
            return 0 # inside or file
        elif s.startswith(('+---', '\---'), l * 4):
            return 2 # folder
        return -1 # outside


class t4i(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        parent.title('tree4eyes')
        parent.geometry('400x500')
        ico_app_raw = 'R0lGODdhEAAQAMQAAAAAAAAAAB8fHzg4OEBAQICAgOPj4+bm5tvb2/////Ly8nh4eJ6ennh4eHh4eMLCwpaWlr29vWFhYU2JZQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAkKAAAALAAAAAAQABAAAAVD4CSOZGkGaGCS6DAIKVoGxZEUwRHFZG0rMVXvQGQsYANZyXdYQBjKiVDkQzAYs9UpqmV1pcGvSDjdKstZ7yw1ZotLIQA7'
        self.ico_app = tk.PhotoImage(data=ico_app_raw)
        parent.iconphoto(False, self.ico_app)
        parent.protocol('WM_DELETE_WINDOW', self.cleanup)  # needed coz shutdown hangs for large trees

        self.infotxt = tk.StringVar()
        self.progtxt = tk.StringVar()

        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open...", underline=0, command=self.open_WinASCIITree_th)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", underline=1, command=self.quit)
        self.menubar.add_cascade(label="File", underline=0, menu=self.filemenu)
        parent.config(menu=self.menubar)

        self.bar = tk.Frame(self)
        self.l_infotxt=tk.Label(self.bar, textvariable=self.infotxt, anchor=tk.W)
        self.l_progtxt=tk.Label(self.bar, textvariable=self.progtxt, anchor=tk.E)
        self.l_infotxt.pack(side=tk.LEFT)
        self.l_progtxt.pack(side=tk.RIGHT)
        self.bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.tree = ttk.Treeview(self, show='tree', yscrollcommand=self.scrollbar.set)
        ldfont = font.nametofont("TkDefaultFont").copy()
        ldfont.config(weight=tk.font.BOLD, underline=1)
        self.tree.tag_configure('ld', font=ldfont)
        dirfont = font.nametofont("TkDefaultFont").copy()
        dirfont.config(weight=tk.font.BOLD)
        self.tree.tag_configure('dir', font=dirfont)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.config(command=self.tree.yview)

        self.rmenu = tk.Menu(self.tree, tearoff=0)
        self.rmenu.add_command(label='Copy path', command=self.copypath)
        self.tree.bind('<Button-3>', self.rmenu_raise)
        self.tree.bind('<<TreeviewOpen>>', self.treeload_th)

        ico_file_raw = 'R0lGODdhDAAMAHcAACH5BAkKAAAALAAAAAAMAAwAgAAAAAEBAQIXhI+pGh0LnpGJRkbtRDq2XXGY00EmUgAAOw=='
        self.ico_file = tk.PhotoImage(data=ico_file_raw)
        ico_folder_raw = 'R0lGODdhDAAMAIAAAAAAAAEBASH5BAkKAAAALAAAAAAMAAwAAAIVhI+pGt3rApApTuZutZij+GzeQpYFADs='
        self.ico_folder = tk.PhotoImage(data=ico_folder_raw)

        self.infotxt.set('tree4eyes r0')
        self.progtxt.set(__version__[2:])

        self.dummycount = 1
        self.cached = []
        self.cachelim = 25


    def open_WinASCIITree_th(self):
        thread = threading.Thread(target=self.open_WinASCIITree)
        thread.start()


    def open_WinASCIITree(self):
        log.info('Opening new file')
        self.infotxt.set('Opening file...')
        path = filedialog.askopenfilename(filetypes=((('Text files'), '*.txt'), (('All files'), '*.*')))
        if path:
            self.codec = WinASCIITree(path, info=self.infotxt, progress=self.progtxt)
            self.tree.delete(*self.tree.get_children())
            self.expand('')
        else:
            log.info('Opening file canceled')
            self.infotxt.set('Opening file canceled')


    def treeload_th(self, event):
        thread = threading.Thread(target=self.treeload(event))
        thread.start()


    def treeload(self, event):
        try:
            piid = self.tree.selection()[0]
            if not self.tree.tag_has('ld', piid) and self.tree.tag_has('dir', piid) \
                and self.tree.get_children(piid):
                    self.infotxt.set('Loading file structure...')
                    log.info('Loading file structure')
                    self.expand(piid)
                    self.cached.append(piid)
                    self.tree.delete(self.tree.get_children(piid)[0])
                    self.tree.item(piid, tags=('ld', 'dir', ))

                    if len(self.cached) >= self.cachelim:
                        for iid in self.cached:
                            if self.tree.item(iid)['open'] == False:
                                for c in self.tree.get_children(self.cached[0]):
                                    self.tree.delete
                                self.tree.insert(iid, tk.END, text='/...', iid=-self.dummycount, open=False)
                                self.tree.item(iid, tags=('dir', ))
                                self.dummycount += 1
                                self.cached.remove(iid)
                                log.info(f'Uncached item {iid}')
                                break
        except:
            self.infotxt.set('Loading file structure failed')
            log.info('Loading file structure failed')


    def expand(self, spiid):
        piid = self.codec.start
        if spiid != '': 
            piid = int(spiid)
        log.info(f'Populating tree at {piid}')
        for c in self.codec.seek(piid):
            if c[2]:
                self.tree.insert(spiid, tk.END, text=c[1], image=self.ico_folder, iid=c[0], open=False)
                self.tree.item(c[0], tags=('dir', ))
                if c[3]:
                    self.tree.insert(c[0], tk.END, text='/...', iid=-self.dummycount, open=False)
                    self.dummycount += 1
            else:
                self.tree.insert(spiid, tk.END, text=c[1], image=self.ico_file, iid=c[0], open=False)
        return


    def rmenu_raise(self, event):
        try:
            iid = self.tree.identify_row(event.y)
            if iid:
                self.tree.selection_set(iid)
            self.rmenu.tk_popup(event.x_root, event.y_root)
        finally:
            self.rmenu.grab_release()

            
    def copypath(self):
        if not self.tree.selection():
            return
        item_iid = self.tree.selection()[0]
        parent_iid = self.tree.parent(item_iid)
        s = self.tree.item(item_iid)['text']
        while parent_iid:
            s = self.tree.item(parent_iid)['text'] + '\\' + s
            parent_iid = self.tree.parent(parent_iid)
        self.clipboard_clear()
        self.clipboard_append(s)
        self.infotxt.set('Path copied')
        self.progtxt.set('')
        log.info(f'Path copied \"{s}\"')
        return


    def cleanup(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.parent.destroy()
        return


if __name__ == "__main__":
    log.basicConfig(level=log.DEBUG, format='%(lineno)d %(levelname)s: %(message)s')    
    log.info(f'Started tree4eyes {__version__}')

    root = tk.Tk()
    t4i(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

