<template>
    <div style="padding:30px;">
        <el-tabs v-model="activeName" @tab-click="handleClick">
            <el-tab-pane label="敏感数据识别模板" name="first">
                <el-col :span="4" style="padding-right: 5%;padding-top:1%">
                    <span>ICST数据安全分级分类模板</span>
                    <el-divider></el-divider>
                    <el-tree :data="treedata" show-checkbox default-expand-all node-key="id" ref="tree" highlight-current
                        :props="defaultProps">
                    </el-tree>
                </el-col>
                <el-col :span="20" style="padding-top:1%">
                    <el-row>
                        <el-button type="primary">新建规则</el-button>
                        <el-button type="primary">批量删除</el-button>
                        <el-button type="primary">修改分类</el-button>
                    </el-row>
                    <el-table
                        :data="identifyTable.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
                        style="width: 100%">
                        <el-table-column label="类型名称" prop="identiType">
                        </el-table-column>
                        <el-table-column label="敏感等级" prop="securityLevel">
                            <template slot-scope="scope">
                                <el-tag :type="getTag(scope.row.securityLevel)">
                                    {{ scope.row.securityLevel }}
                                </el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column label="识别算法" prop="识别算法">
                        </el-table-column>
                        <el-table-column label="创建日期" prop="date">
                        </el-table-column>
                        <el-table-column label="具体描述" prop="describe">
                        </el-table-column>
                        <el-table-column label="状态">
                            <template slot-scope="scope">
                                <el-switch v-model="scope.row.status" active-color="#13ce66" inactive-color="#ff4949"
                                    active-value="1" inactive-value="0">
                                </el-switch>
                            </template>
                        </el-table-column>
                        <el-table-column label="操作">
                            <template slot-scope="scope">
                                <el-button size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                                <el-button size="small" type="danger"
                                    @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                            </template>
                        </el-table-column>
                        <el-table-column>
                            <template slot="header" slot-scope="scope">
                                <el-input v-model="search" style="width:50%" size="medium" placeholder="输入关键字搜索" />
                            </template>
                        </el-table-column>
                    </el-table>
                    <div class="block">
                        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
                            :current-page="currentPage" :page-sizes="[10, 20, 30, 40]" :page-size="10"
                            layout="total, sizes, prev, pager, next, jumper" :total="8">
                        </el-pagination>
                    </div>
                </el-col>
            </el-tab-pane>
            <el-tab-pane label="脱敏规则配置" name="second">
                <el-row>
                    <el-button type="primary">新建规则</el-button>
                </el-row>
                <el-table
                    :data="tableData.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
                    style="width: 100%">
                    <el-table-column label="规则名称" prop="规则名称">
                    </el-table-column>
                    <el-table-column label="适用对象" prop="适用对象">
                    </el-table-column>
                    <el-table-column label="脱敏算法" prop="脱敏算法">
                    </el-table-column>
                    <el-table-column label="创建日期" prop="创建日期">
                    </el-table-column>
                    <el-table-column label="执行周期" prop="执行周期">
                    </el-table-column>
                    <el-table-column label="状态">
                        <template slot-scope="scope">
                            <el-switch v-model="scope.row.status" active-color="#13ce66" inactive-color="#ff4949"
                                active-value="1" inactive-value="0">
                            </el-switch>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作">
                        <template slot-scope="scope">
                            <el-button size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                            <el-button size="small" type="danger"
                                @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                        </template>
                    </el-table-column>
                    <el-table-column>
                        <template slot="header" slot-scope="scope">
                            <el-input v-model="search" style="width:80%" size="medium" placeholder="输入关键字搜索" />
                        </template>
                    </el-table-column>
                </el-table>
                <div class="block">
                    <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
                        :current-page="currentPage" :page-sizes="[10, 20, 30, 40]" :page-size="10"
                        layout="total, sizes, prev, pager, next, jumper" :total="8">
                    </el-pagination>
                </div>
            </el-tab-pane>
            <el-tab-pane label="脱敏算法测试" name="third">
                <el-row>
                    <el-button>Hash脱敏</el-button>
                    <el-button>加密脱敏</el-button>
                    <el-button>字符掩盖</el-button>
                    <el-button>截断脱敏</el-button>
                    <el-button>关键字替换</el-button>
                    <el-button>删除脱敏</el-button>
                </el-row>
                <el-form ref="form" :model="yangaiform" label-width="80px" style="width:30%;margin-top:3%;margin-left:10%">
                    <el-form-item label="测试名称">
                        <el-input v-model="yangaiform.name"></el-input>
                    </el-form-item>
                    <el-form-item label="选择规则">
                        <el-select v-model="yangaiform.yangaiRule" placeholder="请选择遮盖规则">
                            <el-option label="保留前x后y" value="1"></el-option>
                            <el-option label="保留自x至y" value="2"></el-option>
                            <el-option label="遮盖前x后y" value="3"></el-option>
                            <el-option label="遮盖自x至y" value="4"></el-option>
                            <el-option label="特殊字符前遮盖" value="5"></el-option>
                            <el-option label="特殊字符后遮盖" value="6"></el-option>
                        </el-select>
                    </el-form-item>                  
                    <el-form-item label="掩盖位置">
                        <el-col :span="10"><el-form-item label="x">
                            <el-input v-model="yangaiform.x"></el-input>
                        </el-form-item></el-col>
                        <el-col :span="10"><el-form-item label="y">
                            <el-input v-model="yangaiform.y"></el-input>
                        </el-form-item></el-col>
                        
                    </el-form-item>
                    <el-form-item label="原始数据">
                        <el-input type="textarea" v-model="yangaiform.origindata" rows="3"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="yangaiSubmit">测试</el-button>
                        <el-button>重置</el-button>
                    </el-form-item>
                    <el-form-item label="脱敏结果">
                        <el-input type="textarea" v-model="yangaiform.tuodata" rows="3"></el-input>
                    </el-form-item>
                </el-form>
            </el-tab-pane>

            <el-tab-pane label="定时任务补偿" name="fourth">定时任务补偿</el-tab-pane>
        </el-tabs>
    </div>
