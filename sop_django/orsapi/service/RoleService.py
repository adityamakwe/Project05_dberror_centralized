from .BaseService import BaseService
from ..models import Role


class RoleService(BaseService):
    def is_duplicate(self, name, exclude_id=None):
        try:
            qs = Role.objects.filter(name=name)
            if exclude_id:
                qs = qs.exclude(id=exclude_id)
            return qs.exists()

        except Exception as ex:
            self.map_and_throw_exception(ex)

    def search(self, params=None):
        try:
            qs = Role.objects.all()

            if params and params.get("id"):
                qs = qs.filter(id=params["id"])

            return {
                "data": [x.to_json() for x in qs],
                "lastId": qs.last().id if qs.exists() else None
            }
        except Exception as ex:
            self.map_and_throw_exception(ex)

    def get_model(self):
        return Role

# from django.db.utils import OperationalError
# from .BaseService import BaseService
# from ..models import Role
#
#
# class RoleService(BaseService):
#
#     def get_model(self):
#         return Role
#
#     # ---------- DUPLICATE CHECK ---------- #
#
#     def is_duplicate(self, name, exclude_id=None):
#
#         def query():
#             qs = Role.objects.filter(name=name)
#             if exclude_id:
#                 qs = qs.exclude(id=exclude_id)
#             return qs.exists()
#
#         return self._db_execute(query)
#
#     # ---------- SEARCH ---------- #
#
#     def search(self, params):
#
#         def query():
#             qs = Role.objects.all()
#
#             if params.get("id"):
#                 qs = qs.filter(id=params["id"])
#
#             data = [x.to_json() for x in qs]
#             last = qs.last()
#
#             return {
#                 "data": data,
#                 "lastId": last.id if last else None
#             }
#
#         return self._db_execute(query)
#
#     # ---------- GET ---------- #
#
#     def get(self, pk):
#
#         def query():
#             return Role.objects.filter(id=pk).first()
#
#         return self._db_execute(query)
#
#     # ---------- DELETE ---------- #
#
#     def delete(self, pk):
#
#         def query():
#             obj = Role.objects.filter(id=pk).first()
#             if obj:
#                 data = obj.to_json()
#                 obj.delete()
#                 return data
#             return None
#
#         return self._db_execute(query)
#
#     # ---------- PRELOAD ---------- #
#
#     def preload(self):
#
#         def query():
#             return [x.to_json() for x in Role.objects.all()]
#
#         return self._db_execute(query)
#
#
#
#
#
#
#
#
# # from ..models import Role
# # from ..utility.DataValidator import DataValidator
# # from .BaseService import BaseService
# # from django.db import connection
# #
# #
# # class RoleService(BaseService):
# #
# #     def search(self, params):
# #         pageNo = (params['pageNo']) * self.pageSize
# #         sql = 'select * from sos_role where 1=1'
# #         val = params.get('id', None)
# #         if (DataValidator.isNotNull(val)):
# #             sql += " and id = " + val
# #         sql += " limit %s, %s"
# #         print(sql)
# #         cursor = connection.cursor()
# #         cursor.execute(sql, [pageNo, self.pageSize])
# #         result = cursor.fetchall()
# #         columnName = ('id', 'name', 'description')
# #         res = {
# #             "data": [],
# #         }
# #         params["index"] = ((params['pageNo'] - 1) * self.pageSize)
# #         for x in result:
# #             print({columnName[i]: x[i] for i, _ in enumerate(x)})
# #             params['maxId'] = x[0]
# #             res['data'].append({columnName[i]: x[i] for i, _ in enumerate(x)})
# #         return res
# #
# #     def get_model(self):
# #         return Role
