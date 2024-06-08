from tkinter import *
from PIL import Image as imi, ImageTk
from tkinter import tix
from tkinter import filedialog
from tkinter import messagebox
from tkinter.tix import *
from PIL import ImageGrab
import math
import time
import os

outerPoints = list()
innerPoints = list()
imgPath1 = str()
rootAwake = True
frames = []
mode = {'Mouse': True, 'Select': False, 'Delete': False, 'Ruler': False}
selmode = {'outer': False, 'inner': False}
mouse_pos = (0, 0)
rulerPos = list()
rulerRatio = 0


def CloseRoot(windows):
    global rootAwake
    rootAwake = 0
    windows.destroy()


class rootWindows():
    root = Tk()
    tip = Balloon(root)

    def updatePointConnection(self):
        root.canves.delete('Line')
        temp = 0
        for i in range(len(outerPoints)-1):
            if outerPoints[i] != (-1, -1):
                if temp != 0:
                    root.canves.create_line(outerPoints[i][0], outerPoints[i][1], temp[0],
                                            temp[1], width=2, fill='red', tag='Line')
                    temp = 0
                if outerPoints[i+1] != (-1, -1):
                    root.canves.create_line(outerPoints[i][0],outerPoints[i][1],outerPoints[i+1][0],
                                            outerPoints[i+1][1], width=2, fill='red',tag='Line')
                else:
                    temp = outerPoints[i]
            else: continue
        temp = 0
        for i in range(len(innerPoints)-1):
            if innerPoints[i] != (-1, -1):
                if temp != 0:
                    root.canves.create_line(innerPoints[i][0], innerPoints[i][1], temp[0],
                                            temp[1], width=2, fill='blue', tag='Line')
                    temp = 0
                if innerPoints[i+1] != (-1, -1):
                    root.canves.create_line(innerPoints[i][0],innerPoints[i][1],innerPoints[i+1][0],
                                            innerPoints[i+1][1], width=2, fill='blue',tag='Line')
                else:
                    temp = innerPoints[i]

    def updatePointsCount(self):
        sum_o,sum_i =0,0
        for i in outerPoints:
            if i != (-1,-1):
                sum_o += 1
        for j in innerPoints:
            if j != (-1,-1):
                sum_i += 1
        root.pointsCount_outer_Num.config(text=str(sum_o))
        root.pointsCount_inner_Num.config(text=str(sum_i))

    def updaterulermode(self):
        if not mode['Ruler']:
            root.tool_rulerConfirm.config(state=DISABLED)
            root.tool_rulerConfirm_num.config(state='readonly')
            root.tool_rulerConfirm_num1.config(fg='black')
        else:
            root.tool_rulerConfirm.config(state=ACTIVE)
            root.tool_rulerConfirm_num.config(state=NORMAL)
            root.tool_rulerConfirm_num1.config(fg='lightgreen')

    def updateSelmod(self):
        if selmode['inner']:
            root.sets_select_Inner.config(state=ACTIVE)
        else:
            root.sets_select_Inner.config(state=DISABLED)
        if selmode['outer']:
            root.sets_select_Outer.config(state=ACTIVE)
        else:
            root.sets_select_Outer.config(state=DISABLED)

    def details(self):
        detail = Toplevel()
        detail.geometry("450x250")
        detail.iconbitmap("resource/icon.ico")
        detail.resizable(0, 0)
        location = Label(detail, text="PIC Alpha 0.4.2")
        location.grid(column=0, row=0)

        numIdx = 14  # gif的帧数
        numIdx1 = 23  # gif的帧数
        # 填充14帧内容到frames
        frames = [PhotoImage(file='resource/YFTCM.gif', format='gif -index %i' % i).subsample(4) for i in range(numIdx)]
        frames1 = [PhotoImage(file='resource/CYWL.gif', format='gif -index %i' % i).subsample(4) for i in range(numIdx1)]

        def update(idx):  # 定时器函数
            frame = frames[idx]
            idx += 1  # 下一帧的序号：在0,1,2,3,4,5之间循环(共6帧)
            YCTFM.configure(image=frame)  # 显示当前帧的图片
            detail.after(100, update, idx % numIdx)  # 0.1秒(100毫秒)之后继续执行定时器函数(update)

        def update1(idx1):  # 定时器函数
            frame1 = frames1[idx1]
            idx1 += 1  # 下一帧的序号：在0,1,2,3,4,5之间循环(共6帧)
            CYWL.configure(image=frame1)  # 显示当前帧的图片
            detail.after(100, update1, idx1 % numIdx1)  # 0.1秒(100毫秒)之后继续执行定时器函数(update)

        YCTFM = Label(detail)
        CYWL = Label(detail)
        YCTFM.grid(column=0, row=1)
        CYWL.grid(column=3, row=1)
        detail.after(0, update, 0)  # 立即启动定时器函数(update)
        detail.after(0, update1, 0)  # 立即启动定时器函数(update)
        names = Label(detail, text="Design: Data7\nCaculatonMethod: HY\nProgram: Data7\n DO NOT SPREAD!")
        names.grid(column=1, row=0, rowspan=2)

        detail.mainloop()

    def saveScreen(self):
        # 获取主窗口的位置和大小
        x = root.root.winfo_rootx()
        y = root.root.winfo_rooty()-35
        w = root.root.winfo_width()
        h = root.root.winfo_height()+35

        # 使用ImageGrab模块的grab()函数来进行截图
        screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        # 保存截图为文件
        filename = imgPath1.split('/')[-1]+'_'+str(time.time())+'.png'
        screenshot.save(filename)
        messagebox.showinfo('已保存为','screenshot has been saved as:\n'+filename)
        os.startfile(filename)

    def fileSelect(self):
        global imgPath1
        global rootAwake
        file_types = [('Image Files', '*.png'), ('Image Files', '*.jpg'), ('Image Files', '*.gif'),
                      ('Image Files', '*.ico'), ('Image Files', '*.bmp')]
        imgPath1 = filedialog.askopenfilename(filetypes=file_types)
        # imgPath1='Weixin Image_20240517202826.jpg'
        if imgPath1 != '':
            messagebox.showinfo("已加载图片:", imgPath1)
        if imgPath1 != '':
            print('OPENED:', imgPath1)
            img = imi.open(imgPath1)  # 打开图片
            img = img.resize((500, int(img.height / img.width * 500)))
            photo = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
            root.canves.create_image(0, 0, anchor='nw', image=photo)
            root.root.mainloop()

    def echo(self):
        global imgPath1
        if imgPath1 != '':
            messagebox.showinfo("ChosenImg:", imgPath1)
        else:
            messagebox.showerror("no img Chosen", "no img Chosen")

    def mouse(self):
        root.tool_mouse.config(state=DISABLED)
        root.tool_select.config(state=ACTIVE)
        root.tool_delet.config(state=ACTIVE)
        root.tool_ruler.config(state=ACTIVE)
        root.mode.config(text='MODE: Mouse')
        root.canves.config(cursor='arrow')
        for i in mode:
            mode[i] = False
        mode['Mouse'] = True
        for j in selmode:
            selmode[j] = False
        root.updateSelmod()
        root.updaterulermode()
    def select(self):
        root.tool_mouse.config(state=ACTIVE)
        root.tool_select.config(state=DISABLED)
        root.tool_delet.config(state=ACTIVE)
        root.tool_ruler.config(state=ACTIVE)
        root.mode.config(text='MODE: DrawPoints')
        root.canves.config(cursor='crosshair')
        for i in mode:
            mode[i] = False
        mode['Select'] = True
        for j in selmode:
            selmode[j] = False
        selmode['inner'] = True
        root.updateSelmod()
        root.updaterulermode()
    def delete(self):
        root.tool_mouse.config(state=ACTIVE)
        root.tool_select.config(state=ACTIVE)
        root.tool_delet.config(state=DISABLED)
        root.tool_ruler.config(state=ACTIVE)
        root.mode.config(text='MODE: DeletePoints')
        root.canves.config(cursor='arrow')
        for i in mode:
            mode[i] = False
        mode['Delete'] = True
        for j in selmode:
            selmode[j] = False
        root.updateSelmod()
        root.updaterulermode()
    def ruler(self):
        root.tool_mouse.config(state=ACTIVE)
        root.tool_select.config(state=ACTIVE)
        root.tool_delet.config(state=ACTIVE)
        root.tool_ruler.config(state=DISABLED)
        root.mode.config(text='MODE: DefineRuler')
        root.canves.config(cursor='circle')
        for i in mode:
            mode[i] = False
        mode['Ruler'] = True
        for j in selmode:
            selmode[j] = False
        root.updateSelmod()
        root.updaterulermode()
    def help(self):
        helps = Toplevel()
        helps.iconbitmap("resource/icon.ico")
        # with open("resource/Help.html", "r", encoding="utf-8") as file:
        #     html_content = file.read()
        # frame = tw.HtmlFrame(helps)
        # frame.pack()
        # frame.load_html(html_content)
        # helps.mainloop()
    def selmode_o(self):
        selmode['outer'] = False
        selmode['inner'] = True
        root.updateSelmod()

    def selmode_i(self):
        selmode['outer'] = True
        selmode['inner'] = False
        root.updateSelmod()

    def rulerConfirm(self):
        global rulerRatio
        if root.tool_rulerConfirm_num.get() != '' and root.tool_rulerConfirm_num.get().isdigit() and imgPath1 != '' and len(rulerPos)==2:
            if ((rulerPos[0][0]-rulerPos[1][0])**2+(rulerPos[0][1]-rulerPos[1][1])**2)**0.5 == 0:
                rulerRatio = 0
            else:
                rulerRatio = eval(root.tool_rulerConfirm_num.get())/(((rulerPos[0][0]-rulerPos[1][0])**2+(rulerPos[0][1]-rulerPos[1][1])**2)**0.5)
            root.position.config(text="X: {} | Y: {}\tRuler: 1:{:.2f}mm".format(mouse_pos[0], mouse_pos[1], rulerRatio))
            root.sets_down1_ratio_num.config(text="1:{:.2f}mm".format(rulerRatio))
            # print(((rulerPos[0][0]-rulerPos[1][0])**2+(rulerPos[0][1]-rulerPos[1][1])**2)**0.5)
            # print(rulerRatio)
    def __init__(self):
        root =self.root
        root.geometry("700x450")
        root.title('PIC')
        root.iconbitmap('resource/PIC.ico')
        root.resizable(0, 0)

    # 样式

    upper = Frame(height=30, width=500)
    upper.grid(column=0, row=0, sticky=W, columnspan=2)

    upperDiv2 = Frame(bg="white", height=1, width=500)
    upperDiv2.grid(column=0, row=1, columnspan=2)
    upperDiv = Frame(bg="grey", height=1, width=500)
    upperDiv.grid(column=0, row=2, columnspan=2)
    upperDiv1 = Frame(bg="white", height=1, width=500)
    upperDiv1.grid(column=0, row=3, columnspan=2)

    detail = Button(upper, text="About", command=lambda: rootWindows.details(root), cursor='hand2')
    detail.grid(column=0, row=0, padx=1)

    canves = Canvas(root, width=500, height=300, bg="#E5E5E5", cursor="", highlightbackground="grey",
                    highlightthickness=1)
    canves.grid(column=0, row=4, columnspan=2)

    file = Button(upper, text="Files", command=lambda: rootWindows.fileSelect(root), cursor='hand2')
    file.grid(column=1, row=0, padx=1)

    file1 = Button(upper, text="ChosenImg", command=lambda: rootWindows.echo(root), cursor='hand2')
    file1.grid(column=2, row=0, padx=1)

    file1 = Button(upper, text="Help", command=lambda: rootWindows.help(root), cursor='question_arrow')
    file1.grid(column=3, row=0, padx=1)

    file1 = Button(upper, text="Save(Ctrl+s)", command=lambda: rootWindows.saveScreen(root), cursor='hand2')
    file1.grid(column=4, row=0, padx=1)

    lowerDiv2 = Frame(bg="white", height=1, width=500)
    lowerDiv2.grid(column=0, row=5, columnspan=2)
    lowerDiv = Frame(bg="grey", height=1, width=500)
    lowerDiv.grid(column=0, row=6, columnspan=2)
    lowerDiv1 = Frame(bg="white", height=1, width=500)
    lowerDiv1.grid(column=0, row=7, columnspan=2)

    position = Label(root, text="X: NULL | Y: NULL\tRuler:no ruler defined")
    position.grid(column=0, row=8, sticky=W)

    mode = Label(root, text="MODE: Mouse")
    mode.grid(column=1, row=8, sticky=E)

    tools = Frame(root, height=75, width=500, highlightbackground="grey", highlightthickness=1)
    tools.grid_propagate(False)
    tools.grid(column=0, row=9, columnspan=2, sticky=W)

    tool_title = Label(tools, text='Tools:')
    tool_title.grid(column=0, row=0, pady=3)

    photo = PhotoImage(file="resource/M.png")
    photo = photo.zoom(2, 2)
    # 图片在button的左边
    tool_mouse = Button(tools, text='', image=photo,
                        compound=CENTER, state=DISABLED, command=lambda: rootWindows.mouse(root))
    tip.bind_widget(tool_mouse, balloonmsg="MouseMod")
    tool_mouse.grid(column=0, row=1, padx=1)

    photoS = PhotoImage(file="resource/S.png")
    photoS = photoS.zoom(2, 2)
    # 图片在button的左边
    tool_select = Button(tools, text='', image=photoS,
                         compound=CENTER, state=ACTIVE, command=lambda: rootWindows.select(root))
    tool_select.grid(column=1, row=1, padx=1)
    tip.bind_widget(tool_select, balloonmsg="SelectMod")

    photoD = PhotoImage(file="resource/D.png")
    photoD = photoD.zoom(2, 2)
    # 图片在button的左边
    tool_delet = Button(tools, text='', image=photoD,
                        compound=CENTER, state=ACTIVE, command=lambda: rootWindows.delete(root))
    tip.bind_widget(tool_delet, balloonmsg="DeleteMod")
    tool_delet.grid(column=2, row=1, padx=1)

    photoR = PhotoImage(file="resource/R.png")
    photoR = photoR.zoom(2, 2)
    # 图片在button的左边
    tool_ruler = Button(tools, text='', image=photoR,
                        compound=CENTER, state=ACTIVE, command=lambda: rootWindows.ruler(root))
    tip.bind_widget(tool_ruler, balloonmsg="RulerMod\ndefine a ruler")
    tool_ruler.grid(column=3, row=1, padx=1)

    tool_rulerConfirm = Button(tools, text='Ruler confirm', state=DISABLED,command=lambda: rootWindows.rulerConfirm(root))
    tool_rulerConfirm.grid(column=4, row=1, padx=10)

    tool_rulerConfirm_num = Entry(tools, width=10, state='readonly')
    tool_rulerConfirm_num.grid(column=6, row=1, padx=3)

    tool_rulerConfirm_num1 = Label(tools, text='▶')
    tool_rulerConfirm_num1.grid(column=5, row=1, padx=0)

    tool_rulerConfirm_num2 = Label(tools, text='mm')
    tool_rulerConfirm_num2.grid(column=7, row=1, padx=0)

    middleDiv = Frame(root, height=400, width=1, bg='grey')
    middleDiv.grid(row=0, column=2, rowspan=10, padx=5)

    sets = Frame(root, height=400, width=180)
    sets.grid(row=0, column=3, rowspan=10, sticky=NW)

    pointsCount = Frame(sets, height=55, width=180, highlightbackground="grey", highlightthickness=1)
    pointsCount.grid(column=0, row=1, columnspan=3, sticky=W)
    pointsCount.grid_propagate(False)

    pointsCount_uppertitle = Label(sets, text='SETS:')
    pointsCount_uppertitle.grid(column=0, row=0, columnspan=2, pady=10, sticky=W)

    pointsCount_outer = Label(pointsCount, text='outerCount:')
    pointsCount_outer.grid(column=0, row=0, pady=0, sticky=W)

    pointsCount_outer_Num = Label(pointsCount, text='0')
    pointsCount_outer_Num.grid(column=1, row=0, pady=0, sticky=W)

    pointsCount_inner = Label(pointsCount, text='innerCount:')
    pointsCount_inner.grid(column=0, row=1, pady=0)

    pointsCount_inner_Num = Label(pointsCount, text='0')
    pointsCount_inner_Num.grid(column=1, row=1, pady=0, sticky=W)

    sets_selectDiv = Frame(sets, height=1, width=180, bg='grey')
    sets_selectDiv.grid(column=0, row=3, pady=3, columnspan=2)

    sets_select = Frame(sets, height=30, width=180)
    sets_select.grid(column=0, row=4, columnspan=2)

    sets_select_Outer = Button(sets_select, text='Sel_Outer', state=DISABLED, command=lambda: rootWindows.selmode_o(root))
    sets_select_Outer.grid(column=0, row=0, padx=3)

    sets_select_Inner = Button(sets_select, text='Sel_Inner', state=DISABLED, command=lambda: rootWindows.selmode_i(root))
    sets_select_Inner.grid(column=1, row=0, padx=3)

    sets_down1 = Frame(sets, height=150, width=180, highlightbackground="grey", highlightthickness=1)
    sets_down1.grid(column=0, row=5, pady=5, columnspan=2)
    sets_down1.grid_propagate(False)

    sets_down1_figureLabel = Label(sets_down1,text='Result:',font=('Times',15,'bold'))
    sets_down1_figureLabel.grid(column=0,row=0,pady=1,columnspan=2,sticky=W)

    sets_down1_figurel = Label(sets_down1,text='AVE:',font=('Times',10,'bold'))
    sets_down1_figurel.grid(column=0,row=1,pady=1,sticky=E)

    sets_down1_figurel_num = Label(sets_down1,text='0 mm')
    sets_down1_figurel_num.grid(column=1,row=1,pady=1,sticky=W)

    sets_down1_figure2 = Label(sets_down1,text='Selected:',font=('Times',10,'bold'))
    sets_down1_figure2.grid(column=0,row=2,pady=1,sticky=E)

    sets_down1_figure2_num = Label(sets_down1,text='0 mm')
    sets_down1_figure2_num.grid(column=1,row=2,pady=1,sticky=W)

    sets_down1_ratio = Label(sets_down1,text='Ratio:',font=('Times',10,'bold'))
    sets_down1_ratio.grid(column=0,row=3,pady=1,sticky=E)

    sets_down1_ratio_num = Label(sets_down1,text='noRuler')
    sets_down1_ratio_num.grid(column=1,row=3,pady=1,sticky=W)

    sets_downLog = Frame(sets, height=140, width=180, highlightbackground="grey", highlightthickness=1)
    sets_downLog.grid_propagate(False)
    sets_downLog.grid(column=0, row=6, pady=3, columnspan=2, sticky=W)

    sets_downLog_logTitle = Label(sets_downLog, text='LOGS:')
    sets_downLog_logTitle.grid(column=0, row=0, sticky=W)

    sets_downLog_logs = Label(sets_downLog, text='', wraplength=170, fg="red")
    sets_downLog_logs.grid(column=0, row=1, sticky=W)

    sets_downLog_logs1 = Label(sets_downLog, text='', wraplength=170, fg="#AAAA00")
    sets_downLog_logs1.grid(column=0, row=1, sticky=W)

    sets_downLog_logs2 = Label(sets_downLog, text='>There will be the logs of the program. '
                                                  'Point out what is happening', wraplength=180, fg="blue")
    sets_downLog_logs2.grid(column=0, row=1, sticky=W)


