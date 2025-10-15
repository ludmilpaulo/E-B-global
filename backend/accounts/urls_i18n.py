from django.urls import path
from .views import I18nView

urlpatterns = [
    path('<str:language>/', I18nView.as_view(), name='i18n_translations'),
]
