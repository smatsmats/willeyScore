from django.db import models

# used for Event, Leg and Section for holding stats across competitors
class ResultsStats(models.Model):
    numb_cars = models.PositiveIntegerField('number of cars')
    numb_scored_cp = models.PositiveIntegerField('number of scored checkpoints')
    numb_abandoned_cp = models.PositiveIntegerField('number of scored checkpoints')
    numb_zeros = models.PositiveIntegerField('number of zerod checkpoints')
    numb_max = models.PositiveIntegerField('number of maxd checkpoints')
    numb_time_allowances = models.PositiveIntegerField('number of T/A\'s')
    def __unicode__(self):
        return str(self.numb_scored_cp)
    
# Event
class Event(models.Model):
    short_name = models.CharField(max_length=10,
                               unique=True)  # handy name like 2013RD, or 2013NA, or 2013NRWSTR
    name = models.CharField(max_length=60,
                               unique=True)
#    start_date = models.DateField()  ######### remove with next db rebuilt ######
#    end_date = models.DateField(blank=True,
#                               null=True)  ######### remove with next db rebuilt ######
    results_stats = models.ForeignKey(ResultsStats,
                               blank=True,
                               null=True)
    sort_order = models.PositiveIntegerField(default=5) # Some day we mght hav a boat load of events and we might remember their order.
    time_between_cars = models.PositiveIntegerField(default=60) # seconds
    certified_timestamp = models.DateTimeField(blank=True,
                               null=True)
    last_modified_timestamp = models.DateTimeField('change timestamp',
                               blank=True,
                               null=True)
    organizers = models.CharField('organizing club',
                               max_length=60, 
                               blank=True)
    scored_by = models.CharField('scoring team',
                               max_length=60, 
                               blank=True)
    INWORK = 'I'
    PRELIM = 'P'
    CERTIFIED = 'C'
    STATUS_CHOICES = (
        (INWORK, 'InWork'),
        (PRELIM, 'Preliminary'),
        (CERTIFIED, 'Certified'),
    )
    status = models.CharField(max_length=1,
                                      choices=STATUS_CHOICES,
                                      default=INWORK)
    def __unicode__(self):
        return self.short_name

# Classes are DB wide, so not bound to any event.  
# For scoring purposes there is nothing event specific about a class
# all we care about is it has a nice name and we put it in the correct order
# if a car has class X then it must be a correct class
class CompClass(models.Model):
    class_code = models.CharField('class code',
                               max_length=3,
                               unique=True)
    class_name = models.CharField('full name of class',
                               unique=20,
                               max_length=20)
    sort_order = models.PositiveIntegerField('order of the classes')
    def __unicode__(self):
        return self.class_code

# previosly called Entrant
class Car(models.Model):
    number = models.PositiveIntegerField('car number',
                               primary_key=True)
    event = models.ForeignKey(Event)
    names = models.CharField('driver and navigator',
                               max_length=120) # derived
    comp_class = models.ForeignKey(CompClass)
    reg_order = models.PositiveIntegerField('order registration received',
                               unique=True)
    driver = models.CharField(max_length=60)
    navigator = models.CharField(max_length=60)
    vehicle = models.CharField(max_length=60) 
    ACTIVE = 'A'
    DNS = 'S'
    DNF = 'F'
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (DNS, 'Did Not Start'),
        (DNF, 'Did Not Finish'),
    )
    status = models.CharField(max_length=1,
                                      choices=STATUS_CHOICES,
                                      default=ACTIVE)
    def __unicode__(self):
        return self.names

# set of heuristics and limited that constrain the scoring 
# of controls, sections and legs
class ScoringRules(models.Model):
    ruleset = models.CharField('name of rule set', 
                               unique=True,
                               max_length=20)
    max_cp = models.PositiveIntegerField('max score per checkpoint')
    max_section = models.PositiveIntegerField('max score per section', 
                               blank=True,
                               null=True)
    max_leg = models.PositiveIntegerField('max score per leg',
                               blank=True,
                               null=True)
    score_factor = models.FloatField('timing resolution', default=1) # translates seconds of error to  score
    allow_declared_time_at_cp = models.BooleanField(default=False)   # for stop controls
    def __unicode__(self):
        return self.ruleset

