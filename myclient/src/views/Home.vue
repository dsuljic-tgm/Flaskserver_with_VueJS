<template>
    <div>
        <b-table striped hover :items="posts" v-bind:fields="postfields">
            <template slot="actions" slot-scope="row">
                <b-button variant="success" size="sm" @click="goToForumpost(row.item.postID)" class="mr-2">
                    Öffnen
                </b-button>
            </template>
        </b-table>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: 'Home',
        props: {
            msg: String
        },
        data() {
            return {
                postfields: [
                    {key: 'postID', label: 'postID', sortable: true},
                    {key: 'title', label: 'title', sortable: true},
                    {key: 'text', label: 'text', sortable: true},
                    {key: 'actions', label: ''}
                ],
                posts: null,
            }
        },
        methods: {
            getForumpost() {
                axios.get('http://localhost:5000/posts')
                    .then((response) => {
                        console.log(response.data)
                        this.posts = response.data
                    })
                    .catch((e) => {
                        console.log(e)
                    })
            },
            goToForumpost(postID) {
                this.$router.push('post/'+postID)

            },
        },
        created() {
            this.getForumpost()
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