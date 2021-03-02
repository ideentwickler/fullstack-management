export interface IClaim {
    contract_nr: number;
    bill: number;
    discharge: number;
    kind: any;
    ticket_id: number;
    owner_id: number;
    store_internal_id: number;
    created_at: string;
    updated_at?: string;
}
