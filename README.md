# 🔐 Système d'authentification à deux facteurs (2FA) avec Flask

## 📋 Description

J'ai développé ce projet pour apprendre à implémenter un système d'authentification à deux facteurs dans une application web. L'idée était de comprendre comment fonctionne la 2FA qu'on utilise tous les jours (Google, GitHub, etc.) et de le coder moi-même.

Le principe est simple : même si quelqu'un découvre votre mot de passe, il ne pourra pas se connecter sans avoir accès à votre téléphone. C'est une couche de sécurité supplémentaire qui protège vraiment bien les comptes.

## ✨ Fonctionnalités

- Inscription avec génération automatique d'un secret TOTP
- Génération de QR code à scanner avec Google Authenticator
- Connexion en deux étapes (mot de passe + code 2FA)
- **Hashage sécurisé des mots de passe avec bcrypt** 🔐
- Dashboard protégé par authentification
- Déconnexion 
- Base de données SQLite pour stocker les utilisateurs

## 🛠️ Technologies utilisées

- **Python 3.10.12** (compatible avec Python 3.8+)
- **Flask** - Framework web
- **Flask-Login** - Gestion des sessions
- **Flask-SQLAlchemy** - ORM base de données
- **PyOTP** - Génération codes TOTP
- **Bcrypt** - Hashage sécurisé des mots de passe
- **QRCode + Pillow** - Création des QR codes
- **SQLite** - Base de données
- **Google Authenticator** - App mobile pour la 2FA

## 🖥️ Environnement de développement

J'ai réalisé ce projet sur ma machine personnelle :
- **OS** : Xubuntu
- **Python** : 3.10.12
- **Environnement virtuel** : venv (pour isoler les dépendances)

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/faizahadd/flask-2fa-project.git
cd flask-2fa-project
```

### 2. Créer l'environnement virtuel

Sur Linux/macOS (ce que j'ai utilisé) :
```bash
python3 -m venv venv
source venv/bin/activate
```

Sur Windows :
```bash
python -m venv venv
venv\Scripts\activate
```

**Note** : Sur Ubuntu/Debian, si vous avez une erreur, installez d'abord :
```bash
sudo apt install python3-venv
```

### 3. Installer les dépendances

```bash
pip install flask flask-login flask-sqlalchemy pyotp qrcode pillow bcrypt
```

### 4. Lancer l'application

```bash
python app.py
```

L'application sera accessible sur `http://localhost:5000`

## 📖 Utilisation

### Étape 1 : Inscription

1. Ouvrez votre navigateur et allez sur `http://localhost:5000/register`
2. Remplissez le formulaire avec :
   - Un nom d'utilisateur
   - Un mot de passe
3. Après validation, un QR code s'affiche
4. Ouvrez Google Authenticator sur votre téléphone
5. Scannez le QR code
6. Votre compte est maintenant protégé par 2FA !

### Étape 2 : Connexion

1. Allez sur `http://localhost:5000/login`
2. Entrez votre nom d'utilisateur et mot de passe
3. Vous êtes redirigé vers la page de vérification 2FA
4. Ouvrez Google Authenticator
5. Entrez le code à 6 chiffres affiché
6. Vous êtes connecté au dashboard !

### Déconnexion

Cliquez simplement sur "Se déconnecter" depuis le dashboard.

## 🔐 Sécurité implémentée

- **Hashage des mots de passe** : Les mots de passe sont hashés avec bcrypt avant d'être stockés en base de données. Même en cas de vol de la base de données, les mots de passe restent protégés.
- **Authentification à deux facteurs** : Protection contre le vol de mot de passe grâce au code TOTP généré sur le téléphone.
- **Sessions sécurisées** : Gestion des sessions avec Flask-Login pour protéger l'accès aux pages sensibles.

## ⚠️ Limitations et améliorations possibles

Ce projet est une simple démo. Pour une utilisation en production, il faudrait :

- **Ajouter HTTPS** pour sécuriser les communications
- **Implémenter des codes de récupération** (backup codes) au cas où le téléphone est perdu,...

## 👤 Auteur

Développé par moi-même (Faiza HADDAI) dans le cadre de mon apprentissage.


