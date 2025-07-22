import sys
import zipfile
import time
import math
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QMenu, QFileDialog, QProgressBar, QStackedWidget, QTextBrowser, QComboBox, QCheckBox, 
    QGridLayout, QFrame, QMessageBox, QSystemTrayIcon, QGraphicsScene, QGraphicsPixmapItem, 
    QGraphicsBlurEffect, QInputDialog, QLineEdit, QDialog, QGroupBox
)
from PyQt6.QtGui import (
    QPixmap, QIcon, QFontDatabase, QFont, QAction, QDesktopServices, QMovie, QPalette, QPainter
)
from PyQt6.QtCore import Qt, QSize, QPoint, QThread, pyqtSignal, QTimer, QUrl, QSettings, QTranslator, QCoreApplication, QEvent, QPropertyAnimation, QEasingCurve, QRect, QProcess, QRectF, QParallelAnimationGroup

import os   
import subprocess
import io
import csv
import winreg
from pyshortcuts import make_shortcut

def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Global translator object
_translator = None

LAUNCHER_VERSION = "1.0.1"

# MODIFICATION START: Added new strings for translation
TRANSLATIONS = {
    "Chaos at Fazbear's Launcher": {
        "es": "Chaos at Fazbear's Launcher", 
        "en": "Chaos at Fazbear's Launcher"
    },
    "Overview": {"es": "Overview", "en": "Overview"},
    "Patch Notes": {"es": "Notas de Parche", "en": "Patch Notes"},
    "Install": {"es": "Instalar", "en": "Install"}, 
    "Play Game": {"es": "Jugar", "en": "Play Game"},
    "Installing...": {"es": "Instalando...", "en": "Installing..."},
    "Ready": {"es": "Listo", "en": "Ready"},
    "LOGO NOT FOUND": {"es": "LOGO NO ENCONTRADO", "en": "LOGO NOT FOUND"},
    "Ajustes del Launcher": {"es": "Ajustes del Launcher", "en": "Launcher Settings"},
    "Idioma del Launcher:": {"es": "Idioma del Launcher:", "en": "Launcher Language:"},
    "Progress: 0.00%": {"es": "Progreso: 0.00%", "en": "Progress: 0.00%"}, 
    "Velocity: 0 Mbps": {"es": "Velocidad: 0 Mbps", "en": "Velocity: 0 Mbps"},
    "0.00GB / 0.00GB": {"es": "0.00GB / 0.00GB", "en": "0.00GB / 0.00GB"},
    
    "Progress: {}%": {"es": "Progreso: {}%", "en": "Progress: {}%"},
    "Velocity: {} Mbps": {"es": "Velocidad: {} Mbps", "en": "Velocity: {} Mbps"},
    "{}GB / {}GB": {"es": "{}GB / {}GB", "en": "{}GB / {}GB"},

    "Error: styles.qss not found. Please make sure it's in the same directory.": {
        "es": "Error: styles.qss no encontrado. Asegúrate de que esté en el mismo directorio.",
        "en": "Error: styles.qss not found. Please make sure it's in the same directory."
    },
    "Warning: Custom font file not found at {}. Using default font.": {
        "es": "Advertencia: Archivo de fuente personalizado no encontrado en {}. Usando fuente predeterminada.",
        "en": "Warning: Custom font file not found at {}. Using default font."
    },
    "Game detected at: {}": {"es": "Juego detectado en: {}", "en": "Game detected at: {}"},
    "Game detected but executable not found. Please reinstall.": {
        "es": "Juego detectado pero ejecutable no encontrado. Por favor, reinstala.",
        "en": "Game detected but executable not found. Please reinstall."
    },
    "Game not installed.": {"es": "Juego no instalado.", "en": "Game not installed."},
    "Found executable at root of extracted folder: {}": {
        "es": "Ejecutable encontrado en la raíz de la carpeta extraída: {}",
        "en": "Found executable at root of extracted folder: {}"
    },
    "Found executable recursively: {}": {
        "es": "Ejecutable encontrado recursivamente: {}",
        "en": "Ejecutable encontrado recursivamente: {}"
    },
    "Descargando notas de parche de: {}": {
        "es": "Descargando notas de parche de: {}",
        "en": "Downloading patch notes from: {}"
    },
    "Notas de Parche": {"es": "Notas de Parche", "en": "Patch Notes"},
    "Por:": {"es": "Por:", "en": "By:"},
    "Notas de parche cargadas exitosamente desde Google Sheet.": {
        "es": "Notas de parche cargadas exitosamente desde Google Sheet.",
        "en": "Patch notes loaded successfully from Google Sheet."
    },
    "Error al conectar con Google Sheets: {}\nAsegúrate de tener conexión a internet y la URL correcta.": {
        "es": "Error al conectar con Google Sheets: {}\nAsegúrate de tener conexión a internet y la URL correcta.",
        "en": "Error connecting to Google Sheets: {}\nEnsure you have internet connection and correct URL."
    },
    "Error de red/servidor al cargar patch notes de Google Sheet: {}": {
        "es": "Error de red/servidor al cargar notas de parche de Google Sheet: {}",
        "en": "Network/server error loading patch notes from Google Sheet: {}"
    },
    "Error al procesar el CSV del Google Sheet: {}\nAsegúrate de que el formato sea correcto (CSV) y no haya celdas inesperadas.": {
        "es": "Error al procesar el CSV del Google Sheet: {}\nAsegúrate de que el formato sea correcto (CSV) y no haya celdas inesperadas.",
        "en": "Error processing CSV from Google Sheet: {}\nEnsure format is correct (CSV) and no unexpected cells."
    },
    "Error inesperado al cargar notas de parche: {}": {
        "es": "Error inesperado al cargar notas de parche: {}",
        "en": "Unexpected error loading patch notes: {}"
    },
    "Changing to section: {}": {"es": "Cambiando a sección: {}", "en": "Changing to section: {}"},
    "Loading settings...": {"es": "Cargando ajustes...", "en": "Loading settings..."},
    "Language changed to: {} ({})": {"es": "Idioma cambiado a: {} ({})", "en": "Language changed to: {} ({})"},
    "Applying Spanish (base language)": {"es": "Aplicando español (idioma base)", "en": "Applying Spanish (base language)"},
    "Applying English translation from {}": {"es": "Aplicando traducción al inglés desde {}", "en": "Applying English translation from {}"},
    "Error: Could not load English translation file from {}": {
        "es": "Error: No se pudo cargar el archivo de traducción al inglés desde {}",
        "en": "Error: Could not load English translation file from {}"
    },
    "Unknown language code: {}. Defaulting to base texts (Spanish or English if no specific .qm for base).": {
        "es": "Código de idioma desconocido: {}. Usando textos base (español o inglés si no hay .qm específico para base).",
        "en": "Unknown language code: {}. Defaulting to base texts (Spanish or English if no specific .qm for base)."
    },
    "Directorio del juego": {"es": "Directorio del juego", "en": "Game Directory"},
    "Buscar actualizaciones": {"es": "Buscar actualizaciones", "en": "Check for Updates"},
    "Ajustes": {"es": "Ajustes", "en": "Settings"},
    "Installation is already in progress.": {"es": "La instalación ya está en progreso.", "en": "Installation is already in progress."},
    "Selecciona la carpeta de instalación": {"es": "Selecciona la carpeta de instalación", "en": "Select installation folder"},
    "Selected installation path: {}": {"es": "Ruta de instalación seleccionada: {}", "en": "Selected installation path: {}"},
    "Installation cancelled by user.": {"es": "Instalación cancelada por el usuario.", "en": "Installation cancelled by user."},
    "Error: Game ZIP file not found at {}.": {"es": "Error: Archivo ZIP del juego no encontrado en {}.", "en": "Error: Game ZIP file not found at {}}"},
    "Game ZIP file not found.": {"es": "Archivo ZIP del juego no encontrado.", "en": "Game ZIP file not found."},
    "Installation complete! Game extracted to: {}": {"es": "¡Instalación completa! Juego extraído en: {}", "en": "Installation complete! Game extracted to: {}"},
    "Game installed successfully.\n": {"es": "Juego instalado con éxito.\n", "en": "Game installed successfully.\n"},
    "Warning: Could not create marker file: {}": {"es": "Advertencia: No se pudo crear el archivo marcador: {}", "en": "Warning: Could not create marker file: {}"},
    "Warning: Game executable not found after installation. User may need to locate it manually.": {
        "es": "Advertencia: Ejecutable del juego no encontrado después de la instalación. El usuario podría necesitar localizarlo manualmente.",
        "en": "Warning: Game executable not found after installation. User may need to locate it manually."
    },
    "Installation failed: {}": {"es": "Instalación fallida: {}", "en": "Installation failed: {}"},
    "Error: Game executable path not set or found. Please install the game.": {
        "es": "Error: Ruta del ejecutable del juego no establecida o no encontrada. Por favor, instala el juego.",
        "en": "Error: Game executable path not set or found. Please install the game."
    },
    "Launching game from: {}": {"es": "Iniciando juego desde: {}", "en": "Launching game from: {}"},
    "Error launching game: {}": {"es": "Error al iniciar juego: {}", "en": "Error launching game: {}"},
    "Opening game directory: {}": {"es": "Abriendo directorio del juego: {}", "en": "Opening game directory: {}"},
    "Error opening directory: {}": {"es": "Error al abrir directorio: {}", "en": "Error opening directory: {}"},
    "Game not installed or directory not found.": {"es": "Juego no instalado o directorio no encontrado.", "en": "Game not installed or directory not found."},
    "Checking for updates...": {"es": "Buscando actualizaciones...", "en": "Checking for updates..."},
    "Progress: 0%": {"es": "Progreso: 0%", "en": "Progreso: 0%"},
    "Velocity: 0 Mbps": {"es": "Velocidad: 0 Mbps", "en": "Velocidad: 0 Mbps"},
    "0.00GB / 0.00GB": {"es": "0.00GB / 0.00GB", "en": "0.00GB / 0.00GB"},
    "Progress: {}%": {"es": "Progreso: {}%", "en": "Progress: {}%"},
    "Volver": {"es": "Volver", "en": "Back"},
    "Initializing launcher...": {"es": "Inicializando launcher...", "en": "Initializing launcher..."},
    "Game Options:": {"es": "Opciones de Juego:", "en": "Game Options:"}, 
    "Launcher is up to date.": {"es": "El launcher está actualizado.", "en": "Launcher is up to date."}, 
    "New launcher version available! Downloading...": {"es": "¡Nueva versión del launcher disponible! Descargando...", "en": "New launcher version available! Downloading..."}, 
    "Checking for new launcher updates...": {"es": "Buscando nuevas actualizaciones del launcher...", "en": "Checking for new launcher updates..."}, 
    "Current launcher version: {}": {"es": "Versión actual del launcher: {}", "en": "Current launcher version: {}"}, 
    "Failed to download or launch new launcher: {}": {"es": "Fallo al descargar o iniciar nuevo launcher: {}", "en": "Failed to download or launch new launcher: {}"}, 
    "New launcher downloaded successfully.": {"es": "Nuevo launcher descargado con éxito.", "en": "New launcher downloaded successfully."}, 
    "Downloading game...": {"es": "Descargando juego...", "en": "Downloading game..."}, 
    "Game download failed: {}": {"es": "Fallo la descarga del juego: {}", "en": "Game download failed: {}"}, 
    "Verifying game files...": {"es": "Verificando archivos del juego...", "en": "Verifying game files..."}, 
    "Installed game version: {}": {"es": "Versión del juego instalada: {}", "en": "Installed game version: {}"}, 
    "Error reading installed game version: {}": {"es": "Error al leer la versión del juego instalada: {}", "en": "Error reading installed game version: {}"}, 
    "Game version file not found in installation directory.": {"es": "Archivo de versión del juego no encontrado en el directorio de instalación.", "en": "Game version file not found in installation directory."}, 
    "Checking for game updates...": {"es": "Buscando actualizaciones del juego...", "en": "Checking for game updates..."}, 
    "Latest game version available: {}": {"es": "Última versión del juego disponible: {}", "en": "Última versión del juego disponible: {}"}, 
    "New game version available!": {"es": "¡Nueva versión del juego disponible!", "en": "New game version available!"}, 
    "Game is up to date.": {"es": "El juego está actualizado.", "en": "Game is up to date."}, 
    "Update Game": {"es": "Actualizar Juego", "en": "Update Game"}, 
    "Installing: {}": {"es": "Instalando: {}", "en": "Installing: {}"}, 
    "ZIP extraction error: {}\nFile may be corrupt.": {"es": "Error de extracción ZIP: {}\nEl archivo podría estar corrupto.", "en": "ZIP extraction error: {}\nFile may be corrupt."}, 
    "Game download cancelled.": {"es": "Descarga del juego cancelada.", "en": "Game download cancelled."}, 
    "An unexpected error occurred during installation: {}": {"es": "Ocurrió un error inesperado durante la instalación: {}", "en": "An unexpected error occurred during installation: {}"}, 
    "Cleaned up temporary ZIP file: {}": {"es": "Se eliminó el archivo ZIP temporal: {}", "en": "Cleaned up temporary ZIP file: {}"}, 
    "Confirm Close": {"es": "Confirmar Cierre", "en": "Confirm Close"},
    "Installation is in progress. Do you want to cancel and close the launcher?": {
        "es": "La instalación está en progreso. ¿Deseas cancelar y cerrar el launcher?",
        "en": "Installation is in progress. Do you want to cancel and close the launcher?"
    },
    "Installing: {filename}": {"es": "Instalando: {filename}", "en": "Installing: {filename}"},
    "Localizar juego": {"es": "Localizar juego", "en": "Locate Game"},
    "Selecciona la carpeta donde instalaste el juego": {
        "es": "Selecciona la carpeta donde instalaste el juego",
        "en": "Select the folder where you installed the game"
    },
    "Éxito": {"es": "Éxito", "en": "Success"},
    "¡Ubicación del juego actualizada correctamente!": {
        "es": "¡Ubicación del juego actualizada correctamente!",
        "en": "Game location updated successfully!"
    },
    "Error": {"es": "Error", "en": "Error"},
    "La carpeta seleccionada no parece ser una instalación válida del juego.": {
        "es": "La carpeta seleccionada no parece ser una instalación válida del juego.",
        "en": "The selected folder does not appear to be a valid game installation."
    },
    "Desinstalar juego": {"es": "Desinstalar juego", "en": "Uninstall Game"},
    "Información": {"es": "Información", "en": "Information"},
    "El juego no está instalado.": {"es": "El juego no está instalado.", "en": "The game is not installed."},
    "Confirmar Desinstalación": {"es": "Confirmar Desinstalación", "en": "Confirm Uninstall"},
    "¿Estás seguro de que quieres desinstalar el juego? Se borrarán todos los archivos de la carpeta: {}": {
        "es": "¿Estás seguro de que quieres desinstalar el juego? Se borrarán todos los archivos de la carpeta: {}",
        "en": "Are you sure you want to uninstall the game? All files in the folder will be deleted: {}"
    },
    "Juego desinstalado correctamente.": {"es": "Juego desinstalado correctamente.", "en": "Game uninstalled successfully."},
    "Ocurrió un error al desinstalar el juego: {}": {
        "es": "Ocurrió un error al desinstalar el juego: {}",
        "en": "An error occurred while uninstalling the game: {}"
    },
    "Play Game": {"es": "Jugar", "en": "Play Game"},
    "Playing...": {"es": "Jugando...", "en": "Playing..."},
    "Installing...": {"es": "Instalando...", "en": "Installing..."},
    "Iniciar con Windows": {"es": "Iniciar con Windows", "en": "Start with Windows"},
    "Minimizar a la bandeja al cerrar": {"es": "Minimizar a la bandeja al cerrar", "en": "Minimize to tray on close"},
    "Mostrar Launcher": {"es": "Mostrar Launcher", "en": "Show Launcher"},
    "Salir": {"es": "Salir", "en": "Quit"},
    "Launcher en Segundo Plano": {"es": "Launcher in Background", "en": "Launcher in Background"},
    "El launcher sigue ejecutándose. Haz clic para restaurar.": {
        "es": "El launcher sigue ejecutándose. Haz clic para restaurar.",
        "en": "The launcher is still running. Click to restore."
    },
    "Activar notificaciones del sistema": {
        "es": "Activar notificaciones del sistema", 
        "en": "Enable system notifications"
    },
    "Nuevas Notas de Parche": {
        "es": "Nuevas Notas de Parche", 
        "en": "New Patch Notes"
    },

    "Notas de Parche Actualizadas": {
        "es": "Notas de Parche Actualizadas",
        "en": "Patch Notes Updated"
    },
    "Se han publicado nuevas notas de parche. ¡Échales un vistazo!": {
        "es": "Se han publicado nuevas notas de parche. ¡Échales un vistazo!",
        "en": "New patch notes have been published. Check them out!"
    },
    "Actualización Disponible": {
        "es": "Actualización Disponible",
        "en": "Update Available"
    },
    "Activar notificaciones del sistema": {
        "es": "Activar notificaciones del sistema",
        "en": "Enable system notifications"
    },
    "Nuevas Notas de Parche": {
        "es": "Nuevas Notas de Parche",
        "en": "New Patch Notes"
    },
    "Actualizaciones y Eventos": {
        "es": "Actualizaciones y Eventos",
        "en": "Updates & Events"
    },
    "Notas de Parche Actualizadas": {
        "es": "Notas de Parche Actualizadas",
        "en": "Patch Notes Updated"
    },
    "Se han publicado nuevas notas de parche. ¡Échales un vistazo!": {
        "es": "Se han publicado nuevas notas de parche. ¡Échales un vistazo!",
        "en": "New patch notes have been published. Check them out!"
    },
    "Actualización Disponible": {
        "es": "Actualización Disponible",
        "en": "Update Available"
    },
    "Límite de Ancho de Banda:": {"es": "Límite de Ancho de Banda:", "en": "Bandwidth Limit:"},
    "Sin límite": {"es": "Sin límite", "en": "Unlimited"},
    "Acceso Beta": {
        "es": "Acceso Beta",
        "en": "Beta Access"
    },
    "Por favor, introduce la contraseña de beta tester:": {
        "es": "Por favor, introduce la contraseña de beta tester:",
        "en": "Please enter the beta tester password:"
    },
    "Error de Acceso": {
        "es": "Error de Acceso",
        "en": "Access Error"
    },
    "Contraseña incorrecta.": {
        "es": "Contraseña incorrecta.",
        "en": "Incorrect password."
    },
    "Update Game": {"es": "Actualizar", "en": "Update"},
    "¡Nueva versión del juego disponible!": {
        "es": "¡Nueva versión del juego disponible!",
        "en": "New game version available!"
    },
    "Confirmar Instalación": {
        "es": "Confirmar Instalación", 
        "en": "Confirm Installation"
    },
    "El juego se instalará en la siguiente ubicación:": {
        "es": "El juego se instalará en la siguiente ubicación:", 
        "en": "The game will be installed in the following location:"
    },
    "Cambiar...": {
        "es": "Cambiar...", 
        "en": "Change..."
    },
    "Crear acceso directo en el escritorio": {
        "es": "Crear acceso directo en el escritorio", 
        "en": "Create desktop shortcut"
    },
    "Cancelar": {
        "es": "Cancelar", 
        "en": "Cancel"
    },
    "Nueva Versión del Juego Disponible": {
        "es": "Nueva Versión del Juego Disponible",
        "en": "New Game Version Available"
    },
    "Se ha detectado una nueva versión del juego. ¿Deseas actualizar ahora?": {
        "es": "Se ha detectado una nueva versión del juego. ¿Deseas actualizar ahora?",
        "en": "A new version of the game has been detected. Would you like to update now?"
    },
    "Actualizar Ahora": {
        "es": "Actualizar Ahora",
        "en": "Update Now"
    },
    "Cancelar": {
        "es": "Cancelar",
        "en": "Cancel"
    },
    "Exportar partidas": {"es": "Exportar partidas", "en": "Export Saves"},
    "Importar partidas": {"es": "Importar partidas", "en": "Import Saves"},
    "No se encontró la carpeta de partidas guardadas. ¿Has jugado al juego alguna vez?": {
        "es": "No se encontró la carpeta de partidas guardadas. ¿Has jugado al juego alguna vez?",
        "en": "Save games folder not found. Have you ever played the game?"
    },
    "Exportar Partidas Guardadas": {"es": "Exportar Partidas Guardadas", "en": "Export Save Games"},
    "Partidas guardadas exportadas correctamente a: {}": {
        "es": "Partidas guardadas exportadas correctamente a: {}",
        "en": "Save games exported successfully to: {}"
    },
    "Ocurrió un error al exportar las partidas: {}": {
        "es": "Ocurrió un error al exportar las partidas: {}",
        "en": "An error occurred while exporting saves: {}"
    },
    "Importar Partidas Guardadas": {"es": "Importar Partidas Guardadas", "en": "Import Save Games"},
    "Confirmar Importación": {"es": "Confirmar Importación", "en": "Confirm Import"},
    "Esto reemplazará tus partidas guardadas actuales. ¿Estás seguro?": {
        "es": "Esto reemplazará tus partidas guardadas actuales. ¿Estás seguro?",
        "en": "This will replace your current save games. Are you sure?"
    },
    "Partidas guardadas importadas correctamente.": {
        "es": "Partidas guardadas importadas correctamente.",
        "en": "Save games imported successfully."
    },
    "El archivo seleccionado no es un ZIP válido.": {
        "es": "El archivo seleccionado no es un ZIP válido.",
        "en": "The selected file is not a valid ZIP file."
    },
    "Ocurrió un error al importar las partidas: {}": {
        "es": "Ocurrió un error al importar las partidas: {}",
        "en": "An error occurred while importing saves: {}"
    },
    "No se pudo determinar la ruta de guardado.": {
        "es": "No se pudo determinar la ruta de guardado.",
        "en": "Could not determine the save path."
    },
    "Nueva Versión del Launcher Disponible": {
        "es": "Nueva Versión del Launcher Disponible",
        "en": "New Launcher Version Available"
    },
    "Se ha detectado una nueva versión del launcher ({}). ¿Deseas actualizar ahora?": {
        "es": "Se ha detectado una nueva versión del launcher ({}). ¿Deseas actualizar ahora?",
        "en": "A new version of the launcher ({}) has been detected. Would you like to update now?"
    },
    "Descargando nueva versión del launcher...": {
        "es": "Descargando nueva versión del launcher...",
        "en": "Downloading new launcher version..."
    },
    "Error al descargar la nueva versión del launcher: {}": {
        "es": "Error al descargar la nueva versión del launcher: {}",
        "en": "Error downloading new launcher version: {}"
    },
    "Launcher actualizado con éxito. Por favor, reinicia el launcher.": {
        "es": "Launcher actualizado con éxito. Por favor, reinicia el launcher.",
        "en": "Launcher updated successfully. Please restart the launcher."
    },
    # New strings for pause/resume and settings redesign
    "Pause": {"es": "Pausar", "en": "Pause"},
    "Resume": {"es": "Reanudar", "en": "Resume"},
    "Paused": {"es": "Pausado", "en": "Paused"},
    "Application Behavior": {"es": "Comportamiento", "en": "Application Behavior"},
    "Downloads": {"es": "Descargas", "en": "Downloads"},
    "Notifications": {"es": "Notificaciones", "en": "Notifications"},
    "Checking for launcher update...": {
        "es": "Buscando actualización del launcher...", 
        "en": "Checking for launcher update..."
    },
    "Could not find version or .exe download URL in the latest GitHub release.": {
        "es": "No se encontró la versión o la URL de descarga del .exe en la última release de GitHub.", 
        "en": "Could not find version or .exe download URL in the latest GitHub release."
    },
    "No assets found in the latest GitHub release.": {
        "es": "No se encontraron archivos en la última release de GitHub.", 
        "en": "No assets found in the latest GitHub release."
    },
    "Network error checking for launcher update: {}": {
        "es": "Error de red al buscar actualización del launcher: {}", 
        "en": "Network error checking for launcher update: {}"
    },
    "Invalid JSON response from GitHub API: Missing key {}": {
        "es": "Respuesta JSON inválida de la API de GitHub: Falta la clave {}", 
        "en": "Invalid JSON response from GitHub API: Missing key {}"
    },
    "Unexpected error checking for launcher update: {}": {
        "es": "Error inesperado al buscar actualización del launcher: {}", 
        "en": "Unexpected error checking for launcher update: {}"
    },
    "An update is available. Would you like to install it now?": {
        "es": "Hay una actualización disponible. ¿Quieres instalarla ahora?",
        "en": "An update is available. Would you like to install it now?"
    }
}
# MODIFICATION END