def is_mouse_inside_canvas(event):
    # 获取鼠标相对于窗口的坐标
    x, y = event.x_root, event.y_root
    # 获取Canvas相对于窗口的位置
    canvas_x, canvas_y = root.canves.winfo_rootx(), root.canves.winfo_rooty()
    canvas_width, canvas_height = root.canves.winfo_width(), root.canves.winfo_height()
    # 检查鼠标是否在Canvas内
    return canvas_x <= x <= canvas_x + canvas_width and canvas_y <= y <= canvas_y + canvas_height


def motion(event): # 鼠标移动
    mouse_pos = (event.x, event.y)
    if is_mouse_inside_canvas(event):
        root.position.config(text="X: {} | Y: {}\tRuler: 1:{:.2f}mm".format(mouse_pos[0], mouse_pos[1],rulerRatio))
        if mode['Delete'] and imgPath1 != '':
            if approachPoints(mouse_pos, 3):
                for pos in outerPoints:
                    if approachPoint(mouse_pos, pos, 3):
                        root.canves.create_oval(pos[0] - 7, pos[1] - 7, pos[0] + 7, pos[1] + 7, fill='red', outline='black',
                                                    tag='appoachO')
                for pos1 in innerPoints:
                    if approachPoint(mouse_pos, pos1, 5):
                        root.canves.create_oval(pos1[0] - 7, pos1[1] - 7, pos1[0] + 7, pos1[1] + 7, fill='black',
                                                outline='blue', tag='appoachI')
            else:
                root.canves.delete("appoachO")
                root.canves.delete("appoachI")

        root.canves.delete('templine')
        if mode['Select'] and imgPath1 != '':
            root.canves.delete('lastline')
            if not selmode['outer']:

                if len(innerPoints) != 0:
                    inLastPos = ()
                    for i in reversed(innerPoints):
                        if i == (-1, -1):
                            continue
                        else:
                            inLastPos = i
                            break
                    inFirstPos = ()
                    for i in innerPoints:
                        if i == (-1, -1):
                            continue
                        else:
                            inFirstPos = i
                            break
                    root.canves.create_line(inFirstPos[0], inFirstPos[1], inLastPos[0], inLastPos[1], fill='blue',
                                            width=2, tag='lastline')

                outLastPos = ()
                for i in reversed(outerPoints):
                    if i == (-1,-1): continue
                    else:
                        outLastPos = i
                        break
                if outLastPos != ():
                    root.canves.create_line(mouse_pos[0],mouse_pos[1],outLastPos[0],outLastPos[1], fill='pink', width=2, tag='templine')
                    if len(outerPoints) >= 5:
                        outFirstPos = ()
                        for i in outerPoints:
                            if i == (-1, -1):
                                continue
                            else:
                                outFirstPos= i
                                break
                        root.canves.create_line(mouse_pos[0], mouse_pos[1], outFirstPos[0], outFirstPos[1], fill='pink',
                                                width=2, tag='templine')
            if not selmode['inner']:

                if len(outerPoints) != 0:
                    outLastPos = ()
                    for i in reversed(outerPoints):
                        if i == (-1, -1):
                            continue
                        else:
                            outLastPos = i
                            break
                    outFirstPos = ()
                    for i in outerPoints:
                        if i == (-1, -1):
                            continue
                        else:
                            outFirstPos = i
                            break
                    root.canves.create_line(outFirstPos[0], outFirstPos[1], outLastPos[0], outLastPos[1], fill='red',
                                            width=2, tag='lastline')

                inLastPos = ()
                for i in reversed(innerPoints):
                    if i == (-1,-1): continue
                    else:
                        inLastPos = i
                        break
                if inLastPos != ():
                    root.canves.create_line(mouse_pos[0],mouse_pos[1],inLastPos[0],inLastPos[1], fill='lightblue', width=2, tag='templine')
                    if len(innerPoints) >= 5:
                        inFirstPos = ()
                        for i in innerPoints:
                            if i == (-1, -1):
                                continue
                            else:
                                inFirstPos= i
                                break
                        root.canves.create_line(mouse_pos[0], mouse_pos[1], inFirstPos[0], inFirstPos[1], fill='lightblue',
                                                width=2, tag='templine')
            if not mode['Select']:
                if len(outerPoints) != 0:
                    outLastPos = ()
                    for i in reversed(outerPoints):
                        if i == (-1, -1):
                            continue
                        else:
                            outLastPos = i
                            break
                    outFirstPos = ()
                    for i in outerPoints:
                        if i == (-1, -1):
                            continue
                        else:
                            outFirstPos = i
                            break
                    root.canves.create_line(outFirstPos[0], outFirstPos[1], outLastPos[0], outLastPos[1], fill='red',
                                            width=2, tag='lastline')
    else:
        # 不在画布内
        root.canves.delete('templine')

        if len(outerPoints) != 0:
            outLastPos = ()
            for i in reversed(outerPoints):
                if i == (-1, -1):
                    continue
                else:
                    outLastPos = i
                    break
            outFirstPos = ()
            for i in outerPoints:
                if i == (-1, -1):
                    continue
                else:
                    outFirstPos = i
                    break
            root.canves.create_line(outFirstPos[0], outFirstPos[1], outLastPos[0], outLastPos[1], fill='red',
                                    width=2, tag='lastline')

        if len(innerPoints) != 0:
            inLastPos = ()
            for i in reversed(innerPoints):
                if i == (-1, -1):
                    continue
                else:
                    inLastPos = i
                    break
            inFirstPos = ()
            for i in innerPoints:
                if i == (-1, -1):
                    continue
                else:
                    inFirstPos = i
                    break
            root.canves.create_line(inFirstPos[0], inFirstPos[1], inLastPos[0], inLastPos[1], fill='blue',
                                    width=2, tag='lastline')
