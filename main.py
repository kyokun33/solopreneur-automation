import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_GEN_DIR = os.path.join(BASE_DIR, "report_generator")

if REPORT_GEN_DIR not in sys.path:
    sys.path.insert(0, REPORT_GEN_DIR)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from report_generator.main import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8090))
    uvicorn.run(app, host="0.0.0.0", port=port)
