from abc import ABC, abstractmethod
from django.db.utils import OperationalError

from ..utility.ApplicationException import ApplicationException



class BaseService(ABC):

    def __init__(self):
        self.pageSize = 5

    def map_and_throw_exception(self,ex):

        print(">>>>>>>>>>>>>>>>inside map and throw method")
        # Database error
        if type(ex) == OperationalError:
            raise ApplicationException(
                "Database service is currently unavailable. Please try again later."
            )
        else:
            raise ApplicationException(
            "Unexpected error occurred"
            )

    def save(self, obj):
        try:
            if obj.id == 0:
                obj.id = None
            obj.save()
            return obj

        except Exception as ex:
            self.map_and_throw_exception(ex)


    def delete(self, obj_id):
        try:
            obj = self.get(obj_id)
            if obj:
                obj.delete()
                return True
            return False
        except Exception as ex:
            self.map_and_throw_exception(ex)

    def get(self, obj_id):
        Model = self.get_model()
        try:
            return Model.objects.get(id=obj_id)
        except Exception as ex:
            self.map_and_throw_exception(ex)

    def search(self):
        try:
            return self.get_model().objects.all()
        except Exception as ex:
            self.map_and_throw_exception(ex)

    def preload(self):
        Model = self.get_model()
        try:
            return Model.objects.all()
        except Exception as ex:
            self.map_and_throw_exception(ex)

    #Check   unique key
    # def duplicateFields(self, field_name, name, exclude_id=None):
    #     try:
    #         qs = self.get_model().objects.filter(**{field_name: name})
    #         # qs = self.get_model().objects.filter(name=name)
    #         if exclude_id:
    #             qs = qs.exclude(id=exclude_id)
    #         return qs.exists()
    #     except Exception as ex:
    #         self.map_and_throw_exception(ex)

    def mduplicateFields(self, dict, exclude_id=None):
        error = {}
        try:
            for uniquekey in dict:
                qs = self.get_model().objects.filter(**{uniquekey: dict[uniquekey]})
                if exclude_id and exclude_id>0 :
                    qs = qs.exclude(id=exclude_id)
                if qs.exists():
                    error[uniquekey] =  dict[uniquekey] + " is duplicate"
            return error
        except Exception as ex:
            self.map_and_throw_exception(ex)

    @abstractmethod
    def get_model(self):
        pass


# from django.db.utils import OperationalError
# from abc import ABC, abstractmethod
#
# from ..utility.ApplicationException import ApplicationException
# from ..utility.Exceptions import DatabaseUnavailable
#
# class BaseService(ABC):
#
#     def __init__(self):
#         self.pageSize = 5
#
#     def handle_and_throw(ex: Exception):
#         ex_type = type(ex)
#
#         # You can customize messages per exception type
#         if isinstance(ex, ValueError):
#             msg = f"Invalid value provided: {ex}"
#         elif isinstance(ex, KeyError):
#             msg = f"Missing key error: {ex}"
#         elif isinstance(ex, OperationalError):
#             msg = "Database is not available, try after sometimes"
#         else:
#             msg = f"Unhandled exception of type {ex_type.__name__}: {ex}"
#         # Raise your custom exception
#         raise ApplicationException(msg, ex)
#
#     def save(self, obj):
#         try:
#             if obj.id == 0:
#                 obj.id = None
#             return (obj.save)
#         except Exception as ex:
#            self.handle_and_throw(ex)
#
#     def delete(self, obj_id):
#         obj = self.get(obj_id)
#         if obj:
#             return (obj.delete)
#         return None
#
#     def get(self, obj_id):
#         try:
#             return (
#                 self.get_model()
#             )
#         except self.get_model().DoesNotExist:
#             return None
#
#     def search(self):
#         return (
#             self.get_model().objects.all
#         )
#
#     def preload(self):
#         return (
#             self.get_model().objects.all
#         )
#
#     @abstractmethod
#     def get_model(self):
#         pass