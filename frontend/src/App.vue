<template>
    <nav class="py-10 px-8 border-b border-gray-200 dark:bg-neutral-900 dark:border-gray-950">
        <div class="max-w-7xl mx-auto ">
            <div class="flex items-center justify-between">
                <div class="menu-left flex items-center">
                    <div @click="toggleMenu" class="rounded hover:bg-gray-100 hover:ring hover:ring-gray-100 dark:text-white dark:hover:bg-neutral-800 dark:hover:ring-neutral-800">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                        </svg>
                    </div>

                    <img class="w-[55px] p-2" src="./assets/Yourneys_Logo7.png">
                    <a href="#" class="text-xl dark:text-white">YOURNEYS</a>
                </div>
                {{ getURL() }}
                <div class="menu-center flex space-x-12" v-if="userStore.user.isAuthenticated" @click="getURL()">
                    <RouterLink to="/feed" class="rounded hover:bg-gray-100 hover:ring hover:ring-gray-100 dark:hover:bg-neutral-800 dark:hover:ring-neutral-800">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" :stroke="house" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
                        </svg>
                    </RouterLink>

                    <RouterLink to="/following" class="rounded hover:bg-gray-100 hover:ring hover:ring-gray-100 dark:hover:bg-neutral-800 dark:hover:ring-neutral-800">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" :stroke="map" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 6.75V15m6-6v8.25m.503 3.498 4.875-2.437c.381-.19.622-.58.622-1.006V4.82c0-.836-.88-1.38-1.628-1.006l-3.869 1.934c-.317.159-.69.159-1.006 0L9.503 3.252a1.125 1.125 0 0 0-1.006 0L3.622 5.689C3.24 5.88 3 6.27 3 6.695V19.18c0 .836.88 1.38 1.628 1.006l3.869-1.934c.317-.159.69-.159 1.006 0l4.994 2.497c.317.158.69.158 1.006 0Z" />
                        </svg>
                    </RouterLink>

                    <RouterLink :to="{name:'chat', params:{id:'0'}}" class="rounded hover:bg-gray-100 hover:ring hover:ring-gray-100 dark:hover:bg-neutral-800 dark:hover:ring-neutral-800">
                        <div :key="unreadMessagesCount" class="flex items-center">
                            <div v-if="unreadMessagesCount" class="relative inline-flex items-center justify-center w-4 h-4 text-xs font-bold text-white bg-red-500 border-2 border-white rounded-full -top-2 -end-7 dark:border-neutral-900"></div>
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" :stroke="message" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H8.25m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H12m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 0 1-2.555-.337A5.972 5.972 0 0 1 5.41 20.97a5.969 5.969 0 0 1-.474-.065 4.48 4.48 0 0 0 .978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25Z" />
                            </svg>
                        </div>
                    </RouterLink>

                    <RouterLink to="/notifications" class="rounded hover:bg-gray-100 hover:ring hover:ring-gray-100 dark:hover:bg-neutral-800 dark:hover:ring-neutral-800">
                        <div :key="notificationCount" class="flex items-center" v-on:readNotification="checkNotifications">
                            <div v-if="notificationCount" v-bind:key="notificationCount" class="relative inline-flex items-center justify-center w-4 h-4 text-xs font-bold text-white bg-red-500 border-2 border-white rounded-full -top-2 -end-7 dark:border-neutral-900">{{ notificationCount }}</div>
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" :stroke="bell" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0"></path>
                            </svg>   
                        </div>                           
                    </RouterLink>

                    <RouterLink to="/search" class="rounded hover:bg-gray-100 hover:ring hover:ring-gray-100 dark:hover:bg-neutral-800 dark:hover:ring-neutral-800">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" :stroke="search" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"></path>
                        </svg>                                                         
                    </RouterLink>
                </div>

                <div class="menu-right">
                    <template v-if="userStore.user.isAuthenticated && userStore.user.id">
                        <RouterLink :to="{name: 'profile', params:{'id': userStore.user.id}}">
                            <img :src="userStore.user.avatar" class="w-12 rounded-full">
                        </RouterLink>
                    </template>

                    <template v-else>
                        <RouterLink to="/login" class="mr-4 py-4 px-6 bg-gray-600 text-white rounded-lg">Log in</RouterLink>
                        <RouterLink to="/signup" class="py-4 px-6 bg-green-600 text-white rounded-lg">Sign up</RouterLink>
                    </template>
                </div>
            </div>

            <div v-if="showMenu">
                <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" v-model="darkMode" @click="switchMode" class="sr-only peer">
                    <div class="w-9 h-5 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                    <span class="ms-3 text-sm font-medium text-gray-900 dark:text-gray-300">Dark mode</span>
                </label>
            </div>
        </div>
    </nav>

    <main class="px-8 py-6 bg-gray-100 dark:bg-neutral-950 min-h-screen">
        <RouterView />
    </main>

    <Toast />
</template>

