import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

#this class has the ability to store images locally and save them for the profile pictures
class TeacherAttachmentStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        # store under <project_root>/group3/teacher_attachments/
        location = os.path.join(settings.BASE_DIR, 'group3', 'teacher_attachments')
        os.makedirs(location, exist_ok=True)
        # serve at /group3/teacher_attachments/
        super().__init__(location=location,
                         base_url='/group3/teacher_attachments/',
                         *args, **kwargs)


teacher_storage = TeacherAttachmentStorage()

