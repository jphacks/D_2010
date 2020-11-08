<template>
  <div id="app">
    <div class="app-title">
      <h1>SUPER LIVE</h1>
      <p>検索したい動画を入力してください</p>
    </div>
    <v-app>
      <router-view/>
    </v-app>
  </div>
</template>
<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
.app-title{
  margin-bottom: 50px;
}
</style>
