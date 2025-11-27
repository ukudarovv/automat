import React from 'react';
import './StartPage.css';

type FlowType = 'school' | 'instructor' | 'certificate';

interface StartPageProps {
  onFlowSelect: (flow: FlowType) => void;
}

const StartPage: React.FC<StartPageProps> = ({ onFlowSelect }) => {
  return (
    <div className="start-page">
      <div className="start-header">
        <h1>👋 Добро пожаловать в AvtoMat!</h1>
        <p>Выберите подходящий вариант:</p>
      </div>
      
      <div className="start-options">
        <button 
          className="flow-button school-button"
          onClick={() => onFlowSelect('school')}
        >
          <div className="button-icon">🚗</div>
          <div className="button-content">
            <div className="button-title">Нет водительских прав</div>
            <div className="button-subtitle">Хочу стать водителем</div>
          </div>
        </button>

        <button 
          className="flow-button instructor-button"
          onClick={() => onFlowSelect('instructor')}
        >
          <div className="button-icon">👨‍🏫</div>
          <div className="button-content">
            <div className="button-title">Есть водительские права</div>
            <div className="button-subtitle">Хочу практику с инструктором</div>
          </div>
        </button>

        <button 
          className="flow-button certificate-button"
          onClick={() => onFlowSelect('certificate')}
        >
          <div className="button-icon">📜</div>
          <div className="button-content">
            <div className="button-title">Есть сертификат</div>
            <div className="button-subtitle">Выберите опцию</div>
          </div>
        </button>
      </div>
    </div>
  );
};

export default StartPage;

