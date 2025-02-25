# Crear una aplicación gráfica que de feedback al usuario cuando utilice el reconocimiento de voz para crear un carpeta

Si quieres aprender a utilizar Vosk para crear aplicaciones gráficas que te permitan llevar a cabo más acciones, a parte de crear una carpeta por voz, consulta el siguiente archivo [005-mas-acciones-app.md](https://github.com/verybboy/EcoEco-Accessible-OS/blob/main/virtual-environment-vosk/tutorial-ES/005-mas-acciones-app.md)

## PASO 1: Instalar las dependencias necesarias en nuestro Debian

Ejecuta el siguiente comando en tu terminal para instalar las bibliotecas requeridas en Debian:

```bash
sudo apt update && sudo apt install -y libxcb-cursor0 libxkbcommon-x11-0
```

## PASO 2: Instalar las dependencias necesarias en nuestro entorno virtual

Activa el entorno virtual:

```bash
source ~/vosk_env/bin/activate
```

Instala PyQt6:

```bash
pip install PyQt6
```

## PASO 3: Descargamos el script que nos permite correr nuestra aplicación y con la función de poder crear un carpeta por voz

**¡IMPORTANTE!** Aunque los nombres de los scripts estén en inglés, hay diferentes versiones para cada idioma.

Descarga el archivo [voice_folder_creator_app.py](https://github.com/verybboy/EcoEco-Accessible-OS/blob/main/virtual-environment-vosk/tutorial-ES/scripts/voice_folder_creator_app.py)

Ejecuta la aplicación:

```bash
python voice_folder_creator_app.py
```

## Ejemplos de salida

![Salida voice_folder_creator_app.py](../images/image_003.png)