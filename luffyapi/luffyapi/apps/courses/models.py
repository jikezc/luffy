from django.db import models
from luffyapi.utils.basemodels import BaseModel
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class CourseCategory(BaseModel):
    """
    课程分类
    """
    name = models.CharField(max_length=64, unique=True, verbose_name="分类名称")

    class Meta:
        db_table = "ly_course_category"
        verbose_name = "课程分类"
        verbose_name_plural = "课程分类"

    def __str__(self):
        return "%s" % self.name


class Course(BaseModel):
    """
    专题课程
    """
    course_type = (
        (0, '付费'),
        (1, 'VIP专享'),
        (2, '学位课程')
    )
    level_choices = (
        (0, '初级'),
        (1, '中级'),
        (2, '高级'),
    )
    status_choices = (
        (0, '上线'),
        (1, '下线'),
        (2, '预上线'),
    )
    name = models.CharField(max_length=128, verbose_name="课程名称")
    course_img = models.ImageField(upload_to="courses", max_length=255, verbose_name="封面图片", blank=True, null=True)
    course_video = models.FileField(upload_to="courses", max_length=255, verbose_name="封面视频", blank=True, null=True)
    course_type = models.SmallIntegerField(choices=course_type, default=0, verbose_name="付费类型")
    # 使用这个字段的原因
    # brief = models.TextField(max_length=2048, verbose_name="详情介绍", null=True, blank=True)
    brief = RichTextUploadingField(max_length=2048, verbose_name="课程概述", null=True, blank=True)
    level = models.SmallIntegerField(choices=level_choices, default=1, verbose_name="难度等级")
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)
    period = models.IntegerField(verbose_name="建议学习周期(day)", default=7)
    attachment_path = models.FileField(max_length=128, verbose_name="课件路径", blank=True, null=True)
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="课程状态")
    course_category = models.ForeignKey("CourseCategory", on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name="课程分类")
    students = models.IntegerField(verbose_name="学习人数", default=0)
    lessons = models.IntegerField(verbose_name="总课时数量", default=0)
    pub_lessons = models.IntegerField(verbose_name="课时更新数量", default=0)
    # price = models.DecimalField(max_digits=6,decimal_places=2, verbose_name="课程原价",default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程原价", default=0,
                                help_text="当前价格表示购买视频的永久价格，所以如果没有永久购买的价格则默认为0,不需要填写！")
    teacher = models.ForeignKey("Teacher", on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="授课老师")

    class Meta:
        db_table = "ly_course"
        verbose_name = "专题课程"
        verbose_name_plural = "专题课程"

    @property
    def lesson_list(self):
        """要展示到列表的课程信息"""
        lesson_list = self.courselessons.filter(is_show_list=True)[:4]
        data = []
        if len(lesson_list) < 1:
            return data

        for lesson in lesson_list:
            data.append({
                "id": lesson.id,
                "name": lesson.name,
                "free_trail": True if lesson.free_trail else False
            })

        return data

    @property
    def level_name(self):
        return self.level_choices[self.level][1]

    @property
    def chapter_list(self):
        data = []
        """1.获取当前课程的所有章节信息"""
        chapters = self.coursechapters.filter(is_show=True, is_delete=False).order_by('chapter')
        for chapter in chapters:
            lesson_list = []
            """2. 循环所有章节，查找章节下面所有的课时"""
            chapter_lesson = chapter.coursesections.filter(is_show=True, is_delete=False)
            for lesson in chapter_lesson:
                lesson_list.append({
                    "id": lesson.id,
                    "name": lesson.name,
                    "section_type": lesson.section_type,
                    "duration": lesson.duration,
                    "free_trail": True if lesson.free_trail else False
                })
            data.append({
                'chapter': chapter.chapter,
                'name': chapter.name,
                'lesson_list': lesson_list,
            })
        return data

    @property
    def expire_list(self):
        """课程有效期列表"""
        data = []
        expire_list = self.course_expire.all().order_by("expire_time")
        for item in expire_list:
            data.append({
                "expire_text": item.expire_text,
                "expire_time": item.expire_time,
                "price": self.real_price(item.price),
            })

        # 永久价格选项
        if self.price > 0:
            data.append({
                "expire_text": "永久有效",
                "expire_time": -1,
                "price": self.real_price()
            })

        return data

    @property
    def discount_name(self):
        """折扣类型"""
        from datetime import datetime
        now = datetime.now()
        course_price_discount_list = self.activeprices.filter(is_show=True, is_delete=False,
                                                              active__start_time__lte=now,
                                                              active__end_time__gt=now).first()

        if course_price_discount_list is None:
            """查找不到当前商品课程参与的活动，则表示没有参加活动，直接范围原价"""
            return None

        discount = course_price_discount_list.discount.discount_type
        return discount.name

    def real_price(self, price=None):
        """计算课程的真实价格"""
        if price is None:
            """如果计算真实价格额时候，含糊没有指定计算价格，则使用永久价格来进行计算"""
            price = self.price

        price = float(price)

        course_price_discount_list = self.activeprices.filter(is_show=True, is_delete=False).first()
        if course_price_discount_list is None:
            """查找不到当前商品课程参与的活动，则表示没有参加活动，直接范围原价"""
            return "%.2f" % price

        # 获取当前商品参加的活动，判断商品是否在活动期间
        active = course_price_discount_list.active
        # 活动开始时间和结束时间
        start_time = active.start_time.timestamp()
        end_time = active.end_time.timestamp()
        from datetime import datetime
        current_time = datetime.now().timestamp()
        # print( "当前时间：%s，活动开始：%s，活动结束：%s" % (current_time, start_time,end_time) )
        # 判断商品是否还在活动有效期内
        if current_time <= start_time or current_time >= end_time:
            """不在活动期间"""
            return "%.2f" % price

        """计算真实价格"""
        discount = course_price_discount_list.discount
        if discount.sale == "":
            """如果sale不填写，则表示价格免费"""
            return "%.2f" % 0

        elif discount.sale[0] == "*":
            """限时折扣"""
            sale = float(discount.sale[1:])
            return "%.2f" % (price * sale)

        elif discount.sale[0] == '-':
            """限时减免"""
            sale = float(discount.sale[1:])
            return "%.2f" % (price - sale)

        elif discount.sale[0] == "满":
            """限时满减"""
            sale = discount.sale
            sale = sale.replace("满", "")
            sale_list = sale.split("\r\n")
            data_dict = []
            for item in sale_list:
                item_list = item.split("-")
                if price >= float(item_list[0]):
                    data_dict.append(float(item_list[1]))

            data_dict.sort()
            data_dict.reverse()
            return "%.2f" % (price - data_dict[0])

        # 返回原价格
        return "%.2f" % price

    @property
    def active_time(self):
        """活动的剩余时间(秒)"""
        from datetime import datetime
        now = datetime.now()
        try:
            active = self.activeprices.get(active__start_time__lte=now, active__end_time__gt=now)
        except:
            # 如果没有参与到任何活动，或者活动已经过期，则返回商品原价
            return 0

        # 服务端当前的时间戳
        now_time = now.timestamp()
        # 活动的结束事件
        end_time = active.active.end_time.timestamp()

        # 返回活动剩余的秒数
        return int(end_time - now_time)

    def __str__(self):
        return "%s" % self.name


