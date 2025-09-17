import tkinter as tk
import ttkbootstrap as tb
from tkinter import ttk, messagebox

LANGUAGES = {
    'cn': {
        'title': "实验动物等效剂量转换工具", 'header': "体表面积等效剂量转换", 'animal_b': "来源动物 (动物B)",
        'animal_a': "目标动物 (动物A)", 'km_factor': "Km系数:", 'dose_b': "实验剂量 (mg/kg):",
        'calculate_btn': "开始计算", 'result_label': "计算结果 (动物A等效剂量):", 'result_default': "等待计算...",
        'switch_lang_btn': "English", 'error_title': "输入错误", 'error_all_fields': "请确保所有字段都已填写！",
        'error_dose_format': "实验剂量必须是一个有效的数字！", 'error_km_zero_title': "计算错误",
        'error_km_zero_msg': "目标动物的Km系数不能为0！",
        'species_list': [
            "小鼠 (Mouse)", "大鼠 (Rat)", "仓鼠 (Hamster)", "豚鼠 (Guinea Pig)", "兔 (Rabbit)",
            "犬 (Dog)", "猴 (Monkey)", "人 (Human, 60kg)"
        ]
    },
    'en': {
        'title': "Equivalent Dose Conversion Tool", 'header': "BSA Equivalent Dose Conversion", 'animal_b': "Source Animal (Animal B)",
        'animal_a': "Target Animal (Animal A)", 'km_factor': "Km Factor:", 'dose_b': "Dose (mg/kg):",
        'calculate_btn': "Calculate", 'result_label': "Result (Equivalent Dose for Animal A):",
        'result_default': "Waiting for calculation...", 'switch_lang_btn': "中文", 'error_title': "Input Error",
        'error_all_fields': "Please ensure all fields are filled!", 'error_dose_format': "The dose must be a valid number!",
        'error_km_zero_title': "Calculation Error", 'error_km_zero_msg': "The Km factor of the target animal cannot be 0!",
        'species_list': [
            "Mouse (小鼠)", "Rat (大鼠)", "Hamster (仓鼠)", "Guinea Pig (豚鼠)", "Rabbit (兔)",
            "Dog (犬)", "Monkey (猴)", "Human, 60kg (人)"
        ]
    }
}
KM_FACTORS = {
    "小鼠 (Mouse)": 3, "大鼠 (Rat)": 6, "仓鼠 (Hamster)": 5, "豚鼠 (Guinea Pig)": 8, "兔 (Rabbit)": 12,
    "犬 (Dog)": 20, "猴 (Monkey)": 12, "人 (Human, 60kg)": 37, "Mouse (小鼠)": 3, "Rat (大鼠)": 6,
    "Hamster (仓鼠)": 5, "Guinea Pig (豚鼠)": 8, "Rabbit (兔)": 12, "Dog (犬)": 20,
    "Monkey (猴)": 12, "Human, 60kg (人)": 37
}

class DoseConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("700x450") # 设置一个更合适的初始尺寸
        self.root.minsize(650, 420) # 设置最小尺寸，防止窗口过小
        self.current_lang = 'cn'

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.main_frame = ttk.Frame(self.root, padding=(20, 10))
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.rowconfigure(3, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

        # --- 顶部区域：标题和语言切换按钮 ---
        header_frame = ttk.Frame(self.main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        self.title_label = ttk.Label(header_frame, font=("Helvetica", 18, "bold"))
        self.title_label.pack(side="left", padx=(10, 0))

        self.lang_button = ttk.Button(header_frame, command=self.switch_language, width=8)
        self.lang_button.pack(side="right")

        # --- 中部区域：输入控件 ---
        self.source_frame = ttk.LabelFrame(self.main_frame, padding=15)
        self.source_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.source_frame.columnconfigure(1, weight=1)

        self.target_frame = ttk.LabelFrame(self.main_frame, padding=15)
        self.target_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.target_frame.columnconfigure(1, weight=1)

        # 来源动物控件
        self.label_dose_b = ttk.Label(self.source_frame)
        self.label_dose_b.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0,5))
        self.dose_b_var = tk.StringVar()
        self.entry_dose_b = ttk.Entry(self.source_frame, textvariable=self.dose_b_var, font=("Helvetica", 10))
        self.entry_dose_b.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        self.label_animal_b = ttk.Label(self.source_frame)
        self.label_animal_b.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0,5))
        self.animal_b_var = tk.StringVar()
        self.combo_animal_b = ttk.Combobox(self.source_frame, textvariable=self.animal_b_var, state="readonly", font=("Helvetica", 10))
        self.combo_animal_b.grid(row=3, column=0, columnspan=2, sticky="ew")
        self.combo_animal_b.bind("<<ComboboxSelected>>", self.update_km_b)

        self.km_b_frame = ttk.Frame(self.source_frame)
        self.km_b_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10,0))
        self.label_km_b = ttk.Label(self.km_b_frame)
        self.label_km_b.pack(side="left")
        self.km_b_label = ttk.Label(self.km_b_frame, text="--", font=("Helvetica", 10, "bold"))
        self.km_b_label.pack(side="left", padx=5)

        # 目标动物控件
        self.label_animal_a = ttk.Label(self.target_frame)
        self.label_animal_a.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0,5))
        self.animal_a_var = tk.StringVar()
        self.combo_animal_a = ttk.Combobox(self.target_frame, textvariable=self.animal_a_var, state="readonly", font=("Helvetica", 10))
        self.combo_animal_a.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.combo_animal_a.bind("<<ComboboxSelected>>", self.update_km_a)
        
        self.km_a_frame = ttk.Frame(self.target_frame)
        self.km_a_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10,0))
        self.label_km_a = ttk.Label(self.km_a_frame)
        self.label_km_a.pack(side="left")
        self.km_a_label = ttk.Label(self.km_a_frame, text="--", font=("Helvetica", 10, "bold"))
        self.km_a_label.pack(side="left", padx=5)

        # --- 底部区域：按钮、结果和声明 ---
        self.calculate_button = ttk.Button(self.main_frame, command=self.calculate_dose, bootstyle="primary") # 使用 bootstyle 美化
        self.calculate_button.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=15, ipady=5)

        self.result_frame = ttk.Frame(self.main_frame)
        self.result_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10)
        
        self.label_result = ttk.Label(self.result_frame, font=("Helvetica", 12, "bold"))
        self.label_result.pack()
        self.result_var = tk.StringVar()
        self.result_label_display = ttk.Label(self.result_frame, textvariable=self.result_var, font=("Helvetica", 22, "bold"), bootstyle="success")
        self.result_label_display.pack(pady=5)
        
        declaration_text = "Created by kaixuncao. For bug reports, please contact kaixuncao@gmail.com."
        self.declaration_label = ttk.Label(self.main_frame, text=declaration_text, font=("Segoe UI", 8), bootstyle="secondary")
        self.declaration_label.grid(row=4, column=0, columnspan=2, sticky="e", padx=10, pady=(10,0))
        
        self.update_ui_language()

    def update_ui_language(self):
        lang_dict = LANGUAGES[self.current_lang]
        b_idx, a_idx = self.combo_animal_b.current(), self.combo_animal_a.current()

        self.root.title(lang_dict['title'])
        self.title_label.config(text=lang_dict['header'])
        self.source_frame.config(text=lang_dict['animal_b'])
        self.target_frame.config(text=lang_dict['animal_a'])
        self.label_dose_b.config(text=lang_dict['dose_b'])
        self.label_animal_b.config(text=lang_dict['animal_b'])
        self.label_animal_a.config(text=lang_dict['animal_a'])
        self.label_km_b.config(text=lang_dict['km_factor'])
        self.label_km_a.config(text=lang_dict['km_factor'])
        self.calculate_button.config(text=lang_dict['calculate_btn'])
        self.lang_button.config(text=lang_dict['switch_lang_btn'])
        self.label_result.config(text=lang_dict['result_label'])

        species_list = lang_dict['species_list']
        self.combo_animal_b['values'] = species_list
        self.combo_animal_a['values'] = species_list
        
        if b_idx != -1: self.combo_animal_b.current(b_idx)
        if a_idx != -1: self.combo_animal_a.current(a_idx)

        if self.result_var.get() in (LANGUAGES['cn']['result_default'], LANGUAGES['en']['result_default']):
            self.result_var.set(lang_dict['result_default'])

    def switch_language(self):
        self.current_lang = 'en' if self.current_lang == 'cn' else 'cn'
        self.update_ui_language()
    def update_km_b(self, event=None):
        species = self.animal_b_var.get()
        if species in KM_FACTORS: self.km_b_label.config(text=str(KM_FACTORS[species]))
    def update_km_a(self, event=None):
        species = self.animal_a_var.get()
        if species in KM_FACTORS: self.km_a_label.config(text=str(KM_FACTORS[species]))
    def calculate_dose(self):
        lang_dict = LANGUAGES[self.current_lang]
        animal_b_name, animal_a_name, dose_b_str = self.animal_b_var.get(), self.animal_a_var.get(), self.dose_b_var.get()
        if not all((animal_b_name, animal_a_name, dose_b_str)):
            messagebox.showerror(lang_dict['error_title'], lang_dict['error_all_fields']); return
        try: dose_b = float(dose_b_str)
        except ValueError: messagebox.showerror(lang_dict['error_title'], lang_dict['error_dose_format']); return
        km_b, km_a = KM_FACTORS[animal_b_name], KM_FACTORS[animal_a_name]
        if km_a == 0: messagebox.showerror(lang_dict['error_km_zero_title'], lang_dict['error_km_zero_msg']); return
        self.result_var.set(f"{dose_b * (km_b / km_a):.4f} mg/kg")

if __name__ == "__main__":
    # 可在此处切换主题，例如 "superhero", "darkly", "litera", "cosmo"
    root = tb.Window(themename="litera")
    app = DoseConverterApp(root)
    root.mainloop()
