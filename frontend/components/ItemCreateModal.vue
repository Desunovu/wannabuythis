<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";

const props = defineProps<{
  wishlistUuid: string;
}>();

const modal = useModal();

const priorityNames: {
  name: string;
  value: components["schemas"]["Priority"];
}[] = [
  { name: "Low", value: 1 },
  { name: "Medium", value: 2 },
  { name: "High", value: 3 },
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

  modal.close();
};
</script>

<template>
  <UModal>
    <UCard>
      <div class="space-y-4">
        <div>Creating new item...</div>

        <UInput block v-model="itemName" placeholder="New item name" />

        <UInput block v-model="itemQuantity" placeholder="Quantity" />

        <USelect
          block
          v-model="itemMeasurement"
          placeholder="Measurement unit"
          :options="measurementUnits"
        />

        <USelect
          block
          v-model="itemPriority"
          placeholder="Priority"
          option-attribute="name"
          :options="priorityNames"
        />
        
        <UButton block @click="createNewItem"> Create new item </UButton>
      </div>
    </UCard>
  </UModal>
</template>
