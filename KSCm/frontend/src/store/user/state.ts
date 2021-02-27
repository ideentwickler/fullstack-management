import { IStore } from '@/interfaces';
import {ITicket} from '@/interfaces/ticket';

export interface UserState {
    stores: IStore[];
    tickets: ITicket[];
}
