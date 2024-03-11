<template>
    <form v-on:submit.prevent="submitForm" method="post">
        <div class="p-4 space-y-2 dark:text-white">  
            <p>Title </p>
            <textarea v-model="title" class="p-4 w-full bg-gray-100 rounded-lg dark:bg-neutral-700" placeholder="Give your journey a cool title!"> {{ journey.title }} </textarea>
            <p>Description </p>
            <textarea v-model="description" class="p-4 w-full bg-gray-100 rounded-lg dark:bg-neutral-700" placeholder="Give a biref description on what this journey is about.">{{ journey.description }}</textarea>
            <p>Topic </p>
            <textarea v-model="topic" class="p-4 w-full bg-gray-100 rounded-lg dark:bg-neutral-700" placeholder="Share your journey's topic.">{{ journey.topic }}</textarea>

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
import { useToastStore } from '@/stores/toast'

export default {
    setup() {
        const toastStore = useToastStore()

        return {
            toastStore,
        }
    },

    props: {
        user: Object,
        journey: Object
    },

    data() {
        return {
            title: this.journey.title,
            description: this.journey.description,
            topic: this.journey.topic,
            is_private: this.journey.is_private,
            only_me: this.journey.only_me,
            url: null,
        }
    },

    methods: {
        submitForm() {
            this.$emit('editJourney', this.journey)
            console.log('submitForm', this.title)

            let formData = new FormData()
            formData.append('title', this.title)
            formData.append('description', this.description)
            formData.append('topic', this.topic)
            formData.append('is_private', this.is_private)
            formData.append('only_me', this.only_me)

            axios
                .post(`/api/journey/${this.$route.params.id}/edit/`, formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    }
                })
                .then(response => {
                    console.log('data', response.data)
                    this.toastStore.showToast(5000, 'The information was saved', 'bg-emerald-500')

                    //this.journeys.unshift(response.data)
                    this.title = ''
                    this.description = ''
                    this.topic = ''
                    this.is_private = false
                    this.only_me = false
                    this.url = null

                    this.$router.go()
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
    }
}
</script>