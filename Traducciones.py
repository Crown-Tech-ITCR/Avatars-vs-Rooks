LANGUAGES = {
    "es": {
        "login_title": "Iniciar sesión",
        "register_title": "Registro",
        "username": "Usuario",
        "password": "Contraseña",
        "login_button": "Iniciar sesión",
        "register_button": "Registrarse",
        "forgot_password": "¿Olvidaste la contraseña?",
        "username_placeholder": "Ingrese su usuario, correo o teléfono",
        "password_placeholder": "Ingrese su contraseña",
        "google_login": "Iniciar sesión con Google",
        "help_button": "Ayuda",
        "credits_button": "Créditos",

        # Ayuda
        "help_title": "Centro de Ayuda - Avatars vs Rooks",
        "help_section_login": "🔐 Inicio de sesión",
        "help_section_login_text": "Si ya tienes una cuenta, ingresa tu información en los espacios señalados.\nDebes ingresar tu usuario, correo o teléfono y tu contraseña.\nSi tus datos son correctos, podrás acceder al sistema.",
        "help_section_register": "🆕 Registro de usuario",
        "help_section_register_text": "Si eres un nuevo jugador, selecciona 'Registrarse'.\nCompleta los campos solicitados con tus datos.\nLuego de registrarse correctamente volverás a la página de Inicio de Sesión.",
        "help_section_forgot": "❓ Recuperar contraseña",
        "help_section_forgot_text": "Si olvidaste tu contraseña, haz clic en '¿Olvidaste la contraseña?'.\nSe te guiará por un proceso para restablecerla y recuperar el acceso.",
        "help_back": "Volver",

        # Créditos
        "credits_title": "Equipo de Desarrollo - Avatars vs Rooks",
        "credits_leader": "Líder Técnico\nDesarrollador",
        "credits_member": "Miembro",
        "credits_admin": "Administrador de Infraestructura\nDesarrollador",
        "credits_ux": "Diseñador de experiencia de Usuario\nDesarrollador",
        "credits_tester": "Líder de Pruebas\nDesarrollador",
        "credits_back": "Volver"
    },
    "en": {
        "login_title": "Login",
        "register_title": "Register",
        "username": "Username",
        "password": "Password",
        "login_button": "Login",
        "register_button": "Register",
        "forgot_password": "Forgot password?",
        "username_placeholder": "Enter your username, email or phone",
        "password_placeholder": "Enter your password",
        "google_login": "Sign in with Google",
        "help_button": "Help",
        "credits_button": "Credits",

        # Help
        "help_title": "Help Center - Avatars vs Rooks",
        "help_section_login": "🔐 Login",
        "help_section_login_text": "If you already have an account, enter your information in the indicated fields.\nYou must enter your username, email or phone and your password.\nIf your data is correct, you will be able to access the system.",
        "help_section_register": "🆕 User Registration",
        "help_section_register_text": "If you are a new player, select 'Register'.\nFill in the requested fields with your data.\nAfter registering successfully, you will return to the Login page.",
        "help_section_forgot": "❓ Recover password",
        "help_section_forgot_text": "If you forgot your password, click on 'Forgot password?'.\nYou will be guided through a process to reset it and regain access.",
        "help_back": "Back",

        # Credits
        "credits_title": "Development Team - Avatars vs Rooks",
        "credits_leader": "Technical Leader\nDeveloper",
        "credits_member": "Member",
        "credits_admin": "Infrastructure Administrator\nDeveloper",
        "credits_ux": "User Experience Designer\nDeveloper",
        "credits_tester": "Testing Leader\nDeveloper",
        "credits_back": "Back"
    },
    "hu": {
        "login_title": "Bejelentkezés",
        "register_title": "Regisztráció",
        "username": "Felhasználónév",
        "password": "Jelszó",
        "login_button": "Bejelentkezés",
        "register_button": "Regisztráció",
        "forgot_password": "Elfelejtette a jelszavát?",
        "username_placeholder": "Adja meg felhasználónevét, e-mailjét vagy telefonszámát",
        "password_placeholder": "Adja meg jelszavát",
        "google_login": "Bejelentkezés Google-lal",
        "help_button": "Súgó",
        "credits_button": "Kreditek",

        # Súgó
        "help_title": "Súgóközpont - Avatars vs Rooks",
        "help_section_login": "🔐 Bejelentkezés",
        "help_section_login_text": "Ha már van fiókja, adja meg adatait a megadott mezőkben.\nAdja meg felhasználónevét, e-mail címét vagy telefonszámát és jelszavát.\nHa az adatok helyesek, hozzáférhet a rendszerhez.",
        "help_section_register": "🆕 Felhasználó regisztráció",
        "help_section_register_text": "Ha új játékos, válassza a 'Regisztráció' lehetőséget.\nTöltse ki a kért mezőket adataival.\nA sikeres regisztráció után visszatér a Bejelentkezés oldalra.",
        "help_section_forgot": "❓ Jelszó visszaállítása",
        "help_section_forgot_text": "Ha elfelejtette jelszavát, kattintson az 'Elfelejtette a jelszavát?' gombra.\nEgy folyamaton keresztül visszaállíthatja azt és visszanyerheti a hozzáférést.",
        "help_back": "Vissza",

        # Kredit
        "credits_title": "Fejlesztői csapat - Avatars vs Rooks",
        "credits_leader": "Technikai vezető\nFejlesztő",
        "credits_member": "Tag",
        "credits_admin": "Infrastruktúra adminisztrátor\nFejlesztő",
        "credits_ux": "Felhasználói élmény tervező\nFejlesztő",
        "credits_tester": "Tesztelési vezető\nFejlesztő",
        "credits_back": "Vissza"
    }
}

current_language = "es"

def set_language(lang_code):
    global current_language
    if lang_code in LANGUAGES:
        current_language = lang_code

def t(key):
    return LANGUAGES[current_language].get(key, key)