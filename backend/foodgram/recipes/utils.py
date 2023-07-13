from django.core.paginator import Paginator


def paginatored(posts, counts_posts, request):
    pages = Paginator(posts, counts_posts)
    page_number = request.GET.get('page')
    page_obj = pages.get_page(page_number)
    return page_obj