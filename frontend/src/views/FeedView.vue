<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-center col-span-3 space-y-4">
            <div class="container">
                <details>
                    <summary class="list-none mb-2">
                        <div class="flex items-center justify-center text-green-600">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.75" stroke="currentColor" class="w-8 h-8">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                    </summary>

                    <div class="bg-white border border-gray-200 rounded-lg">
                        <JourneyForm 
                        v-bind:user="user" 
                        v-bind:journeys="journeys"/>
                    </div>
                </details>
            </div>

            <div 
                class="p-4 bg-white border border-gray-200 rounded-lg space-y-4"
                v-for="post in posts"
                v-bind:key="post.id"
            >
                <JourneyItem v-bind:post="post" v-bind:journey="getJourney(post.journeyid)" v-on:deletePost="deletePost"/>
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
import JourneyItem from '../components/JourneyItem.vue'
import JourneyForm from '../components/JourneyForm.vue'
import { useUserStore } from '@/stores/user'


export default {
    name: 'FeedView',

    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    },
    components: {
    PeopleYouMayKnow,
    Trends,
    PostItem,
    FeedForm,
    JourneyItem,
    JourneyForm
},

    data() {
        return {
            journeys: [],
            posts: [],
            body: '',
            user: {
                id: ''
            },
        }
    },

    mounted() {
        this.getFeed()
    },

    methods: {
        getFeed() {
            axios
                .get('/api/journey/')
                .then(response => {
                    console.log('data', response.data)

                    this.journeys = response.data.journeys
                    this.user = response.data.user
                    this.posts = response.data.posts
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        getJourney(ID) {
            console.log("Getting Journey", ID)
            let currentJourney = null;

            this.journeys.forEach(journey => {
                if(journey.id == ID){
                    console.log("Return Journey", journey)
                    currentJourney = journey
                } 
            });
            return currentJourney;
        },

        deletePost(id) {
            this.posts = this.posts.filter(post => post.id !== id)
        },
    }
}
</script>