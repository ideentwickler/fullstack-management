import { UserState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';
import { ITicket } from '@/interfaces/ticket';

export const getters = {
    userStores: (state: UserState) => state.stores,
    userOneStore: (state: UserState) => (storeId: number) => {
        const filteredStores = state.stores.filter((store) => store.internal_id === storeId);
        if (filteredStores.length > 0) {
            return { ...filteredStores[0] };
        }
    },
    userSupportedStores: (state: UserState) => {
        const filteredStores = state.stores.filter((store) => store.support !== 0);
        if (filteredStores.length > 0) {
            return { ...filteredStores };
        }
    },
    userTickets: (state: UserState) => state.tickets,
    userOneTicket: (state: UserState) => (ticketId: number) => {
        const filteredTickets = state.tickets.filter((ticket: ITicket) => ticket.ticket_id === ticketId);
        if (filteredTickets.length > 0) {
            return { ...filteredTickets[0] };
        }
    },
};

const { read } = getStoreAccessors<UserState, State>('');

export const readUserOneStore = read(getters.userOneStore);
export const readUserStores = read(getters.userStores);
export const readUserSupportedStores = read(getters.userSupportedStores);
export const readUserTickets = read(getters.userTickets);
export const readUserOneTicket = read(getters.userOneTicket);
