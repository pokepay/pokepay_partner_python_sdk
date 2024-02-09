// DO NOT EDIT: File is generated by code generator.

import { Request, Method } from "./Request";
import { PaginatedAccountWithUsers } from "../response/PaginatedAccountWithUsers";

class GetCustomerAccounts implements Request<PaginatedAccountWithUsers> {
  public readonly __r: PaginatedAccountWithUsers | undefined;
  public readonly method: Method = "GET";
  public readonly path: string;
  public readonly bodyParams: {
    private_money_id: string,
    page?: number,
    per_page?: number,
    created_at_from?: string,
    created_at_to?: string,
    is_suspended?: boolean,
    status?: string,
    external_id?: string,
    tel?: string,
    email?: string
  };
  public constructor(params: {
    private_money_id: string,
    page?: number,
    per_page?: number,
    created_at_from?: string,
    created_at_to?: string,
    is_suspended?: boolean,
    status?: string,
    external_id?: string,
    tel?: string,
    email?: string
  }) {
    if (params.private_money_id === void 0) throw new Error('"private_money_id" is required');
    this.path = "/accounts" + "/customers";
    this.bodyParams = {
      private_money_id: params.private_money_id,
    };
    if (params.page !== void 0) this.bodyParams.page = params.page;
    if (params.per_page !== void 0) this.bodyParams.per_page = params.per_page;
    if (params.created_at_from !== void 0) this.bodyParams.created_at_from = params.created_at_from;
    if (params.created_at_to !== void 0) this.bodyParams.created_at_to = params.created_at_to;
    if (params.is_suspended !== void 0) this.bodyParams.is_suspended = params.is_suspended;
    if (params.status !== void 0) this.bodyParams.status = params.status;
    if (params.external_id !== void 0) this.bodyParams.external_id = params.external_id;
    if (params.tel !== void 0) this.bodyParams.tel = params.tel;
    if (params.email !== void 0) this.bodyParams.email = params.email;
  }
}

export { GetCustomerAccounts };