class Teacher(BaseModel):
    """讲师、导师表"""
    role_choices = (
        (0, '讲师'),
        (1, '导师'),
        (2, '班主任'),
    )
    name = models.CharField(max_length=32, verbose_name="讲师title")
    role = models.SmallIntegerField(choices=role_choices, default=0, verbose_name="讲师身份")
    title = models.CharField(max_length=64, verbose_name="职位、职称")
    signature = models.CharField(max_length=255, verbose_name="导师签名", help_text="导师签名", blank=True, null=True)
    image = models.ImageField(upload_to="teacher", null=True, verbose_name="讲师封面")
    brief = models.TextField(max_length=1024, verbose_name="讲师描述")

    class Meta:
        db_table = "ly_teacher"
        verbose_name = "讲师导师"
        verbose_name_plural = "讲师导师"

    def __str__(self):
        return "%s" % self.name


class CourseChapter(BaseModel):
    """课程章节"""
    course = models.ForeignKey("Course", related_name='coursechapters', on_delete=models.CASCADE, verbose_name="课程名称")
    chapter = models.SmallIntegerField(verbose_name="第几章", default=1)
    name = models.CharField(max_length=128, verbose_name="章节标题")
    summary = models.TextField(verbose_name="章节介绍", blank=True, null=True)
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)

    class Meta:
        db_table = "ly_course_chapter"
        verbose_name = "课程章节"
        verbose_name_plural = "课程章节"

    def __str__(self):
        return "%s:(第%s章)%s" % (self.course, self.chapter, self.name)


