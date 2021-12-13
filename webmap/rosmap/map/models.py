from django.db import models

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

class Marker(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    gps = models.CharField(max_length=200)
    image_path = models.CharField(max_length=300)
    marker_type = models.CharField(max_length=100)
    slug = models.SlugField(max_length=230, unique=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status=models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']
    
    def __str__(self):
        return self.name