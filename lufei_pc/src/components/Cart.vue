<template>
  <div class="cart">
    <Header></Header>
    <div class="cart_info">
      <div class="cart_title">
        <span class="text">我的购物车</span>
        <span class="total">共{{$store.state.total}}门课程</span>
      </div>
      <div class="cart_table">
        <div class="cart_head_row">
          <span class="doing_row"></span>
          <span class="course_row">课程</span>
          <span class="expire_row">有效期</span>
          <span class="price_row">单价</span>
          <span class="do_more">操作</span>
        </div>
        <div class="cart_course_list">
          <CartItem v-for="cart in cart_list" @changeprice="calc_total" :cart="cart" @delete="deleteHander"
                    :key="cart.id"></CartItem>
        </div>
        <div class="cart_footer_row">
          <span class="cart_select"><label> <el-checkbox v-model="checked"></el-checkbox><span>全选</span></label></span>
          <span class="cart_delete"><i class="el-icon-delete"></i> <span>删除</span></span>
           <span class="goto_pay"><router-link to="/order">去结算</router-link></span>
          <span class="cart_total">总计：¥{{total}}</span>
        </div>
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
    import Header from "./common/Header"
    import Footer from "./common/Footer"
    import CartItem from "./common/CartItem"

    export default {
        name: "Cart",
        data() {
            return {
                cart_list: [], // 购物车的商品信息
                checked: false,
                total: 0, // 购物车中商品的总价格
            }
        },
        created() {
            this.user_token = this.check_user_login();
            this.get_cart();
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
            calc_total() {
                // 计算总价格
                let total = 0;
                for (let item in this.cart_list) {
                    if (this.cart_list[item].is_selected) {
                        total += parseFloat(this.cart_list[item].price);
                    }
                }
                this.total = total.toFixed(2);
            },
            get_cart() {
                // 获取购物车商品列表
                this.$axios.get(`${this.$settings.Host}/cart/course/get`, {
                    headers: {
                        "Authorization": "jwt " + this.user_token,
                    }
                }).then(response => {
                    this.cart_list = response.data;
                    this.calc_total();
                }).catch(error => {
                    console.log(error.response)
                });
            },
            deleteHander(course_id) {
                // 删除购物车中商品
                for (let item in this.cart_list) {
                    if (this.cart_list[item].id == course_id) {
                        this.cart_list.splice(item, 1);
                    }
                }
                this.calc_total();
            }
        },
        components: {
            Header,
            Footer,
            CartItem,
        }
    }
</script>

<style scoped>
  .cart_info {
    width: 1200px;
    margin: 0 auto 200px;
  }

  .cart_title {
    margin: 25px 0;
  }

  .cart_title .text {
    font-size: 18px;
    color: #666;
  }

  .cart_title .total {
    font-size: 12px;
    color: #d0d0d0;
  }

  .cart_table {
    width: 1170px;
  }

  .cart_table .cart_head_row {
    background: #F7F7F7;
    width: 100%;
    height: 80px;
    line-height: 80px;
    padding-right: 30px;
  }

  .cart_table .cart_head_row::after {
    content: "";
    display: block;
    clear: both;
  }

  .cart_table .cart_head_row .doing_row,
  .cart_table .cart_head_row .course_row,
  .cart_table .cart_head_row .expire_row,
  .cart_table .cart_head_row .price_row,
  .cart_table .cart_head_row .do_more {
    padding-left: 10px;
    height: 80px;
    float: left;
  }

  .cart_table .cart_head_row .doing_row {
    width: 78px;
  }

  .cart_table .cart_head_row .course_row {
    width: 530px;
  }

  .cart_table .cart_head_row .expire_row {
    width: 188px;
  }

  .cart_table .cart_head_row .price_row {
    width: 162px;
  }

  .cart_table .cart_head_row .do_more {
    width: 162px;
  }

  .cart_footer_row {
    padding-left: 30px;
    background: #F7F7F7;
    width: 100%;
    height: 80px;
    line-height: 80px;
  }

  .cart_footer_row .cart_select span {
    margin-left: 7px;
    font-size: 18px;
    color: #666;
  }

  .cart_footer_row .cart_delete {
    margin-left: 58px;
  }

  .cart_delete .el-icon-delete {
    font-size: 18px;
  }

  .cart_delete span {
    margin-left: 15px;
    cursor: pointer;
    font-size: 18px;
    color: #666;
  }

  .cart_total {
    float: right;
    margin-right: 62px;
    font-size: 18px;
    color: #666;
  }

  .goto_pay {
    float: right;
    width: 159px;
    height: 80px;
    outline: none;
    border: none;
    background: #ffc210;
    font-size: 18px;
    color: #fff;
    text-align: center;
    cursor: pointer;
  }
</style>
