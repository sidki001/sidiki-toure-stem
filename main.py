# main.py - Application Sidiki Touré STEM
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
import sqlite3
import os
import json
from datetime import datetime

Window.size = (360, 640)
Window.clearcolor = (0.95, 0.95, 0.95, 1)

DB_NAME = "sidiki_toure_stem.db"

class Database:
    def __init__(self):
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS eleves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ecole TEXT,
                nom TEXT,
                classe TEXT,
                montant REAL,
                matiere TEXT,
                statut TEXT,
                mois TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def get_all_eleves(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM eleves ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def add_eleve(self, ecole, nom, classe, montant, matiere, statut, mois):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO eleves (ecole, nom, classe, montant, matiere, statut, mois) VALUES (?,?,?,?,?,?,?)",
            (ecole, nom, classe, montant, matiere, statut, mois)
        )
        conn.commit()
        conn.close()
    
    def update_eleve(self, id, nom, classe, montant, matiere, statut, mois):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE eleves SET nom=?, classe=?, montant=?, matiere=?, statut=?, mois=? WHERE id=?",
            (nom, classe, montant, matiere, statut, mois, id)
        )
        conn.commit()
        conn.close()
    
    def delete_eleve(self, id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM eleves WHERE id=?", (id,))
        conn.commit()
        conn.close()
    
    def get_ecoles(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT ecole FROM eleves")
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]
    
    def get_eleves_by_ecole(self, ecole):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM eleves WHERE ecole=?", (ecole,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def get_stats(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM eleves")
        total_eleves = cursor.fetchone()[0]
        cursor.execute("SELECT SUM(montant) FROM eleves WHERE statut='Paye'")
        total_paye = cursor.fetchone()[0] or 0
        cursor.execute("""
            SELECT ecole, COUNT(*) as nb, 
            SUM(CASE WHEN statut='Paye' THEN montant ELSE 0 END) as total
            FROM eleves GROUP BY ecole
        """)
        school_stats = cursor.fetchall()
        cursor.execute("SELECT statut, COUNT(*) FROM eleves GROUP BY statut")
        status_stats = cursor.fetchall()
        cursor.execute("SELECT mois, COUNT(*) FROM eleves GROUP BY mois")
        month_stats = cursor.fetchall()
        cursor.execute("SELECT matiere, COUNT(*) FROM eleves GROUP BY matiere")
        subject_stats = cursor.fetchall()
        conn.close()
        return {
            'total_eleves': total_eleves,
            'total_paye': total_paye,
            'school_stats': school_stats,
            'status_stats': status_stats,
            'month_stats': month_stats,
            'subject_stats': subject_stats
        }

