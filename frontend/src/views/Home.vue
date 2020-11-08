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
    <div v-for="item in videos" :key="item.name">
      <div class="video">
        <div class="label" @click="watchVideo(item.id)">
          <div :style="{ backgroundImage: 'url(https://img.youtube.com/vi/bI5jpueiCWw/hqdefault.jpg)' }"></div>
        </div>
        <div class="video__name">
          {{ item.name }}
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
      query : "",
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
    watchVideo(id) {
      this.$router.push(`/video/${id}`)
    },
    async getVideoIds() {
      try {
        return await
            axios.get("http://127.0.0.1:8000/searchvideo/", {params: this.axiosParams})
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
.content-wrapper {
  width: 650px;
  max-width: 100vw;
  margin-right: 0;
  margin-left: 0;
  max-height: 50vh;
}
</style>
