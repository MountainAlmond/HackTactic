//подключение библиотек

import * as React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

//подключение модулей
import { I18nextProvider } from 'react-i18next';
import i18next from 'i18next';
import { NavBar } from './components/NavBar';
import { AuthPage } from './components/AuthPage';
import { PrivateRoute } from './components/PrivateRoute';
import { InfraGrid } from './components/InfraGrid';
import { AttackScriptsGrid } from './components/AttackGrid';
import { SystemDescription } from './components/Description';
import { UsageRules } from './components/UsageRules';
import { CreateUserForm } from './components/CreateForm';
// import  { RegToVoitingPage } from './pages/RegToVoitingPage';
// import  { VotePage } from './pages/VotePage';
// import  { VoitingResultsPage } from './pages/VoitingResultsPage';
// import  { VoiceCheckPage } from './pages/VoiceCheckPage';


// import { EntityList } from './components/EntityList';

//подключение объектов описания инфраструктур и скриптов атак
import { infrastructureItems } from './common/inftaItems';
import { attackScripts } from './common/attackItems';



//подключение стилей компонентов

import './components/styles/LoginForm.css';
import './components/styles/NavBar.css';
import './components/styles/Wallpaper.css';
import './components/styles/FormBackend.css';
import './components/styles/Carousel.css';
import './components/styles/UserComponent.css';
import './components/styles/LangSwitcher.css';
import './components/styles/AuthForm.css';
import './components/styles/InfraGrid.css';
import './components/styles/AttackGrid.css';
import './components/styles/Description.css';
import './components/styles/CreateForm.css';
import './components/styles/UsageRules.css';





//общие стили
import './common/commonStyles/CommonBackground.css';
// import i18next from 'i18next';

// import { initReactI18next } from 'react-i18next';
// import HttpBackend from 'i18next-http-backend';
// import Backend from 'i18next-fs-backend';
// import LanguageDetector from 'i18next-browser-languagedetector';



//Придумать потом, как использовать i18n с подгрузкой json по компонентам с http
// i18next
// .use(HttpBackend)
// .use(initReactI18next)
// .init({
//   fallbackLng: 'ru', // Язык по умолчанию
//   debug: true,
//   interpolation: {
//     escapeValue: false, // react уже безопасен от XSS
//   },
//   backend: {
//     loadPath: '/locales/{{lng}}/{{ns}}.json', // Путь к файлам с переводами
//   },
// });





class App extends React.Component<{}, {}> {
    render() {
        // Проверяем наличие JWT-токена
        const token = localStorage.getItem('jwtToken'); // Или sessionStorage.getItem('jwtToken')
    
        return (
          <I18nextProvider i18n={i18next}>
            {token ? (
              // Если токен есть, отображаем основное приложение
              <BrowserRouter basename="/">
                <div className="app-container">
                  <NavBar />
                  <div className="container">
                    <Routes>
                      <Route element={<PrivateRoute />}>
                      <Route path="/infra-models" element={<InfraGrid items={infrastructureItems} />} />
                      <Route path="/attacks" element={<AttackScriptsGrid items={attackScripts} />} />
                      <Route path="/create-user" element={<CreateUserForm />} />
                      <Route path="/about-system" element={<SystemDescription />} />
                      <Route path="/rules" element={<UsageRules />} />
                      </Route>
                      {/* Перенаправление на главную страницу для несуществующих маршрутов */}
                        <Route path="*" element={<Navigate to="/attacks" />} />
        
                    </Routes>
                  </div>
                </div>
                
              </BrowserRouter>
            ) : (
              // Если токена нет, отображаем форму авторизации
              <div className="wallpaper">
                <AuthPage />
              </div>
              // <SystemDescription />
            )}
          </I18nextProvider>
        );
      }
    }
    
    export default App;
