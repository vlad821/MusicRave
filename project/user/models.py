import datetime
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", 1)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20, default=None)
    last_name = models.CharField(max_length=20, default=None)
    email = models.EmailField(max_length=100, unique=True, default=None)
    password = models.CharField(default=None, max_length=255)
    bio = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(editable=False, auto_now=datetime.datetime.now())

    USERNAME_FIELD = "email"
    objects = UserManager()

    def __str__(self):
        return f"'id': {self.id}, 'first_name': '{self.first_name}', 'last_name': '{self.last_name}', 'email': '{self.email}', 'created_at': {int(self.created_at.timestamp())}"

    def __repr__(self):
        return f"{User.__name__}(id={self.id})"

    @staticmethod
    def get_by_id(user_id):
        custom_user = User.objects.filter(id=user_id).first()
        return custom_user if custom_user else None

    @staticmethod
    def get_by_email(email):
        custom_user = User.objects.filter(email=email).first()
        return custom_user if custom_user else None

    @staticmethod
    def delete_by_id(user_id):
        user_to_delete = User.objects.filter(id=user_id).first()
        if user_to_delete:
            User.objects.filter(id=user_id).delete()
            return True
        return False

    @staticmethod
    def create(email, password, first_name=None, last_name=None):
        if (
            len(first_name) <= 20
            and len(last_name) <= 20
            and len(email) <= 100
            and len(email.split("@")) == 2
            and len(User.objects.filter(email=email)) == 0
        ):
            custom_user = User(
                email=email,
                password=make_password(password),
                first_name=first_name,
                last_name=last_name,
            )
            custom_user.save()
            return custom_user
        return None

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": f"{self.first_name}",
            "last_name": f"{self.last_name}",
            "email": f"{self.email}",
            "created_at": int(self.created_at.timestamp()),
        }

    def update(
        self,
        first_name=None,
        last_name=None,
        password=None,
        bio=None,
    ):
        user_to_update = User.objects.filter(email=self.email).first()
        if first_name != None and len(first_name) <= 20:
            user_to_update.first_name = first_name
        if last_name != None and len(last_name) <= 20:
            user_to_update.last_name = last_name
        if bio != None and len(bio) <= 500:
            user_to_update.bio = bio
        if password != None:
            user_to_update.set_password(password)
        user_to_update.save()

    @staticmethod
    def get_all():
        return User.objects.all()
