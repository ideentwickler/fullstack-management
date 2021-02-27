import { IStore } from '@/interfaces';
import { UserState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';
import { ITicket } from '@/interfaces/ticket';

export const mutations = {
    setStores(state: UserState, payload: IStore[]) {
        state.stores = payload;
    },
    setStore(state: UserState, payload: IStore) {
        const stores = state.stores.filter((store: IStore) => store.id !== payload.id);
        stores.push(payload);
        state.stores = stores;
    },
    setTickets(state: UserState, payload: ITicket[]) {
        state.tickets = payload;
    },
    setTicket(state: UserState, payload: ITicket) {
        const tickets = state.tickets.filter((ticket: ITicket) => ticket.id !== payload.id);
        tickets.push(payload);
        state.tickets = tickets;
    },
};

const { commit } = getStoreAccessors<UserState, State>('');

export const commitSetStore = commit(mutations.setStore);
export const commitSetStores = commit(mutations.setStores);
export const commitSetTickets = commit(mutations.setTickets);
export const commitSetTicket = commit(mutations.setTicket);
