<template>
  <div style="padding:30px;">
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="敏感数据识别模板" name="first">
        <el-col :span="4" style="padding-right: 5%;padding-top:1%">
          <span>ICST数据安全分级分类模板</span>
          <el-divider />
          <el-tree
            ref="tree"
            :data="treedata"
            show-checkbox
            default-expand-all
            node-key="id"
            highlight-current
            :props="defaultProps"
          />
        </el-col>
        <el-col :span="20" style="padding-top:1%">
          <el-row>
            <el-button type="primary">新建规则</el-button>
            <el-button type="primary">批量删除</el-button>
            <el-button type="primary">修改分类</el-button>
          </el-row>
          <el-table
            :data="identifyTable.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
            style="width: 100%"
          >
            <el-table-column label="类型名称" prop="identiType" />
            <el-table-column label="敏感等级" prop="securityLevel">
              <template slot-scope="scope">
                <el-tag :type="getTag(scope.row.securityLevel)">
                  {{ scope.row.securityLevel }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="识别算法" prop="识别算法" />
            <el-table-column label="创建日期" prop="date" />
            <el-table-column label="具体描述" prop="describe" />
            <el-table-column label="状态">
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
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
              </template>
            </el-table-column>
            <el-table-column>
              <template slot="header" slot-scope="scope">
                <el-input v-model="search" style="width:50%" size="medium" placeholder="输入关键字搜索" />
              </template>
            </el-table-column>
          </el-table>
          <div class="block">
            <el-pagination
              :current-page="currentPage"
              :page-sizes="[10, 20, 30, 40]"
              :page-size="10"
              layout="total, sizes, prev, pager, next, jumper"
              :total="8"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
        </el-col>
      </el-tab-pane>

      <el-tab-pane label="定时任务补偿" name="fourth">定时任务补偿</el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  data() {
    return {
      treedata: [{
        id: 1,
        label: '个人信息',
        children: [{
          id: 1 - 1,
          label: '实名认证证明'
        }, {
          id: 1 - 2,
          label: '个人一般信息'
        }, {
          id: 1 - 3,
          label: '个人隐私信息'
        }, {
          id: 1 - 4,
          label: '权威社会标识'
        }, {
          id: 1 - 5,
          label: '银行帐号信息'
        }]
      }, {
        id: 2,
        label: '企业信息',
        children: [{
          id: 2 - 1,
          label: '企业内部信息'
        }, {
          id: 2 - 2,
          label: '企业标识信息'
        }, {
          id: 2 - 3,
          label: '公开披露信息'
        }]
      }, {
        id: 3,
        label: '设备信息',
        children: [{
          id: 3 - 1,
          label: 'IP地址信息'
        }, {
          id: 3 - 2,
          label: '终端配置信息'
        }, {
          id: 3 - 3,
          label: '平台配置信息'
        }]
      }, {
        id: 4,
        label: '通用信息',
        children: [{
          id: 4 - 1,
          label: '系统网络信息'
        }, {
          id: 4 - 2,
          label: '密钥凭证信息'
        }, {
          id: 4 - 3,
          label: '运维管理信息'
        }, {
          id: 4 - 4,
          label: '备品备件信息'
        }]
      }],
      defaultProps: {
        children: 'children',
        label: 'label'
      },
      identifyTable: [{
        identiType: '系统网络信息',
        识别算法: '规则匹配',
        securityLevel: 'L1',
        date: '2023-11-20',
        describe: '记录数据平台网络丢包率'
      }, {
        identiType: '运维管理信息',
        识别算法: '规则匹配',
        securityLevel: 'L1',
        date: '2023-11-20',
        describe: '平台普通登录日志'
      }, {
        identiType: '终端配置信息',
        识别算法: '规则匹配',
        securityLevel: 'L2',
        date: '2023-11-20',
        describe: '记录终端通信链路配置'
      }, {
        identiType: 'IP地址信息',
        识别算法: '规则匹配',
        securityLevel: 'L2',
        date: '2023-11-21',
        describe: '采集终端IP地址'
      }, {
        identiType: '个人隐私信息',
        识别算法: 'NLP',
        securityLevel: 'L3',
        date: '2023-11-21',
        describe: '管理员注册用身份信息'
      }, {
        identiType: '银行帐号信息',
        识别算法: '规则匹配',
        securityLevel: 'L3',
        date: '2023-11-22',
        describe: '甲方交易帐号'
      }, {
        identiType: '公开披露信息',
        识别算法: 'NLP',
        securityLevel: 'L1',
        date: '2023-11-23',
        describe: '企业官网公开数据'
      }, {
        identiType: '密钥凭证信息',
        识别算法: '规则匹配',
        securityLevel: 'L3',
        date: '2023-11-24',
        describe: '加解密密钥'
      }],
      activeName: 'second',
      currentPage: 1,
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
    },
    getTag(securityLevel) {
      switch (securityLevel) {
        case 'L1':
          return 'success'
        case 'L2':
          return 'warning'
        case 'L3':
          return 'danger'
      }
    },
    yangaiSubmit() {
      sendDesensiTest_yangai(this.yangaiform).then(response => {
        console.log(response)
        this.yangaiform.tuodata = response.data.result
      })
        .catch(error => {
          // 处理请求失败的错误信息
          console.error(error)
        })
    },
    hashSubmit() {
      sendDesensiTest_hash(this.hashform).then(response => {
        console.log(response)
        this.hashform.tuodata = response.data.result
      })
        .catch(error => {
          // 处理请求失败的错误信息
          console.error(error)
        })
    }
  }
}
</script>

<style>
  .el-textarea.is-disabled .el-textarea__inner{
    color: rgb(25, 25, 25);
  }
</style>
