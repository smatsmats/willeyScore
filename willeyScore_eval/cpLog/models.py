from django.db import models

class ResultsStats(models.Model):
    numb_cars = models.PositiveIntegerField('number of cars')
    numb_scored_cp = models.PositiveIntegerField('number of scored checkpoints')
    numb_abandoned_cp = models.PositiveIntegerField('number of scored checkpoints')
    numb_zeros = models.PositiveIntegerField('number of zerod checkpoints')
    numb_max = models.PositiveIntegerField('number of maxd checkpoints')
    numb_time_allowances = models.PositiveIntegerField('number of T/A\'s')
    def __unicode__(self):
        return self.numb_scored_cp
    
class Event(models.Model):
    name = models.CharField(max_length=60,
                               unique=True)
    start_date = models.DateField()
    results_stats = models.ForeignKey(ResultsStats)
    time_between_cars = models.PositiveIntegerField(default=60) # seconds
    end_date = models.DateField(blank=True,
                               null=True)
    last_modified_date = models.DateField()
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
        return self.name

# most likely loaded from configuration, maybe doesn't need to be in db
class CompClass(models.Model):
    comp_class = models.CharField('class code',
                               max_length=3,
                               primary_key=True)
    class_name = models.CharField('full name of class',
                               unique=20,
                               max_length=20)
    enabled = models.BooleanField('Use this Class',
                               default=True)
    sort_order = models.PositiveIntegerField('order of the classes')
    def __unicode__(self):
        return self.comp_class

class Entrant(models.Model):
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
        return self.number

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

class Leg(models.Model):
    name = models.CharField(max_length=20, 
                               primary_key=True)
    results_stats = models.ForeignKey(ResultsStats)
    event = models.ForeignKey(Event)
    time_between_cars = models.PositiveIntegerField(blank=True,
                               null=True)
    date = models.DateField('Leg date',
                               blank=True,
                               null=True)
    sort_order = models.PositiveIntegerField('ordering of legs',
                               unique=True)
    scoring_rules = models.ForeignKey(ScoringRules)
    def __unicode__(self):
        return self.name
# legs names may be strings with a separate sort order.  
# e.g. for NoAlibi, (name,sort_order) might be ("Saturday",0) and ("Sunday",1)

class Section(models.Model):
    name = models.PositiveIntegerField()
    results_stats = models.ForeignKey(ResultsStats)
    leg = models.ForeignKey(Leg)
    time_between_cars = models.PositiveIntegerField(blank=True,
                               null=True)
    sort_order = models.PositiveIntegerField('ordering of sections in leg')
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
    car_numb = models.ForeignKey(Entrant)
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
    ENTERED = 'E'
    DENY = 'D'
    RETRACTED = 'R'
    STATUS_CHOICES = (
        (ENTERED, 'Entered'),
        (DENY, 'Deny'),
        (RETRACTED, 'Retracted'),
    )
    status = models.CharField(max_length=1,
                                      choices=STATUS_CHOICES,
                                      default=ENTERED)
    def __unicode__(self):
        return self.section
    
class Mark(models.Model):
    cp = models.ForeignKey(Checkpoint)
    car_numb = models.ForeignKey(Entrant)
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
    STATUS_CHOICES = (
        (EARLY, 'Early'),
	(LATE, 'Late'),
        (ZERO, 'Zero'),
    )
    early_late = models.CharField(max_length=1,
                                      choices=STATUS_CHOICES,
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
    use = models.BooleanField('use this time or drop it, allows for Alcan style single score drops',
                               default=True)
    override = models.BooleanField('true if score was manually derived, allows for Alcan style monkeyshines',
                               default=False)
    def __unicode__(self):
        return self.cp


class EntrantResult(models.Model):
    car = models.ForeignKey(Entrant)
    car_number = models.PositiveIntegerField('car number')
    seconds = models.PositiveIntegerField('seconds of adjustment',
                               blank=True,
                               null=True)
    declared = models.TimeField('declared time',
                               blank=True,
                               null=True)
    reason = models.CharField(max_length=60,
                               blank=True,
                               null=True)
    ENTERED = 'E'
    DENY = 'D'
    RETRACTED = 'R'
    STATUS_CHOICES = (
        (ENTERED, 'Entered'),
	(DENY, 'Deny'),
        (RETRACTED, 'Retracted'),
    )
    status = models.CharField(max_length=1,
                                      choices=STATUS_CHOICES,
                                      default=ENTERED)
    def __unicode__(self):
        return self.cp

class EventResults(models.Model):
    event = models.ForeignKey(Event)
    car_numb = models.ForeignKey(Entrant)
    score = models.PositiveIntegerField(blank=True,
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

class LegResults(models.Model):
    leg = models.ForeignKey(Leg)
    car_numb = models.ForeignKey(Entrant)
    score = models.PositiveIntegerField(blank=True,
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
    car_numb = models.ForeignKey(Entrant)
    score = models.PositiveIntegerField(blank=True,
                               null=True)
    zeros = models.PositiveIntegerField()
    sum_of_squares = models.BigIntegerField()
    overall = models.PositiveIntegerField()
    overall_tie = models.BooleanField(default=False)
    overall_tie_broken = models.PositiveIntegerField()
    byclass = models.PositiveIntegerField()
    byclass_tie = models.BooleanField(default=False)
    byclass_tie_broken = models.PositiveIntegerField()
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

