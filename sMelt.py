import re
from tkinter import filedialog
from tkinter import *


root = Tk()

# initiate global variables for displaying info
layer_count = IntVar()
layer_count.set(0)
tool_display = StringVar()
tool_display.set("\n\n\n\n\n")
extruder_inputs = IntVar()
extruder_inputs.set(4) # 2,3,4
affected_tool = StringVar()
affected_tool.set("T0") # T0,T1,T2...
effect_type = StringVar()
effect_type.set("blend") # blend,effect
unit_type = StringVar()
unit_type.set("percent") # percent layerNumber
percent_change_start = IntVar()
percent_change_start.set(0)
percent_change_end = IntVar()
percent_change_end.set(100)
layer_change_start = IntVar()
layer_change_start.set(0)
layer_change_end = IntVar()
layer_change_end.set(1000)
blend_values = StringVar()
blend_values.set("100,0,0,0")
rotation_order = StringVar()
rotation_order.set("abcd")
extruder_start = IntVar()
extruder_start.set(0)
extruder_end = IntVar()
extruder_end.set(100)
change_rate = IntVar()
change_rate.set(4)
effect_modifier = StringVar()
effect_modifier.set("normal")
rate_modifier = StringVar()
rate_modifier.set("normal")

class Tool:
    def __init__(self, id, start, end):
        self.id = id
        self.start = start
        self.end = end
    

class Actions:
    data = []
    tools = []
    current_layer = 0

    @staticmethod
    def open_file():
        Actions.tools=[] #reset tools
        file = filedialog.askopenfilename(filetypes=(("GCODE files", "*.gcode"), ("All files", "*.*")))
        with open(file, 'r', encoding='utf-8') as the_file:
            Actions.data = the_file.read().strip().split("\n")
        Actions.load_data()
        print("File has been opened")

    @staticmethod
    def load_data():
        index = 0
        # tools = []
        # current_layer = -1

        for line in Actions.data:
            if ";LAYER_COUNT:" in line:
                # FINDING THE ACTUAL AFFECTED LAYERS
                layer_count.set(float(line[(line.index(':') + 1): len(line)]))
            elif "T" in line and ";" not in line and "M" not in line:
                
                current_t = int(line[(line.index('T') + 1): len(line)]) #update current tool
                
            elif ";LAYER" in line:
                Actions.current_layer = (int(line[(line.index(':') + 1): len(line)])) # update current layer

                if len(Actions.tools) == 0:
                    Actions.tools.append(Tool(current_t,Actions.current_layer,Actions.current_layer))

                for t, tool in enumerate(Actions.tools):# NOTE there is maybe a but that tool zero doesnt get updated
                    if tool.id == current_t:
                        tool.end = Actions.current_layer
                        break
                    elif t == len(Actions.tools)-1: #if at the end of options and still hasnt been found create one
                        Actions.tools.append(Tool(current_t,Actions.current_layer,Actions.current_layer))
                #need to know what layers those tools start and end on
                #use this to update the current layer
            
        print("Data within file has been loaded")

        #print out the final tools values
        tools_to_display = "Tools \n"
        for tool in Actions.tools: # NOTE (for i, tool in enumerate(Actions.tools):)
            tools_to_display += ("T") + str(tool.id) +(" Start:")+ str(tool.start) +(" End:")+ str(tool.end) +(" ")
            tools_to_display += "\n"
        tool_display.set(tools_to_display)
            

    @staticmethod
    def modify_data():
        base_input = [0] * extruder_inputs.get()
        base_input[0] = 1

        index = 0
        for line in Actions.data:
            modified_gcode = ""
            
            if ";LAYER:" in line:
                modified_gcode += line + " ;Layer Found\n"
            elif "T" in line:
                modified_gcode += line + ";Tool Found\n" 
            else:
                modified_gcode += line + ";Everything" + "\n"
            Actions.data[index] = modified_gcode
            index += 1
        print("File has been modified")
        

    @staticmethod
    def save_file():
        file = filedialog.asksaveasfile(mode='w', defaultextension=".gcode")
        if file is None:
            return
        for item in Actions.data:
            file.write("%s" % item)

        file.close()
        print("File has been Saved")

    @staticmethod
    def button_click():
        print("click!")

