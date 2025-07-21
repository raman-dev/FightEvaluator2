<script setup>
    
const props = defineProps(['tableName','columns']);

</script>
<template>
    <div class="table-container border">
        <table class="table">
            <caption style="caption-side:top">
                <div class="d-flex justify-content-between">
                  <h4 style="text-transform: capitalize;">{{props.tableName}}</h4>
                  <div class="action-wrapper">
                    <button type="button" class="btn btn-primary">
                      add
                    </button>
                  </div>
                </div>
            </caption>
            <thead>
                <tr>
                    <template v-for="col in columns">
                        <th>{{ col }}</th>
                    </template>
                </tr>
            </thead>
            <tbody>

            </tbody>
        </table>
    </div>
</template>