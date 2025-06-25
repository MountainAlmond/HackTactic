import React, { FC, useState, useEffect } from 'react';
import apiClient from '../common/apiClient'; // Импортируем API-клиент
import { useTranslation } from 'react-i18next';

interface InfrastructureItem {
  id: number;
  nameKey: string; // Ключ для перевода имени
  descriptionKey: string; // Ключ для перевода короткого описания
  fullDescriptionKey: string; // Ключ для перевода полного описания
  imageKey: string; // Ключ для перевода ссылки на миниатюру
  deployEndpoint: string; // Эндпоинт для деплоя
}

interface InfraGridProps {
  items: InfrastructureItem[];
}

interface CreateVmResponse {
  vm_name: string;
  ip_address: string;
}

export const InfraGrid: FC<InfraGridProps> = ({ items }) => {
  const { t } = useTranslation();

  // Состояния для управления модальным окном
  const [showModal, setShowModal] = useState(false);
  const [selectedItem, setSelectedItem] = useState<InfrastructureItem | null>(null);

  // Состояние для формы создания VM
  const [formValues, setFormValues] = useState({ cpuCount: 2, ramGb: 4, diskGb: 20 });
  const [isLoading, setIsLoading] = useState(false);

  // Состояния для хранения информации о VM и глобального списка IP
  const [vmInfoMap, setVmInfoMap] = useState<{ [key: number]: { vmName: string; ip: string } }>(
    JSON.parse(localStorage.getItem('vmInfoMap') || '{}')
  );
  const [globalIpList, setGlobalIpList] = useState<string[]>(
    JSON.parse(localStorage.getItem('globalIpList') || '[]')
  );

  // Проверяем роль пользователя и наличие JWT
  const isUserAdmin = localStorage.getItem('username') === 'admin';
  const hasJwtToken = !!localStorage.getItem('jwtToken');

  // Сохранение vmInfoMap в localStorage при изменении
  useEffect(() => {
    localStorage.setItem('vmInfoMap', JSON.stringify(vmInfoMap));
  }, [vmInfoMap]);

  // Сохранение globalIpList в localStorage при изменении
  useEffect(() => {
    localStorage.setItem('globalIpList', JSON.stringify(globalIpList));
  }, [globalIpList]);

  // Открытие модального окна
  const handleDeployClick = (item: InfrastructureItem) => {
    setSelectedItem(item);
    setShowModal(true);
  };

  // Закрытие модального окна
  const handleCloseModal = () => {
    setShowModal(false);
  };

  // Обработка изменений в форме
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormValues({ ...formValues, [name]: parseInt(value, 10) });
  };

  // Создание новой VM
  const handleSubmit = async () => {
    if (!selectedItem) return;

    try {
      setIsLoading(true); // Включаем лоадер

      // Отправляем запрос на создание VM
      const response = await apiClient.post<CreateVmResponse>(selectedItem.deployEndpoint, formValues);

      // Обновляем информацию о VM только для выбранного элемента
      setVmInfoMap((prev) => ({
        ...prev,
        [selectedItem.id]: { vmName: response.vm_name, ip: response.ip_address },
      }));

      // Если nameKey === 'infrastructure.items.service_4', добавляем IP с портом :5601 в глобальный массив
      if (selectedItem.nameKey === 'infrastructure.items.service_4') {
        const ipWithPort = `${response.ip_address}:5601`;
        setGlobalIpList((prev) => [...prev, ipWithPort]);
      }

      handleCloseModal();
    } catch (error) {
      console.error('Ошибка при создании VM:', error);
    } finally {
      setIsLoading(false); // Выключаем лоадер
    }
  };

  // Перезапуск виртуальной машины
  const handleRestart = async (vmName: string) => {
    try {
      await apiClient.post(`/vm/restart/${vmName}`);
      console.log(`VM '${vmName}' restarted successfully`);
    } catch (error) {
      console.error('Ошибка при перезапуске VM:', error);
    }
  };

  // Остановка виртуальной машины
  const handleStop = async (vmName: string) => {
    try {
      await apiClient.post(`/vm/stop/${vmName}`);
      console.log(`VM '${vmName}' stopped successfully`);
    } catch (error) {
      console.error('Ошибка при остановке VM:', error);
    }
  };

  // Удаление виртуальной машины
  const handleDelete = async (vmName: string, itemId: number) => {
    try {
      await apiClient.post(`/vm/delete/${vmName}`);
      console.log(`VM '${vmName}' deleted successfully`);

      // Удаляем информацию о VM из состояния
      setVmInfoMap((prev) => {
        const newVmInfoMap = { ...prev };
        delete newVmInfoMap[itemId];
        return newVmInfoMap;
      });

      // Удаляем IP из глобального списка, если он есть
      setGlobalIpList((prev) => prev.filter((ip) => !ip.includes(vmName)));
    } catch (error) {
      console.error('Ошибка при удалении VM:', error);
    }
  };

  return (
    <div className="infra-grid-container">
      {items.map((item) => (
        <div className="infra-item" key={item.id}>
          {/* Название карточки */}
          <h3 className="infra-item-title">{t(item.nameKey)}</h3>
          {/* Миниатюра изображения */}
          <img src={t(item.imageKey)} alt={t(item.nameKey)} className="infra-item-image" />
          {/* Короткое описание */}
          <p className="infra-item-description">{t(item.descriptionKey)}</p>

          {/* Кнопки управления только для администраторов */}
          {isUserAdmin && hasJwtToken && (
            <div className="infra-item-actions">
              {/* Верхний ряд кнопок */}
              <div className="action-row">
                <button
                  className="infra-action-button infra-action-start"
                  onClick={() => handleDeployClick(item)}
                  disabled={!!vmInfoMap[item.id]} // Отключаем кнопку, если VM уже создана
                >
                  {t('infra_grid.Start')}
                </button>
                <button
                  className="infra-action-button infra-action-restart"
                  onClick={() => {
                    const vmName = vmInfoMap[item.id]?.vmName;
                    if (vmName) handleRestart(vmName);
                  }}
                  disabled={!vmInfoMap[item.id]}
                >
                  {t('infra_grid.Restart')}
                </button>
              </div>
              {/* Нижний ряд кнопок */}
              <div className="action-row">
                <button
                  className="infra-action-button infra-action-stop"
                  onClick={() => {
                    const vmName = vmInfoMap[item.id]?.vmName;
                    if (vmName) handleStop(vmName);
                  }}
                  disabled={!vmInfoMap[item.id]}
                >
                  {t('infra_grid.Stop')}
                </button>
                <button
                  className="infra-action-button infra-action-delete"
                  onClick={() => {
                    const vmName = vmInfoMap[item.id]?.vmName;
                    if (vmName) handleDelete(vmName, item.id);
                  }}
                  disabled={!vmInfoMap[item.id]}
                >
                  {t('infra_grid.Delete')}
                </button>
              </div>
            </div>
          )}

          {/* Информация о созданной VM только для текущей карточки */}
          {vmInfoMap[item.id] && (
            <div className="vm-info">
              <p>VM Name: {vmInfoMap[item.id].vmName}</p>
              <p>IP Address: {vmInfoMap[item.id].ip}</p>
            </div>
          )}
        </div>
      ))}

      {/* Модальное окно */}
      {showModal && selectedItem && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>{t(selectedItem.nameKey)}</h3>
            <p>{t(selectedItem.fullDescriptionKey)}</p>

            {/* Форма для ввода параметров */}
            <div className="form-group">
              <label>CPU Count:</label>
              <input
                type="number"
                name="cpuCount"
                value={formValues.cpuCount}
                onChange={handleInputChange}
              />
            </div>
            <div className="form-group">
              <label>RAM (GB):</label>
              <input
                type="number"
                name="ramGb"
                value={formValues.ramGb}
                onChange={handleInputChange}
              />
            </div>
            <div className="form-group">
              <label>Disk Size (GB):</label>
              <input
                type="number"
                name="diskGb"
                value={formValues.diskGb}
                onChange={handleInputChange}
              />
            </div>

            <button onClick={handleSubmit} disabled={isLoading}>
              {isLoading ? <span>Creating VM...</span> : <span>{t('infra_grid.Create')}</span>}
            </button>
            <button onClick={handleCloseModal}>{t('infra_grid.Cancel')}</button>
          </div>
        </div>
      )}

      {/* Глобальный список IP-адресов */}
      {/* {globalIpList.length > 0 && (
        <div className="global-ip-list">
          <h4>Global IP List:</h4>
          <ul>
            {globalIpList.map((ip, index) => (
              <li key={index}>{ip}</li>
            ))}
          </ul>
        </div>
      )} */}
    </div>
  );
};