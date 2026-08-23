from __future__ import annotations

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(BASE_DIR, "data", "settings.json")

_current = "en"

TR = {
    "en": {
        "st_notes": 'Quick note',
        "note_title": 'Quick note',
        "calendar_title": "Calendar",
        "chart_total": "total",
        "note_hint": 'Write your note…',
        "notes_new": "New",
        "notes_edit": "Edit",
        "notes_delete": "Delete",
        "notes_close": "Close",
        "notes_confirm_del": "Delete this note?",
        "notes_empty": "(no notes yet)",
        "stat_doctors": 'Doctors',
        "chart_owners": 'Pets per owner',
        "chart_appts": 'Appointments by status',
        "chart_treats": 'Treatments — last 6 months',
        "st_scheduled": 'Scheduled',
        "st_completed": 'Completed',
        "st_cancelled": 'Cancelled',
        "chart_empty": 'No data yet',
        "h_hosp": 'Hosp.',
        "err_number": 'Please enter a valid number of positions.',
        "f_night_vet": 'Night vet name',
        "f_capacity": 'Capacity (positions)',
        "tip_hosp_edit": 'Capacity & night guard',
        "no_night_vet": 'Not set — tap ✎ to assign',
        "night_title": 'Night guard',
        "hosp_free": 'free positions',
        "hosp_occup": '{u} of {c} positions occupied',
        "hosp_title": 'Hospitalization',
        "app_subtitle": "Local clinic dashboard  \u2192  styled Excel workbook",
        "generate_xls": "\u2B07  Generate XLS",
        "load_sample_btn": "\u2726  Load sample data",
        "empty_title": "No records yet",
        "empty_hint": "Load the demo clinic data or add your own records.",
        "species_mix": "Species mix",
        "next_appointments": "Next appointments",
        "manage_lbl": "Manage",
        "stat_pets": "Pets registered",
        "stat_owners": "Owners on file",
        "stat_appts": "Appointments total",
        "stat_vax": "Vaccinations due \u226430d",
        "tip_add": "Add record",
        "tip_edit": "Edit selected",
        "tip_del": "Delete selected",
        "tip_xls": "Write vet_clinic_database.xlsx",
        "no_records_upcoming": "No upcoming appointments scheduled",
        "no_pets_species": "No pets yet \u2014 load sample data to see stats",
        "msg_no_selection": "Select a row in the table first.",
        "title_missing": "Missing field",
        "msg_missing_field": "Please fill in: {f}",
        "title_invalid_date": "Invalid date",
        "msg_invalid_date": "{f} must be YYYY-MM-DD.",
        "title_delete": "Delete record",
        "msg_delete_q": "Delete this {what}?",
        "msg_del_detail_owner": "\n\nThis also removes {n} pet(s) and {v} linked visit(s).",
        "msg_del_detail_pet": "\n\nThis also removes {n} linked visit(s).",
        "title_replace": "Replace data",
        "msg_replace_body": ("This replaces ALL current records with fresh "
                             "sample data.\n\nContinue?"),
        "msg_export_done": "Workbook saved:\n{path}\n\nOpen containing folder?",
        "title_export": "Export complete",
        "lbl_new_record": "New: {label}",
        "lbl_edit_record": "Edit: {label}",
        "entity_owners": "Owners",
        "entity_pets": "Pets",
        "entity_appointments": "Appointments",
        "entity_treatments": "Treatments & Vaccinations",
        "word_owner": "owner",
        "word_pet": "pet",
        "word_appointment": "appointment",
        "word_treatment": "treatment",
        "role_admin": "Admin",
        "role_user": "User",
        "lbl_logout": "Log out",
        "btn_save": "Save",
        "word_cancel": "Cancel",
        "tip_print": "Print report",
        "title_print": "Print",
        "msg_print_sent": "Report sent to the printer.",
        "msg_no_printer": "No printer found.\nWorkbook saved at:\n{path}",
        "tip_theme": "Dark / light mode",
        "signin_btn": "Sign in",
        "create_btn": "Create account",
        "btn_register": "Register",
        "title_create_account": "Create account",
        "f_username": "Username",
        "f_password": "Password",
        "f_display": "Display name",
        "f_confirm": "Confirm password",
        "err_wrong": "Wrong username or password.",
        "err_taken": "This username is already taken.",
        "err_mismatch": "Passwords do not match.",
        "err_fill": "Please fill in all fields.",
        "hint_first_run": "First run \u2014 admin account: admin / admin123",
        "today_lbl": "Today",
        "h_id": "ID", "h_name": "Name", "h_phone": "Phone", "h_email": "Email",
        "h_address": "Address", "h_species": "Species", "h_breed": "Breed",
        "h_sex": "Sex", "h_birth": "Birth date", "h_microchip": "Microchip",
        "h_owner": "Owner", "h_date": "Date", "h_time": "Time",
        "h_pet": "Pet", "h_vet": "Vet", "h_reason": "Reason",
        "h_status": "Status", "h_type": "Type",
        "h_description": "Description", "h_nextdue": "Next due",
    },
    "fr": {
        "st_notes": 'Note rapide',
        "note_title": 'Note rapide',
        "calendar_title": "Calendrier",
        "chart_total": "total",
        "note_hint": 'Écrivez votre note…',
        "notes_new": "Nouvelle",
        "notes_edit": "Modifier",
        "notes_delete": "Supprimer",
        "notes_close": "Fermer",
        "notes_confirm_del": "Supprimer cette note ?",
        "notes_empty": "(aucune note)",
        "stat_doctors": 'Médecins',
        "chart_owners": 'Animaux par propriétaire',
        "chart_appts": 'Rendez-vous par statut',
        "chart_treats": 'Soins — 6 derniers mois',
        "st_scheduled": 'Prévus',
        "st_completed": 'Terminés',
        "st_cancelled": 'Annulés',
        "chart_empty": 'Pas encore de données',
        "h_hosp": 'Hôp.',
        "err_number": 'Veuillez saisir un nombre valide de places.',
        "f_night_vet": 'Vétérinaire de garde',
        "f_capacity": 'Capacité (places)',
        "tip_hosp_edit": 'Capacité et garde de nuit',
        "no_night_vet": 'Non défini — touchez ✎ pour attribuer',
        "night_title": 'Garde de nuit',
        "hosp_free": 'positions libres',
        "hosp_occup": '{u} positions occupées sur {c}',
        "hosp_title": 'Hospitalisation',
        "app_subtitle": "Tableau de bord local  \u2192  classeur Excel stylé",
        "generate_xls": "\u2B07  Générer XLS",
        "load_sample_btn": "\u2726  Charger les données d'exemple",
        "empty_title": "Aucun enregistrement",
        "empty_hint": "Chargez les données de démo ou ajoutez vos enregistrements.",
        "species_mix": "Répartition des espèces",
        "next_appointments": "Prochains rendez-vous",
        "manage_lbl": "Gérer",
        "stat_pets": "Animaux enregistrés",
        "stat_owners": "Propriétaires",
        "stat_appts": "Rendez-vous (total)",
        "stat_vax": "Vaccins dus \u226430 j",
        "tip_add": "Ajouter",
        "tip_edit": "Modifier la sélection",
        "tip_del": "Supprimer la sélection",
        "tip_xls": "Créer vet_clinic_database.xlsx",
        "no_records_upcoming": "Aucun rendez-vous à venir",
        "no_pets_species": "Aucun animal \u2014 chargez les données d'exemple",
        "msg_no_selection": "Sélectionnez d'abord une ligne du tableau.",
        "title_missing": "Champ manquant",
        "msg_missing_field": "Veuillez remplir : {f}",
        "title_invalid_date": "Date invalide",
        "msg_invalid_date": "{f} doit être au format AAAA-MM-JJ.",
        "title_delete": "Supprimer l'enregistrement",
        "msg_delete_q": "Supprimer : {what}\u00a0?",
        "msg_del_detail_owner": ("\n\nCela supprime aussi {n} animal(aux) et "
                                 "{v} visite(s) liée(s)."),
        "msg_del_detail_pet": "\n\nCela supprime aussi {n} visite(s) liée(s).",
        "title_replace": "Remplacer les données",
        "msg_replace_body": ("Tous les enregistrements actuels seront remplacés "
                             "par de nouvelles données d'exemple.\n\n"
                             "Continuer\u00a0?"),
        "msg_export_done": ("Classeur enregistré :\n{path}\n\nOuvrir le "
                            "dossier\u00a0?"),
        "title_export": "Export terminé",
        "lbl_new_record": "Nouveau : {label}",
        "lbl_edit_record": "Modifier : {label}",
        "entity_owners": "Propriétaires",
        "entity_pets": "Animaux",
        "entity_appointments": "Rendez-vous",
        "entity_treatments": "Soins & Vaccins",
        "word_owner": "propriétaire",
        "word_pet": "animal",
        "word_appointment": "rendez-vous",
        "word_treatment": "soin",
        "role_admin": "Admin",
        "role_user": "Utilisateur",
        "lbl_logout": "Déconnexion",
        "btn_save": "Enregistrer",
        "word_cancel": "Annuler",
        "tip_print": "Imprimer le rapport",
        "title_print": "Impression",
        "msg_print_sent": "Rapport envoyé à l'imprimante.",
        "msg_no_printer": "Aucune imprimante détectée.\nClasseur enregistré sous :\n{path}",
        "tip_theme": "Mode sombre / clair",
        "signin_btn": "Se connecter",
        "create_btn": "Créer un compte",
        "btn_register": "S'inscrire",
        "title_create_account": "Créer un compte",
        "f_username": "Identifiant",
        "f_password": "Mot de passe",
        "f_display": "Nom affiché",
        "f_confirm": "Confirmer le mot de passe",
        "err_wrong": "Identifiant ou mot de passe incorrect.",
        "err_taken": "Cet identifiant est déjà utilisé.",
        "err_mismatch": "Les mots de passe ne correspondent pas.",
        "err_fill": "Veuillez remplir tous les champs.",
        "hint_first_run": "Première utilisation \u2014 admin : admin / admin123",
        "today_lbl": "Aujourd'hui",
        "h_id": "ID", "h_name": "Nom", "h_phone": "Téléphone", "h_email": "Email",
        "h_address": "Adresse", "h_species": "Espèce", "h_breed": "Race",
        "h_sex": "Sexe", "h_birth": "Naissance", "h_microchip": "Puce",
        "h_owner": "Propriétaire", "h_date": "Date", "h_time": "Heure",
        "h_pet": "Animal", "h_vet": "Vétérinaire", "h_reason": "Motif",
        "h_status": "Statut", "h_type": "Type",
        "h_description": "Description", "h_nextdue": "Prochain rappel",
    },
    "mg": {
        "st_notes": 'Fanamarihana',
        "note_title": 'Fanamarihana haingana',
        "calendar_title": "Tetiandro",
        "chart_total": "totaly",
        "note_hint": 'Soraty eto…',
        "notes_new": "Vaovao",
        "notes_edit": "Hanova",
        "notes_delete": "Hamafa",
        "notes_close": "Hidiana",
        "notes_confirm_del": "Hamafa ity fanamarihana ity?",
        "notes_empty": "(tsy misy fanamarihana)",
        "stat_doctors": 'Dokotera',
        "chart_owners": "Biby isan'ny tompony",
        "chart_appts": 'Fihaonana araka ny toe-javatra',
        "chart_treats": 'Fitsaboana — volana 6 farany',
        "st_scheduled": 'Voalahatra',
        "st_completed": 'Vita',
        "st_cancelled": 'Nofoanana',
        "chart_empty": 'Mbola tsy misy angona',
        "h_hosp": 'Hôp.',
        "err_number": 'Ampidiro tompoko ny isa marimba.',
        "f_night_vet": "Anaran'ny dokotera fiambenana",
        "f_capacity": "Isan'ny toerana",
        "tip_hosp_edit": 'Toerana sy fiambenana alina',
        "no_night_vet": 'Tsy napetraka — tsindrio ✎ hanendrena',
        "night_title": 'Fiambenana alina',
        "hosp_free": 'toerana malalaka',
        "hosp_occup": "{u} notokana amin'ny {c}",
        "hosp_title": 'Fitsaboana mitoetra',
        "app_subtitle": "Tabilao fanaraha-maso  \u2192  rakitra Excel voalamina",
        "generate_xls": "\u2B07  Hamorona XLS",
        "load_sample_btn": "\u2726  Ampidiro ny angona ohatra",
        "empty_title": "Mbola tsy misy angona",
        "empty_hint": "Ampidiro ny angona ohatra na ampio ny anao manokana.",
        "species_mix": "Karazana biby fiompy",
        "next_appointments": "Fihaonana manaraka",
        "manage_lbl": "Fitantanana",
        "stat_pets": "Biby fiompy voasoratra",
        "stat_owners": "Tompon'ny biby",
        "stat_appts": "Fihaonana (totaly)",
        "stat_vax": "Vaksiny tokony hatao \u226430 and",
        "tip_add": "Hanampy",
        "tip_edit": "Hanova izay voafantina",
        "tip_del": "Hamafa izay voafantina",
        "tip_xls": "Manoratra vet_clinic_database.xlsx",
        "no_records_upcoming": "Tsy misy fihaonana manaraka",
        "no_pets_species": "Tsy misy biby \u2014 ampidiro ny angona ohatra",
        "msg_no_selection": "Safidio aloha ny andalana ao amin'ny tabilao.",
        "title_missing": "Saha tsy feno",
        "msg_missing_field": "Fenoy tompoko: {f}",
        "title_invalid_date": "Daty diso",
        "msg_invalid_date": "Ny {f} dia tsy maintsy AAAA-MM-JJ.",
        "title_delete": "Hamafa angona",
        "msg_delete_q": "Hamafa ity: {what}\u00a0?",
        "msg_del_detail_owner": ("\n\nHfafana koa ny biby {n} sy ny fitsidihana "
                                 "{v} mifandraika aminy."),
        "msg_del_detail_pet": "\n\nHfafana koa ny fitsidihana {n} mifandraika.",
        "title_replace": "Hanolo ny angona",
        "msg_replace_body": ("Ny angona rehetra dia hosoloina angona ohatra "
                             "vaovao.\n\nHitohy\u00a0?"),
        "msg_export_done": ("Voatahiry ny rakitra:\n{path}\n\nHosokafana ny "
                            "lahatahiry\u00a0?"),
        "title_export": "Vita ny fanondranana",
        "lbl_new_record": "Vaovao: {label}",
        "lbl_edit_record": "Hanova: {label}",
        "entity_owners": "Tompon'ny biby",
        "entity_pets": "Biby fiompy",
        "entity_appointments": "Fihaonana",
        "entity_treatments": "Fitsaboana & Vaksiny",
        "word_owner": "tompon'ny biby",
        "word_pet": "biby",
        "word_appointment": "fihaonana",
        "word_treatment": "fitsaboana",
        "role_admin": "Mpitantana",
        "role_user": "Mpampiasa",
        "lbl_logout": "Hivoaka",
        "btn_save": "Tehirizo",
        "word_cancel": "Anafoana",
        "tip_print": "Manonta tatitra",
        "title_print": "Fanontana",
        "msg_print_sent": "Lasa tamin'ny printer ny tatitra.",
        "msg_no_printer": "Tsy nahita printer.\nVoatahiry ny rakitra eto:\n{path}",
        "tip_theme": "Maizina / mazava",
        "signin_btn": "Hiditra",
        "create_btn": "Hamorona kaonty",
        "btn_register": "Hisoratra anarana",
        "title_create_account": "Hamorona kaonty",
        "f_username": "Anaram-pampiasa",
        "f_password": "Teny miafina",
        "f_display": "Anara aseho",
        "f_confirm": "Hamarino ny teny miafina",
        "err_wrong": "Diso ny anaram-pampiasa na ny teny miafina.",
        "err_taken": "Efa misy io anaram-pampiasa io.",
        "err_mismatch": "Tsy mifanaraka ny teny miafina.",
        "err_fill": "Fenoy ny saha rehetra tompoko.",
        "hint_first_run": "Voalohany \u2014 kaonty mpitantana: admin / admin123",
        "today_lbl": "Androany",
        "h_id": "ID", "h_name": "Anarana", "h_phone": "Finday",
        "h_email": "Mailaka", "h_address": "Adiresy", "h_species": "Karazana",
        "h_breed": "Laharana", "h_sex": "Lahy/Vavy", "h_birth": "Teraka",
        "h_microchip": "Microchip", "h_owner": "Tompony", "h_date": "Daty",
        "h_time": "Ora", "h_pet": "Biby", "h_vet": "Dokotera",
        "h_reason": "Antony", "h_status": "Toe-javatra", "h_type": "Karazana",
        "h_description": "Famaritana", "h_nextdue": "Manaraka",
    },
}


