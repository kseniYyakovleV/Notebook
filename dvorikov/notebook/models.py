from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils.timezone import localtime, datetime
import pytz
# Create your models here.

class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")
    title = models.CharField(verbose_name="Название", max_length=20, null=False)
    choices = {"d": "Обычная", "i": "Важная"}
    english_choices = {"d": "default", "i": "important"}
    category = models.CharField(verbose_name="Категория", choices=choices, default="d", max_length=1)
    start_datetime = models.DateTimeField(verbose_name="Время начала")
    end_datetime = models.DateTimeField(verbose_name="Время конца")
    task_description = models.TextField(verbose_name="Описание задачи")
    is_periodic = models.BooleanField(verbose_name="Является периодической")
    last_execution = models.DateTimeField(verbose_name="Последнее выполнение", default= None, null=True)

    class Meta:
        unique_together = ("owner", "title")
        ordering = ["-id"]

    def complete(self)->bool:
        now = datetime.now().replace(tzinfo=pytz.timezone("Europe/Moscow")) - timedelta(0, 0, 0, 0, 30, 0, 0)
        self.last_execution = now
        self.save()
        if self.is_periodic:
            period = Period.objects.get(task = self)
            period.execution_count+=1
            period.save()


        return True

    def not_complete(self)->bool:
        self.last_execution = None
        self.save()
        return True

    def get_short_info(self)-> dict:
        """
        return main information about compliting the task
        status: ahead/current/completed/failed
        """

        now = datetime.now().replace(tzinfo=pytz.timezone("Europe/Moscow")) - timedelta(0, 0, 0, 0, 30, 0, 0)

        if self.is_periodic:
            if self.end_datetime <= now:
                result = ("completed", "Конец", self.end_datetime)
            else:
                period = Period.objects.get(task = self)
                period_duration = timedelta(period.period_duration,0,0,0,0,0,0)
                execution_duration = timedelta(period.execution_duration,0,0,0,0,0,0)
                next_period_start = self.start_datetime
                while next_period_start < now:
                    next_period_start+= period_duration
                current_period_start = next_period_start - period_duration
                current_period_end = current_period_start + execution_duration

                if self.last_execution:
                    if self.last_execution < current_period_start:
                        if now >= current_period_end:
                            if next_period_start >= self.end_datetime:
                                result = ("completed", "Конец", current_period_end)
                            else:
                                result = ("ahead", "Начало", next_period_start)
                        else:
                            result = ("current", "Конец", current_period_end)
                    else:
                        if next_period_start >= self.end_datetime:
                            result = ("completed", "Конец", current_period_end)
                        else:
                            result = ("ahead", "Начало", next_period_start)
                else:
                    if now >= current_period_end:
                        if next_period_start >= self.end_datetime:
                            result = ("completed", "Конец", current_period_end)
                        else:
                            result = ("ahead", "Начало", next_period_start)
                    else:
                        result = ("current", "Конец", current_period_end)
    
        else:
            if self.last_execution and self.last_execution:
                result = ("completed", "Конец", self.last_execution)
            elif now > self.end_datetime:
                result = ("failed", "Конец", self.end_datetime)
            elif now > self.start_datetime:
                result = ("current", "Конец", self.end_datetime)
            else:
                result = ("ahead", "Начало", self.start_datetime)

        return {"id": self.id,
                "title": self.title,
                "category": Task.choices[self.category],
                "category_class": Task.english_choices[self.category],
                "status": result[0],
                "time_label": result[1],
                "deadline": result[2]}
    
    @classmethod
    def get_statistic(cls, user)->dict:
        "npt - not periodic tasks"
        now = datetime.now().replace(tzinfo=pytz.timezone("Europe/Moscow")) - timedelta(0, 0, 0, 0, 30, 0, 0)

        not_periodic_tasks = cls.objects.filter(owner = user, is_periodic = False)
        periodic_tasks = cls.objects.filter(owner = user, is_periodic = True)
        completed_npt = not_periodic_tasks.exclude(last_execution__exact = None)
        ended_pt = periodic_tasks.filter(end_datetime__lt = now)
        completed_on_time_npt = completed_npt.filter(end_datetime__gt = models.F("last_execution"))
        completed_pt = Period.objects.filter(task__owner = user).values("execution_count")
        completed_pt_count = sum((i["execution_count"] for i in completed_pt))
        result = {"npt": not_periodic_tasks.count(),
                "completed_npt": completed_npt.count(),
                "completed_on_time_npt": completed_on_time_npt.count(),
                "pt": periodic_tasks.count(),
                "ended_pt": ended_pt.count(),
                "completed_pt_count": completed_pt_count,
        }
        result|= {
            "current_pt": result["pt"] - result["ended_pt"],
            "completed_npt_per": result["npt"] and int(result["completed_npt"]/result["npt"]*100),
            "completed_on_time_npt_per": result["completed_npt"] and int(result["completed_on_time_npt"]/result["completed_npt"]*100),
            "ended_pt_per": result["pt"] and int(result["ended_pt"]/result["pt"]*100),
        }
        result|= {
            "current_pt_per": 100 - result["ended_pt_per"]
        }
        return result

class Period(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    period_duration = models.SmallIntegerField(verbose_name="Период повтора")
    execution_duration = models.SmallIntegerField(verbose_name="Длительность выполнения")
    execution_count = models.SmallIntegerField(verbose_name="Количество выполнений", default=0)


