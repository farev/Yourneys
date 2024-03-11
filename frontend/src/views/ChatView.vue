<template>
    <div>
    <div class="max-w-7xl mx-auto grid grid-cols-3 gap-2" id="entireScreen">        
        <div class="main-left col-span-1 max-h-screen overflow-y-auto">
            <div class="p-2 bg-white border border-gray-200 rounded-lg dark:bg-neutral-900 dark:border-gray-950">
                <div class="space-y-4">
                    <div 
                        class="flex items-center justify-between"
                        v-for="conversation in conversations"
                        v-bind:key="conversation.id"
                        v-on:click="setActiveConversation(conversation.id)"
                    >
                        <div v-if="conversation.journey == null" class="flex items-center space-x-2">
                            <template
                                v-for="user in conversation.users"
                                v-bind:key="user.id"
                            >
                                <div v-if="user.id !== userStore.user.id" class="flex items-justify-start items-center space-x-2">
                                    <img :src="user.get_avatar" class="w-[50px] rounded-full mr-2">

                                    <div>
                                        <p class="text-sm font-bold dark:text-white">{{ user.name }}</p>
                                        <span class="text-xs text-gray-500">{{ conversation.modified_at_formatted }} ago</span>
                                    </div>
                                </div>
                            </template>

                        </div>

                        <div v-else-if="conversation.journey != null" class="flex items-center space-x-2">
                            <div class="w-[50px] h-[50px] flex container">
                                <div v-for="user in conversation.users">
                                    <div v-if="user.id !== userStore.user.id">
                                        <img :src="user.get_avatar" class="object-scale-down rounded-full min-w-[15px]">
                                    </div>
                                </div>
                            </div>
                            <p class="text-sm font-bold dark:text-white">{{ conversation.journey.title }}</p>
                            <span class="text-xs text-gray-500">{{ conversation.modified_at_formatted }} ago</span>
                        </div>

                        <div v-if="conversation.unread_messages" :id="conversation.id" class="bg-red-600 w-[8px] h-[8px] rounded-full mr-3"></div>
                    </div>
                </div>
            </div>
        </div>

        <div v-bind:key="activeConversation.id" class="main-center col-span-2 space-y-2 max-h-screen overflow-y-auto" id="conversationScreen">
            <div class="bg-white border border-gray-200 rounded-lg dark:bg-neutral-900 dark:border-gray-950">
                <div class="p-4 bg-white border-gray-200 rounded-t-lg border-b-4 dark:bg-neutral-900 dark:border-gray-950 sticky top-0">
                    <div v-if="activeConversation.journey" class="flex justify-start mb-2 text-lg dark:text-white">
                        <p>
                            <strong>{{ activeConversation.journey.title }}</strong>
                        </p>
                    </div>
                    <div class="flex justify-start space-x-2">
                        <div
                            v-for="user in activeConversation.users"
                            v-bind:key="user.id"
                            class=""
                        >
                            <div v-if="user.id !== userStore.user.id" >
                                <RouterLink :to="{name: 'profile', params:{'id': user.id}}">
                                    <div class="flex space-x-2 items-center">
                                        <img :src="user.get_avatar" class="w-[50px] rounded-full">
                                        <p v-if="!activeConversation.journey" class="text-lg font-bold dark:text-white">{{ user.name }}</p>
                                    </div>
                                </RouterLink>
                            </div>
                        </div>
                    </div>
                    
                </div>
                <div class="flex flex-col flex-grow p-4">
                    <template
                        v-for="message in activeConversation.messages"
                        v-bind:key="message.id"
                    >
                        <div 
                            class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end"
                            v-if="message.created_by.id == userStore.user.id"
                        >
                            <div>
                                <div class="bg-green-700 text-white rounded-full rounded-br-lg">
                                    <p class="text-sm ml-2 mr-2 p-1">{{ message.body }}</p>
                                </div>
                                <span class="text-xs text-gray-500 leading-none">{{ message.created_at_formatted }} ago</span>
                            </div>
                            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300 dark:bg-gray-950">
                                <img :src="message.created_by.get_avatar" class="w-[40px] rounded-full">
                            </div>
                        </div>

                        <div 
                            class="flex w-full mt-2 space-x-3 max-w-md"
                            v-else
                        >
                            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300 dark:bg-gray-950">
                                <img :src="message.created_by.get_avatar" class="w-[40px] rounded-full" @load="readMessage(message)">
                            </div>
                            <div >
                                <div class="bg-gray-300 rounded-full rounded-bl-lg dark:bg-neutral-700 dark:text-white">
                                    <p class="text-sm ml-2 mr-2 p-1">{{ message.body }}</p>
                                </div>
                                <span class="text-xs text-gray-500 leading-none">{{ message.created_at_formatted }} ago</span>
                            </div>
                        </div>
                    </template>
                </div>

                <form v-on:submit.prevent="submitForm" v-on:keyup.enter="submitForm" class="p-2">
                    <div class="flex justify-between items-center bg-gray-100 rounded-full border border-gray-200 dark:bg-neutral-700 dark:border-neutral-950"> 
                        <textarea id="text" v-model="body" rows="1" class="p-2 w-full bg-gray-100 rounded-full resize-none text-sm dark:text-white dark:bg-neutral-700" placeholder="Message..."></textarea>

                        <button class="inline-block py-2 px-2 dark:text-white">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5" />
                                </svg>
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    </div>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'

