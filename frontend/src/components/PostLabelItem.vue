<template>
    <RouterLink :to="{name: 'postview', params: {id: post.id}}" >
        <div class="mb-6 flex items-center justify-between">
        <div class="flex items-center space-x-6">
            <p>
                <strong>
                    {{ post.label }}
                </strong>
            </p>
        </div>

        <p class="text-gray-600">{{ post.created_at_formatted }} ago</p>
    </div>
   
    <p>{{ post.body }}</p>
    </RouterLink>


</template>

<script>
import axios from 'axios'
import { RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'

export default {
    props: {
        post: Object
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

    methods: {

    },
}
</script>