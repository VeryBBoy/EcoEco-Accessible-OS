# Tutorial para crear una aplicación gráfica que de feedback al usuario cuando utilice el reconocimiento de voz

## PASO 1: Instalar las dependencias necesarias en nuestro Debian

Ejecuta el siguiente comando en tu terminal para instalar las bibliotecas requeridas en Debian

```bash
sudo apt update && sudo apt install -y libxcb-cursor0 libxkbcommon-x11-0
```

## PASO 2: Instalar las dependencias necesarias en nuestro entorno virtual

Activa el entorno virtual

```bash
source ~/vosk_env/bin/activate
```

Instala PyQt6

```bash
pip install PyQt6
```

## PASO 3: Descargamos el script que nos permite correr nuestra aplicación y con la función de poder crear un carpeta por voz

Descarga el archivo 

Ejecuta la aplicación

```bash
python voice_folder_creator_app.py
```

## Ejemplos de salida
