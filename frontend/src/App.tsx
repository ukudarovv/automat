import React, { useEffect } from 'react';
import { useTelegram } from './hooks/useTelegram';
import StartPage from './pages/StartPage';
import SchoolFlow from './pages/SchoolFlow';
import InstructorFlow from './pages/InstructorFlow';
import CertificateFlow from './pages/CertificateFlow';
import './App.css';

type FlowType = 'start' | 'school' | 'instructor' | 'certificate';

function App() {
  const { webApp, isReady } = useTelegram();
  const [currentFlow, setCurrentFlow] = React.useState<FlowType>('start');

  useEffect(() => {
    if (webApp) {
      // Set theme
      document.documentElement.style.setProperty('--tg-theme-bg-color', webApp.themeParams.bg_color || '#ffffff');
      document.documentElement.style.setProperty('--tg-theme-text-color', webApp.themeParams.text_color || '#000000');
      document.documentElement.style.setProperty('--tg-theme-hint-color', webApp.themeParams.hint_color || '#999999');
      document.documentElement.style.setProperty('--tg-theme-link-color', webApp.themeParams.link_color || '#2481cc');
      document.documentElement.style.setProperty('--tg-theme-button-color', webApp.themeParams.button_color || '#2481cc');
      document.documentElement.style.setProperty('--tg-theme-button-text-color', webApp.themeParams.button_text_color || '#ffffff');
    }
  }, [webApp]);

  if (!isReady) {
    return <div>Loading...</div>;
  }

  const handleFlowChange = (flow: FlowType) => {
    setCurrentFlow(flow);
  };

  return (
    <div className="App">
      {currentFlow === 'start' && <StartPage onFlowSelect={handleFlowChange} />}
      {currentFlow === 'school' && <SchoolFlow onBack={() => setCurrentFlow('start')} />}
      {currentFlow === 'instructor' && <InstructorFlow onBack={() => setCurrentFlow('start')} />}
      {currentFlow === 'certificate' && <CertificateFlow onFlowSelect={handleFlowChange} />}
    </div>
  );
}

export default App;
