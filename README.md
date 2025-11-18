
Instrucciones para desplegar en Render.com

1) Subir este repo a GitHub.
2) Crear un nuevo Web Service en Render:
   - Conectar el repo
   - Branch: main (o el que uses)
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn appi.wsgi:application --bind 0.0.0.0:$PORT
3) Variables de entorno: no es obligatorio, pero puedes poner SECRET_KEY si quieres.
4) Render proveerá HTTPS automáticamente.
5) Si el notebook necesita regeneración al desplegar (por ejemplo se actualizaron datos),
   puedes agregar un build step que ejecute: 
      jupyter nbconvert --to html /path/to/07_Divicion_del_DataSet.ipynb --output appi/templates/notebook.html

Notas:
- Este proyecto sirve una versión convertida del notebook como plantilla Django.
- Si tus gráficas requieren archivos externos (imágenes), nbconvert inlined them in the HTML output.
