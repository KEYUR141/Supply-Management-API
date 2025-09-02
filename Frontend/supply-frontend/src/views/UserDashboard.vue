<!-- <template>
  <div>
    <h1>Welcome to the Dashboard!</h1>
    <div v-if="user">
      <p>User: {{ user.username }}</p>
    </div>
    <button @click="logout">Logout</button>
  </div>
</template>

<script>
import api from "../api";
import DefaultLayout from "../layouts/DefaultLayout.vue";
export default {
  name: "UserDashboard",
  layout: DefaultLayout,
  data() {
    return { user: null };
  },
  async created() {
    try {
      const res = await api.getUser();
      console.log("User API response:", res.data);
      // Adjust this line based on actual response structure
      this.user = res.data.Data ? res.data.Data[0] : res.data;
    } catch (err) {
      console.error("❌ Failed to fetch user:", err);
      this.$router.push("/login");
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      this.$router.push('/login');
    }
  }
};
</script> -->


<template>
  <div class="max-w-xl mx-auto mt-10 p-6 bg-white rounded shadow">
    <h1 class="text-2xl font-bold mb-4">Welcome to the Dashboard!</h1>
    <div v-if="user">
      <p class="mb-2">Username: <span class="font-semibold">{{ user.username }}</span></p>
      <p v-if="user.email">Email: <span class="font-semibold">{{ user.email }}</span></p>
    </div>
    <button
      @click="logout"
      class="mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
    >
      Logout
    </button>
  </div>
</template>

<script>
import api from "../api";
export default {
  name: "UserDashboard",
  data() {
    return { user: null };
  },
  async created() {
    try {
      const res = await api.getUser();
      // Adjust this line based on your backend response structure
      this.user = res.data.Data ? res.data.Data[0] : res.data;
    } catch (err) {
      this.$router.push("/login");
    }
  },
  methods: {
    logout() {
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      this.$router.push("/login");
    }
  }
};
</script>