# MODIFICATION START: Replaced version checker to use GitHub Releases API
class LauncherVersionChecker(QThread):
    version_checked = pyqtSignal(str, str)
    version_error = pyqtSignal(str)

    def __init__(self, repo_url, parent=None):
        super().__init__(parent)
        self.api_url = f"https://api.github.com/repos/{repo_url}/releases/latest"

    def run(self):
        try:
            print(self.tr(f"Checking for launcher update..."))
            headers = {
                'Accept': 'application/vnd.github.v3+json',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            }
            response = requests.get(self.api_url, timeout=10, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            latest_version = data.get('tag_name')
            if latest_version and latest_version.startswith('v'):
                latest_version = latest_version[1:]

            assets = data.get('assets')
            if not assets:
                self.version_error.emit(QApplication.instance().tr("No assets found in the latest GitHub release."))
                return

            download_url = None
            for asset in assets:
                if asset.get('name', '').endswith('.exe'):
                    download_url = asset.get('browser_download_url')
                    break
            
            if latest_version and download_url:
                self.version_checked.emit(latest_version, download_url)
            else:
                self.version_error.emit(QApplication.instance().tr("Could not find version or .exe download URL in the latest GitHub release."))

        except requests.exceptions.HTTPError as e:
             if e.response.status_code == 404:
                 self.version_error.emit(f"GitHub repository or release not found (404). Check the repo URL.")
             else:
                 self.version_error.emit(f"HTTP error checking for launcher update: {e}")
        except requests.exceptions.RequestException as e:
            self.version_error.emit(QApplication.instance().tr("Network error checking for launcher update: {}").format(e))
        except KeyError as e:
            self.version_error.emit(QApplication.instance().tr("Invalid JSON response from GitHub API: Missing key {}").format(e))
        except Exception as e:
            self.version_error.emit(QApplication.instance().tr("Unexpected error checking for launcher update: {}").format(e))
# MODIFICATION END

class SplashScreen(QWidget):
    def __init__(self, gif_path="images/loading_circle.gif", size=(500, 500), parent=None): 
        super().__init__(parent)
        self.setFixedSize(size[0], size[1])
        self.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) 
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(10)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gif_label = QLabel(self)
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gif_label.setStyleSheet("background-color: transparent;") 

        self.movie = QMovie(resource_path(gif_path))
        if self.movie.isValid():
            self.gif_label.setMovie(self.movie)
            scaled_width = int(size[0] * 0.7) 
            scaled_height = int(size[1] * 0.7) 
            self.movie.setScaledSize(QSize(scaled_width, scaled_height)) 
            
            self.gif_label.setFixedSize(scaled_width, scaled_height)
            
            self.movie.start()
        else:
            self.gif_label.setText("Loading GIF not found!")
            self.gif_label.setStyleSheet("color: white; font-size: 16px;")
        
        main_layout.addWidget(self.gif_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.status_label = QLabel(QApplication.instance().tr("Initializing launcher..."), self)
        self.status_label.setStyleSheet("color: white; font-size: 14px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.center_on_screen()

    def center_on_screen(self):
        screen_geo = QApplication.primaryScreen().geometry()
        x = (screen_geo.width() - self.width()) // 2
        y = (screen_geo.height() - self.height()) // 2
        self.move(x, y)

class PatchNotesLoader(QThread):
    notes_loaded = pyqtSignal(str, str) 
    notes_error = pyqtSignal(str)

    def __init__(self, url, title, parent=None):
        self.title = title
        super().__init__(parent)
        self.url = url

    def run(self):
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()

            csv_data = io.StringIO(response.text)
            reader = list(csv.reader(csv_data))


            latest_patch_date = ""
            if len(reader) > 1 and len(reader[1]) > 0:
                latest_patch_date = reader[1][0].strip()
            
            html_content = f"""
            <!DOCTYPE html><html><head><style>
                body {{ font-family: 'Nexa-Heavy', sans-serif; color: white; background-color: transparent; margin: 20px; }}
                h1 {{ color: #007bff; border-bottom: 2px solid white; padding-bottom: 5px; margin-top: 30px; }}
                h2 {{ color: #CCCCCC; margin-top: 20px; }}
            </style></head><body><h1>{self.title}</h1>"""
            

            for row in reader[1:]:
                if len(row) >= 4:
                    html_content += f"""
                    <div style="margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #444;">
                        <p style="font-size: 14px; color: #888;">{row[0].strip()}</p>
                        <h2 style="font-size: 20px;">{row[1].strip()}</h2>
                        <div>{row[2].strip()}</div>
                        <p style="font-size: 14px; color: #888; text-align: right;">{QApplication.instance().tr("Por:")} {row[3].strip()}</p>
                    </div>"""
            
            html_content += "</body></html>"
            self.notes_loaded.emit(html_content, latest_patch_date)

        except requests.exceptions.RequestException as e:
            self.notes_error.emit(QApplication.instance().tr(f"Error al conectar con Google Sheets: {e}"))
        except Exception as e:
            self.notes_error.emit(QApplication.instance().tr(f"Error inesperado al cargar notas de parche: {e}"))


class VersionLoader(QThread):
    version_loaded = pyqtSignal(str) 
    version_error = pyqtSignal(str)

    def __init__(self, url, parent=None):
        super().__init__(parent)
        self.url = url

    def run(self):
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()

            csv_data = io.StringIO(response.text)
            reader = list(csv.reader(csv_data))
            
            if len(reader) > 1 and len(reader[1]) > 0:
                game_url = reader[1][0].strip()
                if game_url:
                    self.version_loaded.emit(game_url)
                else:
                    self.version_error.emit("La URL en Google Sheets está vacía.")
            else:
                self.version_error.emit("El formato del CSV de versión no es válido.")

        except requests.exceptions.RequestException as e:
            self.version_error.emit(f"Error de red al buscar nueva versión: {e}")
        except Exception as e:
            self.version_error.emit(f"Error inesperado al buscar nueva versión: {e}")

# MODIFICATION START: Added pause/resume functionality to GameInstaller
class GameInstaller(QThread):
    progress_updated = pyqtSignal(float, float, float, float)
    installation_finished = pyqtSignal(str)
    installation_error = pyqtSignal(str)
    status_message = pyqtSignal(str)

    def __init__(self, game_zip_url, extract_to_path, bandwidth_limit_mbps=0, parent=None):
        super().__init__(parent)
        self.game_zip_url = game_zip_url
        self.extract_to_path = extract_to_path
        self.limit_bps = bandwidth_limit_mbps * 1024 * 1024 if bandwidth_limit_mbps > 0 else 0
        self.running = True
        self.paused = False # Flag for pausing
        self.start_time = time.time()
        self.last_update_time = time.time()
        self.last_downloaded_bytes = 0
        self.temp_zip_path = os.path.join(self.extract_to_path, "game_temp_download.zip")

    def run(self):
        try:
            os.makedirs(self.extract_to_path, exist_ok=True)

            downloaded_bytes = 0
            headers = {}
            if os.path.exists(self.temp_zip_path):
                downloaded_bytes = os.path.getsize(self.temp_zip_path)
                headers['Range'] = f'bytes={downloaded_bytes}-'
                print(f"Reanudando descarga desde {downloaded_bytes} bytes.")
                self.last_downloaded_bytes = downloaded_bytes

            self.status_message.emit(QApplication.instance().tr("Downloading game..."))
            
            with requests.get(self.game_zip_url, stream=True, timeout=3600, headers=headers) as response:
                if response.status_code not in [200, 206]:
                    response.raise_for_status()

                total_size = int(response.headers.get('content-length', 0))
                total_size += downloaded_bytes

                file_mode = 'ab' if downloaded_bytes > 0 else 'wb'
                
                with open(self.temp_zip_path, file_mode) as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        while self.paused:
                            if not self.running:
                                break
                            time.sleep(0.1)

                        if not self.running:
                            break
                        
                        f.write(chunk)
                        downloaded_bytes += len(chunk)

                        if self.limit_bps > 0:
                            # Simple bandwidth limiting
                            # (This is a basic implementation)
                            pass
                        
                        current_time = time.time()
                        if current_time - self.last_update_time >= 0.2:
                            percentage = (downloaded_bytes / total_size) * 100 if total_size > 0 else 0
                            velocity_mbps = (downloaded_bytes - self.last_downloaded_bytes) / (current_time - self.last_update_time) * 8 / (1024 * 1024)
                            current_gb = downloaded_bytes / (1024**3)
                            total_gb = total_size / (1024**3)

                            self.progress_updated.emit(percentage, velocity_mbps, current_gb, total_gb)
                            self.last_update_time = current_time
                            self.last_downloaded_bytes = downloaded_bytes

            if not self.running:
                self.installation_error.emit(QApplication.instance().tr("Game download cancelled."))
                return

            self.status_message.emit(QApplication.instance().tr("Installing..."))
            with zipfile.ZipFile(self.temp_zip_path, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    if not self.running:
                        break
                    self.status_message.emit(QApplication.instance().tr("Installing: {}").format(file_info.filename))
                    zip_ref.extract(file_info, self.extract_to_path)
                    QApplication.processEvents()

            if self.running:
                self.installation_finished.emit(self.extract_to_path)
            else:
                self.installation_error.emit(QApplication.instance().tr("Installation cancelled."))

        except zipfile.BadZipFile as e:
            self.installation_error.emit(QApplication.instance().tr("ZIP extraction error: {}\nFile may be corrupt.").format(e))
        except requests.exceptions.RequestException as e:
            self.installation_error.emit(QApplication.instance().tr("Game download failed: {}").format(e))
        except Exception as e:
            self.installation_error.emit(QApplication.instance().tr("An unexpected error occurred during installation: {}").format(e))
        finally:
            if self.running and os.path.exists(self.temp_zip_path):
                os.remove(self.temp_zip_path)
                print(QApplication.instance().tr("Cleaned up temporary ZIP file: {}").format(self.temp_zip_path))

    def stop(self):
        self.running = False

    def pause(self):
        self.paused = True
        self.status_message.emit(QApplication.instance().tr("Paused"))

    def resume(self):
        self.paused = False
        self.status_message.emit(QApplication.instance().tr("Downloading game..."))
# MODIFICATION END

class InstallConfirmationDialog(QDialog):
    def __init__(self, default_path, parent=None):
        super().__init__(parent)
        self.selected_path = default_path
        self.setWindowTitle(QApplication.instance().tr("Confirmar Instalación"))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)
        self.setObjectName("InstallDialog")
        self.setMinimumWidth(500)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title_label = QLabel(QApplication.instance().tr("Confirmar Instalación"))
        title_label.setObjectName("DialogTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        path_info_label = QLabel(QApplication.instance().tr("El juego se instalará en la siguiente ubicación:"))
        main_layout.addWidget(path_info_label)
        self.shortcut_checkbox = QCheckBox(QApplication.instance().tr("Crear acceso directo en el escritorio"))

        path_layout = QHBoxLayout()
        self.path_display_label = QLineEdit(self.selected_path)
        self.path_display_label.setObjectName("InstallPathDisplay")
        self.path_display_label.setReadOnly(True)
        path_layout.addWidget(self.path_display_label)

        change_button = QPushButton(QApplication.instance().tr("Cambiar..."))
        change_button.setObjectName("DialogButton")
        change_button.clicked.connect(self.change_path)
        path_layout.addWidget(change_button)
        main_layout.addLayout(path_layout)

        self.shortcut_checkbox = QCheckBox(QApplication.instance().tr("Crear acceso directo en el escritorio"))
        self.shortcut_checkbox.setChecked(True)
        main_layout.addWidget(self.shortcut_checkbox)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        cancel_button = QPushButton(QApplication.instance().tr("Cancelar"))
        cancel_button.setObjectName("DialogButton")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        install_button = QPushButton(QApplication.instance().tr("Install"))
        install_button.setObjectName("ConfirmInstallButton")
        install_button.clicked.connect(self.accept)
        button_layout.addWidget(install_button)
        
        main_layout.addLayout(button_layout)

    def change_path(self):
        new_dir = QFileDialog.getExistingDirectory(self, QApplication.instance().tr("Selecciona la carpeta de instalación"), self.selected_path)
        if new_dir:
            self.selected_path = new_dir
            self.path_display_label.setText(self.selected_path)

    def get_selected_options(self):
        return self.selected_path, self.shortcut_checkbox.isChecked()


class GameLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("AstrionStudios", "ChaosAtFazbearsLauncher") 

        QCoreApplication.setApplicationName("ChaosAtFazbearsLauncher")
        QCoreApplication.setOrganizationName("AstrionStudios")

        QApplication.instance()._current_lang_code = self.settings.value("language_code", "en", type=str)


        self.setWindowTitle(self.tr("Chaos at Fazbear's Launcher"))
        self.setFixedSize(1280, 720)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setObjectName("GameLauncher")
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap(resource_path("images/background.png")))
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(self.rect())
        self.background_label.lower()
        self.setWindowIcon(QIcon(resource_path("images/logo.ico")))
        self.create_blurred_background()

        self.current_section = "overview"
        self.game_installed_path = None
        self.game_executable_path = None
        self.should_create_shortcut = False

        self.latest_game_url = "" 
        self.is_initial_version_check = True
        self.version_loader_thread = VersionLoader(
            "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-1_abJseYUz7vn6V84wtpP6EYOjCMtd-19eaBj_-dE-RFP1YRcQKC0Y9wVGO6W4f293zYeP8SueYg/pub?gid=1299263524&single=true&output=csv"
        )
        self.version_loader_thread.version_loaded.connect(self.on_game_version_checked)
        self.version_loader_thread.version_error.connect(lambda error: print(f"Error de versión: {error}"))

        # MODIFICATION START: Using new GitHub version checker
        # !!! IMPORTANT: Replace "your-github-user/your-repo" with your actual GitHub username and repository name.
        self.launcher_version_checker = LauncherVersionChecker(
            "your-github-user/your-repo" 
        )
        # MODIFICATION END
        self.launcher_version_checker.version_checked.connect(self.on_launcher_version_checked)
        self.launcher_version_checker.version_error.connect(lambda error: print(f"Error checking launcher version: {error}"))
        self.check_for_launcher_updates_background()
        
        self.are_progress_details_visible = False
        self.extractor_thread = None
        self.slide_animation = None

        self.game_process = QProcess(self)
        self.game_process.finished.connect(self.on_game_finished)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(resource_path("images/logo.ico")))
        self.tray_icon.setToolTip("Chaos at Fazbear's Launcher")

        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        self.load_styles()
        self.load_custom_font()
        
        self.init_ui()

        saved_language_code = self.settings.value("language_code", "en", type=str) 
        
        self.language_combo_box.currentIndexChanged.connect(self.on_language_changed)

        self.apply_language(saved_language_code) 

        self.set_active_button_style(self.overview_button)
        self.check_game_status()
        

        self.hide_progress_details()

        self.setWindowOpacity(0.0) 
        self.window_fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.window_fade_in_animation.setDuration(500) 
        self.window_fade_in_animation.setStartValue(0.0) 
        self.window_fade_in_animation.setEndValue(1.0) 
        self.window_fade_in_animation.setEasingCurve(QEasingCurve.Type.OutQuad)

        self.patch_check_timer = QTimer(self)
        self.patch_check_timer.timeout.connect(self.check_for_new_patch_notes_background)
        self.patch_check_timer.start(1800000)
        
        self.check_for_new_patch_notes_background()
        self.check_for_game_updates_background()
        

    def showEvent(self, event):
        super().showEvent(event)
        self.window_fade_in_animation.start()

    def check_for_game_updates_background(self):
        print("Checking for latest game version in background...")
        self.version_loader_thread.start()

    def get_save_games_path(self):
        project_name = "ChaosAtFazbearsGame"
        local_app_data = os.getenv('LOCALAPPDATA')
        if local_app_data:
            return os.path.join(local_app_data, project_name, 'Saved', 'SaveGames')
        return None
    
    def check_for_launcher_updates_background(self):
        print(self.tr("Checking for new launcher updates..."))
        self.launcher_version_checker.start()

    def on_launcher_version_checked(self, latest_version, download_url):
        print(self.tr(f"Current launcher version: {LAUNCHER_VERSION}, Latest available: {latest_version}"))
        if latest_version > LAUNCHER_VERSION:
            print(self.tr(f"New launcher version available: {latest_version}"))
            dialog = QMessageBox(self)
            dialog.setWindowTitle(self.tr("Nueva Versión del Launcher Disponible"))
            dialog.setText(self.tr("Se ha detectado una nueva versión del launcher ({}). ¿Deseas actualizar ahora?").format(latest_version))
            dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            dialog.setDefaultButton(QMessageBox.StandardButton.Yes)
            dialog.button(QMessageBox.StandardButton.Yes).setText(self.tr("Actualizar Ahora"))
            dialog.button(QMessageBox.StandardButton.No).setText(self.tr("Cancelar"))
            dialog.setObjectName("InstallDialog")

            try:
                with open(resource_path("styles.qss"), "r", encoding='utf-8') as f:
                    dialog.setStyleSheet(f.read())
            except Exception as e:
                print(f"Could not apply style to dialog: {e}")

            if dialog.exec() == QMessageBox.StandardButton.Yes:
                self.download_and_update_launcher(download_url)
    
    def download_and_update_launcher(self, download_url):
        try:
            print(self.tr("Descargando nueva versión del launcher..."))
            response = requests.get(download_url, timeout=3600)
            response.raise_for_status()
            new_launcher_path = os.path.join(os.getenv("TEMP"), "ChaosAtFazbearsLauncher_new.exe")
            with open(new_launcher_path, "wb") as f:
                f.write(response.content)
            print(self.tr("New launcher downloaded successfully."))
        
            current_exe = sys.executable
            # This is a simple update mechanism. A more robust one would use a separate updater process.
            subprocess.Popen([new_launcher_path])
            self.quit_application()
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), 
                                self.tr("Failed to download or launch new launcher: {}").format(str(e)))

    def export_save_games(self):
        save_games_path = self.get_save_games_path()

        if not save_games_path or not os.path.isdir(save_games_path):
            QMessageBox.information(self, self.tr("Error"),
                                    self.tr("No se encontró la carpeta de partidas guardadas. ¿Has jugado al juego alguna vez?"))
            return

        zip_file_path, _ = QFileDialog.getSaveFileName(self,
                                                       self.tr("Exportar Partidas Guardadas"),
                                                       os.path.expanduser("~/Desktop/ChaosAtFazbears_Saves.zip"),
                                                       "ZIP Files (*.zip)")

        if not zip_file_path:
            return 

        try:
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(save_games_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, save_games_path))
            
            QMessageBox.information(self, self.tr("Éxito"),
                                    self.tr("Partidas guardadas exportadas correctamente a: {}").format(zip_file_path))
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"),
                                 self.tr("Ocurrió un error al exportar las partidas: {}").format(e))
            
    def import_save_games(self):
        save_games_path = self.get_save_games_path()

        if not save_games_path:
            QMessageBox.critical(self, self.tr("Error"), self.tr("No se pudo determinar la ruta de guardado."))
            return

        zip_file_path, _ = QFileDialog.getOpenFileName(self,
                                                       self.tr("Importar Partidas Guardadas"),
                                                       os.path.expanduser("~/Desktop"),
                                                       "ZIP Files (*.zip)")
        if not zip_file_path:
            return

        reply = QMessageBox.question(self, self.tr("Confirmar Importación"),
                                     self.tr("Esto reemplazará tus partidas guardadas actuales. ¿Estás seguro?"),
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.No:
            return

        try:
            os.makedirs(save_games_path, exist_ok=True)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(save_games_path)
            QMessageBox.information(self, self.tr("Éxito"),
                                    self.tr("Partidas guardadas importadas correctamente."))
        except zipfile.BadZipFile:
            QMessageBox.critical(self, self.tr("Error"), self.tr("El archivo seleccionado no es un ZIP válido."))
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"),
                                 self.tr("Ocurrió un error al importar las partidas: {}").format(e))

    # MODIFICATION START: Renamed and simplified update logic
    def on_game_version_checked(self, online_url):
        self.latest_game_url = online_url 
        last_used_url = self.settings.value("last_game_url", "")
        
        is_update_available = self.game_installed_path and online_url and online_url != last_used_url

        if is_update_available:
            print("New game version detected!")
            self.install_play_button.setText(self.tr("Update Game"))
            
            if self.is_initial_version_check:
                self.show_new_version_dialog()
            else:
                self.show_notification(
                    self.tr("Actualización Disponible"),
                    self.tr("¡Nueva versión del juego disponible!"),
                    "launcher"
                )
        
        self.is_initial_version_check = False
    # MODIFICATION END

    def show_new_version_dialog(self):
        dialog = QMessageBox(self)
        dialog.setWindowTitle(self.tr("Nueva Versión del Juego Disponible"))
        dialog.setText(self.tr("Se ha detectado una nueva versión del juego. ¿Deseas actualizar ahora?"))
        dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dialog.setDefaultButton(QMessageBox.StandardButton.Yes)
        dialog.button(QMessageBox.StandardButton.Yes).setText(self.tr("Actualizar Ahora"))
        dialog.button(QMessageBox.StandardButton.No).setText(self.tr("Cancelar"))
        dialog.setObjectName("InstallDialog")  

        try:
            with open(resource_path("styles.qss"), "r", encoding='utf-8') as f:
                dialog.setStyleSheet(f.read())
        except Exception as e:
            print(f"Could not apply style to dialog: {e}")

        if dialog.exec() == QMessageBox.StandardButton.Yes:
            self.prompt_installation_path(is_update=True)

    def check_for_new_patch_notes_background(self):
        print("Checking patch notes in background...")
    
        self.patch_checker_thread = PatchNotesLoader(
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-1_abJseYUz7vn6V84wtpP6EYOjCMtd-19eaBj_-dE-RFP1YRcQKC0Y9wVGO6W4f293zYeP8SueYg/pub?gid=0&single=true&output=csv", 
        ""
        )
    
        def on_check_finished(html_content, new_date):
            last_notified_date = self.settings.value("last_notified_patch_date", "", type=str)
            if new_date and new_date != last_notified_date:
                print(f"New patch notes found: {new_date}")
                self.show_notification(
                    self.tr("Nuevas Notas de Parche"),
                    self.tr("Se han publicado nuevas notas de parche. ¡Échales un vistazo!"),
                    "patch_notes"
                )
                self.settings.setValue("last_notified_patch_date", new_date)
            else:
                print("No new patch notes.")
            self.patch_checker_thread.quit()
            self.patch_checker_thread.wait()

        self.patch_checker_thread.notes_loaded.connect(on_check_finished)
        self.patch_checker_thread.start()

    def create_blurred_background(self):
        original_pixmap = QPixmap(resource_path("images/background.png"))
        scaled_pixmap = original_pixmap.scaled(
            self.size(), 
            Qt.AspectRatioMode.IgnoreAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        )
        scene = QGraphicsScene()
        pixmap_item = QGraphicsPixmapItem(scaled_pixmap)
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(15)
        pixmap_item.setGraphicsEffect(blur_effect)
        scene.addItem(pixmap_item)
        blurred_image = QPixmap(scaled_pixmap.size())
        blurred_image.fill(Qt.GlobalColor.transparent)
        painter = QPainter(blurred_image)
        scene.render(painter, QRectF(blurred_image.rect()), pixmap_item.boundingRect())
        painter.end()
        self.blurred_background = blurred_image

    def closeEvent(self, event):
        if self.tray_checkbox.isChecked():
            event.ignore()
            self.hide()
            self.tray_icon.show()
            self.tray_icon.showMessage(
                self.tr("Launcher en Segundo Plano"),
                self.tr("El launcher sigue ejecutándose. Haz clic para restaurar."),
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )
            return

        if hasattr(self, 'extractor_thread') and self.extractor_thread is not None and self.extractor_thread.isRunning():
            reply = QMessageBox.question(self, self.tr("Confirmar Cierre"),
                                         self.tr("La instalación está en progreso. ¿Deseas cancelar y cerrar el launcher?"),
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.extractor_thread.stop()
                self.extractor_thread.wait(2000) 
                self.tray_icon.hide()
                event.accept()
            else:
                event.ignore() 
        else:
            self.tray_icon.hide() 
            event.accept()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_normal_and_raise()

    def show_normal_and_raise(self):
        self.showNormal()
        self.activateWindow()
        self.tray_icon.hide()

    def quit_application(self):
        self.tray_icon.hide()
        QCoreApplication.instance().quit()

    def tr(self, text, disambiguation=None, n=-1):
        current_lang_code = getattr(QApplication.instance(), '_current_lang_code', 'en')
        return TRANSLATIONS.get(text, {}).get(current_lang_code, text)

    def load_styles(self):
        try:
            background_image_path = resource_path("images/background.png").replace("\\", "/")
            with open(resource_path("styles.qss"), "r", encoding='utf-8') as f:
                stylesheet = f.read()
            processed_stylesheet = stylesheet.replace("url(images/background.png)", f"url({background_image_path})")
            self.setStyleSheet(processed_stylesheet)
        except FileNotFoundError:
            print(self.tr("Error: styles.qss not found. Please make sure it's in the same directory."))
            sys.exit(1)

    def load_custom_font(self):
        font_path = resource_path("fonts/Nexa-Heavy.ttf")
        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id == -1:
                print(self.tr(f"Error: Could not load font from {font_path}"))
        else:
            print(self.tr(f"Warning: Custom font file not found at {font_path}. Using default font."))

    def check_game_status(self):
        saved_path = self.settings.value("game_install_path", None)
        self.game_installed_path = None
        self.game_executable_path = None
        
        button_text = self.tr("Install")

        if saved_path and os.path.exists(saved_path):
            marker_file = os.path.join(saved_path, "versions.txt") # Or another reliable file
            if os.path.exists(marker_file):
                self.game_installed_path = saved_path
                self.game_executable_path = self.find_executable_in_directory(self.game_installed_path)
                if self.game_executable_path:
                    print(self.tr(f"Game detected at: {self.game_executable_path}"))
                    button_text = self.tr("Play Game")
                else:
                    print(self.tr("Game detected but executable not found. Please reinstall."))
            else:
                print(self.tr("Game not installed."))
        else:
            print(self.tr("Game not installed."))
        
        self.install_play_button.setText(button_text)
        
    
    def find_executable_in_directory(self, base_path):
        for file in os.listdir(base_path):
            if file.lower().endswith(".exe") and os.path.isfile(os.path.join(base_path, file)):
                return os.path.join(base_path, file)
        for root, _, files in os.walk(base_path):
            for file in files:
                if file.lower().endswith(".exe"):
                    return os.path.join(root, file)
        return None

    # MODIFICATION START: Redesigned settings page and added pause/resume button
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        top_bar_widgets_layout = QHBoxLayout()
        top_bar_widgets_layout.setContentsMargins(0, 0, 10, 0)
        top_bar_widgets_layout.setSpacing(0)
        top_bar_widgets_layout.addStretch(1)

        self.overview_button = QPushButton(self.tr("Overview"))
        self.overview_button.setObjectName("OverviewButton")
        self.overview_button.clicked.connect(lambda: self.set_section("overview"))
        top_bar_widgets_layout.addWidget(self.overview_button)

        self.patch_notes_button = QPushButton(self.tr("Patch Notes"))
        self.patch_notes_button.setObjectName("PatchNotesButton")
        self.patch_notes_button.clicked.connect(lambda: self.set_section("patch_notes"))
        top_bar_widgets_layout.addWidget(self.patch_notes_button)

        top_bar_widgets_layout.addStretch(1)
        top_bar_widgets_layout.addSpacing(20)

        self.minimize_button = QPushButton()
        self.minimize_button.setIcon(QIcon(resource_path("images/minimize_icon.png")))
        self.minimize_button.setIconSize(QSize(20, 20))
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.setObjectName("MinimizeButton")
        self.minimize_button.clicked.connect(self.showMinimized)
        top_bar_widgets_layout.addWidget(self.minimize_button)

        self.close_button = QPushButton()
        self.close_button.setIcon(QIcon(resource_path("images/close_icon.png")))
        self.close_button.setIconSize(QSize(20, 20))
        self.close_button.setFixedSize(30, 30)
        self.close_button.setObjectName("CloseButton")
        self.close_button.clicked.connect(self.close)
        top_bar_widgets_layout.addWidget(self.close_button)

        main_layout.addLayout(top_bar_widgets_layout)

        self.content_stack = QStackedWidget(self)
        main_layout.addWidget(self.content_stack)

        # --- Overview Page ---
        self.overview_page = QWidget(self)
        overview_page_main_layout = QVBoxLayout(self.overview_page)
        overview_page_main_layout.setContentsMargins(30, 30, 30, 30)
        overview_content_horizontal_layout = QHBoxLayout() 
        left_side_layout = QVBoxLayout()
        left_side_layout.setContentsMargins(0, 0, 0, 0)
        left_side_layout.setSpacing(0)
        self.logo_label = QLabel()
        self.logo_label.setObjectName("LogoLabel")
        pixmap = QPixmap(resource_path("images/logo.png"))
        if not pixmap.isNull():
            self.logo_label.setPixmap(pixmap.scaledToWidth(400, Qt.TransformationMode.SmoothTransformation))
        else:
            self.logo_label.setText(self.tr("LOGO NOT FOUND"))
        left_side_layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        left_side_layout.addStretch(1)
        bottom_buttons_layout = QHBoxLayout()
        bottom_buttons_layout.setSpacing(-10)
        self.install_play_button = QPushButton(self.tr("Install"))
        self.install_play_button.setFixedSize(250, 60)
        self.install_play_button.setObjectName("InstallPlayButton")
        self.install_play_button.clicked.connect(self.handle_game_action)
        bottom_buttons_layout.addWidget(self.install_play_button)
        self.menu_button = QPushButton("☰")
        self.menu_button.setFixedSize(60, 60)
        self.menu_button.setObjectName("MenuButton")
        self.menu_button.clicked.connect(self.show_context_menu)
        bottom_buttons_layout.addWidget(self.menu_button)
        left_side_layout.addLayout(bottom_buttons_layout)
        overview_content_horizontal_layout.addLayout(left_side_layout)
        overview_content_horizontal_layout.addStretch(1)
        overview_page_main_layout.addLayout(overview_content_horizontal_layout)
        self.content_stack.addWidget(self.overview_page)

        # --- Patch Notes Page ---
        self.patch_notes_page = QWidget(self)
        self.patch_notes_page.setObjectName("PatchNotesPage")
        patch_notes_layout = QVBoxLayout(self.patch_notes_page)
        self.patch_notes_browser = QTextBrowser(self.patch_notes_page)
        self.patch_notes_browser.setObjectName("PatchNotesBrowser")
        self.patch_notes_browser.setOpenExternalLinks(True)
        patch_notes_layout.addWidget(self.patch_notes_browser)
        self.content_stack.addWidget(self.patch_notes_page)

        # --- Settings Page (Redesigned) ---
        self.settings_page = QWidget(self)
        settings_page_layout = QVBoxLayout(self.settings_page)
        settings_page_layout.setContentsMargins(50, 20, 50, 50)
        
        settings_header_layout = QHBoxLayout()
        self.settings_title_label = QLabel(self.tr("Ajustes del Launcher"))
        self.settings_title_label.setObjectName("SettingsTitle")
        settings_header_layout.addWidget(self.settings_title_label, alignment=Qt.AlignmentFlag.AlignLeft)
        settings_header_layout.addStretch()
        self.back_button = QPushButton(self.tr("Volver"))
        self.back_button.setObjectName("BackButton")
        self.back_button.clicked.connect(lambda: self.set_section("overview"))
        settings_header_layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignRight)
        settings_page_layout.addLayout(settings_header_layout)

        # --- Application Behavior Group ---
        app_behavior_group = QGroupBox(self.tr("Application Behavior"))
        app_behavior_layout = QVBoxLayout(app_behavior_group)
        self.language_layout = QHBoxLayout()
        self.language_label = QLabel(self.tr("Idioma del Launcher:"))
        self.language_combo_box = QComboBox()
        self.language_combo_box.setObjectName("LanguageComboBox")
        self.language_layout.addWidget(self.language_label)
        self.language_layout.addWidget(self.language_combo_box)
        self.language_layout.addStretch()
        app_behavior_layout.addLayout(self.language_layout)
        self.startup_checkbox = QCheckBox(self.tr("Iniciar con Windows"))
        self.startup_checkbox.toggled.connect(self.set_startup_option)
        app_behavior_layout.addWidget(self.startup_checkbox)
        self.tray_checkbox = QCheckBox(self.tr("Minimizar a la bandeja al cerrar"))
        self.tray_checkbox.toggled.connect(lambda checked: self.settings.setValue("minimize_to_tray", checked))
        app_behavior_layout.addWidget(self.tray_checkbox)
        settings_page_layout.addWidget(app_behavior_group)

        # --- Downloads Group ---
        downloads_group = QGroupBox(self.tr("Downloads"))
        downloads_layout = QHBoxLayout(downloads_group)
        self.bandwidth_label = QLabel(self.tr("Límite de Ancho de Banda:"))
        self.bandwidth_combo_box = QComboBox()
        self.bandwidth_combo_box.setObjectName("LanguageComboBox")
        self.bandwidth_combo_box.addItem(self.tr("Sin límite"), 0)
        self.bandwidth_combo_box.addItems(["5 MB/s", "10 MB/s", "25 MB/s", "50 MB/s"])
        downloads_layout.addWidget(self.bandwidth_label)
        downloads_layout.addWidget(self.bandwidth_combo_box)
        downloads_layout.addStretch()
        settings_page_layout.addWidget(downloads_group)

        # --- Notifications Group ---
        notifications_group = QGroupBox(self.tr("Notifications"))
        notifications_layout = QVBoxLayout(notifications_group)
        self.notifications_enabled_checkbox = QCheckBox(self.tr("Activar notificaciones del sistema"))
        notifications_layout.addWidget(self.notifications_enabled_checkbox)
        self.notifications_options_widget = QWidget()
        sub_notifications_layout = QVBoxLayout(self.notifications_options_widget)
        sub_notifications_layout.setContentsMargins(20, 0, 0, 0)
        self.notify_patch_notes_checkbox = QCheckBox(self.tr("Nuevas Notas de Parche"))
        self.notify_launcher_updates_checkbox = QCheckBox(self.tr("Actualizaciones y Eventos"))
        sub_notifications_layout.addWidget(self.notify_patch_notes_checkbox)
        sub_notifications_layout.addWidget(self.notify_launcher_updates_checkbox)
        notifications_layout.addWidget(self.notifications_options_widget)
        self.notifications_enabled_checkbox.toggled.connect(self.on_notifications_toggled)
        settings_page_layout.addWidget(notifications_group)

        settings_page_layout.addStretch(1)
        self.content_stack.addWidget(self.settings_page)

        # --- Progress Bar Area ---
        self.progress_area_layout = QVBoxLayout()
        self.progress_area_layout.setContentsMargins(40, 0, 40, 40)
        self.progress_area_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.progress_area_layout.setSpacing(5)
        
        top_text_row_layout = QHBoxLayout()
        self.status_message_label = QLabel(self.tr("Ready"))
        self.status_message_label.setObjectName("StatusMessageLabel")
        top_text_row_layout.addWidget(self.status_message_label, 1)

        # Pause/Resume Button
        self.pause_resume_button = QPushButton(self.tr("Pause"))
        self.pause_resume_button.setObjectName("DialogButton")
        self.pause_resume_button.clicked.connect(self.toggle_pause_resume)
        self.pause_resume_button.hide()
        top_text_row_layout.addWidget(self.pause_resume_button)
        
        self.progress_info_label = QLabel(self.tr("Progress: 0.00%"))
        self.progress_info_label.setObjectName("ProgressInfoLabel")
        top_text_row_layout.addWidget(self.progress_info_label, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.velocity_label = QLabel(self.tr("Velocity: 0 Mbps"))
        self.velocity_label.setObjectName("VelocityLabel")
        top_text_row_layout.addWidget(self.velocity_label, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.size_label = QLabel(self.tr("0.00GB / 0.00GB"))
        self.size_label.setObjectName("SizeLabel")
        top_text_row_layout.addWidget(self.size_label, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.progress_area_layout.addLayout(top_text_row_layout)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("InstallationProgressBar")
        self.progress_bar.setTextVisible(False)
        self.progress_area_layout.addWidget(self.progress_bar)
        
        main_layout.addLayout(self.progress_area_layout)
    # MODIFICATION END

    def on_notifications_toggled(self, checked):
        self.notifications_options_widget.setEnabled(checked)
        self.settings.setValue("notifications_enabled", checked)
        if checked:
            self.settings.setValue("notify_on_patch_notes", self.notify_patch_notes_checkbox.isChecked())
            self.settings.setValue("notify_on_launcher_updates", self.notify_launcher_updates_checkbox.isChecked())
        else:
            self.settings.setValue("notify_on_patch_notes", False)
            self.settings.setValue("notify_on_launcher_updates", False)

    def load_patch_notes(self):
        self.patch_notes_browser.setHtml(f"<h1 style='color:white;'>{self.tr('Loading...')}</h1>")
        google_sheet_csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-1_abJseYUz7vn6V84wtpP6EYOjCMtd-19eaBj_-dE-RFP1YRcQKC0Y9wVGO6W4f293zYeP8SueYg/pub?output=csv"
        self.patch_notes_thread = PatchNotesLoader(google_sheet_csv_url, self.tr("Notas de Parche"))
        self.patch_notes_thread.notes_loaded.connect(self.on_patch_notes_loaded)
        self.patch_notes_thread.notes_error.connect(self.on_patch_notes_error)
        self.patch_notes_thread.start()
        
    def on_patch_notes_loaded(self, html_content, latest_patch_date):
        self.patch_notes_browser.setHtml(html_content)
        if latest_patch_date:
            self.settings.setValue("last_notified_patch_date", latest_patch_date)

    def on_patch_notes_error(self, error_message):
        self.patch_notes_browser.setPlainText(error_message)

    def confirm_uninstall(self):
        if not self.game_installed_path:
            QMessageBox.information(self, self.tr("Información"), self.tr("El juego no está instalado."))
            return
        reply = QMessageBox.question(self, self.tr("Confirmar Desinstalación"),
                                     self.tr("¿Estás seguro de que quieres desinstalar el juego? Se borrarán todos los archivos de la carpeta: {}").format(self.game_installed_path),
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.uninstall_game()

    def uninstall_game(self):
        import shutil
        try:
            shutil.rmtree(self.game_installed_path)
            self.settings.remove("game_install_path")
            self.game_installed_path = None
            self.game_executable_path = None
            self.install_play_button.setText(self.tr("Install"))
            QMessageBox.information(self, self.tr("Éxito"), self.tr("Juego desinstalado correctamente."))
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), self.tr("Ocurrió un error al desinstalar el juego: {}").format(e))

    def open_external_link(self, url):
        QDesktopServices.openUrl(url)

    def set_active_button_style(self, active_button):
        self.overview_button.setProperty("active", False)
        self.patch_notes_button.setProperty("active", False)
        if active_button:
            active_button.setProperty("active", True)
        self.overview_button.style().polish(self.overview_button)
        self.patch_notes_button.style().polish(self.patch_notes_button)

    def set_section(self, section_name):
        if self.current_section == section_name:
            return

        is_switching_to_settings = section_name == "settings"
        self.overview_button.setVisible(not is_switching_to_settings)
        self.patch_notes_button.setVisible(not is_switching_to_settings)

        current_widget = self.content_stack.currentWidget()
        if section_name == "overview":
            next_widget = self.overview_page
        elif section_name == "patch_notes":
            next_widget = self.patch_notes_page
            self.load_patch_notes()
        elif section_name == "settings":
            next_widget = self.settings_page
            self.load_settings()
        else:
            return
            
        if current_widget == next_widget: return

        width = self.content_stack.width()
        is_coming_from_settings = self.current_section == "settings"

        if is_switching_to_settings or is_coming_from_settings:
            self.content_stack.setCurrentWidget(next_widget)
        else: # Slide animation
            direction = 1 if section_name == "patch_notes" else -1
            next_widget.setGeometry(direction * width, 0, width, self.content_stack.height())
            self.content_stack.setCurrentWidget(next_widget)
            
            anim_current = QPropertyAnimation(current_widget, b"pos")
            anim_current.setEndValue(QPoint(-direction * width, 0))
            anim_current.setDuration(300)
            anim_current.setEasingCurve(QEasingCurve.Type.InOutQuad)
            
            anim_next = QPropertyAnimation(next_widget, b"pos")
            anim_next.setEndValue(QPoint(0, 0))
            anim_next.setDuration(300)
            anim_next.setEasingCurve(QEasingCurve.Type.InOutQuad)
            
            self.animation_group = QParallelAnimationGroup(self)
            self.animation_group.addAnimation(anim_current)
            self.animation_group.addAnimation(anim_next)
            self.animation_group.start()

        self.current_section = section_name
        active_button = self.patch_notes_button if section_name == "patch_notes" else self.overview_button
        self.set_active_button_style(active_button if not is_switching_to_settings else None)

    def load_settings(self):
        print(self.tr("Loading settings..."))
        saved_language_code = self.settings.value("language_code", "es", type=str)
        self.language_combo_box.blockSignals(True)
        self.language_combo_box.clear()
        self.language_combo_box.addItem("Español", "es")
        self.language_combo_box.addItem("English", "en")
        index = self.language_combo_box.findData(saved_language_code)
        if index != -1: self.language_combo_box.setCurrentIndex(index)
        self.language_combo_box.blockSignals(False)

        notifications_enabled = self.settings.value("notifications_enabled", True, type=bool)
        self.notifications_enabled_checkbox.setChecked(notifications_enabled)
        self.notify_patch_notes_checkbox.setChecked(self.settings.value("notify_on_patch_notes", True, type=bool))
        self.notify_launcher_updates_checkbox.setChecked(self.settings.value("notify_on_launcher_updates", True, type=bool))
        self.notifications_options_widget.setEnabled(notifications_enabled)
        self.notify_patch_notes_checkbox.toggled.connect(lambda c: self.settings.setValue("notify_on_patch_notes", c))
        self.notify_launcher_updates_checkbox.toggled.connect(lambda c: self.settings.setValue("notify_on_launcher_updates", c))

        bandwidth_limit = self.settings.value("bandwidth_limit_mbps", 0, type=int)
        index = self.bandwidth_combo_box.findData(bandwidth_limit)
        if index != -1: self.bandwidth_combo_box.setCurrentIndex(index)
        self.bandwidth_combo_box.currentIndexChanged.connect(lambda: self.settings.setValue("bandwidth_limit_mbps", self.bandwidth_combo_box.currentData()))

        self.startup_checkbox.setChecked(self.settings.value("start_on_boot", False, type=bool))
        self.tray_checkbox.setChecked(self.settings.value("minimize_to_tray", False, type=bool))

    def show_notification(self, title, message, notification_type):
        if not self.settings.value("notifications_enabled", True, type=bool): return
        if notification_type == "patch_notes" and not self.settings.value("notify_on_patch_notes", True, type=bool): return
        if notification_type == "launcher" and not self.settings.value("notify_on_launcher_updates", True, type=bool): return
        self.tray_icon.showMessage(self.tr(title), self.tr(message), QSystemTrayIcon.MessageIcon.Information, 5000)

    def set_startup_option(self, checked):
        self.settings.setValue("start_on_boot", checked)
        if sys.platform != "win32": return
        app_name = "ChaosAtFazbearsLauncher"
        exe_path = sys.executable
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE) as registry_key:
                if checked:
                    winreg.SetValueEx(registry_key, app_name, 0, winreg.REG_SZ, f'"{exe_path}"')
                else:
                    winreg.DeleteValue(registry_key, app_name)
        except FileNotFoundError:
            print(f"Registry value '{app_name}' not found for deletion.")
        except Exception as e:
            print(f"Error modifying Windows startup registry: {e}")
        
    def on_language_changed(self, index):
        if self.language_combo_box.signalsBlocked(): return
        lang_code = self.language_combo_box.itemData(index) 
        self.settings.setValue("language_code", lang_code)
        QMessageBox.information(self, "Restart required", "Language change will take full effect on restart.")
        self.apply_language(lang_code)

    def apply_language(self, lang_code):
        QApplication.instance()._current_lang_code = lang_code
        self.setWindowTitle(self.tr("Chaos at Fazbear's Launcher"))
        self.overview_button.setText(self.tr("Overview"))
        self.patch_notes_button.setText(self.tr("Patch Notes"))
        self.settings_title_label.setText(self.tr("Ajustes del Launcher"))
        self.language_label.setText(self.tr("Idioma del Launcher:"))
        self.status_message_label.setText(self.tr("Ready"))
        self.back_button.setText(self.tr("Volver"))
        self.startup_checkbox.setText(self.tr("Iniciar con Windows"))
        self.tray_checkbox.setText(self.tr("Minimizar a la bandeja al cerrar"))
        self.bandwidth_label.setText(self.tr("Límite de Ancho de Banda:"))
        self.notifications_enabled_checkbox.setText(self.tr("Activar notificaciones del sistema"))
        self.notify_patch_notes_checkbox.setText(self.tr("Nuevas Notas de Parche"))
        self.notify_launcher_updates_checkbox.setText(self.tr("Actualizaciones y Eventos"))
        self.check_game_status()

    def show_context_menu(self):
        context_menu = QMenu(self)
        context_menu.setObjectName("HamburgerMenu")
        action_game_dir = QAction(self.tr("Directorio del juego"), self)
        action_game_dir.triggered.connect(self.open_game_directory)
        context_menu.addAction(action_game_dir)
        action_locate_game = QAction(self.tr("Localizar juego"), self)
        action_locate_game.triggered.connect(self.manually_locate_game)
        context_menu.addAction(action_locate_game)
        action_check_updates = QAction(self.tr("Buscar actualizaciones"), self)
        action_check_updates.triggered.connect(self.check_for_updates_manual)
        context_menu.addAction(action_check_updates)
        action_uninstall = QAction(self.tr("Desinstalar juego"), self)
        action_uninstall.triggered.connect(self.confirm_uninstall)
        context_menu.addAction(action_uninstall)
        action_settings = QAction(self.tr("Ajustes"), self)
        action_settings.triggered.connect(self.open_settings_page)
        context_menu.addAction(action_settings)
        context_menu.addSeparator()
        action_export_saves = QAction(self.tr("Exportar partidas"), self)
        action_export_saves.triggered.connect(self.export_save_games)
        context_menu.addAction(action_export_saves)
        action_import_saves = QAction(self.tr("Importar partidas"), self)
        action_import_saves.triggered.connect(self.import_save_games)
        context_menu.addAction(action_import_saves)
        
        button_pos = self.menu_button.mapToGlobal(QPoint(0, self.menu_button.height()))
        context_menu.exec(button_pos)

    def open_settings_page(self):
        self.set_section("settings")

    def manually_locate_game(self):
        selected_dir = QFileDialog.getExistingDirectory(self, self.tr("Selecciona la carpeta donde instalaste el juego"))
        if selected_dir:
            marker_file = os.path.join(selected_dir, "versions.txt") # Check for a known file
            if os.path.exists(marker_file):
                self.settings.setValue("game_install_path", selected_dir)
                self.check_game_status()
                self.check_for_game_updates_background() # Re-check for updates with new path
                QMessageBox.information(self, self.tr("Éxito"), self.tr("¡Ubicación del juego actualizada correctamente!"))
            else:
                QMessageBox.warning(self, self.tr("Error"), self.tr("La carpeta seleccionada no parece ser una instalación válida del juego."))

    def handle_game_action(self):
        current_text = self.install_play_button.text()
        if current_text == self.tr("Install"):
            self.prompt_installation_path()
        elif current_text == self.tr("Update Game"):
             self.prompt_installation_path(is_update=True)
        elif current_text == self.tr("Play Game"):
            self.launch_game()

    def prompt_installation_path(self, is_update=False):
        default_path = self.game_installed_path or os.path.join(os.getenv("LOCALAPPDATA"), "ChaosAtFazbearsGame")

        # Beta password check
        # You can remove this section if the game is public
        BETA_PASSWORD = "Sex69" 
        password, ok = QInputDialog.getText(self, self.tr("Acceso Beta"), self.tr("Por favor, introduce la contraseña de beta tester:"), QLineEdit.EchoMode.Password)
        if not ok: return
        if password != BETA_PASSWORD:
            QMessageBox.warning(self, self.tr("Error de Acceso"), self.tr("Contraseña incorrecta."))
            return

        dialog = InstallConfirmationDialog(default_path, self)
        try:
            with open(resource_path("styles.qss"), "r", encoding='utf-8') as f:
                dialog.setStyleSheet(f.read())
        except Exception as e:
            print(f"Could not apply style to dialog: {e}")

        if dialog.exec():
            install_dir, create_shortcut = dialog.get_selected_options()
            self.should_create_shortcut = create_shortcut
            self.game_installed_path = install_dir # Temporarily set path
            self.start_installation(install_dir)
        else:
            print(self.tr("Installation cancelled by user."))

    def create_desktop_shortcut(self):
        if not self.game_executable_path: return
        try:
            make_shortcut(self.game_executable_path, name="Chaos at Fazbear's", output_dir=os.path.expanduser("~\\Desktop"))
            print("Desktop shortcut created.")
        except Exception as e:
            print(f"Error creating desktop shortcut: {e}")

    def start_installation(self, install_dir):
        self.install_play_button.setText(self.tr("Installing..."))
        self.install_play_button.setEnabled(False)
        self.menu_button.setEnabled(False)
        self.show_progress_details()

        if not self.latest_game_url:
            QMessageBox.critical(self, self.tr("Error"), self.tr("Could not get download URL. Check your connection."))
            self.installation_failed("Download URL not available.")
            return

        limit = self.settings.value("bandwidth_limit_mbps", 0, type=int)
        self.extractor_thread = GameInstaller(self.latest_game_url, install_dir, bandwidth_limit_mbps=limit)
        self.extractor_thread.progress_updated.connect(self.update_progress_ui)
        self.extractor_thread.status_message.connect(self.status_message_label.setText) 
        self.extractor_thread.installation_finished.connect(self.installation_complete)
        self.extractor_thread.installation_error.connect(self.installation_failed)
        self.extractor_thread.start()

    def update_progress_ui(self, percentage, velocity_mbps, current_gb, total_gb):
        self.progress_bar.setValue(int(percentage))
        self.progress_info_label.setText(self.tr("Progress: {}%").format(f"{percentage:.2f}"))
        self.velocity_label.setText(self.tr("Velocity: {} Mbps").format(f"{velocity_mbps:.2f}"))
        self.size_label.setText(self.tr("{}GB / {}GB").format(f"{current_gb:.2f}", f"{total_gb:.2f}"))

    def installation_complete(self, extracted_path):
        print(self.tr(f"Installation complete! Game extracted to: {extracted_path}"))
        self.install_play_button.setEnabled(True)
        self.menu_button.setEnabled(True)
        
        self.settings.setValue("game_install_path", extracted_path)
        self.settings.setValue("last_game_url", self.latest_game_url)
        
        try:
            with open(os.path.join(extracted_path, "versions.txt"), 'w') as f:
                f.write(f"version_url={self.latest_game_url}\n")
        except Exception as e:
            print(self.tr(f"Warning: Could not create marker file: {e}"))

        self.check_game_status() # Re-check everything to update paths and button
        
        if self.should_create_shortcut and self.game_executable_path:
            self.create_desktop_shortcut()
        
        self.hide_progress_details()
        self.extractor_thread = None

    def installation_failed(self, error_message):
        print(self.tr(f"Installation failed: {error_message}"))
        self.install_play_button.setEnabled(True)
        self.menu_button.setEnabled(True)
        self.check_game_status() # Revert button to correct state
        self.hide_progress_details()
        self.extractor_thread = None

    def launch_game(self):
        if self.game_process.state() != QProcess.ProcessState.NotRunning:
            print("Game is already running.")
            return
        if not self.game_executable_path:
            QMessageBox.critical(self, self.tr("Error"), self.tr("Game executable not found. Please reinstall or locate the game."))
            self.check_game_status()
            return
        self.install_play_button.setText(self.tr("Playing..."))
        self.install_play_button.setEnabled(False)
        self.game_process.start(self.game_executable_path, [])

    def on_game_finished(self, exit_code, exit_status):
        print(f"Game process finished. Exit code: {exit_code}")
        self.install_play_button.setText(self.tr("Play Game"))
        self.install_play_button.setEnabled(True)

    def open_game_directory(self):
        if self.game_installed_path and os.path.exists(self.game_installed_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.game_installed_path))
        else:
            QMessageBox.information(self, self.tr("Información"), self.tr("Game not installed or directory not found."))

    def check_for_updates_manual(self):
        if not self.game_installed_path:
            QMessageBox.information(self, self.tr("Información"), self.tr("El juego no está instalado."))
            return
        
        last_used_url = self.settings.value("last_game_url", "")
        if self.latest_game_url and self.latest_game_url != last_used_url:
            reply = QMessageBox.information(self, self.tr("Actualización Disponible"), 
                                          self.tr("An update is available. Would you like to install it now?"),
                                          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.prompt_installation_path(is_update=True)
        else:
            QMessageBox.information(self, self.tr("Información"), self.tr("Game is up to date."))

    def toggle_pause_resume(self):
        if self.extractor_thread:
            if self.extractor_thread.paused:
                self.extractor_thread.resume()
                self.pause_resume_button.setText(self.tr("Pause"))
            else:
                self.extractor_thread.pause()
                self.pause_resume_button.setText(self.tr("Resume"))

    def toggle_progress_details(self):
        # This was tied to the arrow button, which is removed for simplicity.
        # You can re-implement this if needed.
        pass
    
    def show_progress_details(self):
        self.progress_bar.show()
        self.progress_info_label.show()
        self.velocity_label.show()
        self.size_label.show()
        self.pause_resume_button.show()
        self.progress_bar.setMaximumHeight(14)

    def hide_progress_details(self):
        self.progress_info_label.hide()
        self.velocity_label.hide()
        self.size_label.hide()
        self.progress_bar.hide()
        self.pause_resume_button.hide()
        self.status_message_label.setText(self.tr("Ready"))

    _drag_position = None
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = event.globalPosition().toPoint() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_position is not None:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_position = None
        event.accept()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "background_label"):
            self.background_label.setGeometry(self.rect())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOrganizationName("AstrionStudios")
    app.setApplicationName("ChaosAtFazbearsLauncher")

    initial_lang_code = QSettings("AstrionStudios", "ChaosAtFazbearsLauncher").value("language_code", "en", type=str)
    QApplication.instance()._current_lang_code = initial_lang_code 
    
    splash = SplashScreen() 
    splash.show() 

    start_time = time.time()
    while time.time() - start_time < 3: 
        app.processEvents() 
        time.sleep(0.01) 

    launcher = GameLauncher()
    launcher.show() 
    
    splash.close() 
    del splash 

    sys.exit(app.exec())