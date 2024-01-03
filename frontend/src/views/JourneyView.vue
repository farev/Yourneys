<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-center col-span-3 space-y-4">
            <div class="flex justify-center">
                <p>
                    <strong>{{ journey.title }}</strong>
                </p>
            </div>

            <div class="space-y-4 mb-2">
                <p>Description: {{ journey.description }}</p>
                <p>Topic: {{ journey.topic }}</p>
            </div>

            <div class="flex">
                <div class="container">
                    <details>
                        <summary class="list-none">
                            <div class="flex items-center justify-center text-green-600">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-7 h-7">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                            </div>
                        </summary>

                        <div class="bg-white border border-gray-200 rounded-lg mt-4">
                            <FeedForm
                                v-bind:user="null" 
                                v-bind:posts="journey.posts"
                                v-bind:journey="journey"
                            />
                        </div>
                    </details>
                </div>

                <div @click="toggleEdit">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
                    </svg>
                </div>  
            </div>

            <div v-if="showEdit" class="bg-white border border-gray-200 rounded-lg">
                <EditJourneyForm 
                    v-bind:user="user" 
                    v-bind:journey="journey"/>
            </div>

            <div 
                class="p-4 bg-white border border-gray-200 rounded-lg"
                v-for="post in journey.posts"
                v-bind:key="post.id"
            >
                <PostItem v-bind:post="post" v-on:deletePost="deletePost" />
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
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import PostItem from '../components/PostItem.vue'
import FeedForm from '../components/FeedForm.vue'
import EditJourneyForm from '../components/EditJourneyForm.vue'

export default {
    name: 'JourneyView',

    components: {
    PeopleYouMayKnow,
    Trends,
    PostItem,
    FeedForm,
    PostItem,
    EditJourneyForm
},

    data() {
        return {
            journey: {
                title: '',
                posts: []
            },
            showEdit: false      
        }
    },

    mounted() {
        this.getJourney()
    },

    methods: {
        getJourney() {
            axios
                .get(`/api/journey/${this.$route.params.id}/`)
                .then(response => {
                    console.log('data', response.data)

                    this.journey = response.data.journey
                    posts = journey.posts
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        toggleEdit() {
            this.showEdit = !this.showEdit
        }, 

        editJourney(journey) {
            this.journey = journey
        },

        deletePost(id) {
            //this.posts = this.posts.filter(post => post.id !== id)
        },
    }
}
</script>