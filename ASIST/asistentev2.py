import speech_recognition as sr
import pyttsx3
import pywhatkit
import webbrowser
import json
import os
import time
from PIL import Image
import subprocess
import platform

# --- CONFIGURACIÓN ---

# Palabra para activar el asistente
PALABRA_ACTIVACION = "eva" 
# Umbral de energía para el micrófono. Más alto = menos sensible al ruido.
ENERGY_THRESHOLD = 350
# Tiempo en segundos que el asistente esperará por un comando antes de volver a modo pasivo.
CONVERSATION_TIMEOUT = 30

# Inicialización del motor de voz
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# Puedes experimentar con otras voces si tienes más instaladas
# engine.setProperty('voice', voices[0].id) 

# --- CARGA DE DATOS ---

def cargar_favoritos():
    try:
        with open('favoritos.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Advertencia: No se encontró 'favoritos.json'. La función de favoritos no estará disponible.")
        return {}

FAVORITOS = cargar_favoritos()

# --- FUNCIONES BÁSICAS DEL ASISTENTE ---

def hablar(texto):
    """Hace que el asistente hable."""
    print(f"Asistente: {texto}")
    engine.say(texto)
    engine.runAndWait()

def escuchar_comando(timeout=5):
    """Escucha la voz del usuario con mejor manejo de ruido."""
    listener = sr.Recognizer()
    listener.energy_threshold = ENERGY_THRESHOLD
    listener.pause_threshold = 0.8

    with sr.Microphone() as source:
        print("Calibrando ruido de fondo...")
        listener.adjust_for_ambient_noise(source, duration=1.5)
        print("Escuchando...")
        
        try:
            audio = listener.listen(source, timeout=timeout, phrase_time_limit=15)
            # Usamos el idioma específico que te funcionaba bien
            comando = listener.recognize_google(audio, language="es-CO")
            print(f"Usuario: {comando}")
            return comando.lower()
        except sr.WaitTimeoutError:
            return "timeout"
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            hablar("No puedo conectar con el servicio de reconocimiento de voz.")
            return ""

# --- MÓDULOS DE ACCIONES (NUEVOS Y ANTIGUOS) ---

def comprimir_imagenes():
    # Tu función de compresión de imágenes (sin cambios)
    hablar("Claro, ¿en qué carpeta quieres comprimir? ¿Escritorio, descargas, imágenes o documentos?")
    respuesta_carpeta = escuchar_comando()

    if not respuesta_carpeta or respuesta_carpeta == "timeout":
        hablar("No escuché una carpeta. Cancelando.")
        return

    directorios = {
        "descargas": os.path.join(os.path.expanduser('~'), "Downloads"),
        "escritorio": os.path.join(os.path.expanduser('~'), "Desktop"),
        "imágenes": os.path.join(os.path.expanduser('~'), "Pictures"),
        "documentos": os.path.join(os.path.expanduser('~'), "Documents")
    }

    ruta_carpeta = next((directorios[clave] for clave in directorios if clave in respuesta_carpeta), None)

    if not ruta_carpeta:
        hablar("No reconocí esa carpeta. Intenta de nuevo.")
        return

    ruta_salida = os.path.join(ruta_carpeta, "comprimidas")
    if not os.path.exists(ruta_salida): os.makedirs(ruta_salida)

    hablar(f"Entendido. Comprimiendo imágenes en tu carpeta de {os.path.basename(ruta_carpeta)}.")
    count = 0
    for archivo in os.listdir(ruta_carpeta):
        if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            try:
                ruta_completa = os.path.join(ruta_carpeta, archivo)
                img = Image.open(ruta_completa)
                img.save(os.path.join(ruta_salida, archivo), optimize=True, quality=85)
                count += 1
            except Exception as e:
                print(f"No se pudo comprimir {archivo}. Error: {e}")
    
    hablar(f"Listo. He comprimido {count} imágenes." if count > 0 else "No encontré imágenes para comprimir.")

def buscar_en_youtube():
    hablar("Por supuesto, ¿qué te gustaría que buscara en YouTube?")
    tema = escuchar_comando()
    if tema and tema != "timeout":
        hablar(f"Buscando '{tema}' en YouTube.")
        pywhatkit.playonyt(tema)
    else:
        hablar("No escuché qué buscar. Cancelando.")

def reproducir_favorito(comando):
    for nombre, url in FAVORITOS.items():
        if nombre.lower() in comando:
            hablar(f"Reproduciendo tu favorito: {nombre}.")
            webbrowser.open(url)
            return True
    return False

# --- NUEVAS FUNCIONES MODULARES ---

def buscar_en_google(comando):
    """Busca en Google lo que venga después de la palabra 'busca'."""
    termino_busqueda = comando.partition('busca')[-1].strip()
    if termino_busqueda:
        hablar(f"Buscando '{termino_busqueda}' en Google.")
        url = f"https://www.google.com/search?q={termino_busqueda}"
        webbrowser.open(url)
    else:
        hablar("No escuché qué buscar. Por favor, inténtalo de nuevo, por ejemplo: 'busca el clima de hoy'.")

def abrir_aplicacion_sistema(comando):
    """Abre aplicaciones del sistema como la calculadora o el administrador de tareas."""
    sistema = platform.system()
    app_cmd = ""
    app_name = ""

    if "calculadora" in comando:
        app_name = "la calculadora"
        if sistema == "Windows": app_cmd = "calc.exe"
        elif sistema == "Darwin": app_cmd = "open -a Calculator"
        else: app_cmd = "gnome-calculator"
    
    elif "administrador de tareas" in comando:
        app_name = "el administrador de tareas"
        if sistema == "Windows": app_cmd = "taskmgr.exe"
        elif sistema == "Darwin": app_cmd = "open -a 'Activity Monitor'"
        else: app_cmd = "gnome-system-monitor"

    if app_cmd and app_name:
        hablar(f"Abriendo {app_name}.")
        try:
            subprocess.Popen(app_cmd, shell=True)
        except Exception as e:
            hablar(f"Tuve un problema al intentar abrir {app_name}.")
            print(f"Error: {e}")
    else:
        hablar("No reconocí esa aplicación del sistema.")

def apagar_equipo():
    """Inicia la secuencia de apagado con confirmación."""
    hablar("¿Estás completamente seguro de que quieres apagar el equipo? Esta acción no se puede deshacer. Responde sí o no.")
    confirmacion = escuchar_comando(timeout=10)
    
    if confirmacion and "sí" in confirmacion:
        hablar("Confirmado. Apagando el equipo en 3 segundos.")
        if platform.system() == "Windows":
            os.system("shutdown /s /t 3")
        elif platform.system() in ["Darwin", "Linux"]:
            os.system("sudo shutdown -h now") # Puede requerir contraseña
    else:
        hablar("De acuerdo, operación cancelada.")

# --- FUNCIÓN PRINCIPAL CON MODO CONVERSACIÓN ---

def ejecutar_asistente():
    hablar("Asistente iniciado.")
    while True:
        print(f"Esperando la palabra de activación '{PALABRA_ACTIVACION}'...")
        # Usamos `or ''` para evitar errores si `escuchar_comando` devuelve None
        if PALABRA_ACTIVACION in (escuchar_comando() or ''):
            hablar("Hola, estoy a tu servicio.")
            last_command_time = time.time()

            # Inicia el modo conversación
            while time.time() - last_command_time < CONVERSATION_TIMEOUT:
                comando_usuario = escuchar_comando(timeout=10)

                if comando_usuario and comando_usuario != "timeout":
                    last_command_time = time.time() # Reinicia el contador con cada comando

                    # --- ENRUTADOR DE COMANDOS ---
                    if "comprime las imágenes" in comando_usuario or "comprimir imágenes" in comando_usuario:
                        comprimir_imagenes()
                    elif "busca en youtube" in comando_usuario:
                        buscar_en_youtube()
                    elif "reproduce mi" in comando_usuario or "pon mi" in comando_usuario:
                        if not reproducir_favorito(comando_usuario):
                            hablar("No encontré ese favorito en tu lista.")
                    # --- NUEVOS COMANDOS ---
                    elif "busca" in comando_usuario:
                        buscar_en_google(comando_usuario)
                    elif "calculadora" in comando_usuario or "administrador de tareas" in comando_usuario:
                        abrir_aplicacion_sistema(comando_usuario)
                    elif "apaga el equipo" in comando_usuario:
                        apagar_equipo()
                    # --- COMANDOS DE SALIDA ---
                    elif "detente" in comando_usuario or "para" in comando_usuario or "adiós" in comando_usuario:
                        hablar("De acuerdo. Vuelvo a modo pasivo.")
                        break # Rompe el bucle de conversación
                    else:
                        hablar("No reconocí ese comando. Intenta de nuevo.")

                elif comando_usuario == "timeout":
                    print("Silencio detectado, esperando...")
            
            # Este mensaje se muestra cuando el bucle `while` termina por el timeout
            else:
                hablar("Tiempo de espera agotado. Vuelvo a modo pasivo.")

if __name__ == "__main__":
    ejecutar_asistente()