<script setup>
const isPrelim = defineModel('isPrelim',{default:false,required:true})
</script>
<template>
    <!--prelim status-->
    <div class="isprelim-checkbox border rounded-2 p-1 px-3">
        <div class="form-check">
            <input class="form-check-input" type="checkbox" v-model="isPrelim" name="isprelim" id="isprelim-checkbox" checked="">
            <label class="form-check-label" for="isprelim-checkbox">
                on prelims
            </label>
        </div>
    </div>
</template>