</template>



<script>
import { sendDesensiTest_yangai } from '@/api/tunnel'

export default {
    data() {
        return {
            treedata: [{
                id: 1,
                label: '个人信息',
                children: [{
                    id: 1 - 1,
                    label: '实名认证证明',
                }, {
                    id: 1 - 2,
                    label: '个人一般信息',
                }, {
                    id: 1 - 3,
                    label: '个人隐私信息',
                }, {
                    id: 1 - 4,
                    label: '权威社会标识',
                }, {
                    id: 1 - 5,
                    label: '银行帐号信息',
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
                describe: '记录数据平台网络丢包率',
            },{
                identiType: '运维管理信息',
                识别算法: '规则匹配',
                securityLevel: 'L1',
                date: '2023-11-20',
                describe: '平台普通登录日志',
            },{
                identiType: '终端配置信息',
                识别算法: '规则匹配',
                securityLevel: 'L2',
                date: '2023-11-20',
                describe: '记录终端通信链路配置',
            },{
                identiType: 'IP地址信息',
                识别算法: '规则匹配',
                securityLevel: 'L2',
                date: '2023-11-21',
                describe: '采集终端IP地址',
            },{
                identiType: '个人隐私信息',
                识别算法: 'NLP',
                securityLevel: 'L3',
                date: '2023-11-21',
                describe: '管理员注册用身份信息',
            },{
                identiType: '银行帐号信息',
                识别算法: '规则匹配',
                securityLevel: 'L3',
                date: '2023-11-22',
                describe: '甲方交易帐号',
            },{
                identiType: '公开披露信息',
                识别算法: 'NLP',
                securityLevel: 'L1',
                date: '2023-11-23',
                describe: '企业官网公开数据',
            },{
                identiType: '密钥凭证信息',
                识别算法: '规则匹配',
                securityLevel: 'L3',
                date: '2023-11-24',
                describe: '加解密密钥',
            }],
            activeName: 'second',
            currentPage: 1,
            tableData: [{
                规则名称: '终端配置信息脱敏',
                适用对象: '加密方SM2私钥',
                脱敏算法: 'hash',
                创建日期: '2023-11-24',
                执行周期: '每小时',
                status: '1',
            }, {
                规则名称: '终端配置信息脱敏',
                适用对象: '加密方SM4密钥',
                脱敏算法: 'hash',
                创建日期: '2023-11-25',
                执行周期: '每小时',
                status: '0',
            },
            {
                规则名称: '终端控制指令脱敏',
                适用对象: 'PLC控制命令记录',
                脱敏算法: '字符掩盖',
                创建日期: '2023-11-25',
                执行周期: '每天',
                status: '0',
            },
            {
                规则名称: '原始生产记录脱敏',
                适用对象: 'data_gen_log',
                脱敏算法: '关键字替换',
                创建日期: '2023-11-25',
                执行周期: '每周',
                status: '0',
            },
            {
                规则名称: '终端配置信息脱敏',
                适用对象: '解密方SM4密钥',
                脱敏算法: 'hash',
                创建日期: '2023-11-25',
                执行周期: '每小时',
                status: '0',
            },
            {
                规则名称: '系统运行状态脱敏',
                适用对象: 'System',
                脱敏算法: '截断',
                创建日期: '2023-11-25',
                执行周期: '手动',
                status: '0',
            }, {
                规则名称: 'IP地址信息遮蔽',
                适用对象: '传感器IP',
                脱敏算法: '字符掩盖',
                创建日期: '2023-11-26',
                执行周期: '每周',
                status: '1',
            }, {
                规则名称: '系统网络信息脱敏',
                适用对象: '网络状态数据日志',
                脱敏算法: '关键字替换',
                创建日期: '2023-11-27',
                执行周期: '每手动',
                status: '1',
            }],
            search: '',
            yangaiform: {
                name: '',
                yangaiRule: '',
                origindata: '',
                x: '',
                y: '',
            },
        };
    },
    methods: {
        handleClick(tab, event) {
            console.log(tab, event);
        },
        handleEdit(index, row) {
            console.log(index, row);
        },
        handleDelete(index, row) {
            console.log(index, row);
        },
        handleSizeChange(val) {
            console.log(`每页 ${val} 条`);
        },
        handleCurrentChange(val) {
            console.log(`当前页: ${val}`);
        },
        getTag(securityLevel) {
            switch (securityLevel) {
                case 'L1':
                    return 'success';
                case 'L2':
                    return 'warning';
                case 'L3':
                    return 'danger';
            }
        },
        yangaiSubmit(){
            const headerIn = {
                'name': this.form.name,
                'origindata': this.form.origindata,
                'yangaiRule': this.form.yangaiRule,
                'x': this.form.x,
                'y': this.form.y,
            }
            sendDesensiTest_yangai(headerIn).then(response => {
                console.log(response);
                this.testFlag = false
                this.message = response.data.message;
            })
                .catch(error => {
                    // 处理请求失败的错误信息
                    console.error(error);
                });
        }
    }
};
</script>

<style></style>