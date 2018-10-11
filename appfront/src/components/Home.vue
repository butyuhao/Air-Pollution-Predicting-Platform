<template>
  <div class="home">

    <el-row class="el1">
      <el-col :span="12" class="el1-left">
        <el-container>
          <el-header class="el1_header1">天气预测走势</el-header>
          <el-main class="el1_main1">
            <el-row :span="10">
              <ve-line :data="PredictionData" :loading="Preloadings" :data-zoom="{startValue:0, endValue:24}" height="280px" :grid="{ bottom: 38 }" :extend="{series:{label: {position: 'top' }}, 'yAxis.0':{min:0,max:120} }" ></ve-line>

              <!--<el-col :span="4">-->
                <!--<el-upload-->
                  <!--class="avatar-uploader"-->
                  <!--action="https://jsonplaceholder.typicode.com/posts/"-->
                  <!--:show-file-list="false"-->
                  <!--:on-success="handleAvatarSuccess"-->
                  <!--:before-upload="beforeAvatarUpload">-->
                  <!--<img v-if="imageUrl" :src="imageUrl" class="avatar">-->
                  <!--<i v-else class="el-icon-plus avatar-uploader-icon">-->
                  <!--</i>-->
                <!--</el-upload>-->
              <!--</el-col>-->
              <!--<el-col :span="24" style="text-align: center" class="new_upload">-->
                <!--<el-upload-->
                  <!--class="upload-demo"-->
                  <!--action="http://127.0.0.1:8000/api/upload_file"-->
                  <!--:on-preview="handlePreview"-->
                  <!--:before-remove="beforeRemove"-->
                  <!--multiple-->
                  <!--:limit="1"-->
                  <!--:on-exceed="handleExceed"-->
                  <!--&gt;-->
                  <!--<el-button size="small" type="primary">点击上传</el-button>-->
                  <!--&lt;!&ndash;<div slot="tip" class="el-upload__tip" style="margin-top: -250px">只能上传jpg/png文件，且不超过500kb</div>&ndash;&gt;-->
                <!--</el-upload>-->

                <!--&lt;!&ndash;<el-button type="success">文件上传</el-button>&ndash;&gt;-->
                <!--&lt;!&ndash;<el-button type="success">移除文件</el-button>&ndash;&gt;-->
              <!--</el-col>-->
              <!--<el-col :span="9">-->
                  <!--<span style="font-family: Helvetica Neue; font-size: 20px">-->
                    <!--上传状态：<span style="color: cornflowerblue">Null</span>-->
                  <!--</span>-->
              <!--</el-col>-->
            </el-row>
          </el-main>
        </el-container>
      </el-col>
      <el-col :span="12" class="el1-right">
        <el-container>
          <el-header class="el1_header2">数据统计分析</el-header>
          <el-main style="overflow: hidden; z-index: 10">
            <el-row>
              <el-col :span="8">
                <span style="color: black; font-weight: bold">数据散点图</span><br>
                <!--<ve-histogram :data="sampleData" :grid="{ bottom: 0 }" height="260px"></ve-histogram>-->
                <ve-scatter :data="chartData" :grid="{ bottom: 0 }" height="260px" :extend="{xAxis: {type: 'value'}}" :loading="loadings" :settings="{symbolSize: 10}"  :tooltip="tooltip"></ve-scatter>
                <!--<ve-histogram :data="chartData" :setting="{}" :extend="{series:{label: { show: true, position: 'top' }}}" :grid="{ bottom: 0 }" height="260px"></ve-histogram>-->
                <!--<ve-pie :data="chartData" :setting="{}" :extend="{series:{radius: '30%', center: ['50%', 90]}}" :grid="{top:50}" height="150px"></ve-pie>-->
                <!--<img src="" style="width: 125px; height: 126px; margin-top: 10px"/>-->
              </el-col>
              <el-col :span="8">
                <span style="color: black; font-weight: bold">数据特征分布</span><br>
                <ve-line :data="sampleData" :loading="loadings" :data-zoom="{startValue:0, endValue:100}" height="260px" :grid="{ bottom: 38 }" :extend="{series:{}}" @ready="flushParams"></ve-line>
              </el-col>
              <el-col :span="8" style="padding-left: 20px" :v-loading="loadings">
                <span style="color: cornflowerblue; font-weight: bold;">数据统计分析</span><br>
                <span style="color: #2c3e50">特征数量</span>
                  <el-alert
                    :title="counts"
                    type="warning"
                    :closable="false">
                  </el-alert>
                <br>
                <span>训练数据</span>
                <el-alert
                    :title="training"
                    type="error"
                    :closable="false">
                  </el-alert>
                <br>
                <span>测试数据</span>
                <el-alert
                    :title="testing"
                    type="success"
                    :closable="false">
                  </el-alert>
              </el-col>
            </el-row>

          </el-main>
        </el-container>
      </el-col>
    </el-row>

    <el-row class="el2">
      <el-col :span="12" class="el2">
        <el-container>
          <el-header class="el2_header1">模型及其参数选择</el-header>
          <el-main style="height: 320px;border-style: solid;border-width: 1px;border-color: #5b85b7;border-bottom-color: #e2c0c0">
            <el-row>
              <el-col :span="8">
                <span style="color: black; font-weight: bold">模型选择</span><br>
                <el-select v-model="value" placeholder="请选择" style="width: 120px" :onchange="checkAttr(this.value)">
                  <el-option
                    v-for="item in options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                  </el-option>
                </el-select>
                <br>
                <br>
                <span style="color: black; font-weight: bold; margin-top: 150px">数据集选择</span><br>
                <el-select v-model="value2" placeholder="请选择" style="width: 140px" :onchange="checkDataset(this.value2)">
                  <el-option
                    v-for="item in dataset"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                  </el-option>
                </el-select>
                <!--<el-input v-model="input" placeholder="0.3" style="width: 120px"></el-input><br>-->
                <br>
                <br>
                <el-button type="success" @click="analyseSample()">数据分析</el-button>
                <el-button type="danger" @click="visualData()">可视化</el-button>
                <br><br>
                <el-button type="success" @click="startTraining()">开始训练</el-button>
                <!--<el-button type="danger">停止训练</el-button>-->
              </el-col>
              <el-col :span="16">
                <span style="color: black; font-weight: bold">参数选择</span><br>
                 <div v-if="this.checkModel == 'regression'">
                   Weight：<el-input ref="weight" v-model="Weight" placeholder="Weight" style="width: 140px; padding-left: 19px"></el-input><br>
                   Bias：<el-input ref="bias" v-model="Bias" placeholder="Bias" style="width: 140px; padding-left: 39px"></el-input><br>

                </div>
                <div v-if="this.checkModel == 'svm'">
                  参数1：<el-input v-model="input" placeholder="请输入内容" style="width: 120px; padding-left: 19px"></el-input><br>
                  参数2：<el-input v-model="input" placeholder="请输入内容" style="width: 120px; padding-left: 15px"></el-input><br>
                  参数3：<el-input v-model="input" placeholder="请输入内容" style="width: 120px; padding-left: 15px"></el-input><br>
                </div>
                 <div v-if="this.checkModel == 'cnn'">
                  参数1：<el-input v-model="input" placeholder="请输入内容" style="width: 120px; padding-left: 19px"></el-input><br>
                  参数2：<el-input v-model="input" placeholder="请输入内容" style="width: 120px; padding-left: 15px"></el-input><br>
                  参数3：<el-input v-model="input" placeholder="请输入内容" style="width: 120px; padding-left: 15px"></el-input><br>
                </div>
                <div v-if="this.checkModel == 'lstm'">
                  TrainSize：<el-input ref="trainSize" v-model="trainSize" placeholder="TrainSize" style="width: 140px; padding-left: 30px"></el-input><br>
                  NeuronUnit：<el-input ref="neuronUnit" v-model="neuronUnit" placeholder="NeuronUnit" style="width: 140px; padding-left: 15px"></el-input><br>
                  Epochs：<el-input ref="epochs" v-model="epochs" placeholder="Epochs" style="width: 140px; padding-left: 44px"></el-input><br>
                  Batch_Size：<el-input ref="batch_size" v-model="batch_size" placeholder="Batch_Size" style="width: 140px; padding-left: 17px"></el-input><br>
                  LearnRate：<el-input ref="learnRate" v-model="learnRate" placeholder="LearnRate" style="width: 140px; padding-left: 22px"></el-input>
                </div>
                <div v-if="this.checkModel == 'forest'">
                  参数1：<el-input v-model="input" placeholder="请输入内容" style="width: 120px; padding-left: 19px"></el-input><br>
                  参数2：<el-input v-model="input" placeholder="请输入内容" style="width: 120px; padding-left: 15px"></el-input><br>
                  参数3：<el-input v-model="input" placeholder="请输入内容" style="width: 120px; padding-left: 15px"></el-input><br>
                  参数4：<el-input v-model="input" placeholder="请输入内容" style="width: 120px; padding-left: 15px"></el-input><br>
                  参数5：<el-input v-model="input" placeholder="请输入内容" style="width: 120px; padding-left: 15px"></el-input><br>
                  参数6：<el-input v-model="input" placeholder="请输入内容" style="width: 120px; padding-left: 15px"></el-input><br>
                </div>
              </el-col>
            </el-row>

          </el-main>
        </el-container>
      </el-col>
      <el-col :span="12">
        <el-container>
          <el-header class="el2_header2">模型测试结果</el-header>
          <el-main class="el2_main2" style="height: 320px;overflow: hidden">
            <el-row>
              <el-col :span="12">
                <span style="color: black; font-weight: bold">模型结果一</span><br>
                <!--<ve-ring :data="ResultData2" :extend="{series:{radius: '30%', center: ['50%',100]}}" height="280px"></ve-ring>-->
                <ve-line :data="ResultData2" :loading="loadings2" :data-zoom="{}" height="260px" :grid="{ bottom: 38 }" :colors="colors" :toolbox="toolbox"></ve-line>
              </el-col>
              <el-col :span="12" style="padding-left: 30px">
                <span style="color: black; font-weight: bold">模型结果二</span><br>
                <!--<ve-line :data="ResultData" height="180px"></ve-line>-->
                <ve-line :data="ResultData" :loading="loadings3" :data-zoom="{startValue:0, endValue:50}" height="260px" :grid="{ bottom: 38 }" :extend="{series:{label: {position: 'top' }}}" :toolbox="toolbox"></ve-line>
              </el-col>
            </el-row>
          </el-main>
        </el-container>
      </el-col>
    </el-row>

    <el-row class="el3">
      <el-col :span="12">
        <el-container>
          <el-header class="el3_header1">模型训练过程</el-header>
          <el-main style="height: 225px;border-style: solid;border-width: 1px;border-color: #e2c0c0;border-bottom-color: #d3dce6">
            <el-row>
              <el-col :span="24">
                <span style="color: black; font-weight: bold">模型参数</span><br><br>
                <span style="color: #2b81af">{{modelParameters}}</span><br><br>
                <span style="color: black; font-weight: bold">模型状态</span><br><br>
                <span style="color: #2b81af">{{modelStatus}}</span>
              </el-col>
            </el-row>
          </el-main>
        </el-container>
      </el-col>
      <el-col :span="12">
        <el-container>
          <el-header class="el3_header2">模型预测结果</el-header>
          <el-main>
            <el-row>
              <el-col :span="12">
                <span style="color: black; font-weight: bold">预测结果一</span><br><br>
                <span>Training Loss: </span><br>
                <el-alert
                    :title="trainingCost"
                    type="info"
                    :closable="false"
                    style="width: 150px">
                  </el-alert>
                <br>
                <span>Testing Loss: </span><br>
                <el-alert
                    :title="testingCost"
                    type="info"
                    :closable="false"
                    style="width: 150px">
                  </el-alert>
              </el-col>
              <el-col :span="12" style="padding-left: 30px">
                <span style="color: black; font-weight: bold">预测结果二</span><br><br>
                <span>RMSE: </span><br>
                <el-alert
                    :title="RMSEValue"
                    type="info"
                    :closable="false"
                    style="width: 150px">
                  </el-alert>
                <br>
                <span>相关系数: </span><br>
                <el-alert
                    :title="pearsonr"
                    type="info"
                    :closable="false"
                    style="width: 150px">
                  </el-alert>
              </el-col>
            </el-row>
          </el-main>

        </el-container>
      </el-col>
    </el-row>
    <el-footer>上海师范大学天气预测深度学习平台</el-footer>

  </div>
