from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

import auth
from i18n import get_lang, set_lang, tr
from widgets import (COLORS, FONT, RoundButton, RoundedCard, load_logo,
                     reset_logo_cache)

LANG_CHOICES = [("en", "EN"), ("fr", "FR"), ("mg", "MG")]


class LoginApp(tk.Tk):
    def __init__(self, first_run: bool = False):
        super().__init__()
        reset_logo_cache()
        self.title("Vet XLS Studio \u2014 Sign in")
        self.configure(bg=COLORS["bg"])
        self.geometry("420x560")
        self.resizable(False, False)
        self.user: auth.User | None = None
        self._first_run = first_run

        self.card = RoundedCard(self, radius=22)
        self.card.place(relx=0.5, rely=0.52, anchor="c", width=360, height=440)

        self.lang_buttons: dict[str, RoundButton] = {}
        bar = tk.Frame(self, bg=COLORS["bg"])
        bar.place(relx=1.0, x=-22, y=18, anchor="ne")
        for code, label in LANG_CHOICES:
            btn = RoundButton(bar, label,
                              command=lambda c=code: self._pick_lang(c),
                              diameter=28, font=(FONT, 8, "bold"),
                              tooltip={"en": "English", "fr": "Français",
                                       "mg": "Malagasy"}[code])
            btn.pack(side="left", padx=3)
            self.lang_buttons[code] = btn
        self._paint_langs()

        self._build_body()
        self._refresh_texts()
        self.bind("<Return>", lambda e: self._do_login())
        self.after(10, self._center)

    def _center(self):
        self.update_idletasks()
        w = max(self.winfo_width(), 420)
        h = max(self.winfo_height(), 560)
        x = max((self.winfo_screenwidth() - w) // 2, 0)
        y = max((self.winfo_screenheight() - h) // 3, 0)
        self.geometry(f"420x560+{x}+{y}")

    def _build_body(self):
        c = self.card.inner
        self.logo = tk.Label(c, image=load_logo(60), bg=COLORS["card"])
        self.logo.pack(pady=(14, 0))
        self.title_lbl = tk.Label(c, text="Vet XLS Studio", bg=COLORS["card"],
                                  fg=COLORS["text"], font=(FONT, 17, "bold"))
        self.title_lbl.pack()
        self.sub_lbl = tk.Label(c, bg=COLORS["card"], fg=COLORS["muted"],
                                font=(FONT, 9))
        self.sub_lbl.pack()

        form = tk.Frame(c, bg=COLORS["card"])
        form.pack(fill="x", padx=34, pady=(16, 0))

        self.f_user = tk.Label(form, bg=COLORS["card"], fg=COLORS["muted"],
                               font=(FONT, 9))
        self.f_user.grid(row=0, column=0, sticky="w")
        self.e_user = tk.Entry(form, relief="flat", bg=COLORS["input"],
                               fg=COLORS["text"], font=(FONT, 11),
                               highlightthickness=1,
                               highlightbackground=COLORS["border"],
                               highlightcolor=COLORS["accent"])
        self.e_user.grid(row=1, column=0, sticky="ew", ipady=7)

        self.f_pass = tk.Label(form, bg=COLORS["card"], fg=COLORS["muted"],
                               font=(FONT, 9))
        self.f_pass.grid(row=2, column=0, sticky="w", pady=(12, 0))
        self.e_pass = tk.Entry(form, show="\u2022", relief="flat",
                               bg=COLORS["input"], fg=COLORS["text"], font=(FONT, 11),
                               highlightthickness=1,
                               highlightbackground=COLORS["border"],
                               highlightcolor=COLORS["accent"])
        self.e_pass.grid(row=3, column=0, sticky="ew", ipady=7, pady=(2, 0))
        form.grid_columnconfigure(0, weight=1)

        self.btn_signin = RoundButton(c, command=self._do_login, diameter=46,
                                      pill=True)
        self.btn_signin.pack(pady=(18, 2))
        self.btn_register = RoundButton(c, command=self._open_register,
                                        diameter=42, pill=True,
                                        bg=COLORS["neutral"])
        self.btn_register.pack()

        self.status = tk.Label(c, text="", bg=COLORS["card"],
                               fg=COLORS["danger"], font=(FONT, 9))
        self.status.pack(pady=(8, 0))

        self.hint = tk.Label(c, bg=COLORS["card"], fg=COLORS["muted"],
                             font=(FONT, 8, "italic"))

    def _refresh_texts(self):
        self.sub_lbl.config(text=tr("app_subtitle"))
        self.f_user.config(text=tr("f_username"))
        self.f_pass.config(text=tr("f_password"))
        self.btn_signin.set_text(tr("signin_btn"))
        self.btn_register.set_text(tr("create_btn"))
        self.hint.config(text=tr("hint_first_run"))
        if self._first_run:
            self.hint.pack_forget()
            self.hint.pack(side="bottom", pady=(6, 10))
        else:
            self.hint.pack_forget()

    # ----------------------------------------------------------- lang --
    def _pick_lang(self, code: str):
        set_lang(code)
        self._paint_langs()
        self._refresh_texts()
        self.after(10, self._center)

    def _paint_langs(self):
        cur = get_lang()
        for code, btn in self.lang_buttons.items():
            btn.recolor(COLORS["accent"] if code == cur else "#B9C4CE")

    # ---------------------------------------------------------- login --
    def _error(self, key: str):
        self.status.config(text=tr(key))

    def _do_login(self):
        user = auth.authenticate(self.e_user.get(), self.e_pass.get())
        if user is None:
            self._error("err_wrong")
            return
        self.user = user
        self.destroy()

    # ------------------------------------------------------- register --
    def _open_register(self):
        dlg = tk.Toplevel(self)
        dlg.title(tr("title_create_account"))
        dlg.configure(bg=COLORS["card"])
        dlg.transient(self)
        dlg.resizable(False, False)

        box = tk.Frame(dlg, bg=COLORS["card"], padx=24, pady=20)
        box.pack()
        fields = []

        labels = [tr("f_username"), tr("f_display"), tr("f_password"),
                  tr("f_confirm")]
        entries = []
        for i, lbl in enumerate(labels):
            tk.Label(box, text=lbl, bg=COLORS["card"], fg=COLORS["muted"],
                     font=(FONT, 9)).grid(row=i * 2, column=0, sticky="w",
                                          pady=(8, 2))
            e = tk.Entry(box, relief="flat", bg=COLORS["input"], fg=COLORS["text"],
                         font=(FONT, 11), highlightthickness=1,
                         highlightbackground=COLORS["border"],
                         highlightcolor=COLORS["accent"],
                         show="\u2022" if i >= 2 else "")
            e.grid(row=i * 2 + 1, column=0, sticky="ew", ipady=6)
            entries.append(e)
        box.grid_columnconfigure(0, weight=1)

        err_lbl = tk.Label(box, text="", bg=COLORS["card"],
                           fg=COLORS["danger"], font=(FONT, 9))
        err_lbl.grid(row=8, column=0, sticky="w", pady=(8, 0))

        def on_register():
            u, d, p, p2 = (e.get() for e in entries)
            if not u.strip() or not p or not d.strip():
                err_lbl.config(text=tr("err_fill"))
                return
            if p != p2:
                err_lbl.config(text=tr("err_mismatch"))
                return
            new_user, err = auth.create_user(u, p, d)
            if new_user is None:
                err_lbl.config(text=tr(err))
                return
            self.e_user.delete(0, "end")
            self.e_user.insert(0, new_user.username)
            self.e_pass.delete(0, "end")
            dlg.destroy()

        btns = tk.Frame(box, bg=COLORS["card"])
        btns.grid(row=9, column=0, pady=(14, 0))
        RoundButton(btns, "Cancel", command=dlg.destroy, diameter=42,
                    pill=True, bg=COLORS["neutral"]).pack(side="left", padx=6)
        RoundButton(btns, tr("btn_register"), command=on_register,
                    diameter=42, pill=True).pack(side="left", padx=6)

    def set_title_labels(self):  # kept for symmetry/future use
        pass

