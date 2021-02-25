#from tkinter import *
import tkinter
import winreg
import ctypes
import sys
import shutil
import os

# Reg DB [(good_name, key, sub_key, value_name, value),...]
version = "0.04a"
window_x = 460
window_y = 350
db = [
    ("Capslock dauerhaft deaktivieren (Neustart erforderlich)",
        winreg.HKEY_LOCAL_MACHINE,
        "SYSTEM\\CurrentControlSet\\Control\\Keyboard Layout",
        "Scancode Map",
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00:\x00\x00\x00\x00\x00'),

    ("'Mit Notepad öffnen' als Shell-Option",
        winreg.HKEY_CLASSES_ROOT,
        "*\\shell",
        "*\\shell\\Mit Notepad öffnen\\command",
        'notepad %1'),


    ("In 'Dieser PC'\nangezeigte Objekte",
        winreg.HKEY_LOCAL_MACHINE,
        "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\MyComputer\\NameSpace\\",
        "Bilder",       "{24ad3ad4-a569-4530-98e1-ab02f9417aa8}",
        "3D-Objekte",   "{0DB7E03F-FC29-4DC6-9020-FF41B59E513A}",
        "Videos",       "{f86fa3ab-70d2-4fc7-9c99-fcbf05467f3a}",
        "Musik",        "{3dfdf296-dbec-4fb4-81d1-6a3438bcf4de}",
        "Desktop",      "{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}",
        "Dokumente",    "{d3162b92-9365-467a-956b-92703aca08af}",
        "Downloads",    "{088e3905-0323-4b02-9826-5d99428e115f}",
        "Unbekannt 1",  "{1CF1260C-4DD0-4ebb-811F-33C572699FDE}",
        "Unbekannt 2",  "{374DE290-123F-4565-9164-39C4925E467B}",
        "Unbekannt 3",  "{3ADD1653-EB32-4cb0-BBD7-DFA0ABB5ACCA}",
        "Unbekannt 4",  "{A0953C92-50DC-43bf-BE83-3742FED03C9C}",
        "Unbekannt 5",  "{A8CDFF1C-4878-43be-B5FD-F8091C1C60D0}"),

    ("Verknüpungspfeile entfernen (Neustart erforderlich)",
     winreg.HKEY_LOCAL_MACHINE,
     "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer",
     "Shell Icons",
     "%windir%\\Blank.ico,0",
     "29"),

    ("'Acryleffekt' vom Sperrbildschirm entfernen (ab 1903)",
     winreg.HKEY_LOCAL_MACHINE,
     "SOFTWARE\\Policies\\Microsoft\\Windows\\System",
     "DisableAcrylicBackgroundOnLogon",
     "1"),

    ("MS-Update Speicherreservierung ausschalten (ab 1903)",
     winreg.HKEY_LOCAL_MACHINE,
     "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ReserveManager",
     "ShippedWithReserves",
     "0"),

    ("Spacing der Desktop Icons zurücksetzen",
     winreg.HKEY_CURRENT_USER,
     "Control Panel\\Desktop\\WindowMetrics",
     "IconSpacing",
     "-1725"
     )
    ]
# Admin Check
lpParameters = ""
for i, item in enumerate(sys.argv[0:]):
    lpParameters += '"' + item + '" '
if ctypes.windll.shell32.IsUserAnAdmin() == 1:
    root = Tk()
    #ctypes.windll.shcore.SetProcessDpiAwareness(1)
    #root.tk.call('tk', 'scaling', 2)
    root.resizable(height=False, width=False)
    # Fensterposition
    res = []
    for r in range(0, 2):
        res.append(ctypes.windll.user32.GetSystemMetrics(r))
    root.geometry('%dx%d+%d+%d' % (window_x,
                                   window_y,
                                   (res[0] - window_x) / 2,
                                   (res[1] - window_y) / 2))
    # print(root.winfo_screenwidth(), root.winfo_screenheight())
    root.wm_title("RegPy " + version)

    class Application(Frame):
        def __init__(self, master=None):

            Frame.__init__(self, master)
            Frame(root,
                  height=130,
                  bd=2,
                  width=window_x - 5,
                  relief=GROOVE
                  ).grid(
                  padx=3,
                  columnspan=4,
                  rowspan=3,
                  sticky=W)

    # Angezeigte Objekte in 'Dieser PC
            Label(text=db[2][0]).grid(column=0,
                                      row=0,
                                      padx=5,
                                      pady=10,
                                      rowspan=2
                                      )

            def bilder_setter():
                entry = winreg.OpenKey(db[2][1],
                                       db[2][2],
                                       0,
                                       winreg.KEY_ALL_ACCESS)
                if bilder_var.get() == 1:
                    winreg.CreateKey(entry, db[2][4])
                else:
                    winreg.DeleteKey(entry, db[2][4])
                entry.Close()

            bilder_var = IntVar()
            try:
                winreg.QueryInfoKey(winreg.OpenKey(db[2][1],
                                                   db[2][2] + db[2][4],
                                                   0))
                bilder_var.set(1)
            except FileNotFoundError:
                bilder_var.set(0)
            self.chk_bilder = Checkbutton(root,
                                          text=db[2][3],
                                          var=bilder_var,
                                          command=bilder_setter)
            self.chk_bilder.grid(row=0,
                                 column=1,
                                 padx=0,
                                 sticky=W)

            def obj3d_setter():
                entry = winreg.OpenKey(db[2][1],
                                       db[2][2],
                                       0,
                                       winreg.KEY_ALL_ACCESS)
                if obj3d_var.get() == 1:
                    winreg.CreateKey(entry, db[2][6])
                else:
                    winreg.DeleteKey(entry, db[2][6])
                entry.Close()

            obj3d_var = IntVar()
            try:
                winreg.QueryInfoKey(winreg.OpenKey(db[2][1],
                                                   db[2][2] + db[2][6],
                                                   0))
                obj3d_var.set(1)
            except FileNotFoundError:
                obj3d_var.set(0)
            self.chk_obj3d = Checkbutton(root,
                                         text=db[2][5],
                                         var=obj3d_var,
                                         command=obj3d_setter)
            self.chk_obj3d.grid(row=0,
                                column=2,
                                padx=0,
                                sticky=W)

            def videos_setter():
                entry = winreg.OpenKey(db[2][1],
                                       db[2][2],
                                       0,
                                       winreg.KEY_ALL_ACCESS)
                if videos_var.get() == 1:
                    winreg.CreateKey(entry, db[2][8])
                else:
                    winreg.DeleteKey(entry, db[2][8])
                entry.Close()

            videos_var = IntVar()
            try:
                winreg.QueryInfoKey(winreg.OpenKey(db[2][1],
                                                   db[2][2] + db[2][8],
                                                   0))
                videos_var.set(1)
            except FileNotFoundError:
                videos_var.set(0)
            self.chk_videos = Checkbutton(root,
                                          text=db[2][7],
                                          var=videos_var,
                                          command=videos_setter)
            self.chk_videos.grid(row=0,
                                 column=3,
                                 padx=0,
                                 sticky=W)

            def musik_setter():
                entry = winreg.OpenKey(db[2][1],
                                       db[2][2],
                                       0,
                                       winreg.KEY_ALL_ACCESS)
                if musik_var.get() == 1:
                    winreg.CreateKey(entry, db[2][10])
                else:
                    winreg.DeleteKey(entry, db[2][10])
                entry.Close()

            musik_var = IntVar()
            try:
                winreg.QueryInfoKey(winreg.OpenKey(db[2][1],
                                                   db[2][2] + db[2][10],
                                                   0))
                musik_var.set(1)
            except FileNotFoundError:
                musik_var.set(0)
            self.chk_musik = Checkbutton(root,
                                         text=db[2][9],
                                         var=musik_var,
                                         command=musik_setter)
            self.chk_musik.grid(row=1,
                                column=1,
                                padx=0,
                                sticky=W)

            def desktop_setter():
                entry = winreg.OpenKey(db[2][1],
                                       db[2][2],
                                       0,
                                       winreg.KEY_ALL_ACCESS)
                if desktop_var.get() == 1:
                    winreg.CreateKey(entry, db[2][12])
                else:
                    winreg.DeleteKey(entry, db[2][12])
                entry.Close()

            desktop_var = IntVar()
            try:
                winreg.QueryInfoKey(winreg.OpenKey(db[2][1],
                                                   db[2][2] + db[2][12],
                                                   0))
                desktop_var.set(1)
            except FileNotFoundError:
                desktop_var.set(0)
            self.chk_desktop = Checkbutton(root,
                                           text=db[2][11],
                                           var=desktop_var,
                                           command=desktop_setter)
            self.chk_desktop.grid(row=1,
                                  column=2,
                                  padx=0,
                                  sticky=W)

            def doku_setter():
                entry = winreg.OpenKey(db[2][1],
                                       db[2][2],
                                       0,
                                       winreg.KEY_ALL_ACCESS)
                if doku_var.get() == 1:
                    winreg.CreateKey(entry, db[2][14])
                else:
                    winreg.DeleteKey(entry, db[2][14])
                entry.Close()

            doku_var = IntVar()
            try:
                winreg.QueryInfoKey(winreg.OpenKey(db[2][1],
                                                   db[2][2] + db[2][14],
                                                   0))
                doku_var.set(1)
            except FileNotFoundError:
                doku_var.set(0)
            self.chk_doku = Checkbutton(root,
                                        text=db[2][13],
                                        var=doku_var,
                                        command=doku_setter)
            self.chk_doku.grid(row=1,
                               column=3,
                               padx=0,
                               sticky=W)

            def dl_setter():
                entry = winreg.OpenKey(db[2][1],
                                       db[2][2],
                                       0,
                                       winreg.KEY_ALL_ACCESS)
                if dl_var.get() == 1:
                    winreg.CreateKey(entry, db[2][16])
                else:
                    winreg.DeleteKey(entry, db[2][16])
                entry.Close()

            dl_var = IntVar()
            try:
                winreg.QueryInfoKey(winreg.OpenKey(db[2][1],
                                                   db[2][2] + db[2][16],
                                                   0))
                dl_var.set(1)
            except FileNotFoundError:
                dl_var.set(0)
            self.chk_dl = Checkbutton(root,
                                      text=db[2][15],
                                      var=dl_var,
                                      command=dl_setter)
            self.chk_dl.grid(row=2,
                             column=1,
                             padx=0,
                             sticky=W)

            Label(root, text="Allgemein").grid(column=0, row=3)

    # Capslock dauerhaft deaktivieren
            capslock_var = IntVar()

            def capslock_setter():
                entry = winreg.OpenKey(db[0][1],
                                       db[0][2],
                                       0,
                                       winreg.KEY_ALL_ACCESS)
                if capslock_var.get() == 1:
                    winreg.SetValueEx(entry,
                                      db[0][3],
                                      0,
                                      3,
                                      db[0][4])
                if capslock_var.get() == 0:
                    winreg.DeleteValue(entry, db[0][3])
                entry.Close()

            try:
                winreg.QueryValueEx(winreg.OpenKey(db[0][1],
                                                   db[0][2],
                                                   0), "Scancode Map")
                capslock_var.set(1)
            except FileNotFoundError:
                capslock_var.set(0)
            self.chk_capslock = Checkbutton(root,
                                            text=db[0][0],
                                            var=capslock_var,
                                            command=capslock_setter)
            self.chk_capslock.grid(column=1,
                                   columnspan=3,
                                   padx=0,
                                   row=3,
                                   sticky=W)

    # 'Mit Notepad öffnen' als Shell-Option
            notepad_var = IntVar()

            def notepad_setter():
                if notepad_var.get() == 1:
                    winreg.CreateKey(db[1][1], db[1][3])
                    entry = winreg.OpenKey(db[1][1],
                                           db[1][3],
                                           0,
                                           winreg.KEY_ALL_ACCESS)
                    winreg.SetValueEx(entry, None, 0, winreg.REG_SZ, db[1][4])
                elif notepad_var.get() == 0:
                    entry = winreg.OpenKey(db[1][1],
                                           db[1][2],
                                           0,
                                           winreg.KEY_ALL_ACCESS)
                    winreg.DeleteKey(entry, "Mit Notepad öffnen\\command")
                    winreg.DeleteKey(entry, "Mit Notepad öffnen")
                entry.Close()
            try:
                winreg.QueryInfoKey(winreg.OpenKey(db[1][1],
                                                   "*\\shell\\Mit Notepad öffnen",
                                                   0))
                notepad_var.set(1)
            except FileNotFoundError:
                notepad_var.set(0)
            self.chk_notepad = Checkbutton(root,
                                           text=db[1][0],
                                           var=notepad_var,
                                           command=notepad_setter)
            self.chk_notepad.grid(column=1,
                                  columnspan=3,
                                  padx=0,
                                  sticky=W)

    # Verknüpungspfeile Entfernen
            sca_var = IntVar()

            def sca_setter():
                entry = winreg.OpenKey(db[3][1],
                                       db[3][2],
                                       0,
                                       winreg.KEY_ALL_ACCESS)

                if sca_var.get() == 1:
                    winreg.CreateKey(entry, db[3][3])
                    entry = winreg.OpenKey(entry,
                                           db[3][3],
                                           0,
                                           winreg.KEY_ALL_ACCESS)
                    winreg.SetValueEx(entry, db[3][5], 0, winreg.REG_SZ, db[3][4])
                    shutil.copyfile("blank.ico", "c:\\windows\\blank.ico")
                elif sca_var.get() == 0:
                    winreg.DeleteKey(entry, db[3][3])
                    os.remove("C:\\windows\\blank.ico")
                entry.Close()
            if os.path.isfile("C:\\windows\\blank.ico") is True:
                try:
                    winreg.QueryValueEx(winreg.OpenKey(db[3][1], "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Icons", 0), db[3][5])
                    sca_var.set(1)
                except FileNotFoundError:
                    sca_var.set(0)
            else:
                pass
            self.chk_sca = Checkbutton(root,
                                       text=db[3][0],
                                       var=sca_var,
                                       command=sca_setter)
            self.chk_sca.grid(column=1,
                              columnspan=3,
                              sticky=W)

    # Entferne 'Edit with IDLE' aus Shell
            #idle_var = IntVar()

            def idle_setter():

                def delRegtree(e):

                    entry = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, e, 0, winreg.KEY_ALL_ACCESS)
                    while winreg.QueryInfoKey(entry)[0] > 0:
                        sub_key = winreg.EnumKey(entry, 0)
                        #num_sub = winreg.QueryInfoKey(entry)
                        for x in range(0, 1):
                            try:
                                winreg.DeleteKey(entry, sub_key)
                                entry = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, e, 0, winreg.KEY_ALL_ACCESS)
                            except PermissionError:
                                entry = winreg.OpenKey(entry, sub_key)
                                continue
                            except OSError:
                                entry = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, e, 0, winreg.KEY_ALL_ACCESS)
                                continue
                    entry.Close()
                if 'editwithidle' in a[0]:
                    delRegtree("Python.File\\Shell\\")
                if 'editwithidle' in a[1]:
                    delRegtree("Python.NoConFile\\Shell\\")
                self.chk_idle.configure(state=DISABLED)

            try:
                a = [[], []]
                for x in range(0, winreg.QueryInfoKey(winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "Python.File\\Shell", 0))[0]):
                    a[0].append(winreg.EnumKey(winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "Python.File\\Shell", 0), x))
                for x in range(0, winreg.QueryInfoKey(winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "Python.NoConFile\\Shell", 0))[0]):
                    a[1].append(winreg.EnumKey(winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "Python.NoConFile\\Shell", 0), x))
                if "editwithidle" not in a[0] and "editwithidle" not in a[1]:
                    raise FileNotFoundError
                else:
                    self.chk_idle = Checkbutton(root, text="'Edit with IDLE' aus Shell entfernen", command=idle_setter)
            except FileNotFoundError:
                self.chk_idle = Checkbutton(root, text="'Edit with IDLE' aus Shell entfernen", state=DISABLED, command=idle_setter)
            self.chk_idle.grid(column=1, columnspan=3, padx=0, sticky=W)

    # Entferne Anmeldebildschirm-Blur
            blur_var = IntVar()

            def blur_setter():
                entry = winreg.OpenKey(db[4][1], db[4][2], 0, winreg.KEY_ALL_ACCESS)
                if blur_var.get() == 1:
                    winreg.SetValueEx(entry, db[4][3], 0, winreg.REG_SZ, db[4][4])
                elif blur_var.get() == 0:
                    winreg.DeleteValue(entry, db[4][3])
                entry.Close()

            try:
                winreg.QueryValueEx(winreg.OpenKey(db[4][1], db[4][2], 0), db[4][3])
                blur_var.set(1)
            except FileNotFoundError:
                blur_var.set(0)

            self.chk_blur = Checkbutton(root, text=db[4][0], var=blur_var, command=blur_setter)
            self.chk_blur.grid(column=1, columnspan=3, sticky=W)

    # Entferne Update-Speicherreservierung

            reserve_var = IntVar()

            def reserve_setter():
                entry = winreg.OpenKey(db[5][1], db[5][2], 0, winreg.KEY_ALL_ACCESS)
                if reserve_var.get() == 1:
                    winreg.SetValueEx(entry, db[5][3], 0, winreg.REG_DWORD, 0)
                elif reserve_var.get() == 0:
                    winreg.SetValueEx(entry, db[5][3], 0, winreg.REG_DWORD,1)
                entry.Close()

            if winreg.QueryValueEx(winreg.OpenKey(db[5][1], db[5][2], 0), db[5][3])[0] == 1:
                reserve_var.set(0)
            else:
                reserve_var.set(1)

            self.chk_reserve = Checkbutton(root, text=db[5][0], var=reserve_var, command=reserve_setter)
            self.chk_reserve.grid(column=1, columnspan=3, sticky=W)

    # Icon Spacing auf dem Desktop Zurücksetzen

            ispace_var = IntVar()

            def ispace_setter():
                entry = winreg.OpenKey(db[6][1],
                                       db[6][2],
                                       0,
                                       winreg.KEY_ALL_ACCESS)
                winreg.SetValueEx(entry, db[6][3],
                                  0,
                                  winreg.REG_SZ,
                                  db[6][5])
                entry.Close()
                self.chk_ispace.configure(state=DISABLED)

            if winreg.QueryValueEx(winreg.OpenKey(db[6][1], db[6][2], 0), db[6][3])[0] != "-1725":
                ispace_var.set(0)
                self.chk_ispace = Checkbutton(root, text=db[6][0], var=ispace_var, command=ispace_setter)
            else:
                self.chk_ispace = Checkbutton(root, text=db[6][0], var=ispace_var, state=DISABLED)
            self.chk_ispace.grid(column=1, columnspan=3, sticky=W)

            Button(root, text="Schließen", command=self.quit, width=20, height=2).grid(column=2, columnspan=3, padx=4, sticky=SE)

    app = Application(master=root)
    app.mainloop()

else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, lpParameters, None, 1)