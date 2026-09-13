"""
One-click Runner for VoiceShield-AI (SIH26104)
Generates test samples, initializes database, and starts FastAPI on http://127.0.0.1:8000
"""

import os
import sys
import subprocess
import webbrowser
import time

def main():
    print("=" * 65)
    print("🛡️  VOICESHIELD-AI — Real-Time Voice Cloning Defense System")
    print("    SIH26104 | AICTE Cyber Security Cell")
    print("=" * 65)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Generate test samples if not already generated
    print("\n[1/3] Generating demo benchmark audio samples...")
    subprocess.run([sys.executable, os.path.join(base_dir, "backend", "generate_samples.py")])

    # 2. Run automated test suite to ensure green health
    print("\n[2/3] Running AI Engine & Blockchain Verification tests...")
    test_proc = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=base_dir)
    if test_proc.returncode != 0:
        print("⚠️ Warning: Some unit tests failed, but starting server...")

    # 3. Start Uvicorn Server
    print("\n[3/3] Starting VoiceShield-AI FastAPI Server on http://127.0.0.1:8000 ...")
    print(">>> Open your browser at: http://127.0.0.1:8000")
    print(">>> Press CTRL + C to stop the server.\n")

    # Launch browser after a brief delay
    def open_browser():
        time.sleep(1.5)
        webbrowser.open("http://127.0.0.1:8000")

    import threading
    threading.Thread(target=open_browser, daemon=True).start()

    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
