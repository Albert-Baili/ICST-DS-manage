<template>
  <div style="padding:30px;">
    <div>
      <el-table
        :data="tableData.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
        style="width: 100%"
      >
        <el-table-column label="资产名称" prop="asset_name" />
        <el-table-column label="资产类型" prop="asset_type" />
        <el-table-column label="所在地区" prop="location" />
        <el-table-column label="创建日期" prop="创建日期" />
        <el-table-column label="总数据量" prop="amount" />
        <el-table-column label="连接状态">
          <template slot-scope="scope">
            <el-switch
              v-model="scope.row.status"
              active-color="#13ce66"
              inactive-color="#ff4949"
              active-value="1"
              inactive-value="0"
            />
          </template>
        </el-table-column>
        <el-table-column label="功能状态" prop="function" />
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
        <el-table-column>
          <template slot="header" slot-scope="scope">
            <el-input v-model="search" style="width:80%" size="medium" placeholder="输入关键字搜索" />
          </template>
        </el-table-column>
      </el-table>
      <div class="block">
        <el-pagination
          :current-page="currentPage"
          :page-sizes="[5, 10, 20, 30, 40]"
          :page-size="pageSize"
          layout="sizes, prev, pager, next"
          :prev-text="'上一页'"
          :next-text="'下一页'"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { sendDesensiTest_yangai, sendDesensiTest_hash } from '@/api/desensiTest'

export default {
  data() {
    return {
      defaultProps: {
        children: 'children',
        label: 'label'
      },
      tableData: [{
        asset_name: '传感数据库',
        asset_type: 'RDS',
        location: '四川-成都',
        创建日期: '2023-11-24',
        amount: '1.24GB',
        status: '1',
        function: '读写'
      }, {
        asset_name: 'PLC指令数据库',
        asset_type: 'RDS',
        location: '四川-成都',
        创建日期: '2023-11-25',
        amount: '41.47MB',
        status: '0',
        function: '读写'
      },
      {
        asset_name: '研发数据库',
        asset_type: 'Redis',
        location: '四川-绵阳',
        创建日期: '2023-11-25',
        amount: '20.58GB',
        status: '0',
        function: '只读'
      },
      {
        asset_name: '管理数据库',
        asset_type: 'Redis',
        location: '四川-乐山',
        创建日期: '2023-11-25',
        amount: '310.02MB',
        status: '0',
        function: '读写'
      },
      {
        asset_name: '设备资产数据库',
        asset_type: 'RDS',
        location: '四川-德阳',
        创建日期: '2023-11-25',
        amount: '58.89MB',
        status: '0',
        function: '只读'
      }
      ],
      search: ''
    }
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event)
    },
    handleEdit(index, row) {
      console.log(index, row)
    },
    handleDelete(index, row) {
      console.log(index, row)
    },
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`)
    },
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
    }
  }
}
</script>
