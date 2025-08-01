// Imports
import React, { useState, useEffect, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Slider } from '@/components/ui/slider';
import { Switch } from '@/components/ui/switch';
import { Badge } from '@/components/ui/badge';
import { 
  Upload, 
  Brain, 
  Eye, 
  FileImage, 
  Settings, 
  Download, 
  FileText, 
  Lightbulb,
  Users,
  Info,
  Activity,
  Shield,
  Cpu,
  CheckCircle
} from 'lucide-react';

// Types
interface SystemStatus {
  status: string;
  ready: boolean;
  overall_progress: number;
  modules: Record<string, any>;
}

interface AnalysisResult {
  session_id: string;
  total_regions: number;
  positive_detections: number;
  results: Array<{
    region_type: string;
    leukocoria_detected: boolean;
    confidence: number;
    risk_level: string;
  }>;
}

interface AnalysisSession {
  totalAnalyses: number;
  positiveDetections: number;
  averageProcessingTime: number;
  errors: number;
}

export const RetinoblastomaInterface = () => {
  // Tous les états React hooks DOIVENT être à l'intérieur du composant
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [imageInfo, setImageInfo] = useState<{ name: string; dimensions: string } | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisProgress, setAnalysisProgress] = useState(0);
  const [confidence, setConfidence] = useState([0.5]);
  const [faceTracking, setFaceTracking] = useState(true);
  const [enhancedDetection, setEnhancedDetection] = useState(true);
  const [initMessage, setInitMessage] = useState<string>('');
  const [sessionStats, setSessionStats] = useState<AnalysisSession>({
    totalAnalyses: 0,
    positiveDetections: 0,
    averageProcessingTime: 2.3,
    errors: 0
  });
  
  // États WebSocket et système
  const [wsConnection, setWsConnection] = useState<WebSocket | null>(null);
  const [systemStatus, setSystemStatus] = useState<SystemStatus>({
    status: 'initializing',
    ready: false,
    overall_progress: 0,
    modules: {}
  });
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);

  // Effet pour la connexion WebSocket
  useEffect(() => {
  const connectWebSocket = () => {
    console.log('🔌 Connecting to WebSocket...');
    const ws = new WebSocket('ws://localhost:8001/ws/progress');
    
    ws.onopen = () => {
      console.log('✅ WebSocket connected to backend');
      setWsConnection(ws);
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log('📨 WebSocket message received:', data);
      
      switch (data.type) {
        case 'initialization_progress':
          console.log('🔄 Initialization progress:', data.status);
          setSystemStatus(data.status);
          setInitMessage(data.message || '');
          break;
          
        case 'initialization_complete':
          console.log('✅ Initialization complete!');
          setSystemStatus(prev => ({
            ...prev,
            status: 'ready',
            ready: true,
            overall_progress: 100
          }));
          break;
          
        case 'initialization_error':
          console.error('❌ Initialization error:', data.error);
          setSystemStatus(prev => ({
            ...prev,
            status: 'error',
            ready: false
          }));
          break;
          
        case 'status_update':
          console.log('📊 Status update:', data.status);
          setSystemStatus(data.status);
          break;
          
        case 'analysis_progress':
          console.log('🔍 Analysis progress:', data.progress);
          setAnalysisProgress(data.progress);
          break;
          
        case 'analysis_complete':
          console.log('✅ Analysis complete:', data.results);
          setAnalysisProgress(100);
          setIsAnalyzing(false);
          setSessionStats(current => ({
            ...current,
            totalAnalyses: current.totalAnalyses + 1,
            positiveDetections: current.positiveDetections + 
              (data.results?.results?.filter(r => r.leukocoria_detected)?.length || 0)
          }));
          break;
          
        case 'analysis_error':
          console.error('❌ Analysis error:', data.error);
          setIsAnalyzing(false);
          alert(`Analysis failed: ${data.error}`);
          break;
          
        case 'ping':
          // Ignore ping messages
          break;
          
        default:
          console.log('📨 Unknown message type:', data.type);
      }
    };
    
    ws.onclose = () => {
      console.log('❌ WebSocket disconnected');
      setWsConnection(null);
      // Reconnexion automatique après 3 secondes
      setTimeout(connectWebSocket, 3000);
    };
    
    ws.onerror = (error) => {
      console.error('❌ WebSocket error:', error);
    };
  };
  
  connectWebSocket();
  
  // Cleanup
  return () => {
    if (wsConnection) {
      wsConnection.close();
    }
  };
}, []); // Dépendances vides pour éviter les reconnexions infinies // Dépendances vides pour éviter les reconnexions infinies

  // Fonction de gestion de l'upload d'image
  const handleImageUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await fetch('http://localhost:8001/api/upload-image', {
        method: 'POST',
        body: formData
      });
      
      if (!response.ok) {
        throw new Error('Upload failed');
      }
      
      const result = await response.json();
      setCurrentSessionId(result.session_id);
      
      const url = URL.createObjectURL(file);
      setSelectedImage(url);
      setImageInfo({
        name: result.image_info.filename,
        dimensions: result.image_info.dimensions
      });
      
      console.log('Image uploaded:', result);
      
    } catch (error) {
      console.error('Upload error:', error);
      alert('Failed to upload image');
      
      // Fallback pour le mode démo
      const url = URL.createObjectURL(file);
      setSelectedImage(url);
      setImageInfo({
        name: file.name,
        dimensions: '224x224' // Dimensions par défaut
      });
    }
  };

  // Fonction d'analyse
  const handleAnalyze = async () => {
    console.log('🔍 ANALYZE CLICKED - REAL MODE ONLY');
    console.log('selectedImage:', selectedImage);
    console.log('currentSessionId:', currentSessionId);
    console.log('systemStatus:', systemStatus);
    
    if (!selectedImage) {
      alert('Please select an image first');
      return;
    }

    if (!currentSessionId) {
      alert('No session ID found. Please re-upload the image.');
      return;
    }

    // PLUS DE MODE DÉMO - SEULEMENT LE VRAI BACKEND
    if (!systemStatus.ready) {
      alert('System is not ready yet. Please wait for all modules to load.');
      return;
    }

    console.log('🚀 Starting REAL analysis with backend');

    try {
      setIsAnalyzing(true);
      setAnalysisProgress(0);

      const requestBody = {
        confidence_threshold: confidence[0],
        face_tracking: faceTracking,
        enhanced_detection: enhancedDetection
      };

      console.log('📤 Sending request to backend:', requestBody);

      const response = await fetch(`http://localhost:8001/api/analyze/${currentSessionId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      });

      console.log('📥 Response status:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Backend error: ${response.status} - ${errorText}`);
      }

      const result = await response.json();
      console.log('✅ Analysis request sent successfully:', result);

      // Le WebSocket se chargera de recevoir les mises à jour de progression

    } catch (error) {
      console.error('❌ Analysis request failed:', error);
      setIsAnalyzing(false);
      alert(`Failed to start analysis: ${error.message}`);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Header */}
      <header className="bg-blue-600 shadow-lg">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-white">
                <Eye className="w-8 h-8" />
                <div>
                  <h1 className="text-2xl font-bold">RetinoblastoGemma</h1>
                  <p className="text-blue-100 text-sm">Google Gemma Hackathon</p>
                </div>
              </div>
            </div>
            
            <div className="flex items-center gap-4 text-white">
              <Badge variant="secondary" className="bg-white/20 text-white border-white/30">
                <Shield className="w-4 h-4 mr-1" />
                100% Local
              </Badge>
              <Badge variant="secondary" className={`${
                systemStatus.ready ? 'bg-emerald-400/30 text-emerald-100 border-emerald-300/50' : 
                'bg-yellow-500/20 text-yellow-700 border-yellow-500/30'
              }`}>
                <Brain className="w-4 h-4 mr-1" />
                {systemStatus.ready ? 'Gemma 3n Ready' : 'Gemma 3n Loading...'}
              </Badge>
              <Badge variant="secondary" className="bg-white/20 text-white border-white/30">
                <CheckCircle className="w-4 h-4 mr-1" />
                Privacy-First
              </Badge>
            </div>
          </div>
        </div>
      </header>

      <div className="flex h-[calc(100vh-80px)]">
        {/* Control Panel */}
        <div className="w-80 bg-white/80 backdrop-blur-sm border-r border-white/20 p-6 space-y-6 overflow-y-auto">
          {/* System Status */}
          <Card className={`border-2 ${
            systemStatus.ready ? 'border-green-200' : 
            systemStatus.status === 'error' ? 'border-red-200' : 'border-yellow-200'
          }`}>
            <CardHeader className="pb-3">
              <CardTitle className={`flex items-center gap-2 ${
                systemStatus.ready ? 'text-green-700' : 
                systemStatus.status === 'error' ? 'text-red-700' : 'text-yellow-700'
              }`}>
                <Activity className="w-5 h-5" />
                System Status
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Status:</span>
                <span className={`font-semibold ${
                  systemStatus.ready ? 'text-green-600' : 
                  systemStatus.status === 'error' ? 'text-red-600' : 'text-yellow-600'
                }`}>
                  {systemStatus.ready ? 'Ready' : systemStatus.status || 'Initializing'}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Progress:</span>
                <span className="font-semibold text-blue-600">
                  {systemStatus.overall_progress || 0}%
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Connection:</span>
                <span className={`font-semibold ${wsConnection ? 'text-green-600' : 'text-red-600'}`}>
                  {wsConnection ? 'Connected' : 'Disconnected'}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Modules:</span>
                <span className="font-semibold text-blue-600">
                  {Object.values(systemStatus.modules || {}).filter(m => m.status === 'ready').length}/4
                </span>
              </div>
              
              {/* Progress bar for initialization */}
              {!systemStatus.ready && (
                <div className="mt-3 space-y-2">
                  <Progress value={systemStatus.overall_progress || 0} className="h-2" />
                  <p className="text-xs text-muted-foreground text-center">
                    System initializing... Please wait.
                  </p>
                </div>
              )}
              
              {/* Detailed module status */}
              {systemStatus.modules && (
                <div className="mt-3 space-y-1">
                  {Object.entries(systemStatus.modules).map(([name, module]) => (
                    <div key={name} className="flex justify-between text-xs">
                      <span className="capitalize">{name.replace('_', ' ')}:</span>
                      <span className={`font-semibold ${
                        module.status === 'ready' ? 'text-green-600' :
                        module.status === 'error' ? 'text-red-600' : 
                        module.status === 'loading' ? 'text-yellow-600' : 'text-gray-600'
                      }`}>
                        {module.status === 'loading' ? 'Loading...' : module.status}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Image Upload */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2">
                <FileImage className="w-5 h-5" />
                Medical Image
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Button 
                  variant="outline" 
                  className="w-full"
                  onClick={() => document.getElementById('image-upload')?.click()}
                >
                  <Upload className="w-4 h-4 mr-2" />
                  Load Medical Image
                </Button>
                <input
                  id="image-upload"
                  type="file"
                  accept="image/*"
                  className="hidden"
                  onChange={handleImageUpload}
                />
              </div>
              
              {imageInfo && (
                <div className="text-sm space-y-1 p-3 bg-blue-50 rounded-lg">
                  <div className="font-medium">{imageInfo.name}</div>
                  <div className="text-muted-foreground">({imageInfo.dimensions})</div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* AI Analysis */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2">
                <Brain className="w-5 h-5" />
                AI Analysis
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Button 
                className="w-full bg-blue-600 hover:bg-blue-700"
                onClick={handleAnalyze}
                disabled={!selectedImage || isAnalyzing}
              >
                {isAnalyzing ? (
                  <>
                    <Cpu className="w-4 h-4 mr-2 animate-pulse" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Brain className="w-4 h-4 mr-2" />
                    Analyze for Retinoblastoma
                  </>
                )}
              </Button>
              
              {isAnalyzing && (
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Progress</span>
                    <span>{analysisProgress}%</span>
                  </div>
                  <Progress value={analysisProgress} className="h-2" />
                  <p className="text-sm text-muted-foreground">
                    Processing with Gemma 3n...
                  </p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Settings */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2">
                <Settings className="w-5 h-5" />
                Settings
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">
                  Confidence Threshold: {confidence[0].toFixed(1)}
                </label>
                <Slider
                  value={confidence}
                  onValueChange={setConfidence}
                  max={1}
                  min={0.1}
                  step={0.1}
                  className="w-full"
                />
              </div>
              
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium">Face Tracking</label>
                <Switch checked={faceTracking} onCheckedChange={setFaceTracking} />
              </div>
              
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium">Enhanced Detection</label>
                <Switch checked={enhancedDetection} onCheckedChange={setEnhancedDetection} />
              </div>
            </CardContent>
          </Card>

          {/* Session Metrics */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2">
                <Activity className="w-5 h-5" />
                Session Metrics
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span>Total analyses:</span>
                <span className="font-semibold">{sessionStats.totalAnalyses}</span>
              </div>
              <div className="flex justify-between">
                <span>Positive detections:</span>
                <span className="font-semibold">{sessionStats.positiveDetections}</span>
              </div>
              <div className="flex justify-between">
                <span>Avg. processing time:</span>
                <span className="font-semibold">{sessionStats.averageProcessingTime}s</span>
              </div>
              <div className="flex justify-between">
                <span>Errors:</span>
                <span className="font-semibold">{sessionStats.errors}</span>
              </div>
            </CardContent>
          </Card>

          {/* Action Buttons */}
          <div className="space-y-2">
            <Button variant="outline" className="w-full">
              <Download className="w-4 h-4 mr-2" />
              Export Results
            </Button>
            <Button variant="outline" className="w-full">
              <FileText className="w-4 h-4 mr-2" />
              Generate Medical Report
            </Button>
            <Button variant="outline" className="w-full">
              <Lightbulb className="w-4 h-4 mr-2" />
              Smart Recommendations
            </Button>
            <Button variant="outline" className="w-full">
              <Users className="w-4 h-4 mr-2" />
              Face Tracking Summary
            </Button>
            <Button variant="outline" className="w-full">
              <Info className="w-4 h-4 mr-2" />
              System Information
            </Button>
          </div>
        </div>

        {/* Main Display Area */}
        <div className="flex-1 p-6">
          <Card className="h-full">
            <CardHeader>
              <CardTitle>Analysis Display</CardTitle>
            </CardHeader>
            <CardContent className="h-full">
              <Tabs defaultValue="image" className="h-full">
                <TabsList className="grid w-full grid-cols-3">
                  <TabsTrigger value="image">🖼️ Image Analysis</TabsTrigger>
                  <TabsTrigger value="results">📋 Medical Results</TabsTrigger>
                  <TabsTrigger value="history">👤 Patient History</TabsTrigger>
                </TabsList>
                
                <TabsContent value="image" className="h-full pt-4">
                  <div className="h-full border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center">
                    {selectedImage ? (
                      <img 
                        src={selectedImage} 
                        alt="Medical scan" 
                        className="max-h-full max-w-full object-contain rounded-lg"
                      />
                    ) : (
                      <div className="text-center text-muted-foreground">
                        <FileImage className="w-16 h-16 mx-auto mb-4 opacity-50" />
                        <p>Upload a medical image to begin analysis</p>
                      </div>
                    )}
                  </div>
                </TabsContent>
                
                <TabsContent value="results" className="h-full pt-4">
                  <div className="h-full border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center">
                    <div className="text-center text-muted-foreground">
                      <FileText className="w-16 h-16 mx-auto mb-4 opacity-50" />
                      <p>Analysis results will appear here</p>
                    </div>
                  </div>
                </TabsContent>
                
                <TabsContent value="history" className="h-full pt-4">
                  <div className="h-full border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center">
                    <div className="text-center text-muted-foreground">
                      <Users className="w-16 h-16 mx-auto mb-4 opacity-50" />
                      <p>Patient history will be displayed here</p>
                    </div>
                  </div>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};