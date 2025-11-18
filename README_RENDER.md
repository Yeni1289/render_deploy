# Despliegue en Render

Instrucciones rápidas para desplegar este proyecto Django en Render (con HTTPS automático).

Pasos resumidos:

1. Crear un repositorio Git y subir el código (GitHub/GitLab/Bitbucket).

  En Windows (cmd):
  ```cmd
  git init
  git add .
  git commit -m "Initial commit"
  git branch -M main
  git remote add origin <TU_REPO_URL>
  git push -u origin main
  ```

2. Conectar el repositorio en Render:
  - En Render, crea un nuevo **Web Service**.
  - Conecta tu cuenta GitHub/GitLab y selecciona el repositorio.
  - Render detectará `render.yaml` y aplicará la configuración.

3. Variables de entorno importantes (configura en el panel de Render -> Environment):
  - `SECRET_KEY`: Pon una cadena segura.
  - `ALLOWED_HOSTS`: `*` o tu dominio (recomendado: el dominio que te asigne Render o tu dominio personalizado).
  - `DJANGO_SETTINGS_MODULE`: `appi.settings` (ya configurado en `render.yaml`).
  - Si vas a usar Postgres: añadir `DATABASE_URL` con la URL de la base de datos de Render.

4. Post-deploy (ya configurado en `render.yaml`):
  Render ejecutará `python manage.py migrate` y `python manage.py collectstatic --noinput` tras el despliegue.

5. HTTPS
  - Render provee TLS/HTTPS automático para el dominio `*.onrender.com` y para dominios personalizados.
  - Solo asegúrate de añadir el dominio personalizado en la sección de Domains de tu servicio y Render solicitará el certificado.

Notas y recomendaciones:
- `gunicorn` ya está en `requirements.txt`. El comando de inicio usa `gunicorn appi.wsgi:application`.
- Si tu proyecto usa SQLite y necesitas persistencia, considera usar una base de datos gestionada (Postgres) en Render.
- Revisa `render.yaml` y reemplaza `SECRET_KEY` con una variable en Render en vez de dejar `REPLACE_ME` en el repositorio.

Si quieres, puedo:
- Preparar y hacer commits para inicializar el repo (si me autorizas a ejecutar comandos Git aquí).
- Crear un `Procfile`/Archivos adicionales si prefieres un flujo distinto.
- Configurar `DATABASE_URL` y crear un servicio de Postgres en Render y actualizar `settings.py` para usar `dj-database-url`.
