import speech_recognition as sr
import pyttsx3
import pywhatkit
import webbrowser
import json
import os
import time
import threading
import subprocess
import platform
import psutil
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
import customtkinter as ctk
import tkinter as tk
from datetime import datetime
import requests
from plyer import notification
import schedule

# --- CONFIGURACIÓN GLOBAL ---
PALABRA_ACTIVACION = "eva"
ENERGY_THRESHOLD = 350
CONVERSATION_TIMEOUT = 30

# Inicialización optimizada del motor de voz
engine = pyttsx3.init()
engine.setProperty('rate', 220)  # Más rápido
engine.setProperty('volume', 0.9)
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)  # Voz femenina si está disponible

# Inicialización optimizada del reconocedor
listener = sr.Recognizer()
listener.energy_threshold = ENERGY_THRESHOLD
listener.pause_threshold = 0.5  # Más rápido
listener.phrase_threshold = 0.3

# --- FUNCIONES OPTIMIZADAS ---

def cargar_favoritos():
    try:
        with open('favoritos.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Creando archivo de favoritos...")
        favoritos_default = {
            "música relajante": "https://www.youtube.com/watch?v=jfKfPfyJRdk",
            "noticias": "https://www.youtube.com/watch?v=live_news"
        }
        with open('favoritos.json', 'w', encoding='utf-8') as f:
            json.dump(favoritos_default, f, indent=2, ensure_ascii=False)
        return favoritos_default

FAVORITOS = cargar_favoritos()

def hablar(texto, priority=False):
    """Hablar optimizado con prioridad"""
    print(f"Asistente: {texto}")
    if priority:
        engine.stop()  # Detiene cualquier habla anterior
    engine.say(texto)
    engine.runAndWait()

def escuchar_comando_optimizado(timeout=3):
    """Escucha optimizada y más rápida"""
    with sr.Microphone() as source:
        try:
            # Calibración rápida solo si es necesario
            listener.adjust_for_ambient_noise(source, duration=0.5)
            audio = listener.listen(source, timeout=timeout, phrase_time_limit=8)
            
            # Reconocimiento en paralelo para mayor velocidad
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(listener.recognize_google, audio, language="es-CO")
                comando = future.result(timeout=5)
                print(f"Usuario: {comando}")
                return comando.lower()
        except:
            return ""

# --- FUNCIONES DE SISTEMA OPTIMIZADAS ---

def obtener_info_sistema():
    """Información del sistema ultra rápida"""
    try:
        cpu = psutil.cpu_percent(interval=0.1)
        memoria = psutil.virtual_memory().percent
        disco = psutil.disk_usage('/').percent
        return f"CPU al {cpu:.1f}%, RAM al {memoria:.1f}%, disco al {disco:.1f}%"
    except:
        return "No pude obtener la información del sistema"

def abrir_app_rapido(app_name):
    """Apertura ultra rápida de aplicaciones"""
    sistema = platform.system()
    apps = {
        "Windows": {
            "calculadora": "calc.exe",
            "notepad": "notepad.exe",
            "explorador": "explorer.exe",
            "administrador": "taskmgr.exe",
            "paint": "mspaint.exe"
        },
        "Darwin": {
            "calculadora": "open -a Calculator",
            "notas": "open -a TextEdit",
            "finder": "open -a Finder",
            "monitor": "open -a 'Activity Monitor'"
        },
        "Linux": {
            "calculadora": "gnome-calculator",
            "editor": "gedit",
            "archivos": "nautilus",
            "monitor": "gnome-system-monitor"
        }
    }
    
    cmd = apps.get(sistema, {}).get(app_name)
    if cmd:
        # Usar Popen para no bloquear
        subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    return False

def buscar_youtube_rapido(query):
    """Búsqueda de YouTube optimizada"""
    try:
        # Usar threading para no bloquear
        def abrir_youtube():
            pywhatkit.playonyt(query)
        
        thread = threading.Thread(target=abrir_youtube)
        thread.daemon = True
        thread.start()
        return True
    except:
        return False

def buscar_google_rapido(query):
    """Búsqueda de Google ultra rápida"""
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    threading.Thread(target=lambda: webbrowser.open(url), daemon=True).start()

def controlar_volumen(accion):
    """Control de volumen rápido"""
    sistema = platform.system()
    if sistema == "Windows":
        if accion == "subir":
            os.system("nircmd changesysvolume 5000")
        elif accion == "bajar":
            os.system("nircmd changesysvolume -5000")
        elif accion == "silenciar":
            os.system("nircmd mutesysvolume 1")

def obtener_clima_rapido():
    """Obtiene el clima de forma rápida"""
    try:
        # API gratuita de OpenWeatherMap (necesitas registrarte)
        # Por simplicidad, retornamos un mensaje genérico
        return "El clima está agradable hoy"
    except:
        return "No pude obtener el clima"

def crear_recordatorio(mensaje, minutos):
    """Crea recordatorios rápidos"""
    def mostrar_recordatorio():
        time.sleep(minutos * 60)
        notification.notify(
            title="Recordatorio EVA",
            message=mensaje,
            timeout=10
        )
    
    threading.Thread(target=mostrar_recordatorio, daemon=True).start()
    return f"Recordatorio creado para {minutos} minutos"

# --- INTERFAZ GRÁFICA MODERNA ---

class AsistenteEVA:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("EVA - Asistente Virtual Avanzado")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        self.asistente_activo = False
        self.modo_conversacion = False
        self.ultimo_comando_tiempo = 0
        
        self.setup_ui()
        self.setup_executor()
        
    def setup_executor(self):
        """Configura el executor para tareas paralelas"""
        self.executor = ThreadPoolExecutor(max_workers=3)
        
    def setup_ui(self):
        # Frame principal con gradiente simulado
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título con estilo
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(20, 10))
        
        title_label = ctk.CTkLabel(title_frame, text="🤖 EVA", 
                                  font=ctk.CTkFont(size=45, weight="bold"))
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(title_frame, text="Asistente Virtual Inteligente", 
                                     font=ctk.CTkFont(size=16))
        subtitle_label.pack()
        
        # Panel de estado
        status_frame = ctk.CTkFrame(self.main_frame)
        status_frame.pack(fill="x", padx=20, pady=10)
        
        self.status_label = ctk.CTkLabel(status_frame, text="🔴 Estado: Inactivo", 
                                        font=ctk.CTkFont(size=18, weight="bold"))
        self.status_label.pack(pady=10)
        
        # Indicador de audio visual
        self.audio_frame = ctk.CTkFrame(status_frame, height=60)
        self.audio_frame.pack(fill="x", pady=5)
        
        self.audio_canvas = tk.Canvas(self.audio_frame, height=50, bg="#2b2b2b", highlightthickness=0)
        self.audio_canvas.pack(fill="x", padx=10, pady=5)
        
        # Panel de información del sistema
        info_frame = ctk.CTkFrame(self.main_frame)
        info_frame.pack(fill="x", padx=20, pady=5)
        
        self.info_label = ctk.CTkLabel(info_frame, text="Sistema: Esperando...", 
                                      font=ctk.CTkFont(size=12))
        self.info_label.pack(pady=5)
        
        # Log de conversación mejorado
        log_frame = ctk.CTkFrame(self.main_frame)
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        log_title = ctk.CTkLabel(log_frame, text="💬 Conversación", 
                                font=ctk.CTkFont(size=16, weight="bold"))
        log_title.pack(pady=(10, 5))
        
        self.conversation_text = ctk.CTkTextbox(log_frame, height=250, 
                                               font=ctk.CTkFont(size=12))
        self.conversation_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Panel de controles
        control_frame = ctk.CTkFrame(self.main_frame)
        control_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Botones principales
        button_frame1 = ctk.CTkFrame(control_frame, fg_color="transparent")
        button_frame1.pack(fill="x", pady=5)
        
        self.start_button = ctk.CTkButton(button_frame1, text="🚀 Iniciar EVA", 
                                         command=self.toggle_asistente,
                                         height=40, font=ctk.CTkFont(size=16, weight="bold"))
        self.start_button.pack(side="left", padx=5, expand=True, fill="x")
        
        self.voice_button = ctk.CTkButton(button_frame1, text="🎤 Escuchar", 
                                         command=self.escuchar_manual,
                                         height=40)
        self.voice_button.pack(side="right", padx=5)
        
        # Botones secundarios
        button_frame2 = ctk.CTkFrame(control_frame, fg_color="transparent")
        button_frame2.pack(fill="x", pady=5)
        
        ctk.CTkButton(button_frame2, text="⚙️ Config", 
                     command=self.abrir_configuracion).pack(side="left", padx=2)
        ctk.CTkButton(button_frame2, text="📊 Sistema", 
                     command=self.mostrar_info_sistema).pack(side="left", padx=2)
        ctk.CTkButton(button_frame2, text="🧹 Limpiar", 
                     command=self.limpiar_log).pack(side="left", padx=2)
        ctk.CTkButton(button_frame2, text="💾 Guardar", 
                     command=self.guardar_log).pack(side="right", padx=2)
        
        # Actualizar info del sistema periódicamente
        self.actualizar_info_sistema()
    
    def agregar_mensaje(self, tipo, mensaje, color=None):
        """Agrega mensajes al log con timestamp y colores"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if tipo == "Usuario":
            emoji = "👤"
            color_text = "#4CAF50"
        elif tipo == "EVA":
            emoji = "🤖"
            color_text = "#2196F3"
        else:
            emoji = "ℹ️"
            color_text = "#FF9800"
        
        mensaje_formateado = f"[{timestamp}] {emoji} {tipo}: {mensaje}\n"
        
        self.conversation_text.insert("end", mensaje_formateado)
        self.conversation_text.see("end")
        
        # Mantener solo los últimos 100 mensajes para rendimiento
        lines = self.conversation_text.get("1.0", "end").split('\n')
        if len(lines) > 100:
            self.conversation_text.delete("1.0", "20.0")
    
    def actualizar_info_sistema(self):
        """Actualiza la información del sistema cada 5 segundos"""
        try:
            info = obtener_info_sistema()
            self.info_label.configure(text=f"💻 {info}")
        except:
            self.info_label.configure(text="💻 Sistema: Error al obtener datos")
        
        # Programar la próxima actualización
        self.root.after(5000, self.actualizar_info_sistema)
    
    def mostrar_indicador_audio(self, activo=False):
        """Muestra indicador visual de audio"""
        self.audio_canvas.delete("all")
        width = self.audio_canvas.winfo_width()
        height = self.audio_canvas.winfo_height()
        
        if width > 1 and activo:  # Solo si el canvas está inicializado
            # Simular ondas de audio
            for i in range(0, width, 20):
                color = "#00ff00" if activo else "#333333"
                self.audio_canvas.create_rectangle(i, height//2-10, i+15, height//2+10, 
                                                 fill=color, outline="")
    
    def toggle_asistente(self):
        """Inicia/detiene el asistente"""
        if not self.asistente_activo:
            self.asistente_activo = True
            self.start_button.configure(text="⏹️ Detener EVA")
            self.status_label.configure(text="🟢 Estado: Activo - Escuchando...")
            self.agregar_mensaje("Sistema", "EVA iniciado correctamente")
            
            # Iniciar en hilo separado
            threading.Thread(target=self.ejecutar_asistente_loop, daemon=True).start()
        else:
            self.asistente_activo = False
            self.modo_conversacion = False
            self.start_button.configure(text="🚀 Iniciar EVA")
            self.status_label.configure(text="🔴 Estado: Inactivo")
            self.agregar_mensaje("Sistema", "EVA desactivado")
    
    def escuchar_manual(self):
        """Escucha un comando manual"""
        if not self.asistente_activo:
            self.agregar_mensaje("Sistema", "Escuchando comando manual...")
            self.mostrar_indicador_audio(True)
            
            comando = escuchar_comando_optimizado(timeout=5)
            self.mostrar_indicador_audio(False)
            
            if comando:
                self.agregar_mensaje("Usuario", comando)
                self.procesar_comando(comando)
            else:
                self.agregar_mensaje("Sistema", "No se detectó comando")
    
    def ejecutar_asistente_loop(self):
        """Loop principal del asistente optimizado"""
        hablar("EVA activado y listo para ayudar", priority=True)
        
        while self.asistente_activo:
            try:
                # Escuchar palabra de activación
                if not self.modo_conversacion:
                    self.root.after(0, lambda: self.status_label.configure(
                        text=f"🟡 Esperando '{PALABRA_ACTIVACION}'..."))
                    
                    comando = escuchar_comando_optimizado(timeout=2)
                    
                    if comando and PALABRA_ACTIVACION in comando:
                        self.modo_conversacion = True
                        self.ultimo_comando_tiempo = time.time()
                        
                        self.root.after(0, lambda: self.agregar_mensaje("Usuario", comando))
                        self.root.after(0, lambda: self.status_label.configure(
                            text="🟢 Modo conversación activo"))
                        
                        hablar("Hola, ¿en qué puedo ayudarte?", priority=True)
                        continue
                
                # Modo conversación activo
                if self.modo_conversacion:
                    if time.time() - self.ultimo_comando_tiempo > CONVERSATION_TIMEOUT:
                        self.modo_conversacion = False
                        hablar("Volviendo a modo pasivo")
                        continue
                    
                    self.root.after(0, lambda: self.mostrar_indicador_audio(True))
                    comando = escuchar_comando_optimizado(timeout=8)
                    self.root.after(0, lambda: self.mostrar_indicador_audio(False))
                    
                    if comando:
                        self.ultimo_comando_tiempo = time.time()
                        self.root.after(0, lambda: self.agregar_mensaje("Usuario", comando))
                        
                        # Procesar comando en paralelo
                        self.executor.submit(self.procesar_comando, comando)
                    
                time.sleep(0.1)  # Pequeña pausa para no saturar la CPU
                
            except Exception as e:
                print(f"Error en loop principal: {e}")
                time.sleep(1)
    
    def procesar_comando(self, comando):
        """Procesa comandos de forma ultra rápida"""
        try:
            respuesta = "Comando no reconocido"
            
            # Comandos de salida
            if any(word in comando for word in ["detente", "para", "adiós", "terminar"]):
                self.modo_conversacion = False
                respuesta = "De acuerdo, volviendo a modo pasivo"
            
            # Información del sistema (ultra rápido)
            elif "sistema" in comando or "información" in comando:
                respuesta = obtener_info_sistema()
            
            # Aplicaciones (apertura instantánea)
            elif "calculadora" in comando:
                if abrir_app_rapido("calculadora"):
                    respuesta = "Calculadora abierta"
                else:
                    respuesta = "No pude abrir la calculadora"
            
            elif "notepad" in comando or "bloc de notas" in comando:
                if abrir_app_rapido("notepad"):
                    respuesta = "Bloc de notas abierto"
            
            elif "explorador" in comando or "archivos" in comando:
                if abrir_app_rapido("explorador"):
                    respuesta = "Explorador de archivos abierto"
            
            elif "administrador" in comando or "tareas" in comando:
                if abrir_app_rapido("administrador"):
                    respuesta = "Administrador de tareas abierto"
            
            # Búsquedas (ultra rápidas)
            elif "busca en youtube" in comando:
                query = comando.replace("busca en youtube", "").strip()
                if query:
                    buscar_youtube_rapido(query)
                    respuesta = f"Buscando '{query}' en YouTube"
                else:
                    respuesta = "¿Qué quieres buscar en YouTube?"
            
            elif "busca" in comando and "google" in comando:
                query = comando.replace("busca", "").replace("google", "").strip()
                if query:
                    buscar_google_rapido(query)
                    respuesta = f"Buscando '{query}' en Google"
            
            elif "busca" in comando:
                query = comando.replace("busca", "").strip()
                if query:
                    buscar_google_rapido(query)
                    respuesta = f"Buscando '{query}' en Google"
            
            # Control de volumen
            elif "subir volumen" in comando or "aumentar volumen" in comando:
                controlar_volumen("subir")
                respuesta = "Volumen aumentado"
            
            elif "bajar volumen" in comando or "disminuir volumen" in comando:
                controlar_volumen("bajar")
                respuesta = "Volumen disminuido"
            
            elif "silenciar" in comando:
                controlar_volumen("silenciar")
                respuesta = "Audio silenciado"
            
            # Favoritos
            elif "reproduce" in comando or "pon" in comando:
                encontrado = False
                for nombre, url in FAVORITOS.items():
                    if nombre.lower() in comando:
                        threading.Thread(target=lambda: webbrowser.open(url), daemon=True).start()
                        respuesta = f"Reproduciendo {nombre}"
                        encontrado = True
                        break
                if not encontrado:
                    respuesta = "No encontré ese favorito"
            
            # Clima
            elif "clima" in comando or "tiempo" in comando:
                respuesta = obtener_clima_rapido()
            
            # Recordatorios
            elif "recordar" in comando or "recordatorio" in comando:
                respuesta = "Los recordatorios están en desarrollo"
            
            # Hora actual
            elif "hora" in comando or "qué hora es" in comando:
                hora_actual = datetime.now().strftime("%H:%M")
                respuesta = f"Son las {hora_actual}"
            
            # Fecha actual
            elif "fecha" in comando or "qué día es" in comando:
                fecha_actual = datetime.now().strftime("%d de %B de %Y")
                respuesta = f"Hoy es {fecha_actual}"
            
            # Comprimir imágenes (mejorado)
            elif "comprimir" in comando and "imágenes" in comando:
                self.comprimir_imagenes_rapido()
                return
            
            # Apagar equipo
            elif "apagar" in comando and "equipo" in comando:
                respuesta = "¿Estás seguro? Di 'confirmar apagado' para continuar"
            
            elif "confirmar apagado" in comando:
                respuesta = "Apagando equipo en 10 segundos..."
                if platform.system() == "Windows":
                    os.system("shutdown /s /t 10")
                
            # Responder y actualizar UI
            self.root.after(0, lambda: self.agregar_mensaje("EVA", respuesta))
            hablar(respuesta)
            
        except Exception as e:
            error_msg = f"Error procesando comando: {str(e)}"
            self.root.after(0, lambda: self.agregar_mensaje("Sistema", error_msg))
            hablar("Hubo un error procesando tu comando")
    
    def comprimir_imagenes_rapido(self):
        """Compresión de imágenes optimizada"""
        def proceso_compresion():
            self.root.after(0, lambda: self.agregar_mensaje("EVA", "¿En qué carpeta? (escritorio, descargas, imágenes)"))
            hablar("¿En qué carpeta quieres comprimir? Escritorio, descargas o imágenes")
            
            respuesta = escuchar_comando_optimizado(timeout=10)
            if not respuesta:
                return
            
            directorios = {
                "escritorio": os.path.join(os.path.expanduser('~'), "Desktop"),
                "descargas": os.path.join(os.path.expanduser('~'), "Downloads"),
                "imágenes": os.path.join(os.path.expanduser('~'), "Pictures")
            }
            
            carpeta_elegida = None
            for nombre, ruta in directorios.items():
                if nombre in respuesta:
                    carpeta_elegida = ruta
                    break
            
            if not carpeta_elegida:
                self.root.after(0, lambda: self.agregar_mensaje("EVA", "No reconocí la carpeta"))
                hablar("No reconocí esa carpeta")
                return
            
            # Proceso de compresión en paralelo
            def comprimir():
                try:
                    ruta_salida = os.path.join(carpeta_elegida, "comprimidas")
                    if not os.path.exists(ruta_salida):
                        os.makedirs(ruta_salida)
                    
                    count = 0
                    archivos = [f for f in os.listdir(carpeta_elegida) 
                               if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
                    
                    with ThreadPoolExecutor(max_workers=4) as executor:
                        futures = []
                        for archivo in archivos:
                            future = executor.submit(self.comprimir_imagen_individual, 
                                                   carpeta_elegida, archivo, ruta_salida)
                            futures.append(future)
                        
                        for future in futures:
                            if future.result():
                                count += 1
                    
                    mensaje = f"¡Listo! Comprimí {count} imágenes" if count > 0 else "No encontré imágenes para comprimir"
                    self.root.after(0, lambda: self.agregar_mensaje("EVA", mensaje))
                    hablar(mensaje)
                    
                except Exception as e:
                    error_msg = f"Error en compresión: {str(e)}"
                    self.root.after(0, lambda: self.agregar_mensaje("Sistema", error_msg))
        
        threading.Thread(target=proceso_compresion, daemon=True).start()
    
    def comprimir_imagen_individual(self, carpeta_origen, archivo, carpeta_destino):
        """Comprime una imagen individual"""
        try:
            ruta_completa = os.path.join(carpeta_origen, archivo)
            with Image.open(ruta_completa) as img:
                img.save(os.path.join(carpeta_destino, archivo), 
                        optimize=True, quality=85)
            return True
        except:
            return False
    
    def abrir_configuracion(self):
        """Ventana de configuración"""
        config_window = ctk.CTkToplevel(self.root)
        config_window.title("⚙️ Configuración de EVA")
        config_window.geometry("500x400")
        config_window.transient(self.root)
        
        # Configuración de palabra de activación
        ctk.CTkLabel(config_window, text="Palabra de Activación:", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.palabra_entry = ctk.CTkEntry(config_window, placeholder_text=PALABRA_ACTIVACION)
        self.palabra_entry.pack(pady=5)
        
        # Configuración de sensibilidad
        ctk.CTkLabel(config_window, text="Sensibilidad del Micrófono:", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20,10))
        
        self.sensibilidad_slider = ctk.CTkSlider(config_window, from_=100, to=500, 
                                                number_of_steps=40)
        self.sensibilidad_slider.set(ENERGY_THRESHOLD)
        self.sensibilidad_slider.pack(pady=5)
        
        # Botones
        button_frame = ctk.CTkFrame(config_window, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(button_frame, text="💾 Guardar", 
                     command=lambda: self.guardar_configuracion(config_window)).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="❌ Cancelar", 
                     command=config_window.destroy).pack(side="right", padx=10)
    
    def guardar_configuracion(self, window):
        """Guarda la configuración"""
        global PALABRA_ACTIVACION, ENERGY_THRESHOLD
        
        nueva_palabra = self.palabra_entry.get().strip().lower()
        if nueva_palabra:
            PALABRA_ACTIVACION = nueva_palabra
        
        ENERGY_THRESHOLD = int(self.sensibilidad_slider.get())
        listener.energy_threshold = ENERGY_THRESHOLD
        
        self.agregar_mensaje("Sistema", "Configuración guardada correctamente")
        window.destroy()
    
    def limpiar_log(self):
        """Limpia el log de conversación"""
        self.conversation_text.delete("1.0", "end")
        self.agregar_mensaje("Sistema", "Log limpiado")
    
    def guardar_log(self):
        """Guarda el log en un archivo"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"eva_log_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.conversation_text.get("1.0", "end"))
            
            self.agregar_mensaje("Sistema", f"Log guardado como {filename}")
        except Exception as e:
            self.agregar_mensaje("Sistema", f"Error guardando log: {str(e)}")
    
    def mostrar_info_sistema(self):
        """Muestra información detallada del sistema"""
        try:
            info = f"""
💻 Información del Sistema:
- CPU: {psutil.cpu_percent(interval=1):.1f}%
- RAM: {psutil.virtual_memory().percent:.1f}%
- Disco: {psutil.disk_usage('/').percent:.1f}%
- Procesos: {len(psutil.pids())}
- Red: {'Conectado' if psutil.net_if_stats() else 'Desconectado'}
- Sistema: {platform.system()} {platform.release()}
            """
            self.agregar_mensaje("Sistema", info.strip())
        except Exception as e:
            self.agregar_mensaje("Sistema", f"Error obteniendo info: {str(e)}")
    

    def run(self):
       """Inicia la aplicación"""
       try:
           self.root.mainloop()
       except KeyboardInterrupt:
           print("EVA terminado por el usuario")
       finally:
           self.executor.shutdown(wait=False)

