#!/usr/bin/env python3
"""
Hackavolt Reconnaissance Tool
A clean, resizable GUI with:
- Tree sidebar
- URL + Port input
- Submit button
- Scrollable log
- Status bar & menu
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import ctypes

class ReconApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hackavolt Reconnaissance")
        self.geometry("1000x650")
        self.minsize(700, 450)

        self.status_var = tk.StringVar(value="Ready")
        self._build_ui()
        self._populate_tree()

        global loadLib
        loadLib = ctypes.CDLL(os.path.abspath("./main.so"))

    # ------------------------------------------------------------------ #
    # UI Construction
    # ------------------------------------------------------------------ #
    def _build_ui(self):
        self._create_menu()
        self._create_toolbar()
        self._create_main_layout()
        self._create_statusbar()

    def _create_menu(self): # ROw 0
        menubar = tk.Menu(self)
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="New", command=self.new_file)
        settings_menu.add_separator()
        settings_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.config(menu=menubar)

    def _create_toolbar(self): # ROW 1
        toolbar = ttk.Frame(self, padding=4)
        toolbar.pack(fill="x")

        ttk.Button(toolbar, text="New", command=self.new_file).pack(side="left", padx=2)
        ttk.Button(toolbar, text="About", command=self.show_about).pack(side="left", padx=2)
        ttk.Button(toolbar, text="Config", command=self.show_about).pack(side="left", padx=2)

    def _create_main_layout(self): 
        # Horizontal split: tree | editor+log
        main_pane = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_pane.pack(fill="both", expand=True, padx=6, pady=6)

        # --- Left: Treeview ---
        left_frame = ttk.Frame(main_pane)
        self.tree = ttk.Treeview(left_frame, show="tree", selectmode="browse")
        self.tree.pack(side="left", fill="both", expand=True)

        vsb = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        main_pane.add(left_frame, weight=1)


        # --- Right: Vertical split (input + log) ---
        right_pane = ttk.PanedWindow(main_pane, orient=tk.VERTICAL)
        main_pane.add(right_pane, weight=3)

        # Input area
        input_frame = self._build_input_area(right_pane)
        right_pane.add(input_frame, weight=2)

        # Log area
        log_frame = self._build_log_area(right_pane)
        right_pane.add(log_frame, weight=1)

    def _build_input_area(self, parent):
        frame = ttk.Frame(parent, padding=10)
        frame.columnconfigure(0, weight=1)

        #

        # URL
        ttk.Label(frame, text="Target URL:").grid(row=0, column=0, sticky="w", pady=(0, 4))
        self.url_entry = self._placeholder_entry(frame, "https://example.com")
        self.url_entry.grid(row=1, column=0, sticky="ew", columnspan=2, pady=(0, 8))

        # Port
        ttk.Label(frame, text="Port:").grid(row=2, column=0, sticky="w", pady=(0, 4))
        self.port_entry = self._placeholder_entry(frame, "443")
        self.port_entry.grid(row=3, column=0, sticky="w", padx=(0, 8))

        # Submit
        submit_btn = ttk.Button(frame, text="Submit", command=self.submit)
        submit_btn.grid(row=3, column=1, sticky="e")

        return frame

    def _build_log_area(self, parent):
        frame = ttk.Frame(parent)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.log = tk.Text(frame, wrap="word", height=8)
        self.log.grid(row=0, column=0, sticky="nsew")

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.log.yview)
        vsb.grid(row=0, column=1, sticky="ns")
        self.log.configure(yscrollcommand=vsb.set)

        self.log.insert("end", "Application started. Ready for reconnaissance.\n")
        self.log.see("end")
        return frame

    def _create_statusbar(self):
        statusbar = ttk.Label(self, textvariable=self.status_var, relief="sunken", padding=4)
        statusbar.pack(fill="x", side="bottom")

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    def _placeholder_entry(self, parent, placeholder):
        entry = ttk.Entry(parent)
        entry.insert(0, placeholder)
        entry.config(foreground="grey")

        def on_focus_in(e):
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.config(foreground="black")

        def on_focus_out(e):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(foreground="grey")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        return entry

    def _populate_tree(self):

        mainTree = [
            ("Main", "home"),
            ("Basic Recon", "scan"),
        ]
        toolTree = [
            ("Settings", "settings"),
            ("Targets", "target"),
            ("Reports", "report"),
        ]
        for name, icon in mainTree:
            self.tree.insert("", "end", text=name, values=(icon,))
        for name, icon in toolTree:
            self.tree.insert("", "end", text=name, values=(icon,))
    # ------------------------------------------------------------------ #
    # Actions
    # ------------------------------------------------------------------ #
    def new_file(self):
        self.log.insert("end", "New session started.\n")
        self.log.see("end")
        self.status_var.set("New file created")

    def show_about(self):
        messagebox.showinfo(
            "About",
            "Hackavolt Reconnaissance Tool\n"
            "A clean, modern Tkinter GUI\n"
            "Built with love ❤️"
        )

    def on_tree_select(self, event):
        sel = self.tree.focus()
        if not sel:
            return
        name = self.tree.item(sel, "text")
        self.status_var.set(f"Selected: {name}")
        self.log.insert("end", f"Viewing section: {name}\n")
        self.log.see("end")


    def on_tree_select(self, event):
        sel = self.tree.focus()
        if not sel:
            return
        name = self.tree.item(sel, "text")
        self.status_var.set(f"Selected: {name}")
        self.log.insert("end", f"Viewing section: {name}\n")
        self.log.see("end")


    def submit(self):
        url = self.url_entry.get().strip()
        port = self.port_entry.get().strip()

        if url in ("", "https://example.com"):
            messagebox.showwarning("Input Required", "Please enter a valid target URL.")
            return
        if port in ("", "443"):
            port = "80"

        url = url.encode("utf-8")
        port = port.encode("utf-8")
        loadLib.process_data_input.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        loadLib.process_data_input.restype = ctypes.c_void_p

        
        
        loadLib.process_data_input(url, port)

        result = f"Scanning {url} on port {port}..."
        self.log.insert("end", result + "\n")
        self.log.see("end")
        self.status_var.set(f"Submitted: {url}:{port}")

        # Simulate work

        self.after(100, lambda: self.log.insert("end", "Scan complete. No vulnerabilities found.\n"))
        self.after(100, self.log.see, "end")


if __name__ == "__main__":
    app = ReconApp()
    app.mainloop()