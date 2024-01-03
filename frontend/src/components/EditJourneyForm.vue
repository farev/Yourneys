<template>
    <form v-on:submit.prevent="submitForm" method="post">
        <div class="p-4">  
            <p>Title </p>
            <textarea v-model="title" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="Give your journey a cool title!"> {{ journey.title }} </textarea>
            <p>Description </p>
            <textarea v-model="description" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="Give a biref description on what this journey is about.">{{ journey.description }}</textarea>
            <p>Topic </p>
            <textarea v-model="topic" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="Share your journey's topic.">{{ journey.topic }}</textarea>

            <label>
                <input type="checkbox" v-model="is_private"> Private
            </label> 
        </div>

        <div class="p-4 border-t border-gray-100 flex justify-between">
            <button class="inline-block py-4 px-6 bg-green-600 text-white rounded-lg">Post</button>
        </div>
    </form>
</template>

<script>
import axios from 'axios'

export default {
    props: {
        user: Object,
        journey: Object
    },

    data() {
        return {
            title: '',
            description: '',
            topic: '',
            is_private: false,
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

            axios
                .post(`/api/journey/${this.$route.params.id}/edit/`, formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    }
                })
                .then(response => {
                    console.log('data', response.data)

                    //this.journeys.unshift(response.data)
                    this.title = ''
                    this.description = ''
                    this.topic = ''
                    this.is_private = false
                    this.url = null

                    /*if (this.user) {
                        this.user.posts_count += 1
                    }*/
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
    }
}
</script>