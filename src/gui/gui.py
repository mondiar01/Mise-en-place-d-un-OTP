# src/gui/gui.py

import tkinter as tk
from tkinter import ttk, messagebox
import re
from datetime import datetime
from tkcalendar import DateEntry

class AuthGUI:
    def __init__(self, root, security_system):
        self.root = root
        self.security_system = security_system
        self.root.title("Système d'Authentification Multi-Facteur")
        self.root.geometry("600x700")
        
        # Configuration du style
        self.style = ttk.Style()
        self.style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'))
        self.style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))
        self.style.configure('Custom.TEntry', padding=5)
        self.style.configure('Custom.TButton', padding=5)

        # Frame principal
        self.main_frame = None
        self.show_main_menu()

    def clear_window(self):
        if self.main_frame:
            self.main_frame.destroy()
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def show_main_menu(self):
        self.clear_window()
        
        # Titre
        ttk.Label(self.main_frame, text="Système d'Authentification", style='Title.TLabel').pack(pady=20)
        
        # Boutons du menu
        ttk.Button(self.main_frame, text="S'inscrire", 
                  command=self.show_register_form, width=30).pack(pady=10)
        ttk.Button(self.main_frame, text="Se connecter", 
                  command=self.show_login_form, width=30).pack(pady=10)
        ttk.Button(self.main_frame, text="Quitter", 
                  command=self.root.quit, width=30).pack(pady=10)

    def show_register_form(self):
        self.clear_window()
        
        # Titre
        ttk.Label(self.main_frame, text="Inscription", style='Title.TLabel').pack(pady=20)

        # Frame pour les champs
        form_frame = ttk.Frame(self.main_frame)
        form_frame.pack(fill=tk.BOTH, padx=20, pady=10)

        # Création des champs
        fields = {
            "Nom d'utilisateur": ttk.Entry(form_frame),
            "Email": ttk.Entry(form_frame),
            "Mot de passe": ttk.Entry(form_frame, show="*"),
            "Confirmer le mot de passe": ttk.Entry(form_frame, show="*"),
            "Date de naissance": DateEntry(form_frame, width=20),
            "Adresse": ttk.Entry(form_frame),
            "Code postal": ttk.Entry(form_frame),
        }

        # Placement des champs
        row = 0
        for label, widget in fields.items():
            ttk.Label(form_frame, text=label + ":", style='Header.TLabel').grid(row=row, column=0, pady=5, sticky='w')
            widget.grid(row=row, column=1, pady=5, padx=10, sticky='ew')
            row += 1

        # Critères du mot de passe
        password_criteria = """
        Critères du mot de passe:
        - Minimum 12 caractères
        - Au moins une majuscule
        - Au moins une minuscule
        - Au moins un chiffre
        - Au moins un caractère spécial
        """
        ttk.Label(form_frame, text=password_criteria, wraplength=400).grid(row=row, column=0, columnspan=2, pady=10)

        # Boutons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, padx=20, pady=20)

        ttk.Button(button_frame, text="S'inscrire", 
                  command=lambda: self.handle_registration(fields)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Retour", 
                  command=self.show_main_menu).pack(side=tk.RIGHT, padx=5)

    def show_login_form(self):
        self.clear_window()
        
        # Titre
        ttk.Label(self.main_frame, text="Connexion", style='Title.TLabel').pack(pady=20)

        # Frame pour les champs
        form_frame = ttk.Frame(self.main_frame)
        form_frame.pack(fill=tk.BOTH, padx=20, pady=10)

        # Champs de connexion
        ttk.Label(form_frame, text="Nom d'utilisateur:", style='Header.TLabel').pack(pady=5)
        username_entry = ttk.Entry(form_frame, width=30)
        username_entry.pack(pady=5)

        ttk.Label(form_frame, text="Mot de passe:", style='Header.TLabel').pack(pady=5)
        password_entry = ttk.Entry(form_frame, show="*", width=30)
        password_entry.pack(pady=5)

        # Boutons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, padx=20, pady=20)

        ttk.Button(button_frame, text="Se connecter", 
                  command=lambda: self.handle_login(username_entry.get(), password_entry.get())).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Retour", 
                  command=self.show_main_menu).pack(side=tk.RIGHT, padx=5)

    def show_otp_verification(self, username):
        self.clear_window()
        
        ttk.Label(self.main_frame, text="Vérification OTP", style='Title.TLabel').pack(pady=20)
        
        ttk.Label(self.main_frame, text="Veuillez entrer le code OTP:", style='Header.TLabel').pack(pady=10)
        otp_entry = ttk.Entry(self.main_frame, width=10)
        otp_entry.pack(pady=10)
        
        ttk.Button(self.main_frame, text="Vérifier", 
                  command=lambda: self.verify_otp(username, otp_entry.get())).pack(pady=10)

    def show_personal_question(self, username):
        self.clear_window()
        
        question, correct_answer = self.security_system.get_random_personal_question(username)
        
        ttk.Label(self.main_frame, text="Question de sécurité", style='Title.TLabel').pack(pady=20)
        ttk.Label(self.main_frame, text=question, style='Header.TLabel').pack(pady=10)
        
        answer_entry = ttk.Entry(self.main_frame, width=30)
        answer_entry.pack(pady=10)
        
        ttk.Button(self.main_frame, text="Vérifier", 
                  command=lambda: self.verify_personal_answer(username, answer_entry.get(), correct_answer)).pack(pady=10)

    def show_welcome_screen(self, username):
        self.clear_window()
        
        ttk.Label(self.main_frame, text=f"Bienvenue {username}!", style='Title.TLabel').pack(pady=20)
        ttk.Label(self.main_frame, text="Vous êtes connecté avec succès.", style='Header.TLabel').pack(pady=10)
        
        ttk.Button(self.main_frame, text="Déconnexion", 
                  command=self.show_main_menu).pack(pady=20)

    def handle_registration(self, fields):
        # Récupération des valeurs
        username = fields["Nom d'utilisateur"].get()
        email = fields["Email"].get()
        password = fields["Mot de passe"].get()
        confirm_password = fields["Confirmer le mot de passe"].get()
        birth_date = fields["Date de naissance"].get_date()
        address = fields["Adresse"].get()
        postal_code = fields["Code postal"].get()

        # Validation des champs
        if not all([username, email, password, confirm_password, birth_date, address, postal_code]):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires")
            return

        # Validation du mot de passe
        is_valid, message = self.security_system.validate_password(password)
        if not is_valid:
            messagebox.showerror("Erreur", message)
            return

        if password != confirm_password:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas")
            return

        # Tentative d'inscription
        success, message = self.security_system.register_user(
            username, email, password, birth_date, address, postal_code)
        
        if success:
            messagebox.showinfo("Succès", message)
            self.show_login_form()
        else:
            messagebox.showerror("Erreur", message)

    def handle_login(self, username, password):
        if not username or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return

        success, message = self.security_system.verify_login(username, password)
        if success:
            self.show_personal_question(username)
        else:
            messagebox.showerror("Erreur", message)

    def verify_otp(self, username, otp):
        if self.security_system.verify_otp(username, otp):
            self.show_welcome_screen(username)
        else:
            messagebox.showerror("Erreur", "Code OTP invalide")
            self.show_login_form()

    def verify_personal_answer(self, username, answer, correct_answer):
        if answer.lower().strip() == correct_answer.lower().strip():
            self.show_otp_verification(username)
        else:
            messagebox.showerror("Erreur", "Réponse incorrecte")
            self.show_login_form()