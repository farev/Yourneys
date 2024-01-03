<template>
    <form v-on:submit.prevent="submitForm" method="post">
        <div class="p-4">  
            <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>

            <label>
                <input type="checkbox" v-model="is_private"> Private
            </label>

            <select v-model="label" class="space-x-5" >
                <option value="Start">Start</option>
                <option value="Update">Update</option>
                <option value="Milestone">Milestone</option>
                <option value="End">End</option>
            </select>

            <div id="preview" v-if="url">
                <img :src="url" class="w-[100px] mt-3 rounded-xl" />
            </div>
        </div>

        <div class="p-4 border-t border-gray-100 flex justify-between">
            <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
                <input type="file" ref="file" @change="onFileChange">
                Attach file
            </label>

            <button class="inline-block py-4 px-6 bg-green-600 text-white rounded-lg">Post</button>
        </div>
    </form>
</template>

<script>
import axios from 'axios'

export default {
    props: {
        user: Object,
        posts: Array,
        journey: String
    },

    data() {
        return {
            body: '',
            journeyid: '',
            label: '',
            is_private: false,
            url: null,
        }
    },

    methods: {
        submitForm() {
            console.log('submitForm', this.body)
            
            this.journeyid = this.journey.id;
            console.log('JourneyID', this.journeyid)
            let formData = new FormData()
            formData.append('image', this.$refs.file.files[0])
            formData.append('body', this.body)
            formData.append('journeyid', this.journeyid)
            formData.append('label', this.label)
            formData.append('is_private', this.is_private) 

            axios
                .post('/api/posts/create/', formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    }
                })
                .then(response => {
                    console.log('data', response.data)
                    console.log('Posts in Journey', this.journey.posts)

                    //this.journey.posts.unshift(response.data)
                    this.posts.unshift(response.data)
                    this.body = ''
                    this.journeyid = ''
                    this.label = ''
                    this.is_private = false
                    this.$refs.file.value = null
                    this.url = null

                    if (this.user) {
                        this.user.posts_count += 1
                    }
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
    }
}
</script>