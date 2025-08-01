import { useState } from 'react';
import { ModuleLoader } from '@/components/ModuleLoader';
import { RetinoblastomaInterface } from '@/components/RetinoblastomaInterface';

const Index = () => {
  const [showLoader, setShowLoader] = useState(true);

  // The ModuleLoader will automatically hide after initialization
  return (
    <div>
      {showLoader && <ModuleLoader />}
      <RetinoblastomaInterface />
    </div>
  );
};

export default Index;
