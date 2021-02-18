import { api } from '@/api';
import { ActionContext } from 'vuex';
import { State } from '../state';
import { UserState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { commitSetStores, commitSetStore } from './mutations';
import { dispatchCheckApiError } from '../main/actions';
import {IReportingFileCreate, IStoreCreate, IStoreUpdate} from '@/interfaces';
import {commitAddNotification, commitRemoveNotification} from '@/store/main/mutations';

type MainContext = ActionContext<UserState, State>;

export const actions = {
    async actionGetFile(context: MainContext, payload: IReportingFileCreate) {
       try {
            const response = await api.createReportingFile(context.rootState.main.token, payload);
            if (response) {
                return response.data;
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionGetStores(context: MainContext) {
        try {
            const response = await api.getStores(context.rootState.main.token);
            if (response) {
                commitSetStores(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionUpdateStore(context: MainContext, payload: {id: number, store: IStoreUpdate}) {
        try {
            const loadingNotification = {content: 'saving', showProgress: true};
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.updateStore(context.rootState.main.token, payload.id, payload.store),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitSetStore(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, {content: 'Store successfully updated', color: 'success'});
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionCreateStore(context: MainContext, payload: IStoreCreate) {
        try {
            const loadingNotification = {content: 'saving', showProgress: true};
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.createStore(context.rootState.main.token, payload),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitSetStore(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, {content: 'Store successfully created', color: 'success'});
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
};

const { dispatch } = getStoreAccessors<UserState, State>('');

export const dispatchGetStores = dispatch(actions.actionGetStores);
export const dispatchUpdateStore = dispatch(actions.actionUpdateStore);
export const dispatchCreateStore = dispatch(actions.actionCreateStore);
export const dispatchGetFile = dispatch(actions.actionGetFile);
