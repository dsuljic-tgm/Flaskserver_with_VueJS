<template>
    <div>
        {{ postData }}
    </div>
</template>

<script>
    import axios from 'axios';
    export default {
        name: "Post",
        data(){
            return {
                postData: null
            }
        },
        methods:{
          getPost(){
              axios.get(`http://localhost:5000/posts/${this.$route.params.postID}`)
                    .then((response) => {
                        this.postData = response.data
                        console.log(response.data)
                    })
                    .catch((e) => {
                        console.log(e)
                    })
          }
        },
        created(){
            this.getPost()
        }
    }
</script>

<style scoped>

</style>