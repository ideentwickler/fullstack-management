import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { UserState } from './state';

const defaultState: UserState = {
  stores: [],
  tickets: [],
};

export const userModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
