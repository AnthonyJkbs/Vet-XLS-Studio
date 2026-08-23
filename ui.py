from __future__ import annotations

import os
import shutil
import subprocess
import tkinter as tk
from dataclasses import asdict
from datetime import date, datetime
from tkinter import messagebox, ttk

import auth
import charts
from i18n import tr, fmt_date, month_name
import paths
from models import Store
from sample_data import build_sample
from widgets import (COLORS, FONT, MonthCalendar, RoundButton, RoundedCard,
                     StatCard,
                     get_theme, reset_logo_cache, set_theme, load_logo,
                     shade)
from workbook import generate_workbook

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORE_PATH = paths.writable("store.json")
XLS_PATH = os.path.join(paths.APP_DIR,
                        "vet_clinic_database.xlsx")


def entity_list():
    return [(tr("entity_owners"), "owners"),
            (tr("entity_pets"), "pets"),
            (tr("entity_appointments"), "appointments"),
            (tr("entity_treatments"), "treatments")]


COLUMNS = {
    "owners": [("id", "h_id", 48), ("name", "h_name", 170),
               ("phone", "h_phone", 130), ("email", "h_email", 210),
               ("address", "h_address", 240)],
    "pets": [("id", "h_id", 48), ("name", "h_name", 120),
             ("species", "h_species", 90), ("breed", "h_breed", 150),
             ("sex", "h_sex", 50), ("hospitalized", "h_hosp", 60),
             ("birth_date", "h_birth", 100),
             ("microchip", "h_microchip", 130), ("owner_id", "h_owner", 180)],
    "appointments": [("id", "h_id", 48), ("date", "h_date", 100),
                     ("time", "h_time", 60), ("pet_id", "h_pet", 190),
                     ("vet", "h_vet", 110), ("reason", "h_reason", 200),
                     ("status", "h_status", 100)],
    "treatments": [("id", "h_id", 48), ("date", "h_date", 100),
                   ("type", "h_type", 110), ("pet_id", "h_pet", 190),
                   ("description", "h_description", 220),
                   ("vet", "h_vet", 110), ("next_due", "h_nextdue", 100)],
}

VETS_SUGGEST = ["Dr. Kim", "Dr. Alvarez", "Dr. Osei", "Dr. Novak", "Dr. Reyes"]
SPECIES_SUGGEST = ["Dog", "Cat", "Bird", "Rabbit", "Hamster", "Reptile"]


