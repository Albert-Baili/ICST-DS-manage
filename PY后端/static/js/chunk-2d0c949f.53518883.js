(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d0c949f"],{5905:function(e,t,a){"use strict";a.r(t);var n=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticStyle:{padding:"30px"}},[a("div",[a("el-table",{attrs:{data:e.logs.slice((e.currentPage-1)*e.pageSize,e.currentPage*e.pageSize),stripe:""}},[a("el-table-column",{attrs:{label:"ID",prop:"id"}}),a("el-table-column",{attrs:{label:"时间",prop:"timestamp"}}),a("el-table-column",{attrs:{label:"消息",prop:"logmessage"}})],1),a("el-pagination",{attrs:{"current-page":e.currentPage,"page-sizes":[10,20,30,40],"page-size":e.pageSize,layout:"sizes, prev, pager, next","prev-text":"上一页","next-text":"下一页"},on:{"size-change":e.handleSizeChange,"current-change":e.handlePageChange}})],1)])},l=[],r=(a("b64b"),a("b775"));function o(){return Object(r["a"])({url:"/api/log_manage/getalllogs",method:"get"})}var i={data:function(){return{logs:[],totalItems:0,currentPage:1,pageSize:10}},methods:{fetchData:function(){var e=this;o().then((function(t){e.logs=JSON.parse(t.data),e.totalItems=e.logs.length})).catch((function(e){console.error(e)}))},handleSizeChange:function(e){console.log(e),this.pageSize=e,this.currentPage=1},handlePageChange:function(e){this.currentPage=e}},mounted:function(){this.fetchData()}},s=i,c=a("2877"),g=Object(c["a"])(s,n,l,!1,null,null,null);t["default"]=g.exports}}]);