<template>

    <RouterLink :to="{name: 'journeyview', params: {id: journey.id}}">
    <div class="flex items-center justify-between">
        <p>
            <strong class="text-lg dark:text-white">
                {{ journey.title }}
            </strong>  
        </p>

        <p v-if="journey.on_going" class="text-green-700 dark:text-green-500">On Going</p>
        <p v-if="!journey.on_going" class="text-blue-700 dark:text-blue-500">Finished</p>

        <p class="text-gray-600 dark:text-gray-500">{{ journey.created_at_formatted }} ago</p>
    </div>
    </RouterLink>

    <div v-if="journey.only_me" class="flex items-center space-x-2 text-gray-500 text-xs mt-1">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
        </svg>

        <span>Only me</span>
    </div>

    <div v-if="userStore.user.id != journey.created_by.id">
        <button v-if="!following" @click="follow()" class="inline-block py-1.5 px-4 bg-green-600 text-white text-xs rounded-lg">Follow</button>
        <button v-if="following" @click="unfollow()" class="inline-block py-1.5 px-4 bg-blue-600 text-white text-xs rounded-lg">Unfollow</button>
    </div>


    <div class="mb-4 mx-auto grid grid-cols-8 gap-1">
        <div class="main-left col-span-1 flex items-center justify-center dark:text-white"> 
                <div v-if=showLeftArrow @click="getPost(-1)">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
                    </svg>
                </div>   
        </div> 

        <div 
            id="CurrentPost"
            class="main-center mt-4 col-span-6 p-4 bg-white border border-gray-200 rounded-lg space-y-4 dark:bg-neutral-900 dark:border-gray-950"       
            v-bind:key="ID"
            v-if="journey.posts.length > 0"
            >
                <PostItem v-bind:post="getPost()"  />
        </div>

        <div v-if=showRightArrow class="main-right col-span-1 flex items-center justify-center dark:text-white">
                <div @click="getPost(1)">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
                    </svg>

                </div>   
        </div>  
    </div>

    <div class="flex justify-between">
        <div v-if="journey.on_going && checkCompanions(userStore.user)" class="container">
            <details>
                <summary class="list-none">
                    <div class="flex items-center justify-center text-green-600">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
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
    </div>
    
</template>

<script>
import axios from 'axios'
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import PostItem from '../components/PostItem.vue'
import JourneyItem from '../components/JourneyItem.vue'
import PostForm from '../components/PostForm.vue'


export default {
    name: 'JourneyItem',

    props: {
        journey: Object,
        post: Object
    },

    //emits: ['deleteJourney'],

    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()

        return {
            userStore,
            toastStore
        }
    },

    components: {
        PostForm,
    },

    data() {
        return {
           ID: 0,
           showExtraModal: false,
           showLeftArrow: true,
           showRightArrow: true,
           following: null
        }
    },

    computed:{
      
    }, 

    mounted() {
        this.checkFollowing()
    },

    methods: {
        getPost(n){
            var currentIndex;
            var lastIndex = this.journey.posts.length - 1;

            if (this.post != null && this.ID == 0){
                for (let i = 0; i <= lastIndex; i++) {
                    if (this.journey.posts[i].id == this.post.id){
                        currentIndex = i;
                    }
                }
            }
            else if(this.ID == 0){
                currentIndex = lastIndex;
            }
            else {
                for(let i = 0; i <= lastIndex; i++){
                    if(this.ID == this.$props.journey.posts[i].id){
                        currentIndex = i;
                        //console.log(currentIndex)
                    }
                }
                if (n==1){
                    if (currentIndex > 0){
                        currentIndex = currentIndex - 1;
                    }
                }
                if(n==-1){
                    if (currentIndex < lastIndex){
                        currentIndex = currentIndex + 1;
                    }           
                }
            }

            //var post = this.$props.journey.posts[currentIndex];
            var post = this.journey.posts[currentIndex]

            if(post != null){
                this.ID = post.id;
            }

            //Check which arrows to show 
            if(currentIndex == 0) {
                this.showRightArrow = false;
            }
            else {
                this.showRightArrow = true;
            }

            if(currentIndex == lastIndex) {
                this.showLeftArrow = false;
            }
            else {
                this.showLeftArrow = true;
            }

            // console.log(currentIndex);
            // console.log(post);
            // console.log(this.ID);

            return post;
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

        checkFollowing() {
            this.journey.followed_by_users.forEach(follower => {
                if (this.userStore.user.id == follower){
                    this.following = true
                }
            })
        },

        follow() {
            axios
            .post(`/api/journey/${this.journey.id}/follow/`)
            .then(response => {
                console.log(response.data)
                this.following = true
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
            })
            .catch(error => {
                console.log("error", error);
            })
        }
    },
    components: { RouterLink, PostItem, PostForm },
}
</script>