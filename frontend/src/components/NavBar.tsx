import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { LanguageSwitcher } from './LangSwitcher';
import { UserComponent } from './UserComponent';

interface IProps {}

const supportedLanguages = {
  en: { label: 'English', flag: './assets/flags/en.png' },
  ru: { label: 'Русский', flag: './assets/flags/ru.png' },
  /* add more languages as needed */
};

export const NavBar: React.FC<IProps> = () => {
  const { t } = useTranslation();
  const [isPopupOpen, setIsPopupOpen] = useState(false); // Состояние для попапа

  const handleLogout = () => {
    console.log('Пользователь вышел из приложения');
  };

  const openPopup = () => {
    setIsPopupOpen(true); // Открываем попап
  };

  const closePopup = () => {
    setIsPopupOpen(false); // Закрываем попап
  };

  // const redirectToSIEM = () => {
  //   window.open('http://192.168.0.105:5601/', '_blank'); // Перенаправляем в SIEM
  //   closePopup(); // Закрываем попап после подтверждения
  // };
  const username = localStorage.getItem('username');
  const jwt = localStorage.getItem('jwtToken');

  return (
    <div>
      <nav className="top-menu">
        {/* Левая часть меню */}
        <div>
          <ul className="menu-main">
            <img src="./assets/logo.png" alt="Логотип приложения" className="logo" />
            <li>
              <Link to="/infra-models">{t('navbar.InfraModels')}</Link>
            </li>
            <li>
              <Link to="/attacks">{t('navbar.Attacks')}</Link>
            </li>
            <li>
              {/* <a href="#" onClick={openPopup}>
                {t('navbar.SIEM')}
              </a> */}
            </li>
            {/* Дополнительный пункт меню для администратора */}
            {username === 'admin' && jwt!= '' && (
              <li>
                <Link to="/create-user">{t('navbar.Create_user')}</Link>
              </li>
            )}

            <li>
              <Link to="/about-system">{t('navbar.about')}</Link>
            </li>
            <li>
              <Link to="/rules">{t('navbar.rules')}</Link>
            </li>
          </ul>
        </div>

        {/* Правая часть меню */}
        <div className="menu-right">
          <div>
            <LanguageSwitcher supportedLanguages={supportedLanguages} />
          </div>
          <div>
            <UserComponent userName={localStorage.getItem('username')} onLogout={handleLogout} />
          </div>
        </div>
      </nav>

      {/* Попап для подтверждения перехода в SIEM
      {isPopupOpen && (
        <div className="popup-overlay">
          <div className="popup-content">
            <h3>{t('popup_redirect.Confirm')}</h3>
            <p>{t('popup_redirect.Message')}</p>
            <div className="popup-buttons">
              <button className="popup-button confirm" onClick={redirectToSIEM}>
                {t('popup_redirect.Y')}
              </button>
              <button className="popup-button cancel" onClick={closePopup}>
                {t('popup_redirect.N')}
              </button>
            </div>
          </div>
        </div>
      )} */}
    </div>
  );
};