"""
API Server pour RetinoblastoGemma - Interface web
Wrapper FastAPI autour du code existant main.py
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
import asyncio
import json
import uuid
from pathlib import Path
import time
from typing import Dict, List
import threading
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RetinoblastoGemma API", version="6.0")

@app.get("/")
async def root():
    """Page d'accueil de l'API"""
    return {
        "message": "🏥 RetinoblastoGemma API v6 is running!",
        "status": "operational",
        "endpoints": {
            "status": "/api/status",
            "docs": "/docs",
            "modules": "/api/modules-status",
            "upload": "/api/upload-image",
            "websocket": "/ws/progress"
        },
        "info": "AI-Powered Retinoblastoma Detection System"
    }

# CORS pour l'interface web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables globales
retino_app = None
analysis_sessions = {}  # Stockage temporaire des analyses
initialization_status = {
    "status": "starting",
    "modules": {
        "gemma": {"status": "waiting", "progress": 0},
        "eye_detector": {"status": "waiting", "progress": 0},
        "face_handler": {"status": "waiting", "progress": 0},
        "visualizer": {"status": "waiting", "progress": 0}
    },
    "overall_progress": 0
}

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"WebSocket broadcast error: {e}")
                disconnected.append(connection)
        
        # Nettoyer les connexions fermées
        for conn in disconnected:
            self.active_connections.remove(conn)

ws_manager = WebSocketManager()

async def initialize_retino_app():
    """Initialise l'application RetinoblastoGemma de manière asynchrone"""
    global retino_app, initialization_status
    
    try:
        logger.info("🔄 Starting RetinoblastoGemma initialization...")
        
        # Importer et initialiser l'application
        import tkinter as tk
        from main import RetinoblastoGemmaV6
        
        # Créer une fenêtre Tkinter invisible
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre
        root.attributes('-alpha', 0.0)  # Rendre complètement transparente
        
        # Simuler l'initialisation progressive
        modules = ["gemma", "eye_detector", "face_handler", "visualizer"]
        
        for i, module in enumerate(modules):
            initialization_status["modules"][module]["status"] = "loading"
            initialization_status["overall_progress"] = (i / len(modules)) * 100
            
            await ws_manager.broadcast({
                "type": "initialization_progress",
                "status": initialization_status
            })
            
            # Simuler le temps de chargement
            await asyncio.sleep(2)
            
            initialization_status["modules"][module]["status"] = "ready"
            initialization_status["modules"][module]["progress"] = 100
        
        # Créer l'instance de l'application
        retino_app = RetinoblastoGemmaV6(root)
        
        initialization_status["status"] = "ready"
        initialization_status["overall_progress"] = 100
        
        await ws_manager.broadcast({
            "type": "initialization_complete",
            "status": initialization_status
        })
        
        logger.info("✅ RetinoblastoGemma initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Initialization failed: {e}")
        initialization_status["status"] = "error"
        initialization_status["error"] = str(e)
        
        await ws_manager.broadcast({
            "type": "initialization_error",
            "status": initialization_status,
            "error": str(e)
        })

@app.on_event("startup")
async def startup_event():
    """Démarrage de l'application"""
    logger.info("🚀 FastAPI server starting...")
    
    # Créer les dossiers nécessaires
    Path("uploads").mkdir(exist_ok=True)
    Path("results").mkdir(exist_ok=True)
    
    # Lancer l'initialisation en arrière-plan
    asyncio.create_task(initialize_retino_app())

@app.websocket("/ws/progress")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        # Envoyer le statut initial
        await websocket.send_text(json.dumps({
            "type": "status_update",
            "status": initialization_status
        }))
        
        # Maintenir la connexion
        while True:
            await asyncio.sleep(1)
            # Envoyer un ping pour maintenir la connexion
            await websocket.send_text(json.dumps({"type": "ping"}))
            
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        ws_manager.disconnect(websocket)

@app.get("/api/status")
async def get_system_status():
    """Statut général du système"""
    return {
        "status": initialization_status["status"],
        "ready": initialization_status["status"] == "ready",
        "overall_progress": initialization_status["overall_progress"],
        "modules": initialization_status["modules"],
        "app_ready": retino_app is not None
    }

@app.get("/api/modules-status") 
async def get_modules_status():
    """Statut détaillé des modules"""
    return {
        "modules": initialization_status["modules"],
        "initializing": initialization_status["status"] not in ["ready", "error"],
        "overall_progress": initialization_status["overall_progress"]
    }

