<template>
    <div v-if="user.friends.length" class="p-4 bg-white border border-gray-200 rounded-lg dark:bg-neutral-800 dark:border-gray-950">
        <p class="mb-2 dark:text-white">
            <strong>Add Companions</strong>
        </p>

        <div 
            v-for="User in user.friends"
            v-bind:key="User.id"
            v-bind:id="User.id"
        >
            <div v-if="checkCompanions(User) && checkRequests(User)" class="p-4 text-center bg-gray-100 rounded-lg mt-2 dark:bg-neutral-700 dark:border-gray-950">
                
                <img :src="User.get_avatar" class="mb-3 rounded-full">
        
                <p class="dark:text-white">
                    <strong>
                        <RouterLink :to="{name: 'profile', params:{'id': User.id}}">{{ User.name }}</RouterLink>
                    </strong>
                </p>

                <button 
                    class="inline-block mt-5 py-2 px-3 bg-green-600 text-xs text-white rounded-lg"
                    @click="sendCompanionRequest(User.id)"
                >
                    Invite
                </button>
            </div>
            
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'


export default {
    name: 'FriendsItem',

    props: {
        user: Object,
        journey: Object
    },

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
            can_send_request : true,
            requests: [],
        }
    },

    mounted() {
        this.user.friends.forEach(friend => {
            this.getRequests(friend)
        })
    },

    methods: {
        sendCompanionRequest(for_userID) {
            axios
                .post(`/api/journey/${this.journey.id}/${for_userID}/`)
                .then(response => {
                    console.log('data', response.data)

                    if (response.data.message == 'request already sent') {
                        this.toastStore.showToast(5000, 'The request has already been sent!', 'bg-red-300')
                    } else {
                        this.toastStore.showToast(5000, 'The request was sent!', 'bg-emerald-300')
                    }

                    document.getElementById(for_userID).remove()
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        async getRequests(user) {
            console.log("Getting Requests")
            await axios
                .get(`/api/requests/${user.id}/${this.journey.id}/`)
                .then(response => {
                    console.log('data', response.data.requests[0])

                    if(response.data.requests.length > 0) {
                        this.requests.push(response.data.requests[0])
                    }
                    else {

                    }
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        checkRequests(user) {
            //console.log(this.requests)
            for (const req of this.requests) {
                if (user.id == req.created_for.id) {
                    console.log("Cannot send to:", req.id)
                    return false
                }
            }
            return true
        },

        checkCompanions(user) {
            console.log("Checking companions")
            let comp = []
            this.journey.companions.forEach(companion => {
                comp.push(companion.id)
            });

            return !comp.includes(user.id)
        }, 
    }
}
</script>