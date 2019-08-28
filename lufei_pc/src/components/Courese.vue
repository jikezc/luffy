<template>
  <div class="course">
    <Header></Header>
    <div class="main">
      <!-- 筛选条件 -->
      <div class="condition">
        <ul class="cate-list">
          <li class="title">课程分类:</li>
          <li :class="filter.course_category == 0?'this':''" @click="filter.course_category = 0">全部</li>
          <li :class="filter.course_category == category.id?'this':''" @click="filter.course_category = category.id"
              v-for="category in category_list" :key="category.id">{{ category.name }}
          </li>
        </ul>

        <div class="ordering">
          <ul>
            <li class="title">筛&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;选:</li>
            <li class="default" :class="if_change('id', filter.ordering)" @click="change('id')">默认</li>
            <li class="hot" :class="if_change('students', filter.ordering)" @click="change('students')">人气</li>
            <li class="price" :class="if_change('price', filter.ordering)" @click="change('price')">价格</li>
          </ul>
          <p class="condition-result">共{{ total }}个课程</p>
        </div>

      </div>
      <!-- 课程列表 -->
      <div class="course-list">
        <div v-for="course in course_list" :key="course.id" class="course-item">
          <div class="course-image">
            <img :src="course.course_img" alt="">
          </div>
          <div class="course-info">
            <h3>
              <router-link :to="`/course/`+course.id">{{ course.name }}</router-link>
              <span><img src="/static/image/avatar1.svg" alt="">{{ course.students }}人已加入学习</span></h3>
            <p class="teather-info">{{ course.teacher.name }} {{ course.teacher.signature }} {{ course.teacher.title }}
              <span>共{{ course.lessons }}课时/{{ course.lessons == course.pub_lessons?'更新完成':`已更新${course.pub_lessons}课时`}}</span>
            </p>
            <ul class="lesson-list">
              <!--              <li><span class="lesson-title">01 | 第1节：初识编码</span> <span class="free">免费</span></li>-->
              <!--              <li><span class="lesson-title">01 | 第1节：初识编码初识编码</span> <span class="free">免费</span></li>-->
              <!--              <li><span class="lesson-title">01 | 第1节：初识编码</span> <span class="free">免费</span></li>-->
              <!--              <li v-for="lesson,key in course_list.lesson_list" :key="key"><span class="lesson-title">0{{key+1}} | 第{{ lesson.id }}节：{{ lesson.name }}</span> <span class="free">免费</span></li>-->
              <li v-for="lesson,key in course.lesson_list" :key="key"><span class="lesson-title">0{{key+1}} | {{lesson.name}}</span>
                <span class="free" v-if="lesson.free_trail">免费</span></li>
            </ul>
            <div class="pay-box">
              <span class="discount-type" v-if="course.discount_name">{{course.discount_name}}</span>
              <span class="discount-price">￥{{course.real_price}}元</span>
              <span class="original-price" v-if="course.discount_name">原价：{{course.price}}元</span>
              <span class="buy-now">立即购买</span>
            </div>
          </div>
        </div>
        <!--        <div class="course-item">-->
        <!--          <div class="course-image">-->
        <!--            <img src="/static/image/course-cover.jpeg" alt="">-->
        <!--          </div>-->
        <!--          <div class="course-info">-->
        <!--            <h3>Python开发21天入门 <span><img src="/static/image/avatar1.svg" alt="">100人已加入学习</span></h3>-->
        <!--            <p class="teather-info">Alex 金角大王 老男孩Python教学总监 <span>共154课时/更新完成</span></p>-->
        <!--            <ul class="lesson-list">-->
        <!--              <li><span class="lesson-title">01 | 第1节：初识编码</span> <span class="free">免费</span></li>-->
        <!--              <li><span class="lesson-title">01 | 第1节：初识编码初识编码</span> <span class="free">免费</span></li>-->
        <!--              <li><span class="lesson-title">01 | 第1节：初识编码</span> <span class="free">免费</span></li>-->
        <!--              <li><span class="lesson-title">01 | 第1节：初识编码初识编码初识编码初识编码</span> <span class="free">免费</span></li>-->
        <!--            </ul>-->
        <!--            <div class="pay-box">-->
        <!--              <span class="discount-type">限时免费</span>-->
        <!--              <span class="discount-price">￥0.00元</span>-->
        <!--              <span class="original-price">原价：9.00元</span>-->
        <!--              <span class="buy-now">立即购买</span>-->
        <!--            </div>-->
        <!--          </div>-->
        <!--        </div>-->
        <!--        <div class="course-item">-->
        <!--          <div class="course-image">-->
        <!--            <img src="/static/image/course-cover.jpeg" alt="">-->
        <!--          </div>-->
        <!--          <div class="course-info">-->
        <!--            <h3>Python开发21天入门 <span><img src="/static/image/avatar1.svg" alt="">100人已加入学习</span></h3>-->
        <!--            <p class="teather-info">Alex 金角大王 老男孩Python教学总监 <span>共154课时/更新完成</span></p>-->
        <!--            <ul class="lesson-list">-->
        <!--              <li><span class="lesson-title">01 | 第1节：初识编码</span> <span class="free">免费</span></li>-->
        <!--              <li><span class="lesson-title">01 | 第1节：初识编码初识编码</span> <span class="free">免费</span></li>-->
        <!--              <li><span class="lesson-title">01 | 第1节：初识编码</span> <span class="free">免费</span></li>-->
        <!--              <li><span class="lesson-title">01 | 第1节：初识编码初识编码初识编码初识编码</span> <span class="free">免费</span></li>-->
        <!--            </ul>-->
        <!--            <div class="pay-box">-->
        <!--              <span class="discount-type">限时免费</span>-->
        <!--              <span class="discount-price">￥0.00元</span>-->
        <!--              <span class="original-price">原价：9.00元</span>-->
        <!--              <span class="buy-now">立即购买</span>-->
        <!--            </div>-->
        <!--          </div>-->
        <!--        </div>-->
        <!--        <div class="course-item">-->
        <!--          <div class="course-image">-->
        <!--            <img src="/static/image/course-cover.jpeg" alt="">-->
        <!--          </div>-->
        <!--          <div class="course-info">-->
        <!--            <h3>Python开发21天入门 <span><img src="/static/image/avatar1.svg" alt="">100人已加入学习</span></h3>-->
        <!--            <p class="teather-info">Alex 金角大王 老男孩Python教学总监 <span>共154课时/更新完成</span></p>-->
        <!--            <ul class="lesson-list">-->
        <!--              <li><span class="lesson-title">01 | 第1节：初识编码</span> <span class="free">免费</span></li>-->
        <!--              <li><span class="lesson-title">01 | 第1节：初识编码初识编码</span> <span class="free">免费</span></li>-->
        <!--              <li><span class="lesson-title">01 | 第1节：初识编码</span> <span class="free">免费</span></li>-->
        <!--              <li><span class="lesson-title">01 | 第1节：初识编码初识编码初识编码初识编码</span> <span class="free">免费</span></li>-->
        <!--            </ul>-->
        <!--            <div class="pay-box">-->
        <!--              <span class="discount-type">限时免费</span>-->
        <!--              <span class="discount-price">￥0.00元</span>-->
        <!--              <span class="original-price">原价：9.00元</span>-->
        <!--              <span class="buy-now">立即购买</span>-->
        <!--            </div>-->
        <!--          </div>-->
        <!--        </div>-->
      </div>
      <el-pagination
        background
        layout="prev, pager, next"
        :page-size="filter.size"
        :total="total"
        @current-change="pageChange"
        :hide-on-single-page="true"
      >
      </el-pagination>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
    import Header from "./common/Header"
    import Footer from "./common/Footer"

    export default {
        name: "Course",
        data() {
            return {
                total: 0,
                category_list: [],
                course_list: [],
                filter: {
                    course_category: 0,
                    ordering: "-id",
                    page: '1',
                    size: 3,
                }
            }
        },
        components: {
            Header,
            Footer,
        },
        created() {
            this.get_course_category();
            this.get_course();
        },
        watch: {
            "filter.course_category": function () {
                this.filter.page = 1;
                this.get_course()
            },
            "filter.ordering": function () {
                this.get_course()
            },
            "filter.page": function () {
                this.get_course()
            }
        },
        methods: {
            get_course_category() {
                // 获取课程分类信息
                this.$axios.get(`${this.$settings.Host}/courses/category/`).then(response => {
                    this.category_list = response.data;
                }).catch(error => {
                    console.log(error.response)
                })
            },
            get_course() {
                let params = {
                    ordering: this.filter.ordering,
                    page: this.filter.page,
                    size: this.filter.size,
                };
                // 如果分类是0，则表示不进行筛选，查询全部，则不需要传递任何分类参数
                if (this.filter.course_category > 0) {
                    params.course_category = this.filter.course_category;
                }

                // 获取课程信息
                this.$axios.get(`${this.$settings.Host}/courses/`, {
                    params
                }).then(response => {
                    // 使用result是因为后端的drf使用了分页器返回的结果
                    this.course_list = response.data.results;
                    this.total = response.data.count;
                }).catch(error => {
                    console.log(error.response)
                })
            },
            if_change(type, ordering) {
                // type 表示条件
                // ordering 表示降序
                if (type == 'id' && ordering == "-id") {
                    return 'this this_desc';
                } else if (type == 'id' && ordering == "id") {
                    return 'this this_asc';
                } else if (type == 'students' && ordering == '-students') {
                    return 'this this_desc';
                } else if (type == 'students' && ordering == 'students') {
                    return 'this this_asc';
                } else if (type == 'price' && ordering == '-price') {
                    return 'this this_desc';
                } else if (type == 'price' && ordering == 'price') {
                    return 'this this_asc'
                }
            },
            change(type) {
                // 从别的条件切换过来点击默认的
                if (type == "id" && this.filter.ordering != "id") {
                    this.filter.ordering = "-id";
                }

                // 点击了默认帅选
                if (type == "id" && this.filter.ordering == 'id') {
                    this.filter.ordering = '-id';
                } else if (type == 'id' && this.filter.ordering == '-id') {
                    this.filter.ordering = 'id';
                }

                // 从别的条件中进行过来点击人气的
                if (type == 'students' && this.filter.ordering != 'students') {
                    this.filter.ordering = '-students';
                }

                // 点击了人气
                if (type == 'students' && this.filter.ordering == 'students') {
                    this.filter.ordering = '-students';
                } else if (type == 'students' && this.filter.ordering == '-students') {
                    this.filter.ordering = 'students';
                }

                // 从别的条件进行切换过来点击价格的
                if (type == 'price' && this.filter.ordering != 'price') {
                    this.filter.ordering = '-price';
                }

                // 点击了价格
                if (type == 'price' && this.filter.ordering == 'price') {
                    this.filter.ordering = '-price';
                } else if (type == 'price' && this.filter.ordering == '-price') {
                    this.filter.ordering = 'price'
                }
            },
            pageChange(page) {
                // 切换页码
                this.filter.page = page;
            }
        }
    }
