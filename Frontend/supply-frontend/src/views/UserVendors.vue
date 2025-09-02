<template>
  <div :class="isDark ? 'dark' : ''">
    <div class="p-6 bg-gray-100 dark:bg-gray-900 min-h-screen transition-colors">
      <div class="flex justify-between items-center mb-4">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">Vendors</h1>
       
      </div>
      <button
        @click="openAddModal"
        class="flex items-center bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 mb-6"
      >
        <span class="material-icons mr-2">add</span>
        Add Vendor
      </button>

      <!-- Vendor Table -->
      <div class="overflow-x-auto overflow-y-auto max-w-full max-h-[70vh] rounded shadow mb-6">
        <table class="min-w-full bg-white dark:bg-gray-800">
          <thead>
            <tr>
              <th class="py-2 px-4 border-b text-left text-gray-700 dark:text-gray-200">Name</th>
              <th class="py-2 px-4 border-b text-left text-gray-700 dark:text-gray-200">Contact Email</th>
              <th class="py-2 px-4 border-b text-left text-gray-700 dark:text-gray-200">Phone</th>
              <th class="py-2 px-4 border-b text-left text-gray-700 dark:text-gray-200">Address</th>
              <th class="py-2 px-4 border-b text-left text-gray-700 dark:text-gray-200">Vendor Type</th>
              <th class="py-2 px-4 border-b text-left text-gray-700 dark:text-gray-200">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="vendor in vendors" :key="vendor.uuid">
              <td class="py-2 px-4 border-b text-left text-gray-800 dark:text-gray-100">{{ vendor.name }}</td>
              <td class="py-2 px-4 border-b text-left text-gray-800 dark:text-gray-100">{{ vendor.contact_email }}</td>
              <td class="py-2 px-4 border-b text-left text-gray-800 dark:text-gray-100">{{ vendor.phone }}</td>
              <td class="py-2 px-4 border-b text-left text-gray-800 dark:text-gray-100">{{ vendor.address }}</td>
              <td class="py-2 px-4 border-b text-left capitalize text-gray-800 dark:text-gray-100">{{ vendor.vendor_type }}</td>
              <td class="py-2 px-4 border-b text-left">
                <button @click="editVendor(vendor)" class="text-blue-600 hover:text-blue-800 mr-2">
                  <span class="material-icons" style="font-size:20px;">edit</span>
                </button>
                <button @click="openDeleteModal(vendor.uuid)" class="text-red-600 hover:text-red-800">
                  <span class="material-icons" style="font-size:20px;">delete</span>
                </button>
              </td>
            </tr>
            <tr v-if="vendors.length === 0">
              <td colspan="6" class="py-4 text-center text-gray-500 dark:text-gray-400">No vendors found.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Add Vendor Modal -->
      <div v-if="showAddModal" class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
        <div class="bg-white dark:bg-gray-900 p-6 rounded shadow-lg w-full max-w-md">
          <h2 class="text-xl font-bold mb-4 text-gray-900 dark:text-gray-100">Add Vendor</h2>
          <form @submit.prevent="addVendor">
            <input v-model="newVendor.name" type="text" placeholder="Name" class="input-style mb-2" required />
            <input v-model="newVendor.contact_email" type="email" placeholder="Contact Email" class="input-style mb-2" />
            <input v-model="newVendor.phone" type="text" placeholder="Phone" class="input-style mb-2" />
            <input v-model="newVendor.address" type="text" placeholder="Address" class="input-style mb-2" />
            <select v-model="newVendor.vendor_type" class="input-style mb-4" required>
              <option value="" disabled>Select Vendor Type</option>
              <option value="freelancer">Freelancer</option>
              <option value="wholesaler">Wholesaler</option>
              <option value="organization">Organization</option>
            </select>
            <div class="flex justify-end space-x-2">
              <button type="button" @click="closeAddModal" class="px-4 py-2 bg-gray-300 dark:bg-gray-700 rounded hover:bg-gray-400 dark:hover:bg-gray-600 text-gray-900 dark:text-gray-100">Cancel</button>
              <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Add</button>
            </div>
          </form>
        </div>
      </div>

      <!-- Delete Vendor Modal -->
      <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
        <div class="bg-white dark:bg-gray-900 p-6 rounded shadow-lg w-full max-w-md">
          <h2 class="text-xl font-bold mb-4 text-gray-900 dark:text-gray-100">Delete Vendor</h2>
          <p class="mb-6 text-gray-700 dark:text-gray-300">
            Are you sure you want to delete this vendor?
          </p>
          <div class="flex justify-end space-x-2">
            <button type="button" @click="showDeleteModal = false"
              class="px-4 py-2 bg-gray-300 dark:bg-gray-700 rounded hover:bg-gray-400 dark:hover:bg-gray-600 text-gray-900 dark:text-gray-100">
              Cancel
            </button>
            <button type="button" @click="deleteVendor"
              class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
              Delete
            </button>
          </div>
        </div>
      </div>

      <!-- Edit Vendor Modal -->
      <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
        <div class="bg-white dark:bg-gray-900 p-6 rounded shadow-lg w-full max-w-md">
          <h2 class="text-xl font-bold mb-4 text-gray-900 dark:text-gray-100">Update Vendor</h2>
          <form @submit.prevent="updateVendor">
            <input v-model="editVendorData.name" type="text" placeholder="Name" class="input-style mb-2" required />
            <input v-model="editVendorData.contact_email" type="email" placeholder="Contact Email" class="input-style mb-2" />
            <input v-model="editVendorData.phone" type="text" placeholder="Phone" class="input-style mb-2" />
            <input v-model="editVendorData.address" type="text" placeholder="Address" class="input-style mb-2" />
            <select v-model="editVendorData.vendor_type" class="input-style mb-4" required>
              <option value="" disabled>Select Vendor Type</option>
              <option value="freelancer">Freelancer</option>
              <option value="wholesaler">Wholesaler</option>
              <option value="organization">Organization</option>
            </select>
            <div class="flex justify-end space-x-2">
              <button type="button" @click="closeEditModal" class="px-4 py-2 bg-gray-300 dark:bg-gray-700 rounded hover:bg-gray-400 dark:hover:bg-gray-600 text-gray-900 dark:text-gray-100">Cancel</button>
              <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Update</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../api";
