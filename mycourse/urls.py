from django.contrib import admin
from django.urls import path, include
from .views import BASE, home, about_us, profile, Profile_Update
from .user_login import signup, doLogin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('courses/', include('courses.urls')),
    path('checkout/', include('checkout.urls')),
    path('payment/', include('payment.urls')),
    path('contact_us/', include('contact.urls')),
    path('mycourses/', include('user_course.urls')),
    path('reviews/', include('review.urls')),
    path('base/',BASE,name='base'),
    path('',home,name='home'),
    # path('contact_us/',contact_us,name='contact_us'),
    # path('about_us/',about_us,name='about_us'),
    path('accounts/signup/',signup,name='signup'),
    path('login/',doLogin,name='login'),
    path('accounts/profile/',profile,name='profile'),
    path('profile/update/',Profile_Update,name='profile_update'),
    path('blog/', include('blog.urls')),

    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'app.views.PAGE_NOT_FOUND'
