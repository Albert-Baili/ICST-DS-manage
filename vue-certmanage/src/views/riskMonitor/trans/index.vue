<template>
    <div style="padding-left:2%;padding-top:1%">
        <el-tabs v-model="activeName" @tab-click="handleClick">
            <el-tab-pane label="新建隧道" name="first">
                <el-form ref="form" :model="form" :rules="rules" label-width="150px" size="medium">
                    <el-form-item label="隧道名称" prop="tunnelname">
                        <el-input v-model="form.tunnelname" style="width: 50%;"></el-input>
                    </el-form-item>
                    <el-form-item label="目的IP" style="width: 50%;">
                        <el-input v-model="form.targetip"></el-input>
                    </el-form-item>
                    <el-form-item label="目的端口" style="width: 50%;">
                        <el-input v-model="form.targetport"></el-input>
                    </el-form-item>
                    <el-form-item label="选择客户端证书">
                        <el-upload class="upload-demo" action="https://jsonplaceholder.typicode.com/posts/"
                            :on-preview="handlePreview" :on-remove="handleRemove" :before-remove="beforeRemove" multiple
                            :limit="1" :on-exceed="handleExceed" :file-list="fileList">
                            <el-button size="small">点击上传</el-button>
                            <div slot="tip" class="el-upload__tip">上传证书文件(.pem),默认使用本机证书</div>
                        </el-upload>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="onSubmit" :loading="testFlag">立即测试</el-button>
                        <el-button>取消</el-button>
                    </el-form-item>
                </el-form>
            </el-tab-pane>
            <el-tab-pane label="隧道列表" name="second">
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
                            <el-button size="mini" type="danger"
                                @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                        </template>
                    </el-table-column>
                </el-table>
                <el-pagination :current-page="currentPage" :page-sizes="[5, 10, 20, 30, 40]" :page-size="pageSize"
                    layout="sizes, prev, pager, next" :prev-text="'上一页'" :next-text="'下一页'" @size-change="handleSizeChange"
                    @current-change="handlePageChange"> </el-pagination>
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
            </el-tab-pane>
            <el-tab-pane label="证书管理" name="third">
                <div>
                    <el-table :data="certificates.slice((currentPage - 1) * pageSize, currentPage * pageSize)" stripe>
                        <el-table-column width="40px" label="ID" prop="id" />
                        <el-table-column label="证书名称" prop="common_name" />
                        <el-table-column label="序列号" prop="serial_number" />
                        <!-- <el-table-column label="Organization" prop="organization"></el-table-column>
        <el-table-column label="Organizational Unit" prop="organizational_unit"></el-table-column> -->
                        <!-- Add more columns as needed for other certificate properties -->
                        <el-table-column label="签发者" prop="issuer_common_name" />
                        <el-table-column label="签发时间" prop="valid_from" />
                        <el-table-column label="到期时间" prop="valid_until" />
                        <el-table-column label="添加时间" prop="added_time" />
                        <el-table-column min-width="100px " label="操作">
                            <template slot-scope="scope">
                                <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">下载</el-button>
                                <el-button size="mini" type="danger"
                                    @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
                <el-pagination :current-page="currentPage" :page-sizes="[2, 10, 20, 30, 40]" :page-size="pageSize"
                    layout="sizes, prev, pager, next" :prev-text="'上一页'" :next-text="'下一页'" @size-change="handleSizeChange"
                    @current-change="handlePageChange" />
            </el-tab-pane>

            <el-tab-pane label="链路状态监测" name="fourth">

            </el-tab-pane>
        </el-tabs>
    </div>
</template>


<script>
import { testtunnel } from '@/api/tunnel'
import { getalltunnel } from '@/api/tunnel'
import { getallcert, certDownloadByID } from '@/api/tunnel'

export default {
    data() {
        return {
            activeName: 'first',
            form: {
                tunnelname: 'testtunnel',
                targetip: '127.0.0.1',
                targetport: '7788'
            },
            rules: {
                tunnelname: [
                    { required: true, message: '请输入名称', trigger: 'blur' },
                    { min: 3, max: 12, message: '长度在 3 到 12 个字符', trigger: 'blur' }
                ]
            },
            fileList: [

            ],
            message: '',
            testFlag: false,
            tunnels: [],
            currentPage: 1,
            pageSize: 10,
            totalItems: 0,
            centerDialogVisible: false,
            contentform: {
                info: ''
            },
            certificates: [] // Initialize an empty array for the certificate list
        };
    },
    created() {
        this.fetchData();
    },
    mounted() {
        // Fetch the certificate list when the component is mounted
        this.fetchData()
    },
    methods: {
        handleClick(tab, event) {
            console.log(tab, event);
        },
        onSubmit() {
            this.testFlag = true
            const headerIn = {
                'tunnelname': this.form.tunnelname,
                'targetip': this.form.targetip,
                'targetport': this.form.targetport,
            }
            testtunnel(headerIn).then(response => {
                console.log(response);
                this.testFlag = false
                this.message = response.data.message;
                this.$alert(this.message, "隧道测试结果", {
                    confirmButtonText: '确定',
                });
            })
                .catch(error => {
                    // 处理请求失败的错误信息
                    console.error(error);
                });
        },
        handleRemove(file, fileList) {
            console.log(file, fileList);
        },
        handlePreview(file) {
            console.log(file);
        },
        handleExceed(files, fileList) {
            this.$message.warning(`当前限制选择 3 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
        },
        beforeRemove(file, fileList) {
            return this.$confirm(`确定移除 ${file.name}？`);
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
        },
        fetchData() {
            getalltunnel().then(response => {
                this.tunnels = JSON.parse(response.data);
                this.totalItems = this.tunnels.length;
            })
                .catch(error => {
                    // 处理请求失败的错误信息
                    console.error(error);
                });
            getallcert().then(response => {
                this.certificates = JSON.parse(response.data)
                this.totalItems = this.certificates.length
            })
                .catch(error => {
                    // 处理请求失败的错误信息
                    console.error(error)
                })
        },
        handleEdit(index, row) {
            certDownloadByID(row.id).then(response => {
                // 处理证书文件下载
                // 创建 Blob
                const blob = new Blob([response.data], { type: 'application/x-pem-file' })

                // 创建下载链接
                const downloadUrl = window.URL.createObjectURL(blob)
                const link = document.createElement('a')
                link.href = downloadUrl
                link.setAttribute('download', 'certificate_' + row.id + '.pem') // 设置为动态文件名
                document.body.appendChild(link)
                link.click()
                link.remove()

                // 清除 Blob URL
                window.URL.revokeObjectURL(downloadUrl)
                return // 不再处理响应
            })
        },
    }
};
</script>



<!-- <script>


export default {
    data() {
        return {   
            
        }
    },

    methods: {
        handleClick(tab, event) {
            console.log(tab, event)
        },
        
}
</script> -->