import logging
import os
import sys

# Ensure stdout and stderr use UTF-8 in-place with error replacement on Windows
# so unicode characters/emojis from third-party libraries (e.g. Phoenix, OpenTelemetry) never raise UnicodeEncodeError
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

# Create logs directory if needed
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "rag_application.log")

# Setup logging handlers
stream_handler = logging.StreamHandler(sys.stdout)
file_handler_rel = logging.FileHandler("rag_application.log", encoding="utf-8", errors="replace")
file_handler_abs = logging.FileHandler(log_file, encoding="utf-8", errors="replace")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[
        stream_handler,
        file_handler_rel,
        file_handler_abs,
    ],
)

logger = logging.getLogger("rag_application")
