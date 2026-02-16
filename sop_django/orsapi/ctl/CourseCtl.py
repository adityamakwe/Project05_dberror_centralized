import json
from django.http import HttpResponse, JsonResponse
from .BaseCtl import BaseCtl
from .ErrorCtl import ErrorCtl
from django.shortcuts import render
from ..utility.DataValidator import DataValidator
from ..models import Course
from ..service.CourseService import CourseService

class CourseCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id')
        self.form['name'] = requestForm.get('name')
        self.form['description'] = requestForm.get('description')
        self.form['duration'] = requestForm.get('duration')

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.name = self.form['name']
        obj.description = self.form['description']
        obj.duration = self.form['duration']
        return obj

    def model_to_form(self, obj):
        if obj == None:
            return
        self.form['id'] = obj.id
        self.form['name'] = obj.name
        self.form['description'] = obj.description
        self.form['duration'] = obj.duration

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['name'])):
            inputError['name'] = "Course Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['name'])):
                inputError['name'] = "Course Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['description'])):
            inputError['description'] = "Course Description can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['duration'])):
            inputError['duration'] = "Course Duration can not be null"
            self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            course = self.get_service().get(params['id'])
            self.model_to_form(course)
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def save(self, request, params={}):
        try:
            json_request = json.loads(request.body)
            self.request_to_form(json_request)
            res = {"result": {}, "success": True}

            # perform input validation
            if (self.input_validation()):
                res["success"] = False
                res["result"]["inputerror"] = self.form["inputError"]
                return JsonResponse(res)
            #Check unique elements
            pk = int(self.form['id'])
            uniqueAttrib = {"name" : self.form['name']}
            duplicateErrors = self.get_service().mduplicateFields(uniqueAttrib, pk)
            size = len(duplicateErrors)
            if (size > 0):
                res["success"] = False
                res["result"]["inputerror"] = duplicateErrors
                return JsonResponse(res)

            # Add/ Update the user
            course = self.form_to_model(Course())
            self.get_service().save(course)
            res["success"] = True
            res["result"]["data"] = course.id
            res["result"]["message"] = "Course added successfully"
            return JsonResponse(res)

        except Exception as ex:
            return ErrorCtl.handle(ex)

    # def save(self, request, params={}):
    #     try:
    #         json_request = json.loads(request.body)
    #         self.request_to_form(json_request)
    #         res = {"result": {}, "success": True}
    #         if (self.input_validation()):
    #             res["success"] = False
    #             res["result"]["inputerror"] = self.form["inputError"]
    #             return JsonResponse(res)
    #         else:
    #             try:
    #                 if params['id'] > 0:
    #                     pk = params['id']
    #                     # duplicate = self.get_service().get_model().objects.exclude(id=pk).filter(name=self.form['name'])
    #                     duplicate = self.get_service().duplicate(self.form['name'], pk)
    #                     if duplicate:
    #                         res["success"] = False
    #                         res["result"]["message"] = "Course Name already exists"
    #                     else:
    #                         r = self.form_to_model(Course())
    #                         self.get_service().save(r)
    #                         self.form['id'] = r.id
    #                         res["success"] = True
    #                         res["result"]["message"] = "Course updated successfully"
    #                     return JsonResponse(res)
    #                 else:
    #                     # duplicate = self.get_service().get_model().objects.filter(name=self.form['name'])
    #                     duplicate = self.get_service().duplicate(self.form['name'])
    #                     if duplicate:
    #                         res["success"] = False
    #                         res["result"]["message"] = "Course Name already exists"
    #                     else:
    #                         course = self.form_to_model(Course())
    #                         self.get_service().save(course)
    #                         res["success"] = True
    #                         res["result"]["message"] = "Course added successfully"
    #
    #             except Exception as ex:
    #                 return ErrorCtl.handle(ex)
    #         return JsonResponse(res)
    #     except Exception as ex:
    #         return ErrorCtl.handle(ex)

    def search(self, request, params={}):
        try:
            json_request = json.loads(request.body)
            res = {"result": {}, "success": True}
            if (json_request):
                params["name"] = json_request.get("name", None)
                params["pageNo"] = json_request.get("pageNo", None)
            records = self.get_service().search(params)
            if records and records.get("data"):
                res["success"] = True
                res["result"]["data"] = records["data"]
                res["result"]["lastId"] = Course.objects.last().id
            else:
                res["success"] = False
                res["result"]["message"] = "No record found"
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get(self, request, params={}):
        try:
            role = self.get_service().get(params["id"])
            res = {"result": {}, "success": True}
            if (role != None):
                res["success"] = True
                res["result"]["data"] = role.to_json()
            else:
                res["success"] = False
                res["result"]["message"] = "No record found"
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def delete(self, request, params={}):
        try:
            role = self.get_service().get(params["id"])
            res = {"result": {}, "success": True}
            if (role != None):
                self.get_service().delete(params["id"])
                res["success"] = True
                res["result"]["data"] = role.to_json()
                res["result"]["message"] = "Data has been deleted successfully"
            else:
                res["success"] = False
                res["result"]["message"] = "Data was not deleted"
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)
    
    def preload(self, request, params={}):
        try:
            res = {"result": {}, "success": True}
            course_list = CourseService().preload()
            preloadList = []
            for x in course_list:
                preloadList.append(x.to_json())
            res["result"]["courseList"] = preloadList
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get_service(self):
        return CourseService()