# Events hav on more Legs
# Leg names are strings with a separate sort order.  
# e.g. (name,sort_order) might be ("Saturday",0) and ("Sunday",1)
class Leg(models.Model):
    name = models.CharField(max_length=20, 
                               primary_key=True)
    sort_order = models.PositiveIntegerField('ordering of legs',
                               unique=True)
    results_stats = models.ForeignKey(ResultsStats,
                               blank=True,
                               null=True)
    event = models.ForeignKey(Event)
    time_between_cars = models.PositiveIntegerField(blank=True,
                               null=True)
    scoring_rules = models.ForeignKey(ScoringRules)
    def __unicode__(self):
        return self.name

# Legs hav on more Sections
# Section names are strings with a separate sort order.  
# e.g. (name,sort_order) might be ("Mud Mountain",0) and ("Buckley",1)
class Section(models.Model):
    name = models.CharField(max_length=20, 
                               primary_key=True)
    sort_order = models.PositiveIntegerField('ordering of sections in leg',
                               unique=True)
    results_stats = models.ForeignKey(ResultsStats,
                               blank=True,
                               null=True)
    leg = models.ForeignKey(Leg)
    time_between_cars = models.PositiveIntegerField(blank=True,
                               null=True)
    scoring_rules = models.ForeignKey(ScoringRules)
    def __unicode__(self):
        return self.name

class Checkpoint(models.Model):
    cp = models.CharField(max_length=20)
    results_stats = models.ForeignKey(ResultsStats)
    section = models.ForeignKey(Section)
    leg = models.ForeignKey(Leg)
    sort_order = models.PositiveIntegerField('order of the checkpoint, in the section')
    scoring_rules = models.ForeignKey(ScoringRules)
    use = models.BooleanField('use this cp or drop it',
                               default=True)
    distance = models.FloatField(unique=True)  # in section
    crew = models.CharField(max_length=60, blank=True)
    input_by = models.CharField(max_length=60, blank=True)
    input_time = models.TimeField('when it went in',
                               blank=True,
                               null=True)
    auditted_by = models.CharField(max_length=60, blank=True)
    audit_time = models.TimeField('when it was checked',
                               blank=True,
                               null=True)
    car0_perfect = models.TimeField('car 0, perfect time',
                               unique=True)
    adjusted_car0_perfect = models.TimeField('manually adjusted car 0 perfect time',
                               blank=True,
                               null=True)
    bump = models.IntegerField('bump all of the arrival times by n seconds',
                               blank=True,
                               null=True)
    def __unicode__(self):
        return self.cp

class TimeAllowance(models.Model):
    section = models.ForeignKey(Section)
    leg = models.ForeignKey(Leg)
    car_numb = models.ForeignKey(Car)
    distance = models.PositiveIntegerField()
    seconds = models.PositiveIntegerField('seconds of adjustment',
                               blank=True,
                               null=True)
    declared = models.TimeField('declared time',
                               blank=True,
                               null=True)
    reason = models.CharField(max_length=60,
                               blank=True,
                               null=True)
    ACTIVE = 'A'
    DENY = 'D'
    RETRACTED = 'R'
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (DENY, 'Deny'),
        (RETRACTED, 'Retracted'),
    )
    status = models.CharField(max_length=1,
                                      choices=STATUS_CHOICES,
                                      default=ACTIVE)
    def __unicode__(self):
        return self.section
    
