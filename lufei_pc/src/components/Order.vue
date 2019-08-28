<template>
  <div class="cart">
    <Header/>
    <div class="cart-info">
      <h3 class="cart-top">购物车结算 <span>共{{course_list.length}}门课程</span></h3>
      <div class="cart-title">
        <el-row>
          <el-col :span="2">&nbsp;</el-col>
          <el-col :span="10">课程</el-col>
          <el-col :span="8">有效期</el-col>
          <el-col :span="4">价格</el-col>
        </el-row>
      </div>
      <div class="cart-item" :key="key" v-for="course,key in course_list">
        <el-row>
          <el-col :span="2" class="checkbox">&nbsp;&nbsp;</el-col>
          <el-col :span="10" class="course-info">
            <img :src="course.course_img" alt="">
            <div class="course_name">
              {{course.name}}
              <span class="discount_name">{{course.discount_name}}</span>
            </div>
          </el-col>
          <el-col :span="8"><span>{{course.expire}}</span></el-col>
          <el-col :span="4" class="course-price">
            ¥{{course.real_price}}
            <span class="original-price">原价 ¥{{course.price}}</span>
          </el-col>
        </el-row>
      </div>

      <div class="discount">
        <div id="accordion">
          <div class="coupon-box">
            <div class="icon-box">
              <span class="select-coupon">使用优惠劵：</span>
              <a class="select-icon unselect" :class="use_coupon?'is_selected':''" @click="use_coupon=!use_coupon"><img
                class="sign is_show_select" src="../../static/image/12.png" alt=""></a>
              <span class="coupon-num">有{{coupon_list.length}}张可用</span>
            </div>
            <p class="sum-price-wrap">商品总金额：<span class="sum-price">{{total}}元</span></p>
          </div>
          <div id="collapseOne" v-if="use_coupon">
            <ul class="coupon-list" v-if="coupon_list.length>0">
              <li class="coupon-item" :class="check_use(item)" @click="check_click(item)" v-for="item in coupon_list">
                <p class="coupon-name">{{item.coupon.name}}</p>
                <p class="coupon-condition">满{{item.coupon.condition}}元可以使用</p>
                <p class="coupon-time start_time">开始时间：{{item.start_time.replace("T"," ")}}</p>
                <p class="coupon-time end_time">过期时间：{{end_time(item.start_time,item.coupon.timer)}}</p>
              </li>
            </ul>
            <div class="no-coupon" v-if="coupon_list.length<1">
              <span class="no-coupon-tips">暂无可用优惠券</span>
            </div>
          </div>
        </div>
        <div class="credit-box">
          <label class="my_el_check_box">
            <el-checkbox class="my_el_checkbox" v-model="use_credit"></el-checkbox>
          </label>
          <p class="discount-num1" v-if="!use_credit">使用我的贝里</p>
          <p class="discount-num2" v-else><span>总积分：{{user_credit}}，抵扣 ￥<el-input-number v-model="credit" :min="1"
                                                                                         :max="max_credit()"
                                                                                         label="请填写积分"></el-input-number>，本次花费以后，剩余{{parseInt(user_credit-credit)}}积分</span>
          </p>
        </div>
        <p class="sun-coupon-num">优惠券抵扣：<span>{{(credit/credit_to_money).toFixed(2)}}元</span></p>
      </div>

      <div class="calc">
        <el-row class="pay-row">
          <el-col :span="4" class="pay-col"><span class="pay-text">支付方式：</span></el-col>
          <el-col :span="8">
                <span class="alipay" @click="pay_type=1">
                  <img v-if="pay_type==1" src="../../static/image/alipay2.png" alt="">
                  <img v-else src="../../static/image/alipay.png" alt="">
                </span>
            <span class="alipay wechat" @click="pay_type=2">
                  <img v-if="pay_type==2" src="../../static/image/wechat2.png" alt="">
                  <img v-else src="../../static/image/wechat.png" alt="">
                </span>
          </el-col>
          <el-col :span="8" class="count">实付款： <span>¥{{(real_total - credit/credit_to_money).toFixed(2)}}</span>
          </el-col>
          <el-col :span="4" class="cart-pay"><span @click="payHander">去支付</span></el-col>
        </el-row>
      </div>
    </div>
    <Footer/>
  </div>
