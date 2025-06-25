import React from 'react';
import { useTranslation } from 'react-i18next';

export const UsageRules = () => {
  const { t } = useTranslation(); // Используем хук useTranslation

  return (
    <div className="rules-container">
      {/* Заголовок */}
      <h1 className="rules-title">{t('usage_rules.title')}</h1>

      {/* Основное описание правил */}
      <div className="rules-content">
        {/* Общие правила */}
        <section className="rules-general">
          <h2 className="rules-general-title">{t('usage_rules.general_title')}</h2>
          <p className="rules-general-text">{t('usage_rules.general_text')}</p>
        </section>

        {/* Правила для синей команды */}
        <section className="rules-blue-team">
          <h2 className="rules-blue-team-title">{t('usage_rules.blue_team_title')}</h2>
          <p className="rules-blue-team-text">{t('usage_rules.blue_team_text')}</p>
        </section>

        {/* Правила для красной команды */}
        <section className="rules-red-team">
          <h2 className="rules-red-team-title">{t('usage_rules.red_team_title')}</h2>
          <p className="rules-red-team-text">{t('usage_rules.red_team_text')}</p>
        </section>
      </div>
    </div>
  );
};