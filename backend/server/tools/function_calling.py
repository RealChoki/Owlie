import os
import json
import requests
from dotenv import load_dotenv
from io import StringIO
from html.parser import HTMLParser

load_dotenv()

moodle_token = os.getenv("MOODLE_TOKEN")

keys_to_remove = [
    'id', 'hiddenbynumsections', 'visible', 'uservisible', 'instance',
    'contextid', 'visibleoncoursepage', 'modicon', 'modname', 'indent',
    'afterlink', 'noviewlink', 'filesize', 'sortorder', 'userid',
    'author', 'license', 'repositorytype', 'isexternalfile'
]

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def remove_html_and_keys(obj, keys_to_remove):
    if isinstance(obj, dict):
        return {k: remove_html_and_keys(strip_tags(v) if isinstance(v, str) else v, keys_to_remove)
                for k, v in obj.items() if k not in keys_to_remove}
    elif isinstance(obj, list):
        return [remove_html_and_keys(item, keys_to_remove) for item in obj]
    else:
        return obj

def get_moodle_course_content(courseid):
    """Fetches content for a specific Moodle course using the Moodle API and strips HTML."""
    moodle_call = (
        f'https://moodle.htw-berlin.de/webservice/rest/server.php?wstoken={moodle_token}'
        f'&wsfunction=core_course_get_contents&moodlewsrestformat=json&courseid={courseid}'
    )
    response = requests.get(moodle_call)
    response.raise_for_status()
    data = response.json()
    cleaned_data = remove_html_and_keys(data, keys_to_remove)

    return json.dumps(cleaned_data)

# id: Eindeutige Kennung der Sektion.
# name: Name der Sektion (z.B. "Allgemein", "Kursmaterialien").
# visible: Sichtbarkeitsstatus (1 = sichtbar).
# summary: Zusammenfassung der Sektion.
# section: Nummer der Sektion.
# hiddenbynumsections: Angabe, ob die Sektion durch die Anzahl der Sektionen versteckt ist.
# uservisible: Boolean-Wert, ob die Sektion für Benutzer sichtbar ist.
# modules: Array von Modulen innerhalb der Sektion.

# Ein Modul enthält:
# id: Eindeutige Kennung des Moduls.
# name: Name des Moduls (z.B. "Kurs-Nachrichten", "Prüfungsleistung").
# url: URL zum Modul (wenn zutreffend).
# instance: Instanznummer des Moduls.
# contextid: Kontext-ID für Berechtigungen und Kontextinformationen.
# visible: Sichtbarkeitsstatus des Moduls.
# uservisible: Boolean-Wert, ob das Modul für Benutzer sichtbar ist.
# visibleoncoursepage: Boolean-Wert, ob das Modul auf der Kursseite sichtbar ist.
# modicon: URL zum Icon des Modultyps.
# modname: Typ des Moduls (z.B. "forum", "resource").
# modplural: Pluralform des Modultyps.
# indent: Einrückungsstufe des Moduls.
# onclick: JavaScript-Funktion beim Klicken (wenn zutreffend).
# afterlink: Zusätzliche Informationen nach dem Link.
# customdata: Zusätzliche benutzerdefinierte Daten.
# noviewlink: Boolean-Wert, ob kein Direktlink angezeigt wird.
# completion: Fortschrittsstatus des Moduls.
# downloadcontent: Boolean-Wert, ob Inhalte heruntergeladen werden können.
# dates: Array von Datumseinträgen (falls vorhanden).
# contents: Array von Inhalten (z.B. Dateien).

# Inhalt eines Moduls:
# type: Typ des Inhalts (z.B. "file").
# filename: Name der Datei.
# filepath: Pfad zur Datei.
# filesize: Größe der Datei in Bytes.
# fileurl: URL zum direkten Download der Datei.
# timecreated: Erstellungszeitpunkt (Unix-Zeitstempel).
# timemodified: Letzter Änderungszeitpunkt (Unix-Zeitstempel).
# sortorder: Sortierreihenfolge innerhalb der Sektion.
# mimetype: MIME-Typ der Datei.
# isexternalfile: Boolean-Wert, ob die Datei extern ist.
# userid: ID des Benutzers, der die Datei hochgeladen hat.
# author: Autor der Datei.
# license: Lizenzinformationen.
# contentsinfo: Zusätzliche Informationen zum Inhalt, wie Anzahl der Dateien und MIME-Typen.