from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import auth
import i18n
import login as login_mod
from ui import VetApp
from widgets import init_theme


def run():
    first_run = auth.ensure_default_admin()
    i18n.init_lang()
    init_theme()
    while True:
        win = login_mod.LoginApp(first_run=first_run)
        win.mainloop()
        user = win.user
        if user is None:
            return
        first_run = False
        while True:
            app = VetApp(user)
            app.mainloop()
            if app.logout_requested:
                break
            if not app.theme_reloaded:
                return


if __name__ == "__main__":
    run()
