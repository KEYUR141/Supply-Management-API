<template>
  <div class="flex items-center justify-center min-h-[80vh] bg-gray-100 dark:bg-gray-900 transition-colors">
    <div class="w-full max-w-lg bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-12"> <!-- Increased max-w and padding -->
      <!-- Header -->
      <h2 class="text-3xl font-bold text-gray-800 dark:text-gray-200 mb-8">Login</h2> <!-- Larger text and more margin -->

      <!-- Login Form -->
      <form @submit.prevent="login" class="space-y-6"> <!-- Increased spacing -->
        <input
          v-model="username"
          placeholder="Username or Email"
          required
          class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 
                 bg-gray-50 dark:bg-gray-700 text-gray-800 dark:text-gray-200 
                 focus:ring-2 focus:ring-blue-500 outline-none"
        />

        <div class="relative">
          <input
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="Password"
            required
            class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 
                   bg-gray-50 dark:bg-gray-700 text-gray-800 dark:text-gray-200 
                   focus:ring-2 focus:ring-blue-500 outline-none pr-12"
          />
          <button
            type="button"
            @click="showPassword = !showPassword"
            class="absolute right-2 top-1/2 -translate-y-1/2 flex items-center justify-center h-8 w-8 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition"
            tabindex="-1"
            aria-label="Toggle password visibility"
          >
            <span class="material-icons" style="font-size:22px;">
              {{ showPassword ? 'visibility_off' : 'visibility' }}
            </span>
          </button>
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg 
                 font-semibold shadow-md transition"
        >
          Login
        </button>
      </form>

      <!-- Messages -->
      <p v-if="error" class="mt-6 text-red-500 text-base text-center">{{ error }}</p>
      <p v-if="success" class="mt-6 text-green-500 text-base text-center">{{ success }}</p>

      <!-- Signup Redirect -->
      <p class="mt-8 text-center text-base text-gray-600 dark:text-gray-400">
        Not registered? 
        <router-link to="/signup" class="text-blue-600 hover:underline">Signup</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import api from "../api";
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
      showPassword: false
    };
  },
  methods: {
    async login() {
      try {
        const response = await api.login({
          username: this.username,
          password: this.password
        });
        localStorage.setItem("access", response.data.access);
        localStorage.setItem("refresh", response.data.refresh);
        this.$router.push("/dashboard");
      } catch (err) {
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