def click(event):  # 鼠标点击
    # print("O:",outerPoints,'\n','I:',innerPoints)
    drawOuterPoints((event.x,event.y), event)
    drawinnerPoints((event.x,event.y), event)
    mouse_pos = (event.x, event.y)
    if is_mouse_inside_canvas(event) and mode['Delete']:
        if approachPoints(mouse_pos, 5):
            i = 0
            for pos in outerPoints:
                if approachPoint(mouse_pos, pos, 3):
                    root.canves.delete('outerPoints'+str(i))
                    outerPoints[i] = (-1, -1)
                i += 1
            i = 0
            for pos1 in innerPoints:
                if approachPoint(mouse_pos, pos1, 3):
                    root.canves.delete('innerPoints'+str(i))
                    innerPoints[i] = (-1, -1)
                i += 1
            root.canves.delete("appoachO")
            root.canves.delete("appoachI")
            root.updatePointsCount()
            root.updatePointConnection()
    if is_mouse_inside_canvas(event) and mode['Ruler']:
        drawRulerPoints((event.x,event.y))

def drawRulerPoints(pos):
    x,y = pos
    if imgPath1 != '' and len(rulerPos) < 2:
        # root.canves.create_rectangle(x - 2, y - 2, x + 2, y + 2, fill='purple', outline='purple',
        #                          tag='ruler1')
        rulerPos.append(pos)
    elif imgPath1 != '' and len(rulerPos) >= 2:
        rulerPos[0] = rulerPos[1]
        rulerPos[1] = pos
    #update
    root.canves.delete('ruler')
    if len(rulerPos)>=1:
        root.canves.create_rectangle(rulerPos[0][0] - 2, rulerPos[0][1] - 2,
                                 rulerPos[0][0] + 2, rulerPos[0][1] + 2, fill='purple', outline='purple',tag='ruler')
        if len(rulerPos)==2:
            root.canves.create_rectangle(rulerPos[1][0] - 2, rulerPos[1][1] - 2,
                                 rulerPos[1][0] + 2, rulerPos[1][1] + 2, fill='purple', outline='purple',
                                 tag='ruler')
            root.canves.create_line(rulerPos[0],rulerPos[1],width=2,fill='purple',tag='ruler')
    # print(rulerPos)
