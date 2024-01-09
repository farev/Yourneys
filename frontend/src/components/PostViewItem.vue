<template>

    <RouterLink :to="{name: 'journeyview', params: {id: journey.id}}">
    <div class="mb-6 flex items-center justify-between">
        <div class="flex justify-center space-x-6">
            <p>
                <strong class="text-lg">
                    {{ journey.title }}
                </strong>
                
            </p>
        </div>

        <p class="text-gray-600">{{ journey.created_at_formatted }} ago</p>
    </div>


    </RouterLink>

    <div class="mb-4 mx-auto grid grid-cols-8 gap-1">

        <RouterLink :to="{name: 'postview', params: {id: prevID}}" class="main-left col-span-1 flex items-center justify-center">
            <div class="main-left col-span-1 flex items-center justify-center"> 
                <div v-if=showLeftArrow>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
                    </svg>
                </div>   
            </div> 
        </RouterLink>

        <div 
            id="CurrentPost"
            class="main-center col-span-6 p-4 bg-white border border-gray-200 rounded-lg space-y-4"       
            v-bind:key="ID"
            >
                <PostItem v-bind:post="post"  />
        </div>

        <RouterLink :to="{name: 'postview', params: {id: nextID}}" class="main-left col-span-1 flex items-center justify-center">
            <div v-if=showRightArrow class="main-right col-span-1 flex items-center justify-center">
                <div>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
                    </svg>

                </div>   
            </div>
        </RouterLink>
          
    </div>

    <div class="flex justify-between">
        <div class="container">
            <details>
                <summary class="list-none">
                    <div class="flex items-center justify-center text-green-600">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </div>
                </summary>

                <div class="bg-white border border-gray-200 rounded-lg mt-4">
                    <PostForm
                        v-bind:user="null" 
                        v-bind:posts="journey.posts"
                        v-bind:journey="journey"
                    />
                </div>
            </details>
        </div>

        <div @click="toggleExtraModal">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z"></path>
            </svg>
        </div>   
    </div>

    <div v-if="showExtraModal">
        <div class="flex space-x-6 items-center">
            <div 
                class="flex items-center space-x-2" 
                @click="deleteJourney"
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
    
</template>

<script>
import axios from 'axios'
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import PostItem from '../components/PostItem.vue'
import PostForm from '../components/PostForm.vue'


export default {
    name: 'PostViewItem',

    props: {
        journey: Object,
        post: Object
    },

    emits: ['deleteJourney'],

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
           prevID: null, 
           nextID: null
        }
    },

    computed:{
      getPr(){
        return this.$props;
      }
    }, 

    mounted() {
        this.getPostID()
    },

    methods: {
        getPostID(){
            var currentIndex;
            var lastIndex = this.journey.posts.length - 1;
            var id;

            if (currentIndex == null){
                for (let i = 0; i <= lastIndex; i++) {
                    if (this.journey.posts[i].id == this.post.id){
                        currentIndex = i;
                    }
                }
            }

            //Clicking to the right
            if (currentIndex > 0){
                this.nextID = this.journey.posts[currentIndex-1].id
                this.showRightArrow = true;
            }
            else {
                this.nextID = this.post.id
                this.showRightArrow = false
            }

            //Clicking left
            if (currentIndex < lastIndex){
                this.prevID = this.journey.posts[currentIndex+1].id
                this.showLeftArrow = true;
            }   
            else {
                this.prevID = this.post.id
                this.showLeftArrow = false;
            }        
        }, 

        reportJourney() {
            axios
                .post(`/api/journey/${this.journey.id}/report/`)
                .then(response => {
                    console.log(response.data)

                    this.toastStore.showToast(5000, 'The journey was reported', 'bg-emerald-500')
                })
                .catch(error => {
                    console.log("error", error);
                })
        },

        deleteJourney() {
            this.$emit('deleteJourney', this.journey.id)

            axios
                .delete(`/api/journey/${this.journey.id}/delete/`)
                .then(response => {
                    console.log(response.data)

                    this.toastStore.showToast(5000, 'The journey was deleted', 'bg-emerald-500')
                })
                .catch(error => {
                    console.log("error", error);
                })
        },

        toggleExtraModal() {
            console.log('toggleExtraModal')

            this.showExtraModal = !this.showExtraModal
        }
    },
    components: { RouterLink, PostItem, PostForm },
}
</script>