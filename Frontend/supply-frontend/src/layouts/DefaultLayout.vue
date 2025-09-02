<template>
  <div class="min-h-screen flex flex-col bg-gray-100 dark:bg-gray-900 transition-colors">
    <!-- Top Navbar -->
    <Disclosure as="nav" class="bg-gray-800 dark:bg-gray-900 shadow-md">
      <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8 flex items-center justify-between h-16">
        <!-- Burger menu button on the left for mobile -->
        <button @click="sidebarOpen = !sidebarOpen" class="md:hidden text-gray-300 hover:text-white focus:outline-none mr-2">
          <span class="material-icons">menu</span>
        </button>
        <div class="flex items-center">
          <img class="h-8 w-auto" src="https://tailwindcss.com/plus-assets/img/logos/mark.svg?color=indigo&shade=500" alt="Supply Management" />
          <span class="ml-2 text-xl font-bold text-white">Supply Management</span>
        </div>
        <!-- Right controls (profile, notification, toggle) -->
        <div class="flex items-center space-x-2">
          <button type="button" class="relative rounded-full p-1 text-gray-400 hover:text-white">
            <span class="sr-only">View notifications</span>
            <BellIcon class="size-6" aria-hidden="true" />
          </button>
          <Menu as="div" class="relative ml-3">
            <MenuButton class="relative flex rounded-full">
              <span class="sr-only">Open user menu</span>
              <img class="size-8 rounded-full bg-gray-800 outline -outline-offset-1 outline-white/10" src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80" alt="" />
            </MenuButton>
            <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform scale-100" leave-to-class="transform opacity-0 scale-95">
              <MenuItems class="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-gray-800 py-1">
                <MenuItem v-slot="{ active }">
                  <a href="#" :class="[active ? 'bg-white/5' : '', 'block px-4 py-2 text-sm text-gray-300']">Your profile</a>
                </MenuItem>
                <MenuItem v-slot="{ active }">
                  <a href="#" :class="[active ? 'bg-white/5' : '', 'block px-4 py-2 text-sm text-gray-300']">Settings</a>
                </MenuItem>
                <MenuItem v-slot="{ active }">
                  <a href="#" :class="[active ? 'bg-white/5' : '', 'block px-4 py-2 text-sm text-gray-300']" @click="$emit('logout')">Sign out</a>
                </MenuItem>
              </MenuItems>
            </transition>
          </Menu>
          <button @click="$emit('toggle-dark')" class="ml-2 p-2 rounded-full bg-gray-700 hover:bg-gray-600">
            <span v-if="!isDark">🌙</span>
            <span v-else>☀️</span>
          </button>
        </div>
      </div>
    </Disclosure>
    <!-- Sidebar and Main Content -->
    <div class="flex flex-1">
      <!-- Sidebar for desktop -->
      <aside class="hidden md:flex flex-col w-64 bg-gray-800 dark:bg-gray-900 shadow-lg pt-6">
        <nav class="flex-1 px-4 space-y-2">
          <router-link to="/dashboard" class="flex items-center px-3 py-2 rounded-md text-gray-300 hover:bg-gray-700 hover:text-white text-base font-medium">
            <span class="material-icons mr-2">dashboard</span>
            Dashboard
          </router-link>
          <router-link to="/warehouses" class="flex items-center px-3 py-2 rounded-md text-gray-300 hover:bg-gray-700 hover:text-white text-base font-medium">
            <span class="material-icons mr-2">store</span>
            Warehouses
          </router-link>
          <router-link to="/products" class="flex items-center px-3 py-2 rounded-md text-gray-300 hover:bg-gray-700 hover:text-white text-base font-medium">
            <span class="material-icons mr-2">inventory_2</span>
            Products
          </router-link>
          <router-link to="/vendors" class="flex items-center px-3 py-2 rounded-md text-gray-300 hover:bg-gray-700 hover:text-white text-base font-medium">
            <span class="material-icons mr-2">business</span>
            Vendors
          </router-link>
          <router-link to="/stock" class="flex items-center px-3 py-2 rounded-md text-gray-300 hover:bg-gray-700 hover:text-white text-base font-medium">
            <span class="material-icons mr-2">layers</span>
            Stock
          </router-link>
          <router-link to="/stock-transfers" class="flex items-center px-3 py-2 rounded-md text-gray-300 hover:bg-gray-700 hover:text-white text-base font-medium">
            <span class="material-icons mr-2">swap_horiz</span>
            Stock Transfers
          </router-link>
          <router-link to="/users" class="flex items-center px-3 py-2 rounded-md text-gray-300 hover:bg-gray-700 hover:text-white text-base font-medium">
            <span class="material-icons mr-2">people</span>
            Users
          </router-link>
          <router-link to="/reports" class="flex items-center px-3 py-2 rounded-md text-gray-300 hover:bg-gray-700 hover:text-white text-base font-medium">
            <span class="material-icons mr-2">bar_chart</span>
            Reports
          </router-link>
        </nav>
      </aside>
      <!-- Sidebar for mobile -->
      <transition name="slide">
        <aside v-if="sidebarOpen" class="fixed inset-0 z-40 flex md:hidden">
          <div class="fixed inset-0 bg-black bg-opacity-50" @click="sidebarOpen = false"></div>
          <div class="relative flex flex-col w-64 bg-gray-800 dark:bg-gray-900 shadow-lg pt-6">
            <nav class="flex-1 px-4 space-y-2">
              <router-link to="/dashboard" class="flex items-center px-3 py-2 rounded-md text-gray-300 hover:bg-gray-700 hover:text-white text-base font-medium">
                <span class="material-icons mr-2">dashboard</span>
                Dashboard
              </router-link>
              <router-link to="/warehouses" class="flex items-center px-3 py-2 rounded-md text-gray-300 hover:bg-gray-700 hover:text-white text-base font-medium">
                <span class="material-icons mr-2">store</span>
                Warehouses
              </router-link>
              <router-link to="/products" class="flex items-center px-3 py-2 rounded-md text-gray-300 hover:bg-gray-700 hover:text-white text-base font-medium">
                <span class="material-icons mr-2">inventory_2</span>
                Products
              </router-link>
              <router-link to="/vendors" class="flex items-center px-3 py-2 rounded-md text-gray-300 hover:bg-gray-700 hover:text-white text-base font-medium">
                <span class="material-icons mr-2">business</span>
                Vendors
              </router-link>
              <router-link to="/stock" class="flex items-center px-3 py-2 rounded-md text-gray-300 hover:bg-gray-700 hover:text-white text-base font-medium">
                <span class="material-icons mr-2">layers</span>
                Stock
              </router-link>
              <router-link to="/stock-transfers" class="flex items-center px-3 py-2 rounded-md text-gray-300 hover:bg-gray-700 hover:text-white text-base font-medium">
                <span class="material-icons mr-2">swap_horiz</span>
                Stock Transfers
              </router-link>
              <router-link to="/users" class="flex items-center px-3 py-2 rounded-md text-gray-300 hover:bg-gray-700 hover:text-white text-base font-medium">
                <span class="material-icons mr-2">people</span>
                Users
              </router-link>
              <router-link to="/reports" class="flex items-center px-3 py-2 rounded-md text-gray-300 hover:bg-gray-700 hover:text-white text-base font-medium">
                <span class="material-icons mr-2">bar_chart</span>
                Reports
              </router-link>
            </nav>
            <button class="absolute top-2 right-2 text-gray-400 hover:text-white" @click="sidebarOpen = false">
              <span class="material-icons">close</span>
            </button>
          </div>
        </aside>
      </transition>
      <!-- Main Content -->
      <main class="flex-1 container mx-auto p-6">
        <slot />
      </main>
    </div>
    <!-- Transfluent Footer -->
    <footer class="bg-gray-900/70 dark:bg-gray-800/70 backdrop-blur-md text-gray-400 text-center p-4 rounded-t-xl shadow-lg">
      &copy; 2025 Supply Management. All rights reserved.
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Disclosure, Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { BellIcon } from '@heroicons/vue/24/outline'
const sidebarOpen = ref(false)
</script>

<style>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');
.slide-enter-active, .slide-leave-active {
  transition: transform 0.3s;
}
.slide-enter-from, .slide-leave-to {
  transform: translateX(-100%);
}
</style>
