import os
import tempfile

APP_NAME = "HugoAura"
TARGET_PROCESS_NAME = "SeewoServiceAssistant.exe"
GITHUB_OWNER = "HugoAura"
GITHUB_REPO = "Seewo-HugoAura"
GITHUB_DL_REPO = "HugoAura-Resources"
ASAR_FILENAME = "app-patched.asar"
ZIP_FILENAME = "aura.zip"
TARGET_ASAR_NAME = "app.asar"
EXTRACTED_FOLDER_NAME = "aura"

BASE_DOWNLOAD_URL = f"https://gcore.jsdelivr.net/gh/{GITHUB_OWNER}/{GITHUB_DL_REPO}"
GITHUB_API_URL = (
    f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
)

SWASS_PATH_PATTERN = r"C:\Program Files (x86)\Seewo\SeewoService\SeewoService_*\SeewoServiceAssistant\resources"
TEMP_DIR_NAME = "Aura-Install-Temp"
TEMP_INSTALL_DIR = os.path.join(tempfile.gettempdir(), TEMP_DIR_NAME)

PROCESS_KILL_INTERVAL_SECONDS = 0.5