def drawOuterPoints(pos, event):
    x,y = pos
    if is_mouse_inside_canvas(event) and drawable(pos, 7) and imgPath1 != '' and not selmode['outer'] and mode['Select']:
        outerPoints.append((pos[0], pos[1]))
        root.canves.create_rectangle(x - 2, y - 2, x + 2, y + 2, fill='red', outline='red',
                                     tag='outerPoints'+str(len(outerPoints)-1))
        # print('outer:',outerPoints)
    root.updatePointsCount()
    root.updatePointConnection()

def drawinnerPoints(pos, event):
    x, y = pos
    if is_mouse_inside_canvas(event) and drawable(pos, 7) and imgPath1 != '' and not selmode['inner'] and mode['Select']:
        innerPoints.append((pos[0], pos[1]))
        root.canves.create_rectangle(x - 2, y - 2, x + 2, y + 2, fill='blue', outline='blue',
                                     tag='innerPoints'+str(len(innerPoints)-1))
        # print('inner:',innerPoints)
        root.updatePointsCount()
        root.updatePointConnection()

def drawable(nowPoint,r):
    for i in outerPoints:
        if ((i[0]-nowPoint[0])**2+(i[1]-nowPoint[1])**2)**0.5 <= r:
            return False
    for j in innerPoints:
        if ((j[0]-nowPoint[0])**2+(j[1]-nowPoint[1])**2)**0.5 <= r:
            return False
    return True

