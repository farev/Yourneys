<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-gray-200 rounded-lg dark:bg-neutral-900 dark:border-gray-950">
                <h1 class="mb-6 text-2xl dark:text-white">Log in</h1>

                <p class="mb-6 text-gray-500 dark:text-gray-400">
                    Yourneys is the perfect place to share and record all of your journeys. 
                    So go show the world what you are creating, exploring, and experiencing!
                </p>

                <p class="font-bold dark:text-white">
                    Don't have an account? <RouterLink :to="{'name': 'signup'}" class="underline">Click here</RouterLink> to create one!
                </p>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-gray-200 rounded-lg dark:bg-neutral-900 dark:border-gray-950">
                <form class="space-y-6 dark:text-white" v-on:submit.prevent="submitForm">
                    <div>
                        <label>E-mail</label><br>
                        <input type="email" v-model="form.email" placeholder="Your e-mail address" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg dark:bg-neutral-700 dark:border-gray-950">
                    </div>

                    <div>
                        <label>Password</label><br>
                        <input type="password" v-model="form.password" placeholder="Your password" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg dark:bg-neutral-700 dark:border-gray-950">
                    </div>

                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button class="py-4 px-6 bg-green-600 text-white rounded-lg">Log in</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

import { useUserStore } from '@/stores/user'

export default {
    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    },

    data() {
        return {
            form: {
                email: '',
                password: '',
            },
            errors: []
        }
    },
    methods: {
        async submitForm() {
            this.errors = []

            if (this.form.email === '') {
                this.errors.push('Your e-mail is missing')
            }

            if (this.form.password === '') {
                this.errors.push('Your password is missing')
            }

            if (this.errors.length === 0) {
                await axios
                    .post('/api/login/', this.form)
                    .then(response => {
                        this.userStore.setToken(response.data)

                        axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access;
                    })
                    .catch(error => {
                        console.log('error', error)

                        this.errors.push('The email or password is incorrect! Or the user is not activated!')
                    })
            }
            
            if (this.errors.length === 0) {
                await axios
                    .get('/api/me/')
                    .then(response => {
                        this.userStore.setUserInfo(response.data)

                        this.$router.push('/feed')
                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            }
        }
    }
}
</script>