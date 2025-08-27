<script setup>
const props = defineProps(['optionState', 'selected', 'state', 'description'])

</script>

<template>
    <div class="attrib-option" :data-option-state="props.optionState" :selected="props.selected ? true : null">
        <h5 class="option">{{ props.state }}</h5>
        <p class="description">{{ props.description }}</p>
    </div>
</template>

<style lang="scss" scoped>
$positiveBg: #0d6efd;
$negativeBg: #dc3545;
$neutralBg: #ffc107;
$outlineColor : #3d7efd;

$optionPadding: 0.8rem;
$borderRadius: 0.5rem;

p {
    margin: 0px;
}

.attrib-option {
    display: flex;
    align-items: center;

    // padding: $optionPadding;
    margin: $optionPadding;
    cursor: pointer;

    font-family: PoppinsSemiBold;
    text-transform: uppercase;

    .option {
        margin: 0px;
        margin-right: 0.5rem;
        padding: $optionPadding;

        border-radius: $borderRadius;
        border: 2px solid lavender;
    }

    .description {
        padding: $optionPadding;
        border-radius: $borderRadius;
        border: 2px solid lavender;
        text-transform: capitalize;
    }
}

.attrib-option[data-option-state="positive"] {

    .option,
    .description {
        border-color: $positiveBg;
    }

    .option {
        color: $positiveBg;
    }
}

.attrib-option[data-option-state="neutral"] {

    .option,
    .description {
        border-color: $neutralBg;
    }

    .option {
        color: $neutralBg;
    }
}

.attrib-option[data-option-state="negative"] {

    .option,
    .description {
        border-color: $negativeBg;
    }

    .option {
        color: $negativeBg;
    }
}

.attrib-option[data-option-state="positive"][selected] {
    border-color: whitesmoke;
    color: whitesmoke;
    background-color: $positiveBg;
}

.attrib-option[data-option-state="neutral"][selected] {
    border-color: whitesmoke;
    color: whitesmoke;
    background-color: $neutralBg;
}

.attrib-option[data-option-state="negative"][selected] {
    border-color: whitesmoke;
    color: whitesmoke;
    background-color: $negativeBg;
}

.attrib-option[selected] {
    border-color: whitesmoke;
    color: whitesmoke;

    .option {
        border-color: whitesmoke;
        color: whitesmoke;
    }
}

.attrib-option[data-option-state="untested"] {
    display: none;
}
</style>