class Window(Frame):
    def __init__(self, root=None):
        Frame.__init__(self, root)
        self.root = root
        self.init_window()

    def init_window(self):
        self.grid(row=0, column=0)

        menu = Menu(self.root)
        self.root.config(menu=menu)

        file = Menu(menu)
        menu.add_cascade(label="File", menu=file)
        file.add_command(label="Open", command=Actions.open_file)
        file.add_command(label="Save", command=Actions.save_file)
        file.add_command(label="Exit", command=exit)

        options = Menu(menu)
        menu.add_cascade(label="Options", menu=options)
        options.add_command(label="Modify", command=Actions.modify_data)

        r=0
        # Display Info
        Label(root, text="Layer Count", fg="DarkGreen", bg="White").grid(row=r, column=0)
        Label(root, textvariable=layer_count, fg="DarkGreen", bg="White").grid(row=r, column=1)
        
        r+=5
        Label(root, textvariable=tool_display, fg="DarkGreen", bg="White").grid(row=r, column=4)
        r+=5

        Label(root,text="Extruder Inputs", fg="DarkBlue", bg="White").grid(row=r, column=0)
        OptionMenu(root, extruder_inputs, "2", "3", "4").grid(row=r,column=1)
        Label(root,textvariable=extruder_inputs, fg="DarkBlue", bg="White").grid(row=r, column=2)
        r+=1
        Label(root,text="Affected Tool", fg="DarkBlue", bg="White").grid(row=r, column=0)
        OptionMenu(root, affected_tool, "T0", "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8").grid(row=r,column=1)
        Label(root,textvariable=affected_tool, fg="DarkBlue", bg="White").grid(row=r, column=2)

        
        r+=1
        Label(root,text="Effect Type", fg="DarkBlue", bg="White").grid(row=r, column=0)
        OptionMenu(root, effect_type, "blend", "effect").grid(row=r,column=1)
        Label(root,textvariable=effect_type, fg="DarkBlue", bg="White").grid(row=r, column=2)
        r+=1
        Label(root,text="Unit Type", fg="DarkBlue", bg="White").grid(row=r, column=0)
        OptionMenu(root, unit_type, "percent", "layer_no").grid(row=r,column=1)
        Label(root,textvariable=unit_type, fg="DarkBlue", bg="White").grid(row=r, column=2)
        r+=1
        Label(root,text="Percent Change Start", fg="DarkBlue", bg="White").grid(row=r, column=0)
        Spinbox(root, from_=0, to=100, textvariable=percent_change_start).grid(row=r,column=1)
        Label(root,textvariable=percent_change_start, fg="DarkBlue", bg="White").grid(row=r, column=2)
        r+=1
        Label(root,text="Percent Change End", fg="DarkBlue", bg="White").grid(row=r, column=0)
        Spinbox(root, from_=0, to=100, textvariable=percent_change_end).grid(row=r,column=1)
        Label(root,textvariable=percent_change_end, fg="DarkBlue", bg="White").grid(row=r, column=2)
        r+=1
        Label(root,text="Layer Change Start", fg="DarkBlue", bg="White").grid(row=r, column=0)
        Spinbox(root, from_=0, to=100, textvariable=layer_change_start).grid(row=r,column=1)
        Label(root,textvariable=layer_change_start, fg="DarkBlue", bg="White").grid(row=r, column=2)
        r+=1
        Label(root,text="Layer Change End", fg="DarkBlue", bg="White").grid(row=r, column=0)
        Spinbox(root, from_=0, to=100, textvariable=layer_change_end).grid(row=r,column=1)
        Label(root,textvariable=layer_change_end, fg="DarkBlue", bg="White").grid(row=r, column=2)
        r+=1
        Label(root,text="Blend Values", fg="DarkBlue", bg="White").grid(row=r, column=0)
        Entry(root,textvariable=blend_values).grid(row=r,column=1)
        Label(root,textvariable=blend_values, fg="DarkBlue", bg="White").grid(row=r, column=2)
        r+=1
        Label(root,text="Rotation Order", fg="DarkBlue", bg="White").grid(row=r, column=0)
        Entry(root,textvariable=rotation_order).grid(row=r,column=1)
        Label(root,textvariable=rotation_order, fg="DarkBlue", bg="White").grid(row=r, column=2)
        r+=1
        Label(root,text="Extruder % Start Clamp", fg="DarkBlue", bg="White").grid(row=r, column=0)
        Spinbox(root, from_=0, to=100, textvariable=extruder_start).grid(row=r,column=1)
        Label(root,textvariable=extruder_start, fg="DarkBlue", bg="White").grid(row=r, column=2)
        r+=1
        Label(root,text="Extruder % End Clamp", fg="DarkBlue", bg="White").grid(row=r, column=0)
        Spinbox(root, from_=0, to=100, textvariable=extruder_end).grid(row=r,column=1)
        Label(root,textvariable=extruder_end, fg="DarkBlue", bg="White").grid(row=r, column=2)
        r+=1
        Label(root,text="Change Rate", fg="DarkBlue", bg="White").grid(row=r, column=0)
        Spinbox(root, from_=0, to=100, textvariable=change_rate).grid(row=r,column=1)
        Label(root,textvariable=change_rate, fg="DarkBlue", bg="White").grid(row=r, column=2)
        r+=1
        Label(root,text="Effect Modifier", fg="DarkBlue", bg="White").grid(row=r, column=0)
        OptionMenu(root, effect_modifier, "normal", "wood", "random").grid(row=r,column=1)
        Label(root,textvariable=effect_modifier, fg="DarkBlue", bg="White").grid(row=r, column=2)
        r+=1
        Label(root,text="Rate Modifier", fg="DarkBlue", bg="White").grid(row=r, column=0)
        OptionMenu(root, rate_modifier, "normal", "random").grid(row=r,column=1)
        Label(root,textvariable=rate_modifier, fg="DarkBlue", bg="White").grid(row=r, column=2)
        r+=1

        r+=1
        button_open = Button(root, text="Open", command=Actions.open_file)
        button_open.grid(row=r,column=0)
        r+=1
        button_modify = Button(root, text="Modify", command=Actions.modify_data)
        button_modify.grid(row=r,column=0)
        r+=1
        button_save = Button(root, text="Save", command=Actions.save_file)
        button_save.grid(row=r,column=0)
        

    @staticmethod
    def display():
        vertical_scrollbar = Scrollbar(root)
        vertical_scrollbar.pack(side=RIGHT, fill=Y)
        T = Text(root, height=800, width=600, yscrollcommand=vertical_scrollbar.set)
        T.grid(side=LEFT, fill=BOTH, expand=TRUE)
        vertical_scrollbar.config(command=T.yview, orient=VERTICAL)
    

# The window info
root.title("sMELT (standalone Multi Extruder Layering Tool)")
root.geometry("1200x800")
app = Window(root)
root.mainloop()

