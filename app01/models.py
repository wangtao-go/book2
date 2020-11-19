
from django.db import models
# Create your models here.
class Publisher(models.Model):
    name=models.CharField(max_length=100)
    #link=models.CharField(max_length=100)

class book(models.Model):
    name=models.CharField(max_length=100)
    publisher=models.ForeignKey(Publisher,on_delete=models.CASCADE)#先后顺序,表示级联删除

class author(models.Model):
    name=models.CharField(max_length=100)
    books=models.ManyToManyField('book') #不新增字段，会创建第三张表









class VideoQuerySet(models.query.QuerySet):

    def get_count(self):
        return self.count()

    def get_published_count(self):
        return self.filter(status=0).count()

    def get_not_published_count(self):
        return self.filter(status=1).count()

    def get_published_list(self):
        return self.filter(status=0).order_by('-create_time')

    def get_search_list(self, q):
        if q:
            return self.filter(title__contains=q).order_by('-create_time')
        else:
            return self.order_by('-create_time')

    def get_recommend_list(self):
        return self.filter(status=0).order_by('-view_count')[:4]





class Video(models.Model):
    STATUS_CHOICES = (
        ('0', '发布中'),
        ('1', '未发布'),
    )
    file = models.FileField(max_length=255)
    cover = models.ImageField(upload_to='cover/', blank=True, null=True)
    objects = VideoQuerySet.as_manager()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, blank=True, null=True)
    view_count = models.IntegerField(default=0, blank=True)

# x=Video.objects.get(id=17)
# print(x.file)

from chunked_upload.models import ChunkedUpload
from django.db import models

# Create your models here.


class MyChunkedUpload(ChunkedUpload):
    pass
# Override the default ChunkedUpload to make the `user` field nullable
MyChunkedUpload._meta.get_field('user').null = True






