from django.contrib import admin

# Register your models here.
from django.db.models import Prefetch

from .models import Archive, ArchiveDetail


@admin.register(ArchiveDetail)
class ArchiveDetailAdmin(admin.ModelAdmin):
    list_filter = ["domainhash", "ddate", "snapshotDdateCounts"]
    # list_per_page = 1
    list_display = ('title', 'domainhash', 'ddate', 'snapshotDdateCounts', 'addtime', 'created')


@admin.register(Archive)
class ArchiveAdmin(admin.ModelAdmin):
    list_filter = ["domain", "rand_id", "addtime"]
    # 每页显示多少条数据
    list_per_page = 20
    list_display = (
        'domain', 'domainhash', 'archive_detail_title', 'archive_detail_ddate', 'archive_detail_snapshotDdateCounts',
        'snapshotYears', 'snapshotCounts')

    def get_queryset(self, request):
        queryset = super(ArchiveAdmin, self).get_queryset(request).prefetch_related(
            Prefetch("archive_detail", to_attr="archive_detail_cache")
        )
        return queryset
