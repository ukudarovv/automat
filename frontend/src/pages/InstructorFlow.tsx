import React, { useState, useEffect } from 'react';
import { useTelegram } from '../hooks/useTelegram';
import api from '../services/api';
import type { City, Instructor } from '../types';
import './InstructorFlow.css';

interface InstructorFlowProps {
  onBack: () => void;
}

const AUTO_TYPES = [
  { value: 'automatic', label: 'Автомат' },
  { value: 'manual', label: 'Механика' },
];

const InstructorFlow: React.FC<InstructorFlowProps> = ({ onBack }) => {
  const { webApp, user } = useTelegram();
  const [step, setStep] = useState<'city' | 'autoType' | 'instructors' | 'form'>('city');
  const [cities, setCities] = useState<City[]>([]);
  const [selectedCity, setSelectedCity] = useState<City | null>(null);
  const [selectedAutoType, setSelectedAutoType] = useState<string>('');
  const [instructors, setInstructors] = useState<Instructor[]>([]);
  const [selectedInstructor, setSelectedInstructor] = useState<Instructor | null>(null);
  const [formData, setFormData] = useState({ name: '', phone: '' });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadCities();
    if (user?.first_name) {
      setFormData(prev => ({ ...prev, name: user.first_name }));
    }
  }, [user]);

  const loadCities = async () => {
    try {
      const data = await api.getCities();
      setCities(data);
    } catch (error) {
      console.error('Failed to load cities:', error);
    }
  };

  const handleCitySelect = (city: City) => {
    setSelectedCity(city);
    setStep('autoType');
  };

  const handleAutoTypeSelect = async (autoType: string) => {
    setSelectedAutoType(autoType);
    setLoading(true);
    try {
      const data = await api.getInstructors(selectedCity?.name, autoType);
      setInstructors(data);
      setStep('instructors');
    } catch (error) {
      console.error('Failed to load instructors:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleInstructorSelect = (instructor: Instructor) => {
    setSelectedInstructor(instructor);
    setStep('form');
  };

  const handleSubmit = async () => {
    if (!formData.name || !formData.phone || !selectedInstructor || !selectedCity) {
      webApp?.showAlert('Пожалуйста, заполните все поля');
      return;
    }

    setLoading(true);
    try {
      await api.createApplication({
        telegram_id: user?.id || 0,
        instructor: selectedInstructor.id,
        city: selectedCity.id,
        student_name: formData.name,
        student_phone: formData.phone,
      });

      webApp?.showAlert('✅ Заявка успешно отправлена!', () => {
        onBack();
      });
    } catch (error) {
      console.error('Failed to create application:', error);
      webApp?.showAlert('Ошибка при отправке заявки');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="instructor-flow">
      {step === 'city' && (
        <div className="step-content">
          <h2>🏙 Выберите город</h2>
          <div className="options-grid">
            {cities.map(city => (
              <button
                key={city.id}
                className="option-button"
                onClick={() => handleCitySelect(city)}
              >
                {city.name_ru || city.name}
              </button>
            ))}
          </div>
        </div>
      )}

      {step === 'autoType' && (
        <div className="step-content">
          <h2>🚗 Выберите тип автомобиля</h2>
          <div className="options-list">
            {AUTO_TYPES.map(type => (
              <button
                key={type.value}
                className="option-button large"
                onClick={() => handleAutoTypeSelect(type.value)}
              >
                {type.label}
              </button>
            ))}
          </div>
        </div>
      )}

      {step === 'instructors' && (
        <div className="step-content">
          <h2>👨‍🏫 Доступные инструкторы</h2>
          {loading ? (
            <div>Загрузка...</div>
          ) : instructors.length === 0 ? (
            <div>В этом городе пока нет доступных инструкторов</div>
          ) : (
            <div className="instructors-list">
              {instructors.map(instructor => (
                <div
                  key={instructor.id}
                  className="instructor-card"
                  onClick={() => handleInstructorSelect(instructor)}
                >
                  <div className="instructor-name">{instructor.name}</div>
                  <div className="instructor-rating">⭐ {instructor.rating}</div>
                  <div className="instructor-type">🚗 {instructor.auto_type_display}</div>
                  <div className="instructor-phone">📞 {instructor.phone}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {step === 'form' && (
        <div className="step-content">
          <h2>📝 Заполните заявку</h2>
          <div className="form">
            <input
              type="text"
              placeholder="Ваше имя"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="form-input"
            />
            <input
              type="tel"
              placeholder="Номер телефона (+7XXXXXXXXXX)"
              value={formData.phone}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              className="form-input"
            />
            <button
              className="submit-button"
              onClick={handleSubmit}
              disabled={loading}
            >
              {loading ? 'Отправка...' : 'Отправить заявку'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default InstructorFlow;

