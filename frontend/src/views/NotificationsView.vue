<template>
    <div class="max-w-7xl mx-auto grid grid-cols-3 gap-4">
        <div class="main-center col-span-2 space-y-2">
            <div 
                class="p-4 bg-white border border-gray-200 rounded-lg dark:bg-neutral-900 dark:border-gray-950"
                v-for="notification in notifications"
                v-bind:key="notification.id"
                v-if="notifications.length"
            >
                <div class="flex justify-normal items-center space-x-2">
                    <img :src="notification.created_by.get_avatar" class="rounded-full w-8 ">
                    <p class="dark:text-white">{{ notification.body }} </p>
                    <button class="underline text-green-800 dark:text-green-600" @click="readNotification(notification)">Read more</button>
                </div>
            </div>

            <div 
                class="p-4 bg-white border border-gray-200 rounded-lg dark:bg-neutral-800 dark:border-gray-950 dark:text-white"
                v-else
            >
                You don't have any unread notifications!
            </div>
        </div>

        <div class="main-right col-span-1 space-y-2">
            <div 
                class="p-4 bg-white border border-gray-200 rounded-lg dark:bg-neutral-900 dark:border-gray-950 dark:text-white"
                v-if="friendshipRequests.length"
            >
                <h2 class="mb-4 text-xl">Requests</h2>

                <div 
                    class="p-4 text-center bg-gray-100 rounded-lg mt-2 dark:bg-neutral-800 dark:border-gray-950"
                    v-for="friendshipRequest in friendshipRequests"
                    v-bind:key="friendshipRequest.id"
                >
                    <p class="mb-3">
                        <strong v-if="friendshipRequest.journeyid">Companion Request</strong>
                        <p v-if="friendshipRequest.journeyid">from</p>
                        <strong v-if="!friendshipRequest.journeyid">Friendship Request</strong>
                    </p>
                    <img :src="friendshipRequest.created_by.get_avatar" class="mb-3 mx-auto rounded-full">
                
                    <p>
                        <strong>
                            <RouterLink :to="{name: 'profile', params:{'id': friendshipRequest.created_by.id}}">{{ friendshipRequest.created_by.name }}</RouterLink>
                        </strong>
                    </p>

                    <p v-if="friendshipRequest.journeyid">
                        for <br>
                        <strong v-if="journeys"> 
                            <RouterLink :to="{name: 'journeyview', params: {id: getJourneyInfo(friendshipRequest.journeyid).id}}"> {{ getJourneyInfo(friendshipRequest.journeyid).title }} </RouterLink>
                            </strong>
                    </p>

                    <div class="mt-3 space-x-2">
                        <button class="inline-block py-2 px-3 bg-green-600 text-xs text-white rounded-lg" @click="handleRequest('accepted', friendshipRequest.created_by.id, friendshipRequest.journeyid)">Accept</button>
                        <button class="inline-block py-2 px-3 bg-red-600 text-xs text-white rounded-lg" @click="handleRequest('rejected', friendshipRequest.created_by.id, friendshipRequest.journeyid)">Reject</button>
                    </div>
                </div>

            </div>
        </div>

    </div>
</template>


<script>
import axios from 'axios'
import { RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user'


export default {
    name: 'notifications',

    setup() {
        const userStore = useUserStore()

        return {
            userStore,
        }
    },

    data() {
        return {
            notifications: [],
            user: {},
            friendshipRequests: [],
            friends: [],
            journeys: [],
            chatSocket: null,
        };
    },
    mounted() {
        this.getNotifications();
        this.connectWS()
    },
    methods: {
        getNotifications() {
            axios
                .get('/api/notifications/')
                .then(response => {
                console.log(response.data);
                this.notifications = response.data;
                this.getFriends();
            })
                .catch(error => {
                console.log('Error: ', error);
            });
        },
        async readNotification(notification) {
            console.log('readNotification', notification.id);
            await axios
                .post(`/api/notifications/read/${notification.id}/`)
                .then(response => {
                console.log(response.data);
                if (notification.type_of_notification == 'post_like' || notification.type_of_notification == 'post_comment') {
                    this.$router.push({ name: 'postview', params: { id: notification.post_id } });
                }
                else if (notification.type_of_notification == 'new_friendrequest' || notification.type_of_notification == 'accepted_friendrequest' || notification.type_of_notification == 'rejected_friendrequest') {
                    this.$router.push({ name: 'friends', params: { id: notification.created_for_id } });
                }
                else if (notification.type_of_notification == 'accepted_companionrequest' || notification.type_of_notification == 'rejected_companionrequest') {
                    this.$router.push({name: 'journeyview', params: {id: notification.journey_id}})
                } 
                else if(notification.type_of_notification == 'journey_follow') {
                    this.$router.push({name: 'journeyview', params: {id: notification.journey_id}})
                }

                this.chatSocket.send(JSON.stringify({
                    'type': 'notification',
                    'message': 'send notification'
                }))

                this.$emit('readNotification')
            })
                .catch(error => {
                console.log('Error: ', error);
            });
        },
        getFriends() {
            axios
                .get(`/api/friends/${this.userStore.user.id}/`)
                .then(response => {
                console.log('data', response.data);
                this.friendshipRequests = response.data.requests;
                this.friends = response.data.friends;
                this.user = response.data.user;
                this.getJourneys(this.friendshipRequests)
            })
                .catch(error => {
                console.log('error', error);
            });
        },
        handleRequest(status, pk, journeyid) {
            console.log('handleRequest', status);
            if (journeyid) {
                axios
                    .post(`/api/journey/${journeyid}/${status}/`)
                    .then(response => {
                    console.log('data', response.data);
                    axios
                        .post(`/api/chat/${journeyid}/add/`)
                        .catch(error => {
                        console.log('error', error)
                    })
                    this.$router.push(`/${journeyid}/`)
                })
                    .catch(error => {
                    console.log('error', error);
                });
            }
            else {
                axios
                    .post(`/api/friends/${pk}/${status}/`)
                    .then(response => {
                    console.log('data', response.data);
                })
                    .catch(error => {
                    console.log('error', error);
                });
            }
        },
        getJourney(id) {
            axios
                .get(`/api/journey/${id}/`)
                .then(response => {
                console.log('data', response.data.journey);
                this.journey = response.data.journey;
                this.journeys.push(response.data.journey)
            })
                .catch(error => {
                console.log('error', error);
            });
        },
        getJourneys(requests) {
            requests.forEach(request => {
                if (request.journeyid) {
                    this.getJourney(request.journeyid)
                }
            });
        },
        getJourneyInfo(id) {
            for (const journey of this.journeys) {
                if (id == journey.id)
                    console.log(journey)
                    return journey
            }
        },

        async connectWS() {
                this.chatSocket = await new WebSocket (`ws://localhost:8000/ws/notifications/`)
                //this.chatSocket = new WebSocket (`ws://${window.location.host}/ws/6c4740da-71b6-4da4-a3a2-2b2b58c08fae/`)

                console.log('Websocket: ', this.chatSocket)

                this.chatSocket.onerror = function(e) {
                    console.log('Websocket error: ', e);
                }

                this.chatSocket.onmessage = (e) => {
                    console.log('onMessage')       
                }

                this.chatSocket.onopen = function(e) {
                    console.log('onOpnen - chat socket was opened')
                }

                this.chatSocket.onclose = function(e) {
                    console.log('onClose - chat socket was closed')
                }
            },
    },
    components: { RouterLink }
}
</script>