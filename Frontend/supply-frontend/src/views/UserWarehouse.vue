<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-2 text-gray-900 dark:text-gray-100">Warehouses</h1>
    <button
      @click="openAddModal"
      class="flex items-center bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 mb-6"
    >
      <span class="material-icons mr-2">add</span>
      Add Warehouse
    </button>

    <!-- Search Bar -->
    <div class="mb-4 flex">
      <input
        v-model="search"
        type="text"
        placeholder="Search warehouse by name, location, incharge.."
        class="input-style flex-1"
      />
    </div>

    <!-- Responsive Table Wrapper -->
    <div class="overflow-x-auto overflow-y-auto max-w-full max-h-[70vh] rounded shadow mb-6">
      <table class="min-w-full bg-white dark:bg-gray-800">
        <thead>
          <tr>
            <th class="py-2 px-4 border-b text-left text-gray-700 dark:text-gray-200">Sr.No</th>
            <th class="py-2 px-4 border-b text-left text-gray-700 dark:text-gray-200">Warehouse Name</th>
            <th class="py-2 px-4 border-b text-left text-gray-700 dark:text-gray-200">Location</th>
            <th class="py-2 px-4 border-b text-left text-gray-700 dark:text-gray-200">Created</th>
            <th class="py-2 px-4 border-b text-left text-gray-700 dark:text-gray-200">Updated</th>
            <th class="py-2 px-4 border-b text-left text-gray-700 dark:text-gray-200">Incharge</th>
            <th class="py-2 px-4 border-b text-left text-gray-700 dark:text-gray-200">Items</th>
            <th class="py-2 px-4 border-b text-left text-gray-700 dark:text-gray-200">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(warehouse, idx) in filteredWarehouses" :key="warehouse.uuid">
            <td class="py-2 px-4 border-b text-left text-gray-800 dark:text-gray-100">{{ idx + 1 }}</td>
            <td class="py-2 px-4 border-b text-left text-gray-800 dark:text-gray-100">{{ warehouse.name }}</td>
            <td class="py-2 px-4 border-b text-left text-gray-800 dark:text-gray-100">{{ warehouse.location }}</td>
            <td class="py-2 px-4 border-b text-left text-gray-800 dark:text-gray-100">{{ formatDate(warehouse.created_at) }}</td>
            <td class="py-2 px-4 border-b text-left text-gray-800 dark:text-gray-100">{{ formatDate(warehouse.updated_at) }}</td>
            <td class="py-2 px-4 border-b text-left text-gray-800 dark:text-gray-100">
              <span v-if="warehouse.incharge">
                {{ warehouse.incharge.first_name }} {{ warehouse.incharge.last_name }} ({{ warehouse.incharge.role }})
              </span>
              <span v-else>-</span>
            </td>
            <td class="py-2 px-4 border-b text-left">
              <span v-if="warehouse.items">{{ warehouse.items.length }}</span>
              <span v-else>-</span>
            </td>
            <td class="py-2 px-4 border-b text-left">
              <button @click="editWarehouse(warehouse)" class="text-blue-600 hover:text-blue-800 mr-2">
                <span class="material-icons" style="font-size:20px;">edit</span>
              </button>
              <button @click="openDeleteModal(warehouse.uuid)" class="text-red-600 hover:text-red-800">
                <span class="material-icons" style="font-size:20px;">delete</span>
              </button>
            </td>
          </tr>
          <tr v-if="filteredWarehouses.length === 0">
            <td colspan="8" class="py-4 text-center text-gray-500">No warehouses found.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add Warehouse Modal (simple example) -->
    <div v-if="showAddModal" class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-900 p-6 rounded shadow-lg w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">Add Warehouse</h2>
        <form @submit.prevent="addWarehouse">
          <input v-model="newWarehouse.name" type="text" placeholder="Name" class="input-style mb-2" required />
          <input v-model="newWarehouse.location" type="text" placeholder="Location" class="input-style mb-4" required />
          <select v-model="newWarehouse.incharge" class="input-style mb-4" required>
            <option value="" disabled>Select Incharge</option>
            <option v-for="user in inchargeUsers" :key="user.uuid" :value="user.uuid">
              {{ user.username }} - {{ user.first_name }} {{ user.last_name }}
            </option>
          </select>
          <div class="flex justify-end space-x-2">
            <button type="button" @click="closeAddModal" class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400">Cancel</button>
            <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Add</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-900 p-6 rounded shadow-lg w-full max-w-md">
        <h2 class="text-xl font-bold mb-4 text-red-600">Delete Warehouse</h2>
        <p class="mb-6">Are you sure you want to delete this warehouse?</p>
        <div class="flex justify-end space-x-2">
          <button @click="closeDeleteModal" class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400">Cancel</button>
          <button @click="confirmDeleteWarehouse" class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">Delete</button>
        </div>
      </div>
    </div>

    <!-- Edit Warehouse Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-900 p-6 rounded shadow-lg w-full max-w-md">
        <h2 class="text-xl font-bold mb-4 text-gray-900 dark:text-gray-100">Update Warehouse</h2>
        <form @submit.prevent="updateWarehouse">
          <input v-model="editWarehouseData.name" type="text" placeholder="Name" class="input-style mb-2" required />
          <input v-model="editWarehouseData.location" type="text" placeholder="Location" class="input-style mb-2" required />
          <select v-model="editWarehouseData.incharge" class="input-style mb-4" required>
            <option value="" disabled>Select Incharge</option>
            <option v-for="user in inchargeUsers" :key="user.uuid" :value="user.uuid">
              {{ user.username }} - {{ user.first_name }} {{ user.last_name }}
            </option>
          </select>
          <div class="flex justify-end space-x-2">
            <button type="button" @click="closeEditModal" class="px-4 py-2 bg-gray-300 dark:bg-gray-700 rounded hover:bg-gray-400 dark:hover:bg-gray-600 text-gray-900 dark:text-gray-100">Cancel</button>
            <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Update</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../api";