</template>

<script>
    import Header from "./common/Header"
    import Footer from "./common/Footer"

    export default {
        name: "Order",
        data() {
            return {
                user_credit: localStorage.user_credit || sessionStorage.user_credit,  // 用户积分
                credit_to_money: localStorage.credit_to_money || sessionStorage.credit_to_money,  // 积分换算比例
                course_list: [],     // 勾选商品
                pay_type: 1,        // 支付方式
                use_credit: false,  // 是否使用了优惠券
                credit: 0,          // 积分
                use_coupon: false,  // 优惠券ID，0表示没有使用优惠券
                coupon: 0,          // 优惠券ID，0表示没有使用优惠券
                coupon_list: [],     // 优惠券列表
                total: 0,           // 购物车中商品总金额
                real_total: 0,      // 实付金额
            }
        },
        components: {
            Header,
            Footer,
        },
        created() {
            this.check_user_login();
            this.get_selected_course();
            this.get_user_coupon();
        },
        watch: {
            coupon() {
                // 每次用户优惠券时，总价格都要重新计算
                this.total = this.get_total();
                this.real_total = this.get_total(true);
            },
            use_coupon() {
                if (!this.use_coupon) {
                    // 当用户不使用优惠券时，把用户当前选择的优惠券ID重置为0
                    this.coupon = 0;
                }
                // 每次用户优惠券时，总价格都要重新计算
                this.total = this.get_total();
                this.real_total = this.get_total(true);
            },
            use_credit() {
                if (!this.use_credit) {
                    // 地方用户不适用积分抵扣时，把用户当前设置的抵扣积分进行重置
                    this.credit = 0;
                }
                // 每次用户优惠券时，总价格都要重新计算
                this.total = this.get_total();
                this.real_total = this.get_total(true);
            }
        },
        methods: {
            check_user_login() {
                // 检查用户是否登录了
                let user_token = localStorage.user_token || sessionStorage.user_token;
                if (!user_token) {
                    // 判断用户是否登录了
                    this.$confirm("对不起，您尚未登录！请登录后继续操作！", "警告").then(() => {
                        this.$router.push("/user/login");
                    });
                }
                return user_token;
            },
            max_credit() {
                // 计算当前用户可以抵扣的最大积分数值
                let user_credit = parseInt(this.user_credit);
                let credit_to_money = parseInt(this.credit_to_money);
                if (user_credit / credit_to_money > this.total) {
                    return parseInt(this.total * credit_to_money);
                } else {
                    console.log(user_credit);
                    return user_credit;
                }
            },
            check_click(user_coupon) {
                let start = new Date(user_coupon.start_time) - 0;
                let end = start + user_coupon.coupon.timer * 24 * 60 * 60 * 1000;
                let now = new Date() - 0;
                if (now > start && now < end) {
                    this.coupon = user_coupon.id;
                }
            },
            check_use(user_coupon) {
                let start = new Date(user_coupon.start_time) - 0;
                let end = start + user_coupon.coupon.timer * 24 * 60 * 60 * 1000;
                let now = new Date() - 0;
                let disable = false;
                if (start > now) {
                    disable = true;
                    return "disable";
                }

                if (now > end) {
                    disable = true;
                    return "disable";
                }

                if (this.coupon == user_coupon.id && !disable) {
                    return "active";
                }

                return "";
            },
            end_time(start_time, timer) {
                // 计算优惠券的过期时间
                // 开始时间
                let start = (new Date(start_time) - 0) / 1000;
                // 过期时间
                let end = (start + timer * 24 * 60 * 60) * 1000; // 微秒
                let end_date = new Date(end);
                let Y = end_date.getFullYear();
                let m = (end_date.getMonth() + 1);
                let d = end_date.getDate();
                let H = end_date.getHours();
                let i = end_date.getMinutes();
                let s = end_date.getSeconds();
                m = m > 9 ? m : '0' + m;
                d = d > 9 ? d : '0' + m;
                H = H > 9 ? H : '0' + H;
                i = i > 9 ? i : '0' + i;
                s = s > 9 ? s : '0' + s;
                return Y + "-" + m + "-" + d + " " + H + ":" + i + ":" + s;
            },
            get_user_coupon() {
                // 获取当前登录用户的优惠券
                let user_id = localStorage.user_id || sessionStorage.user_id;
                this.$axios.get(`${this.$settings.Host}/coupon/`, {
                    params: {
                        user_id: user_id,
                    },
                    headers: {
                        "Authorization": "jwt " + this.check_user_login(),
                    }
                }).then(response => {
                    this.coupon_list = response.data;
                    this.total = this.get_total();
                    this.real_total = this.get_total(true);
                }).catch(error => {
                    console.log(error.response);
                })
            },
            get_selected_course() {
                // 获取购物车中的勾选商品
                // 获取购物车的勾选商品信息
                this.$axios.get(`${this.$settings.Host}/cart/course/selected/`, {
                    headers: {
                        "Authorization": "jwt " + this.check_user_login(),
                    }
                }).then(response => {
                    this.course_list = response.data;
                    this.total = this.get_total();
                    this.real_total = this.get_total(true);
                }).catch(error => {
                    console.log(error.response);
                });
            },
            get_total(user_coupon) {
                // user_coupon 是否使用了优惠券进行计算总价
                // 计算总价格
                let total = 0;

                for (let key in this.course_list) {
                    total += parseFloat(this.course_list[key].real_price);
                }
                if (user_coupon && this.coupon > 0) {
                    console.log(223);
                    for (let item in this.coupon_list) {
                        let coupon_item = this.coupon_list[item];
                        console.log("225", coupon_item, this.coupon);
                        if (coupon_item.id == this.coupon) {
                            // 判断当购物车中商品总价必须大于等于 优惠条件
                            if (total >= coupon_item.coupon.condition) {
                                // 当前优惠券的优惠数值
                                let sale_num = parseFloat(coupon_item.coupon.sale.slice(1));

                                if (coupon_item.coupon.sale[0] == "-") {
                                    // 抵扣优惠券
                                    total -= sale_num;
                                } else if (coupon_item.coupon.sale[0] == "*") {
                                    // 折扣优惠券
                                    total *= sale_num;
                                }
                            }
                        }
                    }
                }
                return total.toFixed(2);
            },
            payHander() {
                // 生成订单
                this.$axios.post(`${this.$settings.Host}/orders/`, {
                    pay_type: this.pay_type,
                    credit: this.credit,
                    coupon: this.coupon
                }, {
                    headers: {
                        "Authorization": "jwt " + this.check_user_login(),
                    }
                }).then(response => {
                    // 下单成功
                    console.log(response);
                    this.get_alipay_payment_url(response.data.order_number);

                    // 发起支付

                }).catch(error => {
                    console.log(error.response);
                })
            },
            get_alipay_payment_url(order_number) {
                this.$axios.post(`${this.$settings.Host}/payments/${order_number}/alipay/`).then(response => {
                    console.log(response.data.pay_url);
                    location.href = response.data.pay_url;
                }).catch(error => {
                    console.log(response.error);
                })
            }
        }
    }
