# MiArte Omi

Colección de dibujos estructurados en página web con script de edición

## Funcionamiento

para ingresar nuevos dibujos

1. pegar las imágenes en origen/
2. ejecutar codigo/main.py
3. ir a "nuevo" allí podrá cargar uno o varios dibujos externos a una de las carpetas internas del repositorio
4. edite los metadatos
5. pulse "guardar"

para editar dibujos

1. pegar las imágenes a agregar, si es que las hay, en origen/
2. ejecutar codigo/main.py
3. ir a "editar" allí podrá elegir uno de los dibujos de la galería de carpetas, se abrirán sus metadatos
4. agregar o eliminar imágenes, eliminar mueve el archivo a papelera/ y si no hay imágenes al guardar elimina ese registro de metadatos
5. edite los metadatos
6. pulse "guardar"

para crear el sitio web html

1. ejecutar codigo/main.py
2. pulsar en "generar" para crear el sitio web en la carpeta website/ (destruye la anterior)

## Archivos

sincronizables con GitHub

- codigo/ contiene los scripts Python para edición de los dibujos y sus metadatos, así como el despliegue html
- miarte/ carpeta de carpetas, donde estas contienen a los dibujos y sus metadatos, cada subcarpeta es un grupo

No se sincronizan con el repositorio

- papelera/ acá se envían imágenes que han sido eliminadas desde el editor, para revisarlas luego
- website/ donde se crea automáticamente el sitio web con su index.html
- origen/ auxiliar para colocar las imágenes manualmente y luego desde aquí tomarlas con el editor

## Requerimientos

### codigo/main

- la UI muestra una interfaz con título, un texto "acerca de" y 3 botónes (nuevo, editar y generar)
- nuevo lleva a la UI arte_nuevo.py
- editar lleva a la UI arte_edita.py
- generar ejecuta un script llamado genera_html.py

### codigo/arte_nuevo

- una UI de creación, que muestra las imágenes seleccionadas y los metadatos en un formulario
- para cargar imágenes "files" pulsar un botón, que abra un selector de archivos múltiples, con formatos (png, jpg, jpeg, gif, bmp, webm), las imágnees cargadas aparecerán en la interfaz pero aún no se moverán o copiarán archivos, por defecto abre la carpeta origen/
- poder eliminar imágenes cargadas en la interfaz, solo desvincula el archivo de la UI, no lo elimina como tal
- editar los metadatos que a futuro irán a data.json para una serie de dibujos nueva
- habrá un selector con las carpetas que existen dentro de miarte/
- los tags son textos separados por comas, a la hora de guardar, se convierten en array de strings
- el atributo "style" es un desplegable con las opciónes de style, ver apartado "Metadatos JSON"
- "nsfw" por defecto está en false
- botón de guardar, en caso de haber al menos una imágen seleccionada, corta y pega las imágenes en la carpeta establecida y agrega los metadatos al data.json de esa carpeta, si salió bien retorna a main.py

### codigo/arte_edita

- una interfaz UI de edición, primero muestra un botón para abrir un selector ubicado por defecto en la carpeta miarte/ al elegir un dibujo, busca los metadatos asociados y abre el forms de edición con todos los dibujos (si son varios) y los metadatos, debe tener presente el ID de la serie
- para cargar imágenes "files" pulsar un botón, que abra un selector de archivos múltiples, con formatos (png, jpg, jpeg, gif, bmp, webm), las imágnees cargadas aparecerán en la interfaz pero aún no se moverán o copiarán archivos, por defecto abre la carpeta origen/
- poder eliminar imágenes cargadas en la interfaz, solo desvincula el archivo de la UI, no lo elimina como tal
- editar los metadatos que a futuro irán a data.json para editar la serie
- habrá un selector con las carpetas que existen dentro de miarte/
- los tags son textos separados por comas, a la hora de guardar, se convierten en array de strings
- el atributo "style" es un desplegable con las opciónes de style, ver apartado "Metadatos JSON"
- botón de guardar, compara los metadatos nuevos con los de data.json para el ID obtenido, según eso, elimina la metadata y mueve dibujos a papelera/ cuando no hay dibujos en la nueva metadata, o mueve todo a otra carpeta si la carpeta cambió, o agrega o elimina dibujos, siempre respetando las reglas de eliminación en papelera/ y movimientos sin duplicar archivos, si salió bien retorna a main.py

### codigo/genera_html

- pendiente...

## Metadatos JSON

### data.json

cada carpeta en miarte/ tiene un data.json, cada carpeta es un grupo temático, esta primera parte contiene los datos de dicho grupo

- title - str (título de la carpeta o grupo)
- description - str (descripción de la carpeta o grupo)
- file - str (nombre de archivo que hace de portada)

y para cada serie de dibujos hay una estructura como la siguiente, tener en cuenta que una serie puede constar de solo un dibujo o de varios que actúan como si fueran uno, por eso files y no file

- id - str (identificador único de la serie, válido en todo miarte/)
- title - str (título de la serie de dibujos)
- description - str (descripción de la serie de dibujos)
- year - int (el año en que fueron hechos los dibujos)
- tags - array-str (etiquetas para identificar los dibujos)
- nsfw - bool (true si los dibujos tienen contenido sexual)
- files - array-str (nombres de archivos de los dibujos)
- style - str (qué tipo de dibujo es, esto es como otro tag)

para el caso de style, los posibles strings son: sketch, vectorial, ilustración, sprite, asset, tradicional, pixelart, lowdigital, modelo3D, manualidad, fotografía, animación, procedural, textura, editor, mixto, otro

### autor.json

- name - str (nombre completo del autor)
- nickname - str (nombre artístico del autor)
- birth - int (año en que nació el autor)
- zodiac - str (signo zodiacal del autor)
- country - str (país de origen del autor)
- websites - array-str (links web diversos asociados al autor)
- gender - str (género de identificación del autor)
- languaje - str (idioma en el que está el repositorio, código)
- description - str (descripción biográfica del autor)
- repository - str (link al repositorio original)
- email - str (correo electrónico del autor)

## License

All artwork in this repository is released under the
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0).

You are welcome to:

- copy
- download
- modify
- redistribute
- use in free projects

As long as you:

- credit **Omwekiatl**
- keep the same license (ShareAlike)
- do not use the artwork commercially

Commercial licenses are available by contacting the author **ojorcio@gmail.com**
