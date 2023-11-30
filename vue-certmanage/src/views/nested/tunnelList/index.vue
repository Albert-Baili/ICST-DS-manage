<template>
  <div style="padding:30px;">
    <div>
      <el-table stripe fit:true strip :data="tunnels.slice((currentPage - 1) * pageSize, currentPage * pageSize)">
        <el-table-column width="40px" prop="id" label="ID"></el-table-column>
        <el-table-column prop="tunnel_name" label="隧道名称"></el-table-column>
        <el-table-column prop="server_ip" label="目的IP"></el-table-column>
        <el-table-column prop="server_port" label="目的端口"></el-table-column>
        <el-table-column prop="status" label="隧道状态"></el-table-column>
        <el-table-column min-width="150px " prop="created_time" label="创建时间"><template slot-scope="scope">
            <i class="el-icon-time"></i>
            <span style="margin-left: 10px">{{ scope.row.created_time }}</span>
          </template></el-table-column>
        <el-table-column prop="cert_id" label="服务器证书"></el-table-column>
        <el-table-column min-width="100px " label="操作">
          <template slot-scope="scope">
            <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">连接</el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination :current-page="currentPage" :page-sizes="[5, 10, 20, 30, 40]" :page-size="pageSize"
        layout="sizes, prev, pager, next" :prev-text="'上一页'" :next-text="'下一页'" @size-change="handleSizeChange"
        @current-change="handlePageChange"> </el-pagination>
    </div>
    <el-dialog title="隧道通信" :visible.sync="centerDialogVisible" width="30%" center>
      <el-form :model="contentform">
    <el-form-item label="消息内容" :label-width="formLabelWidth">
      <el-input v-model="contentform.info" autocomplete="off"></el-input>
    </el-form-item>

  </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="centerDialogVisible = false">断开</el-button>
        <el-button type="primary" @click="centerDialogVisible = false">发送</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { getalltunnel } from '@/api/tunnel'
export default {
  data() {
    return {
      tunnels: [],
      currentPage: 1,
      pageSize: 10,
      totalItems: 0,
      centerDialogVisible: false,
      contentform:{
        info:''
      }
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      getalltunnel().then(response => {
        this.tunnels = JSON.parse(response.data);
        this.totalItems = this.tunnels.length;
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
    handleEdit(a, b) {
      console.log(a)
      console.log(b)
      this.centerDialogVisible = true
    }
  },
};
</script>

<style>
/* Add any custom styles here */
</style>

  