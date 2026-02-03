<script setup lang="ts">
import type { components } from "#open-fetch-schemas/backend";

const props = defineProps<{
  wishlistUuid: string;
}>();

const overlay = useOverlay();

const priorityNames: {
  label: string;
  value: components["schemas"]["Priority"];
}[] = [
  { label: "Low", value: 1 },
  { label: "Medium", value: 2 },
  { label: "High", value: 3 },
];

const measurementUnits: components["schemas"]["MeasurementUnit"][] = [
  "piece",
  "meter",
  "kg.",
];

const itemName = ref("");
const itemQuantity = ref(1);
const itemMeasurement = ref<components["schemas"]["MeasurementUnit"]>("piece");
const itemPriority = ref<components["schemas"]["Priority"]>(1);

const createNewItem = async () => {
  await useBackend("/wishlists/add-item/{wishlist_uuid}", {
    method: "POST",
    path: {
      wishlist_uuid: props.wishlistUuid,
    },
    body: {
      name: itemName.value,
      quantity: itemQuantity.value,
      measurement_unit: itemMeasurement.value,
      priority: itemPriority.value,
    },
  });
  overlay.closeAll();
  reloadNuxtApp();
};
</script>

<template>
  <UModal>
    <template #content>
      <UCard>
        <div class="space-y-4">
          <div>Creating new item...</div>

          <UInput block v-model="itemName" placeholder="New item name" />

          <UInput block v-model="itemQuantity" placeholder="Quantity" />

          <USelect
            block
            v-model="itemMeasurement"
            placeholder="Measurement unit"
            :items="measurementUnits"
          />

          <USelect
            block
            v-model="itemPriority"
            placeholder="Priority"
            option-attribute="name"
            :items="priorityNames"
          />

          <UButton block @click="createNewItem"> Create new item </UButton>
        </div>
      </UCard></template
    >
  </UModal>
</template>
