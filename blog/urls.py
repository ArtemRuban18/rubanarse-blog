from django.urls import path
import blog.views as views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'), 
    path('post/<slug:slug>/', views.detail_post, name = 'detail_post'), 
    path('post-by-category/<slug:slug>', views.post_by_category, name='post_by_category'),
    path('post-by-author/<str:username>/', views.post_by_author, name='post_by_author'),
    path('create-post/',views.create_post, name='create_post' ),
    path('edit-post/<slug:slug>', views.edit_post, name = 'edit_post'),
    path('delete-post/<int:pk>', views.delete_post, name = 'delete_post'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
