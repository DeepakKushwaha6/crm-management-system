from django.contrib import admin
from .models import Lead, Customer, Opportunity, Task, Activity, Document, CalendarEvent

admin.site.register(Lead)
admin.site.register(Customer)
admin.site.register(Opportunity)
admin.site.register(Task)
admin.site.register(Activity)
admin.site.register(Document)
admin.site.register(CalendarEvent)