export default {
    name: 'chat',

    setup() {
        const userStore = useUserStore()

        return {
            userStore,
        }
    },

    props: {
        targetConversation: String
    },

    data() {
        return {
            conversations: [],
            activeConversation: {},
            body: '',
            chatSocket: null
        }
    },

    beforeMount() {
        this.getConversations()
        console.log(this.$route.params.id)
        if (this.$route.params.id)
            this.setActiveConversation(this.$route.params.id)
    },

    mounted() {
        //this.scrollToBottom()
    },
    
    methods: {
        setActiveConversation(id) {
            console.log('setActiveConversation', id)

            this.activeConversation = id
            if(document.getElementById(id))
                document.getElementById(id).remove()
            this.getMessages()
        },
        getConversations() {
            console.log('getConversations')

            axios
                .get('/api/chat/')
                .then(response => {
                    console.log(response.data)

                    this.conversations = response.data

                    if (this.conversations.length && this.$route.params.id==0) {
                        this.activeConversation = this.conversations[0].id
                    }
                
                    this.getMessages()
                })
                .catch(error => {
                    console.log(error)
                })
        },

        getMessages() {
            console.log('getMessages', this.activeConversation)
            
            axios
                .get(`/api/chat/${this.activeConversation}/`)
                .then(response => {
                    console.log(response.data)

                    this.activeConversation = response.data
                    this.connectWS()
                    
                    this.$nextTick(() => {
                        this.scrollToBottom();
                    });
                })
                .catch(error => {
                    console.log(error)
                })
        },

        submitForm() {
            console.log('submitForm', this.body)

            const isWhitespaceString = str => !str.replace(/\s/g, '').length

            if (!isWhitespaceString(this.body)) {
                axios
                .post(`/api/chat/${this.activeConversation.id}/send/`, {
                    body: this.body
                })
                .then(response => {
                    console.log(response.data)

                    this.activeConversation.messages.push(response.data)
                    this.chatSocket.send(JSON.stringify({
                        'type': 'message',
                        'message': 'new message',
                    }))
                    this.body = ''

                    this.$nextTick(() => {
                        this.scrollToBottom();
                    });
                })
                .catch(error => {
                    console.log(error)
                })
            }
        },
        
        readMessage(mes) {
            if(mes.read == false) {
                console.log("read message")
                if(mes.sent_to.id == this.userStore.user.id) {
                    axios
                    .post(`/api/chat/${mes.id}/read/`)
                    .then(response => {
                        console.log(response.data)
                    })
                }
            }  
        },

        connectWS() {
            console.log(this.activeConversation.id)
            this.chatSocket = new WebSocket (`ws://localhost:8000/ws/chat/${this.activeConversation.id}/`)

            console.log('Websocket: ', this.chatSocket)

            this.chatSocket.onerror = function(e) {
                console.log('Websocket error: ', e);
            }

            this.chatSocket.onmessage = (e) => {
                console.log('onMessage')
                const data = JSON.parse(e.data)

                console.log(this.activeConversation)
                axios
                .get(`/api/chat/${this.activeConversation.id}/`)
                .then(response => {
                    console.log(response.data)
                    this.activeConversation = response.data
                    console.log(this.activeConversation)

                    this.$nextTick(() => {
                        this.scrollToBottom();
                    });
                    //this.activeConversation.messages.push(response.data.messages[response.data.messages.length-1])
                })
                .catch(error => {
                    console.log(error)
                })
            }

            this.chatSocket.onopen = function(e) {
                console.log('onOpnen - chat socket was opened')
            }

            this.chatSocket.onclose = function(e) {
                console.log('onClose - chat socket was closed')
            }
        },

        scrollToBottom() {
            let conversatioScreen = document.getElementById("conversationScreen")

            if (conversationScreen) {
                conversationScreen.scrollTop = conversationScreen.scrollHeight;
                console.log("Scroll to Bottom: ", conversatioScreen.scrollTop) 
            }
        },
    }
}
</script>