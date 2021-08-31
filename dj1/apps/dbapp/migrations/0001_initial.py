# Generated by Django 2.1.7 on 2021-04-27 06:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('image_url', models.URLField(default='', verbose_name='轮播图片url')),
                ('priority', models.IntegerField(verbose_name='优先级')),
            ],
            options={
                'verbose_name': '轮播图',
                'verbose_name_plural': '轮播图',
                'db_table': 'banner',
                'ordering': ['priority', '-update_time', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('content', models.TextField(verbose_name='评论内容')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
                'db_table': 'comments',
                'ordering': ['-update_time', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Hotnews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('priority', models.IntegerField(verbose_name='优先级')),
            ],
            options={
                'verbose_name': '热门新闻',
                'verbose_name_plural': '热门新闻',
                'db_table': 'hotnews',
                'ordering': ['-update_time', 'id'],
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('digest', models.CharField(max_length=200, verbose_name='摘要')),
                ('content', models.TextField(verbose_name='内容')),
                ('clicks', models.IntegerField(default=0, verbose_name='点击量')),
                ('image_url', models.URLField(default='', verbose_name='图片')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '文章新闻',
                'verbose_name_plural': '文章新闻',
                'db_table': 'news',
                'ordering': ['-update_time', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('name', models.CharField(max_length=64, verbose_name='标签名')),
            ],
            options={
                'verbose_name': '文章分类',
                'verbose_name_plural': '文章分类',
                'db_table': 'tag',
                'ordering': ['-update_time', 'id'],
            },
        ),
        migrations.AddField(
            model_name='news',
            name='tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dbapp.Tag'),
        ),
        migrations.AddField(
            model_name='hotnews',
            name='new',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dbapp.News'),
        ),
        migrations.AddField(
            model_name='comments',
            name='new',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbapp.News'),
        ),
        migrations.AddField(
            model_name='banner',
            name='new',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dbapp.News'),
        ),
    ]
