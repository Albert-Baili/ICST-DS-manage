<template>
  <div>
    <el-row>
      <el-col :span="6">
        <el-card style="height: 20%;" shadow="hover">
          <el-col :span="6">
            <i class="el-icon-coin" style="font-size: 250%;padding-left: 10%;" />
            <span style="display: grid;padding-top: 5%;padding-left: 10%;">MySQL</span>
          </el-col>
          <el-col :span="6">
            <span style="font-size: larger;">camanage</span>
            <span style="display: grid;">ID:001</span>
            <el-button type="text" @click="table = true">详情</el-button>
            <el-drawer :visible.sync="table" direction="rtl" size="50%">
              <el-col>
                <i class="el-icon-coin" style="font-size: 300%;padding-left: 5%;" />
                <span style="font-size: 150%;padding-left: 2%;">camanage</span>
                <el-divider content-position="left">
                  <span class="custom-divider-text">基本信息</span>
                </el-divider>
              </el-col>
              <el-descriptions
                class="margin-top"
                :column="2"
                style="padding-left: 5%;padding-top: 8%;font-size: 110%;"
              >
                <el-descriptions-item label="数据库类型">MySQL</el-descriptions-item>
                <el-descriptions-item label="数据库版本">5.6.50-log</el-descriptions-item>
                <el-descriptions-item label="创建人">root</el-descriptions-item>
                <el-descriptions-item label="数据总量">0.16MB</el-descriptions-item>
                <el-descriptions-item label="创建时间">2023年11月20日 15:23:09</el-descriptions-item>
                <el-descriptions-item label="更新时间">2023年12月23日 21:59:34</el-descriptions-item>
                <el-descriptions-item label="描述">
                  <el-button type="primary" icon="el-icon-edit" size="small" />
                </el-descriptions-item>
                <el-descriptions-item label="标签">
                  <el-button type="primary" icon="el-icon-edit" size="small" />
                </el-descriptions-item>
                <el-descriptions-item label="分类">
                  <el-button type="primary" icon="el-icon-edit" size="small" />
                </el-descriptions-item>
                <el-descriptions-item label="分级">
                  <el-button type="primary" icon="el-icon-edit" size="small" />
                </el-descriptions-item>
              </el-descriptions>
              <el-divider content-position="left">
                <span class="custom-divider-text">视图信息</span>
              </el-divider>
            </el-drawer>
          </el-col>

        </el-card>
      </el-col>
    </el-row>

    <el-row>
      <el-col :span="6">
        <el-card style="height: 20%;" shadow="hover">
          <el-col :span="6">
            <i class="el-icon-coin" style="font-size: 250%;padding-left: 10%;" />
            <span style="display: grid;padding-top: 5%;padding-left: 10%;">MySQL</span>
          </el-col>
          <el-col :span="6">
            <span style="font-size: larger;">keyManage</span>
            <span style="display: grid;">ID:002</span>
            <el-button type="text" @click="table = true">详情</el-button>
            <el-drawer :visible.sync="table" direction="rtl" size="50%">
              <el-col>
                <i class="el-icon-coin" style="font-size: 300%;padding-left: 5%;" />
                <span style="font-size: 150%;padding-left: 2%;">camanage</span>
                <el-divider content-position="left">
                  <span class="custom-divider-text">基本信息</span>
                </el-divider>
              </el-col>
              <el-descriptions
                class="margin-top"
                :column="2"
                style="padding-left: 5%;padding-top: 8%;font-size: 110%;"
              >
                <el-descriptions-item label="数据库类型">MySQL</el-descriptions-item>
                <el-descriptions-item label="数据库版本">5.6.50-log</el-descriptions-item>
                <el-descriptions-item label="创建人">root</el-descriptions-item>
                <el-descriptions-item label="数据总量">0.16MB</el-descriptions-item>
                <el-descriptions-item label="创建时间">2023年11月20日 15:23:09</el-descriptions-item>
                <el-descriptions-item label="更新时间">2023年12月23日 21:59:34</el-descriptions-item>
                <el-descriptions-item label="描述">
                  <el-button type="primary" icon="el-icon-edit" size="small" />
                </el-descriptions-item>
                <el-descriptions-item label="标签">
                  <el-button type="primary" icon="el-icon-edit" size="small" />
                </el-descriptions-item>
                <el-descriptions-item label="分类">
                  <el-button type="primary" icon="el-icon-edit" size="small" />
                </el-descriptions-item>
                <el-descriptions-item label="分级">
                  <el-button type="primary" icon="el-icon-edit" size="small" />
                </el-descriptions-item>
              </el-descriptions>
              <el-divider content-position="left">
                <span class="custom-divider-text">视图信息</span>
              </el-divider>
            </el-drawer>
          </el-col>

        </el-card>
      </el-col>
    </el-row>

    <el-row>
      <el-col :span="6">
        <el-card style="height: 20%;" shadow="hover">
          <el-col :span="6">
            <i class="el-icon-coin" style="font-size: 250%;padding-left: 10%;" />
            <span style="display: grid;padding-top: 5%;padding-left: 10%;">MySQL</span>
          </el-col>
          <el-col :span="6">
            <span style="font-size: larger;">systemLog</span>
            <span style="display: grid;">ID:003</span>
            <el-button type="text" @click="table = true">详情</el-button>
            <el-drawer :visible.sync="table" direction="rtl" size="50%">
              <el-col>
                <i class="el-icon-coin" style="font-size: 300%;padding-left: 5%;" />
                <span style="font-size: 150%;padding-left: 2%;">camanage</span>
                <el-divider content-position="left">
                  <span class="custom-divider-text">基本信息</span>
                </el-divider>
              </el-col>
              <el-descriptions
                class="margin-top"
                :column="2"
                style="padding-left: 5%;padding-top: 8%;font-size: 110%;"
              >
                <el-descriptions-item label="数据库类型">MySQL</el-descriptions-item>
                <el-descriptions-item label="数据库版本">5.6.50-log</el-descriptions-item>
                <el-descriptions-item label="创建人">root</el-descriptions-item>
                <el-descriptions-item label="数据总量">0.16MB</el-descriptions-item>
                <el-descriptions-item label="创建时间">2023年11月20日 15:23:09</el-descriptions-item>
                <el-descriptions-item label="更新时间">2023年12月23日 21:59:34</el-descriptions-item>
                <el-descriptions-item label="描述">
                  <el-button type="primary" icon="el-icon-edit" size="small" />
                </el-descriptions-item>
                <el-descriptions-item label="标签">
                  <el-button type="primary" icon="el-icon-edit" size="small" />
                </el-descriptions-item>
                <el-descriptions-item label="分类">
                  <el-button type="primary" icon="el-icon-edit" size="small" />
                </el-descriptions-item>
                <el-descriptions-item label="分级">
                  <el-button type="primary" icon="el-icon-edit" size="small" />
                </el-descriptions-item>
              </el-descriptions>
              <el-divider content-position="left">
                <span class="custom-divider-text">视图信息</span>
              </el-divider>
            </el-drawer>
          </el-col>

        </el-card>
      </el-col>
    </el-row>

    <el-row>
      <el-col :span="6">
        <el-card style="height: 20%;" shadow="hover">
          <el-col :span="6">
            <i class="el-icon-coin" style="font-size: 250%;padding-left: 10%;" />
            <span style="display: grid;padding-top: 5%;padding-left: 10%;">MySQL</span>
          </el-col>
          <el-col :span="6">
            <span style="font-size: larger;">desensiData</span>
            <span style="display: grid;">ID:004</span>
            <el-button type="text" @click="table = true">详情</el-button>
            <el-drawer :visible.sync="table" direction="rtl" size="50%">
              <el-col>
                <i class="el-icon-coin" style="font-size: 300%;padding-left: 5%;" />
                <span style="font-size: 150%;padding-left: 2%;">camanage</span>
                <el-divider content-position="left">
                  <span class="custom-divider-text">基本信息</span>
                </el-divider>
              </el-col>
              <el-descriptions
                class="margin-top"
                :column="2"
                style="padding-left: 5%;padding-top: 8%;font-size: 110%;"
              >
                <el-descriptions-item label="数据库类型">MySQL</el-descriptions-item>
                <el-descriptions-item label="数据库版本">5.6.50-log</el-descriptions-item>
                <el-descriptions-item label="创建人">root</el-descriptions-item>
                <el-descriptions-item label="数据总量">0.16MB</el-descriptions-item>
                <el-descriptions-item label="创建时间">2023年11月20日 15:23:09</el-descriptions-item>
                <el-descriptions-item label="更新时间">2023年12月23日 21:59:34</el-descriptions-item>
                <el-descriptions-item label="描述">
                  <el-button type="primary" icon="el-icon-edit" size="small" />
                </el-descriptions-item>
                <el-descriptions-item label="标签">
                  <el-button type="primary" icon="el-icon-edit" size="small" />
                </el-descriptions-item>
                <el-descriptions-item label="分类">
                  <el-button type="primary" icon="el-icon-edit" size="small" />
                </el-descriptions-item>
                <el-descriptions-item label="分级">
                  <el-button type="primary" icon="el-icon-edit" size="small" />
                </el-descriptions-item>
              </el-descriptions>
              <el-divider content-position="left">
                <span class="custom-divider-text">视图信息</span>
              </el-divider>
            </el-drawer>
          </el-col>

        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  data() {
    return {
      table: false,
      dialog: false,
      loading: false,
      formLabelWidth: '80px',
      timer: null
    }
  },
  methods: {
    handleClose(done) {
      if (this.loading) {
        return
      }
    }
  }
}
</script>

<style scoped>
::v-deep .custom-divider-text {
    font-size: 130%;
}
</style>
