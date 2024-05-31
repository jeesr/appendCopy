import keyboard  
import pyperclip  
import time  
import tkinter as tk  
from tkinter import ttk  
from tkinter import messagebox  
from threading import Thread 
root = tk.Tk()
root.withdraw() 
# 用来记录上一个 Ctrl+C 按下时间  
last_ctrl_c_time = None  
# 用来记录 Ctrl+C 被按下的次数  
ctrl_c_count = 0  
delimiter = ''
content = ''  
contents = []  
# 设置两次 Ctrl+C 之间的时间间隔阈值（毫秒）  
DOUBLE_PRESS_THRESHOLD = 800  # 例如，800毫秒  
label2 = []
def on_ctrl_c():  
    global last_ctrl_c_time, ctrl_c_count, content  
    current_time = time.time()  
  
    # 如果上次 Ctrl+C 按下时间不为空，并且当前时间与上次时间之差小于阈值  
    if last_ctrl_c_time and (current_time - last_ctrl_c_time) < DOUBLE_PRESS_THRESHOLD / 1000:  
        ctrl_c_count += 1  
        if ctrl_c_count >= 2:  # 如果在阈值内连续按下了两次或更多次
            content = content + delimiter + pyperclip.paste() if content else pyperclip.paste() 
            time.sleep(0.02)  # 稍微等待以确保剪贴板内容已更新  
            pyperclip.copy(content) # 更新剪贴板内容 
            # 重置计数器，因为我们已经处理了一次“双击”事件 
            ctrl_c_count = 0  
    else:  
        # 如果超过时间阈值或第一次按下，重置计数器 
        ctrl_c_count = 1  
    contents.append(pyperclip.paste())
    # 更新上次 Ctrl+C 按下时间  
    last_ctrl_c_time = current_time  

    time.sleep(0.01)
    for i in range(99,0,-1):
        label2[i].config(text=label2[i-1].cget('text'))
    label2[0].config(text=pyperclip.paste())
    
def on_ctrl_v(): 
    global content
    content = ''
  
def on_ctrl_shift_v(): 
    root.deiconify()
    root.focus_set()
  


# Tkinter窗口的类  
class App:  
    def __init__(self, master):  
        self.master = master  
        master.title("追加复制")  
        master.geometry("500x350") 
     
        self.options_values = [   
            {"value": "", "label": "无"},    
            {"value": " ", "label": "空格"},    
            {"value": "\t", "label": "制表符"},    
            {"value": "\n", "label": "换行符"},    
            {"value": "、", "label": "顿号"},    
            {"value": ",", "label": "逗号(英文)"},    
            {"value": "，", "label": "逗号(中文)"}   
        ]
        self.options = [option["label"] for option in self.options_values] 
        self.selected_separator = tk.StringVar(value=self.options[0])  # 默认值设为"无"
       
        self.frame1 = tk.Frame(master,width=500,height=70)
        self.frame1.grid(row=0, column=0, sticky="wn")
         # 禁止Frame根据内部内容自动调整大小
        self.frame1.grid_propagate(False)
        # 创建一个标签，用于说明下拉菜单的作用
        label = ttk.Label(self.frame1, text="追加复制：按住CTRL快速按两次C，选择间隔符:")
        label.grid(row=0, column=0, padx=5, pady=10)

        # 创建OptionMenu下拉菜单
        def change_option(*args): #解构成元组
            self.selected_separator.set(args[0])
            label_to_value = {option["label"]: option["value"] for option in self.options_values}
            global delimiter
            delimiter = label_to_value[args[0]]
            #print(f"选择了: {label_to_value[val]}")
    
        separator_menu = ttk.OptionMenu(self.frame1, self.selected_separator, self.options[0],*self.options,command = change_option)
        separator_menu.grid(row=0, column=1)

        labeljl = ttk.Label(self.frame1, text="复制记录：")
        labeljl.grid(row=1, column=0, padx=5, pady=5,sticky='nw')
        labelcg = ttk.Label(self.frame1, text="")
        labelcg.grid(row=1, column=0, padx=5, pady=5,sticky='ne')

        self.canvas = tk.Canvas(master,width=500,height=300)
        self.canvas.grid(row=1, column=0, columnspan=1, sticky="nsew")
        self.canvas.grid_propagate(False)
        # 创建Scrollbar并与Canvas的滚动功能绑定
        self.scrollbar = ttk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=1, column=1, sticky="nse")

        # 配置Canvas的滚动区域并绑定Scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # 创建一个Frame，该Frame将放置于Canvas内并作为滚动内容
        self.frame = tk.Frame(self.canvas,width=500, height=300)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
    
        # 绑定鼠标滚轮事件
        self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(-1 * (event.delta // 120), "units"))
        
        def copy_text(event):
            textC = event.widget.winfo_children()[0]
            text_to_copy = textC.cget("text")  # 获取Text组件的文本内容（去除首尾的空白）  
            if text_to_copy:  # 如果文本不为空  
                pyperclip.copy(text_to_copy)  # 复制到剪贴板  
                #messagebox.showinfo("复制成功", "文本已复制到剪贴板")
                labelcg.config(text="复制成功")
                root.after(1000,lambda:labelcg.config(text=""))
        
       

        def create_textboxes():  
            textbox_counter = 1
            for i in range(0, 100):  
                frame = tk.Frame(self.frame, width=400, height=80, bg='white') 
                frame.bind("<Button-1>", copy_text)
                frame.grid_propagate(False) #不自适应
                global label2
                txt = tk.Label(frame, text='', bg='white')
                label2.append(txt)
                label2[i].grid(row=0, column=0,padx=1, pady=1, sticky='nw')
                frame.grid(row=1+textbox_counter, column=0, padx=5, pady=5, sticky='nw')   
                textbox_counter += 1  
        create_textboxes() 
        master.grid_columnconfigure(0, weight=1) #第一列和第一行占据所有剩余空间
        master.grid_rowconfigure(1, weight=1)

# 使用线程来运行keyboard的监听，以避免阻塞tkinter的事件循环 
def start_keyboard_listener():  
    keyboard.add_hotkey('ctrl+c', on_ctrl_c)  
    keyboard.add_hotkey('ctrl+v', on_ctrl_v)  
    keyboard.add_hotkey('ctrl+shift+f', on_ctrl_shift_v)  
    # keyboard.wait('esc')  # 监听直到按下esc键  

listener_thread = Thread(target=start_keyboard_listener)
listener_thread.start()

# 创建Tkinter窗口实例并运行  
root = tk.Tk()  
app = App(root)  
root.mainloop()  
  
# 当tkinter窗口关闭时，确保keyboard的监听也被停止  
# 注意：由于keyboard库没有直接的停止监听方法，你可能需要设置一个标志来在on_ctrl_c中检查  
# 或者使用其他机制来优雅地停止监听，例如捕获窗口关闭事件并发送一个信号给keyboard监听线程