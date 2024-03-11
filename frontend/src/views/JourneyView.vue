<template>
    <div class="max-w-7xl mx-auto grid grid-cols-10 gap-6">
        <div class="main-left col-span-1"></div>

        <div class="main-center col-span-6 space-y-4">

            <div class="flex justify-center">
                <p class="text-xl dark:text-white">
                    <strong>{{ journey.title }}</strong>
                </p>
            </div>

            <div class="grid grid-cols-3 gap-2" v-if="journey.created_by">
                <div v-if="userStore.user.id != journey.created_by.id" class="col-span-1 grid justify-items-start">
                    <button v-if="!following" @click="follow()" class="inline-block py-1.5 px-4 bg-green-600 text-white text-xs rounded-lg">Follow</button>
                    <button v-if="following" @click="unfollow()" class="inline-block py-1.5 px-4 bg-blue-600 text-white text-xs rounded-lg">Unfollow</button>
                </div>

                <div v-if="journey.only_me" class="flex items-center space-x-2 text-gray-500 text-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                    </svg>

                    <span>Only me</span>
                </div>

                <div class="col-span-1 grid justify-items-center"> 
                    <p v-if="journey.on_going" class="text-green-700 dark:text-green-500">On Going</p>
                    <p v-if="!journey.on_going" class="text-blue-700 dark:text-blue-500">Finished</p>
                </div>

                <p class="col-span-1 grid justify-items-end text-gray-600 dark:text-gray-400">
                    {{ journey.follower_count }} followers
                </p>
            </div>

            <div class="space-y-4 mb-2 dark:text-white">
                <p><b>Description:</b> {{ journey.description }}</p>
                <p>{{ journey.topic }}</p>
            </div>

            <div class="flex">
                <div v-if="journey.created_by" class="flex justify-start">
                    <div v-if="journey.created_by.id===userStore.user.id" @click="toggleEdit" class="dark:text-white">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
                        </svg>
                    </div>  
                </div>

                <div v-if="journey.on_going && checkCompanions(userStore.user)" class="container">
                    <details>
                        <summary class="list-none">
                            <div class="flex items-center justify-center text-green-600">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-7 h-7">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                            </div>
                        </summary>

                        <div class="bg-white border border-gray-200 rounded-lg mt-4 dark:bg-neutral-900 dark:border-gray-950">
                            <PostForm
                                v-bind:user="null" 
                                v-bind:posts="journey.posts"
                                v-bind:journey="journey"
                            />
                        </div>
                    </details>
                </div>

                <div @click="toggleExtraModal" class="dark:text-white flex justify-end">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z"></path>
                    </svg>
                </div>  
                
            </div>

            <div v-if="showEdit" class="bg-white border border-gray-200 rounded-lg dark:bg-neutral-900 dark:border-gray-950">
                <EditJourneyForm 
                    v-bind:user="user" 
                    v-bind:journey="journey"/>
            </div>

            <div v-if="showExtraModal">
                <div class="flex space-x-6 items-center">
                    <div 
                        class="flex items-center space-x-2" 
                        @click="toggleDialog"
                        v-if="userStore.user.id == journey.created_by.id"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-red-500">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                        </svg>
        
                        <span class="text-red-500 text-xs">Delete journey</span>
                    </div>

                    <div 
                        class="flex items-center space-x-2"
                        @click="reportJourney"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-orange-500">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M3 3v1.5M3 21v-6m0 0l2.77-.693a9 9 0 016.208.682l.108.054a9 9 0 006.086.71l3.114-.732a48.524 48.524 0 01-.005-10.499l-3.11.732a9 9 0 01-6.085-.711l-.108-.054a9 9 0 00-6.208-.682L3 4.5M3 15V4.5" />
                        </svg>

                        <span class="text-orange-500 text-xs">Report journey</span>
                    </div>
                </div>
            </div>

            <div 
                class="p-4 bg-white border border-gray-200 rounded-lg dark:bg-neutral-900 dark:border-gray-950"
                v-for="post in journey.posts"
                v-bind:key="post.id"
            >
                <PostItem v-bind:post="post" v-on:deletePost="deletePost" />
            </div>
        </div>

        <div v-if="journey.created_by" class="main-right col-span-2 space-y-4">
            <button 
                class="inline-block py-3 px-6 bg-green-600 text-sm text-white rounded-lg"
                @click="createGroupchat(journey.id)"
                v-if="!journey.groupchat && journey.companions.length && userStore.user === journey.created_by"
            >
                Create groupchat
            </button> 

            <RouterLink :to="{name: 'chat', params: {id : conversationID}}">
                <button 
                    class="inline-block py-3 px-6 bg-green-600 text-sm text-white rounded-lg"
                    v-if="journey.groupchat && checkCompanions(userStore.user)"
                >
                    Open groupchat
                </button>
            </RouterLink>
                
            <div class="">
                <CompanionsItem v-bind:journey="journey"/>
            </div>

            <div v-if="journey.created_by.id===userStore.user.id" class="">
                <FriendsItem v-bind:user="journey.created_by" v-bind:journey="journey"/>
            </div>
        </div>   

    </div>

    <div>
        <DialogItem :show="showDialog" :cancel="cancelDelete" :confirm="deleteJourney" title="Delete Yourney?" description="Deleting this yourney will delete any posts and data related to it. It is an irreversible action." />
    </div>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import { RouterLink, RouterView } from 'vue-router'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import PostItem from '../components/PostItem.vue'
