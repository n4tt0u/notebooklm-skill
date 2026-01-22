"""
Configuration for NotebookLM Skill
Centralizes constants, selectors, paths, and utility functions
"""

from pathlib import Path

# =============================================================================
# Paths
# =============================================================================
SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
BROWSER_STATE_DIR = DATA_DIR / "browser_state"
BROWSER_PROFILE_DIR = BROWSER_STATE_DIR / "browser_profile"
STATE_FILE = BROWSER_STATE_DIR / "state.json"
AUTH_INFO_FILE = DATA_DIR / "auth_info.json"
LIBRARY_FILE = DATA_DIR / "library.json"

# =============================================================================
# NotebookLM Selectors
# =============================================================================
QUERY_INPUT_SELECTORS = [
    "textarea.query-box-input",  # Primary
    'textarea[aria-label="Feld für Anfragen"]',  # Fallback German
    'textarea[aria-label="Input for queries"]',  # Fallback English
]

RESPONSE_SELECTORS = [
    ".to-user-container .message-text-content",  # Primary
    "[data-message-author='bot']",
    "[data-message-author='assistant']",
]

# =============================================================================
# Browser Configuration
# =============================================================================
BROWSER_ARGS = [
    '--disable-blink-features=AutomationControlled',  # Patches navigator.webdriver
    '--disable-dev-shm-usage',
    '--no-sandbox',
    '--no-first-run',
    '--no-default-browser-check'
]

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# =============================================================================
# Timeouts
# =============================================================================
LOGIN_TIMEOUT_MINUTES = 10
QUERY_TIMEOUT_SECONDS = 120
PAGE_LOAD_TIMEOUT = 30000

# =============================================================================
# Prompts
# =============================================================================
# Follow-up reminder for Claude to encourage comprehensive questions
FOLLOW_UP_REMINDER = (
    "\n\nEXTREMELY IMPORTANT: Is that ALL you need to know? "
    "You can always ask another question! Think about it carefully: "
    "before you reply to the user, review their original request and this answer. "
    "If anything is still unclear or missing, ask me another comprehensive question "
    "that includes all necessary context (since each question opens a new browser session)."
)

# =============================================================================
# Utility Functions
# =============================================================================
def print_error(message: str) -> None:
    """Print an error message with emoji prefix"""
    print(f"❌ {message}")


def print_success(message: str) -> None:
    """Print a success message with emoji prefix"""
    print(f"✅ {message}")


def print_warning(message: str) -> None:
    """Print a warning message with emoji prefix"""
    print(f"⚠️ {message}")


def print_info(message: str) -> None:
    """Print an info message with emoji prefix"""
    print(f"ℹ️ {message}")
