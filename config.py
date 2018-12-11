import os
DB_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/LaTeXCLI")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
TICKING_ACCURARCY = 0.05
TASK_TIMEOUT = 30
WORKPLACE_DIR = os.path.join(os.path.split(os.path.realpath(__file__))[0], "workplace")
SESSION_LENGTH = 32
FILE_STORAGE_TIME = 3600
