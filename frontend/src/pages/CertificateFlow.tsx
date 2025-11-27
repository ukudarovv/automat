import React from 'react';
import './CertificateFlow.css';

type FlowType = 'school' | 'instructor';

interface CertificateFlowProps {
  onFlowSelect: (flow: FlowType) => void;
}

const CertificateFlow: React.FC<CertificateFlowProps> = ({ onFlowSelect }) => {
  return (
    <div className="certificate-flow">
      <div className="step-content">
        <h2>📜 Выберите опцию</h2>
        <div className="options-list">
          <button
            className="option-button large"
            onClick={() => onFlowSelect('school')}
          >
            Полный курс обучения
          </button>
          <button
            className="option-button large"
            onClick={() => onFlowSelect('instructor')}
          >
            Только практика
          </button>
          <button
            className="option-button large"
            onClick={() => alert('Функция в разработке')}
          >
            Только тесты
          </button>
        </div>
      </div>
    </div>
  );
};

export default CertificateFlow;

