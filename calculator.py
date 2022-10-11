import tkinter as tk

class Calculator(tk.Tk):
    # Stałe zmienne konfiguracyjne 
    COLOR_A = "#424F52"
    COLOR_B = "#D4E6EA"
    COLOR_C = "#A9CAD1"
    COLOR_D = "#004554"
    COLOR_E = "#80999E"
    COLOR_WHITE = "#FFFFFF"
    SMALL_FONT_STYLE = "Arial", 16
    MEDIUM_FONT_STYLE = "Arial", 24, "bold"
    BTN_FONT_STYLE = "Arial", 24
    ERASE_FONT_STYLE = "Arial", 16
    LARGE_FONT_STYLE = "Arial", 40, "bold"

    def __init__(self):
        super().__init__()
        self.geometry("350x650")
        self.resizable(0, 0)
        self.title("Kalkulator")
        
        self.equation = ""
        self.current = ""
        
        self.display_frame = self.create_display_frame()
        self.equation_lbl, self.current_lbl = self.create_display_labels()
        
        self.numbers = {
            7: (1, 1), 8: (1, 2), 9:(1,3),
            4: (2, 1), 5: (2, 2), 6:(2,3),
            1: (3, 1), 2: (3, 2), 3:(3,3),
            0: (4, 2), ".": (4, 1)
        }
        
        self.operators = {
           "/": "\u00F7",
           "*": "\u00D7",
           "-": "-",
           "+": "+"
        }
        
        self.buttons_frame = self.create_buttons_frame()
        
        # Konfiguracja kolumn. Ustawienie szerokości kolumn i wierszy na 1
        self.buttons_frame.rowconfigure(0, weight=1)
        for i in range(1, 5):
            self.buttons_frame.rowconfigure(i, weight=1)
            self.buttons_frame.columnconfigure(i, weight=1)
        
        # Tworzenie przycisków 
        self.create_numbers_buttons()
        self.creater_operator_buttons()
        self.create_special_buttons()
        
    def create_display_frame(self):
        frm = tk.Frame(self, height=220, bg=self.COLOR_C)
        frm.pack(expand=True, fill="both")
        return frm
    
    def create_equation_lbl(self):
        """ Etykieta przechowująca tworzone równanie """
        equation = tk.Label(
            self.display_frame, 
            text=self.equation, 
            anchor=tk.E, 
            bg=self.COLOR_D, 
            fg=self.COLOR_WHITE,
            padx=25,
            font=self.SMALL_FONT_STYLE)
        equation.pack(expand=True, fill="both")
        return equation
        
    def create_current_lbl(self):
        """ Etykieta przechowująca aktualnie wprowadzoną cyfrę """
        current = tk.Label(
            self.display_frame, 
            text=self.current, 
            anchor=tk.E,  
            bg=self.COLOR_D, 
            fg=self.COLOR_WHITE,
            padx=25,
            font=self.LARGE_FONT_STYLE)
        current.pack(expand=True, fill="both")
        return current
        
    def create_display_labels(self):
        """ Tworzy etykiety """
        equation = self.create_equation_lbl()
        current = self.create_current_lbl()
        return equation, current
    
    def create_buttons_frame(self):
        frm = tk.Frame(self)
        frm.pack(expand=True, fill="both")
        return frm
    
    def create_clear_button(self):
        """ Tworzy przycisk czyszczenia etykiet """
        btn = tk.Button(
            self.buttons_frame, 
            text="C",
            bg=self.COLOR_B,
            fg=self.COLOR_A,
            font=self.BTN_FONT_STYLE,
            borderwidth=0,
            command=self.clear)
        btn.grid(row=0, column=1, padx=1, pady=1, columnspan=2, sticky=tk.NSEW) 
        
    def create_equals_button(self):
        """ Tworzy przycisk 'równa się' który po 
        kliknięciu wywołuje metodę 'evaluate """
        btn = tk.Button(
            self.buttons_frame, 
            text="=",
            bg=self.COLOR_B,
            fg=self.COLOR_A,
            font=self.BTN_FONT_STYLE,
            borderwidth=0,
            command=self.evaulate)
        btn.grid(row=4, column=3, columnspan=2, padx=1, pady=1, sticky=tk.NSEW) 
        
    def create_erase_button(self):
        """ Tworzy przycisk usunięcia ustatniego znaku z etykiety urrent_lbl """
        btn = tk.Button(
            self.buttons_frame, 
            text=u"\u232B",
            bg=self.COLOR_B,
            fg=self.COLOR_A,
            font=self.ERASE_FONT_STYLE,
            borderwidth=0,
            command=self.erase)
        btn.grid(row=0, column=3, padx=1, pady=1, sticky=tk.NSEW) 

    def create_special_buttons(self):
        """ Tworzy przyciski specjalne """
        self.create_clear_button()
        self.create_equals_button()
        self.create_erase_button()

    def creater_operator_buttons(self):
        """ Tworzy przyciski operatorów matematycznych"""
        i = 0
        for operator, symbol in self.operators.items():
            btn = tk.Button(
                self.buttons_frame, 
                text=symbol,
                bg=self.COLOR_B,
                fg=self.COLOR_A,
                font=self.BTN_FONT_STYLE,
                borderwidth=0,
                command=lambda x=operator: self.append_operator(x))
            btn.grid(row=i, column=4, padx=1, pady=1, sticky=tk.NSEW)
            i += 1
    
    def create_numbers_buttons(self):
        """ Tworzy przyciski cyfr """
        for num, position in self.numbers.items():
            btn = tk.Button(
                self.buttons_frame, 
                text=str(num),
                bg=self.COLOR_C,
                fg=self.COLOR_A,
                font=self.MEDIUM_FONT_STYLE,
                borderwidth=0,
                command=lambda x=num: self.add_to_equation(x))
            btn.grid(row=position[0], column=position[1], 
                     padx=1, pady=1, sticky=tk.NSEW)
        
    def update_equation_lbl(self):
        self.equation_lbl.config(text=self.equation)
        
    def update_current_lbl(self):
        self.current_lbl.config(text=self.current)
        
    def add_to_equation(self, value):
        """ Dodaje do atrybutu current przekazaną wartość, 
        która przed zostaje zmieniona na ciąg tekstowy """
        self.current += str(value)
        self.update_current_lbl()
        
    def append_operator(self, operator):
        """ Dodaje operator matematyczny do current, 
        która następnie jest odawana do równania, 
        a na końcu current jest czyszczone. Na końcu wywołuje odświeżenie etykiet """
        self.current += str(operator)
        self.equation += self.current
        self.current = ""
        self.update_equation_lbl()
        self.update_current_lbl()
        
    def evaulate(self):
        """ Przetwarza równanie na wyrażenie """
        self.equation += self.current
        self.update_equation_lbl()
        # usuwa ostatni znak równania jeżeli jest operatorem
        if self.equation[-1] in self.operators:
            self.equation = self.equation[:-1]
        self.current = str(eval(self.equation))
        self.equation = ""
        self.update_current_lbl()
        
    def clear(self):
        self.current = ""
        self.equation = ""
        self.update_equation_lbl()
        self.update_current_lbl()
        
    def erase(self):
        _tmp = self.current
        if len(_tmp) > 1:
            self.current = _tmp[:-1]
        else:
            self.current = ""
        self.update_current_lbl()

    def run(self):
        self.mainloop()
        

if __name__ == '__main__':
    Calculator().run()
        