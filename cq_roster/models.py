from django.db import models
from django.db.models.fields import CharField

# Create your models here.


class Katusa(models.Model):
    name = models.CharField(max_length=20)
    eng_name = models.CharField(max_length=20, null=True,blank=True)

    class Rank(models.IntegerChoices):
        PV2 = 1
        PV1 = 2
        CPL = 3
        SGT = 4
    
    class RSO(models.IntegerChoices):
        US = 0
        RSO = 1

    SECTION_NAMES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("E", "E"),
        ("F","F"),
        ("G", "G"),
        ("H", "H"),
        ("I", "I"),
        ("J", "J"),
        ("K", "K"),
        ("L", "L"),
    ]
    section = CharField(choices=SECTION_NAMES, max_length=20, null=True)

    rank = models.IntegerField(choices=Rank.choices)

    is_rso = models.IntegerField(choices=RSO.choices,null=True,blank=True)

    this_duty_dates_score = models.IntegerField(null=True, blank=True)

    total_score = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = [
            "total_score",
        ]

    def __str__(self):
        return f"""
        {self.name}
        """

class OtherDutyDate(models.Model):
    duty_date = models.DateField()

    class DutyType(models.TextChoices):
        HeadCount = 'KP'
        GymGuard = 'GG'

    duty_type = models.CharField(choices = DutyType.choices,max_length=20)   

    class DateScore(models.IntegerChoices):
        WEEKDAY = 1
        OFFDAY = 2

    date_type = models.IntegerField(choices = DateScore.choices)
    worker = models.ForeignKey(
        Katusa,
        on_delete=models.CASCADE,
        null=True,
        related_name="other_duty_dates",
        blank=True,
    )

class DutyDate(models.Model):
    duty_date = models.DateField()

    class DateScore(models.IntegerChoices):
        WEEKDAY_HAS_CCPT = 1
        WEEKDAY = 2
        DEPARTURE = 4
        ARRIVAL = 3
        PASS = 5

    date_score = models.IntegerField(choices=DateScore.choices)

    class Meta:
        abstract = True
        ordering = [
            "duty_date",
        ]

    def __str__(self):
        return f"""
        {self.duty_date}
        """


class ThisDutyDate(DutyDate):
    worker = models.ForeignKey(
        Katusa,
        on_delete=models.CASCADE,
        null=True,
        related_name="this_duty_dates",
        blank=True,
    )

    def to_json(self):
        return {
            "duty_date": self.duty_date.strftime("%Y-%m-%d"),
            "worker": self.worker.name,
            "date_score": self.date_score,
        }


class NextDutyDate(DutyDate):
    worker = models.ForeignKey(
        Katusa,
        on_delete=models.CASCADE,
        null=True,
        related_name="next_duty_dates",
        blank=True,
    )
    def to_json(self):
        try:
            return {
                "duty_date": self.duty_date.strftime("%Y-%m-%d"),
                "worker": self.worker.name,
                "date_score": self.date_score,
            }
        except:
            return {
                "duty_date": self.duty_date.strftime("%Y-%m-%d"),
                "worker": "미정",
                "date_score": self.date_score,
            }

class Leave(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    personnel = models.ForeignKey(
        Katusa,
        on_delete=models.CASCADE,
        null=True,
        related_name="leaves",
        blank=True,
    )

    def __str__(self):
        return f"Leave: {self.start_date} -> {self.end_date}"

class Coefficient(models.Model):
    dates = models.IntegerField()

    rank = models.IntegerField()

    def __str__(self):
        return f"dates:{self.dates}, rank:{self.rank}"
