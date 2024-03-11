<template>
    <form v-on:submit.prevent="submitForm" method="post">
        <div class="p-4 space-y-2 dark:text-white">  
            <p>Title </p>
            <textarea v-model="title" class="p-4 w-full bg-gray-100 rounded-lg dark:bg-neutral-700" placeholder="Give your journey a cool title!"></textarea>
            <p>Description </p>
            <textarea v-model="description" class="p-4 w-full bg-gray-100 rounded-lg dark:bg-neutral-700" placeholder="Give a biref description on what this journey is about."></textarea>
            <p>Topic </p>
            <textarea v-model="topic" class="p-4 w-full bg-gray-100 rounded-lg dark:bg-neutral-700" placeholder="Share your journey's topic."></textarea>

            <label>
                <input type="checkbox" v-model="is_private" :disabled="only_me" :checked="!only_me"> Only friends
                <input class="ml-6" type="checkbox" v-model="only_me"> Only me
            </label> 
        </div>

        <div class="p-4 border-t border-gray-100 flex justify-between dark:border-gray-950">
            <button class="inline-block py-4 px-6 bg-green-600 text-white rounded-lg">Post</button>
        </div>
    </form>
</template>

<script>
import axios from 'axios'

export default {
    props: {
        user: Object,
        journeys: Array
    },

    data() {
        return {
            title: '',
            description: '',
            topic: '',
            is_private: false,
            only_me: false,
            url: null,
        }
    },

    methods: {
        submitForm() {
            console.log('submitForm', this.title)

            let formData = new FormData()
            formData.append('title', this.title)
            formData.append('description', this.description)
            formData.append('topic', this.topic)
            formData.append('is_private', this.is_private)
            formData.append('only_me', this.only_me)

            axios
                .post('/api/journey/create/', formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    }
                })
                .then(response => {
                    console.log('data', response.data)

                    this.journeys.unshift(response.data)
                    this.title = ''
                    this.description = ''
                    this.topic = ''
                    this.is_private = false
                    this.only_me = false
                    this.url = null

                    if (this.user) {
                        this.user.journey_count += 1
                    }

                    this.$router.push(`/${response.data.id}/`)
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
    }
}
</script>