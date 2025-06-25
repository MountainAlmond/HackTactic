import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

export const PrivateRoute: React.FC = () => {
  const token = localStorage.getItem('jwtToken'); // Проверяем наличие JWT-токена

  if (!token) {
    // Если токена нет, перенаправляем на страницу входа
    return <Navigate to="/" />;
  }

  // Если токен есть, отображаем дочерние компоненты
  return <Outlet />;
};

