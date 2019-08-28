<template>
  <div class="success">
    <Header/>
    <div class="main">
      <div class="title">
        <!--          <img src="../../static/images/right.svg" alt="">-->
        <div class="success-tips">
          <p class="tips1">您已成功购买 {{result.course_list.length}} 门课程！</p>
          <p class="tips2">你还可以加入QQ群 <span>747556033</span> 学习交流</p>
        </div>
      </div>
      <div class="order-info">
        <p class="info1"><b>付款时间：</b><span>{{result.pay_time|timeformat}}</span></p>
        <p class="info2"><b>付款金额：</b><span>{{result.real_price}}</span></p>
        <p class="info3"><b>课程信息：</b>
          <span v-for="course in result.course_list">
            {{course.name}}
          </span>
        </p>
      </div>
      <div class="wechat-code">
        <!--          <img src="../../static/image/server.cf99f78.png" alt="" class="er">-->
        <!--          <p><img src="../../static/image/tan.svg" alt="">重要！微信扫码关注获得学习通知&amp;课程更新提醒！否则将严重影响学习进度和课程体验！</p>-->
      </div>
      <div class="study">
        <span>立即学习</span>
      </div>
    </div>
    <Footer/>
  </div>
</template>

<script>
    import Header from "./common/Header"
    import Footer from "./common/Footer"

    export default {
        name: "Success",
        data() {
            return {
                result: {},
            };
        },
        created() {
            // 把地址栏上面的支付结果，转发给后端
            this.get_result();
        },
        components: {
            Header,
            Footer,
        },
        filter: {
            timeformat(time) {
                // 时间格式化
                // 2019/04/02 10:27
                let current_obj = new Date(time);
                // 年
                let Y = current_obj.getFullYear();
                // 月
                let m = current_obj.getMonth();
                m = m < 10 ? "0" + m : m;
                // 日
                let d = current_obj.getDay();
                d = d < 10 ? "0" + d : d;
                // 时
                let H = current_obj.getHours();
                H = H < 10 ? "0" + H : H;
                // 分
                let M = current_obj.getMinutes();
                M = M < 10 ? "0" + M : M;

                return `${Y}/${m}/${d} ${H}:${M}`
            }
        },
        methods: {
            get_result() {
                this.$axios.get(`${this.$settings.Host}/payments/alipay/result/` + location.search).then(response => {
                    console.log(response.data);
                    this.result = response.data;
                    this.update_credit(response.data.user_credit)
                }).catch(error => (
                    console.log(error.response)
                ))
            },
            update_credit(user_credit) {
                if (localStorage.user_credit) {
                    localStorage.user_credit = user_credit;
                } else if (sessionStorage.user_credit) {
                    sessionStorage.user_credit = user_credit;
                }
            }
        }
    }
</script>

<style scoped>
  .success {
    padding-top: 80px;
  }

  .main {
    height: 100%;
    padding-top: 25px;
    padding-bottom: 25px;
    margin: 0 auto;
    width: 1200px;
    background: #fff;
  }

  .main .title {
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    padding: 25px 40px;
    border-bottom: 1px solid #f2f2f2;
  }

  .main .title .success-tips {
    box-sizing: border-box;
  }

  .title img {
    vertical-align: middle;
    width: 60px;
    height: 60px;
    margin-right: 40px;
  }

  .title .success-tips {
    box-sizing: border-box;
  }

  .title .tips1 {
    font-size: 22px;
    color: #000;
  }

  .title .tips2 {
    font-size: 16px;
    color: #4a4a4a;
    letter-spacing: 0;
    text-align: center;
    margin-top: 10px;
  }

  .title .tips2 span {
    color: #ec6730;
  }

  .order-info {
    padding: 25px 48px;
    padding-bottom: 15px;
    border-bottom: 1px solid #f2f2f2;
  }

  .order-info p {
    display: -ms-flexbox;
    display: flex;
    margin-bottom: 10px;
    font-size: 16px;
  }

  .order-info p b {
    font-weight: 400;
    color: #9d9d9d;
    white-space: nowrap;
  }

  .wechat-code {
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    padding: 25px 40px;
    border-bottom: 1px solid #f2f2f2;
  }

  .wechat-code > img {
    width: 100px;
    height: 100px;
    margin-right: 15px;
  }

  .wechat-code p {
    font-size: 14px;
    color: #d0021b;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
  }

  .wechat-code p > img {
    width: 16px;
    height: 16px;
    margin-right: 10px;
  }

  .study {
    padding: 25px 40px;
  }

  .study span {
    display: block;
    width: 140px;
    height: 42px;
    text-align: center;
    line-height: 42px;
    cursor: pointer;
    background: #ffc210;
    border-radius: 6px;
    font-size: 16px;
    color: #fff;
  }
</style>
