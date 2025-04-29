<template>
  <v-row class="pa-5">
    <v-col cols="12">
      <v-card elevation="0" color="white" rounded="lg">
        <InfoPanel
          altText="Forbidden"
          title="403-Forbidden"
          message="You do not have permission to access this page."
        />
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default',
  middleware: 'auth',
})
</script>
