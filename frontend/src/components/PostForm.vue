<template>
    <form v-on:submit.prevent="submitForm" method="post">
        <div class="p-4 dark:text-white">  
            <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg mb-2 dark:bg-neutral-700" placeholder="What are you thinking about?"></textarea>

            <div class="flex justify-between">
                <select :key="label" v-model="label" class="bg-gray-100 rounded-lg text-slate-950 h-8 p-1" :style="{'background-color' : setColor('bg'), 'color' : setColor('t')}">
                    <option value="" disabled selected>Select label</option>
                    <option value="Start" :disabled="checkStart('Start')">Start</option>
                    <option value="Update" :disabled="checkStart()">Update</option>
                    <option value="Milestone" :disabled="checkStart()">Milestone</option>
                    <option value="End" :disabled="checkStart()">End</option>
                </select>

                <label class="dark:text-white">
                    <input type="checkbox" v-model="is_private"> Private
                </label>
            </div>

            <div id="preview" :key="urls.length" v-if="urls.length" class="flex justify-start space-x-2">
                <div v-for="url in urls">
                    <div :id="url">
                        <img v-if="!isVideo(url.fileName)" :src="url.url" class="w-[200px] mt-3 rounded-xl" />
                        <video v-if="isVideo(url.fileName)" :src="url.url" class="w-[200px] mt-3 rounded-xl" controls></video>
                        
                        <div @click="removeFile(url)" class="flex justify-end">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                                <path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                            </svg>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="p-4 border-t border-gray-100 flex justify-between dark:border-gray-950">
            <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
                <input type="file" ref="file" @change="onFileChange" multiple>
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
        journey: Object
    },

    data() {
        return {
            body: '',
            journeyid: '',
            label: '',
            is_private: false,
            urls: [],
            defaultColor: "#f3f4f6",
            defaultTextColor: "black"
        }
    },

    mounted() {
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                // dark mode
                this.defaultColor = "#525252"
                this.defaultTextColor = "white"
            }
        },

    methods: {
        submitForm() {
            console.log('submitForm', this.body)
            
            this.journeyid = this.journey.id;
            console.log('JourneyID', this.journeyid)
            let formData = new FormData()

            console.log(this.$refs.file.files.length)

            /*for (let i = 0; i < this.$refs.file.files.length; i++) {
                formData.append('file', this.$refs.file.files[i])
                console.log("File:", this.$refs.file.files[i])
            }*/

            for (let i = 0; i < this.urls.length; i++) {
                formData.append('file', this.urls[i].fileName)
                console.log("File: ", this.urls[i].fileName)
            }

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
                    this.urls = []

                    if (this.user) {
                        this.user.posts_count += 1
                    }
                })
                .catch(error => {
                    console.log('error', error)
                })         
        },
        
        onFileChange(e) {
            console.log(this.$refs.file.files)
            for (const file of e.target.files) {
                let urlO = {fileName: file, url: URL.createObjectURL(file)}
                this.urls.push(urlO)
                console.log(this.urls)
            }
        },
        
        removeFile(url) {
            console.log("Remove: ", url.fileName)
            /*this.fileList = Array.from(this.$refs.file.files)
            for (var i = 0; i < fileList.length; i++) {
                if (fileList[i] == url.fileName) {
                    fileList.splice(i,i)
                    this.$refs.file.files = fileList
                    console.log(this.$refs.file.files)
                }
            }*/
            const index = this.urls.indexOf(url)
            this.urls.splice(index, index+1)
            console.log(this.urls)
            document.getElementById(url).remove()
        },

        isVideo(file){
            const isVideo =['.mpg', '.mp2', '.mpeg', '.mpe', '.mpv', '.mp4', '.MOV', '.mov'];
            let video = false;
            console.log(file.name)

            isVideo.forEach(ext => {
                if(file.name.includes(ext)) {
                    video = true;
                }
            });
            console.log(video)
            return video
        },

        setColor(a) {
            if (a == "bg") {
                switch(this.label) {
                    case "Start":
                        return "#2ECC71"
                    case "Update":
                        return "#1E8449"
                    case "Milestone":
                        return "#F6851B"
                    case "End":
                        return "#2980B9"
                    default:
                        return this.defaultColor
                }
            }
            else if (a == "t") {
                switch(this.label) {
                    case "Start":
                        return "black"
                    case "Update":
                        return "white"
                    case "Milestone":
                        return "white"
                    case "End":
                        return "white"
                    default:
                        return this.defaultTextColor
                }
            }   
        }, 

        checkStart(b) {
            if (this.journey.posts.length) {
                if (b == "Start")
                    return true
                else return false
            }
            else {
                if (b == "Start")
                    return false
                else return true
            }
        }
    }
}
</script>