</template>

<script src="../../node_modules/vue/dist/vue.js"></script>
<script src="../../node_modules/echarts/dist/echarts.min.js"></script>
<script src="../../node_modules/v-charts/lib/index.min.js"></script>
<!--<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/vue-resource@1.5.1"></script>-->

<script>
import '../../static/css/style.css'
import 'v-charts/lib/style.css'
import 'echarts/lib/component/toolbox'
import ElRow from "element-ui/packages/row/src/row";
const colorsMap = {
  'TrainLoss': 'red',
  'TestLoss': 'blue'
}
export default {
  components: {ElRow},
  name: 'home',

  data () {
    this.toolbox = {
        feature: {
          // magicType: {type: ['line', 'bar']},
          saveAsImage: {}
        }
    }
    this.tooltip = {
      formatter (v) {
        if(v.seriesName == "Point"){
          return [
            v.seriesName,
            `x: ${v.value[0]}`,
            `y: ${v.value[1]}`
          ].join('<br>')
        }else {
          return [
            v.seriesName,
            `PM2.5: ${v.value[0]}`,
            `PM10: ${v.value[1]}`
          ].join('<br>')
        }
      }
    }
    return {
      loadings: false,
      loadings2: false,
      loadings3: false,
      Preloadings: false,
      Weight: '',
      Bias: '',
      trainSize: '',
      neuronUnit: '',
      epochs : '',
      batch_size: '',
      learnRate : '',
      input: '',
      bookList: [],
      imageUrl: '',
      checkModel: 'regression',
      dataseting: 'pollutant',
      tmpData: '',
      staticData: '',
      countData: '',
      counts: '10000',
      training: '8000',
      testing: '2000',
      tmpCounts: '',
      tmpTraining: '',
      tmpTesting: '',
      tmpChartData: '',
      modelStatus: 'Shutting Down',
      modelParameters:'NULL',
      trainingCost: 'NULL',
      testingCost: 'NULL',
      RMSEValue: 'NULL',
      pearsonr:'NULL',
      tableData: [
        {
            date: '10000',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1518 弄'
        },

      ],
      chartData: {
          columns: ['id', 'x', 'y'],
          rows: [
            { 'id': '1', 'x': 1, 'y': 2},
            { 'id': '2', 'x': 2, 'y': 4},
            { 'id': '3', 'x': 3, 'y': 6},
            { 'id': '4', 'x': 4, 'y': 8},
            { 'id': '5', 'x': 5, 'y': 10},
          ]
      },
      sampleData: {
        columns: ['id', 'x', 'y'],
        rows: [
          {'id': '1', 'x': 1.2, 'y': 2.4},
          {'id': '2', 'x': 2.2, 'y': 3.4},
          {'id': '3', 'x': 3.2, 'y': 4.4},
          {'id': '4', 'x': 4.2, 'y': 5.4},
          {'id': '5', 'x': 5.2, 'y': 6.4}
        ]
      },
      ResultData: {
        columns: ['number', 'RMSE'],
        rows: [
          {'number': '1000', 'RMSE': 90},
          {'number': '2000', 'RMSE': 70},
          {'number': '3000', 'RMSE': 60},
          {'number': '4000', 'RMSE': 48},
          {'number': '5000', 'RMSE': 33},
          {'number': '6000', 'RMSE': 24},
          {'number': '7000', 'RMSE': 19},
          {'number': '8000', 'RMSE': 15},
          {'number': '9000', 'RMSE': 13},
          {'number': '10000', 'RMSE': 12},
          {'number': '11000', 'RMSE': 11},
          {'number': '12000', 'RMSE': 10},
        ]
      },
      ResultData2: {
        columns: ['number', 'TrainLoss', 'TestLoss'],
        rows: [
          {'number': '1000', 'TrainLoss': 35, 'TestLoss': 34},
          {'number': '2000', 'TrainLoss': 25, 'TestLoss': 24},
          {'number': '3000', 'TrainLoss': 12, 'TestLoss': 11},
          {'number': '4000', 'TrainLoss': 8.3, 'TestLoss': 7.2},
          {'number': '5000', 'TrainLoss': 7, 'TestLoss': 6},
          {'number': '6000', 'TrainLoss': 6, 'TestLoss': 5},
          {'number': '7000', 'TrainLoss': 5, 'TestLoss': 4},
          {'number': '8000', 'TrainLoss': 4, 'TestLoss': 3},
          {'number': '9000', 'TrainLoss': 3, 'TestLoss': 3},
          {'number': '10000', 'TrainLoss': 2.5, 'TestLoss': 2.3},
          {'number': '11000', 'TrainLoss': 2.2, 'TestLoss': 2.1},
          {'number': '12000', 'TrainLoss': 2, 'TestLoss': 1.9},
        ]
      },

      PredictionData: {
        columns: ['time', '24小时', '72小时', '一周'],
        rows: [
          {'time':'6-3/12:00', '24小时': 75, '72小时': 70, '一周': 65},
          {'time':'6-3/13:00', '24小时': 73, '72小时': 71, '一周': 63},
          {'time':'6-3/14:00', '24小时': 114,'72小时': 102,'一周': 104},
          {'time':'6-3/15:00', '24小时': 48, '72小时': 36, '一周': 38},
          {'time':'6-3/16:00', '24小时': 42, '72小时': 31, '一周': 32},
          {'time':'6-3/17:00', '24小时': 62, '72小时': 51, '一周': 42},
          {'time':'6-3/18:00', '24小时': 39, '72小时': 37, '一周': 36},
          {'time':'6-3/19:00', '24小时': 68, '72小时': 66, '一周': 62},
          {'time':'6-3/20:00', '24小时': 50, '72小时': 47, '一周': 42},
          {'time':'6-3/21:00', '24小时': 49, '72小时': 47, '一周': 42},
          {'time':'6-3/22:00', '24小时': 48, '72小时': 45, '一周': 40},
          {'time':'6-3/23:00', '24小时': 68, '72小时': 65, '一周': 61},
          {'time':'6-4/0:00', '24小时':  26, '72小时': 28, '一周': 21},
          {'time':'6-4/1:00', '24小时':  45, '72小时': 43, '一周': 38},
          {'time':'6-4/2:00', '24小时':  66, '72小时': 63, '一周': 58},
          {'time':'6-4/3:00', '24小时':  35, '72小时': 32, '一周': 27},
          {'time':'6-4/4:00', '24小时':  25, '72小时': 23, '一周': 16},
          {'time':'6-4/5:00', '24小时':  37, '72小时': 36, '一周': 31},
          {'time':'6-4/6:00', '24小时':  29, '72小时': 26, '一周': 20},
          {'time':'6-4/7:00', '24小时':  24, '72小时': 23, '一周': 17},
          {'time':'6-4/8:00', '24小时':  43, '72小时': 41, '一周': 36},
          {'time':'6-4/9:00', '24小时':  49, '72小时': 47, '一周': 41},
          {'time':'6-4/10:00', '24小时': 35, '72小时': 34, '一周': 28},
          {'time':'6-4/11:00', '24小时': 39, '72小时': 38, '一周': 32},
          {'time':'6-4/12:00', '24小时': 24, '72小时': 23, '一周': 19},
          {'time':'6-4/13:00', '24小时': '', '72小时': 33, '一周': 40},
          {'time':'6-4/14:00', '24小时': '', '72小时': 30, '一周': 42},
          {'time':'6-4/15:00', '24小时': '', '72小时': 16, '一周': 32},
          {'time':'6-4/16:00', '24小时': '', '72小时': 10, '一周': 21},
          {'time':'6-4/17:00', '24小时': '', '72小时': 10, '一周': 8},
          {'time':'6-4/18:00', '24小时': '', '72小时': 50, '一周': 38},
          {'time':'6-4/19:00', '24小时': '', '72小时': 45, '一周': 30},
          {'time':'6-4/20:00', '24小时': '', '72小时': 40, '一周': 28},
          {'time':'6-4/21:00', '24小时': '', '72小时': 16, '一周': 26},
          {'time':'6-4/22:00', '24小时': '', '72小时': 25, '一周': 71},
          {'time':'6-4/23:00', '24小时': '', '72小时': 68, '一周': 60},
          {'time':'6-5/0:00', '24小时':  '', '72小时': 25, '一周': 9},
          {'time':'6-5/1:00', '24小时':  '', '72小时': 8,  '一周': 8},
          {'time':'6-5/2:00', '24小时':  '', '72小时': 10, '一周': 24},
          {'time':'6-5/3:00', '24小时':  '', '72小时': 22, '一周': 36},
          {'time':'6-5/4:00', '24小时':  '', '72小时': 17, '一周': 29},
          {'time':'6-5/5:00', '24小时':  '', '72小时': 48, '一周': 38},
          {'time':'6-5/6:00', '24小时':  '', '72小时': 56, '一周': 49},
          {'time':'6-5/7:00', '24小时':  '', '72小时': 19, '一周': 34},
          {'time':'6-5/8:00', '24小时':  '', '72小时': 39, '一周': 42},
          {'time':'6-5/9:00', '24小时':  '', '72小时': 15, '一周': 28},
          {'time':'6-5/10:00', '24小时': '', '72小时': 17, '一周': 43},
          {'time':'6-5/11:00', '24小时': '', '72小时': 37, '一周': 49},
          {'time':'6-5/12:00', '24小时': '', '72小时': 26, '一周': 22},
          {'time':'6-5/13:00', '24小时': '', '72小时': '', '一周': 38},
          {'time':'6-5/14:00', '24小时': '', '72小时': '', '一周': 18},
          {'time':'6-5/15:00', '24小时': '', '72小时': '', '一周': 29},
          {'time':'6-5/16:00', '24小时': '', '72小时': '', '一周': 63},
          {'time':'6-5/17:00', '24小时': '', '72小时': '', '一周': 21},
          {'time':'6-5/18:00', '24小时': '', '72小时': '', '一周': 50},
          {'time':'6-5/19:00', '24小时': '', '72小时': '', '一周': 84},
          {'time':'6-5/20:00', '24小时': '', '72小时': '', '一周': 66},
          {'time':'6-5/21:00', '24小时': '', '72小时': '', '一周': 18},
          {'time':'6-5/22:00', '24小时': '', '72小时': '', '一周': 36},
          {'time':'6-5/23:00', '24小时': '', '72小时': '', '一周': 47},
          {'time':'6-6/0:00', '24小时':  '', '72小时': '', '一周': 31},
          {'time':'6-6/1:00', '24小时':  '', '72小时': '', '一周': 21},
          {'time':'6-6/2:00', '24小时':  '', '72小时': '', '一周': 21},
          {'time':'6-6/3:00', '24小时':  '', '72小时': '', '一周': 22},
          {'time':'6-6/4:00', '24小时':  '', '72小时': '', '一周': 19},
          {'time':'6-6/5:00', '24小时':  '', '72小时': '', '一周': 41},
          {'time':'6-6/6:00', '24小时':  '', '72小时': '', '一周': 52},
          {'time':'6-6/7:00', '24小时':  '', '72小时': '', '一周': 36},
          {'time':'6-6/8:00', '24小时':  '', '72小时': '', '一周': 32},
          {'time':'6-6/9:00', '24小时':  '', '72小时': '', '一周': 22},
          {'time':'6-6/10:00', '24小时': '', '72小时': '', '一周': 10},
          {'time':'6-6/11:00', '24小时': '', '72小时': '', '一周': 17},
          {'time':'6-6/12:00', '24小时': '', '72小时': '', '一周': 16},
          {'time':'6-6/13:00', '24小时': '', '72小时': '', '一周': 12},
          {'time':'6-6/14:00', '24小时': '', '72小时': '', '一周': 19},
          {'time':'6-6/15:00', '24小时': '', '72小时': '', '一周': 39},
          {'time':'6-6/16:00', '24小时': '', '72小时': '', '一周': 14},
          {'time':'6-6/17:00', '24小时': '', '72小时': '', '一周': 12},
          {'time':'6-6/18:00', '24小时': '', '72小时': '', '一周': 20},
          {'time':'6-6/19:00', '24小时': '', '72小时': '', '一周': 37},
          {'time':'6-6/20:00', '24小时': '', '72小时': '', '一周': 58},
          {'time':'6-6/21:00', '24小时': '', '72小时': '', '一周': 49},
          {'time':'6-6/22:00', '24小时': '', '72小时': '', '一周': 24},
          {'time':'6-6/23:00', '24小时': '', '72小时': '', '一周': 51},
          {'time':'6-7/0:00', '24小时':  '', '72小时': '', '一周': 35},
          {'time':'6-7/1:00', '24小时':  '', '72小时': '', '一周': 19},
          {'time':'6-7/2:00', '24小时':  '', '72小时': '', '一周': 41},
          {'time':'6-7/3:00', '24小时':  '', '72小时': '', '一周': 61},
          {'time':'6-7/4:00', '24小时':  '', '72小时': '', '一周': 48},
          {'time':'6-7/5:00', '24小时':  '', '72小时': '', '一周': 34},
          {'time':'6-7/6:00', '24小时':  '', '72小时': '', '一周': 26},
          {'time':'6-7/7:00', '24小时':  '', '72小时': '', '一周': 27},
          {'time':'6-7/8:00', '24小时':  '', '72小时': '', '一周': 25},
          {'time':'6-7/9:00', '24小时':  '', '72小时': '', '一周': 33},
          {'time':'6-7/10:00', '24小时': '', '72小时': '', '一周': 18},
          {'time':'6-7/11:00', '24小时': '', '72小时': '', '一周': 11},
          {'time':'6-7/12:00', '24小时': '', '72小时': '', '一周': 26},
          {'time':'6-7/13:00', '24小时': '', '72小时': '', '一周': 32},
          {'time':'6-7/14:00', '24小时': '', '72小时': '', '一周': 11},
          {'time':'6-7/15:00', '24小时': '', '72小时': '', '一周': 43},
          {'time':'6-7/16:00', '24小时': '', '72小时': '', '一周': 28},
          {'time':'6-7/17:00', '24小时': '', '72小时': '', '一周': 25},
          {'time':'6-7/18:00', '24小时': '', '72小时': '', '一周': 39},
          {'time':'6-7/19:00', '24小时': '', '72小时': '', '一周': 37},
          {'time':'6-7/20:00', '24小时': '', '72小时': '', '一周': 16},
          {'time':'6-7/21:00', '24小时': '', '72小时': '', '一周': 23},
          {'time':'6-7/22:00', '24小时': '', '72小时': '', '一周': 23},
          {'time':'6-7/23:00', '24小时': '', '72小时': '', '一周': 26},
          {'time':'6-8/0:00', '24小时':  '', '72小时': '', '一周': 24},
          {'time':'6-8/1:00', '24小时':  '', '72小时': '', '一周': 15},
          {'time':'6-8/2:00', '24小时':  '', '72小时': '', '一周': 13},
          {'time':'6-8/3:00', '24小时':  '', '72小时': '', '一周': 25},
          {'time':'6-8/4:00', '24小时':  '', '72小时': '', '一周': 30},
          {'time':'6-8/5:00', '24小时':  '', '72小时': '', '一周': 25},
          {'time':'6-8/6:00', '24小时':  '', '72小时': '', '一周': 21},
          {'time':'6-8/7:00', '24小时':  '', '72小时': '', '一周': 12},
          {'time':'6-8/8:00', '24小时':  '', '72小时': '', '一周': 15},
          {'time':'6-8/9:00', '24小时':  '', '72小时': '', '一周': 14},
          {'time':'6-8/10:00', '24小时': '', '72小时': '', '一周': 25},
          {'time':'6-8/11:00', '24小时': '', '72小时': '', '一周': 19},
          {'time':'6-8/12:00', '24小时': '', '72小时': '', '一周': 33},
          {'time':'6-8/13:00', '24小时': '', '72小时': '', '一周': 26},
          {'time':'6-8/14:00', '24小时': '', '72小时': '', '一周': 40},
          {'time':'6-8/15:00', '24小时': '', '72小时': '', '一周': 27},
          {'time':'6-8/16:00', '24小时': '', '72小时': '', '一周': 16},
          {'time':'6-8/17:00', '24小时': '', '72小时': '', '一周': 8},
          {'time':'6-8/18:00', '24小时': '', '72小时': '', '一周': 14},
          {'time':'6-8/19:00', '24小时': '', '72小时': '', '一周': 15},
          {'time':'6-8/20:00', '24小时': '', '72小时': '', '一周': 18},
          {'time':'6-8/21:00', '24小时': '', '72小时': '', '一周': 17},
          {'time':'6-8/22:00', '24小时': '', '72小时': '', '一周': 17},
          {'time':'6-8/23:00', '24小时': '', '72小时': '', '一周': 13},
          {'time':'6-9/0:00', '24小时':  '', '72小时': '', '一周': 11},
          {'time':'6-9/1:00', '24小时':  '', '72小时': '', '一周': 14},
          {'time':'6-9/2:00', '24小时':  '', '72小时': '', '一周': 8},
          {'time':'6-9/3:00', '24小时':  '', '72小时': '', '一周': 14},
          {'time':'6-9/4:00', '24小时':  '', '72小时': '', '一周': 30},
          {'time':'6-9/5:00', '24小时':  '', '72小时': '', '一周': 13},
          {'time':'6-9/6:00', '24小时':  '', '72小时': '', '一周': 13},
          {'time':'6-9/7:00', '24小时':  '', '72小时': '', '一周': 12},
          {'time':'6-9/8:00', '24小时':  '', '72小时': '', '一周': 18},
          {'time':'6-9/9:00', '24小时':  '', '72小时': '', '一周': 30},
          {'time':'6-9/10:00', '24小时': '', '72小时': '', '一周': 41},
          {'time':'6-9/11:00', '24小时': '', '72小时': '', '一周': 26},
          {'time':'6-9/12:00', '24小时': '', '72小时': '', '一周': 9},
          {'time':'6-9/13:00', '24小时': '', '72小时': '', '一周': 8},
          {'time':'6-9/14:00', '24小时': '', '72小时': '', '一周': 14},

        ]

      },

      options: [ {
          value: 'lstm',
          label: 'LSTM'
        }],

      dataset: [
        {
          value: 'pollutant',
          label: '污染物数据集'
        },
      ],
      value: 'regression',
      value2: 'regression'
    }

  },
  computed: {
        colors () {
          return this.ResultData2.columns.slice(1).map(item => colorsMap[item])
        }
  },
  methods: {
      handlePreview(file) {
        console.log(file);
      },
      handleExceed(files, fileList) {
        this.$message.warning(`当前限制选择 1 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
      },
      beforeRemove(file, fileList) {
        return this.$confirm(`确定移除 ${ file.name }？`);
      },
      handleAvatarSuccess(res, file) {
        this.imageUrl = URL.createObjectURL(file.raw);
      },
      beforeAvatarUpload(file) {
        const isJPG = file.type === 'image/jpeg';
        const isLt2M = file.size / 1024 / 1024 < 2;

        if (!isJPG) {
          this.$message.error('上传头像图片只能是 JPG 格式!');
        }
        if (!isLt2M) {
          this.$message.error('上传头像图片大小不能超过 2MB!');
        }
        return isJPG && isLt2M;
      },
      checkAttr(res) {
        this.checkModel = res.valueOf();
      },
      checkDataset(res) {
        this.dataseting = res.valueOf()
      },
      flushParams() {
        // this.loadings = false;
      },
      visualData() {
        if(this.tmpData != ""){
          this.sampleData = this.tmpData
          this.counts = this.tmpCounts
          this.training = this.tmpTraining
          this.testing = this.tmpTesting
          this.chartData = this.tmpChartData
        }else {
          this.$message.error("请先进行数据分析")
        }

      },
      analyseSample() {
        var selectModel = this.checkModel
        var selectDataset = this.dataseting
        var path = 'http://127.0.0.1:8000/api/analyseSample'
        if(selectModel == 'regression' && selectDataset == 'regression') {
          var url = path + '?model=' + selectModel +  "&dataset=" + selectDataset
        }else if(selectModel == 'lstm' && selectDataset == 'pollutant'){
          var url = path + '?model=' + selectModel +  "&dataset=" + selectDataset
        }else {
          this.$message.error("请正确选择相应的模型和数据集")
          return
        }
        this.loadings = true
        this.modelStatus = "Data Analazying"
        this.$http.get(url)
        .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (res.error_num == 0) {
              this.tmpData = res.result
              this.tmpChartData = res.result2
              this.tmpCounts = res.static.counts
              this.tmpTraining = res.static.training
              this.tmpTesting = res.static.testing
              this.loadings = false
              this.$message.success("分析成功")
            } else {
              this.$message.error('分析失败，请重试')
              console.log(res['msg'])
            }
            this.flushParams()
        })
      },

      startTraining() {
         var model = this.checkModel
         var dataset = this.dataseting
         var path = 'http://127.0.0.1:8000/api/startTraining'
         if(model == 'regression' && dataset == 'regression') {
           this.loadings2 = true
           var weight = this.$refs.weight.value
           var bias = this.$refs.bias.value
           var url = path + '?model=' + model +  "&dataset=" + dataset + "&weight=" + weight + "&bias=" + bias
           this.modelParameters = '{"Weight":'+parseInt(weight)+',"Bias":'+parseInt(bias)+'}'
           if(weight == "" || bias == "") {
             this.loadings2 = false
             this.$message.error("请输入相应参数的值")
             return 0;
           }
         }else if(model == 'lstm' && dataset == 'pollutant'){
           this.loadings2 = true
           this.loadings3 = true
           this.Preloadings = true
           var trainSize = this.$refs.trainSize.value
           var neuronUnit = this.$refs.neuronUnit.value
           var epochs = this.$refs.epochs.value
           var batch_size = this.$refs.batch_size.value
           var learnRate = this.$refs.learnRate.value
           this.modelParameters = '{"TotalSize":'+parseInt(trainSize)+',"NeuronUnit":'+parseInt(neuronUnit)+',"Epochs":'+parseInt(epochs)+',"batch_size":'+parseInt(batch_size)+',"learnRate":'+parseInt(learnRate)+'}'
           var url = path + '?model=' + model +  "&dataset=" + dataset + "&TrainSize=" + trainSize +
             "&NeuronUnit=" + neuronUnit + "&Epochs=" + epochs + "&Batch_Size=" + batch_size + "&LearnRate=" + learnRate
           if(trainSize == "" || neuronUnit == "" || epochs == "" || batch_size == "" || learnRate == "") {
             this.loadings2 = false
             this.loadings3 = false
             this.Preloadings = false
             this.$message.error("请输入相应参数的值")
             return
           }
         }else {
            this.$message.error("请正确选择相应的模型和数据集")
            return
         }

         this.modelStatus = "Training"
         this.$http.get(url)
        .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (res.error_num == 0) {
              this.loadings2 = false
              this.loadings3 = false
              this.Preloadings = false
              this.modelStatus = "Finished"
              this.modelParameters = res.modelParameters
              this.trainingCost = res.resultStatic.trainingCost.toFixed(5)
              this.testingCost = res.resultStatic.testingCost.toFixed(5)
              this.RMSEValue = res.resultStatic.RMSE.toFixed(5)
              if(res.resultStatic.pearsonr != "") {
                this.pearsonr = res.resultStatic.pearsonr.toFixed(5)
              }
              this.ResultData2 = res.ResultData2
              this.ResultData = res.ResultData
              this.PredictionData = res.resultPrediction
              this.$message.success("训练成功")
            } else {
              this.$message.error('训练失败，请重试')
              location.reload()
              console.log(res['msg'])
            }
        })
      }

    }
}
</script>

<style scoped lang="scss">

  .el-table {
    font-size: 10px;
  }

  .el-table-column {
    background-color: blue !important;
  }

  .el-row {
    &:last-child {
      margin-bottom: 0;
    }
  }
  .el-col {
    border-radius: 4px;
  }
  .bg-purple-dark {
    background: #99a9bf;
  }
  .bg-purple {
    background: #d3dce6;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }

  p{margin:0;padding:0}

  .el-header {
    border-radius: 5px;
    height: 35px !important;
    background-color: #5b85b7;
    color: #f9fafc;
    text-align: left;
    line-height: 35px;
  }

  .el1 .el1_header2 {
     background-color: #cee8ee;
     color: #5b85b7;
  }
  .el1 .el1_main1 {
    line-height: 279px;
    border-style: solid;
    border-width: 1px;
    border-color: #5b85b7;
  }
  .el2 .el2_header2 {
     background-color: #beceaa;
     color: green;
  }

  .el2 .el2_main1 {
    line-height: 200px;
    border-style: solid;
    border-width: 1px;
    border-color: #5b85b7;
    border-bottom-color: #e2c0c0;
  }

  .el3 .el3_header1 {
     background-color: #e2c0c0;
    color: #af4451;
  }

  .el3 .el3_header2 {
     background-color: #2b81af;
  }

  .el-footer{
    background-color: #303133;
    color: #f3d19e;
    text-align: center;
    line-height: 60px;
  }

  .el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
  }

  .el-main {
    background-color: #E9EEF3;
    color: #333;
    /*text-align: center;*/
    /*line-height: 160px;*/
  }

  .el-button {
    padding: 5px;
    font-size: 16px;
    border-radius: 5px;
  }

  .avatar-uploader {
    border: 1px dashed #303133;
    border-radius: 6px;
    cursor: pointer;
    width: 120px;
    height: 230px;
    /*position: relative;*/
    /*overflow: hidden;*/
    margin-top: 20px;
  }

  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }
  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 18px;
    height: 68px;
    line-height: 68px;
    padding-left: 45px;
    bottom: 100px;
  }
  .avatar {
    width: 168px;
    height: 168px;
    display: block;
  }

  body > .el-container {
    margin-bottom: 40px;
  }

  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }

  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }
</style>
