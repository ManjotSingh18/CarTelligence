from typing import Any
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from cars.models import Car
from .forms import CarForm 
from django.http import HttpResponseRedirect
import os 
from main import activate
import time 
import glob
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def home(request):
    try:
        if request.method == "POST":
            form= CarForm(request.POST, auto_id="Placer")
            if form.is_valid():
                files = request.FILES
                image = files.get("pic")
                instance = Car()
                instance.pic = image
                if 'media' in os.listdir(".") and len(os.listdir("./media/cars/")) >= 1:
                    files = glob.glob('./media/cars/*')
                    for f in files:
                        os.remove(f)
                instance.save()
                time.sleep(2)
                try:
                    filename=os.listdir("./media/cars/")[0]
                except:
                    return render(request, "cars/landing.html", {"form": form, "prediction": "", "error": "File not given or not .JPG"})
                if (filename[-3:] == "jpg" or filename[-3:]=="JPG" or filename[-4:] == "jpeg" or filename[-4:] == "JPEG") and ('media' in os.listdir(".") and len(os.listdir("./media/cars/")) >= 1):
                    p=activate(f"./media/cars/{filename}")
                    return render(request, "cars/carpred.html", {"pico": filename, "car": p})
                else:
                    return render(request, "cars/landing.html", {"form": form, "prediction": "", "error": "File not given or not .JPG"})

        else:
            form = CarForm(auto_id="Placer")
            return render(request, "cars/landing.html", {"form": form, "prediction": "", "error": ""})
    except:
        return render(request, "cars/error.html", {})




    