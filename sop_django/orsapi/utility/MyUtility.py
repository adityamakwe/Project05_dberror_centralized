from django.shortcuts import redirect


class CustomHandle:

    @staticmethod
    def exception_handle():
        return redirect('/orsapi/Error/')