<template>
  <div class="w100">
    <el-row class="w100">
      <el-col :span="23">
        <h1>Comics</h1>
      </el-col>
      <el-col :span="1">
        <el-button type="primary" icon="el-icon-plus" />
      </el-col>
    </el-row>
    <el-row class="w100">
      <el-col :span="24">
        <el-table :data="comics">
          <el-table-column
            prop="title"
            label="title"
          />
          <el-table-column
            prop="url"
            label="url"
          />
        </el-table>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  data () {
    return {
      comics: [
        {
          title: 'hoge',
          url: 'http://example.com/hoge'
        },
        {
          title: 'fuga',
          url: 'http://example.com/fuga'
        }
      ]
    }
  }
}
</script>

<style scoped>
.w100 {
    width: 100%;
}

</style>
