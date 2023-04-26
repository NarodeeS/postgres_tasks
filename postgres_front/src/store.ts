// store.ts
import { InjectionKey } from 'vue'
import { createStore, Store } from 'vuex'
import AccautForm from './types/AccoutForm'

export interface State {
  email: string,
  password: string
}
  // define injection key
  export const key: InjectionKey<Store<State>> = Symbol()
  
  export const store = createStore<State>({
    state: <State>{
      email: '',
      password: '',
    },
    mutations: {
      updatAaccountForRegistratioA(state, new_form: AccautForm){
        state.email = new_form.email
        state.password = new_form.password
      },

    },
    getters: {
      email(state) {
          return state.email;
      },
      password(state) {
        return state.password;
    },
  }
  })