#!/usr/bin/env python3
"""
Script de démarrage pour RetinoblastoGemma v6
Lance le serveur API et ouvre l'interface web
"""
import subprocess
import time
import webbrowser
import sys
import os
from pathlib import Path
import platform

def check_dependencies():
    """Vérifie les dépendances nécessaires"""
    print("🔍 Checking dependencies...")
    
    try:
        import fastapi
        import uvicorn
        print("✅ FastAPI available")
    except ImportError:
        print("❌ FastAPI not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn[standard]"])
    
    try:
        import websockets
        print("✅ WebSockets available")
    except ImportError:
        print("❌ WebSockets not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "websockets"])

def start_api_server():
    """Lance le serveur FastAPI sur le port 8001"""
    print("🚀 Starting RetinoblastoGemma API server...")
    print("📡 API will be available at: http://localhost:8001")
    print("📚 API docs will be available at: http://localhost:8001/docs")
    
    return subprocess.Popen([
        sys.executable, "-c", 
        """
import sys
sys.path.append('.')
from api_server import app
import uvicorn
uvicorn.run(app, host='0.0.0.0', port=8001)
"""
    ])

def start_web_interface():
    """Lance l'interface web (si développement local)"""
    web_dir = Path("web_interface")
    
    if not web_dir.exists():
        print("⚠️ Web interface directory not found")
        print("📥 Please download the Lovable project to 'web_interface/' folder")
        return None
    
    package_json = web_dir / "package.json"
    if not package_json.exists():
        print("⚠️ package.json not found in web_interface/")
        return None
    
    print("🌐 Starting development web server...")
    
    # Vérifier si npm est disponible
    try:
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ npm not found. Please install Node.js")
        return None
    
    # Installer les dépendances si nécessaire
    node_modules = web_dir / "node_modules"
    if not node_modules.exists():
        print("📦 Installing npm dependencies...")
        subprocess.run(["npm", "install"], cwd=web_dir, check=True)
    
    # Lancer le serveur de développement
    return subprocess.Popen([
        "npm", "run", "dev"
    ], cwd=web_dir)

def wait_for_server(url, max_wait=30):
    """Attend que le serveur soit prêt"""
    import requests
    
    for i in range(max_wait):
        try:
            response = requests.get(f"{url}/api/status", timeout=1)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
    return False

def main():
    print("🏥 RetinoblastoGemma v6 - Google Gemma Hackathon")
    print("=" * 60)
    print("🤖 AI-Powered Retinoblastoma Detection System")
    print("🔬 100% Local Processing with Gemma 3n")
    print("=" * 60)
    
    # Vérifier les dépendances
    check_dependencies()
    
    processes = []
    
    try:
        # Démarrer l'API
        api_process = start_api_server()
        processes.append(("API Server", api_process))
        
        print("⏳ Waiting for API server to start...")
        time.sleep(3)
        
        # Vérifier que l'API est prête
        if wait_for_server("http://localhost:8001", max_wait=10):
            print("✅ API server is ready!")
        else:
            print("⚠️ API server may not be ready yet")
        
        # Démarrer l'interface web
        web_process = start_web_interface()
        if web_process:
            processes.append(("Web Interface", web_process))
            time.sleep(3)
        
        # Ouvrir le navigateur
        print("\n🌐 Opening web interface...")
        
        # Déterminer l'URL à ouvrir
        web_url = "http://localhost:8080"  # Vite dev server par défaut
        if not web_process:
            web_url = "http://localhost:8001"  # API serveur seulement
        
        webbrowser.open(web_url)
        
        print("\n" + "=" * 60)
        print("✅ RetinoblastoGemma is running!")
        print(f"🌐 Web interface: {web_url}")
        print("📡 API server: http://localhost:8001")
        print("📚 API documentation: http://localhost:8001/docs")
        print("📊 WebSocket: ws://localhost:8001/ws/progress")
        print("=" * 60)
        print("\n💡 Usage Instructions:")
        print("1. Upload a medical eye image")
        print("2. Configure analysis settings")
        print("3. Click 'Analyze for Retinoblastoma'")
        print("4. View results and medical recommendations")
        print("5. Export medical reports if needed")
        print("\n🛑 Press Ctrl+C to stop all servers...")
        
        # Attendre que l'utilisateur arrête
        api_process.wait()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down RetinoblastoGemma...")
        
        # Arrêter tous les processus
        for name, process in processes:
            if process and process.poll() is None:
                print(f"📴 Stopping {name}...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
        
        print("✅ All servers stopped successfully")
        print("👋 Thank you for using RetinoblastoGemma!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        # Nettoyer les processus en cas d'erreur
        for name, process in processes:
            if process and process.poll() is None:
                process.terminate()

if __name__ == "__main__":
    main()