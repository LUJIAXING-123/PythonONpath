# -*- coding: utf-8 -*-
"""
多功能计算器 - Multi-functional Calculator
功能模块:
    1. 基础计算器 - 四则运算、括号、历史记录
    2. 科学计算器 - 三角/对数/指数/阶乘/平方立方根
    3. 单位换算 - 长度/重量/温度/面积/体积/时间/速度
    4. 方程求解 - 一元一次/一元二次/二元一次方程组
    5. 进制转换 - 二/八/十/十六进制互转
    6. 函数绘图 - 基本函数图像绘制
    7. 统计计算 - 平均值/方差/标准差/中位数/最值
作者: AI Assistant
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import math
import re
import random
import statistics
from datetime import datetime


# ============================================================
# 工具函数
# ============================================================

def safe_eval(expr):
    """安全地计算数学表达式"""
    try:
        expr = expr.replace('×', '*').replace('÷', '/')
        expr = expr.replace('π', 'pi').replace('π', 'pi')
        allowed = {
            'pi': math.pi,
            'e': math.e,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            'sinh': math.sinh,
            'cosh': math.cosh,
            'tanh': math.tanh,
            'log': math.log,
            'log10': math.log10,
            'log2': math.log2,
            'sqrt': math.sqrt,
            'cbrt': lambda x: math.copysign(abs(x) ** (1/3), x),
            'exp': math.exp,
            'abs': abs,
            'factorial': math.factorial,
            'degrees': math.degrees,
            'radians': math.radians,
            'pow': math.pow,
            'ceil': math.ceil,
            'floor': math.floor,
            'round': round,
            '__builtins__': {}
        }
        # 处理百分号
        expr = re.sub(r'(\d+(?:\.\d+)?)%', r'(\1/100)', expr)
        # 处理阶乘符号
        def replace_factorial(m):
            return f'factorial({m.group(1)})'
        expr = re.sub(r'(\d+(?:\.\d+)?|\([^()]+\))!', replace_factorial, expr)
        result = eval(expr, allowed, {})
        if isinstance(result, complex):
            return result
        if result == int(result):
            return int(result)
        return round(result, 12)
    except Exception as ex:
        raise ValueError(f"表达式错误: {ex}")


def format_number(n):
    """格式化数字显示"""
    if isinstance(n, complex):
        return f"{n.real:.6g}{'+' if n.imag >= 0 else ''}{n.imag:.6g}j"
    if n == int(n):
        return str(int(n))
    if abs(n) >= 1e10 or (0 < abs(n) < 1e-6):
        return f"{n:.6e}"
    return f"{n:.10g}"


# ============================================================
# 主应用
# ============================================================

class MultiCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("多功能计算器")
        self.root.minsize(360, 520)

        # 手机适配: 检测窗口大小，自适应
        self.is_mobile = self._detect_mobile()
        self._setup_style()

        self.history = []
        self._build_ui()

        # 默认尺寸
        w, h = 420, 640
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        if self.is_mobile:
            w, h = min(sw - 40, 380), min(sh - 40, 620)
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _detect_mobile(self):
        """简单判断是否为小屏设备"""
        try:
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            return sw < 600 or sh < 700
        except Exception:
            return False

    def _setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except Exception:
            pass

        self.bg_color = "#2b2b2b"
        self.fg_color = "#ffffff"
        self.panel_color = "#3a3a3a"
        self.accent_color = "#4a9eff"
        self.btn_color = "#4a4a4a"
        self.btn_hover = "#5a5a5a"
        self.btn_op = "#f0a040"
        self.btn_eq = "#4a9eff"

        style.configure('TNotebook', background=self.bg_color, borderwidth=0)
        style.configure('TNotebook.Tab',
                        background=self.panel_color,
                        foreground=self.fg_color,
                        padding=(10, 8) if not self.is_mobile else (6, 6),
                        font=('Microsoft YaHei', 10 if not self.is_mobile else 9))
        style.map('TNotebook.Tab',
                  background=[('selected', self.accent_color), ('active', self.btn_hover)],
                  foreground=[('selected', '#ffffff')])
        style.configure('TFrame', background=self.bg_color)
        style.configure('TLabel', background=self.bg_color, foreground=self.fg_color,
                        font=('Microsoft YaHei', 10))
        style.configure('TButton', font=('Microsoft YaHei', 11))
        style.configure('TEntry', font=('Microsoft YaHei', 12))

        self.root.configure(bg=self.bg_color)

    def _build_ui(self):
        # 顶部标题栏
        title_bar = tk.Frame(self.root, bg=self.accent_color, height=36)
        title_bar.pack(fill='x', side='top')
        title_bar.pack_propagate(False)
        tk.Label(title_bar, text="🧮 多功能计算器", bg=self.accent_color,
                 fg='white', font=('Microsoft YaHei', 12, 'bold')).pack(side='left', padx=12)
        tk.Label(title_bar, text=f"{'📱' if self.is_mobile else '💻'}",
                 bg=self.accent_color, fg='white',
                 font=('Microsoft YaHei', 12)).pack(side='right', padx=12)

        self.nb = ttk.Notebook(self.root)
        self.nb.pack(fill='both', expand=True, padx=4, pady=4)

        # 各功能标签页
        self.tab_basic = ttk.Frame(self.nb)
        self.tab_sci = ttk.Frame(self.nb)
        self.tab_unit = ttk.Frame(self.nb)
        self.tab_equ = ttk.Frame(self.nb)
        self.tab_base = ttk.Frame(self.nb)
        self.tab_plot = ttk.Frame(self.nb)
        self.tab_stat = ttk.Frame(self.nb)

        self.nb.add(self.tab_basic, text="基础")
        self.nb.add(self.tab_sci, text="科学")
        self.nb.add(self.tab_unit, text="单位")
        self.nb.add(self.tab_equ, text="方程")
        self.nb.add(self.tab_base, text="进制")
        self.nb.add(self.tab_plot, text="绘图")
        self.nb.add(self.tab_stat, text="统计")

        # 构建各模块
        self._build_basic(self.tab_basic)
        self._build_scientific(self.tab_sci)
        self._build_unit(self.tab_unit)
        self._build_equation(self.tab_equ)
        self._build_baseconv(self.tab_base)
        self._build_plot(self.tab_plot)
        self._build_stats(self.tab_stat)

        # 底部状态栏
        status = tk.Frame(self.root, bg=self.panel_color, height=24)
        status.pack(fill='x', side='bottom')
        status.pack_propagate(False)
        self.status_lbl = tk.Label(status, text="  就绪", bg=self.panel_color,
                                   fg='#cccccc', font=('Microsoft YaHei', 8))
        self.status_lbl.pack(side='left')
        clock = tk.Label(status, text="", bg=self.panel_color,
                         fg='#cccccc', font=('Microsoft YaHei', 8))
        clock.pack(side='right', padx=8)
        self._tick_clock(clock)

    def _tick_clock(self, lbl):
        lbl.config(text=datetime.now().strftime("%H:%M:%S") + "  ")
        self.root.after(1000, self._tick_clock, lbl)

    def _set_status(self, text):
        self.status_lbl.config(text="  " + text)

    # --------------------------------------------------------
    # 通用按钮
    # --------------------------------------------------------

    def _make_button(self, parent, text, command, bg=None, fg='white',
                     width=None, height=None, col=None, row=None, span=1, pad=3):
        b = tk.Button(parent, text=text, command=command,
                      bg=bg or self.btn_color, fg=fg,
                      activebackground=self.btn_hover, activeforeground='white',
                      font=('Microsoft YaHei', 13 if not self.is_mobile else 11, 'bold'),
                      relief='flat', bd=0, cursor='hand2')
        if width:
            b.config(width=width)
        if height:
            b.config(height=height)
        if row is not None and col is not None:
            b.grid(row=row, column=col, columnspan=span,
                   sticky='nsew', padx=pad, pady=pad)
        return b

    # ========================================================
    # 模块 1: 基础计算器
    # ========================================================
    def _build_basic(self, parent):
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(2, weight=1)

        # 显示屏
        top = tk.Frame(parent, bg=self.bg_color)
        top.grid(row=0, column=0, sticky='nsew', padx=8, pady=(8, 4))
        top.columnconfigure(0, weight=1)

        self.basic_expr = tk.Label(top, text="", anchor='e',
                                   bg=self.bg_color, fg='#888888',
                                   font=('Microsoft YaHei', 11))
        self.basic_expr.grid(row=0, column=0, sticky='ew')

        self.basic_display = tk.Label(top, text="0", anchor='e',
                                      bg=self.bg_color, fg='white',
                                      font=('Microsoft YaHei', 28 if not self.is_mobile else 22, 'bold'))
        self.basic_display.grid(row=1, column=0, sticky='ew')

        self.basic_value = ""

        # 按钮区
        btn_frame = tk.Frame(parent, bg=self.bg_color)
        btn_frame.grid(row=2, column=0, sticky='nsew', padx=6, pady=4)
        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)
        for i in range(5):
            btn_frame.rowconfigure(i, weight=1)

        def set_val(s):
            return lambda: self._basic_append(s)

        def compute():
            return self._basic_calc()

        rows = [
            [('C', self.btn_op), ('⌫', self.btn_op), ('(', self.btn_color), (')', self.btn_color)],
            [('7', self.btn_color), ('8', self.btn_color), ('9', self.btn_color), ('÷', self.btn_op)],
            [('4', self.btn_color), ('5', self.btn_color), ('6', self.btn_color), ('×', self.btn_op)],
            [('1', self.btn_color), ('2', self.btn_color), ('3', self.btn_color), ('-', self.btn_op)],
            [('0', self.btn_color), ('.', self.btn_color), ('=', self.btn_eq), ('+', self.btn_op)],
        ]
        for r, row in enumerate(rows):
            for c, (text, color) in enumerate(row):
                if text == 'C':
                    cmd = self._basic_clear
                elif text == '⌫':
                    cmd = self._basic_back
                elif text == '=':
                    cmd = compute
                else:
                    cmd = set_val(text)
                self._make_button(btn_frame, text, cmd, bg=color, row=r, col=c)

        # 历史记录
        history_top = tk.Frame(parent, bg=self.bg_color)
        history_top.grid(row=3, column=0, sticky='ew', padx=8, pady=4)
        tk.Label(history_top, text="📜 历史记录", bg=self.bg_color,
                 fg=self.accent_color, font=('Microsoft YaHei', 10, 'bold')).pack(side='left')
        tk.Button(history_top, text="清空", command=self._clear_basic_history,
                  bg=self.btn_color, fg='white', relief='flat', cursor='hand2',
                  font=('Microsoft YaHei', 9)).pack(side='right')

        history_frame = tk.Frame(parent, bg=self.bg_color, height=120)
        history_frame.grid(row=4, column=0, sticky='nsew', padx=8, pady=(0, 8))
        history_frame.grid_propagate(False)
        parent.rowconfigure(4, weight=0)

        self.basic_history = tk.Listbox(history_frame, bg='#1e1e1e', fg='white',
                                        font=('Microsoft YaHei', 10),
                                        selectbackground=self.accent_color,
                                        relief='flat', bd=0, activestyle='none')
        sb = ttk.Scrollbar(history_frame, command=self.basic_history.yview)
        self.basic_history.config(yscrollcommand=sb.set)
        self.basic_history.pack(side='left', fill='both', expand=True)
        sb.pack(side='right', fill='y')
        self.basic_history.bind('<Double-1>', self._reuse_history)

    def _basic_append(self, ch):
        if ch == '×':
            self.basic_value += '×'
        elif ch == '÷':
            self.basic_value += '÷'
        else:
            self.basic_value += ch
        self.basic_display.config(text=self.basic_value or "0")

    def _basic_clear(self):
        self.basic_value = ""
        self.basic_expr.config(text="")
        self.basic_display.config(text="0")

    def _basic_back(self):
        self.basic_value = self.basic_value[:-1]
        self.basic_display.config(text=self.basic_value or "0")

    def _basic_calc(self):
        if not self.basic_value:
            return
        try:
            expr = self.basic_value
            result = safe_eval(expr)
            self.basic_expr.config(text=expr + " =")
            display = format_number(result)
            self.basic_display.config(text=display)
            # 添加到历史
            record = f"{expr} = {display}"
            self.history.append(record)
            self.basic_history.insert(tk.END, record)
            self.basic_history.see(tk.END)
            self.basic_value = str(result)
            self._set_status("计算完成 ✓")
        except Exception as ex:
            self.basic_display.config(text="错误")
            self._set_status(f"✗ {ex}")

    def _reuse_history(self, event):
        sel = self.basic_history.curselection()
        if sel:
            item = self.basic_history.get(sel[0])
            if '=' in item:
                val = item.split('=')[-1].strip()
                self.basic_value = val
                self.basic_display.config(text=val)

    def _clear_basic_history(self):
        self.basic_history.delete(0, tk.END)
        self._set_status("历史已清空")

    # ========================================================
    # 模块 2: 科学计算器
    # ========================================================
    def _build_scientific(self, parent):
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(2, weight=1)

        top = tk.Frame(parent, bg=self.bg_color)
        top.grid(row=0, column=0, sticky='nsew', padx=8, pady=(8, 4))
        top.columnconfigure(0, weight=1)

        self.sci_expr = tk.Label(top, text="", anchor='e', bg=self.bg_color,
                                 fg='#888888', font=('Microsoft YaHei', 11))
        self.sci_expr.grid(row=0, column=0, sticky='ew')

        self.sci_display = tk.Label(top, text="0", anchor='e', bg=self.bg_color,
                                    fg='white',
                                    font=('Microsoft YaHei', 24 if not self.is_mobile else 20, 'bold'))
        self.sci_display.grid(row=1, column=0, sticky='ew')

        self.sci_value = ""
        self.angle_mode = tk.StringVar(value="DEG")
        mode_bar = tk.Frame(parent, bg=self.bg_color)
        mode_bar.grid(row=1, column=0, sticky='ew', padx=8)
        tk.Label(mode_bar, text="角度:", bg=self.bg_color, fg='white',
                 font=('Microsoft YaHei', 10)).pack(side='left')
        for m in ['DEG', 'RAD']:
            tk.Radiobutton(mode_bar, text=m, variable=self.angle_mode, value=m,
                           bg=self.bg_color, fg='white', selectcolor=self.btn_color,
                           activebackground=self.bg_color, activeforeground='white',
                           font=('Microsoft YaHei', 10), cursor='hand2').pack(side='left')

        btn_frame = tk.Frame(parent, bg=self.bg_color)
        btn_frame.grid(row=2, column=0, sticky='nsew', padx=6, pady=4)
        for i in range(5):
            btn_frame.columnconfigure(i, weight=1)
        for i in range(6):
            btn_frame.rowconfigure(i, weight=1)

        def ap(s):
            return lambda: self._sci_append(s)

        # 符号到函数的映射: 根据角度模式自动转换
        def trig_fn(fn_name):
            def inner():
                if self.angle_mode.get() == 'DEG':
                    self.sci_value += f'{fn_name}(radians('
                else:
                    self.sci_value += f'{fn_name}('
                self.sci_display.config(text=self.sci_value or "0")
            return inner

        def atrig_fn(fn_name):
            def inner():
                if self.angle_mode.get() == 'DEG':
                    self.sci_value += f'degrees({fn_name}('
                else:
                    self.sci_value += f'{fn_name}('
                self.sci_display.config(text=self.sci_value or "0")
            return inner

        rows = [
            [('sin', self.btn_op, trig_fn('sin')), ('cos', self.btn_op, trig_fn('cos')),
             ('tan', self.btn_op, trig_fn('tan')), ('π', self.btn_color, ap('π')),
             ('e', self.btn_color, ap('e'))],
            [('asin', self.btn_op, atrig_fn('asin')), ('acos', self.btn_op, atrig_fn('acos')),
             ('atan', self.btn_op, atrig_fn('atan')), ('x²', self.btn_op, ap('**2')),
             ('x³', self.btn_op, ap('**3'))],
            [('ln', self.btn_op, ap('log(')), ('log₁₀', self.btn_op, ap('log10(')),
             ('log₂', self.btn_op, ap('log2(')), ('√', self.btn_op, ap('sqrt(')),
             ('∛', self.btn_op, ap('cbrt('))],
            [('x^y', self.btn_op, ap('**')), ('eˣ', self.btn_op, ap('exp(')),
             ('n!', self.btn_op, ap('!')), ('%', self.btn_op, ap('%')),
             ('1/x', self.btn_op, ap('**(-1)'))],
            [('C', self.btn_color, self._sci_clear), ('⌫', self.btn_color, self._sci_back),
             ('(', self.btn_color, ap('(')), (')', self.btn_color, ap(')')),
             ('÷', self.btn_op, ap('÷'))],
            [('7', self.btn_color, ap('7')), ('8', self.btn_color, ap('8')),
             ('9', self.btn_color, ap('9')), ('×', self.btn_op, ap('×')),
             ('-', self.btn_op, ap('-'))],
            [('4', self.btn_color, ap('4')), ('5', self.btn_color, ap('5')),
             ('6', self.btn_color, ap('6')), ('+', self.btn_op, ap('+')),
             ('=', self.btn_eq, self._sci_calc)],
            [('1', self.btn_color, ap('1')), ('2', self.btn_color, ap('2')),
             ('3', self.btn_color, ap('3')), ('0', self.btn_color, ap('0')),
             ('.', self.btn_color, ap('.'))],
        ]
        for r, row in enumerate(rows):
            for c, (text, color, cmd) in enumerate(row):
                self._make_button(btn_frame, text, cmd, bg=color, row=r, col=c, pad=2)

        # 快捷功能
        quick = tk.Frame(parent, bg=self.bg_color)
        quick.grid(row=3, column=0, sticky='ew', padx=8, pady=4)
        for text, fn in [('随机数', self._sci_random), ('绝对值', self._sci_abs),
                         ('四舍五入', self._sci_round), ('取整', self._sci_int),
                         ('复制结果', self._sci_copy)]:
            tk.Button(quick, text=text, command=fn, bg=self.btn_color, fg='white',
                      relief='flat', cursor='hand2',
                      font=('Microsoft YaHei', 9)).pack(side='left', padx=2, expand=True, fill='x')

    def _sci_append(self, ch):
        self.sci_value += ch
        self.sci_display.config(text=self.sci_value or "0")

    def _sci_clear(self):
        self.sci_value = ""
        self.sci_expr.config(text="")
        self.sci_display.config(text="0")

    def _sci_back(self):
        self.sci_value = self.sci_value[:-1]
        self.sci_display.config(text=self.sci_value or "0")

    def _sci_calc(self):
        if not self.sci_value:
            return
        try:
            expr = self.sci_value
            result = safe_eval(expr)
            self.sci_expr.config(text=expr + " =")
            display = format_number(result)
            self.sci_display.config(text=display)
            self.sci_value = str(result) if not isinstance(result, complex) else display
            self._set_status(f"计算完成: {display}")
        except Exception as ex:
            self.sci_display.config(text="错误")
            self._set_status(f"✗ {ex}")

    def _sci_random(self):
        r = random.random()
        self.sci_display.config(text=format_number(r))
        self.sci_value = str(r)
        self._set_status("生成随机数")

    def _sci_abs(self):
        try:
            r = abs(safe_eval(self.sci_value or "0"))
            self.sci_display.config(text=format_number(r))
            self.sci_value = str(r)
        except Exception as ex:
            self._set_status(f"✗ {ex}")

    def _sci_round(self):
        try:
            r = round(safe_eval(self.sci_value or "0"))
            self.sci_display.config(text=str(r))
            self.sci_value = str(r)
        except Exception:
            pass

    def _sci_int(self):
        try:
            r = int(float(safe_eval(self.sci_value or "0")))
            self.sci_display.config(text=str(r))
            self.sci_value = str(r)
        except Exception:
            pass

    def _sci_copy(self):
        text = self.sci_display.cget('text')
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self._set_status(f"已复制: {text}")

    # ========================================================
    # 模块 3: 单位换算
    # ========================================================
    UNIT_DATA = {
        "长度": {
            "米(m)": 1, "千米(km)": 1000, "厘米(cm)": 0.01, "毫米(mm)": 0.001,
            "微米(μm)": 1e-6, "纳米(nm)": 1e-9, "英寸(in)": 0.0254, "英尺(ft)": 0.3048,
            "码(yd)": 0.9144, "英里(mi)": 1609.344, "海里(nmi)": 1852, "里": 500,
            "丈": 3.33333, "尺": 0.33333, "寸": 0.03333
        },
        "重量": {
            "千克(kg)": 1, "克(g)": 0.001, "毫克(mg)": 1e-6, "吨(t)": 1000,
            "磅(lb)": 0.453592, "盎司(oz)": 0.0283495, "斤": 0.5, "两": 0.05,
            "克拉(ct)": 0.0002
        },
        "面积": {
            "平方米(m²)": 1, "平方千米(km²)": 1e6, "平方厘米(cm²)": 1e-4,
            "平方毫米(mm²)": 1e-6, "公顷(ha)": 1e4, "亩": 666.667,
            "平方英尺(ft²)": 0.092903, "平方英里(mi²)": 2589988.11, "英亩": 4046.856
        },
        "体积": {
            "立方米(m³)": 1, "升(L)": 0.001, "毫升(mL)": 1e-6,
            "立方厘米(cm³)": 1e-6, "立方英尺(ft³)": 0.0283168,
            "加仑(gal)": 0.00378541, "夸脱(qt)": 0.000946353
        },
        "时间": {
            "秒(s)": 1, "毫秒(ms)": 1e-3, "微秒(μs)": 1e-6,
            "分钟(min)": 60, "小时(h)": 3600, "天(d)": 86400,
            "周(week)": 604800, "年(year)": 31536000
        },
        "速度": {
            "米/秒(m/s)": 1, "千米/时(km/h)": 0.277778, "英里/时(mph)": 0.44704,
            "节(kn)": 0.514444, "英尺/秒(ft/s)": 0.3048, "光速(c)": 299792458,
            "马赫(Ma)": 340.29
        },
        "数据": {
            "字节(B)": 1, "千字节(KB)": 1024, "兆字节(MB)": 1024**2,
            "吉字节(GB)": 1024**3, "太字节(TB)": 1024**4,
            "位(bit)": 0.125
        },
    }

    def _build_unit(self, parent):
        parent.columnconfigure(0, weight=1)
        for r in range(6):
            parent.rowconfigure(r, weight=0)

        # 类型选择
        tk.Label(parent, text="选择类别:", bg=self.bg_color, fg='white',
                 font=('Microsoft YaHei', 11)).grid(row=0, column=0, sticky='w',
                                                    padx=12, pady=(12, 4))

        self.unit_category = tk.StringVar(value="长度")
        cat_combo = ttk.Combobox(parent, textvariable=self.unit_category,
                                 values=list(self.UNIT_DATA.keys()),
                                 state='readonly', font=('Microsoft YaHei', 11))
        cat_combo.grid(row=1, column=0, sticky='ew', padx=12, pady=4)
        cat_combo.bind('<<ComboboxSelected>>', lambda e: self._update_units())

        # 输入单位
        frm1 = tk.Frame(parent, bg=self.bg_color)
        frm1.grid(row=2, column=0, sticky='ew', padx=12, pady=4)
        frm1.columnconfigure(0, weight=2)
        frm1.columnconfigure(1, weight=3)

        tk.Label(frm1, text="输入:", bg=self.bg_color, fg='white',
                 font=('Microsoft YaHei', 10)).grid(row=0, column=0, columnspan=2, sticky='w')
        self.unit_input = tk.Entry(frm1, bg='#1e1e1e', fg='white',
                                   insertbackground='white', relief='flat',
                                   font=('Microsoft YaHei', 14, 'bold'))
        self.unit_input.grid(row=1, column=0, sticky='ew', ipady=6)
        self.unit_from = tk.StringVar()
        self.combo_from = ttk.Combobox(frm1, textvariable=self.unit_from,
                                       state='readonly', font=('Microsoft YaHei', 11))
        self.combo_from.grid(row=1, column=1, sticky='ew', padx=(8, 0), ipady=6)
        self.unit_input.bind('<KeyRelease>', lambda e: self._do_convert())
        self.unit_input.bind('<KeyRelease>', lambda e: self._do_convert())

        # 输出单位
        frm2 = tk.Frame(parent, bg=self.bg_color)
        frm2.grid(row=3, column=0, sticky='ew', padx=12, pady=4)
        frm2.columnconfigure(0, weight=2)
        frm2.columnconfigure(1, weight=3)

        tk.Label(frm2, text="转换为:", bg=self.bg_color, fg='white',
                 font=('Microsoft YaHei', 10)).grid(row=0, column=0, columnspan=2, sticky='w')
        self.unit_output = tk.Label(frm2, text="0", anchor='w', bg='#1e1e1e', fg='white',
                                    font=('Microsoft YaHei', 14, 'bold'))
        self.unit_output.grid(row=1, column=0, sticky='nsew', ipady=6)
        self.unit_output.configure(padx=6)
        self.unit_to = tk.StringVar()
        self.combo_to = ttk.Combobox(frm2, textvariable=self.unit_to,
                                     state='readonly', font=('Microsoft YaHei', 11))
        self.combo_to.grid(row=1, column=1, sticky='ew', padx=(8, 0), ipady=6)

        self.combo_from.bind('<<ComboboxSelected>>', lambda e: self._do_convert())
        self.combo_to.bind('<<ComboboxSelected>>', lambda e: self._do_convert())

        # 温度换算（独立处理，因非线性）
        temp_frame = tk.LabelFrame(parent, text="温度换算 (独立)",
                                   bg=self.bg_color, fg=self.accent_color,
                                   font=('Microsoft YaHei', 10, 'bold'),
                                   bd=1, relief='solid')
        temp_frame.grid(row=4, column=0, sticky='ew', padx=12, pady=8)
        for i in range(4):
            temp_frame.columnconfigure(i, weight=1)

        self.temp_val = tk.Entry(temp_frame, bg='#1e1e1e', fg='white',
                                 insertbackground='white', relief='flat',
                                 font=('Microsoft YaHei', 12))
        self.temp_val.grid(row=0, column=0, columnspan=4, sticky='ew',
                           padx=6, pady=6, ipady=4)
        self.temp_val.insert(0, "100")
        self.temp_val.bind('<KeyRelease>', lambda e: self._temp_convert())

        for i, (label, key) in enumerate([("摄氏度(°C)", "C"), ("华氏度(°F)", "F"),
                                           ("开尔文(K)", "K"), ("列氏度(°Ré)", "R")]):
            tk.Label(temp_frame, text=label, bg=self.bg_color, fg='#cccccc',
                     font=('Microsoft YaHei', 9)).grid(row=1, column=i, padx=4, pady=(6, 0))
            lbl = tk.Label(temp_frame, text="--", bg=self.bg_color, fg='white',
                           font=('Microsoft YaHei', 11, 'bold'))
            lbl.grid(row=2, column=i, padx=4, pady=(0, 6))
            setattr(self, f'temp_{key}', lbl)

        # 常用换算参考
        ref = tk.LabelFrame(parent, text="快速参考", bg=self.bg_color,
                            fg=self.accent_color,
                            font=('Microsoft YaHei', 10, 'bold'), bd=1, relief='solid')
        ref.grid(row=5, column=0, sticky='nsew', padx=12, pady=8)
        ref.columnconfigure(0, weight=1)
        ref.columnconfigure(1, weight=1)

        refs = [
            "1 米 = 3.28 英尺",
            "1 千克 = 2.20 磅",
            "1 公里 = 0.62 英里",
            "1 升 = 33.8 盎司",
            "1 英寸 = 2.54 厘米",
            "1 斤 = 500 克",
        ]
        for i, text in enumerate(refs):
            tk.Label(ref, text=text, bg=self.bg_color, fg='#cccccc',
                     font=('Microsoft YaHei', 9)).grid(row=i // 2, column=i % 2,
                                                        sticky='w', padx=8, pady=2)

        parent.rowconfigure(5, weight=1)
        self._update_units()
        self._do_convert()
        self._temp_convert()

    def _update_units(self):
        cat = self.unit_category.get()
        units = list(self.UNIT_DATA[cat].keys())
        self.combo_from['values'] = units
        self.combo_to['values'] = units
        self.unit_from.set(units[0])
        self.unit_to.set(units[1] if len(units) > 1 else units[0])
        self._do_convert()

    def _do_convert(self):
        try:
            val = float(self.unit_input.get() or "0")
            from_unit = self.unit_from.get()
            to_unit = self.unit_to.get()
            cat = self.unit_category.get()
            factor_from = self.UNIT_DATA[cat][from_unit]
            factor_to = self.UNIT_DATA[cat][to_unit]
            converted = val * factor_from / factor_to
            self.unit_output.config(text=format_number(converted))
            self._set_status(f"{val} {from_unit} = {format_number(converted)} {to_unit}")
        except Exception:
            self.unit_output.config(text="--")

    def _temp_convert(self):
        try:
            c = float(self.temp_val.get() or "0")
            f = c * 9 / 5 + 32
            k = c + 273.15
            r = c * 0.8
            self.temp_C.config(text=f"{c:.4g}")
            self.temp_F.config(text=f"{f:.4g}")
            self.temp_K.config(text=f"{k:.4g}")
            self.temp_R.config(text=f"{r:.4g}")
        except Exception:
            for k in ['C', 'F', 'K', 'R']:
                getattr(self, f'temp_{k}').config(text="--")

    # ========================================================
    # 模块 4: 方程求解
    # ========================================================
    def _build_equation(self, parent):
        parent.columnconfigure(0, weight=1)

        notebook = ttk.Notebook(parent)
        notebook.pack(fill='both', expand=True, padx=6, pady=6)

        # --- 一元一次: ax + b = 0 ---
        t1 = ttk.Frame(notebook)
        notebook.add(t1, text="一元一次")
        self._build_linear1(t1)

        # --- 一元二次: ax² + bx + c = 0 ---
        t2 = ttk.Frame(notebook)
        notebook.add(t2, text="一元二次")
        self._build_quadratic(t2)

        # --- 二元一次方程组 ---
        t3 = ttk.Frame(notebook)
        notebook.add(t3, text="二元一次")
        self._build_linear2(t3)

        # --- 一元三次 ---
        t4 = ttk.Frame(notebook)
        notebook.add(t4, text="一元三次")
        self._build_cubic(t4)

        # --- 自定义表达式 ---
        t5 = ttk.Frame(notebook)
        notebook.add(t5, text="自定义")
        self._build_custom_expr(t5)

    def _entry_row(self, parent, label, default="", row=0):
        tk.Label(parent, text=label, bg=self.bg_color, fg='white',
                 font=('Microsoft YaHei', 11)).grid(row=row, column=0,
                                                    sticky='e', padx=6, pady=6)
        e = tk.Entry(parent, bg='#1e1e1e', fg='white', insertbackground='white',
                     relief='flat', font=('Microsoft YaHei', 12))
        e.grid(row=row, column=1, sticky='ew', padx=6, pady=6, ipady=4)
        e.insert(0, default)
        return e

    def _build_linear1(self, parent):
        parent.configure(bg=self.bg_color)
        parent.columnconfigure(1, weight=1)
        tk.Label(parent, text="方程形式: a·x + b = 0",
                 bg=self.bg_color, fg=self.accent_color,
                 font=('Microsoft YaHei', 12, 'bold')).grid(row=0, column=0, columnspan=2,
                                                           pady=(12, 8))
        e_a = self._entry_row(parent, "a =", "2", row=1)
        e_b = self._entry_row(parent, "b =", "-6", row=2)
        result_lbl = tk.Label(parent, text="x = ?", bg=self.bg_color, fg='white',
                              font=('Microsoft YaHei', 14, 'bold'))
        result_lbl.grid(row=3, column=0, columnspan=2, pady=12)

        def solve():
            try:
                a = float(e_a.get())
                b = float(e_b.get())
                if a == 0:
                    result_lbl.config(text="a 不能为 0" if b != 0 else "无穷多解")
                else:
                    x = -b / a
                    result_lbl.config(text=f"x = {format_number(x)}")
                    self._set_status(f"方程: {a}x + {b} = 0, 解: x={format_number(x)}")
            except Exception as ex:
                result_lbl.config(text=f"错误: {ex}")

        self._solve_btn(parent, solve, 4)

    def _build_quadratic(self, parent):
        parent.configure(bg=self.bg_color)
        parent.columnconfigure(1, weight=1)
        tk.Label(parent, text="方程形式: a·x² + b·x + c = 0",
                 bg=self.bg_color, fg=self.accent_color,
                 font=('Microsoft YaHei', 12, 'bold')).grid(row=0, column=0, columnspan=2,
                                                           pady=(12, 8))
        e_a = self._entry_row(parent, "a =", "1", row=1)
        e_b = self._entry_row(parent, "b =", "-5", row=2)
        e_c = self._entry_row(parent, "c =", "6", row=3)
        result_lbl = tk.Label(parent, text="x₁ = ?, x₂ = ?",
                              bg=self.bg_color, fg='white',
                              font=('Microsoft YaHei', 13, 'bold'))
        result_lbl.grid(row=4, column=0, columnspan=2, pady=12)

        def solve():
            try:
                a, b, c = float(e_a.get()), float(e_b.get()), float(e_c.get())
                if a == 0:
                    result_lbl.config(text="退化为一元一次方程")
                    return
                disc = b * b - 4 * a * c
                if disc > 0:
                    x1 = (-b + math.sqrt(disc)) / (2 * a)
                    x2 = (-b - math.sqrt(disc)) / (2 * a)
                    result_lbl.config(text=f"x₁ = {format_number(x1)}\nx₂ = {format_number(x2)}")
                elif disc == 0:
                    x = -b / (2 * a)
                    result_lbl.config(text=f"x₁ = x₂ = {format_number(x)}")
                else:
                    real = -b / (2 * a)
                    imag = math.sqrt(-disc) / (2 * a)
                    result_lbl.config(
                        text=f"x₁ = {format_number(real)}+{format_number(abs(imag))}i\n"
                             f"x₂ = {format_number(real)}-{format_number(abs(imag))}i")
                self._set_status(f"Δ = {format_number(disc)}")
            except Exception as ex:
                result_lbl.config(text=f"错误: {ex}")

        self._solve_btn(parent, solve, 5)

    def _build_linear2(self, parent):
        parent.configure(bg=self.bg_color)
        parent.columnconfigure(1, weight=1)
        tk.Label(parent, text="方程组:\n a₁·x + b₁·y = c₁\n a₂·x + b₂·y = c₂",
                 bg=self.bg_color, fg=self.accent_color,
                 font=('Microsoft YaHei', 11, 'bold')).grid(row=0, column=0, columnspan=2,
                                                           pady=(12, 8))
        e_a1 = self._entry_row(parent, "a₁ =", "1", row=1)
        e_b1 = self._entry_row(parent, "b₁ =", "1", row=2)
        e_c1 = self._entry_row(parent, "c₁ =", "5", row=3)
        e_a2 = self._entry_row(parent, "a₂ =", "2", row=4)
        e_b2 = self._entry_row(parent, "b₂ =", "-1", row=5)
        e_c2 = self._entry_row(parent, "c₂ =", "1", row=6)
        result_lbl = tk.Label(parent, text="x = ?, y = ?",
                              bg=self.bg_color, fg='white',
                              font=('Microsoft YaHei', 13, 'bold'))
        result_lbl.grid(row=7, column=0, columnspan=2, pady=12)

        def solve():
            try:
                a1, b1, c1 = float(e_a1.get()), float(e_b1.get()), float(e_c1.get())
                a2, b2, c2 = float(e_a2.get()), float(e_b2.get()), float(e_c2.get())
                det = a1 * b2 - a2 * b1
                if det == 0:
                    result_lbl.config(text="无解或无穷多解 (行列式=0)")
                    return
                x = (c1 * b2 - c2 * b1) / det
                y = (a1 * c2 - a2 * c1) / det
                result_lbl.config(text=f"x = {format_number(x)}\ny = {format_number(y)}")
                self._set_status("方程组求解完成")
            except Exception as ex:
                result_lbl.config(text=f"错误: {ex}")

        self._solve_btn(parent, solve, 8)

    def _build_cubic(self, parent):
        parent.configure(bg=self.bg_color)
        parent.columnconfigure(1, weight=1)
        tk.Label(parent, text="方程: a·x³ + b·x² + c·x + d = 0",
                 bg=self.bg_color, fg=self.accent_color,
                 font=('Microsoft YaHei', 12, 'bold')).grid(row=0, column=0, columnspan=2,
                                                           pady=(12, 8))
        e_a = self._entry_row(parent, "a =", "1", row=1)
        e_b = self._entry_row(parent, "b =", "-6", row=2)
        e_c = self._entry_row(parent, "c =", "11", row=3)
        e_d = self._entry_row(parent, "d =", "-6", row=4)
        result_lbl = tk.Label(parent, text="", bg=self.bg_color, fg='white',
                              font=('Microsoft YaHei', 11, 'bold'), justify='left')
        result_lbl.grid(row=5, column=0, columnspan=2, pady=12)

        def solve():
            try:
                a, b, c, d = float(e_a.get()), float(e_b.get()), float(e_c.get()), float(e_d.get())
                if a == 0:
                    result_lbl.config(text="a 不能为 0 (退化为二次方程)")
                    return
                # 归一化
                b, c, d = b / a, c / a, d / a
                # 卡尔达诺公式
                p = c - b * b / 3
                q = d - b * c / 3 + 2 * b ** 3 / 27
                disc = (q / 2) ** 2 + (p / 3) ** 3
                txt = f"判别式 Δ = {format_number(disc)}\n\n"
                if disc > 0:
                    u = (-q / 2 + math.sqrt(disc)) ** (1 / 3)
                    v = (-q / 2 - math.sqrt(disc)) ** (1 / 3)
                    x1 = u + v - b / 3
                    re_part = -(u + v) / 2 - b / 3
                    im_part = (u - v) * math.sqrt(3) / 2
                    txt += f"x₁ = {format_number(x1)} (实根)\n"
                    txt += f"x₂ = {format_number(re_part)}+{format_number(abs(im_part))}i\n"
                    txt += f"x₃ = {format_number(re_part)}-{format_number(abs(im_part))}i"
                elif disc == 0:
                    u = (-q / 2) ** (1 / 3)
                    x1 = 2 * u - b / 3
                    x2 = -u - b / 3
                    txt += f"x₁ = {format_number(x1)}\n"
                    txt += f"x₂ = x₃ = {format_number(x2)}"
                else:
                    # 三实根
                    phi = math.acos(-q / 2 / math.sqrt((-p / 3) ** 3))
                    x1 = 2 * math.sqrt(-p / 3) * math.cos(phi / 3) - b / 3
                    x2 = 2 * math.sqrt(-p / 3) * math.cos((phi + 2 * math.pi) / 3) - b / 3
                    x3 = 2 * math.sqrt(-p / 3) * math.cos((phi + 4 * math.pi) / 3) - b / 3
                    txt += f"x₁ = {format_number(x1)}\n"
                    txt += f"x₂ = {format_number(x2)}\n"
                    txt += f"x₃ = {format_number(x3)}"
                result_lbl.config(text=txt)
                self._set_status("三次方程求解完成")
            except Exception as ex:
                result_lbl.config(text=f"错误: {ex}")

        self._solve_btn(parent, solve, 6)

    def _build_custom_expr(self, parent):
        parent.configure(bg=self.bg_color)
        parent.columnconfigure(0, weight=1)
        tk.Label(parent, text="自定义表达式计算 (支持变量 x)",
                 bg=self.bg_color, fg=self.accent_color,
                 font=('Microsoft YaHei', 11, 'bold')).pack(pady=(12, 8))
        tips = tk.Label(parent,
                        text="函数: sin, cos, tan, log, log10, sqrt, exp, abs, factorial, pow\n"
                             "常量: pi, e  |  运算符: + - * / ** ( )  |  示例: sin(pi/2)+x**2",
                        bg=self.bg_color, fg='#888888', font=('Microsoft YaHei', 9),
                        justify='left')
        tips.pack(fill='x', padx=12)

        frm = tk.Frame(parent, bg=self.bg_color)
        frm.pack(fill='x', padx=12, pady=8)
        frm.columnconfigure(1, weight=1)
        tk.Label(frm, text="表达式:", bg=self.bg_color, fg='white',
                 font=('Microsoft YaHei', 11)).grid(row=0, column=0, sticky='e', padx=4)
        self.custom_expr = tk.Entry(frm, bg='#1e1e1e', fg='white',
                                    insertbackground='white', relief='flat',
                                    font=('Microsoft YaHei', 12))
        self.custom_expr.grid(row=0, column=1, sticky='ew', ipady=4, padx=4)
        self.custom_expr.insert(0, "sin(x) + x**2 / 4")

        tk.Label(frm, text="x =", bg=self.bg_color, fg='white',
                 font=('Microsoft YaHei', 11)).grid(row=1, column=0, sticky='e', padx=4)
        self.custom_x = tk.Entry(frm, bg='#1e1e1e', fg='white',
                                 insertbackground='white', relief='flat',
                                 font=('Microsoft YaHei', 12))
        self.custom_x.grid(row=1, column=1, sticky='ew', ipady=4, padx=4)
        self.custom_x.insert(0, "2")

        self.custom_result = tk.Label(parent, text="结果 = --",
                                      bg=self.bg_color, fg='white',
                                      font=('Microsoft YaHei', 14, 'bold'))
        self.custom_result.pack(pady=12)

        def eval_custom():
            try:
                expr = self.custom_expr.get()
                x = float(self.custom_x.get() or "0")
                allowed = {
                    'pi': math.pi, 'e': math.e, 'x': x,
                    'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                    'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
                    'log': math.log, 'log10': math.log10, 'log2': math.log2,
                    'sqrt': math.sqrt, 'exp': math.exp, 'abs': abs,
                    'factorial': math.factorial, 'pow': math.pow,
                    'ceil': math.ceil, 'floor': math.floor,
                    '__builtins__': {}
                }
                result = eval(expr, allowed, {})
                self.custom_result.config(text=f"结果 = {format_number(result)}")
                self._set_status(f"当 x={x} 时, {expr} = {format_number(result)}")
            except Exception as ex:
                self.custom_result.config(text=f"错误: {ex}")

        self._solve_btn(parent, eval_custom, None, pack=True)

    def _solve_btn(self, parent, cmd, row=None, pack=False):
        b = tk.Button(parent, text="✓ 求解 / 计算", command=cmd,
                      bg=self.btn_eq, fg='white',
                      activebackground=self.accent_color, activeforeground='white',
                      font=('Microsoft YaHei', 12, 'bold'), relief='flat', cursor='hand2',
                      padx=20, pady=8)
        if pack:
            b.pack(pady=8)
        else:
            b.grid(row=row, column=0, columnspan=2, pady=8, sticky='ew', padx=20)

    # ========================================================
    # 模块 5: 进制转换
    # ========================================================
    def _build_baseconv(self, parent):
        parent.columnconfigure(0, weight=1)

        tk.Label(parent, text="📊 进制转换器",
                 bg=self.bg_color, fg=self.accent_color,
                 font=('Microsoft YaHei', 14, 'bold')).pack(pady=(12, 4))

        # 输入区
        in_frame = tk.Frame(parent, bg=self.bg_color)
        in_frame.pack(fill='x', padx=12, pady=8)
        in_frame.columnconfigure(1, weight=1)

        tk.Label(in_frame, text="输入数字:", bg=self.bg_color, fg='white',
                 font=('Microsoft YaHei', 11)).grid(row=0, column=0, sticky='e', padx=4, pady=4)
        self.base_input = tk.Entry(in_frame, bg='#1e1e1e', fg='white',
                                   insertbackground='white', relief='flat',
                                   font=('Microsoft YaHei', 13))
        self.base_input.grid(row=0, column=1, sticky='ew', ipady=6, padx=4)
        self.base_input.insert(0, "255")
        self.base_input.bind('<KeyRelease>', lambda e: self._do_baseconv())

        tk.Label(in_frame, text="源进制:", bg=self.bg_color, fg='white',
                 font=('Microsoft YaHei', 11)).grid(row=1, column=0, sticky='e', padx=4, pady=4)
        self.base_from = tk.StringVar(value="十进制")
        combo1 = ttk.Combobox(in_frame, textvariable=self.base_from,
                              values=["二进制", "八进制", "十进制", "十六进制",
                                      "三十二进制", "六十四进制"],
                              state='readonly', font=('Microsoft YaHei', 11))
        combo1.grid(row=1, column=1, sticky='ew', ipady=4, padx=4)
        combo1.bind('<<ComboboxSelected>>', lambda e: self._do_baseconv())

        # 输出区
        self.base_results = {}
        bases = [("二进制 (BIN)", 2), ("八进制 (OCT)", 8), ("十进制 (DEC)", 10),
                 ("十六进制 (HEX)", 16), ("三十二进制", 32), ("六十四进制", 64)]

        out_frame = tk.Frame(parent, bg=self.bg_color)
        out_frame.pack(fill='both', expand=True, padx=12, pady=8)
        out_frame.columnconfigure(0, weight=1)

        for i, (name, base) in enumerate(bases):
            row_frame = tk.Frame(out_frame, bg='#1e1e1e')
            row_frame.grid(row=i, column=0, sticky='ew', pady=3)
            row_frame.columnconfigure(1, weight=1)
            tk.Label(row_frame, text=name, bg='#1e1e1e', fg=self.accent_color,
                     font=('Microsoft YaHei', 10, 'bold'), width=16,
                     anchor='w').grid(row=0, column=0, padx=6, pady=4, sticky='w')
            lbl = tk.Label(row_frame, text="--", bg='#1e1e1e', fg='white',
                           font=('Consolas', 11), anchor='w')
            lbl.grid(row=0, column=1, sticky='ew', padx=6, pady=4)
            self.base_results[name] = lbl

        # 快速按钮
        quick = tk.Frame(parent, bg=self.bg_color)
        quick.pack(fill='x', padx=12, pady=(0, 8))
        for text, val in [("0", "0"), ("255", "255"), ("1024", "1024"),
                           ("65535", "65535"), ("3.14", "3.1415926535")]:
            def go(v=val):
                self.base_input.delete(0, tk.END)
                self.base_input.insert(0, v)
                self.base_from.set("十进制")
                self._do_baseconv()
            tk.Button(quick, text=text, command=go, bg=self.btn_color, fg='white',
                      relief='flat', cursor='hand2',
                      font=('Microsoft YaHei', 10)).pack(side='left', padx=2, expand=True, fill='x')

        self._do_baseconv()

    BASE_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/"

    def _parse_number(self, s, base):
        """解析数字，支持小数部分"""
        s = s.strip()
        if base == 10:
            return float(s)
        # 整数部分 + 小数部分
        if '.' in s:
            int_part, frac_part = s.split('.', 1)
        else:
            int_part, frac_part = s, ""
        # 整数部分
        int_val = 0
        for ch in int_part.upper():
            idx = self.BASE_CHARS.index(ch) if ch in self.BASE_CHARS else int(ch, base)
            if idx >= base:
                raise ValueError(f"字符 '{ch}' 不属于 {base} 进制")
            int_val = int_val * base + idx
        # 小数部分
        frac_val = 0.0
        for i, ch in enumerate(frac_part.upper()):
            idx = self.BASE_CHARS.index(ch) if ch in self.BASE_CHARS else int(ch, base)
            if idx >= base:
                raise ValueError(f"字符 '{ch}' 不属于 {base} 进制")
            frac_val += idx / (base ** (i + 1))
        return int_val + frac_val

    def _format_number(self, val, base):
        if val < 0:
            return "-" + self._format_number(-val, base)
        int_val = int(val)
        frac = val - int_val
        # 整数部分
        if int_val == 0:
            s = "0"
        else:
            digits = []
            while int_val > 0:
                digits.append(self.BASE_CHARS[int_val % base])
                int_val //= base
            s = ''.join(reversed(digits))
        # 小数部分（最多8位）
        if frac > 1e-12:
            s += '.'
            for _ in range(10):
                frac *= base
                d = int(frac)
                s += self.BASE_CHARS[d]
                frac -= d
                if frac < 1e-10:
                    break
        return s

    def _do_baseconv(self):
        try:
            s = self.base_input.get().strip()
            if not s:
                for lbl in self.base_results.values():
                    lbl.config(text="--")
                return
            base_map = {"二进制": 2, "八进制": 8, "十进制": 10,
                        "十六进制": 16, "三十二进制": 32, "六十四进制": 64}
            base = base_map[self.base_from.get()]
            val = self._parse_number(s, base)
            for name, b in [("二进制 (BIN)", 2), ("八进制 (OCT)", 8),
                            ("十进制 (DEC)", 10), ("十六进制 (HEX)", 16),
                            ("三十二进制", 32), ("六十四进制", 64)]:
                self.base_results[name].config(text=self._format_number(val, b))
            self._set_status(f"值 = {format_number(val)}")
        except Exception as ex:
            for lbl in self.base_results.values():
                lbl.config(text="--")
            self._set_status(f"✗ {ex}")

    # ========================================================
    # 模块 6: 函数绘图
    # ========================================================
    def _build_plot(self, parent):
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)

        ctrl = tk.Frame(parent, bg=self.bg_color)
        ctrl.grid(row=0, column=0, sticky='ew', padx=8, pady=6)
        ctrl.columnconfigure(1, weight=1)

        tk.Label(ctrl, text="y =", bg=self.bg_color, fg='white',
                 font=('Microsoft YaHei', 11)).grid(row=0, column=0, padx=4)
        self.plot_fn = tk.Entry(ctrl, bg='#1e1e1e', fg='white',
                                insertbackground='white', relief='flat',
                                font=('Microsoft YaHei', 12))
        self.plot_fn.grid(row=0, column=1, sticky='ew', ipady=4)
        self.plot_fn.insert(0, "sin(x)")

        tk.Label(ctrl, text="x范围:", bg=self.bg_color, fg='white',
                 font=('Microsoft YaHei', 11)).grid(row=0, column=2, padx=4)
        self.plot_xmin = tk.Entry(ctrl, bg='#1e1e1e', fg='white',
                                  insertbackground='white', relief='flat',
                                  font=('Microsoft YaHei', 11), width=6)
        self.plot_xmin.grid(row=0, column=3, ipady=4)
        self.plot_xmin.insert(0, "-10")

        tk.Label(ctrl, text="~", bg=self.bg_color, fg='white').grid(row=0, column=4)

        self.plot_xmax = tk.Entry(ctrl, bg='#1e1e1e', fg='white',
                                  insertbackground='white', relief='flat',
                                  font=('Microsoft YaHei', 11), width=6)
        self.plot_xmax.grid(row=0, column=5, ipady=4)
        self.plot_xmax.insert(0, "10")

        tk.Button(ctrl, text="🎨 绘制", command=self._do_plot,
                  bg=self.btn_eq, fg='white', relief='flat', cursor='hand2',
                  font=('Microsoft YaHei', 11, 'bold')).grid(row=0, column=6, padx=4)

        # Canvas
        self.canvas = tk.Canvas(parent, bg='#0a0a0a', highlightthickness=0,
                                cursor='crosshair')
        self.canvas.grid(row=1, column=0, sticky='nsew', padx=8, pady=(0, 8))
        self.canvas.bind('<Configure>', lambda e: self._do_plot())

        # 预设函数
        preset = tk.Frame(parent, bg=self.bg_color)
        preset.grid(row=2, column=0, sticky='ew', padx=8, pady=(0, 8))
        tk.Label(preset, text="快速函数:", bg=self.bg_color, fg=self.accent_color,
                 font=('Microsoft YaHei', 10, 'bold')).pack(side='left', padx=4)
        for fn in ["sin(x)", "cos(x)", "tan(x)", "x**2", "x**3", "log(x)",
                   "exp(x)", "1/x", "sqrt(x)", "abs(x)"]:
            def plot_fn(f=fn):
                self.plot_fn.delete(0, tk.END)
                self.plot_fn.insert(0, f)
                self._do_plot()
            tk.Button(preset, text=fn, command=plot_fn,
                      bg=self.btn_color, fg='white', relief='flat',
                      cursor='hand2', font=('Microsoft YaHei', 9)).pack(side='left', padx=2)

        self._do_plot()

    def _do_plot(self):
        try:
            w = self.canvas.winfo_width()
            h = self.canvas.winfo_height()
            if w < 2 or h < 2:
                return
            self.canvas.delete('all')
            expr = self.plot_fn.get().strip()
            xmin = float(self.plot_xmin.get() or "-10")
            xmax = float(self.plot_xmax.get() or "10")
            if xmax <= xmin:
                return
            # 计算所有点
            allowed = {
                'pi': math.pi, 'e': math.e,
                'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
                'log': math.log, 'log10': math.log10, 'log2': math.log2,
                'sqrt': math.sqrt, 'exp': math.exp, 'abs': abs,
                'factorial': math.factorial, 'pow': math.pow,
                'ceil': math.ceil, 'floor': math.floor,
                '__builtins__': {}
            }
            n_points = min(600, max(200, w * 2))
            xs, ys = [], []
            for i in range(n_points):
                x = xmin + (xmax - xmin) * i / (n_points - 1)
                try:
                    allowed['x'] = x
                    y = eval(expr, allowed, {})
                    if isinstance(y, complex):
                        y = y.real
                    if -1e10 < y < 1e10:
                        ys.append(y)
                        xs.append(x)
                    else:
                        ys.append(None)
                        xs.append(x)
                except Exception:
                    ys.append(None)
                    xs.append(x)
            # 自动缩放 y
            valid = [v for v in ys if v is not None]
            if not valid:
                self.canvas.create_text(w // 2, h // 2, text="无有效数据", fill='red',
                                        font=('Microsoft YaHei', 14))
                return
            ymin = min(valid)
            ymax = max(valid)
            if ymin == ymax:
                ymin -= 1
                ymax += 1
            margin = (ymax - ymin) * 0.1
            ymin -= margin
            ymax += margin
            # 坐标轴
            def tx(x):
                return 40 + (x - xmin) / (xmax - xmin) * (w - 60)
            def ty(y):
                return (h - 30) - (y - ymin) / (ymax - ymin) * (h - 50)
            # 绘制网格
            self.canvas.create_rectangle(40, 10, w - 20, h - 30, outline='#333333',
                                          width=1)
            # 横向网格
            for i in range(5):
                yv = ymin + (ymax - ymin) * i / 4
                py = ty(yv)
                self.canvas.create_line(40, py, w - 20, py, fill='#222222')
                self.canvas.create_text(35, py, text=f"{yv:.2f}", fill='#666666',
                                        font=('Consolas', 8), anchor='e')
            # 纵向网格
            for i in range(5):
                xv = xmin + (xmax - xmin) * i / 4
                px = tx(xv)
                self.canvas.create_line(px, 10, px, h - 30, fill='#222222')
                self.canvas.create_text(px, h - 20, text=f"{xv:.2f}", fill='#666666',
                                        font=('Consolas', 8))
            # x=0 与 y=0
            if xmin <= 0 <= xmax:
                self.canvas.create_line(tx(0), 10, tx(0), h - 30, fill='#555555', width=1)
            if ymin <= 0 <= ymax:
                self.canvas.create_line(40, ty(0), w - 20, ty(0), fill='#555555', width=1)
            # 绘制曲线
            points = []
            for xi, yi in zip(xs, ys):
                if yi is None:
                    if len(points) >= 4:
                        self.canvas.create_line(*points, fill='#4a9eff', width=2,
                                                smooth=True)
                    points = []
                else:
                    points.extend([tx(xi), ty(yi)])
            if len(points) >= 4:
                self.canvas.create_line(*points, fill='#4a9eff', width=2, smooth=True)
            # 标题
            self.canvas.create_text(w // 2, 24, text=f"y = {expr}", fill='#4a9eff',
                                    font=('Microsoft YaHei', 11, 'bold'))
            self._set_status(f"绘制完成: y={expr}, x∈[{xmin},{xmax}]")
        except Exception as ex:
            try:
                self.canvas.create_text(
                    self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2,
                    text=f"绘制失败: {ex}", fill='red', font=('Microsoft YaHei', 11))
            except Exception:
                pass
            self._set_status(f"✗ {ex}")

    # ========================================================
    # 模块 7: 统计计算
    # ========================================================
    def _build_stats(self, parent):
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(2, weight=1)

        tk.Label(parent, text="📈 统计分析器",
                 bg=self.bg_color, fg=self.accent_color,
                 font=('Microsoft YaHei', 14, 'bold')).grid(row=0, column=0,
                                                           pady=(12, 4))
        tk.Label(parent, text="输入数字(逗号/空格/换行分隔):",
                 bg=self.bg_color, fg='white',
                 font=('Microsoft YaHei', 11)).grid(row=1, column=0,
                                                    sticky='w', padx=12, pady=4)

        self.stat_input = tk.Text(parent, bg='#1e1e1e', fg='white',
                                  insertbackground='white', relief='flat',
                                  font=('Consolas', 11), height=4)
        self.stat_input.grid(row=2, column=0, sticky='nsew', padx=12, pady=4)
        self.stat_input.insert('1.0', "12 15 18 22 25 28 30 33 35 40\n5 8 12 15 20 22 25 28 30 35")
        self.stat_input.bind('<KeyRelease>', lambda e: self._do_stats())

        # 按钮
        btn_bar = tk.Frame(parent, bg=self.bg_color)
        btn_bar.grid(row=3, column=0, sticky='ew', padx=12, pady=4)
        tk.Button(btn_bar, text="🎲 生成随机数", command=self._gen_random,
                  bg=self.btn_color, fg='white', relief='flat', cursor='hand2',
                  font=('Microsoft YaHei', 10)).pack(side='left', padx=2)
        tk.Button(btn_bar, text="🔢 连续数列", command=self._gen_seq,
                  bg=self.btn_color, fg='white', relief='flat', cursor='hand2',
                  font=('Microsoft YaHei', 10)).pack(side='left', padx=2)
        tk.Button(btn_bar, text="🧹 清空",
                  command=lambda: (self.stat_input.delete('1.0', tk.END),
                                   self._do_stats()),
                  bg=self.btn_color, fg='white', relief='flat', cursor='hand2',
                  font=('Microsoft YaHei', 10)).pack(side='left', padx=2)

        # 结果区
        self.stat_results_frame = tk.Frame(parent, bg=self.bg_color)
        self.stat_results_frame.grid(row=4, column=0, sticky='nsew', padx=12, pady=8)
        self.stat_results_frame.columnconfigure(0, weight=1)
        self.stat_results_frame.columnconfigure(1, weight=1)

        self.stat_labels = {}
        metric_names = [
            ("数据个数", "count"), ("总和", "sum"), ("最小值", "min"),
            ("最大值", "max"), ("极差", "range"), ("算术平均", "mean"),
            ("几何平均", "gmean"), ("调和平均", "hmean"), ("中位数", "median"),
            ("众数", "mode"), ("方差", "var"), ("标准差", "std"),
            ("标准差 (样本)", "std_s"), ("平均偏差", "mad"),
            ("变异系数 CV", "cv"), ("四分位间距 IQR", "iqr")
        ]
        for i, (name, key) in enumerate(metric_names):
            row = i // 2
            col = i % 2
            cell = tk.Frame(self.stat_results_frame, bg='#1e1e1e')
            cell.grid(row=row, column=col, sticky='nsew', padx=3, pady=3)
            tk.Label(cell, text=name, bg='#1e1e1e', fg=self.accent_color,
                     font=('Microsoft YaHei', 9, 'bold'), anchor='w').pack(
                anchor='w', padx=8, pady=(4, 0))
            lbl = tk.Label(cell, text="--", bg='#1e1e1e', fg='white',
                           font=('Consolas', 11, 'bold'), anchor='e')
            lbl.pack(anchor='e', padx=8, pady=(0, 4))
            self.stat_labels[key] = lbl

        # 排序后的数据
        sorted_frame = tk.Frame(parent, bg=self.bg_color)
        sorted_frame.grid(row=5, column=0, sticky='ew', padx=12, pady=(0, 8))
        tk.Label(sorted_frame, text="📋 排序后:", bg=self.bg_color,
                 fg=self.accent_color, font=('Microsoft YaHei', 10, 'bold')).pack(
            anchor='w')
        self.stat_sorted = tk.Label(sorted_frame, text="--", bg='#1e1e1e', fg='white',
                                    font=('Consolas', 10), wraplength=500, justify='left',
                                    anchor='w')
        self.stat_sorted.pack(fill='x', pady=4, ipady=4, padx=4)

        parent.rowconfigure(5, weight=0)
        self._do_stats()

    def _gen_random(self):
        nums = [round(random.gauss(50, 15), 2) for _ in range(30)]
        self.stat_input.delete('1.0', tk.END)
        self.stat_input.insert('1.0', ' '.join(str(n) for n in nums))
        self._do_stats()

    def _gen_seq(self):
        nums = list(range(1, 21)) + [random.randint(1, 20) for _ in range(10)]
        self.stat_input.delete('1.0', tk.END)
        self.stat_input.insert('1.0', ' '.join(str(n) for n in nums))
        self._do_stats()

    def _do_stats(self):
        try:
            text = self.stat_input.get('1.0', tk.END).strip()
            if not text:
                for lbl in self.stat_labels.values():
                    lbl.config(text="--")
                self.stat_sorted.config(text="--")
                return
            tokens = re.split(r'[\s,;，；\n\r\t]+', text)
            data = []
            for t in tokens:
                t = t.strip()
                if not t:
                    continue
                try:
                    data.append(float(t))
                except Exception:
                    continue
            if not data:
                for lbl in self.stat_labels.values():
                    lbl.config(text="--")
                self.stat_sorted.config(text="无有效数字")
                return
            n = len(data)
            data_sorted = sorted(data)
            s = sum(data)
            mean_val = s / n
            variance = sum((x - mean_val) ** 2 for x in data) / n
            variance_s = sum((x - mean_val) ** 2 for x in data) / (n - 1) if n > 1 else 0
            std_val = math.sqrt(variance)
            std_s = math.sqrt(variance_s)
            mad = sum(abs(x - mean_val) for x in data) / n
            mn, mx = min(data), max(data)
            rng = mx - mn
            # 几何平均
            try:
                if all(x > 0 for x in data):
                    gmean = math.exp(sum(math.log(x) for x in data) / n)
                else:
                    gmean = None
            except Exception:
                gmean = None
            # 调和平均
            try:
                if all(x != 0 for x in data):
                    hmean = n / sum(1 / x for x in data)
                else:
                    hmean = None
            except Exception:
                hmean = None
            # 中位数
            if n % 2 == 1:
                median = data_sorted[n // 2]
            else:
                median = (data_sorted[n // 2 - 1] + data_sorted[n // 2]) / 2
            # 众数
            freq = {}
            for x in data:
                key = round(x, 6)
                freq[key] = freq.get(key, 0) + 1
            max_freq = max(freq.values())
            modes = [k for k, v in freq.items() if v == max_freq]
            if max_freq == 1:
                mode_str = "无"
            else:
                mode_str = ", ".join(format_number(m) for m in modes[:5])
                if len(modes) > 5:
                    mode_str += "..."
            # 变异系数
            cv = std_val / abs(mean_val) if mean_val != 0 else None
            # 四分位间距
            def quartile(sorted_data, q):
                pos = (len(sorted_data) - 1) * q
                lower = int(pos)
                upper = min(lower + 1, len(sorted_data) - 1)
                frac = pos - lower
                return sorted_data[lower] * (1 - frac) + sorted_data[upper] * frac
            q1 = quartile(data_sorted, 0.25)
            q3 = quartile(data_sorted, 0.75)
            iqr = q3 - q1
            # 填充
            def fmt(v):
                if v is None:
                    return "N/A"
                return format_number(v)
            self.stat_labels['count'].config(text=str(n))
            self.stat_labels['sum'].config(text=fmt(s))
            self.stat_labels['min'].config(text=fmt(mn))
            self.stat_labels['max'].config(text=fmt(mx))
            self.stat_labels['range'].config(text=fmt(rng))
            self.stat_labels['mean'].config(text=fmt(mean_val))
            self.stat_labels['gmean'].config(text=fmt(gmean))
            self.stat_labels['hmean'].config(text=fmt(hmean))
            self.stat_labels['median'].config(text=fmt(median))
            self.stat_labels['mode'].config(text=mode_str)
            self.stat_labels['var'].config(text=fmt(variance))
            self.stat_labels['std'].config(text=fmt(std_val))
            self.stat_labels['std_s'].config(text=fmt(std_s))
            self.stat_labels['mad'].config(text=fmt(mad))
            self.stat_labels['cv'].config(text=fmt(cv))
            self.stat_labels['iqr'].config(text=fmt(iqr))
            # 排序数据
            sorted_str = ", ".join(format_number(x) for x in data_sorted[:50])
            if len(data_sorted) > 50:
                sorted_str += f"... (+{len(data_sorted) - 50} 更多)"
            self.stat_sorted.config(text=sorted_str)
            self._set_status(f"统计完成: n={n}, 平均={format_number(mean_val)}, σ={fmt(std_val)}")
        except Exception as ex:
            self._set_status(f"✗ {ex}")


# ============================================================
# 主入口
# ============================================================
def main():
    root = tk.Tk()
    root.title("多功能计算器 - Multi Calculator")
    # 初始化尺寸
    root.minsize(400, 550)
    root.geometry("480x720")
    try:
        root.iconbitmap(default='')
    except Exception:
        pass
    app = MultiCalculator(root)
    root.mainloop()


if __name__ == '__main__':
    main()
