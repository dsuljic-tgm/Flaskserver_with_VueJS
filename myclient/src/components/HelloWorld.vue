<template>
  <div class="hello">
    <div v-for="user in users">
      {{user.id}} <br>
     {{user.username}}  <br>
     {{user.email}} <br>
      {{user.password}}
    </div>

    <div v-for="message in messages">
      {{message.messageID}} <br>
     {{message.text}}  <br>
     {{message.owner}}
    </div>

    <input type="text" v-model="text"/>
    <input type="number" v-model="owner"/>
    <button v-on:click="postMessageData">Posten</button>
    {{text}}
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
    data(){
      return {
          users:null,
          messages:null,
          text:null,
          owner:null
      }
    },
    methods:{
      getData(){
          axios.get('http://localhost:5000/')
          .then((response)=>{
            this.users=response.data
          })
          .catch((e)=>{
              console.log(JSON.stringify(e))
          })
      },
          getMessageData(){
              axios.get('http://localhost:5000/chat')
                  .then((response)=>{
                      this.messages=response.data
                  })
                  .catch ((e)=>{
                      console.log(JSON.stringify(e))
                  })
        },

          postMessageData(){
          axios.post('http://localhost:5000/chat',{
              text:this.text,
              owner:this.owner
          })
              .then((response) =>{
                  this.getMessageData()
              })
          }
    },
  created(){
      this.getData()
      this.getMessageData()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
h3 {
  margin: 40px 0 0;
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
