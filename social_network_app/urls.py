from django.contrib import admin
from django.urls import include, path
from authentication.views import UserCreateView, TokenObtainPairView
from authentication.views import create_post, get_user_data,create_post, like_post, unlike_post


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls')),
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('posts/create/', create_post, name='create_post'),
    path('posts/<int:post_id>/like/', like_post, name='like_post'),
    path('posts/<int:post_id>/unlike/', unlike_post, name='unlike_post'),
    path('user/', get_user_data, name='get_user_data'),
]
