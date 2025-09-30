# models.py
class DataUsage(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service_plan = models.ForeignKey(ServicePlan, on_delete=models.CASCADE)
    data_used = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # in GB
    data_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # in GB
    usage_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-usage_date']
    
    def __str__(self):
        return f"{self.client.username} - {self.data_used}GB"