class RoundedButton(Button):
    def __init__(self, bg_color=(0.12, 0.25, 0.69, 1), text_color=(1, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.bg_color = bg_color
        self.text_color = text_color
        self.color = text_color
        self.bind(pos=self.update_rect, size=self.update_rect)
        with self.canvas.before:
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
            self.rect_color = Color(*bg_color)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class RoundedBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[25])
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class GradientBackground(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.06, 0.09, 0.16, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        bg = GradientBackground()
        layout.add_widget(bg)
        content = BoxLayout(orientation='vertical', padding=20, spacing=15, size_hint=(1, 1))
        icon_widget = BoxLayout(size_hint_y=None, height=150)
        try:
            icon = Image(source='icon.png', size_hint=(None, None), size=(100, 100), pos_hint={'center_x': 0.5})
            icon_widget.add_widget(icon)
        except:
            icon_widget.add_widget(Label(text='STEM', font_size='40sp', bold=True, color=(1,1,1,1)))
        content.add_widget(icon_widget)
        content.add_widget(Label(text='SIDIKI TOURE STEM', font_size='28sp', bold=True, halign='center', color=(1, 1, 1, 1)))
        content.add_widget(Label(text='SYSTEME DE GESTION AVANCE', font_size='11sp', bold=True, halign='center', color=(0.7, 0.7, 0.7, 1)))
        features = BoxLayout(orientation='vertical', spacing=8, size_hint_y=None, height=150, padding=(20, 0))
        features.add_widget(Label(text='✓ Gestion Complete des Eleves', font_size='12sp', color=(1, 1, 1, 0.8), halign='left'))
        features.add_widget(Label(text='✓ Statistiques Detaillees', font_size='12sp', color=(1, 1, 1, 0.8), halign='left'))
        features.add_widget(Label(text='✓ Export Multi-Formats', font_size='12sp', color=(1, 1, 1, 0.8), halign='left'))
        features.add_widget(Label(text='✓ Mode Hors-Ligne', font_size='12sp', color=(1, 1, 1, 0.8), halign='left'))
        content.add_widget(features)
        btn = RoundedButton(text='COMMENCER', font_size='16sp', bold=True, bg_color=(0.12, 0.25, 0.69, 1), text_color=(1, 1, 1, 1), size_hint=(None, None), size=(220, 55), pos_hint={'center_x': 0.5})
        btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        content.add_widget(btn)
        content.add_widget(Label(text='Application Offline-First', font_size='8sp', color=(0.5, 0.5, 0.5, 1), halign='center'))
        layout.add_widget(content)
        self.add_widget(layout)

class HomeScreen(Screen):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        header = BoxLayout(size_hint_y=None, height=100, padding=15)
        with header.canvas.before:
            Color(0.06, 0.09, 0.16, 1)
            header.rect = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=self.update_header_rect, size=self.update_header_rect)
        header.add_widget(Label(text='TABLEAU DE BORD', font_size='22sp', bold=True, color=(1, 1, 1, 1)))
        layout.add_widget(header)
        stats_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=120)
        self.total_students_box = RoundedBox()
        self.total_students_box.add_widget(Label(text='Eleves', font_size='10sp', bold=True, color=(0.5, 0.5, 0.5, 1)))
        self.total_students_label = Label(text='0', font_size='24sp', bold=True, color=(0, 0.6, 0, 1))
        self.total_students_box.add_widget(self.total_students_label)
        stats_layout.add_widget(self.total_students_box)
        self.total_money_box = RoundedBox()
        self.total_money_box.add_widget(Label(text='Recettes', font_size='10sp', bold=True, color=(0.5, 0.5, 0.5, 1)))
        self.total_money_label = Label(text='0 F', font_size='20sp', bold=True, color=(0.12, 0.25, 0.69, 1))
        self.total_money_box.add_widget(self.total_money_label)
        stats_layout.add_widget(self.total_money_box)
        layout.add_widget(stats_layout)
        btn_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=250)
        btn_ecoles = RoundedButton(text='🏫 ECOLES', font_size='14sp', bold=True, bg_color=(0.12, 0.25, 0.69, 1), text_color=(1, 1, 1, 1))
        btn_ecoles.bind(on_press=lambda x: setattr(self.manager, 'current', 'schools'))
        btn_layout.add_widget(btn_ecoles)
        btn_stats = RoundedButton(text='📊 STATISTIQUES', font_size='14sp', bold=True, bg_color=(0.12, 0.25, 0.69, 1), text_color=(1, 1, 1, 1))
        btn_stats.bind(on_press=lambda x: setattr(self.manager, 'current', 'stats'))
        btn_layout.add_widget(btn_stats)
        btn_export = RoundedButton(text='📤 EXPORT', font_size='14sp', bold=True, bg_color=(0.12, 0.25, 0.69, 1), text_color=(1, 1, 1, 1))
        btn_export.bind(on_press=lambda x: setattr(self.manager, 'current', 'export'))
        btn_layout.add_widget(btn_export)
        btn_welcome = RoundedButton(text='🏠 ACCUEIL', font_size='14sp', bold=True, bg_color=(0.12, 0.25, 0.69, 1), text_color=(1, 1, 1, 1))
        btn_welcome.bind(on_press=lambda x: setattr(self.manager, 'current', 'welcome'))
        btn_layout.add_widget(btn_welcome)
        layout.add_widget(btn_layout)
        self.add_widget(layout)
        self.update_stats()
    
    def update_header_rect(self, *args):
        if hasattr(self, 'rect'):
            self.rect.pos = self.pos
            self.rect.size = self.size
    
    def update_stats(self):
        stats = self.db.get_stats()
        self.total_students_label.text = str(stats['total_eleves'])
        self.total_money_label.text = f"{stats['total_paye']:,} F"

