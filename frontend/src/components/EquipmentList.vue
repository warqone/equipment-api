<template>
  <el-input v-model="search" placeholder="Поиск по SN или примечанию" @input="fetchList" />
  <el-table :data="list" style="width: 100%">
    <el-table-column prop="equipment_type.name" label="Тип оборудования" />
    <el-table-column prop="serial_number" label="Серийный номер" />
    <el-table-column prop="note" label="Примечание" />
    <el-table-column label="Действия">
      <template #default="scope">
        <el-button size="small" @click="editRow(scope.row)">Редактировать</el-button>
        <el-button size="small" type="danger" @click="deleteRow(scope.row)">Удалить</el-button>
      </template>
    </el-table-column>
  </el-table>
  <el-pagination
    :current-page="page"
    :page-size="10"
    :total="total"
    @current-change="handlePage"
    layout="prev, pager, next"
  />
  <el-dialog v-model="editDialog" title="Редактировать">
    <el-form :model="editForm">
      <el-form-item label="Примечание">
        <el-input v-model="editForm.note" />
      </el-form-item>
      <!-- Можно добавить редактирование других полей -->
      <el-button type="primary" @click="saveEdit">Сохранить</el-button>
    </el-form>
  </el-dialog>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../api";

const list = ref([]);
const total = ref(0);
const page = ref(1);
const search = ref("");
const editDialog = ref(false);
const editForm = ref({});
let lastQuery = "";

async function fetchList() {
  const params = { page: page.value };
  if (search.value) params.search = search.value;
  lastQuery = search.value;
  const { data } = await api.get("equipment/", { params });
  list.value = data.results || data;
  total.value = data.count || list.value.length;
}
onMounted(fetchList);

function handlePage(newPage) {
  page.value = newPage;
  fetchList();
}

function editRow(row) {
  editForm.value = { ...row };
  editDialog.value = true;
}

async function saveEdit() {
  await api.put(`equipment/${editForm.value.id}/`, {
    note: editForm.value.note,
    equipment_type_id: editForm.value.equipment_type.id,
    serial_number: editForm.value.serial_number,
  });
  editDialog.value = false;
  fetchList();
}

async function deleteRow(row) {
  await api.delete(`equipment/${row.id}/`);
  fetchList();
}
</script>
