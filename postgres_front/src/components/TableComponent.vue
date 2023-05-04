<template>
    <table v-if="dataColumns != null" class="table table-output">
        <thead>
            <tr>
                <th class="table-output" scope="col">#</th>
                <th scope="col" v-for="(column, index) in dataColumns" :key="index">
                    {{ column }}
                </th>
            </tr>
        </thead>

        <tbody>
            <tr v-for="element in dataResults" v-bind:key="element.id">
                <td scope="col">{{ element.id }}</td>
                <td scope="col" v-for="raw_element in element.data" v-bind:key="raw_element">
                    {{ raw_element }}
                </td>
            </tr>
        </tbody>
    </table>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'
import type PostgresResultResponse from '@/types/PostgreResultResponse'

export default defineComponent({
    props: {
        dataResults: {
            required: true,
            type: Array as PropType<PostgresResultResponse[]>
        },
        dataColumns: {
            required: true,
            type: null as unknown as PropType<string[] | null>
        }
    }
})
</script>

<style>
.table-output {
    color: #fff;
}
</style>
