<template>
  <div class="min-h-screen flex flex-col bg-gray-100 dark:bg-gray-900 transition-colors">
    <!-- Navbar with Logo and Title -->
    <header class="flex justify-between items-center p-4 container mx-auto bg-gray-800 dark:bg-gray-900 shadow-md">
      <div class="flex items-center">
        <img
          class="h-8 w-auto"
          src="https://tailwindcss.com/plus-assets/img/logos/mark.svg?color=indigo&shade=500"
          alt="Supply Management"
        />
        <span class="ml-2 text-xl font-bold text-white">Supply Management</span>
      </div>
      <!-- Dark Mode Toggle -->
      <button
        @click="$emit('toggle-dark')"
        class="p-2 rounded-full bg-gray-700 hover:bg-gray-600"
      >
        <span v-if="!isDark">🌙</span>
        <span v-else>☀️</span>
      </button>
    </header>
    <main class="flex-grow flex items-center justify-center">
      <slot />
    </main>
  </div>
</template>

<script>
export default {
  props: {
    isDark: Boolean,
  },
};
</script>
