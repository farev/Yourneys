<template>
<div key="key">

<RouterLink :to="{name: 'postview', params: {id: post.id}}">
    <div class="flex justify-center">
        <p>
            <strong v-if="post.label == 'Start'" class="text-green-600 text-lg">
                {{ post.label }}
            </strong>
            <strong v-if="post.label == 'Update'" class="text-green-800 text-lg">
                {{ post.label }}
            </strong>
            <strong v-if="post.label == 'Milestone'" class="text-orange-600 text-lg">
                {{ post.label }}
            </strong>
            <strong v-if="post.label == 'End'" class="text-blue-900 text-lg">
                {{ post.label }}
            </strong>
        </p>
    </div>
</RouterLink>

    <div class="mb-6 flex items-center justify-between">
        <div class="flex items-center space-x-3">
            <img :src="post.created_by.get_avatar" class="w-[45px] rounded-full">
            
            <p class="dark:text-white">
                <strong>
                    <RouterLink :to="{name: 'profile', params:{'id': post.created_by.id}}">{{ post.created_by.name }}</RouterLink>
                </strong>
            </p>
        </div>

        <p class="text-gray-600 dark:text-gray-500">{{ post.created_at_formatted }} ago</p>
    </div>

    <template v-if="post.attachments.length"> 
        <div v-bind:key="fileIndex" class="relative" v-on:mouseenter="getIndex(10)" v-on:mouseleave="getIndex(-10)">  
            <img v-if="!isVideo(post.attachments[fileIndex].get_file)" :src="post.attachments[fileIndex].get_file" class="w-full mb-4 rounded-xl object-contain">

            <video v-bind:id="post.id" v-if="isVideo(post.attachments[fileIndex].get_file)" :src="post.attachments[fileIndex].get_file" class="w-full mb-4 rounded-xl object-contain" controls autoplay muted=false loop @canplay="isInView()"></video>

            <div v-if="showLeftArrow" @click="getIndex(-1)" class="absolute left-0 top-1/2 text-gray-50">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
                </svg>
            </div>    

            <div v-if="showRightArrow" @click="getIndex(1)" class="absolute right-0 top-1/2 text-gray-50">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
                </svg>

            </div> 

            <div v-if="post.attachments.length > 1" class="absolute bottom-4 left-1/2 flex justify-center space-x-1">
                <svg v-for="att in post.attachments" v-bind:key="fileIndex" :id="post.attachments.indexOf(att)" width="10px" height="10px" viewBox="0 0 512 512" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                    <title>circle-filled</title>
                    <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                    <g id="icon" :fill="[post.attachments.indexOf(att)==fileIndex ? '#FFFFFF' : '#E0E0E080']" transform="translate(42.666667, 42.666667)">
                        <path d="M213.333333,3.55271368e-14 C331.15408,3.55271368e-14 426.666667,95.5125867 426.666667,213.333333 C426.666667,331.15408 331.15408,426.666667 213.333333,426.666667 C95.5125867,426.666667 3.55271368e-14,331.15408 3.55271368e-14,213.333333 C3.55271368e-14,95.5125867 95.5125867,3.55271368e-14 213.333333,3.55271368e-14 Z" id="Combined-Shape"></path>
                    </g>
                    </g>
                </svg>
            </div>
            
        </div>
    </template>

    <p class="dark:text-white">{{ post.body }}</p>

    <div class="my-6 flex justify-between">
        <div class="flex space-x-6 items-center">
            <div class="flex items-center space-x-2" @click="like(post.id)">
                <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" :fill="liked ? '#FF1111' : 'none'" viewBox="0 0 21 19" :stroke="liked ? '#FF1111' : strokeColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M11 4C5.5-1.5-1.5 5.5 4 11l7 7 7-7c5.458-5.458-1.542-12.458-7-7Z"/>
                </svg>
                
                <span class="text-gray-500 text-xs">{{ post.likes_count }} likes</span>
            </div>
            
            <div class="flex items-center space-x-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 dark:text-white">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z"></path>
                </svg> 

                <RouterLink :to="{name: 'postview', params: {id: post.id}}" class="text-gray-500 text-xs">{{ post.comments_count }} comments</RouterLink>
            </div>

            <div v-if="post.is_private" class="flex items-center space-x-2 text-gray-500 text-xs">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                </svg>

                <span>Is private</span>
            </div>
        </div>
        
        <div>
            <div @click="toggleExtraModal" class="dark:text-white">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z"></path>
                </svg>
            </div>   
        </div>   
    </div>  

    <div v-if="showExtraModal">
        <div class="flex space-x-6 items-center">
            <div 
                class="flex items-center space-x-2" 
                @click="toggleDialog"
                v-if="userStore.user.id == post.created_by.id"
            >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-red-500">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                </svg>
 
                <span class="text-red-500 text-xs">Delete post</span>
            </div>

            <div 
                class="flex items-center space-x-2"
                @click="reportPost"
            >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-orange-500">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3 3v1.5M3 21v-6m0 0l2.77-.693a9 9 0 016.208.682l.108.054a9 9 0 006.086.71l3.114-.732a48.524 48.524 0 01-.005-10.499l-3.11.732a9 9 0 01-6.085-.711l-.108-.054a9 9 0 00-6.208-.682L3 4.5M3 15V4.5" />
                </svg>

                <span class="text-orange-500 text-xs">Report post</span>
            </div>

            <div 
                class="flex items-center space-x-2"
                @click="toggleEdit"
                v-if="userStore.user.id == post.created_by.id"
            >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-blue-700">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
                </svg>

                <span class="text-blue-700 text-xs">Edit post</span>
            </div>  
        </div>
    </div>

