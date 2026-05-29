# -*- coding: utf-8 -*-
"""
test_configure_methods.py
=========================
Interactive test file for all individual configure_* methods on CTkLineChart.

How to run
----------
    python test_configure_methods.py

Layout
------
- Left panel  : scrollable list of buttons grouped by category.
- Right panel : the live CTkLineChart widget.

Each button calls the corresponding configure_* method with a preset value.
"""

import sys
import os
import tkinter as tk
import customtkinter as ctk
import threading
import random

# ---------------------------------------------------------------------------
# Make sure the local src/ is importable when running from the project root
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from ctkchart import CTkLineChart, CTkLine

# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------
BG_DARK   = "#0f1117"
BG_PANEL  = "#1a1d27"
BTN_BG    = "#2c2f4a"
BTN_HOVER = "#3d4170"
BTN_ACT   = "#5865f2"
SEP_COLOR = "#2e3155"
TEXT_MAIN = "#e0e0f0"
TEXT_DIM  = "#8888aa"
ACCENT2   = "#57f287"
ACCENT    = "#5865f2"

FONT_TITLE = ("Segoe UI", 13, "bold")
FONT_CAT   = ("Segoe UI", 10, "bold")
FONT_BTN   = ("Segoe UI", 9)


# ---------------------------------------------------------------------------
# Flat button widget
# ---------------------------------------------------------------------------
class FlatButton(tk.Frame):
    def __init__(self, master, text, command, width=340, **kw):
        super().__init__(master, bg=BTN_BG, cursor="hand2",
                         highlightthickness=1, highlightbackground=SEP_COLOR)
        self._cmd = command
        self._lbl = tk.Label(
            self, text=text, font=FONT_BTN,
            bg=BTN_BG, fg=TEXT_MAIN,
            padx=8, pady=4, anchor="w"
        )
        self._lbl.pack(fill="x")
        for w in (self, self._lbl):
            w.bind("<Enter>",    self._on_enter)
            w.bind("<Leave>",    self._on_leave)
            w.bind("<Button-1>", self._on_click)

    def _on_enter(self, _):
        self.config(bg=BTN_HOVER, highlightbackground=ACCENT)
        self._lbl.config(bg=BTN_HOVER)

    def _on_leave(self, _):
        self.config(bg=BTN_BG, highlightbackground=SEP_COLOR)
        self._lbl.config(bg=BTN_BG)

    def _on_click(self, _):
        self.config(bg=BTN_ACT)
        self._lbl.config(bg=BTN_ACT)
        self.after(150, self._on_leave, None)
        self._cmd()


