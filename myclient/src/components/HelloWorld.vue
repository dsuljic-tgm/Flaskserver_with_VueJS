<template>
  <div class="hello">

      <div>
      <!-- users table -->
        <b-table striped hover>
          <thead>
            <tr>
              <th scope="col">ID</th>
              <th scope="col">Username</th>
              <th scope="col">Email</th>
              <th scope="col">Password</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in users" :key="index">
              <td width="25%">{{ user.id }}</td>
              <td width="25%">{{ user.username }}</td>
              <td width="25%">{{ user.email }}</td>
              <td width="25%">{{ user.password }}</td>
            </tr>
          </tbody>
        </b-table>
        </div>

      <br />
      <br />
    <div>
    <b-table striped hover>
        <thead>
        <tr>
            <th scope="col">MessageID</th>
            <th scope="col">Text</th>
            <th scope="col">Owner</th>
            <th></th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(message,index) in messages" :key="index">
            <td width="17%">{{message.messageID}}</td>
            <td width="50%">{{message.text}}</td>
            <td width="20%">{{message.owner}}</td>
            <td><button v-on:click="onDeleteMessage(message)">Löschen</button></td>
        </tr>
        </tbody>
    </b-table>
    </div>

      <br />
      <div>
              <h2>Forumpost erstellen</h2>
              <h3>Message</h3>
              <textarea type="text" v-model="text" placeholder="add multiple lines"></textarea>
              <h3>Username</h3>
              <input type="number" v-model="owner"/>
              <br />
              <br />
              <button v-on:click="postMessageData">Posten</button>
          <br />
          <br />
              <h2>Benutzer erstellen</h2>
              <h3>Username</h3>
              <textarea type="text" v-model="text" placeholder="add multiple lines"></textarea>
              <h3>E-Mail</h3>
              <textarea type="text" v-model="text" placeholder="add multiple lines"></textarea>
              <h3>Passwort</h3>
              <input type="password" v-model="owner"/>
              <br />
              <br />
              <button v-on:click="postMessageData">Benutzer hinzufügen</button>
      </div>
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
      getUserData(){
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

         removeMessage(msgID) {
          axios.delete(`http://localhost:5000/chat/${msgID}`)
            .then(() => {
              this.getMessageData()
              this.message = 'Message removed!'
              this.showMessage = true
            })
            .catch((error) => {
              // eslint-disable-next-line
              console.error(error);
              this.getMessageData()
            })
        },
        onDeleteMessage (message) {
              this.removeMessage(message.messageID)
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
      this.getUserData()
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