export default {
  name: "UserVendors",
  data() {
    return {
      vendors: [],
      search: "",
      showAddModal: false,
      showEditModal: false,
      showDeleteModal: false,
      vendorToEdit: null,
      vendorToDelete: null,
      newVendor: {
        name: "",
        contact_email: "",
        phone: "",
        address: "",
        vendor_type: ""
      },
      editVendorData: {
        name: "",
        contact_email: "",
        phone: "",
        address: "",
        vendor_type: ""
      },
      isDark: false
    };
  },
  computed: {
    filteredVendors() {
      if (!this.search) return this.vendors;
      const term = this.search.toLowerCase();
      return this.vendors.filter(v =>
        (v.name && v.name.toLowerCase().includes(term)) ||
        (v.contact_email && v.contact_email.toLowerCase().includes(term)) ||
        (v.phone && v.phone.toLowerCase().includes(term)) ||
        (v.address && v.address.toLowerCase().includes(term)) ||
        (v.vendor_type && v.vendor_type.toLowerCase().includes(term))
      );
    }
  },
  methods: {
    openAddModal() { this.showAddModal = true; },
    closeAddModal() { this.showAddModal = false; },
    editVendor(vendor) { 
      this.vendorToEdit = vendor; 
      this.editVendorData = { ...vendor }; // Populate edit form with vendor data
      this.showEditModal = true; 
    },
    closeEditModal() { this.showEditModal = false; },
    openDeleteModal(uuid) { this.vendorToDelete = uuid; this.showDeleteModal = true; },
    async fetchVendors() {
      try {
        const res = await api.getVendors();
        this.vendors = res.data;
      } catch (err) {
        console.error("Failed to fetch vendors:", err);
      }
    },
    async addVendor() {
      try {
        await api.addVendor(this.newVendor);
        this.closeAddModal();
        this.newVendor = { name: "", contact_email: "", phone: "", address: "", vendor_type: "" };
        this.fetchVendors();
      } catch (err) {
        console.error("Failed to add vendor:", err);
      }
    },
    async updateVendor() {
      try {
        await api.updateVendor(this.vendorToEdit.uuid, this.editVendorData);
        this.closeEditModal();
        this.fetchVendors();
      } catch (err) {
        console.error("Failed to update vendor:", err);
      }
    },
    async deleteVendor() {
      try {
        await api.deleteVendor(this.vendorToDelete);
        this.showDeleteModal = false;
        this.vendorToDelete = null;
        this.fetchVendors();
      } catch (err) {
        console.error("Failed to delete vendor:", err);
      }
    },
    toggleDarkMode() {
      this.isDark = !this.isDark;
      document.documentElement.classList.toggle("dark", this.isDark);
    }
  },
  mounted() {
    this.fetchVendors();
  }
};
</script>

<style>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');
.input-style {
  @apply w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-gray-100;
}
</style>