class SchoolsScreen(Screen):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        header = BoxLayout(size_hint_y=None, height=60, padding=10)
        with header.canvas.before:
            Color(0.06, 0.09, 0.16, 1)
            header.rect = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=self.update_header_rect, size=self.update_header_rect)
        btn_back = Button(text='←', font_size='20sp', color=(1, 1, 1, 1), background_normal='', size_hint=(None, None), size=(50, 50))
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        header.add_widget(btn_back)
        header.add_widget(Label(text='GESTION DES ECOLES', font_size='16sp', bold=True, color=(1, 1, 1, 1)))
        layout.add_widget(header)
        scroll = ScrollView()
        self.schools_list = GridLayout(cols=1, spacing=8, size_hint_y=None, padding=5)
        self.schools_list.bind(minimum_height=self.schools_list.setter('height'))
        scroll.add_widget(self.schools_list)
        layout.add_widget(scroll)
        btn_add = RoundedButton(text='+ AJOUTER UNE ECOLE', font_size='14sp', bold=True, bg_color=(0, 0.6, 0, 1), text_color=(1, 1, 1, 1), size_hint_y=None, height=50)
        btn_add.bind(on_press=self.show_add_ecole_popup)
        layout.add_widget(btn_add)
        self.add_widget(layout)
        self.load_schools()
    
    def update_header_rect(self, *args):
        if hasattr(self, 'rect'):
            self.rect.pos = self.pos
            self.rect.size = self.size
    
    def load_schools(self):
        self.schools_list.clear_widgets()
        ecoles = self.db.get_ecoles()
        for ecole in ecoles:
            eleves = self.db.get_eleves_by_ecole(ecole)
            item = RoundedBox(size_hint_y=None, height=70)
            item_layout = BoxLayout(padding=10, spacing=5)
            info = BoxLayout(orientation='vertical', size_hint=(0.8, 1))
            info.add_widget(Label(text=ecole, font_size='14sp', bold=True, halign='left', color=(0.1, 0.1, 0.1, 1)))
            info.add_widget(Label(text=f'{len(eleves)} eleves', font_size='11sp', halign='left', color=(0.5, 0.5, 0.5, 1)))
            item_layout.add_widget(info)
            btn_gerer = RoundedButton(text='GERER', font_size='11sp', bold=True, bg_color=(0.12, 0.25, 0.69, 1), text_color=(1, 1, 1, 1), size_hint=(0.3, 1))
            btn_gerer.bind(on_press=lambda x, e=ecole: self.show_ecole_detail(e))
            item_layout.add_widget(btn_gerer)
            item.add_widget(item_layout)
            self.schools_list.add_widget(item)
    
    def show_add_ecole_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=15, spacing=10, size_hint_y=None, height=180)
        input_ecole = TextInput(hint_text="Nom de l'ecole", multiline=False, size_hint_y=None, height=50, font_size='14sp')
        content.add_widget(input_ecole)
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        btn_cancel = RoundedButton(text='ANNULER', bg_color=(0.8, 0.8, 0.8, 1), text_color=(1, 1, 1, 1), size_hint=(0.5, 1))
        btn_ok = RoundedButton(text='AJOUTER', bg_color=(0, 0.6, 0, 1), text_color=(1, 1, 1, 1), size_hint=(0.5, 1))
        btn_layout.add_widget(btn_cancel)
        btn_layout.add_widget(btn_ok)
        content.add_widget(btn_layout)
        popup = Popup(title='Nouvelle Ecole', content=content, size_hint=(0.9, 0.4))
        def add_ecole(instance):
            nom = input_ecole.text.strip()
            if nom:
                if nom not in self.db.get_ecoles():
                    self.db.add_eleve(nom, 'Exemple', 'Classe', 0, 'Maths', 'Non paye', 'Janvier')
                    self.load_schools()
                    popup.dismiss()
                else:
                    self.show_message("Erreur", "Cette ecole existe deja")
        btn_ok.bind(on_press=add_ecole)
        btn_cancel.bind(on_press=lambda x: popup.dismiss())
        popup.open()
    
    def show_ecole_detail(self, ecole):
        self.manager.get_screen('students').load_students(ecole)
        self.manager.current = 'students'
    
    def show_message(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message, font_size='14sp'))
        btn = RoundedButton(text='OK', bg_color=(0.12, 0.25, 0.69, 1), text_color=(1, 1, 1, 1), size_hint_y=None, height=40)
        content.add_widget(btn)
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.3))
        btn.bind(on_press=lambda x: popup.dismiss())
        popup.open()