# ---------------------------------------------------------------------------
# Scrollable frame
# ---------------------------------------------------------------------------
class ScrollableFrame(tk.Frame):
    def __init__(self, master, **kw):
        container = tk.Frame(master, bg=BG_PANEL)
        container.pack(fill="both", expand=True)

        self._canvas = tk.Canvas(container, bg=BG_PANEL, highlightthickness=0)
        vsb = tk.Scrollbar(container, orient="vertical",
                           command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        super().__init__(self._canvas, bg=BG_PANEL, **kw)
        self._window = self._canvas.create_window((0, 0), window=self, anchor="nw")

        self.bind("<Configure>", self._on_frame_configure)
        self._canvas.bind("<Configure>", self._on_canvas_configure)
        self._canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_frame_configure(self, _):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_canvas_configure(self, e):
        self._canvas.itemconfig(self._window, width=e.width)

    def _on_mousewheel(self, e):
        self._canvas.yview_scroll(-1 * (e.delta // 120), "units")


# ---------------------------------------------------------------------------
# Main application
# ---------------------------------------------------------------------------
class TestApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CTkLineChart & CTkLine configure_* Test Suite")
        self.geometry("1300x780")
        self.configure(fg_color=BG_DARK)
        self.resizable(True, True)

        self._build_header()
        self._build_body()
        self._build_chart()
        self._build_lines()
        self._start_data_loop()
        self._build_controls()

    # ------------------------------------------------------------------ Header
    def _build_header(self):
        hdr = tk.Frame(self, bg=BG_PANEL, height=52)
        hdr.pack(fill="x", side="top")
        hdr.pack_propagate(False)
        tk.Label(
            hdr, text="CTkLineChart  configure_*  Test Suite",
            font=FONT_TITLE, bg=BG_PANEL, fg=TEXT_MAIN
        ).pack(side="left", padx=20, pady=12)
        tk.Label(
            hdr, text="Click any button to apply the configuration live ->",
            font=("Segoe UI", 9), bg=BG_PANEL, fg=TEXT_DIM
        ).pack(side="right", padx=20)
        tk.Frame(self, bg=SEP_COLOR, height=1).pack(fill="x")

    # ------------------------------------------------------------------ Body
    def _build_body(self):
        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill="both", expand=True)

        # Left – scrollable buttons
        left = tk.Frame(body, bg=BG_PANEL, width=430)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)
        self._scroll = ScrollableFrame(left)

        # Right – chart area
        self._right = tk.Frame(body, bg=BG_DARK)
        self._right.pack(side="left", fill="both", expand=True)

        # Status bar
        self._status_var = tk.StringVar(value="Ready")
        tk.Label(
            self._right, textvariable=self._status_var,
            font=("Segoe UI", 9), bg=BG_DARK, fg=ACCENT2,
            anchor="w"
        ).pack(side="bottom", fill="x", padx=20, pady=4)

    # ------------------------------------------------------------------ Chart
    def _build_chart(self):
        self._x_vals = tuple("T{}".format(i) for i in range(1, 21))

        self._chart = CTkLineChart(
            master=self._right,
            width=800,
            height=430,
            axis_size=2,
            bg_color="#191919",
            fg_color="#191919",
            axis_color="#3a3a5c",
            data_font_style=("Segoe UI", 10, "bold"),
            axis_font_style=("Segoe UI", 9, "normal"),
            y_axis_values=(0, 100),
            y_axis_label_count=5,
            y_axis_section_count=5,
            y_axis_section_color="#2a2a4a",
            y_axis_font_color="#8888aa",
            y_axis_data_font_color="#aaaacc",
            y_axis_data="Y",
            x_axis_values=self._x_vals,
            x_axis_label_count=10,
            x_axis_section_count=5,
            x_axis_section_color="#2a2a4a",
            x_axis_font_color="#8888aa",
            x_axis_data_font_color="#aaaacc",
            x_axis_data="Time",
            x_axis_point_spacing="auto",
            pointer_state="enabled",
            pointer_color="#5865f2",
            pointer_size=2,
        )
        self._chart.pack(pady=20, padx=20)

    # ------------------------------------------------------------------ Lines
    def _build_lines(self):
        self._line1 = CTkLine(
            master=self._chart,
            color="#5865f2",
            size=2,
            style="normal",
            point_highlight="enabled",
            point_highlight_color="#5865f2",
            point_highlight_size=6,
            fill="enabled",
            fill_color="#1e2140",
        )
        self._line2 = CTkLine(
            master=self._chart,
            color="#57f287",
            size=2,
            style="normal",
            point_highlight="enabled",
            point_highlight_color="#57f287",
            point_highlight_size=6,
        )

    # ------------------------------------------------------------------ Live data loop
    def _start_data_loop(self):
        """Spawn a daemon thread that pushes one data point to each line every second.
        The thread itself never touches tkinter; it schedules updates via after()."""
        self._running = True

        def _loop():
            while self._running:
                # Schedule the actual chart update on the main (tkinter) thread
                self.after(0, self._push_data_point)
                threading.Event().wait(1.0)   # sleep 1 second without blocking Tk

        t = threading.Thread(target=_loop, daemon=True)
        t.start()

        # Stop the thread cleanly when the window is closed
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _push_data_point(self):
        """Called on the main thread every second to add one new value to each line."""
        try:
            self._chart.show_data(line=self._line1, data=[random.randint(20, 90)])
            self._chart.show_data(line=self._line2, data=[random.randint(10, 80)])
        except Exception:
            pass   # chart may have been destroyed

    def _on_close(self):
        self._running = False
        self.destroy()

    # ------------------------------------------------------------------ Status
    def _set_status(self, msg):
        self._status_var.set("Applied:  " + msg)

    # ================================================================== All Controls
    def _build_controls(self):
        p = self._scroll  # parent for all buttons

        # ---- Helpers to create controls in loop to save space ----
        def make_buttons(title, values, config_func_name, is_color=False):
            self._section(p, title)
            for v in values:
                lbl_v = repr(v) if isinstance(v, str) and not is_color else str(v)
                btn_text = f"{config_func_name.replace('configure_', '')} = {lbl_v}"
                
                # capture the current v and func_name in a lambda
                def cmd(val=v, f_name=config_func_name):
                    getattr(self._chart, f_name)(val)
                    self._set_status(f"{f_name}({repr(val)})")
                
                self._btn(p, btn_text, cmd, swatch=v if is_color else None)

        # CHART CONFIGURE METHODS
        make_buttons("Width", [400, 500, 600, 700, 800], "configure_width")
        make_buttons("Height", [280, 340, 430, 500, 560], "configure_height")
        make_buttons("Axis Size", [1, 2, 4, 6], "configure_axis_size")
        make_buttons("X Axis Point Spacing", ["auto", 20, 35, 50, 70], "configure_x_axis_point_spacing")
        
        make_buttons("Background Color (bg_color)", ["#191919", "#0d0d1a", "#1a1a2e", "#0f1117", "#2c1810"], "configure_bg_color", True)
        make_buttons("Axis Color (axis_color)", ["#3a3a5c", "#5865f2", "#ff4444", "#44ff88", "#aaaaaa"], "configure_axis_color", True)
        make_buttons("Foreground Color (fg_color)", ["#191919", "#101020", "#1e1e2e", "#0a0a15"], "configure_fg_color", True)
        
        make_buttons("Data Font Style", [("Segoe UI", 9, "bold"), ("Arial", 10, "bold"), ("Courier New", 9, "normal")], "configure_data_font_style")
        make_buttons("Axis Font Style", [("Segoe UI", 8, "normal"), ("Arial", 9, "bold"), ("Consolas", 8, "normal")], "configure_axis_font_style")
        
        make_buttons("Y Axis Values (min, max)", [(0, 100), (-50, 50), (0, 200), (10, 80), (0, 1000)], "configure_y_axis_values")
        make_buttons("Y Axis Precision", [0, 1, 2, 3], "configure_y_axis_precision")
        make_buttons("Y Axis Font Color", ["#8888aa", "#ffffff", "#5865f2", "#57f287", "#ff9900"], "configure_y_axis_font_color", True)
        make_buttons("Y Axis Data Font Color", ["#aaaacc", "#ffffff", "#5865f2", "#57f287"], "configure_y_axis_data_font_color", True)
        make_buttons("Y Axis Label Count", [0, 3, 5, 8, 10], "configure_y_axis_label_count")
        make_buttons("Y Axis Data Title", ["Y", "Value", "Score", "Temp", ""], "configure_y_axis_data")
        make_buttons("Y Axis Data Position", ["top", "side"], "configure_y_axis_data_position")
        make_buttons("Y Axis Section Count", [0, 3, 5, 8], "configure_y_axis_section_count")
        make_buttons("Y Axis Section Color", ["#2a2a4a", "#3d4170", "#444444", "#1e3a1e"], "configure_y_axis_section_color", True)
        make_buttons("Y Axis Section Style", ["normal", "dashed"], "configure_y_axis_section_style")
        make_buttons("Y Axis Section Style Type (dash, gap)", [(100, 50), (60, 30), (20, 10), (10, 5)], "configure_y_axis_section_style_type")
        make_buttons("Y Space", [0, 10, 20, 40], "configure_y_space")

        make_buttons("X Axis Data Title", ["Time", "Date", "Index", "Step", ""], "configure_x_axis_data")
        make_buttons("X Axis Data Position", ["top", "side"], "configure_x_axis_data_position")
        make_buttons("X Axis Font Color", ["#8888aa", "#ffffff", "#5865f2", "#57f287", "#ff9900"], "configure_x_axis_font_color", True)
        make_buttons("X Axis Data Font Color", ["#aaaacc", "#ffffff", "#5865f2", "#57f287"], "configure_x_axis_data_font_color", True)
        make_buttons("X Axis Label Count", [0, 5, 10, 15, 20], "configure_x_axis_label_count")
        make_buttons("X Axis Section Count", [0, 3, 5, 8], "configure_x_axis_section_count")
        make_buttons("X Axis Section Color", ["#2a2a4a", "#3d4170", "#444444", "#3a1e1e"], "configure_x_axis_section_color", True)
        make_buttons("X Axis Section Style", ["normal", "dashed"], "configure_x_axis_section_style")
        make_buttons("X Axis Section Style Type (dash, gap)", [(100, 50), (60, 30), (20, 10), (10, 5)], "configure_x_axis_section_style_type")
        make_buttons("X Space", [0, 10, 20, 40], "configure_x_space")
        
        # New for ctkchart: x_axis_values and x_axis_display_values_indices
        make_buttons("X Axis Values", [tuple("ABCDEFGHIJKLMNOPQRST"), tuple(str(i) for i in range(1, 21)), self._x_vals], "configure_x_axis_values")
        make_buttons("X Axis Display Values Indices", [(0, 4, 9, 14, 19), (0, 9, 19), tuple(range(0, 20, 2))], "configure_x_axis_display_values_indices")

        make_buttons("Pointer State", ["enabled", "disabled"], "configure_pointer_state")
        make_buttons("Pointer Color", ["#5865f2", "#ff4444", "#57f287", "#ffffff", "#ff9900"], "configure_pointer_color", True)
        make_buttons("Pointer Size", [1, 2, 3, 5, 8], "configure_pointer_size")
        make_buttons("Pointer Lock", ["enabled", "disabled"], "configure_pointer_lock")
        make_buttons("Pointing Values Precision", [0, 1, 2, 3], "configure_pointing_values_precision")

        # ---- pointing_callback_function ----
        self._section(p, "Pointing Callback Function")
        def _cb_noop(x, vals): pass
        def _cb_print(x, vals): print("[Pointer Callback]  x={}  values={}".format(x, vals))

        for label, fn in [("None / no-op callback", _cb_noop), ("print to console", _cb_print)]:
            self._btn(p, label, lambda f=fn, l=label: (
                self._chart.configure_pointing_callback_function(f),
                self._set_status("configure_pointing_callback_function  ->  " + l)
            ))


        # ======================================================================
        # CTkLine configure_* methods
        # Apply to self._line1 (blue, with fill) and self._line2 (green)
        # ======================================================================
        tk.Frame(p, bg="#5865f2", height=2).pack(fill="x", pady=(16, 0), padx=0)
        tk.Label(
            p, text="  CTkLine  configure_*  (line1 = blue   |   line2 = green)",
            font=("Segoe UI", 10, "bold"), bg="#20243a", fg="#e0e0f0",
            anchor="w", pady=6
        ).pack(fill="x")
        tk.Frame(p, bg="#5865f2", height=2).pack(fill="x", pady=(0, 4), padx=0)

        def make_line_buttons(title, values, config_func_name, is_color=False):
            self._section(p, title)
            for v in values:
                val, lbl = v if isinstance(v, tuple) and len(v) == 2 and isinstance(v[1], str) else (v, "")
                lbl_v = repr(val) if isinstance(val, str) and not is_color else str(val)
                
                # Line 1
                btn_text_1 = f"line1.{config_func_name}({lbl_v}) {lbl}"
                def cmd1(v_cmd=val, f_name=config_func_name):
                    getattr(self._line1, f_name)(v_cmd)
                    self._set_status(f"line1.{f_name}({repr(v_cmd)})")
                self._btn(p, btn_text_1, cmd1, swatch=val if is_color else None)
                
                # Line 2
                btn_text_2 = f"line2.{config_func_name}({lbl_v}) {lbl}"
                def cmd2(v_cmd=val, f_name=config_func_name):
                    getattr(self._line2, f_name)(v_cmd)
                    self._set_status(f"line2.{f_name}({repr(v_cmd)})")
                self._btn(p, btn_text_2, cmd2, swatch=val if is_color else None)

        colors_line = [("#5865f2", "blue"), ("#57f287", "green"), ("#ff4444", "red"), ("#ff9900", "orange"), ("#ffffff", "white")]
        make_line_buttons("Line Color", colors_line, "configure_color", True)
        make_line_buttons("Line Size (thickness)", [1, 2, 3, 5, 8], "configure_size")
        make_line_buttons("Line Style", ["normal", "dashed", "dotted"], "configure_style")
        make_line_buttons("Line Style Type (segment, gap)", [(4, 4), (8, 4), (12, 6), (2, 8), (20, 5)], "configure_style_type")
        make_line_buttons("Point Highlight", ["enabled", "disabled"], "configure_point_highlight")
        make_line_buttons("Point Highlight Size", [2, 4, 6, 10, 16], "configure_point_highlight_size")
        make_line_buttons("Point Highlight Color", colors_line, "configure_point_highlight_color", True)
        make_line_buttons("Line Fill", ["enabled", "disabled"], "configure_fill")
        make_line_buttons("Line Fill Color", [("#1e2140", "dark blue"), ("#1e3a1e", "dark green"), ("#3a1e1e", "dark red"), ("#2a2010", "dark orange"), ("#252525", "dark grey")], "configure_fill_color", True)


        # Bottom spacer
        tk.Frame(p, bg=BG_PANEL, height=40).pack(fill="x")

    # ================================================================== Helpers
    def _section(self, parent, title):
        """Section separator + title label."""
        tk.Frame(parent, bg=SEP_COLOR, height=1).pack(fill="x", pady=(10, 0), padx=6)
        tk.Label(
            parent, text="   " + title,
            font=FONT_CAT, bg=BG_PANEL, fg=TEXT_DIM,
            anchor="w"
        ).pack(fill="x", pady=(3, 1))

    def _btn(self, parent, text, cmd, swatch=None):
        """Button row, optionally with a color swatch."""
        row = tk.Frame(parent, bg=BG_PANEL)
        row.pack(fill="x", padx=8, pady=2)

        if swatch:
            tk.Frame(row, bg=swatch, width=14, height=14).pack(
                side="left", padx=(2, 6), pady=4)

        FlatButton(row, text=text, command=cmd).pack(side="left", fill="x")


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app = TestApp()
    app.mainloop()
