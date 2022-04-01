from django.shortcuts import render


def page_not_found(request, exception):
    context = {
        'path': request.path,
        'title': 'Custom 404'
    }
    template = 'core/404.html'
    return render(
        request,
        template,
        context,
        status=404
    )


def server_error(request):
    template = 'core/500.html'
    context = {
        'title': 'Custom 500'
    }
    return render(request, template, context, status=500)


def permission_denied(request, exception):
    template = 'core/403.html'
    context = {
        'title': 'Custom 403'
    }
    return render(request, template, context, status=403)


def csrf_failure(request, reason=''):
    template = 'core/403csrf.html'
    context = {
        'title': 'Custom CSRF check error'
    }
    return render(request, template, context)
