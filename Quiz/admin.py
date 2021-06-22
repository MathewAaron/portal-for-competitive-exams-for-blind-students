from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin
from .models import Question

admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    list_display = ('course','marks','question','option1','option2','option3','option4','answer')