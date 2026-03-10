# ============================================================
# TontineSecure – Guide de démarrage
# ============================================================

## 🚀 Installation

### 1. Corriger le problème pip (PowerShell)
```powershell
# Utilisez ceci à la place de "pip install"
python -m pip install -r requirements.txt
```

### 2. Configurer l'environnement
```powershell
# Copier le fichier exemple
copy .env.example .env

# Ouvrez .env et remplissez vos clés :
# - BREVO_API_KEY (email)
# - TWILIO_ACCOUNT_SID + TWILIO_AUTH_TOKEN (SMS)
# - SECRET_KEY (chaîne aléatoire longue)
```

### 3. Initialiser la base de données
```powershell
python -m flask init-db
python -m flask creer-admin
```

### 4. Lancer l'application
```powershell
python run.py
```
Ouvrez : http://localhost:5000

---

## 📁 Structure du projet

```
TontineApp/
├── run.py                    # Point d'entrée
├── config.py                 # Configuration
├── requirements.txt          # Dépendances Python
├── .env.example              # Variables d'environnement (template)
└── app/
    ├── __init__.py           # Factory Flask
    ├── models.py             # Modèles base de données
    ├── services.py           # Email (Brevo) + SMS (Twilio)
    ├── auth/                 # Inscription, connexion, vérification
    ├── kyc/                  # Dépôt documents d'identité
    ├── tontines/             # Gestion des tontines
    ├── contrats/             # Génération PDF + signature
    ├── admin/                # Interface d'administration
    ├── main/                 # Tableau de bord
    ├── static/               # CSS, JS, uploads
    └── templates/            # Templates HTML
```

---

## 🔐 Parcours utilisateur

1. **Inscription** → Email + mot de passe → Confirmation email
2. **Profil** → Nom, prénom, date de naissance, téléphone, revenus
3. **Vérification SMS** → Code 4 chiffres via Twilio
4. **KYC** → Pièce d'identité + bulletin de salaire → Validation admin
5. **Tontine** → Choisir un panier → Signer le contrat PDF
6. **Cotiser** → Payer chaque mois → Recevoir son tour

---

## 💰 Paniers disponibles

| Panier | Mensuel | Pot min (5) | Pot max (10) |
|--------|---------|-------------|--------------|
| Standard | 50 000 FCFA | 250 000 F | 500 000 F |
| Intermédiaire | 100 000 FCFA | 500 000 F | 1 000 000 F |
| Premium | 200 000 FCFA | 1 000 000 F | 2 000 000 F |

---

## 🛡️ Sécurités implémentées

- ✅ Hashage bcrypt des mots de passe (13 rounds)
- ✅ Vérification email obligatoire
- ✅ Vérification SMS (code 4 chiffres, 10 min, 3 tentatives)
- ✅ KYC avec documents + bulletin de salaire
- ✅ Contrat PDF avec hash SHA-256
- ✅ Rate limiting sur routes sensibles
- ✅ CSRF protection sur tous les formulaires
- ✅ Audit log complet (toutes les actions)
- ✅ Fichiers uploadés renommés aléatoirement
- ✅ Sessions sécurisées (httponly, samesite)

---

## 📧 Services externes requis

### Brevo (email)
1. Créez un compte sur https://www.brevo.com
2. Allez dans API Keys → Créez une clé
3. Ajoutez dans .env : `BREVO_API_KEY=votre-cle`

### Twilio (SMS)
1. Créez un compte sur https://www.twilio.com
2. Récupérez Account SID + Auth Token
3. Achetez un numéro de téléphone
4. Ajoutez dans .env les 3 variables Twilio

---

## 🔧 Commandes utiles

```powershell
# Lancer en mode développement
python run.py

# Shell interactif
python -m flask shell

# Migrations (si vous modifiez les modèles)
python -m flask db init
python -m flask db migrate -m "Description"
python -m flask db upgrade
```

---

## 👤 Compte admin par défaut

Après `python -m flask creer-admin` :
- Email : `admin@tontinesecure.com`
- Mot de passe : `Admin@2025!`

**Changez ce mot de passe en production !**
