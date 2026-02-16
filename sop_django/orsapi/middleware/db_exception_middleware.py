# from django.http import JsonResponse
# from django.shortcuts import redirect
# from ..utility.Exceptions import DatabaseUnavailable
#
#
# class DBExceptionMiddleware:
#
#     def __init__(self, get_response):
#         print(">>>>>>>>>>>>>>inside middleware")
#         self.get_response = get_response
#
#     def __call__(self, request):
#         try:
#             return self.get_response(request)
#
#         except DatabaseUnavailable:
#             return JsonResponse(
#                 {
#                     "success": False,
#                     "result": {
#                         "message": "DB Down"
#                     }
#                 },
#                 status=503
#             )
