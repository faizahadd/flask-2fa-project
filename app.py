# app.py
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
import pyotp
import qrcode
import io
import base64
import bcrypt  

# Configuration de l'application Flask
app = Flask(__name__)
app.config.update(
    SECRET_KEY="supersecret123",
    SQLALCHEMY_DATABASE_URI="sqlite:///users.db",
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

# Initialisation
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# Modèle User avec support 2FA
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # 🔐 Augmenté pour stocker le hash
    totp_secret = db.Column(db.String(16), nullable=True)

    def get_totp_uri(self):
        return pyotp.totp.TOTP(self.totp_secret).provisioning_uri(
            self.username, issuer_name="MonApp2FA"
        )

    def verify_totp(self, token):
        totp = pyotp.TOTP(self.totp_secret)
        return totp.verify(token)
    
    # méthode pour hasher le mot de passe
    def set_password(self, password):
        """Hash le mot de passe avant de le stocker"""
        # Convertir le mot de passe en bytes et générer le hash
        password_bytes = password.encode('utf-8')
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        # Stocker le hash en string
        self.password = hashed.decode('utf-8')
    
    # méthode pour vérifier le mot de passe
    def check_password(self, password):
        """Vérifie si le mot de passe correspond au hash stocké"""
        password_bytes = password.encode('utf-8')
        password_hash = self.password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, password_hash)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Routes
@app.route('/')
def index():
    return "Flask fonctionne ! 🎉"


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            return "Utilisateur déjà existant !", 400
        
        # Créer l'utilisateur
        new_user = User(
            username=username,
            totp_secret=pyotp.random_base32()
        )
        #  Hasher le mot de passe 
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        otp_uri = new_user.get_totp_uri()
        img = qrcode.make(otp_uri)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        qr_base64 = base64.b64encode(buf.getvalue()).decode()
        
        return render_template('show_qr.html', qr=qr_base64, username=username)
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        #  Chercher l'utilisateur par username uniquement
        user = User.query.filter_by(username=username).first()
        
        #  Vérifier le mot de passe avec bcrypt
        if user and user.check_password(password):
            session['pre_2fa_userid'] = user.id
            return redirect(url_for('two_factor'))
        else:
            return "Mauvais identifiants !", 401
    
    return render_template('login.html')


@app.route('/two_factor', methods=['GET', 'POST'])
def two_factor():
    user_id = session.get('pre_2fa_userid')
    
    if not user_id:
        return redirect(url_for('login'))
    
    user = User.query.get(user_id)
    
    if request.method == 'POST':
        token = request.form['token']
        
        if user.verify_totp(token):
            login_user(user)
            session.pop('pre_2fa_userid', None)
            return redirect(url_for('dashboard'))
        else:
            return "Code invalide !", 401
    
    return render_template('two_factor.html', username=user.username)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, host='0.0.0.0', port=5000)