def init_lang() -> str:
    global _current
    import settings
    lang = settings.load().get("lang")
    if lang in TR:
        _current = lang
    return _current


def set_lang(lang: str) -> None:
    global _current
    if lang not in TR:
        return
    _current = lang
    import settings
    settings.save("lang", lang)


def get_lang() -> str:
    return _current


def tr(key: str, **kw) -> str:
    text = TR.get(_current, {}).get(key) or TR["en"].get(key) or key
    if kw:
        try:
            text = text.format(**kw)
        except (KeyError, IndexError, ValueError):
            pass
    return text


# ------------------------------------------------ localized dates ----
_DAYS = {
    "en": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "fr": ["lun.", "mar.", "mer.", "jeu.", "ven.", "sam.", "dim."],
    "mg": ["Alats", "Tal", "Arab", "Alak", "Zom", "Asab", "Alah"],
}
_DAYS_FULL = {
    "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
           "Saturday", "Sunday"],
    "fr": ["lundi", "mardi", "mercredi", "jeudi", "vendredi",
           "samedi", "dimanche"],
    "mg": ["Alatsinainy", "Talata", "Alarobia", "Alakamisy", "Zoma",
           "Asabotsy", "Alahady"],
}
_MONTHS_FULL = {
    "en": ["January", "February", "March", "April", "May", "June",
           "July", "August", "September", "October", "November",
           "December"],
    "fr": ["janvier", "février", "mars", "avril", "mai", "juin",
           "juillet", "août", "septembre", "octobre", "novembre",
           "décembre"],
    "mg": ["Janoary", "Febroary", "Martsa", "Aprily", "Mey", "Jona",
           "Jolay", "Aogositra", "Septambra", "Oktobra", "Novambra",
           "Desambra"],
}
_MONTHS = {
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "fr": ["janv.", "f\u00e9vr.", "mars", "avr.", "mai", "juin",
           "juil.", "ao\u00fbt", "sept.", "oct.", "nov.", "d\u00e9c."],
    "mg": ["Jano", "Feb", "Mar", "Apr", "Mey", "Jon",
           "Jol", "Aog", "Sept", "Okt", "Nov", "Des"],
}


