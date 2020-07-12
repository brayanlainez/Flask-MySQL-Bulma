__Flask-MySQL-Bulma__

Instalar Python3

Crea un entorno virtual dentro de tu proyecto y luego activalo

    > mkdir myproject
    > cd myproject
    > py -3 -m venv venv
    > venv\Scripts\activate
    > deactivate

Instalar Flask y MySQL

    > pip install Flask flask-mysql
    > pip list

Correr la aplicación, antes debera indicar el achivo principal de la APP

    > set FLASK_APP=app.py
    > flask run
    > python app.py

Esto le dice a su sistema operativo que escuche en todas las IP públicas

    > flask run --host=0.0.0.0

Modo de depuración

    > set FLASK_ENV=development

Esto hace lo siguiente:
- Activa el depurador.
- Activa el cargador automático.
- Habilita el modo de depuración en la aplicación Flask.