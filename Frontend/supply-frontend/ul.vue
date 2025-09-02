<template>
  <div class="flex items-center justify-center min-h-[80vh] bg-gray-100 dark:bg-gray-900 transition-colors">
    <div class="w-full max-w-md bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8">
      <!-- Header -->
      <h2 class="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-6">Login</h2>

      <!-- Login Form -->
      <form @submit.prevent="login" class="space-y-4">
        <input
          v-model="username"
          placeholder="Username or Email"
          required
          class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 
                 bg-gray-50 dark:bg-gray-700 text-gray-800 dark:text-gray-200 
                 focus:ring-2 focus:ring-blue-500 outline-none"
        />

        <input
          v-model="password"
          placeholder="Password"
          type="password"
          required
          class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 
                 bg-gray-50 dark:bg-gray-700 text-gray-800 dark:text-gray-200 
                 focus:ring-2 focus:ring-blue-500 outline-none"
        />

        <!-- Submit Button -->
        <button
          type="submit"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg 
                 font-semibold shadow-md transition"
        >
          Login
        </button>
      </form>

      <!-- Messages -->
      <p v-if="error" class="mt-4 text-red-500 text-sm">{{ error }}</p>
      <p v-if="success" class="mt-4 text-green-500 text-sm">{{ success }}</p>

      <!-- Signup Redirect -->
      <p class="mt-4 text-center text-sm text-gray-600 dark:text-gray-400">
        Not registered? 
        <router-link to="/signup" class="text-blue-600 hover:underline">Signup</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import api from "./src/api";
import AuthLayout from "../layouts/AuthLayout.vue"; 
export default {
  name: "UserLogin",
  layout: AuthLayout,
  data() {
    return {
      username: "",
      password: "",
      error: null,
      success: null,
    };
  },
  methods: {
    async login() {
      try {
        const response = await api.login({
          username: this.username,
          password: this.password,
        });
        localStorage.setItem("access", response.data.access);
        localStorage.setItem("refresh", response.data.refresh);
        this.$router.push("/dashboard");
      } catch (err) {
        // Show backend error if available
        if (err.response && err.response.data) {
          this.error = err.response.data.detail || JSON.stringify(err.response.data);
        } else {
          this.error = "Login failed. Check credentials.";
        }
      }
    },
  },
};
</script>


