import tkinter as ttk
import tkinter.messagebox as tkmsg

EAN13 = {
    0 : "LLLLLLRRRRRR",
    1 : "LLGLGGRRRRRR",
    2 : "LLGGLGRRRRRR",
    3 : "LLGGGLRRRRRR",
    4 : "LGLLGGRRRRRR",
    5 : "LGGLLGRRRRRR",
    6 : "LGGGLLRRRRRR",
    7 : "LGLGLGRRRRRR",
    8 : "LGLGGLRRRRRR",
    9 : "LGGLGLRRRRRR",
}

LEncoding = {
    0 : "0001101",
    1 : "0011001",
    2 : "0010011",
    3 : "0111101",
    4 : "0100011",
    5 : "0110001",
    6 : "0101111",
    7 : "0111011",
    8 : "0110111",
    9 : "0001011",
}

GEncoding = {
    0 : "0100111",
    1 : "0110011",
    2 : "0011011",
    3 : "0100001",
    4 : "0011101",
    5 : "0111001",
    6 : "0000101",
    7 : "0010001",
    8 : "0001001",
    9 : "0010111",
}

REncoding = {
    0 : "1110010",
    1 : "1100110",
    2 : "1101100",
    3 : "1000010",
    4 : "1011100",
    5 : "1001110",
    6 : "1010000",
    7 : "1000100",
    8 : "1001000",
    9 : "1110100",
}

class MainWindow(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.bind("<Return>", self.submit)
        self.pack()
        self.widgets()

    def widgets(self):
        self.label_file_name = ttk.Label(self, text="Save barcode to PS File [eg : EAN13.eps]").grid(row=0, column=1)
        self.label_enter_code = ttk.Label(self, text="Enter Code (first 12 decimal digits)").grid(row=2, column=1)

        self.file_name = ttk.StringVar()
        self.label_input_file_name = ttk.Entry(self, textvariable=self.file_name)
        self.label_input_file_name.grid(row=1, column=1)

        self.code_value = ttk.StringVar()
        self.label_input_code_value = ttk.Entry(self, textvariable=self.code_value)
        self.label_input_code_value.grid(row=3, column=1)

        self.canvas = ttk.Canvas(self, width=400, height=400, bg="white")
        self.canvas.grid(row=5, column=1)

        self.canvas.create_text(200,20,text="EAN-13 Barcode:",fill="black")

    def check_filename(self):
        if self.file_name.get()[-4:] == ".eps":
            return True

    def check_code(self):
        if len(self.code_value.get()) == 12 and self.code_value.get().isdigit():
            return True

    def draw_SME(self, x, y0, y1, space):
        self.canvas.create_rectangle(x, y0, x+space, y1, fill = "blue", outline="blue")
        x += space
        self.canvas.create_rectangle(x, y0, x+space, y1, fill = "white", outline="white")
        x += space
        self.canvas.create_rectangle(x, y0, x+space, y1, fill = "blue", outline="blue")
        x += space

        return x


    def submit(self, event):
        if not self.check_filename():
            tkmsg.showerror(title="Invalid input", message="Please enter correct file name")
        elif not self.check_code():
            tkmsg.showerror(title="Invalid input", message="Please enter correct input code")
        else:
            x = 60
            space = 3
            index = 0

            binary_code, number = self.get_barcode()
            first_group = binary_code[:42]
            last_group = binary_code[-42:]

            x = self.draw_SME(x, 230, 80, space)
            self.canvas.create_text(x-20,250, text=number[index], font=("Arial", 20, "bold"))
            index += 1

            count = 0
            for i in first_group:
                if int(i) == 1:
                    self.canvas.create_rectangle(x, 220, x+space, 80, fill = "black")
                    x += space
                    count += 1
                else:
                    self.canvas.create_rectangle(x, 220, x+space, 80, fill = "white", outline="white")
                    x += space
                    count += 1

                if count % 7 == 0:
                    self.canvas.create_text(x-10,250, text=number[index], font=("Arial", 20, "bold"))
                    index += 1


            # create long rectangle on start
            self.canvas.create_rectangle(x, 230, x+space, 80, fill = "white", outline="white")
            x += space
            self.canvas.create_rectangle(x, 230, x+space, 80, fill = "blue", outline="blue")
            x += space
            self.canvas.create_rectangle(x, 230, x+space, 80, fill = "white", outline="white")
            x += space
            self.canvas.create_rectangle(x, 230, x+space, 80, fill = "blue", outline="blue")
            x += space
            self.canvas.create_rectangle(x, 230, x+space, 80, fill = "white", outline="white")
            x += space

            count = 0

            for i in last_group:
                if int(i) == 1:
                    self.canvas.create_rectangle(x, 220, x+space, 80, fill = "black")
                    x += space
                    count += 1
                else:
                    self.canvas.create_rectangle(x, 220, x+space, 80, fill = "white", outline="white")
                    x += space
                    count += 1

                if count % 7 == 0:
                    self.canvas.create_text(x-10,250, text=number[index], font=("Arial", 20, "bold")) 
                    index += 1

            x = self.draw_SME(x, 230, 80, space)

            self.canvas.create_text(200,280, text="Check Digit : "+ str(self.get_check_digit()), font=("Times New Roman", 20, "bold"), fill='orange')
            self.export_to_eps()
            

    def export_to_eps(self):
        self.canvas.postscript(file=self.file_name.get(), colormode="color")

    def get_check_digit(self):
        sum_code_genap = 0
        sum_code_ganjil = 0
        check_digit = 0
        index = 1

        # Loop 12 times
        while index <= 12:
            if index % 2 == 0:
                sum_code_genap += int(self.code_value.get()[(index - 1)])
            else:
                sum_code_ganjil += int(self.code_value.get()[(index - 1)])
            index += 1

        # calculate total
        total = (sum_code_genap * 3) + sum_code_ganjil
        mod_10 = total % 10
        if mod_10 != 0:
            check_digit = 10 - mod_10
        else:
            check_digit = mod_10

        return check_digit

    def get_barcode(self):
        angka = self.code_value.get()+str(self.get_check_digit())

        structure = EAN13[int(angka[0])]
        binary_result = ""

        for i in range(1, len(angka)):
            if structure[i - 1] == "L":
                binary_result += LEncoding[int(angka[i])]
            elif structure[i - 1] == "R":
                binary_result += REncoding[int(angka[i])]
            elif structure[i - 1] == "G":
                binary_result += GEncoding[int(angka[i])]

        return binary_result, angka

if__name__ = "__main__"
myapp = MainWindow()
myapp.master.geometry("500x500")
myapp.master.title("EAN-13 ")
myapp.master.mainloop()