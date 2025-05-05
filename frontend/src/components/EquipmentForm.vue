<template>
  <el-form :model="form" :rules="rules" ref="formRef">
    <el-form-item label="Тип оборудования" prop="equipment_type_id">
      <el-select v-model="form.equipment_type_id" placeholder="Выберите тип">
        <el-option v-for="type in types" :key="type.id" :label="type.name" :value="type.id" />
      </el-select>
    </el-form-item>
    <el-form-item label="Серийные номера" prop="serial_numbers">
      <el-input
        type="textarea"
        v-model="form.serial_numbers"
        placeholder="Один или несколько SN, каждый с новой строки"
      />
    </el-form-item>
    <el-form-item label="Примечание" prop="note">
      <el-input type="textarea" v-model="form.note" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit">Добавить</el-button>
    </el-form-item>
    <el-alert v-if="errors.length" type="error" show-icon>
      <div v-for="err in errors" :key="err.serial_number">
        SN: {{ err.serial_number }} - {{ err.error }}
      </div>
    </el-alert>
  </el-form>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import api from "../api";
const emit = defineEmits(["added"]);

const form = ref({
  equipment_type_id: null,
  serial_numbers: "",
  note: "",
});
const types = ref([]);
const errors = ref([]);

const rules = {
  equipment_type_id: [{ required: true, message: "Обязательное поле", trigger: "blur" }],
  serial_numbers: [{ required: true, message: "Обязательное поле", trigger: "blur" }],
};

const formRef = ref();

async function fetchTypes() {
  const { data } = await api.get("equipment-type/");
  types.value = data.results || data;
}

onMounted(fetchTypes);

async function onSubmit() {
  await formRef.value.validate();
  errors.value = [];
  const serialNumbers = form.value.serial_numbers
    .split("\n")
    .map((sn) => sn.trim())
    .filter(Boolean);
  try {
    const { data } = await api.post("equipment/", {
      equipment_type_id: form.value.equipment_type_id,
      serial_numbers: serialNumbers,
      note: form.value.note,
    });
    if (data.errors && data.errors.length) {
      errors.value = data.errors;
    } else {
      emit("added");
      form.value.serial_numbers = "";
      form.value.note = "";
    }
  } catch (e) {
    if (e.response && e.response.data && e.response.data.errors) {
      errors.value = e.response.data.errors;
    }
  }
}
</script>