class CourseLesson(BaseModel):
    """课程课时"""
    section_type_choices = (
        (0, '文档'),
        (1, '练习'),
        (2, '视频')
    )
    chapter = models.ForeignKey("CourseChapter", related_name='coursesections', on_delete=models.CASCADE,
                                verbose_name="课程章节")
    name = models.CharField(max_length=128, verbose_name="课时标题")
    orders = models.PositiveSmallIntegerField(verbose_name="课时排序")
    section_type = models.SmallIntegerField(default=2, choices=section_type_choices, verbose_name="课时种类")
    section_link = models.CharField(max_length=255, blank=True, null=True, verbose_name="课时链接",
                                    help_text="若是video，填vid,若是文档，填link")
    duration = models.CharField(verbose_name="视频时长", blank=True, null=True, max_length=32)  # 仅在前端展示使用
    pub_date = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    free_trail = models.BooleanField(verbose_name="是否可试看", default=False)
    is_show_list = models.BooleanField(verbose_name="是否展示到列表页中", default=False)
    course = models.ForeignKey("Course", related_name='courselessons', on_delete=models.CASCADE, verbose_name="课程名称")

    class Meta:
        db_table = "ly_course_lesson"
        verbose_name = "课程课时"
        verbose_name_plural = "课程课时"

    def __str__(self):
        return "%s-%s" % (self.chapter, self.name)


class CourseExpire(BaseModel):
    """课程有效期的勾选"""
    course = models.ForeignKey("Course", related_name="course_expire", on_delete=models.CASCADE, verbose_name="课程名称")
    expire_time = models.IntegerField(verbose_name="有效期数值", null=True, blank=True)
    expire_text = models.CharField(max_length=150, verbose_name="有效期提示文本", null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程价格", default=0)

    class Meta:
        db_table = "ly_course_expire"
        verbose_name = "课程有效期选项"
        verbose_name_plural = "课程有效期选项"

    def __str__(self):
        return "课程：%s，有效期：%s，价格：%s" % (self.course, self.expire_text, self.price)


"""价格相关的模型"""


class PriceDiscountType(BaseModel):
    """课程优惠类型"""
    name = models.CharField(max_length=32, verbose_name="类型名称")
    remark = models.CharField(max_length=250, blank=True, null=True, verbose_name="备注信息")

    class Meta:
        db_table = "ly_price_discount_type"
        verbose_name = "课程优惠类型"
        verbose_name_plural = "课程优惠类型"

    def __str__(self):
        return "%s" % (self.name)


class PriceDiscount(BaseModel):
    """课程优惠模型"""
    discount_type = models.ForeignKey("PriceDiscountType", on_delete=models.CASCADE, related_name='pricediscounts',
                                      verbose_name="优惠类型")
    condition = models.IntegerField(blank=True, default=0, verbose_name="满足优惠的价格条件",
                                    help_text="设置参与优惠的价格门槛，表示商品必须在xx价格以上的时候才参与优惠活动，<br>如果不填，则不设置门槛")
    sale = models.TextField(verbose_name="优惠公式", blank=True, null=True, help_text="""
    不填表示免费；<br>
    *号开头表示折扣价，例如*0.82表示八二折；<br>
    -号开头则表示减免，例如-20表示原价-20；<br>
    如果需要表示满减,则需要使用 原价-优惠价格,例如表示课程价格大于100,优惠10;大于200,优惠20,格式如下:<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;满100-10<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;满200-20<br>

    """)

    class Meta:
        db_table = "ly_price_discount"
        verbose_name = "价格优惠策略"
        verbose_name_plural = "价格优惠策略"

    def __str__(self):
        return "价格优惠:%s,优惠条件:%s,优惠值:%s" % (self.discount_type.name, self.condition, self.sale)


class CoursePriceDiscount(BaseModel):
    """课程与优惠策略的关系表"""
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="activeprices", verbose_name="课程")
    active = models.ForeignKey("Activity", on_delete=models.DO_NOTHING, related_name="activecourses", verbose_name="活动")
    discount = models.ForeignKey("PriceDiscount", on_delete=models.CASCADE, related_name="discountcourse",
                                 verbose_name="优惠折扣")

    class Meta:
        db_table = "ly_course_price_dicount"
        verbose_name = "课程与优惠策略的关系表"
        verbose_name_plural = "课程与优惠策略的关系表"

    def __str__(self):
        return "课程：%s，优惠活动: %s,开始时间:%s,结束时间:%s" % (
            self.course.name, self.active.name, self.active.start_time, self.active.end_time)


class Activity(BaseModel):
    """优惠活动"""
    name = models.CharField(max_length=150, verbose_name="活动名称")
    start_time = models.DateTimeField(verbose_name="优惠策略的开始时间")
    end_time = models.DateTimeField(verbose_name="优惠策略的结束时间")
    remark = models.CharField(max_length=250, blank=True, null=True, verbose_name="备注信息")

    class Meta:
        db_table = "ly_activity"
        verbose_name = "商品活动"
        verbose_name_plural = "商品活动"

    def __str__(self):
        return self.name
