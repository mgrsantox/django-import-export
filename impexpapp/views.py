from django.views.generic import View
from . models import Student
from django.contrib import messages
from django.shortcuts import render, HttpResponse
import csv
import io
# Create your views here.


class BulkStudentImportView(View):
    template_name = 'upload.html'

    def get(self, request, *args, **kwargs):
        students = Student.objects.all()
        return render(request, self.template_name, {"students":students})

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES['file']
        print(csv_file.name)
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File Must be in CSV Format')
        else:
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for col in csv.reader(io_string, delimiter=',', quotechar="|"):
                obj, created = Student.objects.update_or_create(
                    first_name=col[0], last_name=col[1], address=col[2], age=col[3], email=col[4])
        students = Student.objects.all()
        return render(request, self.template_name, {"students":students})


class BulkStudentExportView(View):
    def get(self, request, *args, **kwargs):
        students = Student.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="student.csv"'
        writer = csv.writer(response, delimiter=',')
        writer.writerow(['first_name', 'last_name', 'address', 'age', 'email'])
        for obj in students:
            writer.writerow([obj.first_name, obj.last_name, obj.address, obj.age, obj.email])
        return response