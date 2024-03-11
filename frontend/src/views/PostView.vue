<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-center col-span-3 space-y-4 dark:text-white">
            <div 
                class="p-4 bg-white border border-gray-200 rounded-lg  dark:bg-neutral-900 dark:border-gray-950"
                v-if="post.id"
                v-bind:key="post.id"
            >
                <PostViewItem v-bind:post="post" v-bind:journey="journey"/>
            </div>

            <div
                class="p-4 ml-6 bg-white border border-gray-200 rounded-lg  dark:bg-neutral-900 dark:border-gray-950"
                v-for="comment in post.comments"
                v-bind:key="comment.id"
            >
                <CommentItem v-bind:comment="comment" />
            </div>

            <div class="bg-white border border-gray-200 rounded-lg  dark:bg-neutral-900 dark:border-gray-950">
                <form v-on:submit.prevent="submitForm" method="post">
                    <div class="p-4">  
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg dark:bg-neutral-700" placeholder="What do you think?"></textarea>
                    </div>

                    <div class="p-4 border-t border-gray-100 dark:border-gray-950">
                        <button class="inline-block py-4 px-6 bg-green-600 text-white rounded-lg">Comment</button>
                    </div>
                </form>
            </div>
        </div>

        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />

            <Trends />
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { RouterLink } from 'vue-router'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import PostItem from '../components/PostItem.vue'
import CommentItem from '../components/CommentItem.vue'
import PostViewItem from '../components/PostViewItem.vue'

export default {
    name: 'PostView',

    data() {
        return {
            post: {
                id: null,
                comments: []
            },
            journey: {
                title: '',
                description: '',
                topic: '',
                posts: ''
            },
            body: ''
        }
    },

    mounted() {
        this.getPost()
    },

    watch: {
        $route(to, from) {
      // react to route changes...
            this.getPost()
        }
    },

    methods: {
        getPost() {
            axios
                .get(`/api/posts/${this.$route.params.id}/`)
                .then(response => {
                    console.log('data', response.data)

                    this.post = response.data.post
                    this.journey = response.data.journey
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        submitForm() {
            console.log('submitForm', this.body)

            axios
                .post(`/api/posts/${this.$route.params.id}/comment/`, {
                    'body': this.body
                })
                .then(response => {
                    console.log('data', response.data)

                    this.post.comments.push(response.data)
                    this.post.comments_count += 1
                    this.body = ''
                })
                .catch(error => {
                    console.log('error', error)
                })
        }
    }, 

    components: {
    PeopleYouMayKnow,
    Trends,
    PostItem,
    CommentItem,
    PostViewItem,
    RouterLink
},
}
</script>