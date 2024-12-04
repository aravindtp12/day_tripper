from django.contrib import admin
from .models import TravelPlan

@admin.register(TravelPlan)
class TravelPlanAdmin(admin.ModelAdmin):
    list_display = ('destination', 'start_date', 'end_date', 'created_at')
    list_filter = ('destination', 'start_date')
    search_fields = ('destination',)
