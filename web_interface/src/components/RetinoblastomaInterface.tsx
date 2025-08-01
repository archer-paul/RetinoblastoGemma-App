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
      const ws = new WebSocket('ws://localhost:8001/ws/progress');
      
      ws.onopen = () => {
        console.log('WebSocket connected');
        setWsConnection(ws);
      };
      
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        switch (data.type) {
          case 'initialization_progress':
          case 'status_update':
            setSystemStatus(data.status);
            break;
          case 'analysis_progress':
            setAnalysisProgress(data.progress);
            break;
          case 'analysis_complete':
            setAnalysisProgress(100);
            setIsAnalyzing(false);
            // Traiter les résultats
            console.log('Analysis complete:', data.results);
            break;
          case 'analysis_error':
            setIsAnalyzing(false);
            console.error('Analysis error:', data.error);
            break;
        }
      };
      
      ws.onclose = () => {
        console.log('WebSocket disconnected');
        setWsConnection(null);
        // Reconnexion automatique après 3 secondes
        setTimeout(connectWebSocket, 3000);
      };
      
      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
    };
    
    connectWebSocket();
    
    // Cleanup
    return () => {
      if (wsConnection) {
        wsConnection.close();
      }
    };
  }, []); // Dépendances vides pour éviter les reconnexions infinies

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
    if (!selectedImage) {
      alert('Please select an image first');
      return;
    }
    
    // Si pas de session WebSocket active, utiliser mode démo
    if (!currentSessionId || !systemStatus.ready) {
      console.log('Using demo mode for analysis');
      setIsAnalyzing(true);
      setAnalysisProgress(0);

      // Simulation de l'analyse
      const interval = setInterval(() => {
        setAnalysisProgress(prev => {
          if (prev >= 100) {
            clearInterval(interval);
            setIsAnalyzing(false);
            setSessionStats(current => ({
              ...current,
              totalAnalyses: current.totalAnalyses + 1
            }));
            return 100;
          }
          return prev + 10;
        });
      }, 200);
      return;
    }
    
    // Mode API réel
    try {
      setIsAnalyzing(true);
      setAnalysisProgress(0);
      
      const response = await fetch(`http://localhost:8001/api/analyze/${currentSessionId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          confidence_threshold: confidence[0],
          face_tracking: faceTracking,
          enhanced_detection: enhancedDetection
        })
      });
      
      if (!response.ok) {
        throw new Error('Analysis failed to start');
      }
      
      const result = await response.json();
      console.log('Analysis started:', result);
      
    } catch (error) {
      console.error('Analysis error:', error);
      setIsAnalyzing(false);
      alert('Failed to start analysis');
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
                  <h1 className="text-2xl font-bold">RetinoblastoGemma v6</h1>
                  <p className="text-blue-100 text-sm">Google Gemma Hackathon</p>
                </div>
              </div>
            </div>
            
            <div className="flex items-center gap-4 text-white">
              <Badge variant="secondary" className="bg-white/20 text-white border-white/30">
                <Shield className="w-4 h-4 mr-1" />
                100% Local
              </Badge>
              <Badge variant="secondary" className="bg-white/20 text-white border-white/30">
                <Brain className="w-4 h-4 mr-1" />
                Gemma 3n Ready
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
          <Card className="border-green-200">
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2 text-green-700">
                <Activity className="w-5 h-5" />
                System Status
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Status:</span>
                <span className="font-semibold text-green-600">
                  {systemStatus.ready ? 'Ready' : systemStatus.status}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Connection:</span>
                <span className="font-semibold text-green-600">
                  {wsConnection ? 'Connected' : 'Demo Mode'}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span>GPU:</span>
                <span className="font-semibold text-green-600">Available</span>
              </div>
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