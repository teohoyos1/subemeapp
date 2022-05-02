from django.db import models

# Create your models here CREADOTEO
class Fi_file_type(models.Model):
    name = models.CharField(max_length=250) #foruser
    isActive = models.IntegerField(default=0) #interno

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name',)
        # verbose_name = 'File_type'
        # verbose_name_plural = 'File_types'
        # db_table = 'fi_File_type'
        # ordering = ['name','isActive']


class Fi_file(models.Model):
    fileType = models.ForeignKey(Fi_file_type, verbose_name='Grupo:', help_text="Seleccione...", on_delete=models.CASCADE)
    fileTypeName = models.CharField(max_length=250, verbose_name='Nombre de Documento:',help_text='Prueba texto')
    fileDescription = models.TextField(verbose_name='Descripción de archivo:',blank=True,null=True) #foruser
    files = models.FileField(upload_to='docs/',null=True, blank=True,verbose_name='Archivo:') #interno JSON and foruser
    modified_date = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        self.files.delete()
        super().delete(*args, **kwargs)