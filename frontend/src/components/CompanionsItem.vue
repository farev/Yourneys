<template>
    <div v-if="journey.companions.length" class="p-4 bg-white border border-gray-200 rounded-lg dark:bg-neutral-900 dark:border-gray-950">
        <p class="mb-2 dark:text-white">
            <strong>Companions</strong>
        </p>

        <div 
            v-for="companion in journey.companions"
            v-bind:key="companion.id"
            v-bind:id="companion.id"
        >
            <div class="p-4 text-center bg-gray-100 rounded-lg mt-2 dark:bg-neutral-800 dark:border-gray-950">
                
                <img :src="companion.get_avatar" class="mb-3 rounded-full">
        
                <p class="dark:text-white">
                    <strong>
                        <RouterLink :to="{name: 'profile', params:{'id': companion.id}}">{{ companion.name }}</RouterLink>
                    </strong>
                </p>

                <button 
                    v-if="journey.created_by.id===userStore.user.id"
                    class="inline-block mt-5 py-2 px-3 bg-red-600 text-xs text-white rounded-lg"
                    @click="removeCompanion(companion.id)"
                >
                    Remove
                </button>
            </div>
            
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'


export default {
    name: 'FriendsItem',

    props: {
        journey: Object
    },

    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()

        return {
            userStore,
            toastStore
        }
    },

    data() {
        return {

        }
    },

    mounted() {
 
    },

    methods: {
        removeCompanion(compID) {
            axios
                .post(`/api/journey/${this.journey.id}/${compID}/remove/`)
                .then(response => {
                    console.log('data', response.data)

                    if (response.data.message) {
                        this.toastStore.showToast(5000, 'Companion removed', 'bg-emerald-300')
                    }

                    document.getElementById(compID).remove()
                })
                .catch(error => {
                    console.log('error', error)
                })
        }
    }
}
</script>