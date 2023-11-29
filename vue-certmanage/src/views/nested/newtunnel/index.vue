<template>
    <div style="padding:80px">
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
                    :on-preview="handlePreview" :on-remove="handleRemove" :before-remove="beforeRemove" multiple :limit="1"
                    :on-exceed="handleExceed" :file-list="fileList">
                    <el-button size="small">点击上传</el-button>
                    <div slot="tip" class="el-upload__tip">上传证书文件(.pem),默认使用本机证书</div>
                </el-upload>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="onSubmit" :loading="testFlag">立即测试</el-button>
                <el-button>取消</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
import { testtunnel } from '@/api/tunnel'

export default {
    data() {
        return {
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
            testFlag: false
        }
    },
    methods: {
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
        }
    }
}
</script>