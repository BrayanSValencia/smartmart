from django.db import models
from django.utils import timezone

class BlacklistedAccessToken(models.Model):
    token = models.TextField()
    blacklisted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()  
    
    def is_expired(self):
        return timezone.now() >= self.expires_at
    
    class Meta:
        db_table = 'BlacklistedAccessToken'