</div>

<div v-if="showEdit" class="bg-white border border-gray-200 rounded-lg dark:bg-neutral-900 dark:border-gray-950">
                <EditPostForm 
                    v-bind:user="user" 
                    v-bind:post="post"/>
</div>

    <div>
        <DialogItem :show="showDialog" :cancel="cancelDelete" :confirm="deletePost" title="Delete Post?" description="Deleting this post will delete any fotos and videos related to it. It is an irreversible action." />
    </div>
</template>

<script>
import axios from 'axios'
import { RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import {_} from 'vue-underscore'
import EditPostForm from './EditPostForm.vue'
import DialogItem from '../components/DialogItem.vue'


export default {
    props: {
        post: Object
    },

    emits: ['deletePost'],

    components: { RouterLink, EditPostForm, DialogItem},

    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()

        return {
            userStore,
            toastStore
        }
    },

    data() {
        return {
            key: 0,
            showExtraModal: false,
            showEdit: false,
            showDialog: false,
            playVideo: false,
            fileIndex: 0,
            showLeftArrow: false,
            showRightArrow: false,
            hover: false,
            active: "#E0E0E080",
            liked: false,
            strokeColor: '#000000'
        }
    },

    mounted () {
        const throtledInView = this.throttle(this.isInView, 500)
        window.addEventListener('scroll', throtledInView);

        //console.log("Post likes:", this.post.likes)
        this.post.likes.forEach(like => {
            //console.log("Like: ", like.created_by)
            if (this.userStore.user.id == like.created_by.id) {
                this.liked = true;
            }
        });

        const savedDarkMode = localStorage.getItem('dark-mode')
        console.log(savedDarkMode)

        if (savedDarkMode == "true") {
            this.strokeColor = '#FFFFFF'
        }
        else if (savedDarkMode == "false") {
            this.strokeColor = '#000000'
        }
        else {
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                // dark mode
                this.strokeColor = '#FFFFFF'
            }
        }
        

        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
                const newColorScheme = event.matches ? "dark" : "light";

                if (newColorScheme == 'dark') {
                    this.strokeColor = '#FFFFFF'
                }
                else if (newColorScheme == 'light') {
                    this.strokeColor = '#000000'
                    console.log(this.strokeColor)
                }
        });
    },

    methods: {
        like(id) {
            if (this.liked == false)
                this.likePost(id)
            else if (this.liked == true)
                this.unlikePost(id)
        },

        likePost(id) {
            this.liked = true;
            axios
                .post(`/api/posts/${id}/like/`)
                .then(response => {
                    if (response.data.message == "like created") {
                        this.post.likes_count += 1;
                    }
                })
                .catch(error => {
                    console.log("error", error);
                });
        },

        unlikePost(id) {
            this.liked = false;
            axios
                .post(`/api/posts/${id}/unlike/`)
                .then(response => {
                    if (response.data.message == "unliked") {
                        this.post.likes_count -= 1;
                    }
                })
                .catch(error => {
                    console.log("error", error);
                });
        },

        reportPost() {
            axios
                .post(`/api/posts/${this.post.id}/report/`)
                .then(response => {
                    console.log(response.data)

                    this.toastStore.showToast(5000, 'The post was reported', 'bg-emerald-500')
                })
                .catch(error => {
                    console.log("error", error);
                })
        },

        cancelDelete() {
            console.log("Cancel")
            this.toggleDialog()
        },

        deletePost() {
            this.$emit('deletePost', this.post.id)

            axios
                .delete(`/api/posts/${this.post.id}/delete/`)
                .then(response => {
                    console.log(response.data)
                    this.toggleDialog()
                    this.toastStore.showToast(5000, 'The post was deleted', 'bg-emerald-500')
                    this.$router.go()
                })
                .catch(error => {
                    console.log("error", error);
                })
        },

        toggleExtraModal() {
            console.log('toggleExtraModal')

            this.showExtraModal = !this.showExtraModal
        },

        toggleEdit() {
            this.showEdit = !this.showEdit
        }, 

        toggleDialog() {
            console.log("Toggle dialog")
            this.showDialog = !this.showDialog
        },

        isVideo(file){
            const isImage = ['.gif','.jpg','.jpeg','.png']; 
            const isVideo =['.mpg', '.mp2', '.mpeg', '.mpe', '.mpv', '.mp4', '.MOV', '.mov'];
            let video = false;

            isVideo.forEach(ext => {
                if(file.includes(ext)) {
                    video = true;
                    //console.log(video)
                }
            });

            return video
        },

        isInView() {
            if (document != null) {
                var video = document.getElementById(this.post.id);
                if (video != null)
                {
                    const rect = video.getBoundingClientRect();
                    var inView;
                    var threshold = 1.5;

                    if (rect.top < 0 && rect.bottom >= rect.height/threshold) {
                        inView = true
                    } 
                    else if (rect.top >= 0 && window.innerHeight - rect.top >= rect.height/threshold) {
                        inView = true;
                    }
                    else {
                        inView = false;
                    }

                    //console.log(video)
                    if (inView) {
                        video.play() 
                    }
                    else {
                        video.pause()
                    }
                }
            }
        },
        
        throttle(mainFunction, delay) {
            let timerFlag = null; // Variable to keep track of the timer

            // Returning a throttled version 
            return (...args) => {
                if (timerFlag === null) { // If there is no timer currently running
                mainFunction(...args); // Execute the main function 
                timerFlag = setTimeout(() => { // Set a timer to clear the timerFlag after the specified delay
                    timerFlag = null; // Clear the timerFlag to allow the main function to be executed again
                }, delay);
                }
            };
        },

        getIndex(n) {
            if (Math.abs(n) <= 1) {
                this.fileIndex = this.fileIndex + n;
                console.log(this.fileIndex)
            }

            if (n==10) {
                this.hover = true;
            }
            else if (n == -10) {
                this.hover = false;
            }

            if (this.fileIndex == 0) {
                this.showLeftArrow = false;
            } 
            else if (this.hover) {
                this.showLeftArrow = true;
            }
            else {
                this.showLeftArrow = false;
            }


            if (this.fileIndex == this.post.attachments.length - 1) {
                this.showRightArrow = false;
            }
            else if (this.hover) {
                this.showRightArrow = true;
            }
            else
            {
                this.showRightArrow = false;
            }
        }
    },
}
</script>