</script>


<style scoped>
  .course {
    background: #f6f6f6;
  }

  .course .main {
    width: 1100px;
    margin: 35px auto 0;
  }

  .course .condition {
    margin-bottom: 35px;
    padding: 25px 30px 25px 20px;
    background: #fff;
    border-radius: 4px;
    box-shadow: 0 2px 4px 0 #f0f0f0;
  }

  .course .cate-list {
    border-bottom: 1px solid #333;
    border-bottom-color: rgba(51, 51, 51, .05);
    padding-bottom: 18px;
    margin-bottom: 17px;
  }

  .course .cate-list::after {
    content: "";
    display: block;
    clear: both;
  }

  .course .cate-list li {
    float: left;
    font-size: 16px;
    padding: 6px 15px;
    line-height: 16px;
    margin-left: 14px;
    position: relative;
    transition: all .3s ease;
    cursor: pointer;
    color: #4a4a4a;
    border: 1px solid transparent; /* transparent 透明 */
  }

  .course .cate-list .title {
    color: #888;
    margin-left: 0;
    letter-spacing: .36px;
    padding: 0;
    line-height: 28px;
  }

  .course .cate-list .this {
    color: #ffc210;
    border: 1px solid #ffc210 !important;
    border-radius: 30px;
  }

  .course .ordering::after {
    content: "";
    display: block;
    clear: both;
  }

  .course .ordering ul {
    float: left;
  }

  .course .ordering ul::after {
    content: "";
    display: block;
    clear: both;
  }

  .course .ordering .condition-result {
    float: right;
    font-size: 14px;
    color: #9b9b9b;
    line-height: 28px;
  }

  .course .ordering ul li {
    float: left;
    padding: 6px 15px;
    line-height: 16px;
    margin-left: 14px;
    position: relative;
    transition: all .3s ease;
    cursor: pointer;
    color: #4a4a4a;
  }

  .course .ordering .title {
    font-size: 16px;
    color: #888;
    letter-spacing: .36px;
    margin-left: 0;
    padding: 0;
    line-height: 28px;
  }

  .course .ordering .this {
    color: #ffc210;
  }

  .course .ordering .price {
    position: relative;
  }

  .course .ordering .this::before,
  .course .ordering .this::after {
    cursor: pointer;
    content: "";
    display: block;
    width: 0px;
    height: 0px;
    border: 5px solid transparent;
    position: absolute;
    right: 0;
  }

  .course .ordering .this::before {
    border-bottom: 5px solid #aaa;
    margin-bottom: 2px;
    top: 2px;
  }

  .course .ordering .this::after {
    border-top: 5px solid #aaa;
    bottom: 2px;
  }

  .course .ordering .this_desc::after {
    border-top-color: #ffc210;
  }

  .course .ordering .this_asc::before {
    border-bottom-color: #ffc210;
  }

  .course .course-item:hover {
    box-shadow: 4px 6px 16px rgba(0, 0, 0, .5);
  }

  .course .course-item {
    width: 1050px;
    background: #fff;
    padding: 20px 30px 20px 20px;
    margin-bottom: 35px;
    border-radius: 2px;
    cursor: pointer;
    box-shadow: 2px 3px 16px rgba(0, 0, 0, .1);
    /* css3.0 过渡动画 hover 事件操作 */
    transition: all .2s ease;
  }

  .course .course-item::after {
    content: "";
    display: block;
    clear: both;
  }

  /* 顶级元素 父级元素  当前元素{} */
  .course .course-item .course-image {
    float: left;
    width: 423px;
    height: 210px;
    margin-right: 30px;
  }

  .course .course-item .course-image img {
    width: 100%;
    max-height: 100%;
  }

  .course .course-item .course-info {
    float: left;
    width: 596px;
  }

  .course-item .course-info h3 a {
    font-size: 26px;
    color: #333;
    font-weight: normal;
    margin-bottom: 8px;
  }

  .course-item .course-info h3 span {
    font-size: 14px;
    color: #9b9b9b;
    float: right;
    margin-top: 14px;
  }

  .course-item .course-info h3 span img {
    width: 11px;
    height: auto;
    margin-right: 7px;
  }

  .course-item .course-info .teather-info {
    font-size: 14px;
    color: #9b9b9b;
    margin-bottom: 14px;
    padding-bottom: 14px;
    border-bottom: 1px solid #333;
    border-bottom-color: rgba(51, 51, 51, .05);
  }

  .course-item .course-info .teather-info span {
    float: right;
  }

  .course-item .lesson-list::after {
    content: "";
    display: block;
    clear: both;
  }

  .course-item .lesson-list li {
    float: left;
    width: 44%;
    font-size: 14px;
    color: #666;
    padding-left: 22px;
    /* background: url("路径") 是否平铺 x轴位置 y轴位置 */
    background: url("/static/image/play-icon-gray.svg") no-repeat left 4px;
    margin-bottom: 15px;
  }

  .course-item .lesson-list li .lesson-title {
    /* 以下3句，文本内容过多，会自动隐藏，并显示省略符号 */
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
    display: inline-block;
    max-width: 200px;
  }

  .course-item .lesson-list li:hover {
    background-image: url("/static/image/play-icon-yellow.svg");
    color: #ffc210;
  }

  .course-item .lesson-list li .free {
    width: 34px;
    height: 20px;
    color: #fd7b4d;
    vertical-align: super;
    margin-left: 10px;
    border: 1px solid #fd7b4d;
    border-radius: 2px;
    text-align: center;
    font-size: 13px;
    white-space: nowrap;
  }

  .course-item .lesson-list li:hover .free {
    color: #ffc210;
    border-color: #ffc210;
  }

  .course-item .pay-box::after {
    content: "";
    display: block;
    clear: both;
  }

  .course-item .pay-box .discount-type {
    padding: 6px 10px;
    font-size: 16px;
    color: #fff;
    text-align: center;
    margin-right: 8px;
    background: #fa6240;
    border: 1px solid #fa6240;
    border-radius: 10px 0 10px 0;
    float: left;
  }

  .course-item .pay-box .discount-price {
    font-size: 24px;
    color: #fa6240;
    float: left;
  }

  .course-item .pay-box .original-price {
    text-decoration: line-through;
    font-size: 14px;
    color: #9b9b9b;
    margin-left: 10px;
    float: left;
    margin-top: 10px;
  }

  .course-item .pay-box .buy-now {
    width: 120px;
    height: 38px;
    background: transparent;
    color: #fa6240;
    font-size: 16px;
    border: 1px solid #fd7b4d;
    border-radius: 3px;
    transition: all .2s ease-in-out;
    float: right;
    text-align: center;
    line-height: 38px;
  }

  .course-item .pay-box .buy-now:hover {
    color: #fff;
    background: #ffc210;
    border: 1px solid #ffc210;
  }

  .el-pagination {
    text-align: center;
    margin-bottom: 90px;
    margin-top: 60px;
  }
</style>
