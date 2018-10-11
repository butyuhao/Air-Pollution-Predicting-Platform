<template>
  <div>
    <el-row>
      <el-col :span="24" class="header">
          {{ sysName }}
      </el-col>
    </el-row>
    <router-view/>
  </div>
</template>

<script>
export default {
  data () {
    return {
      sysName: '天气预测深度学习平台'
    }
  }
}
</script>

<style>
.header {
  line-height: 60px;
  background: #122031;
  color: #fff;
  font-size: 2em;
  text-align: left;
  padding-left: 20px;
}
body{margin:0;padding:0}

</style>
