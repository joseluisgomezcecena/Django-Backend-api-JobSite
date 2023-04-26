from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    exception_class = exc.__class__.__name__

    print(exception_class)

    if exception_class == 'AuthenticationFailed':
        response.data = {
            "detail": "Incorrect authentication credentials."
        }
        response.status_code = 401

    if exception_class == 'NotLoggedIn':
        response.data = {
            "detail": "Not Logged In."
        }
        response.status_code = 401

    if exception_class == 'NotAuthenticated':
        response.data = {
            "detail": "Not Authenticated, please login first."
        }
        response.status_code = 401

    if exception_class == 'PermissionDenied':
        response.data = {
            "detail": "Permission Denied."
        }
        response.status_code = 403

    return response
