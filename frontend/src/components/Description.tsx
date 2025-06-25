import React from 'react';
import { useTranslation } from 'react-i18next';

export const SystemDescription = () => {
  const { t } = useTranslation();

  return (
    <div className="description-container">
      {/* Заголовок */}
      <h1 className="description-title">{t('system_description.title')}</h1>

      {/* Основное описание системы */}
      <div className="description-content">
        <section className="description-purpose">
          <h2 className="description-purpose-title">{t('system_description.purpose')}</h2>
          <p className="description-purpose-text">{t('system_description.purpose_text')}</p>
        </section>

        {/* Основные возможности */}
        <section className="description-features">
          <h2 className="description-features-title">{t('system_description.features')}</h2>
          <div className="description-feature description-feature-blue">
            <img
              src="/assets/blue.jpg"
              alt={t('system_description.blue_team_training')}
              className="description-feature-image"
            />
            <div className="description-feature-text">
              <h3 className="description-feature-title">{t('system_description.blue_team_training')}</h3>
              <span className='highlight-blue'>{t('system_description.blue_team_desc')}</span>
            </div>
          </div>
          <div className="description-feature description-feature-red">
            <img
              src="/assets/red.jpg"
              alt={t('system_description.red_team_training')}
              className="description-feature-image"
            />
            <div className="description-feature-text">
              <h3 className="description-feature-title">{t('system_description.red_team_training')}</h3>
              <span className='highlight-red'>{t('system_description.red_team_desc')}</span>
            </div>
          </div>
        </section>

        {/* Раздел о разработчике*/}
        <section className="description-contributors">
          <h2 className="description-contributors-title">{t('system_description.contributors_title')}</h2>
          <p className="description-contributors-text">
          </p>
          <ul className="description-contributors-list">
            <li>{t('system_description.developer')}</li>
          </ul>
        </section>
      </div>
    </div>
  );
};