class StudentsScreen(Screen):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.current_ecole = ''
        self.current_id = None
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        header = BoxLayout(size_hint_y=None, height=60, padding=10)
        with header.canvas.before:
            Color(0.06, 0.09, 0.16, 1)
            header.rect = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=self.update_header_rect, size=self.update_header_rect)
        btn_back = Button(text='←', font_size='20sp', color=(1, 1, 1, 1), background_normal='', size_hint=(None, None), size=(50, 50))
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'schools'))
        header.add_widget(btn_back)
        self.ecole_title = Label(text='', font_size='16sp', bold=True, color=(1, 1, 1, 1))
        header.add_widget(self.ecole_title)
        layout.add_widget(header)
        form = RoundedBox(size_hint_y=None, height=320, padding=10)
        form_layout = BoxLayout(orientation='vertical', spacing=5)
        self.nom_input = TextInput(hint_text="Nom de l'eleve", multiline=False, size_hint_y=None, height=40, font_size='14sp')
        form_layout.add_widget(self.nom_input)
        self.classe_input = TextInput(hint_text='Classe', multiline=False, size_hint_y=None, height=40, font_size='14sp')
        form_layout.add_widget(self.classe_input)
        self.montant_input = TextInput(hint_text='Montant (FCFA)', multiline=False, size_hint_y=None, height=40, font_size='14sp', input_filter='float')
        form_layout.add_widget(self.montant_input)
        spinner_grid = GridLayout(cols=2, spacing=5, size_hint_y=None, height=80)
        self.mois_spinner = Spinner(text='Janvier', values=['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Decembre'], size_hint_y=None, height=35, font_size='12sp')
        spinner_grid.add_widget(self.mois_spinner)
        self.matiere_spinner = Spinner(text='Maths', values=['Maths', 'PC', 'SVT', 'Anglais', 'Philo', 'Histoire', 'Geographie'], size_hint_y=None, height=35, font_size='12sp')
        spinner_grid.add_widget(self.matiere_spinner)
        self.statut_spinner = Spinner(text='Non paye', values=['Paye', 'Non paye'], size_hint_y=None, height=35, font_size='12sp')
        spinner_grid.add_widget(self.statut_spinner)
        form_layout.add_widget(spinner_grid)
        self.btn_submit = RoundedButton(text='AJOUTER', font_size='14sp', bold=True, bg_color=(0.12, 0.25, 0.69, 1), text_color=(1, 1, 1, 1), size_hint_y=None, height=45)
        self.btn_submit.bind(on_press=self.save_student)
        form_layout.add_widget(self.btn_submit)
        form.add_widget(form_layout)
        layout.add_widget(form)
        scroll = ScrollView()
        self.students_list = GridLayout(cols=1, spacing=5, size_hint_y=None, padding=5)
        self.students_list.bind(minimum_height=self.students_list.setter('height'))
        scroll.add_widget(self.students_list)
        layout.add_widget(scroll)
        self.add_widget(layout)
    
    def update_header_rect(self, *args):
        if hasattr(self, 'rect'):
            self.rect.pos = self.pos
            self.rect.size = self.size
    
    def load_students(self, ecole):
        self.current_ecole = ecole
        self.ecole_title.text = ecole
        self.current_id = None
        self.btn_submit.text = 'AJOUTER'
        self.clear_form()
        self.update_list()
    
    def clear_form(self):
        self.nom_input.text = ''
        self.classe_input.text = ''
        self.montant_input.text = ''
        self.mois_spinner.text = 'Janvier'
        self.matiere_spinner.text = 'Maths'
        self.statut_spinner.text = 'Non paye'
    
    def update_list(self):
        self.students_list.clear_widgets()
        eleves = self.db.get_eleves_by_ecole(self.current_ecole)
        for eleve in eleves:
            item = RoundedBox(size_hint_y=None, height=60)
            item_layout = BoxLayout(padding=8, spacing=5)
            info = BoxLayout(orientation='vertical', size_hint=(0.7, 1))
            info.add_widget(Label(text=f'{eleve[2]}', font_size='14sp', bold=True, halign='left', color=(0.1, 0.1, 0.1, 1)))
            info.add_widget(Label(text=f'{eleve[3]} | {eleve[5]} | {eleve[6]} | {eleve[4]:,} F', font_size='10sp', color=(0.5, 0.5, 0.5, 1), halign='left'))
            item_layout.add_widget(info)
            btn_edit = RoundedButton(text='✏️', bg_color=(0.12, 0.25, 0.69, 1), text_color=(1, 1, 1, 1), size_hint=(0.15, 1))
            btn_edit.bind(on_press=lambda x, e=eleve: self.edit_student(e))
            item_layout.add_widget(btn_edit)
            btn_delete = RoundedButton(text='🗑️', bg_color=(0.8, 0.1, 0.1, 1), text_color=(1, 1, 1, 1), size_hint=(0.15, 1))
            btn_delete.bind(on_press=lambda x, e=eleve: self.delete_student(e))
            item_layout.add_widget(btn_delete)
            item.add_widget(item_layout)
            self.students_list.add_widget(item)
    
    def save_student(self, instance):
        nom = self.nom_input.text.strip()
        classe = self.classe_input.text.strip()
        try:
            montant = float(self.montant_input.text.strip()) if self.montant_input.text.strip() else 0
        except:
            montant = 0
        if nom and classe:
            if self.current_id:
                self.db.update_eleve(self.current_id, nom, classe, montant, self.matiere_spinner.text, self.statut_spinner.text, self.mois_spinner.text)
            else:
                self.db.add_eleve(self.current_ecole, nom, classe, montant, self.matiere_spinner.text, self.statut_spinner.text, self.mois_spinner.text)
            self.current_id = None
            self.btn_submit.text = 'AJOUTER'
            self.clear_form()
            self.update_list()
            self.manager.get_screen('home').update_stats()
    
    def edit_student(self, eleve):
        self.current_id = eleve[0]
        self.nom_input.text = eleve[2]
        self.classe_input.text = eleve[3]
        self.montant_input.text = str(eleve[4])
        self.matiere_spinner.text = eleve[5]
        self.statut_spinner.text = eleve[6]
        self.mois_spinner.text = eleve[7]
        self.btn_submit.text = 'MODIFIER'
    
    def delete_student(self, eleve):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=f'Supprimer {eleve[2]} ?', font_size='14sp'))
        btn_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_non = RoundedButton(text='NON', bg_color=(0.8, 0.8, 0.8, 1), text_color=(1, 1, 1, 1), size_hint=(0.5, 1))
        btn_oui = RoundedButton(text='OUI', bg_color=(0.8, 0.1, 0.1, 1), text_color=(1, 1, 1, 1), size_hint=(0.5, 1))
        btn_layout.add_widget(btn_non)
        btn_layout.add_widget(btn_oui)
        content.add_widget(btn_layout)
        popup = Popup(title='Confirmation', content=content, size_hint=(0.8, 0.3))
        def confirm_delete(instance):
            self.db.delete_eleve(eleve[0])
            self.update_list()
            self.manager.get_screen('home').update_stats()
            popup.dismiss()
        btn_oui.bind(on_press=confirm_delete)
        btn_non.bind(on_press=lambda x: popup.dismiss())
        popup.open()

