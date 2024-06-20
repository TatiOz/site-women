from django import template
# from django.db.models import Count
#
import women.views as views
# from women.models import Category, TagsPosts
# from women.utils import menu
#
register = template.Library()

@register.simple_tag(name='getcats')
def get_categoties():
    return views.cats_db

@register.inclusion_tag('women/list_categories.html')
def show_categories(cat_selected=0):
    cats = views.cats_db
    return {'cats': cats, 'cat_selected': cat_selected}


# @register.inclusion_tag('women/list_tags.html')
# def show_all_tags():
#     return {'tags': TagsPosts.objects.annotate(total=Count("tags")).filter(total__gt=0)}