# --- FUNCIONES ADICIONALES RÁPIDAS ---

def obtener_noticias_rapido():
   """Obtiene noticias de forma rápida"""
   try:
       # Simulación de noticias - puedes integrar una API real
       noticias = [
           "Tecnología: Nuevos avances en IA",
           "Ciencia: Descubrimiento espacial",
           "Deportes: Resultados del día"
       ]
       return "Últimas noticias: " + ", ".join(noticias[:2])
   except:
       return "No pude obtener las noticias"

def traducir_texto_rapido(texto, idioma_destino="en"):
   """Traducción rápida básica"""
   traducciones_basicas = {
       "hola": {"en": "hello", "fr": "bonjour"},
       "gracias": {"en": "thank you", "fr": "merci"},
       "adiós": {"en": "goodbye", "fr": "au revoir"}
   }
   
   texto_lower = texto.lower()
   if texto_lower in traducciones_basicas:
       return traducciones_basicas[texto_lower].get(idioma_destino, texto)
   return f"Traducción de '{texto}' no disponible"

def calcular_rapido(expresion):
   """Calculadora rápida para operaciones básicas"""
   try:
       # Limpieza básica de seguridad
       expresion_limpia = ''.join(c for c in expresion if c in '0123456789+-*/()., ')
       resultado = eval(expresion_limpia)
       return f"El resultado es {resultado}"
   except:
       return "No pude realizar el cálculo"

