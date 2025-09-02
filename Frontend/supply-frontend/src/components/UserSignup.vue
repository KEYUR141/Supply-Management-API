<template>
  <div class="flex items-center justify-center w-full">
    <div
      class="w-full max-w-md bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg transition-colors"
    >
      <h2 class="text-2xl font-bold mb-6 text-center text-gray-900 dark:text-white">
        Create Account
      </h2>

      <form @submit.prevent="signup">
        <input
          type="text"
          placeholder="Username"
          v-model="username"
          class="w-full mb-4 p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white"
        />
        <input
          type="email"
          placeholder="Email"
          v-model="email"
          class="w-full mb-4 p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white"
        />
        <input
          type="text"
          placeholder="First Name"
          v-model="first_name"
          class="w-full mb-4 p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white"
        />
        <input
          type="text"
          placeholder="Last Name"
          v-model="last_name"
          class="w-full mb-4 p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white"
        />

        <!-- Password field with toggle -->
        <div class="relative mb-4">
          <input
            :type="showPassword ? 'text' : 'password'"
            placeholder="Password"
            v-model="password"
            class="w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white"
          />
          <button
            type="button"
            @click="showPassword = !showPassword"
            class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 dark:text-gray-300"
            tabindex="-1"
          >
            <span class="material-icons">
              {{ showPassword ? 'visibility_off' : 'visibility' }}
            </span>
          </button>
        </div>

        <!-- Confirm Password field with toggle -->
        <div class="relative mb-4">
          <input
            :type="showPassword2 ? 'text' : 'password'"
            placeholder="Confirm Password"
            v-model="password2"
            class="w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white"
          />
          <button
            type="button"
            @click="showPassword2 = !showPassword2"
            class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 dark:text-gray-300"
            tabindex="-1"
          >
            <span class="material-icons">
              {{ showPassword2 ? 'visibility_off' : 'visibility' }}
            </span>
          </button>
        </div>

        <select
          v-model="role"
          class="input-style mb-4"
          required
        >
          <option value="" disabled>Select Role</option>
          <option value="admin">Admin</option>
          <option value="manager">Manager</option>
          <option value="employee">Employee</option>
          <option value="incharge">Warehouse-Incharge</option>
          <option value="vendor">Vendor</option>
          <option value="auditor">Auditor</option>
        </select>

        <button
          type="submit"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg shadow-md"
        >
          Signup
        </button>
        <div v-if="success" class="mt-4 text-green-600 text-center">
          {{ success }}
        </div>
        <div v-if="error" class="mt-4 text-red-600 text-center">
          {{ error }}
        </div>
      </form>

      <p class="mt-6 text-center text-sm text-gray-600 dark:text-gray-400">
        Already have an account?
        <router-link to="/login" class="text-blue-500 hover:underline">
          Login
        </router-link>
      </p>
    </div>
  </div>
</template>

<script>
import api from "../axios";

export default {
  data() {
    return {
      username: "",
      email: "",
      first_name: "",
      last_name: "",
      password: "",
      password2: "",
      role: "",
      error: null,
      success: null,
      isDark: false,
      showPassword: false,
      showPassword2: false
    };
  },
  methods: {
    async signup() {
      try {
        const response = await api.post("auth/register/", {
          username: this.username,
          email: this.email,
          first_name: this.first_name,
          last_name: this.last_name,
          password: this.password,
          password2: this.password2,
          role: this.role,
        });
        this.success = "Signup successful!";
        this.error = null;
        console.log("Signup response:", response.data);
      } catch (err) {
        console.error("Signup error:", err.response?.data || err.message);
        this.error = JSON.stringify(err.response?.data) || "Signup failed";
        this.success = null;
      }
    },
    toggleDarkMode() {
      this.isDark = !this.isDark;
      document.documentElement.classList.toggle("dark", this.isDark);
    },
  },
};
</script>

<style>
/* ✅ Common input styles (to avoid repeating Tailwind classes) */
.input-style {
  @apply w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 
         bg-gray-50 dark:bg-gray-700 text-gray-800 dark:text-gray-200 
         focus:ring-2 focus:ring-blue-500 outline-none transition;
}
</style>

