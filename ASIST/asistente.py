import speech_recognition as sr
import pyttsx3
import pywhatkit
import webbrowser
import json
import os
import time
from PIL import Image

# --- CONFIGURACIÓN MEJORADA ---

# 1. Ajustes de Audio y Conversación
PALABRA_ACTIVACION = "python"
# Umbral de energía para el micrófono. Más alto = menos sensible al ruido. Empieza con 300 y ajústalo si es necesario.
ENERGY_THRESHOLD = 350
# Tiempo en segundos que el asistente esperará por un comando antes de volver a modo pasivo.
CONVERSATION_TIMEOUT = 30

# 2. Inicialización del motor de voz
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# --- CARGA DE DATOS ---

def cargar_favoritos():
    try:
        with open('favoritos.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Advertencia: No se encontró el archivo 'favoritos.json'. La función de favoritos no estará disponible.")
        return {}

FAVORITOS = cargar_favoritos()

# --- FUNCIONES BÁSICAS DEL ASISTENTE (CON MEJORAS) ---

def hablar(texto):
    """Hace que el asistente hable."""
    print(f"Asistente: {texto}")
    engine.say(texto)
    engine.runAndWait()

def escuchar_comando(timeout=5):
    """Escucha la voz del usuario con mejor manejo de ruido."""
    listener = sr.Recognizer()
    listener.energy_threshold = ENERGY_THRESHOLD
    listener.pause_threshold = 0.8 # Tiempo de silencio para considerar que una frase ha terminado

    with sr.Microphone() as source:
        # Calibración de ruido mejorada
        print("Calibrando ruido de fondo, por favor espera...")
        listener.adjust_for_ambient_noise(source, duration=1.5)
        print("Escuchando...")
        
        try:
            audio = listener.listen(source, timeout=timeout, phrase_time_limit=15)
            comando = listener.recognize_google(audio, language="es-CO")
            print(f"Usuario: {comando}")
            return comando.lower()
        except sr.WaitTimeoutError:
            return "timeout" # Devolvemos una palabra clave para manejar el tiempo de espera
        except sr.UnknownValueError:
            return "" # No entendió, devuelve vacío
        except sr.RequestError:
            hablar("No puedo conectar con el servicio de reconocimiento de voz.")
            return ""

# --- MÓDULOS DE ACCIONES (INTERACTIVOS) ---

def comprimir_imagenes():
    """Función interactiva para comprimir imágenes."""
    hablar("Claro, ¿en qué carpeta quieres comprimir las imágenes? Puedes decir escritorio, descargas, imágenes o documentos.")
    respuesta_carpeta = escuchar_comando()

    if not respuesta_carpeta or respuesta_carpeta == "timeout":
        hablar("No escuché una carpeta. Cancelando la operación.")
        return

    directorios = {
        "descargas": os.path.join(os.path.expanduser('~'), "Downloads"),
        "escritorio": os.path.join(os.path.expanduser('~'), "Desktop"),
        "imágenes": os.path.join(os.path.expanduser('~'), "Pictures"),
        "documentos": os.path.join(os.path.expanduser('~'), "Documents")
    }

    nombre_carpeta = ""
    for clave in directorios.keys():
        if clave in respuesta_carpeta:
            nombre_carpeta = clave
            break

    if not nombre_carpeta:
        hablar(f"No reconocí la carpeta en tu respuesta. Por favor, intenta de nuevo.")
        return

    ruta_carpeta = directorios[nombre_carpeta]
    ruta_salida = os.path.join(ruta_carpeta, "comprimidas")
    if not os.path.exists(ruta_salida): os.makedirs(ruta_salida)

    hablar(f"Entendido. Comprimiendo imágenes en la carpeta {nombre_carpeta}.")
    count = 0
    # (El resto de la lógica de compresión sigue igual)
    for archivo in os.listdir(ruta_carpeta):
        if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            try:
                ruta_completa = os.path.join(ruta_carpeta, archivo)
                img = Image.open(ruta_completa)
                img.save(os.path.join(ruta_salida, archivo), optimize=True, quality=85)
                count += 1
            except Exception as e:
                print(f"No se pudo comprimir el archivo {archivo}. Error: {e}")
    
    hablar(f"Listo. He comprimido {count} imágenes." if count > 0 else "No encontré imágenes para comprimir.")


def buscar_en_youtube():
    """Función interactiva para buscar en YouTube."""
    hablar("Por supuesto, ¿qué te gustaría que buscara?")
    tema = escuchar_comando()
    if tema and tema != "timeout":
        hablar(f"Buscando '{tema}' en YouTube.")
        pywhatkit.playonyt(tema)
    else:
        hablar("No escuché qué buscar. Cancelando.")

def reproducir_favorito(comando):
    """Reproduce un video de la lista de favoritos."""
    for nombre, url in FAVORITOS.items():
        if nombre in comando:
            hablar(f"Reproduciendo tu favorito: {nombre}.")
            webbrowser.open(url)
            return True # Devuelve True si encontró un favorito
    return False # Devuelve False si no encontró nada


# --- FUNCIÓN PRINCIPAL (CON MODO CONVERSACIÓN) ---

def ejecutar_asistente():
    """Bucle principal con modo conversación y tiempo de espera."""
    hablar("Asistente iniciado.")
    while True:
        print("Esperando la palabra de activación 'python'...")
        if PALABRA_ACTIVACION in (escuchar_comando() or ''):
            hablar("Hola, estoy a tu servicio.")
            last_command_time = time.time()

            # Inicia el modo conversación
            while time.time() - last_command_time < CONVERSATION_TIMEOUT:
                comando_usuario = escuchar_comando(timeout=10)

                if comando_usuario and comando_usuario != "timeout":
                    # Si se detecta un comando, se reinicia el contador de tiempo
                    last_command_time = time.time()

                    # MÓDULOS DE ACCIONES
                    if "comprime las imágenes" in comando_usuario or "comprimir imágenes" in comando_usuario:
                        comprimir_imagenes()
                    elif "busca en youtube" in comando_usuario:
                        buscar_en_youtube()
                    elif "reproduce mi" in comando_usuario or "pon mi" in comando_usuario:
                        if not reproducir_favorito(comando_usuario):
                            hablar("No encontré ese favorito en tu lista.")
                    elif "detente" in comando_usuario or "para" in comando_usuario or "adiós" in comando_usuario:
                        hablar("De acuerdo. Vuelvo a modo pasivo.")
                        break # Rompe el bucle de conversación
                    else:
                        hablar("No reconocí ese comando. Intenta de nuevo.")

                elif comando_usuario == "timeout":
                    # Si hay silencio, no hagas nada, solo deja que el bucle `while` compruebe el tiempo de espera.
                    print("Silencio detectado, esperando...")
            
            else: # Este `else` se ejecuta cuando el `while` termina de forma natural (por el timeout)
                hablar("Tiempo de espera agotado. Vuelvo a modo pasivo.")


if __name__ == "__main__":
    ejecutar_asistente()