export default {
  name: "UserWarehouse",
  data() {
    return {
      warehouses: [],
      search: "",
      showAddModal: false,
      showDeleteModal: false,
      showEditModal: false,
      warehouseToDelete: null,
      newWarehouse: {
        name: "",
        location: "",
        incharge: ""
      },
      editWarehouseData: {
        name: "",
        location: "",
        incharge: ""
      },
      inchargeUsers: []
    };
  },
  computed: {
    filteredWarehouses() {
      if (!this.search) return this.warehouses;
      const term = this.search.toLowerCase();
      return this.warehouses.filter(w => {
        const name = w.name?.toLowerCase() || "";
        const location = w.location?.toLowerCase() || "";
        const incharge =
          w.incharge
            ? [
                w.incharge.username,
                w.incharge.first_name,
                w.incharge.last_name
              ]
                .filter(Boolean)
                .map(str => str.toLowerCase())
                .join(" ")
            : "";
        return (
          name.includes(term) ||
          location.includes(term) ||
          incharge.includes(term)
        );
      });
    }
  },
  methods: {
    async fetchWarehouses() {
      try {
        const res = await api.getWarehouses();
        this.warehouses = res.data;
      } catch (err) {
        console.error("Failed to fetch warehouses:", err);
      }
    },
    async fetchInchargeUsers() {
      try {
        const res = await api.getInchargeUsers();
        // Log the response to debug
        console.log("get_user response:", res.data);
        // Adjust this line based on actual response structure
        this.inchargeUsers = Array.isArray(res.data.Data)
          ? res.data.Data.filter(
              user =>
                user.role &&
                user.role.toLowerCase().includes('incharge')
            )
          : [];
      } catch (err) {
        console.error("Failed to fetch incharge users:", err);
        this.inchargeUsers = [];
      }
    },
    async addWarehouse() {
      try {
        await api.addWarehouse({
          name: this.newWarehouse.name,
          location: this.newWarehouse.location,
          incharge_id: this.newWarehouse.incharge // This should be the UUID of the selected user
        });
        this.closeAddModal();
        this.newWarehouse = { name: "", location: "", incharge: "" };
        this.fetchWarehouses();
      } catch (err) {
        console.error("Failed to add warehouse:", err);
      }
    },
    openAddModal() {
      this.showAddModal = true;
      this.fetchInchargeUsers();
    },
    closeAddModal() {
      this.showAddModal = false;
      this.newWarehouse = { name: "", location: "", incharge: "" };
    },
    editWarehouse(warehouse) {
      this.showEditModal = true;
      this.editWarehouseData = {
        uuid: warehouse.uuid,
        name: warehouse.name,
        location: warehouse.location,
        incharge: warehouse.incharge ? warehouse.incharge.uuid : ""
      };
      this.fetchInchargeUsers(); // Make sure the dropdown is populated
    },
    closeEditModal() {
      this.showEditModal = false;
      this.editWarehouseData = { name: "", location: "", incharge: "" };
    },
    openDeleteModal(uuid) {
      this.warehouseToDelete = uuid;
      this.showDeleteModal = true;
    },
    closeDeleteModal() {
      this.showDeleteModal = false;
      this.warehouseToDelete = null;
    },
    async confirmDeleteWarehouse() {
      try {
        await api.deleteWarehouse(this.warehouseToDelete);
        this.closeDeleteModal();
        this.fetchWarehouses();
      } catch (err) {
        console.error("Failed to delete warehouse:", err);
        this.closeDeleteModal();
      }
    },
    async updateWarehouse() {
      try {
        await api.updateWarehouse(this.editWarehouseData.uuid, {
          name: this.editWarehouseData.name,
          location: this.editWarehouseData.location,
          incharge_id: this.editWarehouseData.incharge
        });
        this.closeEditModal();
        this.fetchWarehouses();
      } catch (err) {
        console.error("Failed to update warehouse:", err);
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return "-";
      const date = new Date(dateStr);
      return isNaN(date) ? "-" : date.toLocaleDateString();
    }
  },
  mounted() {
    this.fetchWarehouses();
  }
};
</script>

<style>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');
.input-style {
  @apply w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 
         bg-gray-50 dark:bg-gray-700 text-gray-800 dark:text-gray-200 mb-2;
}
</style>