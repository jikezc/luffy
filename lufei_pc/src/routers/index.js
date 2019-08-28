import Vue from "vue"
import Router from "vue-router"

// 这里导入可以让用户访问的组件
import Home from "../components/Home"
import Login from "@/components/Login"
import Register from "../components/Register"
import Courese from "../components/Courese";
import Detail from "../components/Detail";
Vue.use(Router);
import Cart from "@/components/Cart"
import Order from "../components/Order";
import Success from "../components/Success";
import UserOrder from "../components/user/order"
import Player from "../components/Player";

export default new Router({
  // 设置路由模式为"history",去掉默认的#
  mode: "history",
  routes: [
    //路由列表
    {
      name: "Home",
      path: "/",
      component: Home,
    },
    {
      name: "Home",
      path: "/home",
      component: Home,
    },
    {
      name: "Login",
      path: "/user/login",
      component: Login,
    },
    {
      name: "Register",
      path: "/user/register",
      component: Register,
    },
    {
      name: "Course",
      path: "/course",
      component: Courese,
    },
    {
      name: "Detail",
      path: "/course/:course",
      component: Detail,
    },
    {
      name: "Cart",
      path: "/cart",
      component: Cart,
    },
    {
      name: "Order",
      path: "/order",
      component: Order,
    },
    {
      name:"Success",
      path: "/pay/result",
      component: Success,
    },
    {
      name: "UserOrder",
      path: "/user/order",
      component: UserOrder,
    },
    {
      name: "Player",
      path: "/player",
      component: Player,
    }
  ]
})
