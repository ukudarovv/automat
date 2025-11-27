import React, { useState, useEffect } from 'react';
import { useTelegram } from '../hooks/useTelegram';
import api from '../services/api';
import type { City, School } from '../types';
import './SchoolFlow.css';

interface SchoolFlowProps {
  onBack: () => void;
}

const CATEGORIES = ['A', 'B', 'BE', 'C', 'CE', 'D', 'DE', 'A1', 'C1', 'D1'];
const FORMATS = [
  { value: 'online', label: 'Онлайн' },
  { value: 'offline', label: 'Оффлайн' },
  { value: 'hybrid', label: 'Гибрид' },
];

const SchoolFlow: React.FC<SchoolFlowProps> = ({ onBack }) => {
  const { webApp, user, initData } = useTelegram();
  const [step, setStep] = useState<'city' | 'category' | 'format' | 'schools' | 'form'>('city');
  const [cities, setCities] = useState<City[]>([]);
  const [selectedCity, setSelectedCity] = useState<City | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [selectedFormat, setSelectedFormat] = useState<string>('');
  const [schools, setSchools] = useState<School[]>([]);
  const [selectedSchool, setSelectedSchool] = useState<School | null>(null);
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
    setStep('category');
  };

  const handleCategorySelect = (category: string) => {
    setSelectedCategory(category);
    setStep('format');
  };

  const handleFormatSelect = async (format: string) => {
    setSelectedFormat(format);
    setLoading(true);
    try {
      const data = await api.getSchools(selectedCity?.name);
      setSchools(data);
      setStep('schools');
    } catch (error) {
      console.error('Failed to load schools:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSchoolSelect = (school: School) => {
    setSelectedSchool(school);
    setStep('form');
  };

  const handleSubmit = async () => {
    if (!formData.name || !formData.phone || !selectedSchool || !selectedCity) {
      webApp?.showAlert('Пожалуйста, заполните все поля');
      return;
    }

    setLoading(true);
    try {
      await api.createApplication({
        telegram_id: user?.id || 0,
        school: selectedSchool.id,
        city: selectedCity.id,
        category: selectedCategory,
        format: selectedFormat as 'online' | 'offline' | 'hybrid',
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
    <div className="school-flow">
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

      {step === 'category' && (
        <div className="step-content">
          <h2>🚗 Выберите категорию прав</h2>
          <div className="options-grid">
            {CATEGORIES.map(cat => (
              <button
                key={cat}
                className="option-button"
                onClick={() => handleCategorySelect(cat)}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>
      )}

      {step === 'format' && (
        <div className="step-content">
          <h2>📚 Выберите формат обучения</h2>
          <div className="options-list">
            {FORMATS.map(format => (
              <button
                key={format.value}
                className="option-button large"
                onClick={() => handleFormatSelect(format.value)}
              >
                {format.label}
              </button>
            ))}
          </div>
        </div>
      )}

      {step === 'schools' && (
        <div className="step-content">
          <h2>🏫 Доступные автошколы</h2>
          {loading ? (
            <div>Загрузка...</div>
          ) : schools.length === 0 ? (
            <div>В этом городе пока нет доступных автошкол</div>
          ) : (
            <div className="schools-list">
              {schools.map(school => (
                <div
                  key={school.id}
                  className="school-card"
                  onClick={() => handleSchoolSelect(school)}
                >
                  <div className="school-name">{school.name}</div>
                  <div className="school-rating">⭐ {school.rating}</div>
                  <div className="school-address">📍 {school.address}</div>
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

export default SchoolFlow;

