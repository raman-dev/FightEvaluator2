<script setup>
const props = ['likelihood','likelihood_val','justification','fighter'];
</script>

<template>
    <td>
        <div>
            <div class="likelihood likelihood-{{ props.likelihood_val }}">
                <span>
                    {{ props.likelihood }}</span>
            </div>
            <p class="justification">
                {{ props.justification }}
            </p>
        </div>
    </td>
</template>