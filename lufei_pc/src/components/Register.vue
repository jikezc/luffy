<template>
  <div class="box">
    <img src="/static/image/Loginbg.3377d0c.jpg" alt="">
    <div class="register">
      <div class="register_box">
        <div class="register-title">注册路飞学城</div>
        <div class="inp">
          <input v-model="mobile" type="text" placeholder="手机号码" class="user">
          <input v-model="password" type="password" placeholder="输入密码" class="user">
          <div class="sms_code">
            <input v-model="sms" maxlength=6 type="text" placeholder="输入验证码" class="user">
            <span class="code_text" @click="sendSMS">{{ sms_tip }}</span>
          </div>
          <div id="geetest"></div>
          <button class="register_btn" @click="registerHander">注册</button>
          <p class="go_login">已有账号
            <router-link to="/user/login">直接登录</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
    export default {
        name: 'Register',
        data() {
            return {
                sms: "",
                mobile: "",
                password: "",
                validateResult: false,
                is_sms: false,
                sms_tip: "点击发送短信"
            }
        },
        created() {
        },
        methods: {
            registerHander: function () {
                // 用户注册
                // 1. 接受验证数据
                if (!/1[3-9]\d{9}/.test(this.mobile)) {
                    this.$message("对不起，手机号有误！");
                }
                if (this.password.length < 6 || this.password.length > 16) {
                    this.$message("对不起，密码必须保持6-16位字符之间");
                }

                if (this.sms.length != 6) {
                    this.$message("对不起，短信验证码有误！");
                }

                // 2. 发送ajax
                this.$axios.post(`${this.$settings.Host}/users/register/`, {
                    mobile: this.mobile,
                    password: this.password,
                    sms_code: this.sms
                }).then(response => {
                    // 保存登录状态
                    sessionStorage.user_id = response.data.id;
                    sessionStorage.user_name = response.data.mobile;
                    sessionStorage.user_token = response.data.token;
                    let self = this;
                    this.$alert("欢迎注册路飞学城！", "注册成功", {
                        callback() {
                            self.$router.push("/");
                        }
                    })
                })
            },
            sendSMS(){
                // 发送短信验证码
                let mobile = this.mobile;
                console.log(mobile);
                if(!/^1[3-9]\d{9}$/.test(mobile)){
                    this.$message("手机号码格式有误！");
                    return; // 阻止代码继续往下执行
                }

                if(this.is_sms){
                    this.$message("对不起，发送短信过于频繁，请在60s后再次发送");
                    return;
                }

                //发送ajax
                this.$axios.get(`${this.$settings.Host}/users/sms/${mobile}`).then(response=>{
                    let interval_time = 60;
                    this.is_sms = true;
                    let timer = setInterval(()=>{
                        if(interval_time < 1){
                            this.is_sms = false;
                            clearInterval(timer);
                            this.sms_tip = "点击发送短信";
                        }else{
                            interval_time--;
                            this.sms_tip = `${interval_time}后再次点击`
                        }
                    },1000);
                    this.$message(response.data.message);
                }).catch(error=>{
                    this.$message(error.response.data.message);
                })
            }
        },

    };
</script>

<style scoped>
  .box {
    width: 100%;
    height: 100%;
    position: relative;
    overflow: hidden;
  }

  .box img {
    width: 100%;
    min-height: 100%;
  }

  .box .register {
    position: absolute;
    width: 500px;
    height: 400px;
    left: 0;
    margin: auto;
    right: 0;
    bottom: 0;
    top: -338px;
  }

  .register .register-title {
    width: 100%;
    font-size: 24px;
    text-align: center;
    padding-top: 30px;
    padding-bottom: 30px;
    color: #4a4a4a;
    letter-spacing: .39px;
  }

  .register-title img {
    width: 190px;
    height: auto;
  }

  .register-title p {
    font-size: 18px;
    color: #fff;
    letter-spacing: .29px;
    padding-top: 10px;
    padding-bottom: 50px;
  }

  .register_box {
    width: 400px;
    height: auto;
    background: #fff;
    box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .5);
    border-radius: 4px;
    margin: 0 auto;
    padding-bottom: 40px;
  }

  .register_box .title {
    font-size: 20px;
    color: #9b9b9b;
    letter-spacing: .32px;
    border-bottom: 1px solid #e6e6e6;
    display: flex;
    justify-content: space-around;
    padding: 50px 60px 0 60px;
    margin-bottom: 20px;
    cursor: pointer;
  }

  .register_box .title span:nth-of-type(1) {
    color: #4a4a4a;
    border-bottom: 2px solid #84cc39;
  }

  .inp {
    width: 350px;
    margin: 0 auto;
  }

  .inp input {
    outline: 0;
    width: 100%;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
  }

  .inp input.user {
    margin-bottom: 16px;
  }

  .inp .rember {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    margin-top: 10px;
  }

  .inp .rember p:first-of-type {
    font-size: 12px;
    color: #4a4a4a;
    letter-spacing: .19px;
    margin-left: 22px;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    /*position: relative;*/
  }

  .inp .rember p:nth-of-type(2) {
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .19px;
    cursor: pointer;
  }

  .inp .rember input {
    outline: 0;
    width: 30px;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
  }

  .inp .rember p span {
    display: inline-block;
    font-size: 12px;
    width: 100px;
    /*position: absolute;*/
    /*left: 20px;*/

  }

  #geetest {
    margin-top: 20px;
  }

  .register_btn {
    width: 100%;
    height: 45px;
    background: #84cc39;
    border-radius: 5px;
    font-size: 16px;
    color: #fff;
    letter-spacing: .26px;
    margin-top: 30px;
  }

  .inp .go_login {
    text-align: center;
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .26px;
    padding-top: 20px;
  }

  .inp .go_login span {
    color: #84cc39;
    cursor: pointer;
  }

  .sms_code {
    position: relative;
  }
  .code_text{
    position: absolute;
    right:14px;
    top: 13px;
    border-left: 1px solid orange;
    padding-left: 14px;
    cursor: pointer;
    background-color: #fff;

  }
</style>
