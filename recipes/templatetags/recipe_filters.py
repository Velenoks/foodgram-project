from django import template


register = template.Library()


@register.filter(name='get_filter_values')
def get_filter_values(value):
    return value.getlist('tag')

@register.filter(name="get_filter_link")
def get_filter_link(request, tag):
    new_request = request.GET.copy()
    tags = new_request.getlist('tag')
    if tag in tags:
        tags.remove(tag)
    else:
        tags.append(tag)
    if new_request.__contains__('page'):
        new_request.pop('page')
    new_request.setlist('tag', tags)
    return new_request.urlencode()

@register.filter(name='construct_page_link')
def construct_page_link(request, page: int):
    new_request = request.GET.copy()
    new_request.setlist('page', [str(page)])
    return new_request.urlencode()
