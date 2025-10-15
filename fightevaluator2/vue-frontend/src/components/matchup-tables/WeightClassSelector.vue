<script setup>
const weightClass = defineModel('weightClass', {
    type: String,
    required: false,
    default: ''
});
</script>
<template>
    <!--weight class-->
    <div class="weightclass-selector my-4">
        <div class="weightclass input-group mb-3">
            <label class="input-group-text" for="weight-class-select">Weightclass</label>
            <select class="form-select" id="weight-class-select" name="weight_class" v-model="weightClass">
                <option selected="" value="">Choose a weight class...</option>
                <option value="strawweight">Strawweight</option>
                <option value="flyweight">Flyweight</option>
                <option value="bantamweight">Bantamweight</option>
                <option value="featherweight">Featherweight</option>
                <option value="lightweight">Lightweight</option>
                <option value="welterweight">Welterweight</option>
                <option value="middleweight">Middleweight</option>
                <option value="light_heavyweight">Light Heavyweight</option>
                <option value="heavyweight">Heavyweight</option>
            </select>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.weightclass-selector {
    width: fit-content;
  }
</style>