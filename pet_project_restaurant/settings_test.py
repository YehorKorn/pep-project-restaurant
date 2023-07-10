from django.conf import settings


# Using MemoryStorage instead of FileSystemStorage for tests
settings.DEFAULT_FILE_STORAGE = 'django.core.files.storage.InMemoryStorage'