</script>

<style scoped>
  .cart {
    margin-top: 80px;
  }

  .cart-info {
    overflow: hidden;
    width: 1200px;
    margin: auto;
  }

  .cart-top {
    font-size: 18px;
    color: #666;
    margin: 25px 0;
    font-weight: normal;
  }

  .cart-top span {
    font-size: 12px;
    color: #d0d0d0;
    display: inline-block;
  }

  .cart-title {
    background: #F7F7F7;
    height: 70px;
  }

  .calc {
    margin-top: 25px;
    margin-bottom: 40px;
  }

  .calc .count {
    text-align: right;
    margin-right: 10px;
    vertical-align: middle;
  }

  .calc .count span {
    font-size: 36px;
    color: #333;
  }

  .calc .cart-pay {
    margin-top: 5px;
    width: 110px;
    height: 38px;
    outline: none;
    border: none;
    color: #fff;
    line-height: 38px;
    background: #ffc210;
    border-radius: 4px;
    font-size: 16px;
    text-align: center;
    cursor: pointer;
  }

  .cart-item {
    height: 120px;
    line-height: 120px;
    margin-bottom: 30px;
  }

  .course-info img {
    width: 175px;
    height: 115px;
    margin-right: 35px;
    vertical-align: middle;
  }

  .alipay {
    display: inline-block;
    height: 48px;
  }

  .alipay img {
    height: 100%;
    width: auto;
  }

  .pay-text {
    display: block;
    text-align: right;
    height: 100%;
    line-height: 100%;
    vertical-align: middle;
    margin-top: 20px;
  }

  .course-price {
    line-height: 28px;
    padding-top: 30px;
  }

  .course-price .original-price {
    display: block;
    text-decoration: line-through;
    color: #9b9b9b;
  }

  .course-info img {
    float: left;
  }

  .course-info .course_name {
    float: left;
    line-height: 28px;
    padding-top: 30px;
  }

  .course-info .course_name .discount_name {
    display: block;
    height: 14px;
    color: #ffc210;
  }

  .coupon-box {
    text-align: left;
    padding-bottom: 22px;
    padding-left: 30px;
    border-bottom: 1px solid #e8e8e8;
  }

  .coupon-box::after {
    content: "";
    display: block;
    clear: both;
  }

  .icon-box {
    float: left;
  }

  .icon-box .select-coupon {
    float: left;
    color: #666;
    font-size: 16px;
  }

  .icon-box::after {
    content: "";
    clear: both;
    display: block;
  }

  .select-icon {
    width: 20px;
    height: 20px;
    float: left;
  }

  .select-icon img {
    max-height: 100%;
    max-width: 100%;
    margin-top: 2px;
    transform: rotate(-90deg);
    transition: transform .5s;
  }

  .is_show_select {
    transform: rotate(0deg) !important;
  }

  .coupon-num {
    height: 22px;
    line-height: 22px;
    padding: 0 5px;
    text-align: center;
    font-size: 12px;
    float: left;
    color: #fff;
    letter-spacing: .27px;
    background: #fa6240;
    border-radius: 2px;
    margin-left: 20px;
  }

  .sum-price-wrap {
    float: right;
    font-size: 16px;
    color: #4a4a4a;
    margin-right: 45px;
  }

  .sum-price-wrap .sum-price {
    font-size: 18px;
    color: #fa6240;
  }

  .no-coupon {
    text-align: center;
    width: 100%;
    padding: 50px 0px;
    align-items: center;
    justify-content: center; /* 文本两端对其 */
    border-bottom: 1px solid rgb(232, 232, 232);
  }

  .no-coupon-tips {
    font-size: 16px;
    color: #9b9b9b;
  }

  .credit-box {
    height: 30px;
    margin-top: 40px;
    display: flex;
    align-items: center;
    justify-content: flex-end
  }

  .my_el_check_box {
    position: relative;
  }

  .my_el_checkbox {
    margin-right: 10px;
    width: 16px;
    height: 16px;
  }

  .discount-num1 {
    color: #9b9b9b;
    font-size: 16px;
    margin-right: 45px;
  }

  .discount-num2 {
    margin-right: 45px;
    font-size: 16px;
    color: #4a4a4a;
  }

  .sun-coupon-num {
    margin-right: 45px;
    margin-bottom: 43px;
    margin-top: 40px;
    font-size: 16px;
    width: 100%;
    text-align: right;
    color: #4a4a4a;
    display: inline-block;
  }

  .sun-coupon-num span {
    font-size: 18px;
    color: #fa6240;
    margin-right: 40px;
  }

  .coupon-list {
    margin: 20px 0;
  }

  .coupon-list::after {
    display: block;
    content: "";
    clear: both;
  }

  .coupon-item {
    float: left;
    margin: 15px 8px;
    width: 180px;
    height: 100px;
    padding: 5px;
    background-color: #fa3030;
    cursor: pointer;
  }

  .coupon-list .active {
    background-color: #fa9000;
  }

  .coupon-list .disable {
    cursor: not-allowed;
    background-color: #fa6060;
  }

  .coupon-condition {
    font-size: 12px;
    text-align: center;
    color: #fff;
  }

  .coupon-name {
    color: #fff;
    font-size: 24px;
    text-align: center;
  }

  .coupon-time {
    text-align: left;
    color: #fff;
    font-size: 12px;
  }

  .unselect {
    margin-left: 0px;
    transform: rotate(-90deg);
  }

  .is_selected {
    transform: rotate(-1turn) !important;
  }
</style>
