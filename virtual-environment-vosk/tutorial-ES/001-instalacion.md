# Tutorial para crear un etorno virtual de pruebas en Debian para la utilización de vosk 

Esto es un tutorial paso a paso para crear un entorno virtual en Python y crear nuestros primeros scripts de reconocimiento de voz con Vosk

## Paso 1: Instalar el paquete necesario para crear el entorno virtual de python

```bash
apt install python3-venv -y
```

## Paso 2: Crear un entorno virtual en tu directorio home

```bash
python3 -m venv ~/vosk_env
```

## Paso 3: Activar el entorno virtual

```bash
source ~/vosk_env/bin/activate
```

## Paso 4: Instalar Vosk y las bibliotecas necesarias dentro del entorno virtual

```bash
pip install vosk numpy
```

## Paso 5: Descargar un modelo de voz

```bash
mkdir -p ~/vosk_models && cd ~/vosk_models

wget https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip

unzip vosk-model-small-es-0.42.zip

mv vosk-model-small-es-0.42 model-es
```

## Paso 7: Instalamos PortAudio dentro de nuestro Debian

PortAudio es una biblioteca que maneja el audio en **sounddevide**

Salimos de nuestro entorno virtual

```bash
deactivate
```

Instalamos PortAudio en nuestro SO

```bash
sudo apt install portaudio19-dev -y
```

## Paso 8: Instalamos Sounddevice en nuestro entorno virtual

Activamos nuestro entorno virtual

```bash
source ~/vosk_env/bin/activate
```

Instalamos **sounddevide**

```bash
pip install sounddevice
```

Verificamos la instalación de sounddevice

```bash
python3 -c "import sounddevice as sd; print(sd.query_devices())"
```

Si muestra una lista de dispositivos de audio, significa que PortAudio ya está funcionando.

## Paso 6: Creamos un script para hacer una prueba de reconocimiento de voz

**¡IMPORTANTE!** Aunque los nombres de los scripts estén en inglés, hay diferentes versiones para cada idioma.

Descarga el archivo [test_vosk.py](https://github.com/verybboy/EcoEco-Accessible-OS/blob/main/virtual-environment-vosk/tutorial-ES/scripts/test_vosk.py)

Ejecutamos el scrypt

```bash
python3 ~/test_vosk.py
```

## Ejemplo de salida

![Salida test_vosk.py](../images/image_001.png)