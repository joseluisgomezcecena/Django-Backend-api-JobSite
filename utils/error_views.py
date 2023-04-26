from django.http import JsonResponse


def handler500(request):
    return JsonResponse({'error': 'Internal Server Error.'}, status=500)


def handler404(request, exception):
    return JsonResponse({'error': 'Route not found.'}, status=404)
