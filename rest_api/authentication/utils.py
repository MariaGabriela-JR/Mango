from .models import BlacklistedToken

def is_token_blacklisted(token):
    return BlacklistedToken.objects.filter(token=token).exists()