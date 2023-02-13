from django_filters import FilterSet
from .models import Post

# class PostFilter(FilterSet):
#     author = ModelChoiceFilter(
#         field_name = 'author',
#         label = 'Author',
#         empty_label = 'любой',
#     )

class PostFilter(FilterSet):
   class Meta:
       model = Post
       fields = {
           'author': ['exact'],
           'title': ['icontains'],
       }