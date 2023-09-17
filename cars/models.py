from django.db import models
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
# Create your models here.
from PIL import Image
class Car(models.Model):
    pic = models.ImageField(null= True, blank=True, upload_to='cars/')
    def save(self):
        img=Image.open(self.pic)
        output = BytesIO()
        oldwidth, oldheight = img.size
        aspectratio = round(oldwidth/oldheight)
        newheight=150
        newwidth=aspectratio*newheight
        img = img.resize((newwidth, newheight))
        img.save(output, format="JPEG", quality=90)
        output.seek(0)
        self.pic = InMemoryUploadedFile(output, 'Imagefield', f"{self.pic.name.split('.')[0]}.jpg", 'image/jpeg', sys.getsizeof(output),None)
        super(Car, self).save()