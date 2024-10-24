from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class WeatherData(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.FloatField()
    feels_like = models.FloatField()
    main_condition = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]


class DailySummary(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    date = models.DateField()
    avg_temperature = models.FloatField()
    max_temperature = models.FloatField()
    min_temperature = models.FloatField()
    dominant_condition = models.CharField(max_length=100)

    class Meta:
        unique_together = ["city", "date"]


class AlertThreshold(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    max_temperature = models.FloatField()
    consecutive_checks = models.IntegerField(default=2)
    is_active = models.BooleanField(default=True)


class Alert(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
