from django.db import models

# Create your models here.
from django.utils.html import format_html
from django.views.decorators.cache import cache_page


class ArchiveDetail(models.Model):
    archive = models.ForeignKey("Archive", on_delete=models.CASCADE, related_name="archive_detail")
    domainhash = models.BigIntegerField(verbose_name='域名hash值', db_index=True)  # 普通索引，方便查询
    title = models.TextField(verbose_name='快照的标题')
    ddate = models.IntegerField(verbose_name='抓取快照的年月')
    snapshotDdateCounts = models.IntegerField(verbose_name='快照在此年月中的个数')
    addtime = models.DateField(verbose_name='放入域名的时间')
    created = models.DateTimeField(auto_now_add=True, verbose_name='抓取时间')

    class Meta:
        verbose_name = "快照详情"
        verbose_name_plural = "快照详情"
        ordering = ["-ddate"]

    def __str__(self):
        return '%s' % self.domainhash


class Archive(models.Model):
    domain = models.CharField(max_length=30, blank=False, verbose_name='域名')
    domainhash = models.BigIntegerField(verbose_name='域名hash值', unique=True)
    snapshotYears = models.IntegerField(blank=False, verbose_name='域名的快照总年份')
    snapshotCounts = models.IntegerField(blank=False, verbose_name='域名的快照总数')
    flag = models.IntegerField(blank=False, verbose_name='是否包含非法词')
    type = models.IntegerField(blank=False, verbose_name='域名的类型')
    rand_id = models.IntegerField(blank=False, verbose_name='rand_id')
    addtime = models.DateField(verbose_name='放入域名的时间')

    class Meta:
        verbose_name = "快照"
        verbose_name_plural = "快照"

    def __str__(self):
        return self.domain

    def get_archive_detail(self):
        return getattr(self, "archive_detail_cache") if hasattr(self, "archive_detail_cache") \
            else ArchiveDetail.objects.filter(archive=self)

    def archive_detail_title(self):
        queryset = self.get_archive_detail()
        result_data = "</br>".join(["{}".format(i.title) for i in queryset])
        return format_html("<div>{}</div>".format(result_data))

    archive_detail_title.admin_order_field = 'archive_detail__title'
    archive_detail_title.short_description = '快照标题'

    def archive_detail_ddate(self):
        queryset = self.get_archive_detail()
        result_data = "</br>".join(["{}".format(i.ddate) for i in queryset])
        return format_html("<div>{}</div>".format(result_data))

    archive_detail_ddate.admin_order_field = 'archive_detail__ddate'
    archive_detail_ddate.short_description = '快照对应的年月'

    def archive_detail_snapshotDdateCounts(self):
        queryset = self.get_archive_detail()
        result_data = "</br>".join(["{}".format(i.snapshotDdateCounts) for i in queryset])
        return format_html("<div>{}</div>".format(result_data))

    archive_detail_snapshotDdateCounts.admin_order_field = 'archive_detail__snapshotDdateCounts'
    archive_detail_snapshotDdateCounts.short_description = '当前的快照个数'
