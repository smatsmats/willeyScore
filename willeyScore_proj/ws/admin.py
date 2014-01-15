from django.contrib import admin
from ws.models import *

class EventAdmin(admin.ModelAdmin):
    fields = ['name', 'short_name', 'sort_order', 'organizers', 'scored_by', 'status', 'results_stats', 'time_between_cars', 'last_modified_timestamp']
class LegAdmin(admin.ModelAdmin):
    fields = ['name', 'sort_order', 'event', 'scoring_rules', 'time_between_cars', 'results_stats']
    list_display = ('name', 'event')
class SectionAdmin(admin.ModelAdmin):
    fields = ['name', 'sort_order', 'leg', 'scoring_rules', 'time_between_cars', 'results_stats']
    list_display = ('name', 'leg')
class CompClassAdmin(admin.ModelAdmin):
    fields = ['class_code', 'class_name', 'sort_order']

admin.site.register(Event, EventAdmin)
admin.site.register(Leg, LegAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(CompClass, CompClassAdmin)

admin.site.register(Car)
admin.site.register(Mark)
admin.site.register(ScoringRules)
admin.site.register(TimeAllowance)
admin.site.register(Checkpoint)
admin.site.register(ResultsStats)
admin.site.register(SectionResults)
admin.site.register(LegResults)
admin.site.register(EventResults)
admin.site.register(CarResults)
