# re defined in baseservice



# from django.db.utils import OperationalError
#
# from sop_django.orsapi.utility.Exceptions import DatabaseUnavailable, ValidationFailed, ResourceNotFound, \
#     ApplicationException
#
#
# def map_and_throw_exception(ex):
#     # Database error
#     if type(ex) == OperationalError:
#         raise DatabaseUnavailable(
#             "Database service is currently unavailable. Please try again later."
#         )
#
#     # Validation error
#     if type(ex) == ValueError:
#         raise ValidationFailed(
#             "Validation failed"
#         )
#
#     # Resource not found
#     if type(ex) == KeyError:
#         raise ResourceNotFound(
#             "Requested resource not found"
#         )
#
#     # Any other error
#     raise ApplicationException(
#         "Unexpected error occurred"
#     )