class Mark(models.Model):
    cp = models.ForeignKey(Checkpoint)
    car_numb = models.ForeignKey(Car)
    section = models.ForeignKey(Section)
    leg = models.ForeignKey(Leg)
    arrival = models.TimeField('arrival time')
    ta_applied = models.ForeignKey(TimeAllowance,
                               blank=True,
                               null=True)
    declared_time = models.TimeField('competitor declared time',
                               blank=True,
                               null=True)
    use_declared_time = models.BooleanField(blank=False)
    due = models.TimeField('time due')
    absolute_diff = models.TimeField('time diff, absolute value')
    score = models.PositiveIntegerField()
    score_gross = models.PositiveIntegerField('raw score ignoring max or ta')
    EARLY = 'E'
    LATE = 'L'
    ZERO = '-'
    EORL_CHOICES = (
        (EARLY, 'Early'),
	(LATE, 'Late'),
        (ZERO, 'Zero'),
    )
    early_late = models.CharField(max_length=1,
                                      choices=EORL_CHOICES,
                                      blank=True,
                                      null=True)
    use = models.BooleanField('use this time or drop it, allows for Alcan style single score drops',
                               default=True)
    override = models.BooleanField('true if score was manually derived, allows for Alcan style monkeyshines',
                               default=False)
    def __unicode__(self):
        return self.cp

class EventResults(models.Model):
    event = models.ForeignKey(Event)
    car_numb = models.ForeignKey(Car)
    total = models.PositiveIntegerField(blank=True,
                               null=True)
    zeros = models.PositiveIntegerField()
    sum_of_squares = models.BigIntegerField()
    VALUE = 'VAL'
    DNS = 'DNS'
    DNF = 'DNF'
    TYPE_CHOICES = (
        (VALUE, 'Value'),
        (DNS, 'Did Not Start'),
        (DNF, 'Did Not Finish'),
    )
    result_type = models.CharField(max_length=3,
                                      choices=TYPE_CHOICES,
                                      default=VALUE)
    def __unicode__(self):
        return str(self.event)

class LegResults(models.Model):
    leg = models.ForeignKey(Leg)
    car_numb = models.ForeignKey(Car)
    total = models.PositiveIntegerField(blank=True,
                               null=True)
    zeros = models.PositiveIntegerField()
    sum_of_squares = models.BigIntegerField()
    VALUE = 'VAL'
    DNS = 'DNS'
    DNF = 'DNF'
    TYPE_CHOICES = (
        (VALUE, 'Value'),
        (DNS, 'Did Not Start'),
        (DNF, 'Did Not Finish'),
    )
    result_type = models.CharField(max_length=3,
                                      choices=TYPE_CHOICES,
                                      default=VALUE)
    def __unicode__(self):
        return self.leg

class SectionResults(models.Model):
    section = models.ForeignKey(Section)
    leg = models.ForeignKey(Leg)
    car_numb = models.ForeignKey(Car)
    total = models.PositiveIntegerField(blank=True,
                               null=True)
    zeros = models.PositiveIntegerField()
    sum_of_squares = models.BigIntegerField()
    VALUE = 'VAL'
    DNS = 'DNS'
    DNF = 'DNF'
    TYPE_CHOICES = (
        (VALUE, 'Value'),
        (DNS, 'Did Not Start'),
        (DNF, 'Did Not Finish'),
    )
    result_type = models.CharField(max_length=3,
                                      choices=TYPE_CHOICES,
                                      default=VALUE)
    def __unicode__(self):
        return self.section

class CarResults(models.Model):
    car_numb = models.ForeignKey(Car)
    score = models.PositiveIntegerField(blank=True,
                               null=True)
    zeros = models.PositiveIntegerField()
    sum_of_squares = models.BigIntegerField()
    overall = models.PositiveIntegerField()
    overall_tie = models.BooleanField(default=False)
    overall_tie_broken = models.PositiveIntegerField(blank=True,
                               null=True)
    byclass = models.PositiveIntegerField()
    byclass_tie = models.BooleanField(default=False)
    byclass_tie_broken = models.PositiveIntegerField(blank=True,
                               null=True)
    VALUE = 'VAL'
    DNS = 'DNS'
    DNF = 'DNF'
    TYPE_CHOICES = (
        (VALUE, 'Value'),
        (DNS, 'Did Not Start'),
        (DNF, 'Did Not Finish'),
    )
    result_type = models.CharField(max_length=3,
                                      choices=TYPE_CHOICES,
                                      default=VALUE)
    def __unicode__(self):
        return string(self.car_numb)

