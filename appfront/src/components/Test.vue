<template>
  <div class="home">
    <el-row display="margin-top:10px">
        <el-input v-model="input" placeholder="请输入书名" style="display:inline-table; width: 30%; float:left"></el-input>
        <el-button type="primary" @click="addBook()" style="float:left; margin: 2px;">新增</el-button>
    </el-row>
    <el-row>
        <el-table :data="bookList" style="width: 100%" border>
          <el-table-column prop="id" label="编号" min-width="100">
            <template slot-scope="scope"> {{ scope.row.pk }} </template>
          </el-table-column>
          <el-table-column prop="book_name" label="书名" min-width="100">
            <template slot-scope="scope"> {{ scope.row.fields.book_name }} </template>
          </el-table-column>
          <el-table-column prop="add_time" label="添加时间" min-width="100">
            <template slot-scope="scope"> {{ scope.row.fields.add_time }} </template>
          </el-table-column>
        </el-table>
    </el-row>
    <el-row display="margin-top:10px">
       <ve-histogram :data="chartData" :loading="true" ></ve-histogram>
    </el-row>
  </div>
</template>
<!--<link rel="stylesheet" href="//unpkg.com/v-charts/lib/style.min.css">-->
<script type="text/javascript" src="../../node_modules/vue/dist/vue.js"></script>
<!--<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/vue-resource@1.5.1"></script>-->
<script src="../../node_modules/echarts/dist/echarts.min.js"></script>
<script src="../../node_modules/v-charts/lib/index.min.js"></script>

<script>
import 'v-charts/lib/style.css'
export default {
  name: 'home',
  data () {
    return {
      input: '',
      bookList: [],
      chartData: {
          columns: ['日期', '访问用户', '下单用户', '下单率'],
          rows: [
            { '日期': '1/1', '访问用户': 1393, '下单用户': 1093, '下单率': 0.32 },
            { '日期': '1/2', '访问用户': 3530, '下单用户': 3230, '下单率': 0.26 },
            { '日期': '1/3', '访问用户': 2923, '下单用户': 2623, '下单率': 0.76 },
            { '日期': '1/4', '访问用户': 1723, '下单用户': 1423, '下单率': 0.49 },
            { '日期': '1/5', '访问用户': 3792, '下单用户': 3492, '下单率': 0.323 },
            { '日期': '1/6', '访问用户': 4593, '下单用户': 4293, '下单率': 0.78 }
          ]
      }
    }
  },
  mounted: function() {
      this.showBooks()
  },
  methods: {
    addBook(){
      console.log(this.input)
      this.$http.get('http://127.0.0.1:8000/api/add_book?book_name=' + this.input)
        .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (res.error_num == 0) {
              this.showBooks()
            } else {
              this.$message.error('新增书籍失败，请重试')
              console.log(res['msg'])
            }
        })
    },
    showBooks(){
      this.$http.get('http://127.0.0.1:8000/api/show_books')
        .then((response) => {
            var res = JSON.parse(response.bodyText)
            console.log(res)
            if (res.error_num == 0) {
              this.bookList = res['list']
            } else {
              this.$message.error('查询书籍失败')
              console.log(res['msg'])
            }
        })
    }
  }
}
</script>

<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