def approachPoints(nowPoint,r):
    for i in outerPoints:
        if ((i[0]-nowPoint[0])**2+(i[1]-nowPoint[1])**2)**0.5 <= r:
            return True
    for j in innerPoints:
        if ((j[0]-nowPoint[0])**2+(j[1]-nowPoint[1])**2)**0.5 <= r:
            return True
    return False

def approachPoint(nowPoint,Point,r):
    if ((Point[0]-nowPoint[0])**2+(Point[1]-nowPoint[1])**2)**0.5 <= r:
        return True
    if ((Point[0]-nowPoint[0])**2+(Point[1]-nowPoint[1])**2)**0.5 <= r:
        return True
    return False

if __name__ == '__main__':
    # rootWindowsInit() -> root
    root = rootWindows()
    imgb = imi.open('resource/BP.png')  # 打开图片
    imgb = imgb.resize((500, int(imgb.height / imgb.width * 500)))
    photo = ImageTk.PhotoImage(imgb)  # 用PIL模块的PhotoImage打开
    root.canves.create_image(0, 0, anchor='nw', image=photo)
    root.root.protocol('WM_DELETE_WINDOW', lambda: CloseRoot(root.root))
    # getMouseMotion()
    root.root.bind("<Motion>", motion)
    root.root.bind("<Button-1>", click)
    root.root.bind("<Control-s>", lambda event: rootWindows.saveScreen(root))
    # drawPoints()
    # caculations()

    mainloop()