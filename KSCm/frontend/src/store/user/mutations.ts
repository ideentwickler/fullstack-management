import { IStore } from '@/interfaces';
import { UserState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const mutations = {
    setStores(state: UserState, payload: IStore[]) {
        state.stores = payload;
    },
    setStore(state: UserState, payload: IStore) {
        const stores = state.stores.filter((store: IStore) => store.id !== payload.id);
        stores.push(payload);
        state.stores = stores;
    },
};

const { commit } = getStoreAccessors<UserState, State>('');

export const commitSetStore = commit(mutations.setStore);
export const commitSetStores = commit(mutations.setStores);
