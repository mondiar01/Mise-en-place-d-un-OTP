# src/utils/auth_system.py
import random
from src.database.database import Database
from src.utils.security import Security

class AuthSystem:
    def __init__(self):
        self.db = Database()
        self.security = Security()

    def register(self, username, password, email, birth_date, address, postal_code):
        # Vérification du mot de passe
        valid, msg = self.security.verify_password_strength(password)
        if not valid:
            return False, msg

        # Hashage du mot de passe
        hashed_password = self.security.hash_password(password)

        # Ajout de l'utilisateur
        return self.db.add_user(
            username=username,
            password_hash=hashed_password,
            email=email,
            birth_date=birth_date,
            address=address,
            postal_code=postal_code
        )

    def login(self, username, password):
        user = self.db.get_user(username)
        if not user:
            return False, "Utilisateur non trouvé"

        if user['login_attempts'] >= 3:
            return False, "Compte bloqué après 3 tentatives échouées"

        if not self.security.verify_password(password, user['password_hash']):
            self.db.update_login_attempts(username)
            return False, "Mot de passe incorrect"

        self.db.update_login_attempts(username, reset=True)
        return True, user

    def get_security_question(self, username):
        user = self.db.get_user(username)
        if not user:
            return None, None
            
        questions = [
            ("Quel est votre code postal ?", user['postal_code']),
            ("Quelle est votre date de naissance ?", user['birth_date']),
            ("Quelle est votre adresse email ?", user['email'])
        ]
        return random.choice(questions)