class VetApp(tk.Tk):
    def __init__(self, user: auth.User):
        super().__init__()
        reset_logo_cache()
        self.title("Vet XLS Studio")
        self.configure(bg=COLORS["bg"])
        self.geometry("1120x740")
        self.minsize(980, 660)
        self.user = user
        self.logout_requested = False
        self.theme_reloaded = False
        self._day_filter = None
        self.upcoming_title = None
        self.store: Store = Store.load(STORE_PATH)
        self.entity_var = tk.StringVar(value=tr("entity_owners"))

        self._setup_styles()
        self.ver_lbl = tk.Label(
            self, text="v 0.5 (beta)", bg=COLORS["bg"],
            fg=COLORS["shell_muted"], font=(FONT, 8))
        self.ver_lbl.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-4)
        self._build_header()
        self._build_clock()
        self._build_stats()
        self._build_middle()
        self._build_manage()
        self._build_empty()
        self.refresh()

    def _build_clock(self):
        self.clock_lbl = tk.Label(self, bg=COLORS["bg"],
                                  fg=COLORS["shell_muted"],
                                  font=(FONT, 9, "bold"))
        self.clock_lbl.place(relx=1.0, x=-18, y=6, anchor="ne")
        self._tick()

    def _tick(self):
        if not self.winfo_exists():
            return
        now = datetime.now()
        self.clock_lbl.config(
            text=f"{fmt_date(now, 'full')}  \u00B7  "
                 f"{now.strftime('%H:%M:%S')}")
        self.after(1000, self._tick)

    def _setup_styles(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Card.Treeview", background=COLORS["card"],
                        fieldbackground=COLORS["card"], foreground=COLORS["text"],
                        rowheight=32, font=(FONT, 10), borderwidth=0,
                        relief="flat")
        style.map("Card.Treeview",
                  background=[("selected", COLORS["accent_soft"])],
                  foreground=[("selected", COLORS["accent_dark"])])
        style.configure("Card.Treeview.Heading", background=COLORS["card"],
                        foreground=COLORS["muted"], font=(FONT, 9, "bold"),
                        relief="flat", borderwidth=0, padding=(4, 8))
        style.map("Card.Treeview.Heading", background=[("active", COLORS["card"])])
        style.configure("Entity.TCombobox", fieldbackground=COLORS["input"],
                        background=COLORS["input"],
                        foreground=COLORS["text"],
                        arrowcolor=COLORS["accent"], borderwidth=0,
                        font=(FONT, 11))
        self.option_add("*TCombobox*Listbox.font", (FONT, 11))
        style.configure("Form.TCombobox", fieldbackground=COLORS["input"],
                        background=COLORS["input"],
                        foreground=COLORS["text"],
                        arrowcolor=COLORS["accent"], font=(FONT, 10))

    def _build_header(self):
        bar = tk.Frame(self, bg=COLORS["bg"])
        bar.pack(fill="x", padx=26, pady=(20, 12))
        left = tk.Frame(bar, bg=COLORS["bg"])
        left.pack(side="left")
        self._logo_img = load_logo(40)
        logo_lbl = tk.Label(left, image=self._logo_img, bg=COLORS["bg"],
                            cursor="hand2")
        logo_lbl.pack(side="left", padx=(0, 10))
        logo_lbl.bind("<Button-1>",
                      lambda e: messagebox.showinfo("Vet XLS Studio",
                                                    "Made by Leez",
                                                    parent=self))
        titles = tk.Frame(left, bg=COLORS["bg"])
        titles.pack(side="left")
        tk.Label(titles, text="Vet XLS Studio", bg=COLORS["bg"],
                 fg=COLORS["shell_text"],
                 font=(FONT, 19, "bold")).pack(anchor="w")
        tk.Label(titles, text=tr("app_subtitle"), bg=COLORS["bg"],
                 fg=COLORS["shell_muted"], font=(FONT, 10)).pack(
            anchor="w")

        right = tk.Frame(bar, bg=COLORS["bg"])
        right.pack(side="right")

        role_txt = (tr("role_admin") if self.user.role == "admin"
                    else tr("role_user"))
        chip = tk.Frame(right, bg=COLORS["accent_soft"])
        tk.Label(chip,
                 text=f"\U0001F464 {self.user.display_name} \u00B7 {role_txt}",
                 bg=COLORS["accent_soft"], fg=COLORS["accent_dark"],
                 font=(FONT, 9, "bold")).pack(side="left", padx=(12, 8),
                                              pady=8)
        chip.pack(side="right", padx=(0, 12))

        self.btn_logout = RoundButton(right, "\u23FB", command=self._logout,
                                      diameter=40, bg=COLORS["neutral"],
                                      tooltip=tr("lbl_logout"))
        self.btn_logout.pack(side="right", padx=(0, 12))
        self.btn_print = RoundButton(right, "\u2399",
                                     command=self.print_report,
                                     diameter=40, bg=COLORS["neutral"],
                                     tooltip=tr("tip_print"))
        self.btn_print.pack(side="right", padx=(0, 8))
        theme_icon = "\u2600" if get_theme() == "dark" else "\u263E"
        self.btn_theme = RoundButton(right, theme_icon,
                                     command=self._toggle_theme,
                                     diameter=40, bg=COLORS["neutral"],
                                     tooltip=tr("tip_theme"))
        self.btn_theme.pack(side="right", padx=(0, 8))
        self.btn_xls = RoundButton(right, tr("generate_xls"),
                                   command=self.generate_xls,
                                   diameter=44, pill=True, tooltip=tr("tip_xls"))
        self.btn_xls.pack(side="right")

    def open_quick_note(self):
        dlg = tk.Toplevel(self)
        dlg.title(tr("note_title"))
        dlg.configure(bg=COLORS["card"])
        dlg.transient(self)
        dlg.resizable(False, False)
        box = tk.Frame(dlg, bg=COLORS["card"], padx=16, pady=14)
        box.pack()
        lb = tk.Listbox(box, width=48, height=8, relief="flat",
                        bg=COLORS["input"], fg=COLORS["text"],
                        font=(FONT, 10), activestyle="none",
                        selectbackground=COLORS["accent"],
                        selectforeground="#FFFFFF",
                        highlightthickness=1,
                        highlightbackground=COLORS["border"])
        lb.pack()

        def reload_list():
            lb.delete(0, "end")
            if not self.store.notes:
                lb.insert("end", tr("notes_empty"))
                return
            for n in self.store.notes:
                text = n["text"]
                preview = text if len(text) <= 46 else text[:43] + "…"
                lb.insert("end", f"{fmt_date(n['date'])}  ·  {preview}")

        def selected_idx():
            if not self.store.notes or not lb.curselection():
                return None
            return lb.curselection()[0]

        def refresh_badge():
            self.card_notes.set_value(len(self.store.notes))

        def open_editor(initial, on_submit):
            ed = tk.Toplevel(dlg)
            ed.title(tr("note_title"))
            ed.configure(bg=COLORS["card"])
            ed.transient(dlg)
            ed.resizable(False, False)
            ebox = tk.Frame(ed, bg=COLORS["card"], padx=16, pady=14)
            ebox.pack()
            txt = tk.Text(ebox, width=42, height=7, relief="flat",
                          bg=COLORS["input"], fg=COLORS["text"],
                          font=(FONT, 10), padx=10, pady=8,
                          highlightthickness=1,
                          highlightbackground=COLORS["border"],
                          highlightcolor=COLORS["accent"])

            def on_save():
                text = txt.get("1.0", "end").strip()
                if not text:
                    return
                on_submit(text)
                try:
                    dlg.grab_set()
                except tk.TclError:
                    pass
                ed.destroy()

            btns = tk.Frame(ebox, bg=COLORS["card"])
            RoundButton(btns, tr("word_cancel"), command=ed.destroy,
                        diameter=38, pill=True, bg=COLORS["neutral"]).pack(
                side="left", padx=6)
            RoundButton(btns, "\u2713  " + tr("btn_save"),
                        command=on_save, diameter=38, pill=True).pack(
                side="left", padx=6)
            txt.insert("1.0", initial)
            txt.pack()
            btns.pack(pady=(10, 0))
            ed._on_save = on_save
            self._center(ed)
            ed.update_idletasks()
            try:
                dlg.grab_release()
                ed.wait_visibility()
                ed.grab_set()
                txt.focus_set()
            except tk.TclError:
                pass

        def on_new():
            def submit(text):
                self.store.add_note(text)
                self._autosave()
                refresh_badge()
                reload_list()
            open_editor("", submit)

        def on_edit():
            i = selected_idx()
            if i is None:
                return
            note = self.store.notes[i]

            def submit(text):
                self.store.update_note(i, text)
                self._autosave()
                reload_list()
            open_editor(note["text"], submit)

        def on_delete():
            i = selected_idx()
            if i is None:
                return
            if messagebox.askyesno(tr("note_title"),
                                   tr("notes_confirm_del"), parent=dlg):
                self.store.delete_note(i)
                self._autosave()
                refresh_badge()
                reload_list()

        btns = tk.Frame(box, bg=COLORS["card"])
        RoundButton(btns, "\u2795  " + tr("notes_new"), command=on_new,
                    diameter=38, pill=True).pack(side="left", padx=4)
        RoundButton(btns, tr("notes_edit"), command=on_edit,
                    diameter=38, pill=True, bg=COLORS["neutral"]).pack(
            side="left", padx=4)
        RoundButton(btns, tr("notes_delete"), command=on_delete,
                    diameter=38, pill=True, bg=COLORS["danger"]).pack(
            side="left", padx=4)
        RoundButton(btns, tr("notes_close"), command=dlg.destroy,
                    diameter=38, pill=True, bg=COLORS["neutral"]).pack(
            side="left", padx=4)
        lb.bind("<Double-Button-1>", lambda e: on_edit())
        reload_list()
        btns.pack(pady=(10, 0))
        self._center(dlg)
        dlg._lb = lb
        dlg._reload = reload_list
        dlg._on_new = on_new
        dlg._on_edit = on_edit
        dlg._on_delete = on_delete
        dlg.update_idletasks()
        try:
            dlg.wait_visibility()
            dlg.grab_set()
            lb.focus_set()
        except tk.TclError:
            pass
        dlg.wait_window()

    def _logout(self):
        self.logout_requested = True
        self.destroy()

    def _toggle_theme(self):
        set_theme("light" if get_theme() == "dark" else "dark")
        self.theme_reloaded = True
        self.destroy()

    def edit_hospital_config(self):
        s = self.store

        def apply(values):
            try:
                cap = int(str(values.get("capacity")).strip())
            except (TypeError, ValueError):
                messagebox.showwarning(tr("title_missing"),
                                       tr("err_number"), parent=self)
                return
            if cap <= 0:
                messagebox.showwarning(tr("title_missing"),
                                       tr("err_number"), parent=self)
                return
            s.hospital_capacity = cap
            s.night_vet_name = str(values.get("night_vet_name") or "").strip()
            s.night_vet_phone = str(
                values.get("night_vet_phone") or "").strip()
            self._autosave()
            self.after(10, self.refresh)

        self._open_form(tr("tip_hosp_edit"), [
            dict(k="capacity", label=tr("f_capacity"), required=True),
            dict(k="night_vet_name", label=tr("f_night_vet")),
            dict(k="night_vet_phone", label=tr("h_phone")),
        ], initial={"capacity": s.hospital_capacity,
                    "night_vet_name": s.night_vet_name,
                    "night_vet_phone": s.night_vet_phone}, on_done=apply)

    def _logout(self):
        self.logout_requested = True
        self.destroy()

    def _toggle_theme(self):
        set_theme("light" if get_theme() == "dark" else "dark")
        self.theme_reloaded = True
        self.destroy()

    def print_report(self):
        path = generate_workbook(self.store, XLS_PATH)
        exe = shutil.which("lp") or shutil.which("lpr")
        if exe and subprocess.run([exe, path],
                                  capture_output=True).returncode == 0:
            messagebox.showinfo(tr("title_print"), tr("msg_print_sent"),
                                parent=self)
        else:
            messagebox.showwarning(tr("title_print"),
                                   tr("msg_no_printer", path=path),
                                   parent=self)

    def _build_stats(self):
        row = tk.Frame(self, bg=COLORS["bg"])
        row.pack(fill="x", padx=20)
        for i in range(6):
            row.grid_columnconfigure(i, weight=1, uniform="stat")
        palette = (
            ("#16A34A", "#DFF2E4"),   # green
            ("#0284C7", "#E0F0FB"),   # blue
            ("#7C3AED", "#ECE5FC"),   # violet
            ("#D97706", "#FCEFD9"),   # amber
            ("#DB2777", "#FBE3EF"),   # pink
            ("#0D9488", "#DCF2F0"),   # teal
        )
        self.card_pets = StatCard(row, "\U0001F415", tr("stat_pets"),
                                  chip=palette[0][1],
                                  value_color=palette[0][0])
        self.card_owners = StatCard(row, "\U0001F464", tr("stat_owners"),
                                    chip=palette[1][1],
                                    value_color=palette[1][0])
        self.card_docs = StatCard(row, "\U0001FA7A", tr("stat_doctors"),
                                  chip=palette[2][1],
                                  value_color=palette[2][0])
        self.card_appts = StatCard(row, "\U0001F4C5", tr("stat_appts"),
                                   chip=palette[3][1],
                                   value_color=palette[3][0])
        self.card_vax = StatCard(row, "\U0001F498", tr("stat_vax"),
                                 chip=palette[4][1],
                                 value_color=palette[4][0])
        self.card_notes = StatCard(row, "\u270E", tr("st_notes"),
                                   chip=palette[5][1],
                                   value_color=palette[5][0])
        for i, card in enumerate((self.card_pets, self.card_owners,
                                  self.card_docs, self.card_appts,
                                  self.card_vax, self.card_notes)):
            card.grid(row=0, column=i, sticky="nsew", padx=3, pady=5)
        self.card_notes.configure(cursor="hand2")
        self.card_notes.bind("<Button-1>",
                             lambda e: self.open_quick_note())

    def _build_middle(self):
        mid = tk.Frame(self, bg=COLORS["bg"])
        mid.pack(fill="x", padx=26)
        for i in range(4):
            mid.grid_columnconfigure(i, weight=3, uniform="mid")

        ch_card = RoundedCard(mid, height=210)
        ch_card.grid(row=0, column=0, sticky="nsew", padx=5)
        self.chart_title = tk.Label(ch_card.inner, text="", bg=COLORS["card"],
                                    fg=COLORS["muted"],
                                    font=(FONT, 10, "bold"))
        self.chart_title.pack(anchor="w")
        self.chart_canvas = tk.Canvas(ch_card.inner, bg=COLORS["card"],
                                      height=150, highlightthickness=0)
        self.chart_canvas.pack(fill="both", expand=True)
        self.chart_canvas.bind("<Configure>",
                               lambda e: self._redraw_chart())

        cal_card = RoundedCard(mid, height=210)
        cal_card.grid(row=0, column=1, sticky="nsew", padx=5)
        tk.Label(cal_card.inner, text=tr("calendar_title"),
                 bg=COLORS["card"], fg=COLORS["muted"],
                 font=(FONT, 10, "bold")).pack(anchor="w")
        self.calendar = MonthCalendar(
            cal_card.inner, get_marks=self._cal_marks,
            on_pick=self._on_day_pick, height=158)
        self.calendar.pack(fill="both", expand=True)

        ho_card = RoundedCard(mid, height=210)
        ho_card.grid(row=0, column=2, sticky="nsew", padx=5)
        head = tk.Frame(ho_card.inner, bg=COLORS["card"])
        head.pack(fill="x")
        tk.Label(head, text=tr("hosp_title"), bg=COLORS["card"],
                 fg=COLORS["muted"], font=(FONT, 10, "bold")).pack(side="left")
        RoundButton(head, "\u270E  ", command=self.edit_hospital_config,
                    diameter=30, font=(FONT, 10, "bold"),
                    bg=COLORS["accent"], tooltip=tr("tip_hosp_edit")
                    ).pack(side="right")
        self.hosp_canvas = tk.Canvas(ho_card.inner, bg=COLORS["card"],
                                     height=150, highlightthickness=0)
        self.hosp_canvas.pack(fill="both", expand=True)
        self.hosp_canvas.bind("<Configure>",
                              lambda e: self._redraw_hospital())

        up_card = RoundedCard(mid, height=210)
        up_card.grid(row=0, column=3, sticky="nsew", padx=5)
        self.upcoming_title = tk.Label(up_card.inner,
                                       text=tr("next_appointments"),
                                       bg=COLORS["card"], fg=COLORS["muted"],
                                       font=(FONT, 10, "bold"))
        self.upcoming_title.pack(anchor="w")
        self.upcoming_canvas = tk.Canvas(up_card.inner, bg=COLORS["card"],
                                         height=140, highlightthickness=0)
        self.upcoming_canvas.pack(fill="both", expand=True)
        self.upcoming_canvas.bind("<Configure>",
                                  lambda e: self._redraw_upcoming())

    def _cal_marks(self):
        days = {a.date for a in self.store.appointments}
        days |= {t.date for t in self.store.treatments}
        days |= {t.next_due for t in self.store.treatments if t.next_due}
        return days

    def _on_day_pick(self, iso):
        self._day_filter = None if (iso is None
                                    or iso == self._day_filter) else iso
        if self.upcoming_title is not None:
            if self._day_filter:
                self.upcoming_title.config(
                    text=f"{tr('next_appointments')}"
                         f"  \u00B7  {fmt_date(self._day_filter)}")
            else:
                self.upcoming_title.config(text=tr("next_appointments"))
        self._redraw_upcoming()

    def _build_manage(self):
        self.manage_card = RoundedCard(self)
        strip = tk.Frame(self.manage_card.inner, bg=COLORS["card"])
        strip.pack(fill="x", pady=(0, 10))
        tk.Label(strip, text=tr("manage_lbl"), bg=COLORS["card"],
                 fg=COLORS["text"], font=(FONT, 12, "bold")).pack(side="left",
                                                                 padx=(0, 14))

        self.entity_box = ttk.Combobox(
            strip, textvariable=self.entity_var, state="readonly",
            values=[label for label, _ in entity_list()],
            font=(FONT, 11), width=28)
        self.entity_box.configure(style="Entity.TCombobox")
        self.entity_box.pack(side="left")
        self.entity_box.bind("<<ComboboxSelected>>",
                             lambda e: (self._rebuild_table(),
                                        self._redraw_chart()))

        actions = tk.Frame(strip, bg=COLORS["card"])
        actions.pack(side="right")
        self.btn_add = RoundButton(actions, "+", command=self.add_record,
                                   diameter=40, tooltip=tr("tip_add"))
        self.btn_edit = RoundButton(actions, "\u270E", command=self.edit_record,
                                    diameter=40, bg=COLORS["neutral"],
                                    tooltip=tr("tip_edit"))
        self.btn_del = RoundButton(actions, "\U0001F5D1",
                                   command=self.delete_record,
                                   diameter=40, bg=COLORS["danger"],
                                   tooltip=tr("tip_del"))
        for b in (self.btn_del, self.btn_edit, self.btn_add):
            b.pack(side="right", padx=6)

        holder = tk.Frame(self.manage_card.inner, bg=COLORS["card"])
        holder.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(holder, style="Card.Treeview",
                                 show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(holder, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self.tree.tag_configure("odd", background=COLORS["zebra"])
        self.tree.bind("<Double-1>", lambda e: self.edit_record())
        self.manage_card.pack(fill="both", expand=True, padx=26, pady=(12, 22))
        self._rebuild_table()

    def _rebuild_table(self):
        key = self._entity_key()
        cols = COLUMNS[key]
        self.tree.configure(columns=[c[0] for c in cols])
        for c in cols:
            anchor = "e" if c[0] == "id" else "w"
            self.tree.heading(c[0], text=tr(c[1]))
            self.tree.column(c[0], width=c[2], anchor=anchor, stretch=True)
        self._fill_table()

    def _fill_table(self):
        self.tree.delete(*self.tree.get_children())
        key = self._entity_key()
        rows = []
        if key == "owners":
            for o in sorted(self.store.owners, key=lambda x: x.name.lower()):
                rows.append((o.id, o.name, o.phone, o.email, o.address))
        elif key == "pets":
            for p in sorted(self.store.pets, key=lambda x: x.name.lower()):
                rows.append((p.id, p.name, p.species, p.breed, p.sex,
                             "\u2713" if p.hospitalized else "",
                             p.birth_date, p.microchip,
                             self.store.owner_name(p)))
        elif key == "appointments":
            for a in sorted(self.store.appointments,
                            key=lambda x: (x.date, x.time)):
                rows.append((a.id, fmt_date(a.date), a.time,
                             self.store.pet_label(a.pet_id), a.vet, a.reason,
                             a.status))
        else:
            for t in sorted(self.store.treatments, key=lambda x: x.date):
                rows.append((t.id, fmt_date(t.date), t.type,
                             self.store.pet_label(t.pet_id), t.description,
                             t.vet,
                             fmt_date(t.next_due) if t.next_due else ""))
        for i, row in enumerate(rows):
            self.tree.insert("", "end", values=row,
                             tags=("odd",) if i % 2 else ())

    def _build_empty(self):
        self.empty_card = RoundedCard(self)
        box = tk.Frame(self.empty_card.inner, bg=COLORS["card"])
        box.place(relx=0.5, rely=0.45, anchor="c")
        self._empty_logo = load_logo(64)
        tk.Label(box, image=self._empty_logo, bg=COLORS["card"]).pack()
        tk.Label(box, text=tr("empty_title"), bg=COLORS["card"],
                 fg=COLORS["text"], font=(FONT, 16, "bold")).pack(pady=(4, 2))
        tk.Label(box, text=tr("empty_hint"), bg=COLORS["card"],
                 fg=COLORS["muted"], font=(FONT, 10)).pack()
        RoundButton(box, tr("load_sample_btn"), command=self.load_sample,
                    diameter=46, pill=True).pack(pady=(16, 0))

    def refresh(self):
        s = self.store
        self.card_pets.set_value(len(s.pets))
        self.card_owners.set_value(len(s.owners))
        self.card_docs.set_value(len(VETS_SUGGEST))
        self.card_appts.set_value(len(s.appointments))
        self.card_vax.set_value(len(s.vaccinations_due(30)))
        self.card_notes.set_value(len(s.notes))
        self._redraw_chart()
        self._redraw_hospital()
        self._redraw_upcoming()
        cal = getattr(self, "calendar", None)
        if cal is not None and cal.winfo_exists():
            cal.refresh()
        self.manage_card.pack_forget()
        self.empty_card.pack_forget()
        if s.is_empty():
            self.empty_card.pack(fill="both", expand=True, padx=26,
                                 pady=(12, 22))
        else:
            self.manage_card.pack(fill="both", expand=True, padx=26,
                                  pady=(12, 22))
            self._fill_table()

    def _month_start(self, back: int) -> date:
        today = date.today()
        m, y = today.month - back, today.year
        while m < 1:
            m += 12
            y -= 1
        return date(y, m, 1)

    def _chart_payload(self, key):
        """Return (title_key, chart_data) for the selected entity."""
        if key == "owners":
            rows = sorted(((o.name, len(self.store.pets_of(o.id)))
                           for o in self.store.owners),
                          key=lambda x: -x[1])[:5]
            return "chart_owners", rows
        if key == "pets":
            return "species_mix", list(self.store.species_breakdown().items())
        if key == "appointments":
            counts = {"Scheduled": 0, "Completed": 0, "Cancelled": 0}
            for a in self.store.appointments:
                counts[a.status] = counts.get(a.status, 0) + 1
            data = [(tr(f"st_{s.lower()}"), counts[s])
                    for s in ("Scheduled", "Completed", "Cancelled")]
            return "chart_appts", data
        labels, keys, counts = [], [], {}
        for i in range(5, -1, -1):
            ms = self._month_start(i)
            ym = ms.strftime("%Y-%m")
            labels.append(month_name(ms.month))
            keys.append(ym)
            counts[ym] = 0
        for t in self.store.treatments:
            if t.date[:7] in counts:
                counts[t.date[:7]] += 1
        return "chart_treats", (labels, [counts[k] for k in keys])

    def _redraw_chart(self):
        c = self.chart_canvas
        c.delete("all")
        w = max(c.winfo_width(), 240)
        h = max(c.winfo_height(), 110)
        title_key, payload = self._chart_payload(self._entity_key())
        self.chart_title.config(text=tr(title_key))
        if isinstance(payload, tuple):
            values = payload[1]
        else:
            values = [v for _, v in payload]
        if not values or all(v == 0 for v in values):
            c.create_text(w / 2, h / 2, fill=COLORS["muted"],
                          font=(FONT, 10), text=tr("chart_empty"))
            self._chart_img = None
            return
        img = charts.render(self._entity_key(), w, h, payload, COLORS)
        self._chart_img = img
        c.create_image(0, 0, anchor="nw", image=img)

    def _redraw_hospital(self):
        c = self.hosp_canvas
        c.delete("all")
        s = self.store
        w = max(c.winfo_width(), 200)
        h = max(c.winfo_height(), 110)
        used, cap = s.hospitalized_count(), s.hospital_capacity
        free = max(cap - used, 0)

        c.create_text(4, 14, anchor="w", text=str(free),
                      font=(FONT, 24, "bold"), fill=COLORS["accent_dark"])
        c.create_text(6 + 12 * max(len(str(free)), 1), 22, anchor="w",
                      text=f"/ {cap}  {tr('hosp_free')}",
                      font=(FONT, 10), fill=COLORS["muted"])

        bar_y, bar_h = 44, 16
        x1, x2 = 6, w - 12
        c.create_polygon(
            [x1 + 8, bar_y, x2 - 8, bar_y, x2, bar_y, x2, bar_y + bar_h - 8,
             x2, bar_y + bar_h, x2 - 8, bar_y + bar_h, x1 + 8, bar_y + bar_h,
             x1, bar_y + bar_h, x1, bar_y + 8, x1, bar_y],
            smooth=True, outline="", fill=COLORS["input"])
        ratio = min(used / cap, 1.0) if cap else 0
        fx2 = x1 + max((x2 - x1) * ratio, 0)
        if used:
            c.create_polygon(
                [x1 + 8, bar_y, fx2 - (8 if fx2 - x1 > 16 else 0), bar_y,
                 fx2, bar_y, fx2, bar_y + bar_h - 8, fx2, bar_y + bar_h,
                 fx2 - (8 if fx2 - x1 > 16 else 0), bar_y + bar_h,
                 x1 + 8, bar_y + bar_h, x1, bar_y + bar_h,
                 x1, bar_y + 8, x1, bar_y],
                smooth=True, outline="", fill=COLORS["accent"])
        c.create_text(x1, bar_y + bar_h + 7, anchor="w",
                      text=tr("hosp_occup", u=used, c=cap),
                      font=(FONT, 9), fill=COLORS["muted"])

        ny = bar_y + bar_h + 26
        c.create_text(6, ny, anchor="nw", text="\u263E", font=(FONT, 13),
                      fill=COLORS["accent"])
        if s.night_vet_name:
            c.create_text(30, ny + 1, anchor="nw", text=s.night_vet_name,
                          font=(FONT, 11, "bold"), fill=COLORS["text"])
            phone = f"\u260E  {s.night_vet_phone}" if s.night_vet_phone else ""
            c.create_text(30, ny + 20, anchor="nw", text=phone,
                          font=(FONT, 10), fill=COLORS["muted"])
        else:
            c.create_text(30, ny + 1, anchor="nw", text=tr("night_title")
                          + " \u00B7 " + tr("no_night_vet"),
                          font=(FONT, 9, "italic"), fill=COLORS["muted"])

    def _redraw_upcoming(self):
        c = self.upcoming_canvas
        c.delete("all")
        rows = self.store.upcoming_appointments(limit=6)
        if self._day_filter:
            day_rows = sorted((a for a in self.store.appointments
                               if a.date == self._day_filter),
                              key=lambda x: x.time)
            rows = day_rows or []
        w = max(c.winfo_width(), 240)
        h = max(c.winfo_height(), 100)
        if not rows:
            c.create_text(w / 2, h / 2, fill=COLORS["muted"], font=(FONT, 10),
                          text=tr("no_records_upcoming"))
            return
        today = date.today()
        y = 10
        for a in rows:
            pet = self.store.get_pet(a.pet_id)
            try:
                d = date.fromisoformat(a.date)
                when = (tr("today_lbl") if d == today
                        else fmt_date(d, "wd"))
            except ValueError:
                when = a.date
            label = f"{when}  {a.time}"
            c.create_text(4, y, anchor="nw", text=label,
                          font=(FONT, 10, "bold"),
                          fill=COLORS["accent_dark"])
            who = f"{pet.name} ({self.store.owner_name(pet)})" if pet else ""
            c.create_text(118, y + 1, anchor="nw",
                          text=f"{who}  \u00B7  {a.vet}",
                          font=(FONT, 10), fill=COLORS["text"])
            c.create_text(118, y + 17, anchor="nw", text=a.reason,
                          font=(FONT, 9), fill=COLORS["muted"])
            y += 36

    def _entity_key(self):
        label = self.entity_var.get()
        return dict(entity_list()).get(label, "pets")

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Vet XLS Studio", tr("msg_no_selection"),
                                parent=self)
            return None
        return int(self.tree.item(sel[0], "values")[0])

    def _autosave(self):
        self.store.save(STORE_PATH)

    def generate_xls(self):
        path = generate_workbook(self.store, XLS_PATH)
        if messagebox.askyesno(tr("title_export"),
                               tr("msg_export_done", path=path),
                               parent=self):
            try:
                subprocess.Popen(["xdg-open", os.path.dirname(path)])
            except OSError:
                pass

    def load_sample(self):
        if not self.store.is_empty() and not messagebox.askyesno(
                tr("title_replace"), tr("msg_replace_body"),
                icon="warning", parent=self):
            return
        self.store = build_sample(Store())
        self._autosave()
        # defer refresh out of dialog-teardown context (Tcl race)
        self.after(10, self.refresh)

    def _field_specs(self, key):
        owners = [(o.id, o.name) for o in
                  sorted(self.store.owners, key=lambda x: x.name.lower())]
        pets = [(p.id, self.store.pet_label(p.id)) for p in
                sorted(self.store.pets, key=lambda x: x.name.lower())]
        if key == "owners":
            return [
                dict(k="name", label=tr("h_name"), required=True),
                dict(k="phone", label=tr("h_phone")),
                dict(k="email", label=tr("h_email")),
                dict(k="address", label=tr("h_address")),
            ]
        if key == "pets":
            return [
                dict(k="name", label=tr("h_name"), required=True),
                dict(k="species", label=tr("h_species"),
                     combo=SPECIES_SUGGEST),
                dict(k="breed", label=tr("h_breed")),
                dict(k="sex", label=tr("h_sex"), combo=["M", "F"]),
                dict(k="hospitalized", label=tr("h_hosp"), check=True),
                dict(k="birth_date", label=tr("h_birth"), date=True),
                dict(k="microchip", label=tr("h_microchip")),
                dict(k="owner_id", label=tr("h_owner"), choices=owners,
                     required=bool(owners)),
            ]
        if key == "appointments":
            return [
                dict(k="pet_id", label=tr("h_pet"), choices=pets,
                     required=True),
                dict(k="date", label=tr("h_date"), date=True, required=True),
                dict(k="time", label=tr("h_time")),
                dict(k="vet", label=tr("h_vet"), combo=VETS_SUGGEST),
                dict(k="reason", label=tr("h_reason")),
                dict(k="status", label=tr("h_status"),
                     combo=["Scheduled", "Completed", "Cancelled"]),
            ]
        return [
            dict(k="pet_id", label=tr("h_pet"), choices=pets, required=True),
            dict(k="date", label=tr("h_date"), date=True, required=True),
            dict(k="type", label=tr("h_type"),
                 combo=["Treatment", "Vaccination"]),
            dict(k="description", label=tr("h_description")),
            dict(k="vet", label=tr("h_vet"), combo=VETS_SUGGEST),
            dict(k="next_due", label=tr("h_nextdue"), date=True),
        ]

    def _center(self, dlg, rel=3):
        """Place dlg centered over the main window."""
        try:
            dlg.update_idletasks()
            sw, sh = dlg.winfo_reqwidth(), dlg.winfo_reqheight()
            px, py = self.winfo_rootx(), self.winfo_rooty()
            pw, ph = self.winfo_width(), self.winfo_height()
            x = px + max((pw - sw) // 2, 0)
            y = py + max((ph - sh) // rel, 0)
            dlg.geometry(f"+{x}+{y}")
        except tk.TclError:
            pass

    def _open_form(self, title, specs, initial=None, on_done=None):
        initial = initial or {}
        out = {}                 # shared; filled before destroy
        dlg = tk.Toplevel(self)
        dlg.title(title)
        dlg.configure(bg=COLORS["card"])
        dlg.transient(self)
        dlg.resizable(False, False)

        body = tk.Frame(dlg, bg=COLORS["card"], padx=22, pady=18)
        body.pack()
        widgets_by_key = {}
        keep_vars = []          # prevent GC unsetting Tcl variables

        for r, spec in enumerate(specs):
            tk.Label(body, text=spec["label"], bg=COLORS["card"],
                     fg=COLORS["muted"], font=(FONT, 9)).grid(
                row=r * 2, column=0, sticky="w", pady=(8, 2))
            if "choices" in spec:
                idmap = {lbl: oid for oid, lbl in spec["choices"]}
                var = tk.StringVar(value=(
                    dict(spec["choices"]).get(initial.get(spec["k"]))
                    or (spec["choices"][0][1] if spec["choices"] else "")))
                w = ttk.Combobox(body, textvariable=var, state="readonly",
                                 values=[lbl for _, lbl in spec["choices"]],
                                 width=30, style="Form.TCombobox")
                keep_vars.append(var)
                widgets_by_key[spec["k"]] = ("choice", w, idmap)
            elif "combo" in spec:
                var = tk.StringVar(value=str(initial.get(spec["k"])
                                            or spec["combo"][0]))
                w = ttk.Combobox(body, textvariable=var,
                                 values=spec["combo"], width=32,
                                 style="Form.TCombobox")
                keep_vars.append(var)
                widgets_by_key[spec["k"]] = ("plain", w)
            elif spec.get("check"):
                var = tk.BooleanVar(value=bool(initial.get(spec["k"])))
                w = tk.Checkbutton(body, variable=var, bg=COLORS["card"],
                                   fg=COLORS["text"], font=(FONT, 11),
                                   activebackground=COLORS["card"],
                                   selectcolor=COLORS["input"],
                                   highlightthickness=0, relief="flat")
                keep_vars.append(var)
                widgets_by_key[spec["k"]] = ("bool", w, var)
            else:
                var = tk.StringVar(value=str(initial.get(spec["k"]) or ""))
                w = tk.Entry(body, textvariable=var, width=34,
                             relief="flat", bg=COLORS["input"],
                             fg=COLORS["text"], font=(FONT, 10),
                             highlightthickness=1,
                             highlightbackground=COLORS["border"],
                             highlightcolor=COLORS["accent"])
                keep_vars.append(var)
                widgets_by_key[spec["k"]] = ("plain", w)
            w.grid(row=r * 2 + 1, column=0, sticky="ew", ipady=5)

        def on_ok():
            values = {}
            for k, entry in widgets_by_key.items():
                if entry[0] == "choice":
                    values[k] = entry[2].get(entry[1].get().strip())
                elif entry[0] == "bool":
                    values[k] = bool(entry[2].get())
                else:
                    values[k] = entry[1].get().strip()
            for spec in specs:
                v = values.get(spec["k"])
                if spec.get("required") and not v:
                    messagebox.showwarning(tr("title_missing"),
                                           tr("msg_missing_field",
                                              f=spec["label"]), parent=dlg)
                    return
                if spec.get("date") and v:
                    try:
                        date.fromisoformat(v)
                    except ValueError:
                        messagebox.showwarning(
                            tr("title_invalid_date"),
                            tr("msg_invalid_date", f=spec["label"]),
                            parent=dlg)
                        return
            out.clear()
            out.update(values)
            dlg.result = dict(values)
            dlg.destroy()
            if on_done is not None:
                try:
                    on_done(dict(out))
                except Exception:
                    import traceback
                    traceback.print_exc()

        btns = tk.Frame(dlg, bg=COLORS["card"])
        btns.pack(pady=(6, 16))
        RoundButton(btns, tr("word_cancel"), command=dlg.destroy, diameter=42,
                    pill=True, bg=COLORS["neutral"]).pack(side="left", padx=8)
        RoundButton(btns, "\u2713  " + tr("btn_save"), command=on_ok,
                    diameter=42, pill=True).pack(side="left", padx=8)
        dlg.result = None
        dlg._form_vars = keep_vars
        dlg._on_ok = on_ok
        self._center(dlg)
        dlg.update_idletasks()
        try:
            dlg.wait_visibility()
            dlg.grab_set()
            dlg.focus_force()
        except tk.TclError:
            pass
        dlg.wait_window()
        return dict(out) if out else None

    # ------------------------------------------------------------- CRUD --
    def _record_word(self, key):
        return {"owners": tr("word_owner"), "pets": tr("word_pet"),
                "appointments": tr("word_appointment"),
                "treatments": tr("word_treatment")}[key]

    def add_record(self):
        if self.store.is_empty():
            return
        key = self._entity_key()

        def create(vals):
            getattr(self.store, f"add_{key[:-1]}")(**vals)
            self._autosave()
            self.after(10, self.refresh)

        self._open_form(tr("lbl_new_record",
                           label=self._record_word(key)),
                        self._field_specs(key), on_done=create)

    def edit_record(self):
        rid = self._selected_id()
        if rid is None:
            return
        key = self._entity_key()
        pools = {"owners": self.store.owners, "pets": self.store.pets,
                 "appointments": self.store.appointments,
                 "treatments": self.store.treatments}
        rec = next((r for r in pools[key] if r.id == rid), None)
        if rec is None:
            return
        def apply(vals):
            for k, v in vals.items():
                setattr(rec, k, v)
            self._autosave()
            self.after(10, self.refresh)

        self._open_form(tr("lbl_edit_record",
                           label=self._record_word(key)),
                        self._field_specs(key), initial=asdict(rec),
                        on_done=apply)

    def delete_record(self):
        rid = self._selected_id()
        if rid is None:
            return
        key = self._entity_key()
        what = self._record_word(key)

        if key == "owners":
            owned = self.store.pets_of(rid)
            extra = sum(len(self.store.appointments_of(p.id))
                        + len(self.store.treatments_of(p.id)) for p in owned)
            detail = tr("msg_del_detail_owner", n=len(owned), v=extra)
        elif key == "pets":
            extra = (len(self.store.appointments_of(rid))
                     + len(self.store.treatments_of(rid)))
            detail = tr("msg_del_detail_pet", n=extra)
        else:
            detail = ""

        if not messagebox.askyesno(tr("title_delete"),
                                   tr("msg_delete_q", what=what) + detail,
                                   icon="warning", parent=self):
            return

        if key == "owners":
            self.store.delete_owner(rid)
        elif key == "pets":
            self.store.delete_pet(rid)
        elif key == "appointments":
            self.store.appointments = [a for a in self.store.appointments
                                       if a.id != rid]
        else:
            self.store.treatments = [t for t in self.store.treatments
                                     if t.id != rid]
        self._autosave()
        # defer refresh out of dialog-teardown context (Tcl race)
        self.after(10, self.refresh)




