<template>
  <equipment-form @added="fetchList" />
  <equipment-list ref="listRef" />
</template>

<script setup>
import EquipmentForm from "../components/EquipmentForm.vue";
import EquipmentList from "../components/EquipmentList.vue";
import { ref } from "vue";

const listRef = ref();

function fetchList() {
  listRef.value.fetchList();
}
</script>