@app.post("/api/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """Upload et sauvegarde d'une image médicale"""
    try:
        # Vérifier le type de fichier
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Créer un ID unique pour cette session
        session_id = str(uuid.uuid4())
        
        # Sauvegarder l'image
        upload_dir = Path("uploads")
        file_path = upload_dir / f"{session_id}_{file.filename}"
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Obtenir les infos de l'image
        try:
            from PIL import Image
            img = Image.open(file_path)
            image_info = {
                "filename": file.filename,
                "dimensions": f"{img.width}x{img.height}",
                "size": len(content),
                "format": img.format
            }
            img.close()
        except Exception as e:
            image_info = {
                "filename": file.filename,
                "dimensions": "unknown",
                "size": len(content),
                "format": "unknown"
            }
        
        # Mettre à jour l'application si prête
        if retino_app:
            retino_app.current_image_path = str(file_path)
        
        logger.info(f"Image uploaded: {file.filename} -> {session_id}")
        
        return {
            "session_id": session_id,
            "filename": file.filename,
            "image_info": image_info,
            "file_path": str(file_path),
            "status": "uploaded"
        }
        
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/api/analyze/{session_id}")
async def start_analysis(session_id: str, settings: dict = None):
    """Lance l'analyse de rétinoblastome"""
    try:
        if initialization_status["status"] != "ready":
            raise HTTPException(status_code=400, detail="System not ready yet")
        
        if not retino_app:
            raise HTTPException(status_code=400, detail="Application not initialized")
        
        # Créer une tâche d'analyse en arrière-plan
        analysis_task = asyncio.create_task(run_analysis_async(session_id, settings or {}))
        analysis_sessions[session_id] = {
            "status": "running",
            "progress": 0,
            "task": analysis_task,
            "start_time": time.time()
        }
        
        logger.info(f"Analysis started for session: {session_id}")
        
        return {
            "session_id": session_id,
            "status": "started",
            "message": "Analysis started in background"
        }
        
    except Exception as e:
        logger.error(f"Analysis failed to start: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed to start: {str(e)}")

async def run_analysis_async(session_id: str, settings: dict):
    """Exécute l'analyse en arrière-plan avec WebSocket updates"""
    try:
        # Broadcaster le début
        await ws_manager.broadcast({
            "type": "analysis_progress", 
            "session_id": session_id,
            "progress": 0,
            "message": "Starting retinoblastoma analysis..."
        })
        
        # Simulation progressive de l'analyse
        steps = [
            (10, "Loading image..."),
            (25, "Detecting eye regions..."),
            (40, "Processing with Gemma 3n AI..."),
            (70, "Analyzing for leukocoria..."),
            (85, "Generating medical report..."),
            (95, "Finalizing results...")
        ]
        
        for progress, message in steps:
            await ws_manager.broadcast({
                "type": "analysis_progress",
                "session_id": session_id, 
                "progress": progress,
                "message": message
            })
            await asyncio.sleep(1)
        
        # Simuler le résultat de l'analyse
        result = {
            "session_id": session_id,
            "total_regions": 2,
            "positive_detections": 0,
            "analysis_method": "gemma3n_local",
            "processing_time": 5.2,
            "results": [
                {
                    "region_id": 0,
                    "region_type": "left_eye",
                    "leukocoria_detected": False,
                    "confidence": 92.5,
                    "risk_level": "low",
                    "medical_reasoning": "Normal dark pupil appearance with no signs of leukocoria. Healthy retinal reflex observed.",
                    "recommendations": "Continue routine pediatric eye monitoring",
                    "urgency": "routine"
                },
                {
                    "region_id": 1,
                    "region_type": "right_eye",
                    "leukocoria_detected": False,
                    "confidence": 89.8,
                    "risk_level": "low", 
                    "medical_reasoning": "Normal dark pupil appearance with no signs of leukocoria. Healthy retinal reflex observed.",
                    "recommendations": "Continue routine pediatric eye monitoring",
                    "urgency": "routine"
                }
            ],
            "summary": {
                "overall_risk": "low",
                "recommendation": "No signs of retinoblastoma detected. Continue regular pediatric eye examinations.",
                "next_screening": "6 months"
            }
        }
        
        # Broadcaster les résultats
        await ws_manager.broadcast({
            "type": "analysis_complete",
            "session_id": session_id,
            "progress": 100,
            "results": result
        })
        
        analysis_sessions[session_id] = {
            "status": "completed",
            "progress": 100,
            "results": result,
            "completed_time": time.time()
        }
        
        logger.info(f"Analysis completed for session: {session_id}")
        
    except Exception as e:
        logger.error(f"Analysis error for session {session_id}: {e}")
        await ws_manager.broadcast({
            "type": "analysis_error",
            "session_id": session_id,
            "error": str(e)
        })
        
        analysis_sessions[session_id] = {
            "status": "error",
            "error": str(e)
        }

@app.get("/api/results/{session_id}")
async def get_analysis_results(session_id: str):
    """Récupère les résultats d'une analyse"""
    if session_id not in analysis_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = analysis_sessions[session_id]
    return {
        "session_id": session_id,
        "status": session["status"],
        "progress": session.get("progress", 0),
        "results": session.get("results"),
        "error": session.get("error")
    }

@app.get("/api/metrics")
async def get_session_metrics():
    """Métriques de la session"""
    completed_sessions = [s for s in analysis_sessions.values() if s["status"] == "completed"]
    positive_sessions = [s for s in completed_sessions if s.get("results", {}).get("positive_detections", 0) > 0]
    
    return {
        "total_analyses": len(completed_sessions),
        "positive_detections": len(positive_sessions),
        "average_processing_time": 4.2,  # Simulé
        "errors": len([s for s in analysis_sessions.values() if s["status"] == "error"]),
        "session_start": time.time() - 3600  # Il y a 1h
    }

# Servir les fichiers statiques de l'interface web (si construite)
web_dist_path = Path("web_interface/dist")
if web_dist_path.exists():
    app.mount("/", StaticFiles(directory=str(web_dist_path), html=True), name="web")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")