class StatsScreen(Screen):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        header = BoxLayout(size_hint_y=None, height=60, padding=10)
        with header.canvas.before:
            Color(0.06, 0.09, 0.16, 1)
            header.rect = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=self.update_header_rect, size=self.update_header_rect)
        btn_back = Button(text='←', font_size='20sp', color=(1, 1, 1, 1), background_normal='', size_hint=(None, None), size=(50, 50))
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        header.add_widget(btn_back)
        header.add_widget(Label(text='STATISTIQUES', font_size='16sp', bold=True, color=(1, 1, 1, 1)))
        layout.add_widget(header)
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, padding=5)
        content.bind(minimum_height=content.setter('height'))
        stats_box = RoundedBox(size_hint_y=None, height=150, padding=10)
        stats_layout = GridLayout(cols=2, spacing=10)
        self.total_eleves_label = Label(text='Total Eleves: 0', font_size='14sp', bold=True, color=(0.1, 0.1, 0.1, 1))
        stats_layout.add_widget(self.total_eleves_label)
        self.total_paye_label = Label(text='Total Recettes: 0 F', font_size='14sp', bold=True, color=(0.12, 0.25, 0.69, 1))
        stats_layout.add_widget(self.total_paye_label)
        self.paye_count_label = Label(text='Paye: 0', font_size='14sp', color=(0, 0.6, 0, 1))
        stats_layout.add_widget(self.paye_count_label)
        self.nonpaye_count_label = Label(text='Non paye: 0', font_size='14sp', color=(0.8, 0.1, 0.1, 1))
        stats_layout.add_widget(self.nonpaye_count_label)
        stats_box.add_widget(stats_layout)
        content.add_widget(stats_box)
        school_stats_box = RoundedBox(size_hint_y=None, padding=10)
        school_stats_box.add_widget(Label(text='📊 Par Ecole', font_size='14sp', bold=True, color=(0.1, 0.1, 0.1, 1), size_hint_y=None, height=30))
        self.school_stats_label = Label(text='', font_size='12sp', size_hint_y=None, text_size=(300, None), halign='left', valign='top')
        school_stats_box.add_widget(self.school_stats_label)
        content.add_widget(school_stats_box)
        month_stats_box = RoundedBox(size_hint_y=None, padding=10)
        month_stats_box.add_widget(Label(text='📅 Par Mois', font_size='14sp', bold=True, color=(0.1, 0.1, 0.1, 1), size_hint_y=None, height=30))
        self.month_stats_label = Label(text='', font_size='12sp', size_hint_y=None, text_size=(300, None), halign='left', valign='top')
        month_stats_box.add_widget(self.month_stats_label)
        content.add_widget(month_stats_box)
        subject_stats_box = RoundedBox(size_hint_y=None, padding=10)
        subject_stats_box.add_widget(Label(text='📚 Par Matiere', font_size='14sp', bold=True, color=(0.1, 0.1, 0.1, 1), size_hint_y=None, height=30))
        self.subject_stats_label = Label(text='', font_size='12sp', size_hint_y=None, text_size=(300, None), halign='left', valign='top')
        subject_stats_box.add_widget(self.subject_stats_label)
        content.add_widget(subject_stats_box)
        scroll.add_widget(content)
        layout.add_widget(scroll)
        self.add_widget(layout)
        self.update_stats()
    
    def update_header_rect(self, *args):
        if hasattr(self, 'rect'):
            self.rect.pos = self.pos
            self.rect.size = self.size
    
    def update_stats(self):
        stats = self.db.get_stats()
        self.total_eleves_label.text = f'Total Eleves: {stats["total_eleves"]}'
        self.total_paye_label.text = f'Total Recettes: {stats["total_paye"]:,} F'
        paye = 0
        nonpaye = 0
        for status, count in stats['status_stats']:
            if status == 'Paye':
                paye = count
            else:
                nonpaye = count
        self.paye_count_label.text = f'Paye: {paye}'
        self.nonpaye_count_label.text = f'Non paye: {nonpaye}'
        school_text = ""
        for ecole, nb, total in stats['school_stats']:
            school_text += f"{ecole}: {nb} eleves - {total:,} F\n"
        self.school_stats_label.text = school_text
        month_text = ""
        for mois, count in stats['month_stats']:
            month_text += f"{mois}: {count} eleves\n"
        self.month_stats_label.text = month_text
        subject_text = ""
        for matiere, count in stats['subject_stats']:
            subject_text += f"{matiere}: {count} eleves\n"
        self.subject_stats_label.text = subject_text

