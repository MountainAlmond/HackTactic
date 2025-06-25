import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import apiClient from '../common/apiClient';
import { useTranslation } from 'react-i18next';

interface CreateUserFormValues {
  username: string;
  password: string;
}

export const CreateUserForm: React.FC = () => {
  const { t } = useTranslation();

  // Валидация формы
  const validationSchema = Yup.object().shape({
  username: Yup.string()
    .required(t('create_user_form.Username_is_req'))
    .min(3, t('create_user_form.Username_min_length')),
  password: Yup.string()
    .required(t('create_user_form.Password_is_req'))
    .min(8, t('create_user_form.Password_min_length')),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref('password'), undefined], t('create_user_form.Passwords_must_match')) // Исправление здесь
    .required(t('create_user_form.Confirm_password_is_req')),
});

  // Обработчик отправки формы
  const handleSubmit = async (values: CreateUserFormValues) => {
    try {
      // Отправляем данные на бэкенд
      await apiClient.post('/admin/create-user', values);

      // Уведомление об успешной регистрации
      alert(t('create_user_form.User_created_success'));

      // Очистка формы
      window.location.reload();
    } catch (error: any) {
      console.error('Error:', error.response?.data?.msg || 'Unknown error');
      alert(error.response?.data?.msg || t('create_user_form.Unknown_error'));
    }
  };

  return (
    <div className="create-user-form">
      <h2>{t('create_user_form.Create_User')}</h2>
      <Formik
        initialValues={{
          username: '',
          password: '',
          confirmPassword: '',
        }}
        validationSchema={validationSchema}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting }) => (
          <Form>
            <div className="input-group">
              <label>{t('create_user_form.Username')}</label>
              <Field type="text" name="username" className="input" />
              <ErrorMessage name="username" component="div" className="error" />
            </div>
            <div className="input-group">
              <label>{t('create_user_form.Password')}</label>
              <Field type="password" name="password" className="input" />
              <ErrorMessage name="password" component="div" className="error" />
            </div>
            <div className="input-group">
              <label>{t('create_user_form.Confirm_password')}</label>
              <Field type="password" name="confirmPassword" className="input" />
              <ErrorMessage name="confirmPassword" component="div" className="error" />
            </div>
            <button type="submit" className="button-submit" disabled={isSubmitting}>
              {t('create_user_form.Submit')}
            </button>
          </Form>
        )}
      </Formik>
    </div>
  );
};