<template>
  <div class="home" style="display: flex; justify-content: center;">
    <div style="display: flex; flex-direction: row; ">
      <v-text-field v-model="query" @keydown.enter="changeVideo"></v-text-field>
      <v-btn depressed
             color="primary"
             @click="changeVideo">
        検索
      </v-btn>
    </div>
    <div v-for="item in videos" :key="item.title">
      <div class="video">
        <div class="label">
          <div :style="{ backgroundImage: 'url(https://img.youtube.com/vi/bI5jpueiCWw/hqdefault.jpg)' }"></div>
<!--          <div :style="{ backgroundImage: 'url(' + require('@/assets/giphy.gif') + ')' }"></div>-->
        </div>
        <div class="video__name">
          {{ item.title }}
        </div>
        <div class="video__description">
          {{ item.description }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const axios = require('axios')

export default {
  name: 'Home',
  data() {
    return {
      videos: [],
      interval: undefined,
    }
  },
  methods: {
    playVideo() {
      this.player.playVideo()
    },
    changeVideo() {
      this.getVideoIds().then((response) => {
        this.videos = response.data;
      })
    },

    async getVideoIds() {
      try {
        return await
            axios.get("http://127.0.0.1:8000/search/", {params: this.axiosParams})
      } catch (error) {
        console.error(error)
      }
    },
  },
  computed: {
    axiosParams() {
      const params = new URLSearchParams();
      params.append('name', this.query);
      return params;
    },
    player() {
      return this.$refs.youtube.player
    }
  }
}
</script>

<style lang="scss">

iframe {
  width: 100%;
  max-width: 650px; /* Also helpful. Optional. */
}

.content-wrapper {
  width: 650px;
  max-width: 100vw;
  margin-right: 0;
  margin-left: 0;
  max-height: 50vh;
}

.animation {
  width: 100vw;
  height: 50vh;
  z-index: 300;
  position: fixed;
  top: 50vh;
  left: 0;
  padding: 50px;


  .bg {
    width: 100%;
    max-width: 600px;
    height: 100%;
    margin-left: auto;
    margin-right: auto;
    background-size: cover;
  }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .8s;
}

.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */
{
  opacity: 0;
}
</style>