class ExportScreen(Screen):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        header = BoxLayout(size_hint_y=None, height=60, padding=10)
        with header.canvas.before:
            Color(0.06, 0.09, 0.16, 1)
            header.rect = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=self.update_header_rect, size=self.update_header_rect)
        btn_back = Button(text='←', font_size='20sp', color=(1, 1, 1, 1), background_normal='', size_hint=(None, None), size=(50, 50))
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        header.add_widget(btn_back)
        header.add_widget(Label(text='EXPORTATION', font_size='16sp', bold=True, color=(1, 1, 1, 1)))
        layout.add_widget(header)
        btn_export_txt = RoundedButton(text='📄 EXPORTER EN TXT', font_size='14sp', bold=True, bg_color=(0.12, 0.25, 0.69, 1), text_color=(1, 1, 1, 1), size_hint_y=None, height=60)
        btn_export_txt.bind(on_press=self.export_txt)
        layout.add_widget(btn_export_txt)
        btn_export_csv = RoundedButton(text='📊 EXPORTER EN CSV', font_size='14sp', bold=True, bg_color=(0, 0.6, 0, 1), text_color=(1, 1, 1, 1), size_hint_y=None, height=60)
        btn_export_csv.bind(on_press=self.export_csv)
        layout.add_widget(btn_export_csv)
        btn_export_stats = RoundedButton(text='📈 EXPORTER LES STATS', font_size='14sp', bold=True, bg_color=(0.8, 0.5, 0, 1), text_color=(1, 1, 1, 1), size_hint_y=None, height=60)
        btn_export_stats.bind(on_press=self.export_stats)
        layout.add_widget(btn_export_stats)
        self.add_widget(layout)
    
    def update_header_rect(self, *args):
        if hasattr(self, 'rect'):
            self.rect.pos = self.pos
            self.rect.size = self.size
    
    def export_txt(self, instance):
        eleves = self.db.get_all_eleves()
        try:
            filename = f'/sdcard/rapport_stem_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("="*50 + "\n")
                f.write("RAPPORT SIDIKI TOURE STEM\n")
                f.write(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
                f.write("="*50 + "\n\n")
                for eleve in eleves:
                    f.write(f"Ecole: {eleve[1]}\n")
                    f.write(f"Nom: {eleve[2]}\n")
                    f.write(f"Classe: {eleve[3]}\n")
                    f.write(f"Montant: {eleve[4]:,} FCFA\n")
                    f.write(f"Matiere: {eleve[5]}\n")
                    f.write(f"Statut: {eleve[6]}\n")
                    f.write(f"Mois: {eleve[7]}\n")
                    f.write("-"*30 + "\n")
            self.show_message("Succes", f"Rapport exporte:\n{filename}")
        except Exception as e:
            self.show_message("Erreur", f"Erreur: {str(e)}")
    
    def export_csv(self, instance):
        eleves = self.db.get_all_eleves()
        try:
            filename = f'/sdcard/eleves_stem_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            import csv
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Ecole', 'Nom', 'Classe', 'Montant', 'Matiere', 'Statut', 'Mois'])
                for eleve in eleves:
                    writer.writerow(eleve)
            self.show_message("Succes", f"CSV exporte:\n{filename}")
        except Exception as e:
            self.show_message("Erreur", f"Erreur: {str(e)}")
    
    def export_stats(self, instance):
        stats = self.db.get_stats()
        try:
            filename = f'/sdcard/stats_stem_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("="*50 + "\n")
                f.write("STATISTIQUES SIDIKI TOURE STEM\n")
                f.write(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
                f.write("="*50 + "\n\n")
                f.write(f"Total Eleves: {stats['total_eleves']}\n")
                f.write(f"Total Recettes: {stats['total_paye']:,} FCFA\n\n")
                f.write("--- Par Ecole ---\n")
                for ecole, nb, total in stats['school_stats']:
                    f.write(f"{ecole}: {nb} eleves - {total:,} FCFA\n")
                f.write("\n--- Par Statut ---\n")
                for status, count in stats['status_stats']:
                    f.write(f"{status}: {count} eleves\n")
                f.write("\n--- Par Mois ---\n")
                for mois, count in stats['month_stats']:
                    f.write(f"{mois}: {count} eleves\n")
                f.write("\n--- Par Matiere ---\n")
                for matiere, count in stats['subject_stats']:
                    f.write(f"{matiere}: {count} eleves\n")
            self.show_message("Succes", f"Stats exportees:\n{filename}")
        except Exception as e:
            self.show_message("Erreur", f"Erreur: {str(e)}")
    
    def show_message(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message, font_size='12sp'))
        btn = RoundedButton(text='OK', bg_color=(0.12, 0.25, 0.69, 1), text_color=(1, 1, 1, 1), size_hint_y=None, height=40)
        content.add_widget(btn)
        popup = Popup(title=title, content=content, size_hint=(0.9, 0.4))
        btn.bind(on_press=lambda x: popup.dismiss())
        popup.open()

class SidikiToureApp(App):
    def build(self):
        self.db = Database()
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(HomeScreen(self.db, name='home'))
        sm.add_widget(SchoolsScreen(self.db, name='schools'))
        sm.add_widget(StudentsScreen(self.db, name='students'))
        sm.add_widget(StatsScreen(self.db, name='stats'))
        sm.add_widget(ExportScreen(self.db, name='export'))
        return sm

if __name__ == '__main__':
    SidikiToureApp().run()
