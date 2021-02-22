export interface IUserProfile {
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    first_name: string;
    last_name: string;
    id: number;
}

export interface IUserProfileUpdate {
    email?: string;
    first_name?: string;
    last_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IUserProfileCreate {
    email: string;
    first_name: string;
    last_name: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IStore {
    id: number;
    support: number;
    internal_id: number;
    name: string;
}

export interface IStoreCreate {
    support: number;
    internal_id: number;
    name: string;
}

export interface IStoreUpdate {
    support?: number;
    internal_id?: number;
    name?: string;
}

export interface IReportingFileCreate {
    year: string | number;
    month_start: string | number;
    month_end: string | number;
    stores: number[] | string[];
    title: string;
    email_reciepent?: string;
    filename?: string;
}
