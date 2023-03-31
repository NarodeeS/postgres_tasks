from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Поле email не может быть пустым! ')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        print('after creating')
        user.set_password(password)
        print('before saving')
        user.save(using=self._db)
        print('saving user')
        return user

    def create_user(self, email, password=None, **extra_fields):
        print('in manager')
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        print('before creation')
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Администратор должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Администратор должен иметь is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
