<template>
    <div style="padding:30px;">
        <div>
            <el-table :data="logs.slice((currentPage-1)*pageSize,currentPage*pageSize)" stripe>
                <el-table-column label="ID" prop="id"></el-table-column>
                <el-table-column label="时间" prop="timestamp"></el-table-column>
                <el-table-column label="消息" prop="logmessage"></el-table-column>
            </el-table>

            <el-pagination :current-page="currentPage" :page-sizes="[10, 20, 30, 40]" :page-size="pageSize"
                layout="sizes, prev, pager, next" :prev-text="'上一页'" :next-text="'下一页'" @size-change="handleSizeChange"
                @current-change="handlePageChange"> </el-pagination>
        </div>
    </div>
</template>
  
<script>
import { getalllogs } from '@/api/log'
export default {
    data() {
        return {
            logs: [], // Initialize an empty array for the certificate list
            totalItems: 0,
            currentPage: 1,
            pageSize: 10,
        };
    },
    methods: {
        fetchData() {
            getalllogs().then(response => {
                this.logs = JSON.parse(response.data);
                this.totalItems = this.logs.length;
            })
                .catch(error => {
                    // 处理请求失败的错误信息
                    console.error(error);
                });
        },
        handleSizeChange(val) {
      console.log(val)
      this.pageSize = val;
      this.currentPage = 1;
    },
    handlePageChange(val) {
      this.currentPage = val;
    },
    },
    mounted() {
        this.fetchData();
    },
};
</script>
    