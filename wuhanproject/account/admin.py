from django.contrib import admin
from .models import Account # MyAccountManager 는 Account를 만들기 위한 것이니 필요 없다.
# Register your models here.

admin.site.register(Account)
