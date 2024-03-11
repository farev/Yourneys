<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-gray-200 rounded-lg dark:bg-neutral-900 dark:border-gray-950">
                <h1 class="mb-6 text-2xl dark:text-white">Edit profile</h1>

                <p class="mb-6 text-gray-500 dark:text-gray-400">
                    It is not about who you are but about what you do.  
                    - Fabian A.
                </p>

                <RouterLink to="/profile/edit/password" class="underline dark:text-white">Edit password</RouterLink>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-gray-200 rounded-lg dark:bg-neutral-900 dark:border-gray-950 dark:text-white">
                <form class="space-y-6" v-on:submit.prevent="submitForm">
                    <div>
                        <label>Name</label><br>
                        <input type="text" v-model="form.name" placeholder="Your full name" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg dark:bg-neutral-700 dark:border-gray-950">
                    </div>

                    <div>
                        <label>E-mail</label><br>
                        <input type="email" v-model="form.email" placeholder="Your e-mail address" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg dark:bg-neutral-700 dark:border-gray-950">
                    </div>

                    <div id="preview" :key="image" v-if="image" class="w-[200px] mt-3 rounded-xl">
                        <img ref="previmg" :src="image" class="w-full mt-3 rounded-xl" v-on:load="createCropper()"/>
                    </div>

                    <div class="">
                        <label class="inline-block py-4 px-6 bg-gray-600 text-white  rounded-lg">
                            <input type="file" ref="file" @change="onFileChange">
                            Select profile picture
                         </label>
                    </div>
                    
                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button class="py-4 px-6 bg-green-600 text-white rounded-lg">Save changes</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import Cropper from 'cropperjs'

import { useToastStore } from '@/stores/toast'
import { useUserStore } from '@/stores/user'

export default {
    setup() {
        const toastStore = useToastStore()
        const userStore = useUserStore()

        return {
            toastStore,
            userStore
        }
    },

    data() {
        return {
            form: {
                email: this.userStore.user.email,
                name: this.userStore.user.name
            },
            errors: [],
            cropper: {}, 
            image: this.userStore.user.avatar,
            prevImg: {},
            newImg : {}
        }
    },

    mounted() {
        //console.log(this.userStore.user.avatar)
        this.createCropper()
    },

    methods: {
        submitForm() {
            this.errors = []

            if (this.form.email === '') {
                this.errors.push('Your e-mail is missing')
            }

            if (this.form.name === '') {
                this.errors.push('Your name is missing')
            }

            if (this.errors.length === 0) {
                let formData = new FormData()
                console.log(this.newImg)
                console.log(this.$refs.file.files[0])
                formData.append('avatar', this.newImg)
                formData.append('name', this.form.name)
                formData.append('email', this.form.email)

                axios
                    .post('/api/editprofile/', formData, {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        }
                    })
                    .then(response => {
                        if (response.data.message === 'information updated') {
                            this.toastStore.showToast(5000, 'The information was saved', 'bg-emerald-500')

                            this.userStore.setUserInfo({
                                id: this.userStore.user.id,
                                name: this.form.name,
                                email: this.form.email,
                                avatar: response.data.user.get_avatar
                            })

                            this.$router.back()
                        } else {
                            this.toastStore.showToast(5000, `${response.data.message}. Please try again`, 'bg-red-300')
                        }
                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            }
        }, 

        onFileChange(e) {
            console.log("File change")
            console.log(e.target.files[0])
            this.image = URL.createObjectURL(e.target.files[0])
            console.log(this.image)
            this.createCropper()
        }, 

        createCropper() {
            console.log(this.$refs.previmg)
            this.cropper = new Cropper(this.$refs.previmg, {
                aspectRatio : 1,
                zoomable: true,
                scalable: true,
                dragMode: 'move',
                background: false,
                cropBoxMovable: false,
                cropBoxResizable: false,
                viewMode: 1,
                minCropBoxWidth: 256,
                minCropBoxHeight: 256,
                crop: () => {
                    const canvas = this.cropper.getCroppedCanvas()
                    if (canvas) {
                        canvas.toBlob((blob) => {
                            //console.log(this.userStore.user)
                            //let name = this.$refs.file.files[0].name
                            let name = this.userStore.user.name + "avatar.png"
                            this.newImg = new File([blob], name, {type: "image/png"});
                        })
                    }
                }
            })
        }, 

        blobToFile(theBlob, fileName){
            //A Blob() is almost a File() - it's just missing the two properties below which we will add
            theBlob.lastModifiedDate = new Date();
            theBlob.name = fileName;
            return theBlob;
        }
    }
}
</script> 

<style>
    .cropper-view-box,
    .cropper-face {
      border-radius: 50%;
    }

    /* The css styles for `outline` do not follow `border-radius` on iOS/Safari (#979). */
    .cropper-view-box {
        outline: 0;
        box-shadow: 0 0 0 1px #39f;
    }
</style>