def reproducir_musica_local():
   """Reproduce música local"""
   import glob
   
   try:
       # Buscar archivos de música en carpetas comunes
       rutas_musica = [
           os.path.join(os.path.expanduser('~'), "Music", "*.mp3"),
           os.path.join(os.path.expanduser('~'), "Música", "*.mp3"),
           os.path.join(os.path.expanduser('~'), "Downloads", "*.mp3")
       ]
       
       archivos_musica = []
       for ruta in rutas_musica:
           archivos_musica.extend(glob.glob(ruta))
       
       if archivos_musica:
           archivo_aleatorio = archivos_musica[0]  # Tomar el primero por simplicidad
           if platform.system() == "Windows":
               os.startfile(archivo_aleatorio)
           elif platform.system() == "Darwin":
               subprocess.call(["open", archivo_aleatorio])
           else:
               subprocess.call(["xdg-open", archivo_aleatorio])
           return "Reproduciendo música local"
       else:
           return "No encontré archivos de música"
   except:
       return "Error reproduciendo música"

def crear_nota_rapida(contenido):
   """Crea una nota rápida"""
   try:
       timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
       filename = f"nota_eva_{timestamp}.txt"
       
       with open(filename, 'w', encoding='utf-8') as f:
           f.write(f"Nota creada por EVA - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
           f.write("="*50 + "\n\n")
           f.write(contenido)
       
       return f"Nota guardada como {filename}"
   except:
       return "Error creando la nota"

def organizar_descargas_rapido():
   """Organiza la carpeta de descargas por tipo de archivo"""
   try:
       downloads_path = os.path.join(os.path.expanduser('~'), "Downloads")
       
       tipos_archivo = {
           'Imágenes': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
           'Documentos': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
           'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
           'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
           'Programas': ['.exe', '.msi', '.dmg', '.deb', '.rpm'],
           'Comprimidos': ['.zip', '.rar', '.7z', '.tar', '.gz']
       }
       
       archivos_movidos = 0
       
       for filename in os.listdir(downloads_path):
           if os.path.isfile(os.path.join(downloads_path, filename)):
               extension = os.path.splitext(filename)[1].lower()
               
               for tipo, extensiones in tipos_archivo.items():
                   if extension in extensiones:
                       # Crear carpeta si no existe
                       carpeta_tipo = os.path.join(downloads_path, tipo)
                       if not os.path.exists(carpeta_tipo):
                           os.makedirs(carpeta_tipo)
                       
                       # Mover archivo
                       origen = os.path.join(downloads_path, filename)
                       destino = os.path.join(carpeta_tipo, filename)
                       
                       if not os.path.exists(destino):
                           os.rename(origen, destino)
                           archivos_movidos += 1
                       break
       
       return f"Organizadas las descargas. {archivos_movidos} archivos movidos"
   except Exception as e:
       return f"Error organizando descargas: {str(e)}"

def backup_rapido():
   """Crea un backup rápido de documentos importantes"""
   try:
       timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
       backup_folder = os.path.join(os.path.expanduser('~'), f"Backup_EVA_{timestamp}")
       
       if not os.path.exists(backup_folder):
           os.makedirs(backup_folder)
       
       # Carpetas importantes para backup
       carpetas_importantes = [
           os.path.join(os.path.expanduser('~'), "Documents"),
           os.path.join(os.path.expanduser('~'), "Desktop")
       ]
       
       archivos_copiados = 0
       
       for carpeta in carpetas_importantes:
           if os.path.exists(carpeta):
               carpeta_nombre = os.path.basename(carpeta)
               destino_carpeta = os.path.join(backup_folder, carpeta_nombre)
               
               if not os.path.exists(destino_carpeta):
                   os.makedirs(destino_carpeta)
               
               # Copiar solo archivos importantes (no muy grandes)
               for archivo in os.listdir(carpeta):
                   ruta_archivo = os.path.join(carpeta, archivo)
                   if (os.path.isfile(ruta_archivo) and 
                       os.path.getsize(ruta_archivo) < 10*1024*1024 and  # Menor a 10MB
                       any(archivo.endswith(ext) for ext in ['.txt', '.doc', '.docx', '.pdf', '.jpg', '.png'])):
                       
                       try:
                           import shutil
                           shutil.copy2(ruta_archivo, destino_carpeta)
                           archivos_copiados += 1
                       except:
                           continue
       
       return f"Backup creado en {backup_folder}. {archivos_copiados} archivos respaldados"
   except Exception as e:
       return f"Error creando backup: {str(e)}"

# --- EXTENSIÓN DE LA CLASE PRINCIPAL ---

# Agregar estos métodos a la clase AsistenteEVA existente
def agregar_comandos_adicionales(self, comando):
   """Comandos adicionales para el procesador principal"""
   
   # Noticias
   if "noticias" in comando:
       respuesta = obtener_noticias_rapido()
       return respuesta
   
   # Traducción
   elif "traduce" in comando:
       texto_a_traducir = comando.replace("traduce", "").strip()
       if texto_a_traducir:
           respuesta = traducir_texto_rapido(texto_a_traducir)
       else:
           respuesta = "¿Qué quieres que traduzca?"
       return respuesta
   
   # Calculadora
   elif "calcula" in comando or "cuánto es" in comando:
       expresion = comando.replace("calcula", "").replace("cuánto es", "").strip()
       if expresion:
           respuesta = calcular_rapido(expresion)
       else:
           respuesta = "¿Qué quieres que calcule?"
       return respuesta
   
   # Música local
   elif "pon música" in comando or "reproduce música" in comando:
       respuesta = reproducir_musica_local()
       return respuesta
   
   # Crear nota
   elif "crea una nota" in comando or "anota" in comando:
       contenido = comando.replace("crea una nota", "").replace("anota", "").strip()
       if contenido:
           respuesta = crear_nota_rapida(contenido)
       else:
           respuesta = "¿Qué quieres anotar?"
       return respuesta
   
   # Organizar descargas
   elif "organiza descargas" in comando or "ordena descargas" in comando:
       respuesta = organizar_descargas_rapido()
       return respuesta
   
   # Backup
   elif "haz backup" in comando or "crear respaldo" in comando:
       respuesta = backup_rapido()
       return respuesta
   
   # Comandos de cortesía
   elif any(saludo in comando for saludo in ["hola", "buenos días", "buenas tardes", "buenas noches"]):
       respuesta = "¡Hola! ¿En qué puedo ayudarte hoy?"
       return respuesta
   
   elif "gracias" in comando:
       respuesta = "De nada, siempre es un placer ayudarte"
       return respuesta
   
   elif "cómo estás" in comando:
       respuesta = "Estoy funcionando perfectamente y listo para ayudarte"
       return respuesta
   
   return None

# Modificar el método procesar_comando para incluir los nuevos comandos
def procesar_comando_extendido(self, comando):
   """Versión extendida del procesador de comandos"""
   try:
       # Primero intentar comandos adicionales
       respuesta_adicional = agregar_comandos_adicionales(self, comando)
       if respuesta_adicional:
           self.root.after(0, lambda: self.agregar_mensaje("EVA", respuesta_adicional))
           hablar(respuesta_adicional)
           return
       
       # Si no hay respuesta adicional, usar el procesador original
       self.procesar_comando_original(comando)
       
   except Exception as e:
       error_msg = f"Error procesando comando: {str(e)}"
       self.root.after(0, lambda: self.agregar_mensaje("Sistema", error_msg))
       hablar("Hubo un error procesando tu comando")

# --- SCRIPT PRINCIPAL ---

def main():
   """Función principal optimizada"""
   print("🤖 Iniciando EVA - Asistente Virtual Avanzado")
   print("⚡ Cargando componentes...")
   
   try:
       # Verificar dependencias críticas
       required_modules = ['speech_recognition', 'pyttsx3', 'customtkinter', 'psutil']
       missing_modules = []
       
       for module in required_modules:
           try:
               __import__(module)
           except ImportError:
               missing_modules.append(module)
       
       if missing_modules:
           print(f"❌ Módulos faltantes: {', '.join(missing_modules)}")
           print("📦 Instala con: pip install " + " ".join(missing_modules))
           return
       
       print("✅ Todos los módulos están disponibles")
       print("🚀 Iniciando interfaz gráfica...")
       
       # Crear y ejecutar la aplicación
       app = AsistenteEVA()
       
       # Parche para agregar los comandos adicionales
       app.procesar_comando_original = app.procesar_comando
       app.procesar_comando = lambda cmd: procesar_comando_extendido(app, cmd)
       
       print("✅ EVA listo para usar!")
       app.run()
       
   except Exception as e:
       print(f"❌ Error crítico: {e}")
       print("🔧 Intenta reinstalar las dependencias o contacta soporte")

if __name__ == "__main__":
   main()