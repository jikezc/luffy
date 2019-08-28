<template>
  <div class="cart_item">
    <div class="cart_column column_1">
      <el-checkbox class="my_el_checkbox" v-model="cart.is_selected"></el-checkbox>
    </div>
    <div class="cart_column column_2">
      <img :src="cart.course_img" alt="">
      <span><router-link :to="`/course/${cart.id}`">{{cart.name}}</router-link></span>
    </div>
    <div class="cart_column column_3">
      <el-select v-model="expire" size="mini" placeholder="请选择购买有效期" class="my_el_select">
        <el-option v-for="item in cart.expire_list" :label="item.expire_text" :value="item.expire_time"
                   :key="item.expire_time"></el-option>
      </el-select>
    </div>
    <div class="cart_column column_4">¥{{cart.price}}</div>
    <div class="cart_column column_4" @click="deleteHander">删除</div>
  </div>
</template>

<script>
    export default {
        name: "CartItem",
        props: ["cart"],
        watch: {
            "cart.is_selected": function (value) {
                this.selectedChange();
                this.$emit("changeprice");
            },
            "expire": function (value) {
                this.cart.expire_list.forEach((item, key) => {
                    if (item.expire_time == value) {
                        this.cart.price = item.price;

                        // 发送请求
                        this.$axios.put(`${this.$settings.Host}/cart/course/put/`, {
                            course_id: this.cart.id,
                            expire: item.expire_time,
                        }, {
                            headers: {
                                "Authorization": "jwt " + this.check_user_login(),
                            }
                        }).then(response => {
                            console.log(response.data);
                        }).catch(error => {
                            console.log(error.response);
                        })

                    }
                });
                this.$emit("changeprice");
            }
        },
        data() {
            return {
                checked: false,
                expire: -1,
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
            selectedChange() {
                let course_id = this.cart.id;
                let is_selected = this.cart.is_selected;

                this.$axios.patch(`${this.$settings.Host}/cart/course/patch/`, {
                    course_id,  // course_id: course_id
                    is_selected: Boolean(is_selected),
                }, {
                    headers: {
                        "Authorization": "jwt " + this.check_user_login(),
                    },
                }).then(response => {
                    this.$message("切换商品勾选状态成功");
                }).catch(error => {
                    console.log("对不起，切换勾选状态失败！");
                })
            },
            deleteHander() {
                // 删除商品
                // 发送ajax请求，删除当前商品
                this.$axios.delete(`${this.$settings.Host}/cart/course/delete/`, {
                    params: {
                        course_id: this.cart.id,
                    },
                    headers: {
                        "Authorization": "jwt " + this.check_user_login(),
                    },
                }).then(response => {
                    this.$message("移除商品成功！");
                }).catch(error => {
                    this.$message("移除商品发生异常，请联系客服工作人员！");
                })
                // 删除成功以后，通过子组件传递删除状态给父组件，让父组件把当前组件删除
                this.$emit("delete", this.cart.id);
            }
        }
    };
</script>

<style scoped>
  .cart_item::after {
    content: "";
    display: block;
    clear: both;
  }

  .cart_column {
    float: left;
    height: 250px;
  }

  .cart_item .column_1 {
    width: 88px;
    position: relative;
  }

  .my_el_checkbox {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    top: 0;
    margin: auto;
    width: 16px;
    height: 16px;
  }

  .cart_item .column_2 {
    padding: 67px 10px;
    width: 520px;
    height: 116px;
  }

  .cart_item .column_2 img {
    width: 175px;
    height: 115px;
    margin-right: 35px;
    vertical-align: middle;
  }

  .cart_item .column_3 {
    width: 197px;
    position: relative;
    padding-left: 10px;
  }

  .my_el_select {
    width: 117px;
    height: 28px;
    position: absolute;
    top: 0;
    bottom: 0;
    margin: auto;
  }

  .cart_item .column_4 {
    padding: 67px 10px;
    height: 116px;
    width: 142px;
    line-height: 116px;
  }

</style>
