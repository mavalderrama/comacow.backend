from django.db import models

class Farm(models.Model):
    id_farm = models.PositiveIntegerField(primary_key=True)
    n_cow   = models.PositiveIntegerField()
    n_bull  = models.PositiveIntegerField()
    n_calf  = models.PositiveIntegerField()
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    id_user = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return str(self.id_farm)

class Livestock(models.Model):
    id_animal    = models.PositiveIntegerField(primary_key=True)
    animal_type  = models.CharField(max_length=264)
    status       = models.CharField(max_length=264)
    id_farm      = models.ForeignKey(Farm, on_delete= models.CASCADE)
    name_cow     = models.CharField(max_length=264)
    price        = models.DecimalField(max_digits=10, decimal_places=2)
    raze         = models.CharField(max_length= 264)
    weigth       = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name_cow

class Middleman_order(models.Model):
    id_order = models.PositiveIntegerField(primary_key=True)
    status = models.CharField(max_length=264)
    details = models.CharField(max_length=264)
    id_user = models.ForeignKey(User, on_delete= models.CASCADE)
    id_animal = models.ForeignKey(Livestock, on_delete= models.CASCADE)

    def __str__(self):
        return str(self.id_order)

class Custumer_order(models.Model):
    id_order = models.PositiveIntegerField(primary_key=True)
    status = models.CharField(max_length=264)
    details = models.CharField(max_length=264)
    id_user = models.ForeignKey(User, on_delete= models.CASCADE)
    id_animal = models.ForeignKey(Livestock, on_delete= models.CASCADE)

    def __str__(self):
        return str(self.id_order)


