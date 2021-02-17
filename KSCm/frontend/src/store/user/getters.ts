import { UserState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const getters = {
    userStores: (state: UserState) => state.stores,
    userOneStore: (state: UserState) => (storeId: number) => {
        const filteredStores = state.stores.filter((store) => store.internal_id === storeId);
        if (filteredStores.length > 0) {
            return { ...filteredStores[0] };
        }
    },
};

const { read } = getStoreAccessors<UserState, State>('');

export const readUserOneStore = read(getters.userOneStore);
export const readUserStores = read(getters.userStores);
