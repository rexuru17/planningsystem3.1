from django.db import models

# Create your models here.
class CSVFile(models.Model):
    csv_file = models.FileField(upload_to='tmp_data', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f"File ID: {self.id}"
