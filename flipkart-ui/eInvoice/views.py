from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import csv
import os

# Create your views here.
def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url=os.path.abspath(filename)
        return render(request, 'eInvoice/home.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'eInvoice/home.html')

def analyze(request):
    dir_path=os.path.dirname(os.path.abspath(__file__))+r"/extract.py"
    exec(open(dir_path).read())
    return redirect('homepage')
    
def download(request):
    dir_path="Invoice_output1.csv"
    with open(dir_path) as myfile:
        response = HttpResponse(myfile, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Invoice_output.csv'
        return response
