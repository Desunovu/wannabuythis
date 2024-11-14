<template>
  <div
    class="container mx-auto p-6 flex flex-col items-center justify-center h-screen bg-cover bg-center relative"
    style="
      background-image: linear-gradient(
          to bottom,
          rgba(0, 0, 0, 0.6),
          rgba(0, 0, 0, 0.9)
        ),
        url('/img/background.jpg');
    "
  >
    <div class="relative z-10 text-center text-white drop-shadow-lg">
      <h1 class="text-4xl md:text-5xl font-semibold mb-6 tracking-wide">
        Manage and share your wishlist easily
      </h1>

      <p
        class="text-lg md:text-xl text-gray-300 mb-8 max-w-xl mx-auto leading-relaxed"
      >
        Wannabuythis helps you organize your wishlist and track your purchase
        priorities. Share your list with others and keep everything in one
        place.
      </p>

      <UButton
        class="px-8 py-3 text-lg bg-green-500 hover:bg-green-600 text-white rounded-lg shadow-md"
        to="/login"
      >
        Get Started
      </UButton>
    </div>
  </div>
</template>
