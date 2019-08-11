<template>
    <div class="hello">
        <div class="container">
            <div class="row">
                <div class="col-sm-6">
                    <b-table striped hover :items="messages" v-bind:fields="messagefields">
                        <template slot="actions" slot-scope="row">
                            <b-button variant="danger" size="sm" @click="removeMessage(row.item.messageID)" class="mr-2">
                                Löschen
                            </b-button>
                        </template>
                    </b-table>
                    <h2>Forumpost erstellen</h2>
                    <h3>Message</h3>
                    <textarea type="text" v-model="messageText" placeholder="add multiple lines"></textarea>

                    <!--
                    <h3>User-ID</h3>
                    <b-form-input min="1" type="number" v-model="messageOwner"/>
                    -->
                    <br/>
                    <br/>
                    <b-button variant="success" v-on:click="postMessageData">Posten</b-button>
                </div>
                <div class="col-sm-6">
                    <b-table striped hover :items="users" v-bind:fields="userfield" id="usertable">
                        <template slot="actions" slot-scope="row">
                            <b-button variant="danger" size="sm" @click="removeUser(row.item.id)" class="mr-2">
                                Löschen
                            </b-button>
                            <b-button v-on:click="updateUser(row.item.id)">
                                Update
                            </b-button>
                        </template>
                    </b-table>
                    <h2>Benutzer erstellen</h2>
                    <h3>Username</h3>
                    <b-form-input type="text" v-model="userUsername" placeholder="Dzenan"></b-form-input>
                    <h3>E-Mail</h3>
                    <b-form-input type="text" v-model="userEmail"
                                  placeholder="dsuljic@student.tgm.ac.at"></b-form-input>
                    <h3>Passwort</h3>
                    <b-form-input type="password" v-model="userPassword"/>
                    <br/>
                    <br/>
                    <b-button id="newuser" variant="success" v-on:click="postUserData">Benutzer hinzufügen</b-button>
                </div>
            </div>

            <br />
            <br />

            <div>
                <b-form-input type="text" v-model="updateUserUsername" placeholder="Dzenan"></b-form-input>
                <b-form-input type="text" v-model="updateUserEmail" placeholder="email"></b-form-input>
                <b-form-input type="text" v-model="updateUserPassword" placeholder="password"></b-form-input>
            </div>

        </div>

        <input v-model="userloginusername"type="text">
        <input v-model="userloginpassword"type="text">
        <button @click="getID()">add</button>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: 'HelloWorld',
        props: {
            msg: String
        },
        data() {
            return {
                users: null,
                userfield: [
                    {key: 'id', label: 'id', sortable: true},
                    {key: 'username', label: 'Benutzername', sortable: true},
                    {key: 'email', label: 'Email', sortable: true},
                    {key: 'password', label: 'Password', sortable: true},
                    {key: 'actions', label: ''}
                ],
                messagefields: [
                    {key: 'messageID', label: 'messageID', sortable: true},
                    {key: 'text', label: 'text', sortable: true},
                    {key: 'owner', label: 'owner', sortable: true},
                    {key: 'actions', label: ''}
                ],
                messages: null,
                messageText: null,
                messageOwner: null,
                userUsername: null,
                userEmail: null,
                userPassword: null,

                updateUserUsername:null,
                updateUserEmail: null,
                updateUserPassword:null,

                userloginusername: null,
                userloginpassword: null
            }
        },
        methods: {
            getID(){
                axios.get(`http://localhost:5000/login?username=${this.userloginusername}&password=${this.userloginpassword}`)
                    .then((response) => {
                        axios.defaults.headers.common['Authorization'] = 'Basic '+btoa(this.userloginusername+':'+this.userloginpassword);
                        this.getUserData()
                        this.getMessageData()
                    })
                    .catch((e) => {
                        console.log(e)
                    })
            },
            getUserData() {
                axios.get('http://localhost:5000/users')
                    .then((response) => {
                        this.users = response.data
                    })
                    .catch((e) => {
                        console.log(e)
                    })
            },
            postUserData() {
                axios.post('http://localhost:5000/users', {
                    username: this.userUsername,
                    email: this.userEmail,
                    password: this.userPassword
                })
                    .then((response) => {
                        this.getUserData()
                    })
            },
            removeUser(id) {
                axios.delete(`http://localhost:5000/users/${id}`)
                    .then(() => {
                        this.getUserData()
                        this.message = 'User removed!'
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        console.error(error);
                        this.getUserData()
                    })
            },
            updateUser (id) {
                axios.put(`http://localhost:5000/users/${id}`, {
                    username: this.updateUserUsername,
                    email: this.updateUserEmail,
                    password: this.updateUserPassword
                })
                    .then(() => {
                        this.getUserData()
                        this.message = 'User updated!'
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        console.error(error);
                    })
            },
            getMessageData() {
                axios.get('http://localhost:5000/chat')
                    .then((response) => {
                        this.messages = response.data
                    })
                    .catch((e) => {
                        console.log(JSON.stringify(e))
                    })
            },

            removeMessage(msgID) {
                axios.delete(`http://localhost:5000/chat/${msgID}`)
                    .then(() => {
                        this.getMessageData()
                        this.message = 'Message removed!'
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        console.error(error);
                        this.getMessageData()
                    })
            },
            postMessageData() {
                axios.post('http://localhost:5000/chat', {
                    text: this.messageText,
                    owner: this.messageOwner
                })
                    .then((response) => {
                        this.getMessageData()
                    })
            }
        },
        created() {
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
