<template>
  <div class="search">
    <div style="display: flex; flex-direction: row; ">
      <v-text-field v-model="query" @keydown.enter="changeVideo"></v-text-field>
      <v-btn depressed
             color="primary"
             @click="changeVideo">
        検索
      </v-btn>
    </div>

    <div v-for="item in videos" :key="item.name">
      <div class="video" @click="watchVideo(item.id)">
        <div class="video__img">
          <img :src="'https://img.youtube.com/vi/'+item.id+'/hqdefault.jpg'">
        </div>
        <div class="video__content">
          <h2 class="video__name">
            動画のタイトル : {{ item.videoTitle }}
          </h2>

          <h4 class="video__user">
            チャンネル名 : {{ name }}
          </h4>
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
      query: "",
      name: "",
      videos: [],
      interval: undefined,
    }
  },
  methods: {
    playVideo() {
      this.player.playVideo()
    },
    changeVideo() {
      let temp;
      this.getVideoIds().then((response) => {
        temp = JSON.parse(response.data);
        this.name = temp.name;
        this.videos = temp.videos;
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
  }
}
</script>

<style lang="scss">
.search {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-left: 300px;
  padding-right: 300px;
}

.video {
  display: flex;
  flex-direction: row;
  cursor: pointer;
  text-align: left;

  &__img {
    img {
      width: 100%;
      max-width: 250px;
    }
  }

  &__content {
    flex-direction: column;
    margin-left: 50px;
  }

  h4 {
    margin-top: 30px;
  }
}
</style>
