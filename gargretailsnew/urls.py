"""gargretailsnew URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import home.views
import stocks.views
import purchase.views
import reports.views
import returns.views
urlpatterns = [
   url(r'^admin/', admin.site.urls),
	url(r'^home/',home.views.home),
	url(r'^landing/',home.views.landing),
	url(r'^stocks/',stocks.views.stocklanding),
	url(r'^purchase/',purchase.views.purchase),
	url(r'^Reports/',reports.views.reportshome),
	url(r'^returns/',returns.views.rethome),
	url(r'^sync/',home.views.sync),
	
]
