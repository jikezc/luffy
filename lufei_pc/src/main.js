// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './routers/index';
import settings from './settings'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import "../static/css/reset.css"
import axios from "axios";
import '../static/js/gt.js'
import store from './store/index';

Vue.use(ElementUI);
Vue.config.productionTip = false;
Vue.prototype.$settings = settings;

axios.defaults.withCredentials = false;
Vue.prototype.$axios = axios; // 把对象挂载vue中

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
});

// 注册加载vue-video播放器组件
require('video.js/dist/video-js.css');
require('vue-video-player/src/custom-theme.css');
import VideoPlayer from 'vue-video-player'
// import store from "element-ui/packages/cascader-panel/src/store";
Vue.use(VideoPlayer);