import PostForm from '../components/PostForm.vue'
import EditJourneyForm from '../components/EditJourneyForm.vue'
import FriendsItem from '../components/FriendsItem.vue'
import CompanionsItem from '../components/CompanionsItem.vue'
import DialogItem from '../components/DialogItem.vue'

export default {
    name: 'JourneyView',

    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()

        return {
            userStore,
            toastStore
        }
    },

    components: {
    PeopleYouMayKnow,
    Trends,
    PostItem,
    PostForm,
    PostItem,
    EditJourneyForm,
    FriendsItem,
    CompanionsItem,
    DialogItem,
    RouterView,
    RouterLink
},

    data() {
        return {
            journey: {
                title: '',
                posts: []
            },
            conversationID: 0,
            showExtraModal: false,
            showEdit: false,
            showDialog: false,
            following: false      
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
                    this.conversationID = response.data.conversation
                    //posts = journey.posts

                    response.data.journey.followed_by_users.forEach(follower => {
                        console.log(follower)
                        if (this.userStore.user.id == follower){
                            this.following = true
                        }
                    })
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

        checkCompanions(user) {
            if (this.journey.created_by.id == this.userStore.user.id) 
                return true
            else {
                let comp = []
                this.journey.companions.forEach(companion => {
                    comp.push(companion.id)
                });
                return comp.includes(user.id)
            }
        }, 

        createGroupchat(journeyID) {
            axios
                .get(`/api/chat/${journeyID}/create/`)
                .then(response => {
                    console.log(response.data)

                    this.$router.push('/chat')
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        follow() {
            axios
            .post(`/api/journey/${this.journey.id}/follow/`)
            .then(response => {
                console.log(response.data)
                this.following = true
                this.journey.follower_count += 1
            })
            .catch(error => {
                console.log("error", error);
            })
        }, 

        unfollow() {
            axios
            .post(`/api/journey/${this.journey.id}/unfollow/`)
            .then(response => {
                console.log(response.data)
                this.following = false
                this.journey.follower_count -= 1
            })
            .catch(error => {
                console.log("error", error);
            })
        }, 

        toggleExtraModal() {
            console.log('toggleExtraModal')

            this.showExtraModal = !this.showExtraModal
        },

        toggleDialog() {
            console.log("Toggle dialog")
            this.showDialog = !this.showDialog
        },

        reportJourney() {
            axios
                .post(`/api/journey/${this.journey.id}/report/`)
                .then(response => {
                    console.log(response.data)
                    this.toastStore.showToast(5000, 'The journey was reported', 'bg-emerald-500')
                    this.toggleExtraModal()
                })
                .catch(error => {
                    console.log("error", error);
                })
        },

        cancelDelete() {
            console.log("Cancel")
            this.toggleDialog()
        },

        deleteJourney() {
            this.$emit('deleteJourney', this.journey.id)

            axios
                .delete(`/api/journey/${this.journey.id}/delete/`)
                .then(response => {
                    console.log(response.data)
                    this.toggleDialog()
                    this.toastStore.showToast(5000, 'The journey was deleted', 'bg-emerald-500')
                    this.$router.push(`/profile/${this.journey.created_by.id}`)
                })
                .catch(error => {
                    console.log("error", error);
                })
        },
        testDelete() {
            console.log("Delete")
        }
    }
}
</script>