import React, { FC, useState } from 'react';
import { useTranslation } from 'react-i18next';
import apiClient from '../common/apiClient'; // Импортируем API-клиент

interface AttackScript {
  id: number;
  nameKey: string; // Ключ для перевода имени
  descriptionKey: string; // Ключ для перевода короткого описания
  fullDescriptionKey: string; // Ключ для перевода полного описания
  imageKey: string; // Ключ для перевода ссылки на миниатюру
  backendRoute: string; // Роут на бэкенде для запуска скрипта
}

interface AttackScriptsGridProps {
  items: AttackScript[];
}

export const AttackScriptsGrid: FC<AttackScriptsGridProps> = ({ items }) => {
  const { t } = useTranslation();
  const [showModal, setShowModal] = useState(false);
  const [selectedScript, setSelectedScript] = useState<AttackScript | null>(null);
  const [executionResult, setExecutionResult] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [inputData, setInputData] = useState({
    targetSubnet: '',
    kaliIp: '',
  });

  // Открытие модального окна с формой
  const handleShowDetails = (script: AttackScript) => {
    setSelectedScript(script);
    setShowModal(true);
  };

  // Закрытие модального окна
  const handleCloseModal = () => {
    setShowModal(false);
    setExecutionResult(null); // Очищаем результат после закрытия
    setInputData({ targetSubnet: '', kaliIp: '' }); // Сбрасываем ввод
  };

  // Обработка ввода данных
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setInputData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // Запуск скрипта
  const handleRunScript = async () => {
    if (!selectedScript || !inputData.targetSubnet || !inputData.kaliIp) {
      alert('Пожалуйста, заполните все поля.');
      return;
    }

    setIsLoading(true); // Показываем индикатор загрузки
    try {
      // Выполняем запрос к бэкенду
      const response = await apiClient.post(selectedScript.backendRoute, {
        target_subnet: inputData.targetSubnet,
        kali_ip: inputData.kaliIp,
      });
      setExecutionResult(JSON.stringify(response, null, 2)); // Сохраняем результат
    } catch (error) {
      console.error('Ошибка при выполнении скрипта:', error);
      setExecutionResult('Произошла ошибка при выполнении скрипта.');
    } finally {
      setIsLoading(false); // Скрываем индикатор загрузки
    }
  };

  return (
    <div className="attack-scripts-grid-container">
      {items.map((script) => (
        <div className="attack-script-item" key={script.id}>
          {/* Название карточки */}
          <h3 className="attack-script-title">{t(script.nameKey)}</h3>
          {/* Миниатюра изображения */}
          <img src={script.imageKey} alt={t(script.nameKey)} className="attack-script-image" />
          {/* Короткое описание */}
          <p className="attack-script-description">{t(script.descriptionKey)}</p>
          {/* Кнопки управления */}
          <div className="attack-script-actions">
            <button
              className="attack-script-button attack-script-run"
              onClick={() => handleShowDetails(script)}
            >
              {t('attack_scripts.Run')}
            </button>
          </div>
        </div>
      ))}

      {/* Модальное окно */}
      {showModal && selectedScript && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>{t(selectedScript.nameKey)}</h3>
            <p>{t(selectedScript.fullDescriptionKey)}</p>

            {/* Форма для ввода данных */}
            <div className="input-form">
              <label>
                {t('attack_scripts.Target_Subnet')}:
                <input
                  type="text"
                  name="targetSubnet"
                  value={inputData.targetSubnet}
                  onChange={handleInputChange}
                  placeholder="192.168.0.0/24"
                />
              </label>
              <label>
                {t('attack_scripts.Kali_IP')}:
                <input
                  type="text"
                  name="kaliIp"
                  value={inputData.kaliIp}
                  onChange={handleInputChange}
                  placeholder="192.168.0.101"
                />
              </label>
            </div>

            {/* Кнопки управления */}
            <div className="modal-buttons">
              <button
                onClick={handleRunScript}
                disabled={isLoading || !inputData.targetSubnet || !inputData.kaliIp}
              >
                {isLoading ? t('attack_scripts.Running') : t('attack_scripts.Run')}
              </button>
              <button onClick={handleCloseModal}>{t('attack_scripts.Close')}</button>
            </div>

            {/* Результат выполнения */}
            {executionResult && (
              <div className="execution-result">
                <h4>{t('attack_scripts.Execution_Result')}:</h4>
                <pre className="result-output">{executionResult}</pre>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};