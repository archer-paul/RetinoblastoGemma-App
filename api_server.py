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
        logger.info("🔄 Starting REAL RetinoblastoGemma initialization...")
        
        # === VRAIE INITIALISATION - PAS DE SIMULATION ===
        print("\n🤖 STARTING REAL GEMMA 3N INITIALIZATION")
        print("="*60)
        
        # Importer le module main réel
        import sys
        sys.path.append('.')
        from main import RetinoblastoGemmaV6
        
        # Créer une instance réelle (pas Tkinter)
        class HeadlessRetinoblastoGemma:
            def __init__(self):
                self.eye_detector = None
                self.face_handler = None
                self.visualizer = None
                self.gemma_handler = None
            
            async def initialize_real_modules(self):
                """Initialise les vrais modules avec diffusion WebSocket"""
                try:
                    initialization_status["status"] = "loading"
                    initialization_status["overall_progress"] = 0
                    
                    # Diffuser l'état initial
                    await ws_manager.broadcast({
                        "type": "initialization_progress",
                        "status": initialization_status,
                        "message": "Starting system initialization..."
                    })
                    
                    # 1. Eye Detector (25%)
                    print("🔄 Loading Eye Detector...")
                    initialization_status["modules"]["eye_detector"]["status"] = "loading"
                    initialization_status["overall_progress"] = 10
                    await ws_manager.broadcast({
                        "type": "initialization_progress",
                        "status": initialization_status,
                        "message": "Loading Eye Detector..."
                    })
                    
                    from core.eye_detector_v2 import EyeDetectorV2
                    self.eye_detector = EyeDetectorV2()
                    initialization_status["modules"]["eye_detector"]["status"] = "ready"
                    initialization_status["overall_progress"] = 25
                    print("✅ Eye Detector loaded")
                    
                    await ws_manager.broadcast({
                        "type": "initialization_progress",
                        "status": initialization_status,
                        "message": "Eye Detector ready"
                    })
                    
                    # 2. Face Handler (50%)
                    print("🔄 Loading Face Handler...")
                    initialization_status["modules"]["face_handler"]["status"] = "loading"
                    initialization_status["overall_progress"] = 35
                    await ws_manager.broadcast({
                        "type": "initialization_progress",
                        "status": initialization_status,
                        "message": "Loading Face Handler..."
                    })
                    
                    from core.face_handler_v2 import FaceHandlerV2
                    self.face_handler = FaceHandlerV2()
                    initialization_status["modules"]["face_handler"]["status"] = "ready"
                    initialization_status["overall_progress"] = 50
                    print("✅ Face Handler loaded")
                    
                    await ws_manager.broadcast({
                        "type": "initialization_progress",
                        "status": initialization_status,
                        "message": "Face Handler ready"
                    })
                    
                    # 3. Visualizer (65%)
                    print("🔄 Loading Visualizer...")
                    initialization_status["modules"]["visualizer"]["status"] = "loading"
                    initialization_status["overall_progress"] = 55
                    await ws_manager.broadcast({
                        "type": "initialization_progress",
                        "status": initialization_status,
                        "message": "Loading Visualizer..."
                    })
                    
                    from core.visualization_v2 import VisualizationV2
                    self.visualizer = VisualizationV2()
                    initialization_status["modules"]["visualizer"]["status"] = "ready"
                    initialization_status["overall_progress"] = 65
                    print("✅ Visualizer loaded")
                    
                    await ws_manager.broadcast({
                        "type": "initialization_progress",
                        "status": initialization_status,
                        "message": "Visualizer ready"
                    })
                    
                    # 4. GEMMA 3N - LE PLUS CRITIQUE (65% -> 100%)
                    print("🔄 Loading Gemma 3n - This will take 3-5 minutes...")
                    initialization_status["modules"]["gemma"]["status"] = "loading"
                    initialization_status["overall_progress"] = 70
                    await ws_manager.broadcast({
                        "type": "initialization_progress",
                        "status": initialization_status,
                        "message": "🤖 Loading Gemma 3n model - this may take 3-5 minutes..."
                    })
                    
                    from core.gemma_handler_v2 import GemmaHandlerV2
                    self.gemma_handler = GemmaHandlerV2()
                    
                    # Diffuser pendant le chargement de Gemma
                    await ws_manager.broadcast({
                        "type": "initialization_progress",
                        "status": initialization_status,
                        "message": "🤖 Initializing Gemma 3n model weights..."
                    })
                    
                    # VRAIE CHARGEMENT DU MODÈLE (bloquant)
                    print("🤖 Starting Gemma 3n local model loading...")
                    
                    # Utiliser run_in_executor pour ne pas bloquer
                    import asyncio
                    loop = asyncio.get_event_loop()
                    
                    initialization_status["overall_progress"] = 75
                    await ws_manager.broadcast({
                        "type": "initialization_progress",
                        "status": initialization_status,
                        "message": "🤖 Loading Gemma 3n weights (3-5 minutes)..."
                    })
                    
                    gemma_success = await loop.run_in_executor(
                        None, self.gemma_handler.initialize_local_model
                    )
                    
                    if gemma_success:
                        initialization_status["modules"]["gemma"]["status"] = "ready"
                        initialization_status["overall_progress"] = 100
                        print("✅ Gemma 3n REALLY loaded and ready!")
                        
                        await ws_manager.broadcast({
                            "type": "initialization_progress",
                            "status": initialization_status,
                            "message": "✅ Gemma 3n model loaded successfully!"
                        })
                    else:
                        raise Exception("Gemma 3n failed to initialize")
                    
                except Exception as e:
                    print(f"❌ Module initialization error: {e}")
                    initialization_status["status"] = "error"
                    initialization_status["error"] = str(e)
                    await ws_manager.broadcast({
                        "type": "initialization_error",
                        "status": initialization_status,
                        "error": str(e)
                    })
                    raise e
        
        # Créer l'instance headless
        retino_app = HeadlessRetinoblastoGemma()
        
        # Initialiser les modules de façon asynchrone
        await retino_app.initialize_real_modules()
        
        initialization_status["status"] = "ready"
        initialization_status["overall_progress"] = 100
        
        await ws_manager.broadcast({
            "type": "initialization_complete",
            "status": initialization_status,
            "message": "All modules loaded successfully!"
        })
        
        logger.info("✅ REAL RetinoblastoGemma initialized successfully")
        print("🚀 SYSTEM READY FOR REAL ANALYSIS!")
        
    except Exception as e:
        logger.error(f"❌ REAL Initialization failed: {e}")
        print(f"❌ INITIALIZATION FAILED: {e}")
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
    """Lance l'analyse RÉELLE de rétinoblastome"""
    try:
        logger.info(f"🔍 REAL Analysis request for session: {session_id}")
        
        if initialization_status["status"] != "ready":
            raise HTTPException(status_code=400, detail="System not ready yet")
        
        if not retino_app:
            raise HTTPException(status_code=400, detail="Application not initialized")
        
        # Lancer l'analyse RÉELLE en arrière-plan
        analysis_task = asyncio.create_task(run_REAL_analysis_async(session_id, settings or {}))
        analysis_sessions[session_id] = {
            "status": "running",
            "progress": 0,
            "task": analysis_task,
            "start_time": time.time()
        }
        
        logger.info(f"✅ REAL Analysis started for session: {session_id}")
        
        return {
            "session_id": session_id,
            "status": "started",
            "message": "REAL Analysis started with Gemma 3n"
        }
        
    except Exception as e:
        logger.error(f"REAL Analysis failed to start: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


async def run_REAL_analysis_async(session_id: str, settings: dict):
    """Exécute l'analyse RÉELLE avec les vrais modules"""
    try:
        global retino_app
        
        # 1. Récupérer le chemin de l'image - CORRIGÉ
        import glob
        image_files = glob.glob(f"uploads/{session_id}_*")
        if not image_files:
            raise Exception(f"No image found for session {session_id}")
        
        image_path = image_files[0]  # Prendre le premier fichier trouvé
        
        await ws_manager.broadcast({
            "type": "analysis_progress", 
            "session_id": session_id,
            "progress": 10,
            "message": "Loading image with real eye detector..."
        })
        
        # 2. VRAIE détection des yeux
        detection_results = retino_app.eye_detector.detect_eyes_and_faces(
            image_path, enhanced_mode=settings.get('enhanced_detection', True)
        )
        
        await ws_manager.broadcast({
            "type": "analysis_progress", 
            "session_id": session_id,
            "progress": 40,
            "message": "Running REAL Gemma 3n analysis..."
        })
        
        # 3. VRAIE analyse avec Gemma 3n
        if retino_app.gemma_handler and retino_app.gemma_handler.is_ready():
            analysis_results = retino_app.gemma_handler.analyze_eye_regions(
                detection_results['regions'],
                confidence_threshold=settings.get('confidence_threshold', 0.5)
            )
        else:
            # Fallback si Gemma pas prêt
            analysis_results = {
                'regions_analyzed': len(detection_results.get('regions', [])),
                'method': 'fallback_no_gemma',
                'results': [{
                    'region_id': 0,
                    'region_type': 'fallback',
                    'leukocoria_detected': False,
                    'confidence': 25,
                    'risk_level': 'unknown',
                    'medical_reasoning': 'Gemma 3n not available - basic analysis only',
                    'recommendations': 'Professional medical evaluation required',
                    'urgency': 'soon'
                }]
            }
        
        await ws_manager.broadcast({
            "type": "analysis_progress", 
            "session_id": session_id,
            "progress": 80,
            "message": "Processing results..."
        })
        
        # 4. Finaliser
        analysis_sessions[session_id] = {
            "status": "completed",
            "progress": 100,
            "results": analysis_results,
            "completed_time": time.time()
        }
        
        await ws_manager.broadcast({
            "type": "analysis_complete",
            "session_id": session_id,
            "progress": 100,
            "results": analysis_results
        })
        
        logger.info(f"✅ REAL Analysis completed for session: {session_id}")
        
    except Exception as e:
        logger.error(f"❌ REAL Analysis error: {e}")
        await ws_manager.broadcast({
            "type": "analysis_error",
            "session_id": session_id,
            "error": str(e)
        })

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