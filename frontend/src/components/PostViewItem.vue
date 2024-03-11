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

        <p class="text-gray-600 dark:text-gray-500">{{ journey.created_at_formatted }} ago</p>
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
            class="main-center col-span-6 p-4 bg-white border border-gray-200 rounded-lg space-y-4  dark:bg-neutral-800 dark:border-gray-950"       
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