# Installing Vet XLS Studio

Step-by-step installation guide for version **0.5 (beta)**.
For an overview of what the app does, see [README.md](README.md).

---

## 1. Requirements

| | Windows | Linux |
|---|---|---|
| OS | Windows 10 / 11 (64-bit) | any mainstream distro (X11 or Wayland) |
| RAM | 4 GB recommended | 4 GB recommended |
| Disk | ~150 MB | ~150 MB |
| Extra software | none | none (Tk ships with most distros) |

The application is fully self-contained: no Python, no database server,
no internet connection needed after download.

---

## 2. Windows — guided installer (recommended)

1. Get **`VetXLSStudio-Setup-0.5.exe`**.
2. Double-click it. If Windows SmartScreen shows a warning (the app is
   not code-signed yet), click **More info → Run anyway**.
3. The setup wizard walks you through:
   - **License agreement** — read and click *I accept*.
   - **Information page** — quick intro of the app.
   - **Install location** — default is
     `C:\Program Files\VetXLSStudio`. Click *Browse* to choose another
     folder.
   - **Shortcuts** — desktop icon and Start-menu folder (both checked
     by default).
4. Click *Install*. Files are copied and the wizard finishes with a
   *Launch Vet XLS Studio* checkbox.
5. The app appears in **Start menu**, on the **desktop**, and in
   *Settings → Apps* for a clean uninstall later.

### Windows — portable alternative

The bundle also contains a single **`VetXLSStudio.exe`** that runs from
any USB stick or folder — just copy it somewhere writable and
double-click. It keeps its data in a `data\` folder next to itself.

---

## 3. Linux

### Option A — ready-made bundle

```bash
tar xzf VetXLSStudio-0.5-linux-x64.tar.gz
cd vet-xls-studio-0.5-linux
./install.sh
```

`install.sh` copies the executable to `~/.local/bin`, installs the logo
into your icon theme and registers **Vet XLS Studio** in your
applications menu (*Office* category). No root password needed.

### Option B — build it yourself

See *"Building from source"* in [README.md](README.md).

### Uninstalling on Linux

```bash
./uninstall.sh        # same folder as install.sh
```

This removes the binary, icon and menu entry but **keeps your clinic
data** (see next section). Delete the data folder manually if you want
a complete wipe.

---

## 4. First launch & login

The very first start creates an administrator account automatically:

```
username: admin
password: admin123
```

1. Start **Vet XLS Studio** from the menu/desktop.
2. Pick your language on the login screen: 🇬🇧 English · 🇫🇷 Français ·
   🇲🇬 Malagasy.
3. Log in with the credentials above.
4. **Create real accounts right away**: on the login screen use
   *Create account* to add one login per staff member (display name +
   username + password). Accounts are stored salted & hashed
   (PBKDF2-SHA256, 200k iterations).
5. Keep `admin / admin123` only as a recovery account, or treat it as
   shared until proper accounts exist.

> **Forgot all passwords?** Close the app and delete or rename
> `users.json` inside the data folder (below). Next start recreates the
> default admin account.

---

## 5. Where your data lives & backups

Everything (records, notes, accounts, settings) lives in one folder:

| Platform | Data folder |
|---|---|
| Windows (installer) | `C:\Program Files\VetXLSStudio\data\` |
| Windows (portable) | next to `VetXLSStudio.exe`, in `data\` |
| Linux | `~/.local/share/VetXLSStudio/data/` |

Inside you'll find:

- `store.json` — owners, pets, appointments, treatments, notes
- `users.json` — login accounts
- `settings.json` — theme, language

**Backup = copy this folder.** Do it before upgrading, and keep a copy
on another drive. To restore, put the folder back and restart the app.

**Upgrading:** install the new version over the old one; the data folder
is never touched by installs or uninstallers.

---

## 6. Troubleshooting

| Symptom | Fix |
|---|---|
| SmartScreen / Gatekeeper warning | unsigned beta binary — *Run anyway* (Win) or allow in system settings |
| Text looks plain (no Poppins font) | cosmetic fallback; install Poppins system-wide if you want the exact look |
| Login window doesn't appear | make sure the data folder is writable; on Linux check that a graphical session is running |
| Forgot password | see §4 tip about deleting `users.json` |
| App won't start after moving the exe (portable) | move `data\` together with the .exe |

Still stuck? Re-read [README.md](README.md) or open an issue with your
OS, version and the contents of `settings.json`.

---

*Vet XLS Studio v0.5 (beta) · MIT license · made by Leez*
