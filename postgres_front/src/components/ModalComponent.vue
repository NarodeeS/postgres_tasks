<template>
    <div
        class="modal fad"
        id="forceCloseModal"
        tabindex="-1"
        aria-labelledby="exampleModalLabel"
        aria-hidden="true"
    >
        <div class="modal-dialog custom-modal">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Вы уверены ?</h1>
                </div>
                <div class="modal-body">
                    Вы хотите прервать задание ? Это действие нельзя будет отменить
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-warning" data-bs-dismiss="modal">
                        Отмена
                    </button>
                    <button
                        type="button"
                        class="btn btn-outline-danger"
                        data-bs-dismiss="modal"
                        @click="$emit('end_task')"
                    >
                        Закончить задание
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
    emits: {
        end_task: () => true
    },
    setup() {
        return {}
    }
})
</script>
<style>
.modal-content {
    background-color: var(--light-grey-color);
    color: var(--white-color);
    border: none;
    border-radius: 3px;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
}
</style>