def fmt_date(value, style: str = "short") -> str:
    """Localized date. value = ISO 'YYYY-MM-DD' or datetime/date."""
    try:
        if hasattr(value, "year"):
            d = value
        else:
            from datetime import date as _d
            d = _d.fromisoformat(str(value)[:10])
    except Exception:
        return str(value)
    lang = get_lang()
    days, months = _DAYS.get(lang, _DAYS["en"]), _MONTHS.get(lang,
                                                             _MONTHS["en"])
    if style == "full":
        fdays = _DAYS_FULL.get(lang, _DAYS_FULL["en"])
        fmonths = _MONTHS_FULL.get(lang, _MONTHS_FULL["en"])
        return (f"{fdays[d.weekday()]} {d.day:02d} "
                f"{fmonths[d.month - 1]} {d.year}")
    if style == "long":
        return (f"{days[d.weekday()]} {d.day:02d} "
                f"{months[d.month - 1]} {d.year}")
    if style == "wd":                      # weekday + short month
        return f"{days[d.weekday()]} {d.day:02d} {months[d.month - 1]}"
    return f"{d.day:02d} {months[d.month - 1]}"


def month_name(idx: int) -> str:
    """1-based month -> localized short name."""
    lang = get_lang()
    return _MONTHS.get(lang, _MONTHS["en"])[idx - 1]


def day_initials() -> list[str]:
    """Localized weekday initials, Monday first."""
    lang = get_lang()
    days = _DAYS.get(lang, _DAYS["en"])
    return [d[:2].title() if not d.endswith(".") else d[:3]
            for d in days]