<script>
    import axios from 'axios'
    import Toast from '@/components/Toast.vue'
    import { useUserStore } from '@/stores/user'

    export default {
        setup() {
            const userStore = useUserStore()

            return {
                userStore
            }
        },

        components: {
            Toast
        },

        beforeCreate() {
            this.userStore.initStore()

            const token = this.userStore.user.access

            if (token) {
                axios.defaults.headers.common["Authorization"] = "Bearer " + token;
            } else {
                axios.defaults.headers.common["Authorization"] = "";
            }
        },

        data() {
            return {
                house: "#16a34a",
                map: "#000000",
                message: "#000000",
                bell: "#000000",
                search: "#000000",
                darkMode: false,
                notificationCount: 0,
                unreadMessagesCount: 0,
                showMenu: false,
                toggleDarkMode: false,
                chatSocket: null
            }
        },

        beforeMount() {
            
        },

        mounted() {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
                const newColorScheme = event.matches ? "dark" : "light";
                console.log("Changed theme ", newColorScheme)

                if (newColorScheme == 'dark') {
                    document.documentElement.classList.add('dark');
                    localStorage.setItem('dark-mode', true);
                    this.darkMode = true
                }
                else if (newColorScheme == 'light') {
                    document.documentElement.classList.remove('dark');
                    localStorage.setItem('dark-mode', false);
                    this.darkMode = false
                }

                this.getURL()
            });

            //console.log("Saved theme", localStorage.getItem('dark-mode'))
            const savedDarkMode = localStorage.getItem('dark-mode')
            console.log(savedDarkMode)

            if (savedDarkMode == "true") {
                console.log("Dark mode")
                document.documentElement.classList.add('dark');
                localStorage.setItem('dark-mode', true);
                this.darkMode = true
            }
            else if (savedDarkMode == "false") {
                console.log("Light mode")
                document.documentElement.classList.remove('dark');
                localStorage.setItem('dark-mode', false);
                this.darkMode = false
            }
            else {
                if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                    // dark mode
                    console.log("System Dark Mode")
                    console.log("Saved theme", localStorage.getItem('dark-mode'))
                    if (localStorage.getItem('dark-mode') == "false")
                        console.log("Should be light mode")

                    document.documentElement.classList.add('dark');
                    localStorage.setItem('dark-mode', true);
                    this.darkMode = true
                }
            }
        
            this.checkNotifications()
            this.checkMessages()
            //this.chatSocket = new WebSocket (`ws://${window.location.host}/ws/notifications/`)
            this.chatSocket = new WebSocket (`ws://localhost:8000/ws/notifications/`)
            this.connectWS()
        },

        methods: {
            getURL(){
                let url = this.$route.path
                console.log(url)
                if (url == "/feed")
                    this.house = "#16a34a"
                else
                    if (this.darkMode)
                        this.house = "#FFFFFF"
                    else 
                        this.house = "#000000"

                if (url == "/following")
                    this.map = "#16a34a"
                else 
                    if (this.darkMode)
                        this.map = "#FFFFFF"
                    else 
                        this.map = "#000000"

                if (url == "/chat")
                    this.message = "#16a34a"
                else
                    if (this.darkMode)
                        this.message = "#FFFFFF"
                    else 
                        this.message = "#000000"

                if (url == "/notifications")
                    this.bell = "#16a34a"
                else
                    if (this.darkMode)
                        this.bell = "#FFFFFF"
                    else 
                        this.bell = "#000000"

                if (url == "/search")
                    this.search = "#16a34a"
                else
                    if (this.darkMode)
                        this.search = "#FFFFFF"
                    else 
                        this.search = "#000000"
            },

            checkNotifications() {
                console.log("Check Notifications")
                axios
                .get('/api/notifications/check/')
                .then(response => {
                console.log(response.data);
                this.notificationCount = response.data
            })
                .catch(error => {
                console.log('Error: ', error);
            });
            },

            checkMessages() {
                console.log("Check Messages")
                axios
                .get('/api/chat/check/')
                .then(response => {
                console.log("Unread messages count: ", response.data);
                this.unreadMessagesCount = response.data
            })
                .catch(error => {
                console.log('Error: ', error);
            });
            },

            toggleMenu() {
                this.showMenu = !this.showMenu
                console.log("Toggle menu", this.showMenu)
            }, 

            switchMode() {
                console.log("Switch mode")
                if (!this.darkMode) {
                    document.documentElement.classList.add('dark');
                    localStorage.setItem('dark-mode', true);
                    this.darkMode = true
                } else {
                    document.documentElement.classList.remove('dark');
                    localStorage.setItem('dark-mode', false);
                    this.darkMode = false
                }
            },

            async connectWS() {
                this.chatSocket = await new WebSocket (`ws://localhost:8000/ws/notifications/`)
                //this.chatSocket = await new WebSocket (`ws://${window.location.host}/ws/notifications/`)

                console.log('Websocket: ', this.chatSocket)

                this.chatSocket.onerror = function(e) {
                    console.log('Websocket error: ', e);
                }

                this.chatSocket.onmessage = (e) => {
                    console.log('onMessage')
                    this.checkNotifications()
                    this.checkMessages()
                }

                this.chatSocket.onnotifcation = (e) => {
                    console.log('onNotification')
                    this.checkNotifications()
                    this.checkMessages()
                }

                this.chatSocket.onopen = function(e) {
                    console.log('onOpnen - chat socket was opened')
                }

                this.chatSocket.onclose = function(e) {
                    console.log('onClose - chat socket was closed')
                }
            },

        }
    }
</script>