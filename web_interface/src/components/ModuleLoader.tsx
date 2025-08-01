import { useState, useEffect } from 'react';
import { Progress } from '@/components/ui/progress';
import { CheckCircle, Clock, AlertTriangle, Brain, Eye, Users, BarChart3 } from 'lucide-react';

interface Module {
  id: string;
  name: string;
  icon: React.ComponentType<{ className?: string }>;
  description: string;
  status: 'waiting' | 'loading' | 'ready' | 'error';
  progress: number;
  loadTime?: string;
}

export const ModuleLoader = () => {
  const [modules, setModules] = useState<Module[]>([
    {
      id: 'gemma',
      name: 'Gemma 3n',
      icon: Brain,
      description: 'AI Model Loading...',
      status: 'waiting',
      progress: 0
    },
    {
      id: 'eye-detector',
      name: 'Eye Detector',
      icon: Eye,
      description: 'Computer Vision Module',
      status: 'waiting',
      progress: 0
    },
    {
      id: 'face-handler',
      name: 'Face Handler',
      icon: Users,
      description: 'Face Tracking System',
      status: 'waiting',
      progress: 0
    },
    {
      id: 'visualizer',
      name: 'Visualizer',
      icon: BarChart3,
      description: 'Medical Results Engine',
      status: 'waiting',
      progress: 0
    }
  ]);

  const [isInitializing, setIsInitializing] = useState(true);
  const [overallProgress, setOverallProgress] = useState(0);

  useEffect(() => {
    const loadModules = async () => {
      const loadOrder = ['gemma', 'eye-detector', 'face-handler', 'visualizer'];
      const loadTimes = [5000, 1500, 1000, 800]; // Simulated load times

      for (let i = 0; i < loadOrder.length; i++) {
        const moduleId = loadOrder[i];
        const loadTime = loadTimes[i];

        // Start loading
        setModules(prev => prev.map(module => 
          module.id === moduleId 
            ? { ...module, status: 'loading', description: 'Loading...' }
            : module
        ));

        // Simulate loading progress
        const startTime = Date.now();
        const interval = setInterval(() => {
          const elapsed = Date.now() - startTime;
          const progress = Math.min((elapsed / loadTime) * 100, 100);
          
          setModules(prev => prev.map(module => 
            module.id === moduleId 
              ? { ...module, progress }
              : module
          ));

          if (progress >= 100) {
            clearInterval(interval);
            const finalLoadTime = ((Date.now() - startTime) / 1000).toFixed(1);
            
            setModules(prev => prev.map(module => 
              module.id === moduleId 
                ? { 
                    ...module, 
                    status: 'ready', 
                    progress: 100,
                    description: 'Ready',
                    loadTime: `${finalLoadTime}s`
                  }
                : module
            ));
          }
        }, 50);

        // Wait for module to load before starting next
        await new Promise(resolve => setTimeout(resolve, loadTime));
        
        // Update overall progress
        setOverallProgress(((i + 1) / loadOrder.length) * 100);
      }

      setTimeout(() => setIsInitializing(false), 1000);
    };

    loadModules();
  }, []);

  const getStatusIcon = (status: Module['status']) => {
    switch (status) {
      case 'ready':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'loading':
        return <Clock className="w-5 h-5 text-yellow-500 animate-pulse" />;
      case 'error':
        return <AlertTriangle className="w-5 h-5 text-red-500" />;
      default:
        return <Clock className="w-5 h-5 text-gray-400" />;
    }
  };

  if (!isInitializing) return null;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="glass-card max-w-2xl w-full mx-4 space-y-6">
        <div className="text-center space-y-4">
          <div className="inline-flex items-center gap-3 bg-gemini px-6 py-3 rounded-full text-white font-semibold">
            <Brain className="w-6 h-6" />
            RetinoblastoGemma Initialization
          </div>
          <p className="text-muted-foreground">
            Loading AI modules for local retinoblastoma detection
          </p>
          
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span>Overall Progress</span>
              <span>{Math.round(overallProgress)}%</span>
            </div>
            <Progress value={overallProgress} className="h-2" />
          </div>
        </div>

        <div className="space-y-4">
          {modules.map((module) => {
            const IconComponent = module.icon;
            return (
              <div key={module.id} className="flex items-center gap-4 p-4 rounded-lg border bg-card/50">
                <div className="flex-shrink-0">
                  <IconComponent className="w-8 h-8 text-primary" />
                </div>
                
                <div className="flex-1 space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <h3 className="font-semibold">{module.name}</h3>
                      {getStatusIcon(module.status)}
                    </div>
                    {module.loadTime && (
                      <span className="text-xs text-muted-foreground">
                        {module.loadTime}
                      </span>
                    )}
                  </div>
                  
                  <p className="text-sm text-muted-foreground">
                    {module.description}
                  </p>
                  
                  {module.status === 'loading' && (
                    <Progress value={module.progress} className="h-1" />
                  )}
                </div>
              </div>
            );
          })}
        </div>

        <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          100% Local Processing - Privacy First
        </div>
      </div>
    </div>
  );
};