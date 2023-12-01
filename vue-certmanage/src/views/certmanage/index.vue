<template>
  <div style="padding:30px;">
    <div>
      <el-table :data="certificates.slice((currentPage - 1) * pageSize, currentPage * pageSize)" stripe>
        <el-table-column width="40px" label="ID" prop="id"></el-table-column>
        <el-table-column label="Common Name" prop="common_name"></el-table-column>
        <el-table-column label="序列号" prop="serial_number"></el-table-column>
        <!-- <el-table-column label="Organization" prop="organization"></el-table-column>
        <el-table-column label="Organizational Unit" prop="organizational_unit"></el-table-column> -->
        <!-- Add more columns as needed for other certificate properties -->
        <el-table-column label="签发者" prop="issuer_common_name"></el-table-column>
        <el-table-column label="签发时间" prop="valid_from"></el-table-column>
        <el-table-column label="到期时间" prop="valid_until"></el-table-column>
        <el-table-column label="添加时间" prop="added_time"></el-table-column>
        <el-table-column min-width="100px " label="操作">
          <template slot-scope="scope">
            <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">下载</el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-pagination :current-page="currentPage" :page-sizes="[2, 10, 20, 30, 40]" :page-size="pageSize"
        layout="sizes, prev, pager, next" :prev-text="'上一页'" :next-text="'下一页'" @size-change="handleSizeChange"
        @current-change="handlePageChange"> </el-pagination>
  </div>
</template>

<script>
import { getallcert,certDownloadByID } from '@/api/tunnel'
export default {
  data() {
    return {
      currentPage: 1,
      pageSize: 10,
      totalItems: 0,
      certificates: [], // Initialize an empty array for the certificate list
    };
  },
  methods: {
    fetchData() {
      getallcert().then(response => {
        this.certificates = JSON.parse(response.data);
        this.totalItems = this.certificates.length;
      })
        .catch(error => {
          // 处理请求失败的错误信息
          console.error(error);
        });
    },
    handleEdit(index,row){
      certDownloadByID(row.id).then(response => {
        console.log(response);
      })
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
    // Fetch the certificate list when the component is mounted
    this.fetchData();
  },
};
</script>
  