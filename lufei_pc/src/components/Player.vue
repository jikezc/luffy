<template>
    <div class="player">
      <div id="player"></div>
    </div>
</template>

<script>
export default {
  name:"Player",
  data () {
    return {

    }
  },
  methods: {
      check_login(){
        // 检查当前访问者是否登录了！
        let token = localStorage.user_token || sessionStorage.user_token;
        if( !token ){
          this.$alert("对不起，您尚未登录，请登录以后再进行购物车").then(()=>{
            this.$router.push("/user/login");
          });
          return false; // 阻止代码往下执行
        }
        return token;
      },
      init_player(){
        // 保利威html5视频播放器初始化
        // 验证用户是否登录
        let token = this.check_login();
        let user_name = localStorage.user_name || sessionStorage.user_name;
        let _this = this;
        // 获取vid参数
        let vid = this.$route.query.vid;
        if(!vid){
            this.$message("对不起，当前视频不存在！");
            return false;
        }
        var player = polyvObject('#player').videoPlayer({
            wrap: '#player',
            width: document.documentElement.clientWidth-260, // 页面宽度
            height: document.documentElement.clientHeight, // 页面高度
            forceH5: true,
            vid: vid,
            code: user_name, // 一般是用户昵称
            // 视频加密播放的配置
            playsafe: function (vid, next) { // 向后端发送请求获取加密的token
                _this.$axios.get(`${_this.$settings.Host}/courses/polyv/token/`,{
                  params:{
                    vid: vid,
                  },
                  headers:{
                    "Authorization":"jwt " + token,
                  }
                }).then(function (response) {
                    console.log(response);
                    next(response.data.token);
                });
            }
        });
      }
  },
  mounted(){
    this.init_player();
  },
  computed: {
  }
}
</script>

<style scoped>
</style>
