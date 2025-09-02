<template>
  <component
    :is="layout"
    :isDark="isDark"
    @toggle-dark="toggleDarkMode"
    @logout="logout"
  >
    <router-view />
  </component>
</template>

<script>
import DefaultLayout from './layouts/DefaultLayout.vue'
import AuthLayout from './layouts/AuthLayout.vue'

export default {
  name: "App",
  data() {
    return {
      isDark: false
    }
  },
  computed: {
    layout() {
      const layout = this.$route.meta.layout
      if (layout === 'auth') return AuthLayout
      return DefaultLayout
    }
  },
  methods: {
    toggleDarkMode() {
      this.isDark = !this.isDark;
      document.documentElement.classList.toggle("dark", this.isDark);
    },
    logout() {
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      this.$router.replace('/login');
    }
  }
}
</script>

<style>
body {
  margin: 0;
  font-family: 'Inter', sans-serif;
}
</style>
