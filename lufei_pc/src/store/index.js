import Vue from 'vue'

import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
  // 数据仓库,类似vue里面的data
  state: {
    // 购物车数据
    cart:{
      total: 0,
    }
  },

  // 数据操作方法,类似vue里面的methods
  mutations: {
     // 修改购物车的商品总数
    get_total(state,data){
      state.cart.total = data;

    }
  }
});
