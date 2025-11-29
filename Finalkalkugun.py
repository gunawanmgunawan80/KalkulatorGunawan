import tkinter as tk

class SimpleCalculator:
    def __init__(self, root, theme_color):
        self.root = root
        self.theme_color = theme_color

        self.current_value = "0"
        self.tokens = []             
        self.expression_text = ""     
        self.should_reset_display = False

        # Display atas
        self.expression_label = tk.Label(
            root,
            text="",
            bg="#000000",
            fg="#8AF27C",
            font=("Arial", 28),
            anchor="e"
        )
        self.expression_label.pack(fill=tk.X, padx=20, pady=(20,5))

        # Display bawah
        self.display_frame = tk.Frame(root, bg="#000000", height=150)
        self.display_frame.pack(fill=tk.X, padx=10, pady=10)
        self.display_frame.pack_propagate(False)

        self.result_label = tk.Label(
            self.display_frame,
            text="0",
            bg="#000000",
            fg="white",
            font=("Arial", 40, "bold"),
            anchor="e"
        )
        self.result_label.pack(fill=tk.X, padx=50, pady=(5, 10))

        # Tombol
        self.buttons_frame = tk.Frame(root, bg="#000000")
        self.buttons_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        button_layout = [
            ["C", "⌫", "%", "÷"],
            ["7", "8", "9", "x"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["0", "", ".", "="]
        ]

        for r, row in enumerate(button_layout):
            for c, val in enumerate(row):
                if val != "":
                    self.create_button(val, r, c)
                    
    # Membuat tombol
    def create_button(self, text, row, col):
        if text in ["÷", "x", "−", "+"]:
            bg_color = "#A5A5A5"
            fg_color = "#000000"
        elif text in ["C", "⌫", "%"]:
            bg_color = "#A5A5A5"
            fg_color = "#000000"
        elif text == "=":
            bg_color = "#4CD964"
            fg_color = "#000000"
        else:
            bg_color = "#000000"
            fg_color = "#FFFFFF"

        btn = tk.Button(
            self.buttons_frame,
            text=text,
            font=("Arial", 20, "bold"),
            bg=bg_color,
            fg=fg_color,
            activebackground="#555555",
            border=0,
            command=lambda: self.button_click(text)
        )

        if text == "0":
            btn.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=5, pady=5)
        else:
            btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

        self.buttons_frame.grid_rowconfigure(row, weight=1)
        self.buttons_frame.grid_columnconfigure(col, weight=1)
        
    # Input tombol
    def button_click(self, text):
        if text.isdigit() or text == ".":
            self.append_number(text)
        elif text in ["÷", "x", "−", "+"]:
            self.add_operator(text)
        elif text == "=":
            self.calculate()
        elif text == "C":
            self.clear()
        elif text == "⌫":
            self.delete_last()
        elif text == "%":
            self.percent()

    # Update display
    def update_display(self):
        self.result_label.config(text=self.current_value)
        self.expression_label.config(text=self.expression_text)

    # Tambah angka display atas berurutan
    def append_number(self, num):
        if self.should_reset_display:
            self.current_value = num
            self.should_reset_display = False
        else:
            if self.current_value == "0":
                self.current_value = num
            else:
                self.current_value += num

        self.expression_text += num
        self.update_display()

    # Tambah operator ke token
    def add_operator(self, op):
        # masukkan angka terakhir ke token
        self.tokens.append(self.current_value)

        # masukkan operator
        self.tokens.append(op)

        self.expression_text += " " + op + " "

        self.should_reset_display = True
        self.update_display()

    # prioritas operator
    def evaluate_tokens(self, tokens):
        if not tokens:
            return "0"

        # STEP 1: selesaikan x dan ÷ terlebih dahulu
        high = []
        i = 0
        while i < len(tokens):
            if tokens[i] in ["x", "÷"]:
                op = tokens[i]
                prev = float(high.pop())
                nxt = float(tokens[i+1])

                if op == "x":
                    high.append(prev * nxt)
                elif op == "÷":
                    high.append(prev / nxt if nxt != 0 else 0)

                i += 2
            else:
                high.append(tokens[i])
                i += 1

        # STEP 2: selesaikan + dan −
        result = float(high[0])
        i = 1
        while i < len(high):
            op = high[i]
            val = float(high[i+1])

            if op == "+":
                result += val
            elif op == "−":
                result -= val

            i += 2

        return result

    # Tombol sama dengan
    def calculate(self):
        self.tokens.append(self.current_value)

        result = self.evaluate_tokens(self.tokens)

        self.current_value = self.format_number(result)

        self.expression_text = self.current_value
        self.tokens = []
        self.should_reset_display = True
        self.update_display()

    # Utility (tombol lainnya)
    def percent(self):
        try:
            num = float(self.current_value) / 100
            self.current_value = self.format_number(num)
            self.expression_text = self.current_value
            self.update_display()
        except:
            pass

    def clear(self):
        self.current_value = "0"
        self.tokens = []
        self.expression_text = ""
        self.should_reset_display = False
        self.update_display()

    def delete_last(self):
        if len(self.current_value) > 1:
            self.current_value = self.current_value[:-1]
            self.expression_text = self.expression_text[:-1]
        else:
            self.current_value = "0"
        self.update_display()

    def format_number(self, num):
        s = ('{:.3f}'.format(num)).rstrip("0").rstrip(".")
        return s if s != "" else "0"


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Kalkulator Gunawan")
    root.geometry("350x550")
    root.config(bg="#000000")
    root.resizable(True, True)
    calc = SimpleCalculator(root, theme_color="#000000")
    root.mainloop()
