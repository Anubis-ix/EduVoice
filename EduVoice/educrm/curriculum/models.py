from django.db import models


class CurriculumFramework(models.Model):
    """
    A curriculum system a school follows — CBC, Cambridge/IGCSE, IB, British
    National Curriculum, 8-4-4, etc. Schools pick or create one; nothing
    about Subject or ClassRoom below is hardcoded to any single system.
    """
    name = models.CharField(max_length=100, unique=True)   # e.g. "CBC", "Cambridge IGCSE", "IB"
    code = models.CharField(max_length=20, unique=True)     # e.g. "cbc", "igcse", "ib"
    country = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CurriculumLevel(models.Model):
    """
    A stage within a framework — e.g. CBC's "Primary" and "Junior School",
    or Cambridge's "Lower Secondary" and "IGCSE", or IB's "MYP" and "DP".
    Replaces the old hardcoded Subject.LEVEL_CHOICES (primary/junior only).
    """
    framework = models.ForeignKey(CurriculumFramework, on_delete=models.CASCADE, related_name='levels')
    name = models.CharField(max_length=100)          # e.g. "Primary", "IGCSE", "Diploma Programme"
    order = models.PositiveIntegerField(default=0)   # for sorting stages low → high

    class Meta:
        ordering = ['framework', 'order']
        unique_together = ['framework', 'name']

    def __str__(self):
        return f"{self.framework.code} — {self.name}"


class Subject(models.Model):
    framework = models.ForeignKey(
        CurriculumFramework, on_delete=models.CASCADE, related_name='subjects',
        null=True,  # nullable during migration from the old hardcoded data; see migration note
    )
    level = models.ForeignKey(
        CurriculumLevel, on_delete=models.SET_NULL, null=True, blank=True, related_name='subjects'
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, default='📚')  # emoji icon
    is_core = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['framework', 'level', 'name']

    def __str__(self):
        level_part = f" ({self.level.name})" if self.level else ""
        return f"{self.name}{level_part}"


class SoftSkill(models.Model):
    """Values-based skills tracked per student — curiosity, reading, etc.
    Deliberately framework-agnostic: every institution benefits from these
    regardless of which academic curriculum it runs."""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=10, default='⭐')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
