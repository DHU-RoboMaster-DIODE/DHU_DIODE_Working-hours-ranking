from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.StudentInformationModel)
admin.site.register(models.TeacherInformationModel)
admin.site.register(models.StudentAwardsRecodeModel)
admin.site.register(models.CollegeModel)
admin.site.register(models.MajorModel)
admin.site.register(models.CourseModel)
admin.site.register(models.ClassModel)
admin.site.register(models.CourseClassModel)
admin.site.register(models.StudentScoreModel)
